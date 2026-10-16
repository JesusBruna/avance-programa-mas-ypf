# Informe de avance Programa +YPF — Octubre 2026

**Fuente:** tableros "Performance de Red" de YPF (13 bocas ACA), datos actualizados al **14/10/2026** (combustibles, lubricantes, mix, app) y **13/10/2026** (croselling, comidas y café).
**Detalle completo por concepto:** `datos/avance_2026-10.csv` (generado con `scripts/analizar_pdfs.py`).

## Cómo leer este informe

- El tablero muestra **0 %** en volúmenes porque compara el acumulado parcial (14 días) contra el objetivo del mes completo. Por eso se **proyecta el cierre**: `real ÷ días transcurridos × 31`.
- Escala de puntaje deducida de los PDFs: **debajo del mínimo = 0 pts; en el mínimo = 70 %; en el máximo = 100 %**, lineal entre ambos. No hay puntaje parcial por debajo del mínimo: quedar al 99 % del mínimo vale 0.
- Los ratios (mix, croselling, app) se toman tal cual están hoy.
- Supuesto: los datos incluyen el día de actualización. Si en realidad cierran el día anterior, las proyecciones de volumen mejoran ~7 %, y los conceptos que hoy están entre 93 % y 100 % pasarían a cumplir.

## Resumen ejecutivo

| Boca | Pts hoy | Pts proyectados (medibles) | Pts sin medir / sin objetivo | Alertas principales |
|---|---|---|---|---|
| 889 Susana | 14.5 | **59.4** | 20 | Croselling 59,3 % muy exigente |
| 1089 Rufino | 14.2 | **51.3** | 20 | Comidas al límite, App |
| 1080 Gualeguaychú | 0.0 | **45.0** | 20 | Todos los ratios apenas abajo del mínimo |
| 1101 Concordia | 13.4 | **41.1** | 20 | **Diesel 89 %** |
| 1133 La Paz | 18.8 | **40.7** | 20 | Naftas al límite, App 5,4 % |
| 1082 Venado Tuerto | 22.4 | **37.3** | 15 | **Naftas 86 %**, Mix GO sin objetivo |
| 888 Rafaela | 0.0 | **33.8** | 40 | Croselling/Comidas sin dato real |
| 931 Santa Fe | 14.4 | **33.3** | 30 | **Lubricantes 33 %**, sin obj. tienda |
| 887 Ceres | 14.4 | **32.1** | 40 | **Diesel 91 %**, sin obj. tienda |
| 1046 Firmat | 21.6 | **31.6** | 20 | **Diesel 90 %**, naftas al límite |
| 1006 Tortugas | 11.8 | **29.1** | 40 | Diesel 97 %, sin obj. tienda |
| 1239 Curuzú Cuatiá | 12.4 | **28.1** | 10 | **Diesel 80 %**, naftas al límite |
| 1240 Paso de los Libres | 17.4 | **17.4** | 40 | **Diesel 79 %**, sin obj. tienda |

"Pts sin medir" = lubricantes sin dato real, croselling/comidas sin objetivo o sin dato, y cliente incógnito + auditoría de imagen (10 pts, todavía sin evaluar en ninguna boca).

## 1. Objetivos a reclamar por altos (proyección muy por debajo del mínimo)

| Boca | Concepto | Mínimo | Proyección cierre | % del mín. | Ritmo actual → necesario | Pts en juego |
|---|---|---|---|---|---|---|
| 931 Santa Fe | Lubricantes | 1,54 m3 | 0,51 m3 | **33 %** | 0,016 → 0,08 m3/día | 10 |
| 1240 Paso de los Libres | Diesel | 45,0 m3 | 35,4 m3 | **79 %** | 1,14 → 1,71 m3/día | 15 |
| 1239 Curuzú Cuatiá | Diesel | 181,5 m3 | 146,1 m3 | **80 %** | 4,7 → 6,8 m3/día | 15 |
| 1082 Venado Tuerto | Naftas | 452,5 m3 | 389,7 m3 | **86 %** | 12,6 → 16,3 m3/día | 20 |
| 1101 Concordia | Diesel | 74,4 m3 | 66,4 m3 | **89 %** | 2,1 → 2,6 m3/día | 15 |
| 1046 Firmat | Diesel | 234,9 m3 | 210,4 m3 | **90 %** | 6,8 → 8,2 m3/día | 15 |
| 887 Ceres | Diesel | 136,8 m3 | 124,0 m3 | **91 %** | 4,0 → 4,75 m3/día | 15 |

