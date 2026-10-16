---
name: avance-programa-mas-ypf
description: Analiza los tableros PDF "Performance de Red" del Programa +YPF de las estaciones ACA, proyecta el cierre de mes y detecta objetivos para reclamar a YPF por altos, metas faltantes o datos no informados. Arma el informe general, un PDF por estación, el mail de reclamo a YPF y un mail por estación con dónde seguir trabajando (Gmail). Usar siempre que el usuario suba o mencione tableros +YPF / Performance de Red / PDFs de bocas ACA (ej. "888-ACA RAFAELA.pdf"), pida ver "cómo venimos con el programa", "qué objetivos reclamar", "mandar el avance a las estaciones" o "armar el reclamo a YPF", aunque no nombre la skill.
---

# Avance Programa +YPF (red ACA)

Flujo mensual: leer los tableros PDF de YPF de cada estación, entender dónde está cada indicador, proyectar el cierre del mes y producir:

1. un análisis general (qué reclamar y dónde están los puntos fáciles);
2. un mail de reclamo a YPF por objetivos altos, metas faltantes y datos que no aparecen;
3. un mail para cada estación, para mandar junto con su tablero de YPF;
4. opcionalmente, un PDF propio de una página por estación.

El usuario es un coordinador comercial y no programador. Entrégale siempre cosas que pueda abrir o mandar: PDFs, borradores de Gmail o texto para copiar. Nunca le pases un `.py`, un `.csv` o una ruta del repositorio como entregable. Escríbele en español rioplatense.

## Los tableros

Cada PDF tiene una página titulada `<código>-ACA <LOCALIDAD>`, por ejemplo `888-ACA RAFAELA`. Trae una tabla con estas columnas: Concepto, Objetivo mínima, Objetivo máxima, Real, % Cumplimiento, Puntos posibles, Puntos obtenidos y Fecha de actualización. Los conceptos y sus puntos (suman 100) son:

| Concepto | Pts | Tipo |
|---|---|---|
| Volumen diesel m3 (Infinia Diesel + D500) | 15 | acumulado del mes |
| Volumen naftas m3 (Infinia + Súper) | 20 | acumulado del mes |
| Mix Infinia naftas | 10 | ratio |
| Mix Infinia GO | 5 | ratio |
| Volumen lubricantes m3 | 10 | acumulado del mes |
| Croselling | 10 | ratio (tienda) |
| Unidades Comidas y Café | 10 | acumulado del mes (tienda) |
| Penetración App YPF | 10 | ratio |
| Cliente incógnito | 5 | auditoría |
| Auditoría de imagen | 5 | auditoría |

"--" significa sin dato o sin objetivo. Croselling y comidas suelen actualizarse un día antes que el resto.

**Escala de puntaje** (deducida de los PDFs, confirmala con los valores de % Cumplimiento):
- debajo del mínimo: 0 %;
- en el mínimo: 70 %;
- en el máximo: 100 %;
- lineal entre el mínimo y el máximo.

No hay puntaje parcial debajo del mínimo, así que quedar al 99 % del mínimo vale cero. Este es el argumento central de cualquier reclamo y de los mensajes a las estaciones.

**Por qué proyectar:** a mitad de mes el tablero muestra 0 % en todos los volúmenes porque compara el acumulado parcial contra la meta del mes entero. Proyecta `real ÷ días transcurridos × días del mes` y toma los ratios tal como están. Aclara siempre este supuesto. Si los datos en realidad cierran el día anterior, la proyección mejora alrededor de un 7 % a mitad de mes.

## Paso 1: extraer y proyectar

Los scripts están en `scripts/` dentro de esta skill. Necesitan `pdftotext` (poppler) y, para los PDFs propios, Node con Playwright y Chromium.

```bash
SK=<ruta de esta skill>/scripts
python3 $SK/analizar_pdfs.py <carpeta_con_pdfs> > datos/avance_AAAA-MM.csv
python3 $SK/candidatos_reclamo.py datos/avance_AAAA-MM.csv 95
```

`analizar_pdfs.py` genera un CSV con una fila por estación y concepto. Columnas: mínimo, máximo, real, fecha, días, % del PDF, puntos, proyección, proyección/mínimo, cumplimiento y puntos proyectados, ritmo diario actual y necesario.

**Verificá el parseo.** Compará los puntos obtenidos de cada estación contra el total "Puntos obtenidos" del PDF (pueden diferir ±0,1 por redondeo). Mirá también un PDF como imagen (`pdftoppm -r 60 -png`) para confirmar que no cambió el formato. Si YPF agrega o renombra conceptos, ajustá `CONCEPTOS` en `analizar_pdfs.py`.

