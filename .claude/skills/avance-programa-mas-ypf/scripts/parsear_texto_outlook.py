"""Convierte el texto que devuelve el conector de Outlook al leer el PDF adjunto de YPF
(read_resource sobre el adjunto) al mismo CSV que genera analizar_pdfs.py.

El conector extrae el PDF como texto "desordenado", pero el orden de los valores es fijo:
  ... Puntos posibles  <mixN_real> <lub_real>  Condiciones básicas ... designados.
  <cros_real>  Cliente incognito  <app_real>  ... Puntos obtenidos <TOTAL> Volumen lubricantes m3 <NOMBRE> <diesel_real>
  Croselling ... Puntos Posibles  <naf_min> <naf_max> <mixN_min> <mixN_max> <lub_min> <lub_max> <cros_min> <cros_max>
  <app_min> 80 % 100 % <x> <naf_real> <com_real> ... 15 20 10 10 10 5 Penetración App YPF <die_max> <die_min> 10 <x> <x>
  <com_max> <app_max> <com_min> Auditoría de Imagen 80 % 100 % <img_real> 5 <img_cumpl> <img_pts>
  Mix Naftas Mix GO <mixGO_real> <mixGO_min> <mixGO_max> <cumpl> <pts> <fechas...>

Uso: python3 parsear_texto_outlook.py <carpeta_con_txt> > avance.csv
     (un .txt por estación con el texto tal cual lo devolvió el conector)
Verifica que los puntos recalculados coincidan con el total del tablero (±0,3) y avisa por stderr si no.
"""
import glob
import os
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))
import calendar  # noqa: E402
import datetime as dt  # noqa: E402


