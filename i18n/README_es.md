<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../docs/brand/logo-light.svg">
  <img src="../docs/brand/logo-dark.svg" width="400" alt="rea-video">
</picture>

Ingeniería inversa para cualquier vídeo.

Plano a plano: si se grabó, se generó con IA o se hizo con código, y cómo volver a hacerlo.

[Sitio web](https://www.reavideo.ai) | [中文](README_zh.md) | [English](../README.md) | [Русский](README_ru.md) | [日本語](README_ja.md) | [한국어](README_ko.md) | Español | [Português](README_pt.md) | [Français](README_fr.md) | [Deutsch](README_de.md) | [Tiếng Việt](README_vi.md)

[![Stars](https://img.shields.io/github/stars/JuneYaooo/rea-video?style=flat)](https://github.com/JuneYaooo/rea-video/stargazers)
![Python](https://img.shields.io/badge/python-%E2%89%A53.10-blue)
![Agent](https://img.shields.io/badge/runs%20in-Claude%20Code%20%7C%20Codex-8A2BE2)

<a href="https://trendshift.io/repositories/334878" target="_blank"><img src="https://trendshift.io/api/badge/trendshift/repositories/334878/daily" alt="JuneYaooo/rea-video | Trendshift" width="250" height="55"></a>

[![Visit our website](https://img.shields.io/badge/Visit%20our%20website-6644D8?style=for-the-badge)](https://www.reavideo.ai) [![Join our Discord](https://img.shields.io/badge/Join%20our%20Discord-5865F2?style=for-the-badge&logo=discord&logoColor=white)](https://discord.gg/dZj8D3GqWT) [![Follow on X](https://img.shields.io/badge/Follow%20%40yao__june12106-000000?style=for-the-badge&logo=x&logoColor=white)](https://x.com/yao_june12106)

⭐ *Si te sirve, dale una estrella: así más gente encuentra rea-video.*

<img src="../docs/cases/demo.gif" width="440" alt="Izquierda: original de TikTok grabado con un móvil; derecha: el remake con IA que hizo otra persona con un producto distinto">

A la izquierda, un anuncio de TikTok grabado con el móvil; a la derecha, un remake con IA y otro producto. Según rea-video, el de la izquierda es todo imagen real, con un solo decorado y dos posiciones de cámara; el de la derecha es todo IA: 8 planos en 3 generaciones.

</div>

## Inicio rápido

rea-video está pensado para usarse desde un agente de IA. En Claude Code, Codex o cualquier agente que pueda ejecutar comandos, escribe:

```text
Instala https://github.com/JuneYaooo/rea-video y luego analiza este vídeo: /path/to/video.mp4
```

El agente instala la CLI, aprende el flujo de trabajo y se encarga del resto. Solo necesitas ffmpeg y Python 3.10+.

<details><summary>Instalación manual</summary>

```bash
brew install ffmpeg            # sudo apt install ffmpeg
git clone https://github.com/JuneYaooo/rea-video && cd rea-video
bash scripts/install_skill.sh  # instala la CLI (pip, o pipx / .venv local) y enlaza el skill → ~/.claude, ~/.codex, ~/.agents
rea-video --help
```

</details>

Lo que obtienes:

- un resumen en una línea, por ejemplo "41 % vídeo con IA + 59 % UI en código, 8 s de grabación de pantalla real, música de biblioteca a 122 BPM"
- un plan para rehacerlo, separado en qué hay que grabar, qué generar y qué programar
- un `report.html` completo con fotogramas por plano, evidencias, prompts, notas de cámara e iluminación, y el desglose del audio

Si añades un modelo que entienda vídeo (vale Gemini o Doubao), basta con pasarle al agente el endpoint y la clave. Con él acierta más al distinguir entre imagen real, IA y 3D, y reconstruye el prompt de cada plano. Sin él también funciona: si tu agente puede ver imágenes, revisa él mismo los planos dudosos.

> El informe sale en el idioma en que lo pidas (chino o inglés). Los informes de ejemplo de más abajo están en inglés.

## Qué tipo de vídeos analiza

| Tipo de vídeo | Ejemplos | Qué obtienes |
|---|---|---|
| Imagen real | Vídeo a cámara, tabletop, demo de producto en mano, vlog, visita a tienda | Montajes de rodaje y posiciones de cámara, encuadre, movimientos de cámara, iluminación (12 esquemas, cada uno con su lista de equipo), etalonaje |
| Vídeo con IA | Texto/imagen a vídeo, microdramas con IA, videoclips con IA | Evidencias, el prompt reconstruido de cada plano, cómo agruparlos en generaciones y qué modelo usar |
| Avatar | Un retrato animado a partir de audio, sincronización labial | Qué planos son de avatar y qué retrato y audio necesitas |
| 3D / animación | Vídeos explicativos en Blender / C4D, animación de producto, animación 2D, stop-motion | Si conviene generarlo con un modelo de vídeo o renderizarlo con código 3D |
| Código / plantilla | Tipografía cinética, demos de UI, gráficos, tarjetas tipo diapositiva | Texto, maquetación y tiempos de animación, listos para rehacerlo como proyecto de Remotion |
| Grabación de pantalla | Tutoriales de software, demos web | Qué partes son material real que tendrás que grabar tú |
| Mixto / montajes | Personajes de IA + UI en código + captura de pantalla real; imagen real con retoques de IA | Cada plano se analiza por separado y después todo se vuelve a montar sobre la línea de tiempo original |

Además de cómo se hizo la imagen, de cada vídeo se analiza:

- Subtítulos y rótulos: dónde empieza y termina cada línea (se puede exportar a SRT / ASS), además del color, el contorno y cómo entra el texto
- Stickers, emojis, picture-in-picture: dónde aparecen y cuánto duran
- Montaje: dónde están los cortes, a qué ritmo van y si caen a tempo
- Audio: si la voz es humana o de IA, si la música es de IA o de biblioteca y a cuántos BPM va, y dónde cae cada efecto de sonido
- El material que tendrás que poner tú: grabaciones de pantalla, capturas, fotos de producto

## Ejemplos

Los vídeos de ejemplo de `docs/cases/videos/` están recomprimidos para que el repo no pese tanto, y eso borra las etiquetas de TikTok / Douyin. Si los pasas tú, te saldrán resultados distintos a los de los informes de abajo, sobre todo sin un modelo de visión. Para reproducirlos, usa la descarga original de la plataforma.

<table>
<tr>
<td width="50%" valign="top">
<a href="../docs/cases.md#2-混合片ai-人物对话--代码界面--真实录屏"><img src="../docs/cases/dual_role/thumb.jpg"></a><br>
<b>Clip mixto</b> · 19 s · 10 planos<br>
Personajes de IA conversando + UI hecha en código + 8 s de grabación de pantalla real. Los 5 planos de diálogo están intercalados con tramos de UI, pero comparten decorado, así que salen todos de una sola generación.<br>
<a href="../docs/cases/videos/dual_role.mp4">Vídeo</a> · <a href="../docs/cases/dual_role/report_en.md">Informe</a>
</td>
<td width="50%" valign="top">
<a href="../docs/cases.md#3-3d-科普片咸鸭蛋为什么会流油"><img src="../docs/cases/salted_egg/thumb.jpg"></a><br>
<b>Vídeo explicativo en 3D</b> · 67 s · 21 planos<br>
Todo en 3D, con narración de IA. Se puede sacar en 10 generaciones de vídeo, o pedirle a un LLM que escriba el código en Blender / Three.js.<br>
<a href="../docs/cases/videos/salted_egg.mp4">Vídeo</a> · <a href="../docs/cases/salted_egg/report_en.md">Informe</a>
</td>
</tr>
<tr>
<td width="50%" valign="top">
<a href="../docs/cases.md#4-代码-ui-动效产品宣传片"><img src="../docs/cases/v10/thumb.jpg"></a><br>
<b>Vídeo promocional de producto</b> · 70 s · 12 planos<br>
83 % motion graphics generados por código, 12 % grabación de pantalla. No hace falta ningún modelo de vídeo: con un proyecto de Remotion basta.<br>
<a href="../docs/cases/videos/v10_oiioii_gen_coding_first.mp4">Vídeo</a> · <a href="../docs/cases/v10/report_en.md">Informe</a>
</td>
<td width="50%" valign="top">
<a href="../docs/cases.md#5-ai-音乐-mv歌是-ai-写的还是曲库的"><img src="../docs/cases/qing_mv/thumb.jpg"></a><br>
<b>Videoclip con IA</b> · 165 s · 86 planos<br>
Detecta bien que la canción es de IA (se hizo con Suno). El modelo de visión tomó algunos planos por "drama de imagen real"; el agente vio caracteres chinos inventados en un pergamino y los marcó como IA.<br>
<a href="../docs/cases/videos/qing_mv.mp4">Vídeo</a> · <a href="../docs/cases/qing_mv/report_en.md">Informe</a>
</td>
</tr>
<tr>
<td width="50%" valign="top">
<a href="../docs/cases.md#6-实拍带货沉浸式开箱"><img src="../docs/cases/unboxing/thumb.jpg"></a><br>
<b>Unboxing con imagen real</b> · 72 s · 29 planos<br>
Todo es imagen real: el móvil en un soporte cenital, una alfombra, una sola posición de cámara, sin voz en off, solo sonido ambiente y música de fondo de biblioteca. Por la recompresión de la plataforma, la herramienta offline dio un 35 % como IA; tras la revisión del agente, quedó en un 97 % de imagen real.<br>
<a href="../docs/cases/videos/unboxing.mp4">Vídeo</a> · <a href="../docs/cases/unboxing/report_en.md">Informe</a>
</td>
<td width="50%" valign="top">
<a href="../docs/cases.md#7-ai-与真人混合用自己的出镜视频生成带货片"><img src="../docs/cases/ai_daihuo/thumb.jpg"></a><br>
<b>Híbrido de IA y persona real</b> · 58 s · 21 planos<br>
75 % real (vídeo a cámara + la pantalla de un móvil grabada) y 25 % IA: la creadora le pasó a Jimeng un clip suyo hablando a cámara y dos fotos del producto para generar un tramo de producto "con persona real". La parte de IA la delataron la marca de agua de Jimeng y el texto deformado de la caja de regalo.<br>
<a href="../docs/cases/videos/ai_daihuo.mp4">Vídeo</a> · <a href="../docs/cases/ai_daihuo/report_en.md">Informe</a>
</td>
</tr>
</table>

## Remakes

Una vez que rea-video ha analizado un vídeo, la receta de remake de [capsule-cinema](https://github.com/JuneYaooo/capsule-cinema) genera una versión nueva: la cámara, el movimiento, el ritmo y las transiciones son los del original, y solo cambian los elementos que tú elijas.
Estos resultados salen de un MiniMax H3 autoalojado: el plano original hace de referencia de movimiento, y los fotogramas clave con los elementos ya cambiados (gpt-image-2) marcan el aspecto.
Abajo hay tres remakes que OiiOii enseñó en sus artículos de WeChat. De cada uno hicimos dos versiones: una con el mismo cambio que hizo OiiOii y otra que además cambia el protagonista, el escenario y el atrezo.
Cada GIF muestra las cuatro versiones a la vez: original, remake de OiiOii, nuestro remake y la versión con los elementos cambiados.

<table>
<tr><td>
<b>Cambio de ropa en plano cenital</b> · 12 s<br>
Mismo cambio: mujer → hombre, tres conjuntos → su equivalente en ropa de hombre. Cambio de elementos: una chica con tres trajes tradicionales Hanfu en un estudio de estilo chino; el mando a distancia se convierte en un abanico redondo.<br>
<img src="../docs/cases/remake/outfit.gif"><br>
<a href="../docs/cases/remake/outfit_compare.mp4">Vídeo comparativo en HD (con audio)</a> · <a href="../docs/cases/remake/outfit_sheet.jpg">fotogramas del mismo instante</a>
</td></tr>
<tr><td>
<b>Animación de papel / acuarela</b> · 30 s<br>
Mismo cambio: otra chica de plastilina como protagonista. Cambio de elementos: un zorro; bosque → arrecife de coral, nubes → cielo estrellado, atardecer → aurora.<br>
<img src="../docs/cases/remake/paper.gif"><br>
<a href="../docs/cases/remake/paper_compare.mp4">Vídeo comparativo en HD (con audio)</a> · <a href="../docs/cases/remake/paper_sheet.jpg">fotogramas del mismo instante</a>
</td></tr>
<tr><td>
<b>Vídeo de producto en mano</b> · 21 s · 11 planos<br>
Mismo cambio: un producto nuevo y propio, sticker en inglés → subtítulo en chino. Cambio de elementos: producto rosa, cocina → mesa de camping, ingredientes nuevos.<br>
<img src="../docs/cases/remake/juicer.gif"><br>
<a href="../docs/cases/remake/juicer_compare.mp4">Vídeo comparativo en HD (con audio)</a> · <a href="../docs/cases/remake/juicer_sheet.jpg">fotogramas del mismo instante</a>
</td></tr>
</table>

Los vídeos comparativos en HD llevan el audio original. Los originales y las versiones de OiiOii salen de esos artículos y se incluyen solo para comparar.

## Precisión

Precisión al identificar cómo se hizo cada plano, ponderada por su duración:

| | Conjunto de ajuste (15) | Holdout (16) | Vídeos de WeChat recodificados (10) |
|---|---|---|---|
| Solo herramientas (offline, gratis) | 98.3% | 99.6% / 98.9% | 88.6% |
| + modelo de visión (Gemini) | — | 99.6% / 99.8% | 99.6% |
| + revisión visual del agente | — | 99.6% / 99.8% | 100% |

En la columna de holdout, la primera cifra es holdout (9 vídeos) y la segunda, holdout2 (7 vídeos).

Con los archivos originales, las herramientas solas suelen bastar. Los vídeos descargados de plataformas vienen recomprimidos y pierden la evidencia del ruido, así que para volver a pasar del 99 % hace falta una revisión visual.

La detección de material real acierta entre un 97 y un 99 %; en nueve clips anotados a mano, los cortes entre planos se detectan con un 95 % de recall y un 94 % de precisión. Las cifras y cómo reproducirlas, en [eval/RESULTS.md](../eval/RESULTS.md).

## Cómo funciona

![Pipeline de rea-video](../docs/rea-flow_es.svg)

1. Separar: corta el vídeo en planos y divide el audio en voz, música y efectos.
2. Reunir evidencias: mide los fotogramas (cadencia, ruido del sensor, si toda la imagen se desplaza como un único plano, etiquetas AIGC en los metadatos), mira las imágenes (manos, texto, física) y escucha el audio (BPM, tonalidad, si se canta o se habla).
3. Decidir: las pruebas objetivas, como las etiquetas AIGC o la cadencia de fotogramas, pesan más que un "parece que". Cuando hay contradicciones, se marcan para que el agente las revise a ojo.
4. Planificar el remake: agrupa los planos según lo que de verdad puede hacer el modelo de vídeo que vayas a usar: duración máxima del clip, si admite varios planos seguidos y cuántas imágenes de referencia acepta.

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=JuneYaooo/rea-video&type=Date)](https://star-history.com/#JuneYaooo/rea-video&Date)

## Preguntas frecuentes

<details>
<summary>¿En qué se diferencia de herramientas de remake en un clic como Hypit?</summary>

[Hypit](https://github.com/hypit-ai/hypit) parte de un vídeo de referencia y hace uno nuevo: el agente lee cuadrículas de fotogramas para entender el original, genera las imágenes con los modelos que soporta (Seedance, PixVerse, MiniMax, Wan y otros) y renderiza los subtítulos y los motion graphics en HTML.

No se plantea cómo se hizo el original. Un vídeo de imagen real pasa por el mismo pipeline, así que no te va a decir cuántas cámaras había ni cómo se iluminó. Qué vídeos de IA puede igualar depende de los modelos que tiene: no incluye Kling ni Veo, no tiene una vía propia para avatares o 3D, y tampoco hace música con IA: esa la pones tú. Va mejor con vídeos a cámara, podcasts y entrevistas que siguen un guion, y peor con montajes que van al ritmo de la música, motion graphics de producto y cortos de estilo cinematográfico.

rea-video no renderiza vídeo. Averigua plano a plano si se grabó, se generó con IA o se hizo con código, y para cada uno te da un plan de rodaje, prompts o cómo enfocarlo en código. Si lo que buscas es un vídeo parecido cuanto antes, Hypit va más rápido. Si quieres entender cómo se hizo el original y rehacerlo gastando poco, usa rea-video. Se pueden usar juntos sin problema.

</details>

<details>
<summary>¿Necesito un modelo que entienda vídeo? ¿Cuánto cuesta?</summary>

No. El modo solo con herramientas funciona offline, es gratis y con archivos originales ya acierta mucho. Para vídeos descargados de plataformas, que vienen recomprimidos, añade un modelo que entienda vídeo (vale Gemini o Doubao) o usa un agente que pueda ver imágenes; pagas lo que cobre ese servicio. La generación automática de vídeo (capsule-cinema) hace primero una simulación gratis y no llama a ningún modelo de pago hasta que tú lo confirmes.

</details>

<details>
<summary>¿Puede rehacer el vídeo entero de forma automática?</summary>

En parte. Si tienes instalado [capsule-cinema](https://github.com/JuneYaooo/capsule-cinema), los planos de IA se generan y se colocan solos en la línea de tiempo original. Los de imagen real los grabas tú siguiendo el plan de rodaje, y los de código los escribe el agente como proyecto de Remotion. Más detalles en [docs/replicate.md](../docs/replicate.md).

</details>

<details>
<summary>¿Puedo resubir sin más el vídeo de otra persona?</summary>

No. rea-video sirve para aprender de un vídeo su estructura, su ritmo y sus técnicas, y luego rehacerlo con material sobre el que tengas derechos. No reutilices las imágenes, la música, los personajes ni la imagen de otras personas. Cuando publiques, cumple las normas de la plataforma y lo que exija la ley de tu país sobre etiquetar contenido generado con IA.

</details>

## Documentación

- [docs/what-it-detects.md](../docs/what-it-detects.md): todo lo que detecta (10 tipos de imagen, cámara, iluminación, etalonaje, audio)
- [docs/replicate.md](../docs/replicate.md): cómo rehacer el vídeo a partir del informe
- [docs/cases.md](../docs/cases.md): detalles de los casos
- [docs/decompose.md](../docs/decompose.md): reglas de detección
- [docs/cli.md](../docs/cli.md): uso de la CLI e integración con capsule-cinema
- [rea_video/capabilities/](../rea_video/capabilities/README.md): tablas de capacidades de modelos de vídeo / imagen / audio, que se usan para elegir modelo en el plan de remake
- [eval/RESULTS.md](../eval/RESULTS.md): resultados de la evaluación

De momento, la documentación solo está en chino.

## Comunidad

Para dudas, análisis e ideas de remake: [GitHub Discussions](https://github.com/JuneYaooo/rea-video/discussions). También estamos en [Discord](https://discord.gg/dZj8D3GqWT), y si hablas chino, en [linux.do](https://linux.do/).

¿Quieres que analicemos un vídeo? Abre una [issue de solicitud](https://github.com/JuneYaooo/rea-video/issues/new?template=request_breakdown.yml) con el enlace y publicaremos el resultado como un caso más.

## Créditos

Inspirado en [REA (Reverse Engineer Anything)](https://github.com/morluto/rea): partir de lo que se ve para llegar a cómo se hizo, respaldar cada afirmación con pruebas y comprobarlo midiendo.