Notas:
- **Diesel es el problema transversal**: 8 de 13 bocas proyectan por debajo del mínimo (las 6 de la tabla, más Santa Fe 95 %, Venado Tuerto 96 % y Tortugas 97 %, que todavía son alcanzables). Vale consultar si el objetivo de diesel se armó sobre una base estacional (cosecha/siembra) que no se está dando este mes.
- Ratios con objetivo llamativamente alto (revisar base de cálculo): **Susana croselling 59,3 %** (resto de la red 5–25 %), **Gualeguaychú mix GO 77,6 %**, **Santa Fe app 20 %**.

## 2. Objetivos faltantes o datos no informados (reclamo administrativo)

- **Sin objetivo de Croselling ni de Comidas y Café** (20 pts que no se pueden ganar): **887 Ceres, 931 Santa Fe, 1006 Tortugas, 1240 Paso de los Libres**. Pedir que se carguen o que se redistribuyan esos puntos.
- **Con objetivo pero sin dato real de tienda:** **888 Rafaela** (croselling y comidas, 20 pts). Además su objetivo de comidas (250 un.) es muy bajo vs. la red → posible mala vinculación tienda–boca.
- **Lubricantes sin dato real** en 10 bocas (Ceres, Rafaela, Susana, Tortugas, Firmat, Gualeguaychú, Rufino, Concordia, La Paz, Paso de los Libres). Solo informan Venado Tuerto, Santa Fe y Curuzú. Confirmar si es falta de compras en el mes o falta de carga del dato (10 pts por boca).
- **1082 Venado Tuerto – Mix GO sin objetivo** y real 100 % (hoy suma 5 pts). Dato atípico; conviene aclararlo para que no lo corrijan a la baja al cierre.
- **Cliente incógnito y Auditoría de imagen**: ninguna boca evaluada aún (10 pts). Además son **condición básica** (≥75 % incógnito, ≥80 % imagen): prepararse.

## 3. Puntos "baratos" (a menos de 1 punto porcentual del mínimo)

| Boca | Concepto | Real | Mínimo | Brecha | Pts |
|---|---|---|---|---|---|
| 1239 Curuzú Cuatiá | Croselling | 5,1 % | 5,4 % | 0,3 pp | 10 |
| 888 Rafaela | Mix naftas | 24,8 % | 25,2 % | 0,4 pp | 10 |
| 1082 Venado Tuerto | Mix naftas | 26,7 % | 27,2 % | 0,5 pp | 10 |
| 1089 Rufino | Croselling | 13,6 % | 14,2 % | 0,6 pp | 10 |
| 1080 Gualeguaychú | App YPF | 13,4 % | 14,0 % | 0,6 pp | 10 |
| 1101 Concordia | App YPF | 12,1 % | 12,7 % | 0,6 pp | 10 |
| 888 Rafaela | App YPF | 11,2 % | 11,9 % | 0,7 pp | 10 |
| 1006 Tortugas | Mix naftas | 31,4 % | 32,1 % | 0,7 pp | 10 |
| 931 Santa Fe | App YPF | 19,2 % | 20,0 % | 0,8 pp | 10 |
| 1080 Gualeguaychú | Croselling | 14,1 % | 15,0 % | 0,9 pp | 10 |
| 1101 Concordia | Mix naftas | 24,8 % | 25,7 % | 0,9 pp | 10 |

Volúmenes que se definen al cierre (entre 97 % y 100 % del mínimo): naftas de **Firmat, La Paz, Curuzú Cuatiá y Paso de los Libres**; diesel de **Tortugas**. Cualquier día flojo los deja en 0; uno bueno les da 14–20 pts.

**Penetración App YPF** es el concepto más flojo de la red: 10 de 13 bocas debajo del mínimo (peores: La Paz 5,4 vs 8,0; Curuzú 5,9 vs 8,0; Rufino 6,8 vs 8,4; Firmat 9,7 vs 11,2). Una campaña de alta de app en playa impacta en casi todas las bocas.

## 4. Detalle por boca

Columnas: *Proy. cierre* = proyección lineal a fin de mes (solo volúmenes y unidades; "=" significa que el ratio se toma como está hoy). *Proy/Mín* = proyección como % del objetivo mínimo.

### 887-ACA CERES

| Concepto | Pts | Mín | Máx | Real | Proy. cierre | Proy/Mín | Pts hoy | Pts proy. |
|---|---|---|---|---|---|---|---|---|
| Diesel m3 | 15 | 136.8 | 151.2 | 56.0 | 124.0 | 91 % | 0.0 | 0.0 |
| Naftas m3 | 20 | 90.4 | 105.5 | 45.0 | 99.64 | 110 % | 0.0 | 17.7 |
| Mix Infinia naftas % | 10 | 29.9 | 33.1 | 33.3 | = | 111 % | 10.0 | 10.0 |
| Mix Infinia GO % | 5 | 57.2 | 63.3 | 60.7 | = | 106 % | 4.4 | 4.4 |
| Lubricantes m3 | 10 | 0.61 | 0.68 | -- | = | -- | -- | -- |
| Croselling % | 10 | -- | -- | -- | = | -- | -- | -- |
| Comidas y Café (un.) | 10 | -- | -- | -- | = | -- | -- | -- |
| Penetración App % | 10 | 8.9 | 12.9 | 7.6 | = | 85 % | 0.0 | 0.0 |
| Cliente incógnito | 5 | 80.0 | 100.0 | -- | = | -- | -- | -- |
| Auditoría imagen | 5 | 80.0 | 100.0 | -- | = | -- | -- | -- |

