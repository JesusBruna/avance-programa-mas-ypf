"""Genera el mail para cada estación, pensado para enviar con el tablero original de YPF adjunto.

Uso: python3 mails_estaciones.py <avance.csv> <carpeta_salida> [notas.json]
"""
import calendar
import collections
import csv
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from informes_por_estacion import CORTO, UNIDAD, VOLUMEN, evaluar, f, fmt  # noqa: E402

# Se cargan desde el mismo JSON de notas (opcional):
#   "reclamos":   {"931": ["lubricantes_m3"], ...}  -> conceptos cuya revisión se pidió a YPF
#   "extra_mail": {"888": "texto ..."}               -> línea adicional en "Para tener en cuenta"
RECLAMOS, EXTRA = {}, {}


def es(v, d=1):
    return f"{v:.{d}f}".replace(".", ",")


def main():
    src, out = sys.argv[1], sys.argv[2]
    if len(sys.argv) > 3:
        import json
        cfg = json.load(open(sys.argv[3], encoding="utf-8"))
        RECLAMOS.update(cfg.get("reclamos", {}))
        EXTRA.update(cfg.get("extra_mail", {}))
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
        hoy = sum(f(r["puntos_obtenidos"]) or 0 for r in rs)
        proy = sum(f(r["puntos_proyectados"]) or 0 for r in rs)
        reclamos = RECLAMOS.get(cod, [])

        foco, bien, pend = [], [], []
        for r in rs:
            c = r["concepto"]
            est, _ = evaluar(r, dias_mes)
            mn, real, proyc = f(r["obj_min"]), f(r["real"]), f(r["proyeccion"])
            n = CORTO[c]
            if est in ("justo", "riesgo"):
                if c in VOLUMEN:
                    dias = int(r["dias"])
                    u = UNIDAD[c]
                    dec = 0 if c == "comidas_un" else (3 if c == "lubricantes_m3" else 1)
                    nec, act = (mn - real) / (dias_mes - dias), real / dias
                    s = (f"{n}: llevan {fmt(real, c)} {u} y el mínimo es {fmt(mn, c)} {u}. "
                         f"Hay que vender ~{es(nec, dec)} {u}/día (hoy ~{es(act, dec)}).")
                    if est == "justo":
                        s += " Está al límite: cada día cuenta."
                else:
                    s = f"{n}: {fmt(real, c)} contra un mínimo de {fmt(mn, c)} (faltan {es(mn - real)} pp)."
                    if mn - real <= 1:
                        s += " Está muy cerca."
                if c in reclamos:
                    s += " Pedimos a YPF que revise este objetivo; mientras tanto, sigamos empujando."
                foco.append(s)
            elif est == "ok":
                bien.append(n)
            elif est == "sindato" and c == "lubricantes_m3":
                pend.append("Lubricantes no muestra ventas en el tablero. Si compraron o vendieron lubricantes este mes, avísennos para reclamar el dato.")
        sin_obj = {r["concepto"] for r in rs if not r["obj_min"]}
        if {"croselling", "comidas_un"} <= sin_obj:
            pend.append("Croselling y Comidas y Café no tienen objetivo asignado (20 pts). Ya lo reclamamos a YPF.")
        if cod in EXTRA:
            pend.append(EXTRA[cod])
        pend.append("Cliente incógnito y Auditoría de imagen todavía no se evaluaron. Además de sumar puntos, son condición del programa "
                    "(mínimo 75 % y 80 %): prolijidad, imagen y atención en playa.")

        L = [f"Asunto: Programa +YPF – {nombre} – Avance al {fecha[:5]}", "",
             f"Hola equipo de {nombre}:", "",
             f"Les adjuntamos el tablero de Performance de Red de YPF con datos al {fecha}.", "",
             "Cómo leerlo:",
             "- Los volúmenes (diesel, naftas, lubricantes y comidas) son acumulados del mes. Por eso hoy aparecen con 0 % de cumplimiento: se evalúan al cierre.",
             "- Cada indicador suma puntos solo si se llega al objetivo mínimo (ahí suma el 70 % de los puntos) y suma el 100 % al llegar al máximo. Quedar apenas por debajo del mínimo no suma nada.",
             f"- Hoy llevan {es(hoy)} pts. Al ritmo actual estimamos ~{es(proy)} pts al cierre (sin contar lo que todavía no se mide).", ""]
        if foco:
            L += ["Dónde seguir trabajando:"] + [f"- {x}" for x in foco] + [""]
        if bien:
            L += ["Vienen bien en: " + ", ".join(bien) + ". ¡A sostenerlo!", ""]
        L += ["Para tener en cuenta:"] + [f"- {x}" for x in pend] + [""]
        L += ["Cualquier duda, quedamos en contacto.", "", "Saludos,", "[Nombre y firma]"]
        txt = "\n".join(L) + "\n"
        with open(os.path.join(out, f"{cod} - {nombre} - mail.txt"), "w", encoding="utf-8") as fh:
            fh.write(txt)
        todos.append(f"==================== {cod} - {nombre}  (adjuntar: {boca}.pdf) ====================\n{txt}")
    with open(os.path.join(out, "02 - Mails a estaciones (todos).txt"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(todos))


if __name__ == "__main__":
    main()
