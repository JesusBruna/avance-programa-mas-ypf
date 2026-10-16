"""Genera un mail de reclamo a YPF POR ESTACIÓN (cada estación tiene su propio contacto en YPF).

Uso: python3 reclamos_ypf.py <avance.csv> <carpeta_salida> <notas.json> [--sin-administrativos]

Del notas.json usa:
  "reclamos":  {"931": ["lubricantes_m3"], "1239": ["diesel_m3"], "889": ["croselling"]}
               -> objetivos cuya revisión se pide (decisión de criterio, ver SKILL.md)
  "extra_ypf": {"888": "texto ..."}  -> párrafo adicional para el reclamo de esa estación

Además agrega automáticamente, salvo --sin-administrativos:
  - croselling / comidas sin objetivo asignado
  - conceptos con objetivo pero sin dato real
  - conceptos sin objetivo pero con dato real
Genera un .txt por estación con algo para reclamar y un archivo con todos juntos.
"""
import calendar
import collections
import csv
import json
import os
import statistics
import sys

sys.path.insert(0, os.path.dirname(__file__))
from informes_por_estacion import MESES, UNIDAD, VOLUMEN, f, fmt  # noqa: E402

LARGO = {
    "diesel_m3": "Diesel (Infinia Diesel + D500)", "naftas_m3": "Naftas (Infinia + Súper)",
    "mix_naftas": "Mix Infinia naftas", "mix_go": "Mix Infinia Diesel", "lubricantes_m3": "Lubricantes",
    "croselling": "Croselling", "comidas_un": "Unidades Comidas y Café", "app_ypf": "Penetración App YPF",
}
PORC = {"mix_naftas", "mix_go", "croselling", "app_ypf"}