def proyectar(r, fecha):
    """Proyección acumulada del TRIMESTRE.

    YPF fija objetivos trimestrales y el tablero muestra el acumulado desde el inicio del trimestre
    contra el mínimo acumulado al cierre del mes en curso (oct: mes 1; nov: oct+nov; dic: trimestre).
    En el primer mes del trimestre esto coincide con la proyección mensual.
    """
    f = r.get("fecha") or fecha
    d, m, y = map(int, f.split("/"))
    hoy = dt.date(y, m, d)
    ini = dt.date(y, 3 * ((m - 1) // 3) + 1, 1)
    fin_mes = dt.date(y, m, calendar.monthrange(y, m)[1])
    dias_trim = (hoy - ini).days + 1
    dias_total = (fin_mes - ini).days + 1
    restan = max((fin_mes - hoy).days, 1)
    r["dias"] = dias_trim
    r["dias_restantes_mes"] = (fin_mes - hoy).days
    real, mn, mx = r["real"], r["obj_min"], r["obj_max"]
    if r["acumulable"] and real is not None:
        r["proyeccion"] = round(real / dias_trim * dias_total, 2)
        r["ritmo_actual_dia"] = round(real / dias_trim, 3)
        r["ritmo_necesario_dia"] = round(max(mn - real, 0) / restan, 3) if mn else None
    else:
        r["proyeccion"] = real
    r["cumpl_proyectado"] = cumpl(r["proyeccion"], mn, mx)
    r["puntos_proyectados"] = round(r["cumpl_proyectado"] / 100 * r["puntos_posibles"], 1) if r["cumpl_proyectado"] is not None else None
    r["proy_vs_min"] = round(r["proyeccion"] / mn * 100, 1) if r["proyeccion"] and mn else None
    return r

TOK = re.compile(r"--|[\d][\d,]*(?:\.\d+)?\s*%?")
PTS = {"diesel_m3": 15, "naftas_m3": 20, "mix_naftas": 10, "mix_go": 5, "lubricantes_m3": 10, "croselling": 10,
       "comidas_un": 10, "app_ypf": 10, "cliente_incognito": 5, "auditoria_imagen": 5}
ACUM = {"diesel_m3", "naftas_m3", "lubricantes_m3", "comidas_un"}


def toks(s):
    return [t.strip() for t in TOK.findall(s)]


def num(t):
    if t is None or t == "--":
        return None
    return float(t.replace("%", "").replace(",", "").strip())


def cumpl(real, mn, mx):
    if real is None or mn is None or mx is None:
        return None
    if real < mn:
        return 0.0
    if real >= mx:
        return 100.0
    return 70 + 30 * (real - mn) / (mx - mn)


def parse(txt):
    fechas = re.findall(r"\d{2}/\d{2}/\d{4}", txt)
    t = re.sub(r"(\d{2}|--)/(\d{2}|--)/(\d{4}|----)", " ", txt)
    a, rest = t.split("Condiciones básicas solicitadas", 1)
    head = toks(a.split("Puntos posibles", 1)[1])
    rest = rest.split("designados.", 1)[1]
    b, rest = rest.split("Cliente incognito", 1)
    cros_real = toks(b)[0]
    app_real = toks(rest)[0]
    m = re.search(r"Puntos obtenidos\s+([\d.]+)\s+Volumen lubricantes\s+m3\s+(.+?)\s{2,}([\d.,]+|--)\s", rest)
    total, nombre, die_real = float(m.group(1)), m.group(2).strip(), m.group(3)
    seq = toks(rest.split("Puntos Posibles", 1)[1].split("Penetración App YPF", 1)[0])
    (naf_min, naf_max, mn_min, mn_max, lub_min, lub_max, cr_min, cr_max, app_min, _ci1, _ci2, _x, naf_real, com_real) = seq[:14]
    s2 = toks(rest.split("Penetración App YPF", 1)[1].split("Auditoría de Imagen", 1)[0])
    die_max, die_min, _10, incog_real, _b, com_max, app_max, com_min = s2[:8]
    s3 = toks(rest.split("Auditoría de Imagen", 1)[1].split("Mix Naftas", 1)[0])
    img_real = s3[2]
    s4 = toks(rest.split("Mix GO", 1)[1])
    go_real, go_min, go_max = s4[:3]
    d = {
        "diesel_m3": (die_min, die_max, die_real), "naftas_m3": (naf_min, naf_max, naf_real),
        "mix_naftas": (mn_min, mn_max, head[0]), "mix_go": (go_min, go_max, go_real),
        "lubricantes_m3": (lub_min, lub_max, head[1]), "croselling": (cr_min, cr_max, cros_real),
        "comidas_un": (com_min, com_max, com_real), "app_ypf": (app_min, app_max, app_real),
        "cliente_incognito": ("80", "100", incog_real), "auditoria_imagen": ("80", "100", img_real),
    }
    # fecha principal = la más repetida (combustibles); la de tienda = la más vieja
    fecha = max(set(fechas), key=lambda x: (fechas.count(x), x[6:], x[3:5], x[:2])) if fechas else None
    fecha_tienda = min(fechas, key=lambda x: (x[6:], x[3:5], x[:2])) if fechas else fecha
    return nombre, total, d, fecha, fecha_tienda


def main():
    cols = ["boca", "concepto", "obj_min", "obj_max", "real", "fecha", "dias", "cumpl_pdf",
            "puntos_posibles", "puntos_obtenidos", "proyeccion", "proy_vs_min",
            "cumpl_proyectado", "puntos_proyectados", "ritmo_actual_dia", "ritmo_necesario_dia", "dias_restantes_mes"]
    import csv
    w = csv.DictWriter(sys.stdout, fieldnames=cols, extrasaction="ignore")
    w.writeheader()
    archivos = sorted(glob.glob(os.path.join(sys.argv[1], "*.txt")), key=lambda p: int(re.match(r"\d+", os.path.basename(p)).group()))
    for path in archivos:
        nombre, total, d, fecha, fecha_tienda = parse(open(path, encoding="utf-8").read())
        calc = 0.0
        for c, (mn, mx, real) in d.items():
            mn, mx, real = num(mn), num(mx), num(real)
            cp = cumpl(real, mn, mx)
            po = round(cp / 100 * PTS[c], 1) if cp is not None else None
            calc += po or 0
            f = fecha_tienda if c in ("croselling", "comidas_un") else fecha
            r = {"boca": nombre, "concepto": c, "obj_min": mn, "obj_max": mx, "real": real, "fecha": f,
                 "cumpl_pdf": round(cp, 1) if cp is not None else None, "puntos_posibles": PTS[c], "puntos_obtenidos": po,
                 "acumulable": c in ACUM}
            if c == "cliente_incognito":
                r["obj_min"], r["obj_max"] = 80.0, 100.0  # mínimo para puntaje; la condición básica exige 75 %
            w.writerow(proyectar(r, fecha))
        if abs(calc - total) > 0.3:
            print(f"ATENCION {nombre}: puntos recalculados {calc:.1f} vs tablero {total:.1f} — revisar a mano", file=sys.stderr)
        else:
            print(f"ok {nombre}: {calc:.1f} pts (tablero {total:.1f})", file=sys.stderr)


if __name__ == "__main__":
    main()
