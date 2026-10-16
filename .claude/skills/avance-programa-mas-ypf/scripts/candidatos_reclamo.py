"""Lista candidatos a reclamo y datos faltantes a partir del CSV de avance.

Uso: python3 candidatos_reclamo.py <avance.csv> [umbral_pct=95]
Imprime:
  1) Volúmenes cuya proyección queda por debajo del umbral (% del mínimo), con ritmo actual vs necesario.
  2) Objetivos porcentuales que se destacan contra el resto de la red (> 2x la mediana).
  3) Conceptos sin objetivo o sin dato real.
"""
import calendar
import collections
import csv
import statistics
import sys

src = sys.argv[1]
umbral = float(sys.argv[2]) if len(sys.argv) > 2 else 95
rows = list(csv.DictReader(open(src, encoding="utf-8")))
f = lambda x: float(x) if x not in ("", None) else None
VOL = {"diesel_m3", "naftas_m3", "lubricantes_m3", "comidas_un"}

print(f"== 1) VOLÚMENES CON PROYECCIÓN < {umbral:.0f} % DEL MÍNIMO ==")
cand = []
for r in rows:
    if r["concepto"] in VOL and f(r["proy_vs_min"]) is not None and f(r["proy_vs_min"]) < umbral:
        d, m, y = map(int, r["fecha"].split("/")) if r["fecha"] else (int(r["dias"]), 1, 2000)
        dm = calendar.monthrange(y, m)[1]
        real, mn, dias = f(r["real"]), f(r["obj_min"]), int(r["dias"])
        nec, act = (mn - real) / (dm - dias), real / dias
        cand.append((f(r["proy_vs_min"]), r["boca"], r["concepto"], mn, f(r["obj_max"]), real, f(r["proyeccion"]), act, nec, f(r["puntos_posibles"])))
for c in sorted(cand):
    print(f"{c[1]:30} {c[2]:15} min {c[3]:>8} max {c[4]:>8} real {c[5]:>8} proy {c[6]:>9.2f} ({c[0]:5.1f} %)  "
          f"ritmo {c[7]:.3f} -> {c[8]:.3f}/día (+{(c[8]/c[7]-1)*100 if c[7] else 0:.0f} %)  pts {c[9]:.0f}")

print("\n== 2) OBJETIVOS PORCENTUALES ATÍPICOS (> 2x la mediana de la red) ==")
por = collections.defaultdict(list)
for r in rows:
    if r["concepto"] in ("mix_naftas", "mix_go", "croselling", "app_ypf") and f(r["obj_min"]):
        por[r["concepto"]].append(r)
for c, rs in por.items():
    med = statistics.median(f(r["obj_min"]) for r in rs)
    for r in rs:
        if f(r["obj_min"]) > 2 * med or (f(r["obj_min"]) == max(f(x["obj_min"]) for x in rs) and f(r["real"]) is not None and f(r["real"]) < f(r["obj_min"])):
            print(f"{r['boca']:30} {c:12} min {r['obj_min']} % (mediana red {med:.1f} %) real {r['real'] or '--'}")

print("\n== 3) SIN OBJETIVO / SIN DATO REAL ==")
for r in rows:
    if r["concepto"] in ("cliente_incognito", "auditoria_imagen"):
        continue
    if not r["obj_min"]:
        print(f"{r['boca']:30} {r['concepto']:15} SIN OBJETIVO" + (f" (real {r['real']})" if r["real"] else ""))
    elif not r["real"]:
        print(f"{r['boca']:30} {r['concepto']:15} SIN DATO REAL (objetivo {r['obj_min']})")
