"""Genera el mail para cada estación, pensado para enviar con el tablero original de YPF adjunto.
Tono: como lo escribe el coordinador (primera persona, rioplatense, cercano y concreto).

Uso: python3 mails_estaciones.py <avance.csv> <carpeta_salida> [notas.json] [--cerrado]
  --cerrado: el mes de los datos ya terminó (se habla de cómo cerró y del mes siguiente).
             Si no se pasa, se detecta solo cuando faltan 3 días o menos para fin de mes.
"""
import calendar
import collections
import csv
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from informes_por_estacion import MESES, UNIDAD, VOLUMEN, evaluar, f, fmt  # noqa: E402

# Del JSON de notas (opcional):
#   "reclamos":   {"931": ["lubricantes_m3"], ...}  -> conceptos cuya revisión se pidió a YPF
#   "extra_mail": {"888": "texto ..."}               -> línea adicional en "Otros temas"
RECLAMOS, EXTRA = {}, {}
SIN_MOV = set()  # (boca, concepto) cuyo real no cambió respecto del CSV anterior (--anterior=<csv>)

NOMBRE_MAIL = {
    "diesel_m3": "Diesel", "naftas_m3": "Naftas", "mix_naftas": "Mix de Infinia en naftas",
    "mix_go": "Mix de Infinia Diesel", "lubricantes_m3": "Lubricantes", "croselling": "Croselling",
    "comidas_un": "Comidas y Café", "app_ypf": "App YPF",
}


def es(v, d=1):
    return f"{v:,.{d}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def lista(items):
    items = [i if i in ("App YPF", "Comidas y Café") else i[0].lower() + i[1:] for i in items]
    return items[0] if len(items) == 1 else ", ".join(items[:-1]) + " y " + items[-1]


