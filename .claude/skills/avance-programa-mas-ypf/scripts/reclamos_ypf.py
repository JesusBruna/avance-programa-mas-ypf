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

NOMBRE_CORTO = {
    "diesel_m3": "Diesel", "naftas_m3": "Naftas", "mix_naftas": "Mix de Infinia en naftas", "mix_go": "Mix de Infinia Diesel",
    "lubricantes_m3": "Lubricantes", "croselling": "Croselling", "comidas_un": "Comidas y Café", "app_ypf": "App YPF",
}
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

        mes = MESES[mm].lower()
        cerrado = "--cerrado" in sys.argv
        for c in reclamos.get(cod, []):
            r = cs[c]
            mn, real = f(r["obj_min"]), f(r["real"])
            red = sorted(f(x["obj_min"]) for x in por_conc[c])
            pos = len([v for v in red if v > mn]) + 1
            nom = NOMBRE_CORTO[c]
            if c in VOLUMEN:
                u = UNIDAD[c]
                dec = 0 if c == "comidas_un" else (2 if c == "lubricantes_m3" else 1)
                dias = int(r["dias"])
                proy = f(r["proyeccion"])
                act = real / dias
                nec = (mn - real) / (dm - dias) if not cerrado and dm > dias else mn / dm
                verbo = "habría cerrado" if cerrado else "cerraría"
                t = (f"- {nom}: el mínimo es {fmt(mn, c)} {u} y al {fecha[:5]} la estación llevaba {fmt(real, c)} {u}, así que "
                     f"{mes} {verbo} en aprox. {es(proy, 0 if proy >= 10 else dec)} {u} (un {es(f(r['proy_vs_min']), 0)} % del mínimo). "
                     f"Para llegar tendrían que vender aprox. {es(nec, dec)} {u} por día y hoy vienen en aprox. {es(act, dec)}.")
                if pos == 1:
                    t += f" Además es el objetivo de {nom.lower()} más alto de toda nuestra red."
                if critico.get(c, 0) >= max(3, n_bocas // 3):
                    t += (f" Y no es un caso aislado: {bajo_min[c]} de nuestras {n_bocas} estaciones quedan abajo del mínimo en "
                          f"{nom.lower()}, así que también les pediría la base con la que se armaron estos objetivos.")
                t += " ¿Lo podemos revisar para lo que queda del trimestre?"
            else:
                med = statistics.median(red)
                t = (f"- {nom}: el mínimo es {es(mn)} % y la estación está en {es(real) + ' %' if real is not None else '(sin dato)'}. "
                     + ("Es el objetivo más alto de toda nuestra red" if pos == 1 else f"Es de los objetivos más altos de nuestra red (el {pos}.º)")
                     + f"; el promedio de nuestras estaciones anda en aprox. {es(med, 0)} %. ¿Lo podemos revisar?")
            items.append(t)

        if admin:
            sin_obj = [c for c in ("croselling", "comidas_un") if f(cs[c]["obj_min"]) is None and f(cs[c]["real"]) is None]
            if len(sin_obj) == 2:
                adm.append("- Croselling y Comidas y Café: siguen sin objetivo cargado, así que la estación no puede sumar esos "
                           "20 puntos. ¿Se pueden cargar o redistribuir esos puntos?")
            for c, r in cs.items():
                if c not in LARGO:
                    continue
                if f(r["obj_min"]) is not None and f(r["real"]) is None:
                    u = (" " + UNIDAD[c]) if c in UNIDAD else " %"
                    adm.append(f"- {NOMBRE_CORTO[c]}: tiene objetivo ({fmt(f(r['obj_min']), c).replace(' %', '')}{u}) pero en el tablero "
                               "no aparece el dato real. ¿Me confirman si se está cargando?")
                elif f(r["obj_min"]) is None and f(r["real"]) is not None:
                    adm.append(f"- {NOMBRE_CORTO[c]}: figura sin objetivo (el real es {fmt(f(r['real']), c)}). "
                               "¿Me confirman cómo se va a evaluar?")
        if cod in extra:
            adm.append("- " + extra[cod])
        if not items and not adm:
            continue

        loc = "ACA " + nombre.replace("ACA ", "").title()
        L = [f"Asunto: Programa +YPF – Revisión de objetivos – {cod} {nombre}", "", "Hola, ¿cómo están?", ""]
        todos_items = items + adm
        if len(todos_items) == 1:
            L += [f"Les escribo por el avance de {loc} al {fecha[:5]}. Les quería pedir que revisen esto:", ""]
        else:
            L += [f"Les escribo por el avance de {loc} al {fecha[:5]}. Hay algunos temas que les quería pedir que revisen:", ""]
        for x in todos_items:
            L += [x, ""]
        L += ["Quedo atento. ¡Gracias!", "", "Saludos,"]
        txt = "\n".join(L) + "\n"
        with open(os.path.join(out, f"Reclamo YPF - {cod} - {nombre}.txt"), "w", encoding="utf-8") as fh:
            fh.write(txt)
        todos.append(f"==================== {cod} - {nombre} ====================\n{txt}")
    with open(os.path.join(out, "01 - Reclamos a YPF por estación (todos).txt"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(todos))
    print(f"{len(todos)} reclamos generados")


if __name__ == "__main__":
    main()