**Puntos hoy: 14.4 / 100 · Proyección cierre (con lo medible): 32.1 / 100**

- **Diesel en riesgo:** ritmo 4,0 m3/día vs 4,75 necesarios → cierra ~124 m3 (91 % del mínimo). Requiere empuje fuerte o revisión del objetivo.
- **Naftas OK** (~110 % del mínimo) y mix Infinia naftas en el máximo.
- **App YPF 7,6 % vs 8,9 %**: faltan 1,3 pp → 10 pts en juego.
- **Reclamar:** Croselling y Comidas y Café **sin objetivo cargado** (20 pts que hoy no se pueden ganar). Lubricantes sin dato real.

### 888-ACA RAFAELA

| Concepto | Pts | Mín | Máx | Real | Proy. cierre | Proy/Mín | Pts hoy | Pts proy. |
|---|---|---|---|---|---|---|---|---|
| Diesel m3 | 15 | 86.8 | 96.0 | 43.0 | 95.21 | 110 % | 0.0 | 14.6 |
| Naftas m3 | 20 | 234.1 | 273.2 | 121.0 | 267.93 | 114 % | 0.0 | 19.2 |
| Mix Infinia naftas % | 10 | 25.2 | 27.9 | 24.8 | = | 98 % | 0.0 | 0.0 |
| Mix Infinia GO % | 5 | 57.3 | 63.3 | 53.5 | = | 93 % | 0.0 | 0.0 |
| Lubricantes m3 | 10 | 0.72 | 0.8 | -- | = | -- | -- | -- |
| Croselling % | 10 | 5.0 | 8.4 | -- | = | -- | -- | -- |
| Comidas y Café (un.) | 10 | 250.0 | 275.0 | -- | = | -- | -- | -- |
| Penetración App % | 10 | 11.9 | 15.9 | 11.2 | = | 94 % | 0.0 | 0.0 |
| Cliente incógnito | 5 | 80.0 | 100.0 | -- | = | -- | -- | -- |
| Auditoría imagen | 5 | 80.0 | 100.0 | -- | = | -- | -- | -- |

**Puntos hoy: 0.0 / 100 · Proyección cierre (con lo medible): 33.8 / 100**

- **Volúmenes bien encaminados:** diesel ~110 % y naftas ~114 % del mínimo (≈29 pts a cierre).
- **Mixes por debajo del mínimo:** naftas 24,8 % vs 25,2 % (a 0,4 pp, recuperable) y GO 53,5 % vs 57,3 %.
- **App 11,2 % vs 11,9 %** (a 0,7 pp).
- **Reclamar:** Croselling y Comidas tienen objetivo pero **no informan dato real** (20 pts); Lubricantes sin dato. Además el objetivo de Comidas (250 un.) es atípicamente bajo vs. el resto de la red: verificar si la tienda está bien vinculada a la boca. Hoy 0 puntos en el tablero.

### 889-ACA SUSANA

| Concepto | Pts | Mín | Máx | Real | Proy. cierre | Proy/Mín | Pts hoy | Pts proy. |
|---|---|---|---|---|---|---|---|---|
| Diesel m3 | 15 | 255.6 | 282.5 | 159.0 | 352.07 | 138 % | 0.0 | 15.0 |
| Naftas m3 | 20 | 189.4 | 221.0 | 102.0 | 225.86 | 119 % | 0.0 | 20.0 |
| Mix Infinia naftas % | 10 | 30.7 | 33.9 | 33.3 | = | 108 % | 9.5 | 9.4 |
| Mix Infinia GO % | 5 | 41.7 | 46.1 | 47.8 | = | 115 % | 5.0 | 5.0 |
| Lubricantes m3 | 10 | 0.4 | 0.45 | -- | = | -- | -- | -- |
| Croselling % | 10 | 59.3 | 72.5 | 57.9 | = | 98 % | 0.0 | 0.0 |
| Comidas y Café (un.) | 10 | 5548.0 | 6103.0 | 3191.0 | 7609.31 | 137 % | 0.0 | 10.0 |
| Penetración App % | 10 | 16.4 | 19.4 | 15.0 | = | 92 % | 0.0 | 0.0 |
| Cliente incógnito | 5 | 80.0 | 100.0 | -- | = | -- | -- | -- |
| Auditoría imagen | 5 | 80.0 | 100.0 | -- | = | -- | -- | -- |