def localidad(nombre):
    return nombre.replace("ACA ", "").title()


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    src, out = args[0], args[1]
    if len(args) > 2:
        cfg = json.load(open(args[2], encoding="utf-8"))
        RECLAMOS.update(cfg.get("reclamos", {}))
        EXTRA.update(cfg.get("extra_mail", {}))
    forzar_cerrado = "--cerrado" in sys.argv
    for a in sys.argv:
        if a.startswith("--anterior="):
            prev = {(r["boca"], r["concepto"]): r["real"] for r in csv.DictReader(open(a.split("=", 1)[1], encoding="utf-8"))}
            for r in csv.DictReader(open(args[0], encoding="utf-8")):
                if r["concepto"] in VOLUMEN and r["concepto"] != "lubricantes_m3" and r["real"] and prev.get((r["boca"], r["concepto"])) == r["real"]:
                    SIN_MOV.add((r["boca"], r["concepto"]))
    os.makedirs(out, exist_ok=True)
    d = collections.defaultdict(list)
    for r in csv.DictReader(open(src, encoding="utf-8")):
        d[r["boca"]].append(r)
    todos = []
    for boca, rs in d.items():
        cod, nombre = boca.split("-")[0], boca.split("-", 1)[1].strip()
        fecha = next(r["fecha"] for r in rs if r["fecha"])
        dd, mm, yy = map(int, fecha.split("/"))
        dias_mes = calendar.monthrange(yy, mm)[1]
        mes, mes_sig = MESES[mm].lower(), MESES[mm % 12 + 1].lower()
        dias_sig = calendar.monthrange(yy + (mm == 12), mm % 12 + 1)[1]
        cerrado = forzar_cerrado
        acumulado_trim = (mm - 1) % 3 > 0  # 2.º o 3.º mes del trimestre: tablero acumulado
        sin_mov = {c for (b, c) in SIN_MOV if b == boca}
        cierre = cerrado or dias_mes - dd <= 3
        hoy = sum(f(r["puntos_obtenidos"]) or 0 for r in rs)
        proy = sum(f(r["puntos_proyectados"]) or 0 for r in rs)
        reclamos = RECLAMOS.get(cod, [])

        foco, bien, otros = [], [], []
        for r in rs:
            c = r["concepto"]
            if c in ("cliente_incognito", "auditoria_imagen"):
                continue
            est, _ = evaluar(r, dias_mes)
            mn, real, proyc = f(r["obj_min"]), f(r["real"]), f(r["proyeccion"])
            n = NOMBRE_MAIL[c]
            if est in ("justo", "riesgo"):
                if c in VOLUMEN:
                    u = "unidades" if c == "comidas_un" else UNIDAD[c]
                    dias = int(r["dias"])
                    dec = 0 if c == "comidas_un" else (2 if c == "lubricantes_m3" else 1)
                    act = real / dias
                    if c == "lubricantes_m3":
                        s = (f"{n}: llevan {fmt(real, c)} {u} de un mínimo de {fmt(mn, c)} {u}. "
                             "Acuérdense de que el último día para hacer el pedido es el 7/12.")
                    elif acumulado_trim:
                        nec = f(r.get("ritmo_necesario_dia"))
                        falta = mn - real
                        s = (f"{n}: llevan {fmt(real, c)} {u} en el trimestre y el mínimo acumulado a fin de {mes} es "
                             f"{fmt(mn, c)} {u}. Les faltan {fmt(falta, c)} {u}: aprox. {es(nec, dec)} {u} por día de acá a fin de mes "
                             f"(en lo que va del trimestre vienen promediando aprox. {es(act, dec)} {u} por día).")
                    elif cierre and proyc >= mn:
                        verbo = "habría cerrado" if cerrado else "cerraría"
                        s = (f"{n}: {mes} {verbo} en aprox. {fmt(proyc, c)} {u}, apenas arriba del mínimo de {fmt(mn, c)} {u}. "
                             f"Ojo en {mes_sig}, porque si quedan un poco abajo se pierden todos los puntos.")
                    elif cierre:
                        verbo = "habría cerrado" if cerrado else "cerraría"
                        s = (f"{n}: {mes} {verbo} en aprox. {fmt(proyc, c)} {u}, un {es(proyc / mn * 100, 0)} % del mínimo "
                             f"({fmt(mn, c)} {u}). Para llegar en {mes_sig} tendrían que promediar aprox. {es(mn / dias_sig, dec)} {u} "
                             f"por día; en {mes} vendieron aprox. {es(act, dec)} {u} por día.")
                    else:
                        nec = (mn - real) / (dias_mes - dias)
                        s = (f"{n}: llevan {fmt(real, c)} {u} y el mínimo es {fmt(mn, c)} {u}. Tendrían que vender aprox. "
                             f"{es(nec, dec)} {u} por día de acá a fin de mes (hoy vienen en aprox. {es(act, dec)} {u} por día).")
                        if est == "justo":
                            s += " Está muy parejo, así que cada día cuenta."
                    if c in sin_mov:
                        s += (" Ojo: este dato no se movió desde el tablero anterior, así que puede que YPF todavía no haya "
                              "cargado los últimos días; si ustedes ven otra cosa, avísenme.")
                else:
                    falta = mn - real
                    s = f"{n}: están en {fmt(real, c)} y el mínimo es {fmt(mn, c)}; les faltan {es(falta)} puntos."
                    if falta <= 1:
                        s += " Están muy cerca."
                if c in reclamos:
                    s += " Ya le pedí a YPF que revise este objetivo, pero mientras tanto sigamos empujando."
                foco.append(s)
            elif est == "ok":
                bien.append(NOMBRE_MAIL[c])
            elif est == "sindato" and c == "lubricantes_m3":
                otros.append(f"Lubricantes todavía no muestra compras. El último día para hacer el pedido es el 7/12; "
                             f"planifíquenlo para llegar al mínimo de {fmt(mn, c)} m3.")
        sin_obj = {r["concepto"] for r in rs if not r["obj_min"]}
        if {"croselling", "comidas_un"} <= sin_obj:
            otros.append("Croselling y Comidas y Café siguen sin objetivo cargado (son 20 puntos). Ya se lo estoy reclamando a YPF.")
        if cod in EXTRA:
            otros.append(EXTRA[cod])
        inc = next((r for r in rs if r["concepto"] == "cliente_incognito"), None)
        inc_real = f(inc["real"]) if inc else None
        img = next(r for r in rs if r["concepto"] == "auditoria_imagen")
        if f(img["real"]) is not None:
            if f(img["real"]) >= 80:
                otros.append(f"La auditoría de imagen les dio {es(f(img['real']))} %. ¡Muy bien! (el mínimo es 80 %).")
            else:
                otros.append(f"La auditoría de imagen les dio {es(f(img['real']))} %, por debajo del 80 % que pide el programa. "
                             "Hay que corregirlo, porque es condición para cobrar.")
            if inc_real is None:
                otros.append("Todavía falta la evaluación de cliente incógnito. El mínimo es 75 %, así que atención y prolijidad en la playa.")
            elif inc_real < 75:
                otros.append(f"Cliente incógnito les dio {es(inc_real)} %, por debajo del 75 % que pide el programa como condición básica. "
                             "Es urgente revisar la atención en playa; ya le pedí a YPF el detalle de la evaluación para ver en qué fallamos.")
            elif inc_real < 80:
                otros.append(f"Cliente incógnito les dio {es(inc_real)} %: cumple la condición (75 %) pero no suma puntos (hace falta 80 %).")
            else:
                otros.append(f"Cliente incógnito les dio {es(inc_real)} %. ¡Muy bien!")
        else:
            otros.append("Todavía faltan la auditoría de imagen y la evaluación de cliente incógnito. Los mínimos son 80 % y 75 % "
                         "y son condición del programa, así que prolijidad, imagen y atención en la playa.")

        estimado = (f"Al {fecha[:5]} llevaban {es(hoy)} puntos y calculo que {mes} cerró en aprox. {es(proy)}"
                    if cerrado else f"Al {fecha[:5]} llevan {es(hoy)} puntos y, si siguen a este ritmo, {mes} cerraría en aprox. {es(proy)}")
        L = [f"Asunto: Programa +YPF – {nombre} – Avance al {fecha[:5]}", "",
             f"Hola, equipo de {localidad(nombre)}, ¿cómo están?", "",
             f"Les paso el tablero del Programa +YPF que nos mandó YPF con los datos al {fecha[:5]}.", "",
             ("Un par de aclaraciones para leerlo: los objetivos son trimestrales y ahora el tablero muestra el acumulado del trimestre "
              f"contra el mínimo acumulado a fin de {mes}. Por eso los volúmenes figuran con 0 % hasta que se alcanza ese mínimo. "
              if acumulado_trim else
              "Un par de aclaraciones para leerlo: los objetivos son trimestrales, pero el tablero muestra cómo viene cada mes. "
              "Los volúmenes se van acumulando durante el mes, así que hasta que no se llega al mínimo figuran con 0 %. ") +
             "Y ojo, que cada indicador suma recién cuando se pasa el mínimo: quedar apenas abajo no suma nada.", "",
             estimado + " (sin contar lo que todavía no se mide).", ""]
        if bien:
            L += [f"Lo bueno: vienen bien en {lista(bien)}. ¡Sigan así!", ""]
        if foco:
            L += [("Para " + mes_sig if cierre else "Para lo que queda del mes") + " les pido que pongan foco en:"]
            L += [f"- {x}" for x in foco] + [""]
        L += ["Otros temas:"] + [f"- {x}" for x in otros] + [""]
        L += ["Cualquier cosa me avisan.", "", "Saludos,"]
        txt = "\n".join(L) + "\n"
        with open(os.path.join(out, f"{cod} - {nombre} - mail.txt"), "w", encoding="utf-8") as fh:
            fh.write(txt)
        todos.append(f"==================== {cod} - {nombre}  (adjuntar: {boca}.pdf) ====================\n{txt}")
    with open(os.path.join(out, "02 - Mails a estaciones (todos).txt"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(todos))


if __name__ == "__main__":
    main()
