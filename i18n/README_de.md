<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../docs/brand/logo-light.svg">
  <img src="../docs/brand/logo-dark.svg" width="400" alt="rea-video">
</picture>

Reverse Engineering für beliebige Videos.

Shot für Shot: gedreht, mit KI generiert oder programmiert? Und wie baut man es nach?

[Website](https://www.reavideo.ai) | [中文](README_zh.md) | [English](../README.md) | [Русский](README_ru.md) | [日本語](README_ja.md) | [한국어](README_ko.md) | [Español](README_es.md) | [Português](README_pt.md) | [Français](README_fr.md) | Deutsch | [Tiếng Việt](README_vi.md)

[![Stars](https://img.shields.io/github/stars/JuneYaooo/rea-video?style=flat)](https://github.com/JuneYaooo/rea-video/stargazers)
![Python](https://img.shields.io/badge/python-%E2%89%A53.10-blue)
![Agent](https://img.shields.io/badge/runs%20in-Claude%20Code%20%7C%20Codex-8A2BE2)

<a href="https://trendshift.io/repositories/334878" target="_blank"><img src="https://trendshift.io/api/badge/trendshift/repositories/334878/daily" alt="JuneYaooo/rea-video | Trendshift" width="250" height="55"></a>

[![Visit our website](https://img.shields.io/badge/Visit%20our%20website-6644D8?style=for-the-badge)](https://www.reavideo.ai) [![Join our Discord](https://img.shields.io/badge/Join%20our%20Discord-5865F2?style=for-the-badge&logo=discord&logoColor=white)](https://discord.gg/dZj8D3GqWT) [![Follow on X](https://img.shields.io/badge/Follow%20%40yao__june12106-000000?style=for-the-badge&logo=x&logoColor=white)](https://x.com/yao_june12106)

⭐ *Mit einem Stern hilfst du, dass mehr Leute rea-video finden.*

<img src="../docs/cases/demo.gif" width="440" alt="Links: TikTok-Original, mit dem Handy gedreht; rechts: KI-Remake von jemand anderem mit einem anderen Produkt">

Links: eine TikTok-Werbung, mit dem Handy gedreht. Rechts: ein KI-Remake mit einem anderen Produkt. Laut rea-video ist links alles echt gedreht – ein Set, zwei Kamerapositionen –, rechts alles KI: 8 Shots aus 3 Generierungen.

</div>

## Schnellstart

rea-video ist für KI-Agenten gemacht. Schreib in Claude Code, Codex oder einem anderen Agenten, der Befehle ausführen kann:

```text
Installiere https://github.com/JuneYaooo/rea-video und nimm dann dieses Video auseinander: /path/to/video.mp4
```

Der Agent installiert die CLI, liest sich in den Ablauf ein und erledigt den Rest. Voraussetzung sind ffmpeg und Python 3.10+.

<details><summary>Manuell installieren</summary>

```bash
brew install ffmpeg            # sudo apt install ffmpeg
git clone https://github.com/JuneYaooo/rea-video && cd rea-video
bash scripts/install_skill.sh  # installiert die CLI (pip, sonst pipx / lokales .venv) und verlinkt den Skill → ~/.claude, ~/.codex, ~/.agents
rea-video --help
```

</details>

Am Ende hast du:

- eine Zusammenfassung in einer Zeile, z. B. „41 % KI-Video + 59 % Code-UI, 8 s echte Bildschirmaufnahme, Stockmusik mit 122 BPM“
- einen Remake-Plan, aufgeteilt in: was du drehst, was du generierst und was du programmierst
- einen vollständigen `report.html` mit Frames zu jedem Shot, Belegen, Prompts, Notizen zu Kamera und Licht und der Audioanalyse

Optional kannst du ein Modell anbinden, das Video versteht – Gemini oder Doubao, beides geht: Gib dem Agenten einfach Endpoint und Key. Dann wird die Einstufung echt/KI/3D genauer, und zu jedem Shot gibt es einen rekonstruierten Prompt. Ohne Modell geht es auch; kann dein Agent Bilder sehen, schaut er sich die unsicheren Shots selbst an.

> Der Bericht kommt in der Sprache, in der du fragst (Chinesisch oder Englisch). Die Beispielberichte unten sind auf Englisch.

## Was sich analysieren lässt

| Videotyp | Beispiele | Was du bekommst |
|---|---|---|
| Realaufnahmen | Talking Head, Tabletop, Produktdemo aus der Hand, Vlog, Ladenbesuch | Sets und Kamerapositionen, Bildausschnitt, Kamerabewegungen, Licht (12 Setups mit Ausrüstungslisten), Color Grading |
| KI-Video | Text/Bild-zu-Video, KI-Kurzserie, KI-Musikvideo | Belege, ein rekonstruierter Prompt pro Shot, wie sich die Shots auf Generierungen verteilen lassen und welches Modell passt |
| Avatar | Porträt, das per Audio animiert wird; Lipsync | Welche Shots Avatar-Shots sind und welches Porträt und Audio du dafür brauchst |
| 3D / Animation | Blender- / C4D-Erklärvideos, Produktanimation, 2D-Animation, Stop-Motion | Ob du besser mit einem Videomodell generierst oder per 3D-Code renderst |
| Code / Vorlage | Kinetische Typografie, UI-Demos, Diagramme, Karten im Folienstil | Text, Layout und Animations-Timing – direkt als Remotion-Projekt nachbaubar |
| Bildschirmaufnahme | Software-Tutorials, Web-Demos | Welche Teile echtes Material sind, das du selbst aufnehmen musst |
| Gemischt / Schnitte | KI-Figuren + Code-UI + echte Bildschirmaufnahme; echtes Filmmaterial mit KI-Bearbeitung | Jeder Shot wird einzeln bewertet und danach auf der Original-Timeline wieder zusammengesetzt |

Unabhängig davon, wie das Bild entstanden ist, schaut sich rea-video bei jedem Video außerdem an:

- Untertitel und Texteinblendungen: Start und Ende jeder Zeile (Export als SRT / ASS), dazu Farbe, Kontur und wie der Text reinkommt
- Sticker, Emoji, Bild-in-Bild: wo sie sitzen und wie lange sie bleiben
- Schnitt: wo geschnitten wird, in welchem Tempo und ob die Schnitte auf dem Beat liegen
- Audio: echte oder KI-Stimme, KI- oder Stockmusik samt BPM, wo welcher Soundeffekt sitzt
- Material, das du selbst beisteuern musst: Bildschirmaufnahmen, Screenshots, Produktfotos

## Beispiele

Die Beispielvideos in `docs/cases/videos/` sind neu komprimiert, damit das Repo klein bleibt – dabei gehen die TikTok-/Douyin-Plattformtags verloren. Wenn du sie selbst durchlaufen lässt, kommt deshalb etwas anderes heraus als in den Berichten unten, vor allem ohne Vision-Modell. Zum Nachvollziehen nimm den Original-Download von der Plattform.

<table>
<tr>
<td width="50%" valign="top">
<a href="../docs/cases.md#2-混合片ai-人物对话--代码界面--真实录屏"><img src="../docs/cases/dual_role/thumb.jpg"></a><br>
<b>Gemischter Clip</b> · 19 s · 10 Shots<br>
KI-Figuren im Gespräch + per Code gebaute UI + 8 s echte Bildschirmaufnahme. Die 5 Dialog-Shots sind zwar durch UI-Segmente getrennt, spielen aber im selben Set – eine Generierung reicht für alle.<br>
<a href="../docs/cases/videos/dual_role.mp4">Video</a> · <a href="../docs/cases/dual_role/report_en.md">Bericht</a>
</td>
<td width="50%" valign="top">
<a href="../docs/cases.md#3-3d-科普片咸鸭蛋为什么会流油"><img src="../docs/cases/salted_egg/thumb.jpg"></a><br>
<b>3D-Erklärvideo</b> · 67 s · 21 Shots<br>
Komplett 3D, Sprecher per KI. Lässt sich mit 10 Videogenerierungen umsetzen – oder ein LLM schreibt Blender- / Three.js-Code.<br>
<a href="../docs/cases/videos/salted_egg.mp4">Video</a> · <a href="../docs/cases/salted_egg/report_en.md">Bericht</a>
</td>
</tr>
<tr>
<td width="50%" valign="top">
<a href="../docs/cases.md#4-代码-ui-动效产品宣传片"><img src="../docs/cases/v10/thumb.jpg"></a><br>
<b>Produktvideo</b> · 70 s · 12 Shots<br>
83 % Motion Graphics aus Code, 12 % Bildschirmaufnahme. Ein Videomodell braucht es nicht, ein Remotion-Projekt reicht.<br>
<a href="../docs/cases/videos/v10_oiioii_gen_coding_first.mp4">Video</a> · <a href="../docs/cases/v10/report_en.md">Bericht</a>
</td>
<td width="50%" valign="top">
<a href="../docs/cases.md#5-ai-音乐-mv歌是-ai-写的还是曲库的"><img src="../docs/cases/qing_mv/thumb.jpg"></a><br>
<b>KI-Musikvideo</b> · 165 s · 86 Shots<br>
Erkennt richtig, dass der Song KI-generiert ist (er stammt aus Suno). Das Vision-Modell hielt einige Shots für „Realfilm-Drama“; der Agent fand falsche chinesische Schriftzeichen auf einer Schriftrolle und stufte die Shots als KI ein.<br>
<a href="../docs/cases/videos/qing_mv.mp4">Video</a> · <a href="../docs/cases/qing_mv/report_en.md">Bericht</a>
</td>
</tr>
<tr>
<td width="50%" valign="top">
<a href="../docs/cases.md#6-实拍带货沉浸式开箱"><img src="../docs/cases/unboxing/thumb.jpg"></a><br>
<b>Unboxing, real gedreht</b> · 72 s · 29 Shots<br>
Komplett echt gedreht: Handy-Rig von oben, ein Teppich, eine Kameraposition, kein Voice-over, Raumton plus Stock-BGM. Nach dem Transcoding durch die Plattform hielt das Offline-Tool 35 % für KI; nach der Prüfung durch den Agenten waren es 97 % Realaufnahmen.<br>
<a href="../docs/cases/videos/unboxing.mp4">Video</a> · <a href="../docs/cases/unboxing/report_en.md">Bericht</a>
</td>
<td width="50%" valign="top">
<a href="../docs/cases.md#7-ai-与真人混合用自己的出镜视频生成带货片"><img src="../docs/cases/ai_daihuo/thumb.jpg"></a><br>
<b>Hybrid aus KI und echter Person</b> · 58 s · 21 Shots<br>
75 % echt (Talking Head + abgefilmter Handybildschirm), 25 % KI: Die Creatorin hat Jimeng einen Clip von sich vor der Kamera und zwei Produktfotos gegeben und daraus ein Produktsegment mit „echter Person“ generieren lassen. Verraten haben den KI-Teil das Jimeng-Wasserzeichen und verstümmelter Text auf der Geschenkbox.<br>
<a href="../docs/cases/videos/ai_daihuo.mp4">Video</a> · <a href="../docs/cases/ai_daihuo/report_en.md">Bericht</a>
</td>
</tr>
</table>

## Remakes

Hat rea-video ein Video zerlegt, baut das Remake-Rezept in [capsule-cinema](https://github.com/JuneYaooo/capsule-cinema) daraus eine neue Version: Kamera, Bewegung, Tempo und Übergänge bleiben wie im Original, getauscht wird nur, was du auswählst.
Erzeugt wurden die Ergebnisse mit einem selbst gehosteten MiniMax H3: Der Original-Shot liefert die Bewegungsreferenz, Keyframes mit den getauschten Elementen (gpt-image-2) bestimmen den Look.
Unten drei Remakes, die OiiOii in seinen WeChat-Artikeln gezeigt hat. Zu jedem haben wir zwei Versionen gebaut: eine mit demselben Tausch wie bei OiiOii und eine, in der zusätzlich Hauptfigur, Umgebung und Requisiten getauscht sind.
Jedes GIF zeigt vier Versionen synchron: Original, OiiOii-Remake, unser Remake und die Version mit getauschten Elementen.

<table>
<tr><td>
<b>Outfitwechsel von oben</b> · 12 s<br>
Gleicher Tausch: Frau → Mann, drei Outfits → passende Herrenmode. Elemente getauscht: ein Mädchen in drei historischen Hanfu-Outfits in einem chinesischen Studierzimmer; die Fernbedienung wird zu einem runden Fächer.<br>
<img src="../docs/cases/remake/outfit.gif"><br>
<a href="../docs/cases/remake/outfit_compare.mp4">HD-Vergleichsvideo (mit Ton)</a> · <a href="../docs/cases/remake/outfit_sheet.jpg">Standbilder vom selben Moment</a>
</td></tr>
<tr><td>
<b>Papier- / Aquarell-Animation</b> · 30 s<br>
Gleicher Tausch: ein neues Knetmädchen als Hauptfigur. Elemente getauscht: ein Fuchs; Wald → Korallenriff, Wolken → Sternenhimmel, Sonnenuntergang → Polarlicht.<br>
<img src="../docs/cases/remake/paper.gif"><br>
<a href="../docs/cases/remake/paper_compare.mp4">HD-Vergleichsvideo (mit Ton)</a> · <a href="../docs/cases/remake/paper_sheet.jpg">Standbilder vom selben Moment</a>
</td></tr>
<tr><td>
<b>Produktvideo aus der Hand</b> · 21 s · 11 Shots<br>
Gleicher Tausch: ein eigenes, neues Produkt; englischer Sticker → chinesische Bildunterschrift. Elemente getauscht: rosa Produkt, Küche → Campingtisch, neue Zutaten.<br>
<img src="../docs/cases/remake/juicer.gif"><br>
<a href="../docs/cases/remake/juicer_compare.mp4">HD-Vergleichsvideo (mit Ton)</a> · <a href="../docs/cases/remake/juicer_sheet.jpg">Standbilder vom selben Moment</a>
</td></tr>
</table>

Die HD-Vergleichsvideos laufen mit dem Originalton. Originale und OiiOii-Versionen stammen aus den Artikeln und sind nur zum Vergleich dabei.

## Genauigkeit

Wie zuverlässig rea-video erkennt, wie ein Shot entstanden ist (gewichtet nach Shot-Länge):

| | Tuning-Set (15) | Holdout (16) | Neu kodierte WeChat-Videos (10) |
|---|---|---|---|
| Nur Tools (offline, kostenlos) | 98.3% | 99.6% / 98.9% | 88.6% |
| + Vision-Modell (Gemini) | — | 99.6% / 99.8% | 99.6% |
| + visuelle Prüfung durch den Agenten | — | 99.6% / 99.8% | 100% |

Die beiden Holdout-Werte gelten für holdout (9 Videos) bzw. holdout2 (7 Videos).

Bei Originaldateien reichen meist schon die Tools. Von Plattformen heruntergeladene Videos sind neu komprimiert, dabei gehen die Rauschspuren verloren – um wieder über 99 % zu kommen, braucht es dann eine visuelle Prüfung.

Echte Assets werden zu 97–99 % erkannt; bei neun von Hand annotierten Clips werden die Shot-Grenzen mit 95 % Recall und 94 % Precision gefunden. Zahlen und wie du sie reproduzierst: [eval/RESULTS.md](../eval/RESULTS.md).

## Wie es funktioniert

![rea-video-Pipeline](../docs/rea-flow_de.svg)

1. Zerlegen: Video in Shots schneiden, Ton in Stimme, Musik und Effekte trennen.
2. Belege sammeln: Frames vermessen (Frame-Takt, Sensorrauschen, ob sich das ganze Bild wie eine einzige Ebene verschiebt, AIGC-Tags in den Metadaten), Bilder anschauen (Hände, Text, Physik), hinhören (BPM, Tonart, Gesang oder Sprache).
3. Entscheiden: Harte Belege wie AIGC-Tags und Frame-Takt zählen mehr als „sieht aus wie“. Widersprüche werden markiert, damit der Agent sie sich ansieht.
4. Remake planen: Shots so bündeln, wie es das Ziel-Videomodell tatsächlich hergibt – maximale Cliplänge, Multi-Shot-Support, wie viele Referenzbilder es nimmt.

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=JuneYaooo/rea-video&type=Date)](https://star-history.com/#JuneYaooo/rea-video&Date)

## FAQ

<details>
<summary>Was ist der Unterschied zu Ein-Klick-Remake-Tools wie Hypit?</summary>

[Hypit](https://github.com/hypit-ai/hypit) macht aus einem Referenzvideo ein neues: Der Agent liest Frame-Raster, um das Original zu verstehen, generiert Material mit den unterstützten Modellen (Seedance, PixVerse, MiniMax, Wan und andere) und rendert Untertitel und Motion Graphics in HTML.

Wie das Original entstanden ist, spielt dabei keine Rolle. Eine Realfilm-Vorlage läuft durch dieselbe Pipeline; wie viele Kameras im Einsatz waren oder wie ausgeleuchtet wurde, erfährst du nicht. Welche KI-Videos es nachbauen kann, hängt von seinen Modellen ab: kein Kling, kein Veo, kein eigener Avatar- oder 3D-Weg und keine KI-Musik – die musst du selbst mitbringen. Stark ist es bei Talking-Head-, Podcast- und Interview-Videos nach Skript, schwächer bei musikgetriebenen Schnitten, Produkt-Motion-Graphics und filmischen Kurzfilmen.

rea-video rendert kein Video. Es klärt Shot für Shot, ob etwas gedreht, mit KI generiert oder in Code gebaut wurde, und liefert dazu jeweils einen Drehplan, Prompts oder einen Code-Ansatz. Wer schnell etwas Ähnliches haben will, ist mit Hypit schneller. Wer verstehen will, wie das Original gemacht ist, und es günstig nachbauen möchte, nimmt rea-video. Die beiden vertragen sich gut.

</details>

<details>
<summary>Brauche ich ein Modell, das Video versteht? Was kostet das?</summary>

Nein. Der reine Tool-Modus läuft offline, kostet nichts und ist bei Originaldateien schon genau. Für neu komprimierte Downloads von Plattformen nimmst du ein videofähiges Modell dazu (Gemini oder Doubao, beides geht) oder einen Agenten, der Bilder sehen kann; bezahlt wird, was der jeweilige Dienst verlangt. Die automatische Videogenerierung (capsule-cinema) macht vorher einen kostenlosen Testlauf und ruft kostenpflichtige Modelle erst auf, wenn du bestätigst.

</details>

<details>
<summary>Baut es das ganze Video automatisch nach?</summary>

Teilweise. Mit installiertem [capsule-cinema](https://github.com/JuneYaooo/capsule-cinema) werden KI-Shots automatisch generiert und wieder an ihre Stelle in der Original-Timeline gesetzt. Realfilm-Shots drehst du selbst nach Drehplan, Code-Shots schreibt der Agent als Remotion-Projekt. Mehr dazu in [docs/replicate.md](../docs/replicate.md).

</details>

<details>
<summary>Kann ich einfach fremde Videos neu hochladen?</summary>

Nein. rea-video ist dafür gedacht, Aufbau, Tempo und Technik eines Videos zu verstehen und es dann mit Material nachzubauen, an dem du die Rechte hast. Fremdes Filmmaterial, fremde Musik, Figuren oder das Abbild anderer Personen sind tabu. Beim Veröffentlichen gelten die Regeln der Plattform und die Kennzeichnungspflichten für KI-Inhalte in deinem Land.

</details>

## Dokumentation

- [docs/what-it-detects.md](../docs/what-it-detects.md): alles, was erkannt wird (10 Bildtypen, Kamera, Licht, Grading, Audio)
- [docs/replicate.md](../docs/replicate.md): nachbauen anhand des Berichts
- [docs/cases.md](../docs/cases.md): die Fälle im Detail
- [docs/decompose.md](../docs/decompose.md): Erkennungsregeln
- [docs/cli.md](../docs/cli.md): CLI-Nutzung und capsule-cinema-Integration
- [rea_video/capabilities/](../rea_video/capabilities/README.md): Fähigkeitstabellen für Video-, Bild- und Audiomodelle; danach werden die Modelle für den Remake-Plan ausgewählt
- [eval/RESULTS.md](../eval/RESULTS.md): Evaluationsergebnisse

Die Doku gibt es vorerst nur auf Chinesisch.

## Community

Fragen, Analysen und Remake-Ideen gehören in die [GitHub Discussions](https://github.com/JuneYaooo/rea-video/discussions). Zum Quatschen gibt es unseren [Discord](https://discord.gg/dZj8D3GqWT). Wer Chinesisch spricht, findet uns auch auf [linux.do](https://linux.do/).

Du willst ein bestimmtes Video analysiert haben? Mach ein [Request-Issue](https://github.com/JuneYaooo/rea-video/issues/new?template=request_breakdown.yml) mit dem Link auf, dann veröffentlichen wir das Ergebnis als Fallbeispiel.

## Danksagung

Inspiriert von [REA (Reverse Engineer Anything)](https://github.com/morluto/rea): vom Sichtbaren aus zurückverfolgen, wie es entstanden ist, jede Aussage mit Belegen untermauern und per Messung überprüfen.
