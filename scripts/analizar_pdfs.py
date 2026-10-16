"""Extrae los tableros "Performance de Red" (PDF) de cada boca y proyecta el cierre de mes.

Uso: python3 scripts/analizar_pdfs.py [carpeta_pdfs] > datos/avance.csv
Requiere pdftotext (poppler-utils).

Supuestos:
- Período de medición mensual (mes calendario).
- Los valores de volumen / unidades son acumulados del mes hasta la fecha de actualización
  inclusive; se proyectan linealmente: real / días transcurridos * días del mes.
- Los ratios (mix, croselling, penetración app) no se proyectan: se toman como están.
- Escala de cumplimiento observada en los PDFs: < mínimo = 0 %, mínimo = 70 %, máximo = 100 %,
  lineal entre ambos.
"""
import calendar
import csv
import glob
import os
import re
import subprocess
import sys

CONCEPTOS = [
    ("Volumen diesel", "diesel_m3", True),
    ("Volumen naftas", "naftas_m3", True),
    ("Mix Naftas", "mix_naftas", False),
    ("Mix GO", "mix_go", False),
    ("Volumen lubricantes", "lubricantes_m3", True),
    ("Croselling", "croselling", False),
    ("Unidades Comidas", "comidas_un", True),
    ("Penetración App", "app_ypf", False),
    ("Cliente incognito", "cliente_incognito", False),
    ("Auditoría de Imagen", "auditoria_imagen", False),
]

NUM = r"(--|[\d.,]+\s*%?)"


def num(s):
    s = s.strip()
    if s == "--":
        return None
    return float(s.replace("%", "").replace(",", "").strip())


def cumplimiento(real, mn, mx):
    if real is None or mn is None or mx is None:
        return None
    if real < mn:
        return 0.0
    if real >= mx:
        return 100.0
    return 70 + 30 * (real - mn) / (mx - mn)


def parse(path):
    txt = subprocess.run(["pdftotext", "-layout", path, "-"], capture_output=True, text=True).stdout
    boca = os.path.basename(path)[:-4]
    filas = []
    lineas = txt.splitlines()
    for etiqueta, clave, acumulable in CONCEPTOS:
        for i, ln in enumerate(lineas):
            if etiqueta not in ln:
                continue
            resto = ln[ln.index(etiqueta):]
            resto = re.sub(r"^.*?(m3 \(.*?\)|m3|Café|YPF|incognito|Imagen|Naftas|GO|Croselling)", "", resto, count=1)
            vals = re.findall(NUM, re.sub(r"(\d{2}|--)/(\d{2}|--)/(\d{4}|----)", "", resto))
            # la fecha de actualización a veces cae en la línea anterior o siguiente del texto
            fecha = None
            for j in (i, i - 1, i + 1):
                if 0 <= j < len(lineas):
                    fecha = re.search(r"(\d{2}/\d{2}/\d{4})\s*$", lineas[j])
                    if fecha:
                        break
            mn, mx, real, pct, pp, po = (vals + ["--"] * 6)[:6]
            filas.append({
                "boca": boca, "concepto": clave, "acumulable": acumulable,
                "obj_min": num(mn), "obj_max": num(mx), "real": num(real),
                "cumpl_pdf": num(pct), "puntos_posibles": num(pp), "puntos_obtenidos": num(po),
                "fecha": fecha.group(1) if fecha else None,
            })
            break
    return filas


def proyectar(f, fecha_def):
    fecha = f["fecha"] or fecha_def
    d, m, y = map(int, fecha.split("/"))
    dias_mes = calendar.monthrange(y, m)[1]
    f["dias"] = d
    if f["acumulable"] and f["real"] is not None:
        f["proyeccion"] = round(f["real"] / d * dias_mes, 2)
        f["ritmo_necesario_dia"] = round(max(f["obj_min"] - f["real"], 0) / max(dias_mes - d, 1), 2) if f["obj_min"] else None
        f["ritmo_actual_dia"] = round(f["real"] / d, 2)
    else:
        f["proyeccion"] = f["real"]
    f["cumpl_proyectado"] = cumplimiento(f["proyeccion"], f["obj_min"], f["obj_max"])
    if f["cumpl_proyectado"] is not None and f["puntos_posibles"]:
        f["puntos_proyectados"] = round(f["cumpl_proyectado"] / 100 * f["puntos_posibles"], 1)
    else:
        f["puntos_proyectados"] = None
    f["proy_vs_min"] = round(f["proyeccion"] / f["obj_min"] * 100, 1) if f["proyeccion"] and f["obj_min"] else None
    return f


def main():
    carpeta = sys.argv[1] if len(sys.argv) > 1 else "."
    cols = ["boca", "concepto", "obj_min", "obj_max", "real", "fecha", "dias", "cumpl_pdf",
            "puntos_posibles", "puntos_obtenidos", "proyeccion", "proy_vs_min",
            "cumpl_proyectado", "puntos_proyectados", "ritmo_actual_dia", "ritmo_necesario_dia"]
    w = csv.DictWriter(sys.stdout, fieldnames=cols, extrasaction="ignore")
    w.writeheader()
    for path in sorted(glob.glob(os.path.join(carpeta, "*.pdf")), key=lambda p: int(os.path.basename(p).split("-")[0])):
        filas = parse(path)
        fecha_def = next((f["fecha"] for f in filas if f["fecha"]), "14/10/2026")
        for f in filas:
            w.writerow(proyectar(f, fecha_def))


if __name__ == "__main__":
    main()
