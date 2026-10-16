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

Hola equipo de ACA <ESTACIÓN>:

Les adjuntamos el tablero de Performance de Red de YPF con datos al <fecha>.

Cómo leerlo:
- Los volúmenes (diesel, naftas, lubricantes y comidas) son acumulados del mes. Por eso hoy aparecen con 0 % de cumplimiento: se evalúan al cierre.
- Cada indicador suma puntos solo si se llega al objetivo mínimo (ahí suma el 70 % de los puntos) y suma el 100 % al llegar al máximo. Quedar apenas por debajo del mínimo no suma nada.
- Hoy llevan <x> pts. Al ritmo actual estimamos ~<y> pts al cierre (sin contar lo que todavía no se mide).

Dónde seguir trabajando:
- <Concepto>: llevan <r> y el mínimo es <m>. Hay que vender ~<n>/día (hoy ~<a>). [Está al límite: cada día cuenta.] [Pedimos a YPF que revise este objetivo; mientras tanto, sigamos empujando.]
- <Ratio>: <r> % contra un mínimo de <m> % (faltan <g> pp). [Está muy cerca.]

Vienen bien en: <lista>. ¡A sostenerlo!

Para tener en cuenta:
- Lubricantes sin ventas en el tablero → que avisen si compraron o vendieron.
- Metas de tienda sin cargar → ya lo reclamamos a YPF.
- Cliente incógnito y Auditoría de imagen pendientes: además son condición del programa (mínimo 75 % y 80 %).

Cualquier duda, quedamos en contacto.

Saludos,
```

El tono es motivador y concreto, nunca de reproche. A la estación no se le explica la lógica interna del reclamo: solo se le avisa que la meta está en revisión y que siga empujando.