**Puntos hoy: 14.5 / 100 · Proyección cierre (con lo medible): 59.4 / 100**

- **La mejor proyectada** (~59 pts medibles): diesel ~138 %, naftas ~119 %, comidas ~137 % del mínimo, mixes en zona de puntaje.
- **Croselling 57,9 % vs 59,3 %**: muy cerca, pero el objetivo es **muy alto vs. el resto de la red** (5–25 %). Si no se cruza, vale reclamar/consultar la base de cálculo.
- **App 15,0 % vs 16,4 %**: 1,4 pp abajo.
- Lubricantes sin dato real.

### 931-ACA SANTA FE

| Concepto | Pts | Mín | Máx | Real | Proy. cierre | Proy/Mín | Pts hoy | Pts proy. |
|---|---|---|---|---|---|---|---|---|
| Diesel m3 | 15 | 84.3 | 93.1 | 36.0 | 79.71 | 95 % | 0.0 | 0.0 |
| Naftas m3 | 20 | 238.5 | 278.2 | 122.0 | 270.14 | 113 % | 0.0 | 18.8 |
| Mix Infinia naftas % | 10 | 37.2 | 41.1 | 41.0 | = | 110 % | 9.9 | 9.9 |
| Mix Infinia GO % | 5 | 77.6 | 85.7 | 83.3 | = | 107 % | 4.6 | 4.6 |
| Lubricantes m3 | 10 | 1.54 | 1.71 | 0.23 | 0.51 | 33 % | 0.0 | 0.0 |
| Croselling % | 10 | -- | -- | -- | = | -- | -- | -- |
| Comidas y Café (un.) | 10 | -- | -- | -- | = | -- | -- | -- |
| Penetración App % | 10 | 20.0 | 23.0 | 19.2 | = | 96 % | 0.0 | 0.0 |
| Cliente incógnito | 5 | 80.0 | 100.0 | -- | = | -- | -- | -- |
| Auditoría imagen | 5 | 80.0 | 100.0 | -- | = | -- | -- | -- |

**Puntos hoy: 14.5 / 100 · Proyección cierre (con lo medible): 33.3 / 100**

- **Lubricantes — RECLAMAR:** objetivo 1,54 m3, el más alto de la red; ritmo actual proyecta ~0,51 m3 (**33 % del mínimo**). Inalcanzable salvo una compra puntual grande.
- **Diesel** ~95 % del mínimo (faltan ~0,3 m3/día de ritmo): alcanzable con empuje.
- Naftas OK (~113 %), mixes casi al máximo.
- **App 19,2 % vs 20,0 %**: a 0,8 pp (objetivo de app más exigente de la red).
- **Reclamar:** Croselling y Comidas **sin objetivo** (20 pts).

### 1006-ACA TORTUGAS

| Concepto | Pts | Mín | Máx | Real | Proy. cierre | Proy/Mín | Pts hoy | Pts proy. |
|---|---|---|---|---|---|---|---|---|
| Diesel m3 | 15 | 77.5 | 85.6 | 34.0 | 75.29 | 97 % | 0.0 | 0.0 |
| Naftas m3 | 20 | 71.1 | 83.0 | 35.0 | 77.5 | 109 % | 0.0 | 17.2 |
| Mix Infinia naftas % | 10 | 32.1 | 35.4 | 31.4 | = | 98 % | 0.0 | 0.0 |
| Mix Infinia GO % | 5 | 40.6 | 44.8 | 44.1 | = | 109 % | 4.7 | 4.8 |
| Lubricantes m3 | 10 | 0.59 | 0.65 | -- | = | -- | -- | -- |
| Croselling % | 10 | -- | -- | -- | = | -- | -- | -- |
| Comidas y Café (un.) | 10 | -- | -- | -- | = | -- | -- | -- |
| Penetración App % | 10 | 12.0 | 16.0 | 12.1 | = | 101 % | 7.1 | 7.1 |
| Cliente incógnito | 5 | 80.0 | 100.0 | -- | = | -- | -- | -- |
| Auditoría imagen | 5 | 80.0 | 100.0 | -- | = | -- | -- | -- |

**Puntos hoy: 11.8 / 100 · Proyección cierre (con lo medible): 29.1 / 100**

- **Diesel justo:** ~97 % del mínimo (2,43 vs 2,56 m3/día necesarios). Muy cerca, empujar.
- Naftas OK (~109 %). Mix naftas 31,4 % vs 32,1 % (a 0,7 pp).
- App 12,1 %: apenas sobre el mínimo (12,0 %), sostener.
- **Reclamar:** Croselling y Comidas **sin objetivo** (20 pts). Lubricantes sin dato.

