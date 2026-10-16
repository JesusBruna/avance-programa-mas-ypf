"""Genera un informe HTML por estación (para imprimir a PDF) y el texto de mail sugerido.

Uso: python3 informes_por_estacion.py <avance.csv> <carpeta_salida> [notas.json]
Luego: NODE_PATH=$(npm root -g) node html_a_pdf.js <carpeta_salida>
"""
import calendar
import csv
import collections
import html
import os
import sys

NOMBRE = {
    "diesel_m3": "Volumen diesel (Infinia Diesel + D500)",
    "naftas_m3": "Volumen naftas (Infinia + Súper)",
    "mix_naftas": "Mix Infinia en naftas",
    "mix_go": "Mix Infinia Diesel en gasoil",
    "lubricantes_m3": "Volumen lubricantes",
    "croselling": "Croselling (tienda)",
    "comidas_un": "Unidades Comidas y Café",
    "app_ypf": "Penetración App YPF",
    "cliente_incognito": "Cliente incógnito",
    "auditoria_imagen": "Auditoría de imagen",
}
UNIDAD = {"diesel_m3": "m3", "naftas_m3": "m3", "lubricantes_m3": "m3", "comidas_un": "un."}
VOLUMEN = set(UNIDAD)
CORTO = {"diesel_m3": "Diesel", "naftas_m3": "Naftas", "mix_naftas": "Mix Infinia naftas", "mix_go": "Mix Infinia Diesel",
         "lubricantes_m3": "Lubricantes", "croselling": "Croselling", "comidas_un": "Comidas y Café",
         "app_ypf": "App YPF", "cliente_incognito": "Cliente incógnito", "auditoria_imagen": "Auditoría de imagen"}
MESES = ["", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto",
         "Septiembre", "Octubre", "Noviembre", "Diciembre"]

# Observaciones puntuales por estación (las que no salen de reglas automáticas).
# Se cargan desde un JSON opcional: {"notas": {"931": {"gestion": [...], "foco": [...]}}, ...}
NOTAS = {}


def f(x):
    return float(x) if x not in ("", None) else None


def fmt(v, c, dec=None):
    if v is None:
        return "--"
    if c in ("comidas_un",):
        return f"{v:,.0f}".replace(",", ".")
    if c in VOLUMEN:
        d = 2 if c == "lubricantes_m3" else 1
        return f"{v:.{d}f}".replace(".", ",")
    return f"{v:.1f} %".replace(".", ",")


def evaluar(r, dias_mes):
    """Devuelve (estado, texto) para la tabla y listas de bullets."""
    c = r["concepto"]
    mn, mx, real, proy = f(r["obj_min"]), f(r["obj_max"]), f(r["real"]), f(r["proyeccion"])
    if c in ("cliente_incognito", "auditoria_imagen"):
        return "pend", "Pendiente de evaluación"
    if mn is None and real is None:
        return "sinobj", "Sin objetivo asignado"
    if mn is None:
        return "sinobj", "Sin objetivo asignado"
    if real is None:
        return "sindato", "Sin dato registrado"
    if c in VOLUMEN:
        pct = proy / mn * 100
        if proy >= mx:
            return "ok", f"Proyecta {pct:.0f} % del mínimo (supera el máximo)"
        if proy >= mn:
            return "ok" if pct >= 103 else "justo", f"Proyecta {pct:.0f} % del mínimo"
        return ("justo" if pct >= 97 else "riesgo"), f"Proyecta {pct:.0f} % del mínimo"
    if real >= mx:
        return "ok", "En el máximo"
    if real >= mn:
        return "ok", "Cumple el mínimo"
    brecha = mn - real
    return ("justo" if brecha <= 1 else "riesgo"), f"Faltan {brecha:.1f} pp".replace(".", ",")


