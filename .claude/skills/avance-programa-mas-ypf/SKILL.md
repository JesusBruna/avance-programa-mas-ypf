---
name: avance-programa-mas-ypf
description: Analiza los tableros PDF "Performance de Red" del Programa +YPF de las estaciones ACA, proyecta el cierre de mes y detecta objetivos para reclamar a YPF por altos, metas faltantes o datos no informados. Arma el informe general, un PDF por estación, el mail de reclamo a YPF y un mail por estación con dónde seguir trabajando (Gmail). Usar siempre que el usuario suba o mencione tableros +YPF / Performance de Red / PDFs de bocas ACA (ej. "888-ACA RAFAELA.pdf"), pida ver "cómo venimos con el programa", "qué objetivos reclamar", "mandar el avance a las estaciones" o "armar el reclamo a YPF", aunque no nombre la skill.
---

# Avance Programa +YPF (red ACA)

Flujo mensual: leer los tableros PDF de YPF de cada estación, entender dónde está cada indicador, proyectar el cierre del mes y producir:

1. un análisis general (qué reclamar y dónde están los puntos fáciles);
2. un mail de reclamo a YPF **por estación** (cada una tiene su contacto en YPF), por objetivos altos, metas faltantes y datos que no aparecen;
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

## Paso 3: reclamos a YPF (un mail por estación)

Cada estación tiene su propio contacto en YPF, así que los reclamos van **separados por estación**: un mail por estación, nunca uno solo con toda la red.

1. **Decidí qué reclamar** con el criterio del Paso 1 y cargalo en `notas.json`. Guardalo como `datos/notas_AAAA-MM.json` para reusarlo y actualizarlo en el mes:
   - `reclamos`: código → conceptos a reclamar;
   - `extra_ypf`: código → párrafo especial (tienda sin datos, metas de mix mal calibradas, etc.).
2. **Generá los mails:**
   ```bash
   python3 $SK/reclamos_ypf.py datos/avance_AAAA-MM.csv informes/mails/reclamos_ypf datos/notas_AAAA-MM.json
   ```
   Sale un `.txt` por estación con asunto `Programa +YPF – Solicitud de revisión de objetivos <Mes AAAA> – <cód> <ESTACIÓN>`, más un archivo con todos juntos.

   Cada mail incluye:
   - cada objetivo reclamado, con mínimo y máximo, real, proyección, % del mínimo, ritmo actual contra necesario y puntos en juego;
   - comparación con la red cuando suma: "es el objetivo más alto de la red", la mediana de la red para los porcentajes, y "No es un caso aislado: X de N estaciones…" si al menos un tercio de la red está debajo del 95 %;
   - los temas administrativos de esa estación: metas de tienda sin cargar, conceptos con meta y sin dato, o sin meta y con dato. Si no los querés, usá `--sin-administrativos`.

   Las estaciones que no tienen nada para reclamar no generan mail.
3. **Revisá los textos** antes de entregarlos: los números tienen que coincidir con el CSV y el tono tiene que ser formal.

Si el usuario agrega una estación a mitad de mes, generá solo el reclamo de esa estación. No vuelvas a mandar los ya enviados.

## Paso 4: mails a cada estación

Usan el mismo `notas.json` del Paso 3 (ejemplo completo):