### 1046-ACA FIRMAT

| Concepto | Pts | Mín | Máx | Real | Proy. cierre | Proy/Mín | Pts hoy | Pts proy. |
|---|---|---|---|---|---|---|---|---|
| Diesel m3 | 15 | 234.9 | 259.6 | 95.0 | 210.36 | 90 % | 0.0 | 0.0 |
| Naftas m3 | 20 | 206.2 | 240.6 | 92.0 | 203.71 | 99 % | 0.0 | 0.0 |
| Mix Infinia naftas % | 10 | 25.9 | 28.6 | 26.1 | = | 101 % | 7.2 | 7.2 |
| Mix Infinia GO % | 5 | 42.7 | 47.2 | 46.3 | = | 108 % | 4.7 | 4.7 |
| Lubricantes m3 | 10 | 0.31 | 0.35 | -- | = | -- | -- | -- |
| Croselling % | 10 | 20.5 | 25.1 | 24.6 | = | 120 % | 9.7 | 9.7 |
| Comidas y Café (un.) | 10 | 4480.0 | 4928.0 | 2446.0 | 5832.77 | 130 % | 0.0 | 10.0 |
| Penetración App % | 10 | 11.2 | 15.2 | 9.7 | = | 87 % | 0.0 | 0.0 |
| Cliente incógnito | 5 | 80.0 | 100.0 | -- | = | -- | -- | -- |
| Auditoría imagen | 5 | 80.0 | 100.0 | -- | = | -- | -- | -- |

**Puntos hoy: 21.6 / 100 · Proyección cierre (con lo medible): 31.6 / 100**

- **Diesel en riesgo:** objetivo 234,9 m3, ritmo proyecta ~210 m3 (90 %). Necesita 8,2 m3/día vs 6,8 actuales → **candidato a reclamo**.
- **Naftas al límite:** ~99 % del mínimo, se define en los últimos días.
- Comidas OK (~130 %), croselling cerca del máximo, mix GO en zona.
- **App 9,7 % vs 11,2 %** (1,5 pp abajo). Lubricantes sin dato.

### 1080-ACA GUALEGUAYCHU

| Concepto | Pts | Mín | Máx | Real | Proy. cierre | Proy/Mín | Pts hoy | Pts proy. |
|---|---|---|---|---|---|---|---|---|
| Diesel m3 | 15 | 72.0 | 79.6 | 39.0 | 86.36 | 120 % | 0.0 | 15.0 |
| Naftas m3 | 20 | 241.0 | 281.2 | 128.0 | 283.43 | 118 % | 0.0 | 20.0 |
| Mix Infinia naftas % | 10 | 25.3 | 27.9 | 23.4 | = | 92 % | 0.0 | 0.0 |
| Mix Infinia GO % | 5 | 77.6 | 85.8 | 74.4 | = | 96 % | 0.0 | 0.0 |
| Lubricantes m3 | 10 | 1.06 | 1.18 | -- | = | -- | -- | -- |
| Croselling % | 10 | 15.0 | 18.4 | 14.1 | = | 94 % | 0.0 | 0.0 |
| Comidas y Café (un.) | 10 | 1777.0 | 1954.0 | 1018.0 | 2427.54 | 137 % | 0.0 | 10.0 |
| Penetración App % | 10 | 14.0 | 17.5 | 13.4 | = | 96 % | 0.0 | 0.0 |
| Cliente incógnito | 5 | 80.0 | 100.0 | -- | = | -- | -- | -- |
| Auditoría imagen | 5 | 80.0 | 100.0 | -- | = | -- | -- | -- |

**Puntos hoy: 0.0 / 100 · Proyección cierre (con lo medible): 45.0 / 100**

- **Volúmenes muy bien:** diesel ~120 % y naftas ~118 % del mínimo, comidas ~137 %. Con eso solo suma ~45 pts.
- **Todo lo de ratios está apenas abajo del mínimo** (0 pts hoy): mix naftas 23,4 vs 25,3; **mix GO 74,4 vs 77,6** (objetivo muy alto); croselling 14,1 vs 15,0; app 13,4 vs 14,0. Hay ~30 pts recuperables con acciones comerciales.
- Lubricantes: objetivo 1,06 m3 y sin dato real — verificar.

### 1082-ACA VENADO TUERTO