def es(v, d=1):
    return f"{v:,.{d}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def main():
    src, out, notas_path = sys.argv[1], sys.argv[2], sys.argv[3]
    admin = "--sin-administrativos" not in sys.argv
    cfg = json.load(open(notas_path, encoding="utf-8"))
    reclamos, extra = cfg.get("reclamos", {}), cfg.get("extra_ypf", {})
    os.makedirs(out, exist_ok=True)

    rows = list(csv.DictReader(open(src, encoding="utf-8")))
    por_boca = collections.defaultdict(dict)
    por_conc = collections.defaultdict(list)
    for r in rows:
        por_boca[r["boca"]][r["concepto"]] = r
        if f(r["obj_min"]) is not None:
            por_conc[r["concepto"]].append(r)
    n_bocas = len(por_boca)
    bajo_min = {c: sum(1 for r in rs if f(r["proy_vs_min"]) is not None and f(r["proy_vs_min"]) < 100)
                for c, rs in por_conc.items() if c in VOLUMEN}
    # Solo se menciona como problema "de red" si al menos un tercio de las estaciones está claramente abajo (< 95 %)
    critico = {c: sum(1 for r in rs if f(r["proy_vs_min"]) is not None and f(r["proy_vs_min"]) < 95)
               for c, rs in por_conc.items() if c in VOLUMEN}

    todos = []
    for boca, cs in por_boca.items():
        cod, nombre = boca.split("-")[0], boca.split("-", 1)[1].strip()
        fecha = next(r["fecha"] for r in cs.values() if r["fecha"])
        dd, mm, yy = map(int, fecha.split("/"))
        dm = calendar.monthrange(yy, mm)[1]
        items, adm = [], []

        for i, c in enumerate(reclamos.get(cod, []), 1):
            r = cs[c]
            mn, mx, real = f(r["obj_min"]), f(r["obj_max"]), f(r["real"])
            red = sorted(f(x["obj_min"]) for x in por_conc[c])
            pos = len([v for v in red if v > mn]) + 1
            if c in VOLUMEN:
                u = UNIDAD[c]
                dec = 0 if c == "comidas_un" else (3 if c == "lubricantes_m3" else 1)
                dias = int(r["dias"])
                act, nec = real / dias, (mn - real) / (dm - dias)
                t = (f"{len(items) + 1}. {LARGO[c]}\n"
                     f"   Objetivo: mín. {fmt(mn, c)} {u} / máx. {fmt(mx, c)} {u}\n"
                     f"   Real al {fecha[:5]}: {fmt(real, c)} {u}, que proyecta {fmt(f(r['proyeccion']), c)} {u} al cierre "
                     f"({es(f(r['proy_vs_min']), 0)} % del mínimo)\n"
                     f"   Ritmo necesario {es(nec, dec)} {u}/día contra {es(act, dec)} {u}/día actual (+{es((nec / act - 1) * 100, 0)} %)\n")
                if pos == 1:
                    t += f"   Es el objetivo de {LARGO[c].split(' (')[0].lower()} más alto de nuestra red de {n_bocas} estaciones.\n"
                if critico.get(c, 0) >= max(3, n_bocas // 3):
                    t += (f"   No es un caso aislado: {bajo_min[c]} de nuestras {n_bocas} estaciones proyectan {LARGO[c].split(' (')[0].lower()} "
                          f"por debajo del mínimo. Les pedimos también la base con la que se fijaron estos objetivos.\n")
            else:
                med = statistics.median(red)
                t = (f"{len(items) + 1}. {LARGO[c]}\n"
                     f"   Objetivo: mín. {es(mn)} % / máx. {es(mx)} %. Real: {es(real) + ' %' if real is not None else 'sin dato'}"
                     + (f" ({es(mn - real)} pp debajo del mínimo)" if real is not None and real < mn else "") + ".\n"
                     f"   La mediana de nuestra red para este objetivo es {es(med)} %"
                     + (" y es el valor más alto de la red" if pos == 1 else f" (es el {pos}.º más alto)") + ".\n")
            t += f"   Puntos en juego: {int(f(r['puntos_posibles']))}\n"
            items.append(t)

        if admin:
            sin_obj = [c for c in ("croselling", "comidas_un") if f(cs[c]["obj_min"]) is None and f(cs[c]["real"]) is None]
            if len(sin_obj) == 2:
                adm.append("- Sin objetivo de Croselling ni de Unidades Comidas y Café (20 pts que no se pueden sumar). "
                           "Solicitamos que se carguen los objetivos o que se redistribuya ese puntaje.")
            for c, r in cs.items():
                if c not in LARGO:
                    continue
                if f(r["obj_min"]) is not None and f(r["real"]) is None:
                    u = (" " + UNIDAD[c]) if c in UNIDAD else " %"
                    adm.append(f"- {LARGO[c]}: tiene objetivo ({fmt(f(r['obj_min']), c).replace(' %', '')}{u}) pero el tablero no muestra "
                               "dato real. Solicitamos confirmar si la información se está cargando.")
                elif f(r["obj_min"]) is None and f(r["real"]) is not None:
                    adm.append(f"- {LARGO[c]}: figura sin objetivo y con un real de {fmt(f(r['real']), c)}. "
                               "Les pedimos confirmar cómo se va a evaluar este indicador al cierre.")
        if cod in extra:
            adm.append("- " + extra[cod])
        if not items and not adm:
            continue

        L = [f"Asunto: Programa +YPF – Solicitud de revisión de objetivos {MESES[mm]} {yy} – {cod} {nombre}", "",
             "Estimados:", ""]
        if items:
            L += [f"Solicitamos la revisión de los siguientes objetivos del Programa +YPF de {MESES[mm].lower()} {yy} para la estación "
                  f"{cod} {nombre}. Según el tablero de Performance de Red con datos al {fecha} ({dd} de {dm} días), "
                  "el objetivo mínimo queda fuera de alcance al ritmo de venta real del mes. Como el indicador no suma puntos "
                  "si no se llega al mínimo, la estación pierde el puntaje completo aunque sostenga su nivel de venta habitual.", "",
                  f"Criterio de proyección: venta acumulada al {fecha[:5]} ÷ {dd} días × {dm} días.", ""]
            L += items
        else:
            L += [f"Les escribimos por el tablero de Performance de Red del Programa +YPF de la estación {cod} {nombre} "
                  f"(datos al {fecha}). Hay algunos puntos que hoy le impiden sumar puntaje:", ""]
        if adm:
            if items:
                L += ["Además, hay puntos del tablero que hoy impiden sumar puntaje:", ""]
            L += adm + [""]
        L += ["Quedamos a disposición para revisarlo juntos.", "", "Saludos cordiales,"]
        txt = "\n".join(L) + "\n"
        with open(os.path.join(out, f"Reclamo YPF - {cod} - {nombre}.txt"), "w", encoding="utf-8") as fh:
            fh.write(txt)
        todos.append(f"==================== {cod} - {nombre} ====================\n{txt}")
    with open(os.path.join(out, "01 - Reclamos a YPF por estación (todos).txt"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(todos))
    print(f"{len(todos)} reclamos generados")


if __name__ == "__main__":
    main()