def bullets(rs, dias_mes):
    bien, foco, gestion = [], [], []
    for r in rs:
        c = r["concepto"]
        estado, _ = evaluar(r, dias_mes)
        n = NOMBRE[c]
        mn, real, proy = f(r["obj_min"]), f(r["real"]), f(r["proyeccion"])
        if estado == "ok":
            if c in VOLUMEN:
                bien.append(f"{n}: al ritmo actual cerraría en ~{fmt(proy, c)} {UNIDAD[c]} (mínimo {fmt(mn, c)}).")
            else:
                bien.append(f"{n}: {fmt(real, c)} (mínimo {fmt(mn, c)}).")
        elif estado in ("justo", "riesgo"):
            if c in VOLUMEN:
                dias = int(r["dias"])
                falta = mn - real
                nec = falta / (dias_mes - dias)
                act = real / dias
                u = UNIDAD[c]
                d = 0 if c == "comidas_un" else (3 if c == "lubricantes_m3" else 1)
                es = lambda v: f"{v:.{d}f}".replace(".", ",")
                s = (f"{n}: llevan {fmt(real, c)} {u}; faltan {fmt(falta, c)} {u} para el mínimo. "
                     f"Necesitan ~{es(nec)} {u}/día (hoy venden ~{es(act)} {u}/día).")
                if estado == "justo":
                    s += " Está al límite: se define en los últimos días."
                foco.append(s)
            else:
                brecha = mn - real
                s = f"{n}: {fmt(real, c)} vs mínimo {fmt(mn, c)} (faltan {brecha:.1f} pp".replace(".", ",") + ")."
                if brecha <= 1:
                    s += " Muy cerca: son puntos accesibles."
                foco.append(s)
        elif estado == "sinobj" and c != "mix_go":
            gestion.append(f"{n}: no tiene objetivo asignado, por lo que hoy esos {int(f(r['puntos_posibles']))} pts no se pueden sumar. Lo estamos gestionando con YPF.")
        elif estado == "sindato":
            gestion.append(f"{n}: tiene objetivo ({fmt(mn, c)}{(' ' + UNIDAD[c]) if c in UNIDAD else ''}) pero no se registra venta en el tablero. "
                           "Por favor confirmen si hubo ventas/compras en el mes para revisar la carga del dato.")
    return bien, foco, gestion


CSS = """
@page { size: A4; margin: 11mm 13mm; }
* { box-sizing: border-box; }
body { font-family: 'DejaVu Sans', 'Liberation Sans', Arial, sans-serif; color: #1c2330; font-size: 9.6pt; margin: 0; }
.head { background: #0a3d91; color: #fff; padding: 14px 18px; border-radius: 6px; display: flex; justify-content: space-between; align-items: center; }
.head h1 { font-size: 17pt; margin: 0; }
.head .sub { font-size: 9.5pt; opacity: .85; margin-top: 3px; }
.head .prog { text-align: right; font-weight: 700; font-size: 11pt; letter-spacing: .5px; }
.kpis { display: flex; gap: 10px; margin: 12px 0; }
.kpi { flex: 1; border: 1px solid #d5dbe6; border-radius: 6px; padding: 9px 12px; }
.kpi .v { font-size: 16pt; font-weight: 700; color: #0a3d91; }
.kpi .l { font-size: 8.5pt; color: #5a6578; }
h2 { font-size: 11.5pt; color: #0a3d91; border-bottom: 2px solid #0a3d91; padding-bottom: 3px; margin: 14px 0 7px; }
table { width: 100%; border-collapse: collapse; font-size: 9pt; }
th { background: #eef2f8; text-align: left; padding: 5px 6px; font-weight: 600; color: #34405a; }
td { padding: 4px 6px; border-bottom: 1px solid #e6eaf1; }
td.n { text-align: right; white-space: nowrap; }
.chip { display: inline-block; padding: 2px 7px; border-radius: 10px; font-size: 8pt; font-weight: 600; white-space: nowrap; }
.ok { background: #dff3e4; color: #17642f; }
.justo { background: #fff1cc; color: #7a5a00; }
.riesgo { background: #fde0dd; color: #a02518; }
.sinobj, .sindato { background: #e8e3f5; color: #4b3a8a; }
.pend { background: #eceff3; color: #555f70; }
ul { margin: 4px 0 0; padding-left: 18px; }
li { margin-bottom: 2px; }
.box { border-radius: 6px; padding: 8px 12px; margin-bottom: 8px; }
.box.b-ok { background: #f3faf5; border-left: 4px solid #2e9e55; }
.box.b-foco { background: #fffaee; border-left: 4px solid #d9a400; }
.box.b-gest { background: #f6f4fb; border-left: 4px solid #6a55b5; }
.box h3 { margin: 0 0 2px; font-size: 10pt; }
.nota { font-size: 8pt; color: #5a6578; margin-top: 12px; line-height: 1.35; }
"""