| Concepto | Pts | Mín | Máx | Real | Proy. cierre | Proy/Mín | Pts hoy | Pts proy. |
|---|---|---|---|---|---|---|---|---|
| Diesel m3 | 15 | 105.7 | 116.8 | 46.0 | 101.86 | 96 % | 0.0 | 0.0 |
| Naftas m3 | 20 | 452.5 | 527.9 | 176.0 | 389.71 | 86 % | 0.0 | 0.0 |
| Mix Infinia naftas % | 10 | 27.2 | 30.0 | 26.7 | = | 98 % | 0.0 | 0.0 |
| Mix Infinia GO % | 5 | -- | -- | 100.0 | = | -- | 5.0 | -- |
| Lubricantes m3 | 10 | 0.33 | 0.37 | 0.27 | 0.6 | 182 % | 0.0 | 10.0 |
| Croselling % | 10 | 11.3 | 13.8 | 14.9 | = | 132 % | 10.0 | 10.0 |
| Comidas y Café (un.) | 10 | 2466.0 | 2713.0 | 1409.0 | 3359.92 | 136 % | 0.0 | 10.0 |
| Penetración App % | 10 | 15.0 | 18.5 | 15.4 | = | 103 % | 7.4 | 7.3 |
| Cliente incógnito | 5 | 80.0 | 100.0 | -- | = | -- | -- | -- |
| Auditoría imagen | 5 | 80.0 | 100.0 | -- | = | -- | -- | -- |

**Puntos hoy: 22.4 / 100 · Proyección cierre (con lo medible): 37.3 / 100**

- **Naftas — RECLAMAR:** objetivo 452,5 m3 (el más alto de la red); ritmo 12,6 m3/día proyecta ~390 m3 (**86 %**). Necesitaría 16,3 m3/día el resto del mes.
- **Diesel** ~96 % del mínimo: alcanzable con empuje.
- **Mix GO sin objetivo** y real 100 % (5 pts otorgados): dato raro (implica 0 venta de D500). Verificar antes de que lo corrijan en contra.
- Lubricantes, croselling y comidas bien encaminados. Mix naftas 26,7 vs 27,2 (a 0,5 pp).

### 1089-ACA RUFINO

| Concepto | Pts | Mín | Máx | Real | Proy. cierre | Proy/Mín | Pts hoy | Pts proy. |
|---|---|---|---|---|---|---|---|---|
| Diesel m3 | 15 | 75.3 | 83.2 | 35.0 | 77.5 | 103 % | 0.0 | 11.8 |
| Naftas m3 | 20 | 127.9 | 149.2 | 64.0 | 141.71 | 111 % | 0.0 | 17.9 |
| Mix Infinia naftas % | 10 | 21.8 | 24.1 | 31.3 | = | 144 % | 10.0 | 10.0 |
| Mix Infinia GO % | 5 | 65.3 | 72.1 | 68.6 | = | 105 % | 4.2 | 4.2 |
| Lubricantes m3 | 10 | 0.33 | 0.37 | -- | = | -- | -- | -- |
| Croselling % | 10 | 14.2 | 17.3 | 13.6 | = | 96 % | 0.0 | 0.0 |
| Comidas y Café (un.) | 10 | 1344.0 | 1478.0 | 572.0 | 1364.0 | 102 % | 0.0 | 7.4 |
| Penetración App % | 10 | 8.4 | 12.4 | 6.8 | = | 81 % | 0.0 | 0.0 |
| Cliente incógnito | 5 | 80.0 | 100.0 | -- | = | -- | -- | -- |
| Auditoría imagen | 5 | 80.0 | 100.0 | -- | = | -- | -- | -- |

**Puntos hoy: 14.2 / 100 · Proyección cierre (con lo medible): 51.3 / 100**

- Volúmenes OK pero justos: diesel ~103 %, naftas ~111 %.
- **Comidas al límite** (~101 % del mínimo) — cualquier baja lo deja en 0.
- Croselling 13,6 vs 14,2 (a 0,6 pp). **App 6,8 vs 8,4** (1,6 pp abajo).
- Mix naftas muy por encima (31,3 % vs 24,1 % máx). Lubricantes sin dato.

### 1101-ACA CONCORDIA

| Concepto | Pts | Mín | Máx | Real | Proy. cierre | Proy/Mín | Pts hoy | Pts proy. |
|---|---|---|---|---|---|---|---|---|
| Diesel m3 | 15 | 74.4 | 82.3 | 30.0 | 66.43 | 89 % | 0.0 | 0.0 |
| Naftas m3 | 20 | 227.1 | 265.0 | 113.0 | 250.21 | 110 % | 0.0 | 17.7 |
| Mix Infinia naftas % | 10 | 25.7 | 28.4 | 24.8 | = | 96 % | 0.0 | 0.0 |
| Mix Infinia GO % | 5 | 71.5 | 79.1 | 83.3 | = | 116 % | 5.0 | 5.0 |
| Lubricantes m3 | 10 | 1.25 | 1.39 | -- | = | -- | -- | -- |
| Croselling % | 10 | 6.1 | 8.4 | 7.2 | = | 118 % | 8.4 | 8.4 |
| Comidas y Café (un.) | 10 | 970.0 | 1067.0 | 501.0 | 1194.69 | 123 % | 0.0 | 10.0 |
| Penetración App % | 10 | 12.7 | 16.7 | 12.1 | = | 95 % | 0.0 | 0.0 |
| Cliente incógnito | 5 | 80.0 | 100.0 | -- | = | -- | -- | -- |
| Auditoría imagen | 5 | 80.0 | 100.0 | -- | = | -- | -- | -- |