```json
{
  "reclamos":   {"931": ["lubricantes_m3"], "1239": ["diesel_m3"], "889": ["croselling"]},
  "extra_ypf":  {"888": "El objetivo de Comidas (250 un.) es muy bajo... verificar la vinculación de la tienda."},
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
- **Orden de envío:** el reclamo a YPF de cada estación va antes que el mail a esa estación, porque este dice "pedimos a YPF que revise". Mandá los mails por pares, estación por estación, para que el usuario los reenvíe a cada contacto.

Al terminar, decile al usuario dónde encontrar todo (Borradores o bandeja de entrada de tal cuenta) y los pasos para enviarlo, sin jerga técnica.

## Modo automático desde Outlook (casilla Jesus_Bruna@aca.org.ar)

YPF manda un mail por estación desde `Programa+YPF@ypf.com`, con asunto `Avance + YPF <Trimestre> <cód> - ACA <ESTACIÓN>` y el tablero en PDF adjunto. Cada mail trae en **CC al representante comercial de YPF** de esa estación. Con el conector de Microsoft 365 (Outlook), procesá cada mail nuevo así:

1. **Buscar pendientes.** Usá `outlook_email_search` con `sender: Programa+YPF@ypf.com`, `query: Avance` y `afterDateTime` de hace 10 días. Quedate con los asuntos que empiezan con "Avance + YPF" y que **no** tienen la categoría `Procesado +YPF`. Mirá las categorías con `read_resource` sobre el mail. Los mails "Resultados … Trimestre" no se procesan: son resultados ya cerrados.
2. **Leer cada tablero.**
   - Con `read_resource` sobre el mail sacá el adjunto `.pdf`, el CC (el representante) y la fecha.
   - Con `read_resource` sobre la URI del adjunto obtenés el texto del PDF, desordenado. Guardalo tal cual en `datos/outlook_<AAAA-MM-DD>/<cód>.txt`.
3. **Pasar a CSV y validar:**
   ```bash
   python3 $SK/parsear_texto_outlook.py datos/outlook_<fecha> > datos/avance_<fecha>.csv
   ```
   El script recalcula los puntos y los compara con el total del tablero.
   - Si una estación da `ATENCION`, no generes nada para ella y avisalo en el resumen.
   - Con `ok`, los números son confiables.
4. **Tablero acumulado del trimestre (visto el 06/11).** Desde el 2.º mes, el real se cuenta desde el inicio del trimestre y el mínimo es la suma de los meses (oct + nov, y en diciembre el trimestre completo). `parsear_texto_outlook.py` proyecta así y calcula el ritmo necesario hasta fin de mes. En los mails a la estación hablá de "llevan X en el trimestre y el mínimo acumulado a fin de <mes> es Y; les faltan Z, aprox. W por día". Pasá `--anterior=<csv previo>` a `mails_estaciones.py` para marcar los datos que no se movieron, porque YPF a veces carga noviembre con demora. A principio de mes, o con datos sin moverse, no reclames volúmenes. Compará el mínimo nuevo con el del mes anterior: si YPF bajó la meta del mes, mencionalo como logro. Cliente incógnito aparece en el tablero después de "Penetración App YPF" y el parser ya lo lee. Si da menos de 75 %, no cumple la condición básica: es una alerta y amerita pedirle a YPF el informe detallado.
5. **Período (confirmado por el usuario).** Los objetivos son **trimestrales**, pero el tablero muestra el avance de **cada mes**: los volúmenes son acumulados del mes en curso y se proyectan al cierre del mes.
   - **Lubricantes:** YPF fija la fecha límite de pedido el 7/12 (14/12 en la región Metropolitana), así que no los reclames por ritmo diario. Recordale a la estación que haga el pedido. Reclamá solo si la meta cambió de forma brusca o es la más alta de la red con mucha diferencia.
   - **Cambios de meta:** compará con el CSV anterior de `datos/` y mencioná los cambios en el reclamo, por ejemplo "pasó de 0,33 a 1,52 m3".
   - **Lote recibido después de que terminó el mes de los datos:** `mails_estaciones.py` dice "el mes cerraría…". Ajustalo a "<mes> habría cerrado en…" y "Para llegar en <mes siguiente> hay que promediar…", y en la intro poné "Al dd/mm llevaban X pts y estimamos que <mes> cerró en ~Y pts".
   - **Reclamos al cierre del mes:** pedí que revisen la meta para los meses que quedan del trimestre. Si la estación ya está al 95 % o más, no reclames.
6. **Decidir reclamos** con el criterio del Paso 1 y armar `datos/notas_<fecha>.json`. Después generá los textos con `mails_estaciones.py` y `reclamos_ypf.py`, como en los Pasos 3 y 4.
7. **Crear borradores en Outlook** (nunca enviar):
   - **Mail a la estación:** `outlook_create_draft`, sin destinatario, con asunto `Programa +YPF – ACA <ESTACIÓN> – Avance al dd/mm` y `bodyType: text` con el texto del `.txt` sin la línea de asunto ni "[Nombre y firma]". El tablero no se puede adjuntar desde el conector: el usuario reenvía o adjunta el PDF del mail de YPF.
   - **Reclamo:** solo si esa estación tiene algo para reclamar. Usá `outlook_create_reply_all_draft` sobre el mail de YPF de esa estación, con el texto del reclamo en HTML. Así queda dirigido a Programa+YPF y al representante en copia, dentro del mismo hilo.
8. **Marcar el mail de YPF** con `outlook_modify_labels` y la categoría `Procesado +YPF`, para no repetirlo.
9. **Guardar y resumir.** Hacé commit de `datos/` en la rama de trabajo y push. Dejá un último borrador `Resumen +YPF – dd/mm` dirigido a Jesus_Bruna@aca.org.ar con:
   - el ranking de puntos hoy y proyectados;
   - qué reclamos quedaron en borrador;
   - las alertas de parseo o de cambio de metas.

## Tono de los mails (preferencia del usuario)

Los mails tienen que sonar **como si los hubiera escrito el coordinador**:
- **Persona y voz:** primera persona del singular ("les paso", "ya le pedí a YPF", "quedo atento"), en español rioplatense, cercano y concreto.
- **Aproximaciones:** "aprox." y nunca "~".
- **Puntos en juego:** no escribas "Puntos en juego: X", ni nada parecido, al final de cada ítem.
- **Mail a la estación:** saludo ("Hola, equipo de <Localidad>, ¿cómo están?"), una aclaración breve sobre cómo leer el tablero, "Lo bueno" primero, después "Para <mes> les pido que pongan foco en", después "Otros temas", y cierre con "Cualquier cosa me avisan. Saludos,".
- **Reclamo a YPF:** "Hola, ¿cómo están?", "Les escribo por el avance de ACA <Localidad> al dd/mm…", ítems en viñetas que terminan en una pregunta ("¿Lo podemos revisar…?"), y cierre con "Quedo atento. ¡Gracias! Saludos,". Si YPF ya corrigió algo que se le reclamó, agradecelo al principio.
- **Al cierre del mes:** pasá `--cerrado` a `mails_estaciones.py` y a `reclamos_ypf.py` cuando el mes de los datos ya terminó.