def main():
    src, out = sys.argv[1], sys.argv[2]
    if len(sys.argv) > 3:
        import json
        NOTAS.update(json.load(open(sys.argv[3], encoding="utf-8")).get("notas", {}))
    os.makedirs(out, exist_ok=True)
    d = collections.defaultdict(list)
    for r in csv.DictReader(open(src, encoding="utf-8")):
        d[r["boca"]].append(r)
    for boca, rs in d.items():
        cod = boca.split("-")[0]
        nombre = boca.split("-", 1)[1].strip()
        fecha = next(r["fecha"] for r in rs if r["fecha"])
        dd, mm, yy = map(int, fecha.split("/"))
        dias_mes = calendar.monthrange(yy, mm)[1]
        hoy = sum(f(r["puntos_obtenidos"]) or 0 for r in rs)
        proy = sum(f(r["puntos_proyectados"]) or 0 for r in rs)
        bien, foco, gestion = bullets(rs, dias_mes)
        hoy_s, proy_s = f"{hoy:.1f}".replace(".", ","), f"{proy:.1f}".replace(".", ",")
        extra = NOTAS.get(cod, {})
        foco += extra.get("foco", [])
        gestion += extra.get("gestion", [])
        gestion.append("Cliente incógnito y Auditoría de imagen (10 pts) aún no fueron evaluados. Recuerden que además son condición básica "
                       "del programa: se requiere ≥75 % en Cliente incógnito y ≥80 % en Auditoría de imagen.")

        filas = []
        for r in rs:
            c = r["concepto"]
            est, txt = evaluar(r, dias_mes)
            proy_txt = fmt(f(r["proyeccion"]), c) if c in VOLUMEN and r["proyeccion"] else ""
            filas.append(
                f"<tr><td style=\"white-space:nowrap\">{CORTO[c]}{' <span style=\"color:#8a93a3\">(' + UNIDAD[c] + ')</span>' if c in UNIDAD else ''}</td>"
                f"<td class=n>{int(f(r['puntos_posibles']))}</td>"
                f"<td class=n>{fmt(f(r['obj_min']), c)}</td><td class=n>{fmt(f(r['obj_max']), c)}</td>"
                f"<td class=n>{fmt(f(r['real']), c)}</td><td class=n>{proy_txt or '—'}</td>"
                f"<td><span class='chip {est}'>{html.escape(txt)}</span></td></tr>")

        def caja(cls, titulo, items):
            if not items:
                return ""
            lis = "".join(f"<li>{html.escape(i)}</li>" for i in items)
            return f"<div class='box {cls}'><h3>{titulo}</h3><ul>{lis}</ul></div>"

        doc = f"""<!doctype html><html lang="es"><head><meta charset="utf-8"><title>Avance +YPF {cod} {nombre}</title><style>{CSS}</style></head><body>
<div class="head"><div><h1>{cod} – {html.escape(nombre)}</h1><div class="sub">Avance del Programa +YPF · datos al {fecha} (día {dd} de {dias_mes})</div></div><div class="prog">PROGRAMA +YPF<br><span style="font-weight:400;font-size:9pt">{MESES[mm]} {yy}</span></div></div>
<div class="kpis">
<div class="kpi"><div class="v">{hoy_s}</div><div class="l">Puntos obtenidos hoy (de 100)</div></div>
<div class="kpi"><div class="v">{proy_s}</div><div class="l">Puntos proyectados al cierre del mes, al ritmo actual</div></div>
<div class="kpi"><div class="v">{len(foco)}</div><div class="l">Indicadores donde enfocar</div></div>
</div>
<h2>Situación por indicador</h2>
<table><thead><tr><th>Indicador</th><th class=n>Pts</th><th class=n>Obj. mín.</th><th class=n>Obj. máx.</th><th class=n>Real</th><th class=n>Proyección cierre</th><th>Estado</th></tr></thead><tbody>
{''.join(filas)}</tbody></table>
<h2>Lectura</h2>
{caja('b-ok', 'Lo que viene bien', bien)}
{caja('b-foco', 'Dónde enfocar en lo que queda del mes', foco)}
{caja('b-gest', 'Temas en gestión / a verificar', gestion)}
<div class="nota"><b>Cómo se calcula:</b> los volúmenes del tablero son acumulados del mes, por eso hoy figuran con 0 % de cumplimiento. La proyección
estima el cierre al ritmo de venta actual (real ÷ {dd} días × {dias_mes}). Los indicadores en % se toman como están hoy.
Puntaje: debajo del objetivo mínimo = 0 pts; en el mínimo = 70 % de los puntos; en el máximo = 100 %. Por eso quedar apenas debajo del mínimo no suma nada.
Fuente: tablero Performance de Red YPF.</div>
</body></html>"""
        base = f"{cod} - {nombre}"
        with open(os.path.join(out, base + ".html"), "w", encoding="utf-8") as fh:
            fh.write(doc)



if __name__ == "__main__":
    main()