**Puntos hoy: 13.4 / 100 · Proyección cierre (con lo medible): 41.1 / 100**

- **Diesel en riesgo:** ~66 m3 proyectados vs 74,4 (89 %) → **candidato a reclamo** o acción fuerte.
- Naftas OK (~110 %), comidas OK (~123 %), mix GO y croselling sumando.
- Mix naftas 24,8 vs 25,7; App 12,1 vs 12,7.
- **Lubricantes:** objetivo 1,25 m3 (de los más altos) y sin dato real — verificar.

### 1133-ACA LA PAZ

| Concepto | Pts | Mín | Máx | Real | Proy. cierre | Proy/Mín | Pts hoy | Pts proy. |
|---|---|---|---|---|---|---|---|---|
| Diesel m3 | 15 | 102.8 | 113.6 | 48.0 | 106.29 | 103 % | 0.0 | 12.0 |
| Naftas m3 | 20 | 235.3 | 274.6 | 106.0 | 234.71 | 100 % | 0.0 | 0.0 |
| Mix Infinia naftas % | 10 | 18.6 | 20.6 | 18.9 | = | 102 % | 7.4 | 7.4 |
| Mix Infinia GO % | 5 | 60.4 | 66.7 | 62.5 | = | 104 % | 4.0 | 4.0 |
| Lubricantes m3 | 10 | 0.92 | 1.03 | -- | = | -- | -- | -- |
| Croselling % | 10 | 6.5 | 8.4 | 6.7 | = | 103 % | 7.4 | 7.3 |
| Comidas y Café (un.) | 10 | 585.0 | 643.0 | 320.0 | 763.08 | 130 % | 0.0 | 10.0 |
| Penetración App % | 10 | 8.0 | 12.0 | 5.4 | = | 68 % | 0.0 | 0.0 |
| Cliente incógnito | 5 | 80.0 | 100.0 | -- | = | -- | -- | -- |
| Auditoría imagen | 5 | 80.0 | 100.0 | -- | = | -- | -- | -- |

**Puntos hoy: 18.8 / 100 · Proyección cierre (con lo medible): 40.7 / 100**

- Diesel OK (~103 %). **Naftas al límite** (~99,7 %): se define al cierre.
- Mixes y croselling sumando. Comidas OK (~130 %).
- **App 5,4 % vs 8,0 %**: la brecha más grande de la red (68 % del mínimo).
- Lubricantes sin dato.

### 1239-ACA CURUZU CUATIA

| Concepto | Pts | Mín | Máx | Real | Proy. cierre | Proy/Mín | Pts hoy | Pts proy. |
|---|---|---|---|---|---|---|---|---|
| Diesel m3 | 15 | 181.5 | 200.6 | 66.0 | 146.14 | 80 % | 0.0 | 0.0 |
| Naftas m3 | 20 | 262.5 | 306.3 | 117.0 | 259.07 | 99 % | 0.0 | 0.0 |
| Mix Infinia naftas % | 10 | 24.4 | 27.0 | 24.8 | = | 102 % | 7.4 | 7.5 |
| Mix Infinia GO % | 5 | 61.0 | 67.4 | 68.2 | = | 112 % | 5.0 | 5.0 |
| Lubricantes m3 | 10 | 0.68 | 0.75 | 0.31 | 0.69 | 102 % | 0.0 | 7.4 |
| Croselling % | 10 | 5.4 | 8.4 | 5.1 | = | 94 % | 0.0 | 0.0 |
| Comidas y Café (un.) | 10 | 1480.0 | 1628.0 | 646.0 | 1540.46 | 104 % | 0.0 | 8.2 |
| Penetración App % | 10 | 8.0 | 12.0 | 5.9 | = | 74 % | 0.0 | 0.0 |
| Cliente incógnito | 5 | 80.0 | 100.0 | -- | = | -- | -- | -- |
| Auditoría imagen | 5 | 80.0 | 100.0 | -- | = | -- | -- | -- |

**Puntos hoy: 12.4 / 100 · Proyección cierre (con lo medible): 28.1 / 100**

