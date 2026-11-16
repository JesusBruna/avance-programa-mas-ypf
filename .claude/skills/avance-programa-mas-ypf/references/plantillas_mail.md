# Plantillas de mail

Escribí el cuerpo en texto plano, sin Markdown. Los decimales llevan coma y las unidades van con espacio: `74,4 m3`, `57,9 %`.

## Reclamo a YPF (uno por estación)

`reclamos_ypf.py` genera un mail por estación, porque cada una tiene su propio contacto en YPF. Esta es la estructura de referencia; en el mail de cada estación queda solo esa estación.

Asunto: `Programa +YPF – Solicitud de revisión de objetivos <Mes AAAA> – <cód> ACA <ESTACIÓN>`

```
Estimados:

Solicitamos la revisión de los siguientes objetivos del Programa +YPF de <mes AAAA>. Según el tablero de Performance de Red con datos al <dd/mm/aaaa> (<d> de <N> días), en estas estaciones el objetivo mínimo queda fuera de alcance al ritmo de venta real del mes. Como el indicador no suma puntos si no se llega al mínimo, la estación pierde el puntaje completo aunque sostenga su nivel de venta habitual.

Criterio de proyección: venta acumulada al <dd/mm> ÷ <d> días × <N> días.

OBJETIVOS DE VOLUMEN

1. <cód> ACA <ESTACIÓN> – <Concepto>
   Objetivo: mín. <x> / máx. <y>
   Real al <dd/mm>: <r>, que proyecta <p> al cierre (<pct> % del mínimo)
   Ritmo necesario <n>/día contra <a>/día actual (+<inc> %)
   [Comparación con la red si es el más alto: "Es el objetivo de <concepto> más alto de la red; el resto va de <min> a <max>."]
   Puntos en juego: <pts>
   (Ordenar del peor % al mejor.)

[Si un concepto falla en muchas estaciones: "En <concepto> el desvío es generalizado: <k> de nuestras <n> estaciones proyectan por debajo del mínimo. Les pedimos que nos indiquen con qué base histórica o estacional se definieron los objetivos de <mes>."]

OBJETIVOS PORCENTUALES
<cód> ACA <ESTACIÓN> – <Concepto>: objetivo mín. / máx., real; comparación con el rango del resto de la red.

[Opcional] OBJETIVOS FALTANTES Y DATOS NO INFORMADOS
- Sin objetivo de Croselling / Comidas y Café (20 pts que no se pueden sumar): <lista>. Pedir que carguen los objetivos o redistribuyan el puntaje.
- Con objetivo pero sin ventas reales de tienda: <estación>. Pedir que verifiquen la vinculación de la tienda.
- Lubricantes sin dato real: <lista>.
- Otros datos atípicos (por ejemplo, un indicador sin objetivo pero con dato real).

SOLICITUD
Pedimos que se ajusten los objetivos mínimos detallados a valores acordes al nivel de venta real de cada estación o, en su defecto, que nos informen el criterio utilizado. Quedamos a disposición para revisarlo juntos y, si les sirve, les enviamos el detalle de cálculo por estación.

Saludos cordiales,
```

## Mail a cada estación

`mails_estaciones.py` lo genera solo. Esta es la estructura, por si hay que ajustarlo a mano:

```
Asunto: Programa +YPF – ACA <ESTACIÓN> – Avance al <dd/mm>

Hola, ¿cómo están?

Les paso el avance del +YPF al <dd/mm>.

Les recuerdo que los objetivos son trimestrales: el tablero muestra lo que llevan desde el 1/10 contra lo que hay que tener a fin de <mes>, por eso los volúmenes aparecen en 0 % hasta que pasan el mínimo. Cada indicador suma recién cuando se pasa el mínimo.

Al <dd/mm> llevan <x> puntos y, si siguen a este ritmo, <mes> cerraría en aprox. <y> (sin contar lo que todavía no se mide).

Vienen bien en <lista>, ¡sigan así!

Para lo que queda del mes, hay que ponerle foco a:
- <Concepto>: llevan <r> en el trimestre y el mínimo acumulado a fin de <mes> es <m>. Les faltan <f>: aprox. <n> por día de acá a fin de mes (en lo que va del trimestre vienen promediando aprox. <a> por día).
- <Ratio>: están en <r> % y el mínimo es <m> %; les faltan <g> puntos. [Están muy cerca.]

Además:
- Lubricantes / metas de tienda sin cargar / auditoría de imagen / cliente incógnito.

Cualquier cosa me avisan.

Saludos,
Jesus.-
```

El tono es el de Jesús escribiendo: frases cortas, cercano, motivador y concreto, nunca de reproche. Usar "aprox." (nunca "~") y no poner "Puntos en juego". A la estación no se le explica la lógica interna del reclamo: solo se le avisa que la meta está en revisión y que siga empujando.