`candidatos_reclamo.py` lista:
- los volúmenes que proyectan por debajo del umbral, con ritmo actual contra necesario y puntos en juego;
- los objetivos porcentuales atípicos contra la mediana de la red;
- los conceptos sin objetivo o sin dato real.

Usalo como punto de partida y aplicá criterio:
- **Reclamo firme:** proyección por debajo de ~92 % del mínimo, o metas que son las más altas de la red con mucha diferencia.
- **Alcanzables (93–100 %):** van como "foco" para la estación, no como reclamo.
- **Diesel en varias estaciones:** si falla en muchas a la vez, pedí además la base estacional con la que se fijaron las metas.

## Paso 2: análisis para el usuario

Respondé corto y concreto:
- **Ranking:** puntos hoy, puntos proyectados y puntos sin medir de cada estación.
- **Tabla de reclamos:** estación, concepto, mínimo, proyección, % del mínimo, ritmo actual → necesario y puntos.
- **Faltantes administrativos:** metas sin cargar, datos de tienda o lubricantes que no aparecen y auditorías pendientes. Cliente incógnito (≥75 %) y Auditoría de imagen (≥80 %) además son condición básica del programa.
- **Puntos baratos:** ratios a menos de 1 pp del mínimo y volúmenes entre 97 % y 100 %.

Guardá el informe en `informes/` si estás en el repositorio del usuario.

## Paso 3: mail de reclamo a YPF

Seguí la plantilla de `references/plantillas_mail.md`. Usá los números exactos del CSV y nada inventado. Si el usuario pide solo los objetivos altos, mandá únicamente las secciones de volumen y de porcentajes.

## Paso 4: mails a cada estación

Antes de generarlos, armá un `notas.json` con lo que no sale de las reglas automáticas:

```json
{
  "reclamos":   {"931": ["lubricantes_m3"], "1239": ["diesel_m3"], "889": ["croselling"]},
  "extra_mail": {"888": "Croselling y Comidas no muestran ventas: pedimos a YPF revisar la vinculación de la tienda."},
  "notas":      {"931": {"gestion": ["El objetivo de Lubricantes (1,54 m3) es el más alto de la red; lo estamos reclamando a YPF."]}}
}
```

- **`reclamos`:** solo lo que efectivamente va en el mail a YPF. Esos conceptos llevan la frase "Pedimos a YPF que revise este objetivo; mientras tanto, sigamos empujando".
- **`extra_mail` y `notas`:** casos especiales, como una tienda sin datos o una meta atípica a verificar.

```bash
python3 $SK/mails_estaciones.py datos/avance_AAAA-MM.csv informes/mails notas.json
```

Esto genera un `.txt` por estación y uno con todos juntos. Cada mail incluye:
- cómo leer el tablero, en tres líneas;
- puntos hoy y proyectados;
- dónde seguir trabajando, con cuánto falta y la venta diaria necesaria contra la actual;
- en qué vienen bien;
- puntos a tener en cuenta.

El mail está pensado para mandarse con el PDF original de YPF de esa estación como adjunto.

**PDF propio por estación (opcional):** sirve si el usuario quiere un informe más visual en vez del tablero de YPF, o además de él.

```bash
python3 $SK/informes_por_estacion.py datos/avance_AAAA-MM.csv informes/estaciones notas.json
NODE_PATH=$(npm root -g) node $SK/html_a_pdf.js informes/estaciones && rm informes/estaciones/*.html
```

Debe salir de una página. Revisá uno como imagen antes de entregarlo.

## Paso 5: entrega por Gmail

Con el conector de Gmail:
- **Por defecto, borradores** (`create_draft`) sin destinatario, para que el usuario complete el "Para:", adjunte el tablero y envíe. Usá `includeSignature: true`, cuerpo en texto plano y sin "[Nombre y firma]".
- **Envío directo** (`send_message`) solo si el usuario lo pide explícitamente y da la dirección. Por ejemplo, "mandámelos a mi mail" quiere decir enviarlos a esa dirección para que él los reenvíe.
- **Adjuntos:** los tableros de YPF pesan alrededor de 600 KB, demasiado para mandarlos codificados desde la sesión. Avisá que el adjunto queda manual y decí qué PDF va con cada mail.
- **Orden de envío:** el reclamo a YPF va antes que los mails a las estaciones, porque estos dicen "pedimos a YPF que revise".

Al terminar, decile al usuario dónde encontrar todo (Borradores o bandeja de entrada de tal cuenta) y los pasos para enviarlo, sin jerga técnica.