- **Diesel — RECLAMAR:** objetivo 181,5 m3, proyecta ~146 m3 (**80 %**). Necesita 6,8 m3/día vs 4,7 actuales.
- **Naftas al límite** (~99 %). Comidas justa (~104 %). Lubricantes justo (~101 %).
- Croselling 5,1 vs 5,4 (a 0,3 pp). **App 5,9 vs 8,0**.
- Es la única boca con todos los conceptos con objetivo y casi todos con dato (solo faltan auditorías).

### 1240-ACA PASO DE LOS LIBRES

| Concepto | Pts | Mín | Máx | Real | Proy. cierre | Proy/Mín | Pts hoy | Pts proy. |
|---|---|---|---|---|---|---|---|---|
| Diesel m3 | 15 | 45.0 | 49.8 | 16.0 | 35.43 | 79 % | 0.0 | 0.0 |
| Naftas m3 | 20 | 69.4 | 80.9 | 31.0 | 68.64 | 99 % | 0.0 | 0.0 |
| Mix Infinia naftas % | 10 | 13.7 | 15.2 | 16.1 | = | 118 % | 10.0 | 10.0 |
| Mix Infinia GO % | 5 | 35.6 | 39.4 | 31.2 | = | 88 % | 0.0 | 0.0 |
| Lubricantes m3 | 10 | 0.58 | 0.64 | -- | = | -- | -- | -- |
| Croselling % | 10 | -- | -- | -- | = | -- | -- | -- |
| Comidas y Café (un.) | 10 | -- | -- | -- | = | -- | -- | -- |
| Penetración App % | 10 | 8.1 | 12.1 | 8.6 | = | 106 % | 7.4 | 7.4 |
| Cliente incógnito | 5 | 80.0 | 100.0 | -- | = | -- | -- | -- |
| Auditoría imagen | 5 | 80.0 | 100.0 | -- | = | -- | -- | -- |

**Puntos hoy: 17.4 / 100 · Proyección cierre (con lo medible): 17.4 / 100**

- **Diesel — RECLAMAR:** proyecta ~35 m3 vs 45 (**79 %**, el peor de la red en %).
- **Naftas al límite** (~99 %).
- **Mix GO 31,2 % vs 35,6 %**. Mix naftas y app sumando.
- **Reclamar:** Croselling y Comidas **sin objetivo** (20 pts). Lubricantes sin dato. Es la boca con peor proyección (~17 pts medibles).



---

## Anexo: estación incorporada — 3233 ACA COLÓN (datos al 14/10/2026)

| Concepto | Pts | Mín | Máx | Real | Proy. cierre | Proy/Mín | Pts hoy | Pts proy. |
|---|---|---|---|---|---|---|---|---|
| Diesel m3 | 15 | 106,6 | 117,8 | 39,0 | 86,4 | **81 %** | 0,0 | 0,0 |
| Naftas m3 | 20 | 46,0 | 53,7 | 21,0 | 46,5 | 101 % | 0,0 | 14,4 |
| Mix Infinia naftas % | 10 | 35,0 | 38,7 | 28,6 | = | 82 % | 0,0 | 0,0 |
| Mix Infinia GO % | 5 | 34,1 | 37,7 | 53,8 | = | 158 % | 5,0 | 5,0 |
| Lubricantes m3 | 10 | 0,58 | 0,65 | -- | | | -- | -- |
| Croselling % | 10 | -- | -- | -- | | | -- | -- |
| Comidas y Café | 10 | -- | -- | -- | | | -- | -- |
| App YPF % | 10 | 19,7 | 22,7 | 21,0 | = | 107 % | 8,4 | 8,3 |
| Cliente incógnito / Auditoría imagen | 10 | 80 | 100 | -- | | | -- | -- |

**Puntos hoy: 13,4 · Proyección: ~27,7 (40 pts sin medir).**

- **Diesel – reclamar:** proyecta 86,4 m3 contra un mínimo de 106,6 m3 (81 %). Necesita 4,0 m3/día contra 2,8 actuales (+43 %). Con Colón, ya son 9 de 14 estaciones con diesel por debajo del mínimo.
- **Mix Infinia naftas – reclamar:** el objetivo de 35,0 % es el segundo más alto de la red (la mediana es 25,8 %) y el real es 28,6 %, a 6,4 pp. En cambio, el objetivo de Mix GO (34,1 %) es bajo para su real de 53,8 %. Parece que las metas de mix están mal calibradas.
- **Naftas al límite:** proyecta 101 % del mínimo, un objetivo bajo para el volumen de la estación. No hay que aflojar.
- **App YPF** cumple (21,0 % contra 19,7 %).
- **Faltantes:** no tiene objetivo de croselling ni de comidas (20 pts) y lubricantes no muestra dato.
