<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../docs/brand/logo-light.svg">
  <img src="../docs/brand/logo-dark.svg" width="400" alt="rea-video">
</picture>

어떤 영상이든 어떻게 만들었는지 리버스 엔지니어링합니다.

샷 하나하나가 직접 찍은 건지, AI로 만든 건지, 코드로 짠 건지 가려내고 다시 만드는 방법까지 알려 줍니다.

[웹사이트](https://www.reavideo.ai) | [中文](README_zh.md) | [English](../README.md) | [Русский](README_ru.md) | [日本語](README_ja.md) | 한국어 | [Español](README_es.md) | [Português](README_pt.md) | [Français](README_fr.md) | [Deutsch](README_de.md) | [Tiếng Việt](README_vi.md)

[![Stars](https://img.shields.io/github/stars/JuneYaooo/rea-video?style=flat)](https://github.com/JuneYaooo/rea-video/stargazers)
![Python](https://img.shields.io/badge/python-%E2%89%A53.10-blue)
![Agent](https://img.shields.io/badge/runs%20in-Claude%20Code%20%7C%20Codex-8A2BE2)

<a href="https://trendshift.io/repositories/334878" target="_blank"><img src="https://trendshift.io/api/badge/trendshift/repositories/334878/daily" alt="JuneYaooo/rea-video | Trendshift" width="250" height="55"></a>

[![Visit our website](https://img.shields.io/badge/Visit%20our%20website-6644D8?style=for-the-badge)](https://www.reavideo.ai) [![Join our Discord](https://img.shields.io/badge/Join%20our%20Discord-5865F2?style=for-the-badge&logo=discord&logoColor=white)](https://discord.gg/dZj8D3GqWT) [![Follow on X](https://img.shields.io/badge/Follow%20%40yao__june12106-000000?style=for-the-badge&logo=x&logoColor=white)](https://x.com/yao_june12106)

⭐ *더 많은 사람이 rea-video를 찾을 수 있게 Star 한 번 눌러 주세요!*

<img src="../docs/cases/demo.gif" width="440" alt="왼쪽: 휴대폰으로 촬영한 TikTok 원본, 오른쪽: 다른 제품으로 바꾼 누군가의 AI 리메이크">

왼쪽은 휴대폰으로 찍은 TikTok 광고, 오른쪽은 제품만 바꾼 AI 리메이크입니다. rea-video 판정: 왼쪽은 전부 실사로 세트 하나에 카메라 위치 두 곳, 오른쪽은 전부 AI로 8개 샷을 3번에 나눠 생성.

</div>

## 빠른 시작

rea-video는 AI 에이전트가 쓰라고 만든 도구입니다. Claude Code, Codex처럼 명령을 실행할 수 있는 에이전트에게 이렇게 말하면 됩니다.

```text
https://github.com/JuneYaooo/rea-video 설치하고 이 영상 분석해 줘: /path/to/video.mp4
```

CLI 설치부터 워크플로 파악, 전체 실행까지 에이전트가 알아서 합니다. ffmpeg와 Python 3.10 이상만 있으면 됩니다.

<details><summary>직접 설치하기</summary>

```bash
brew install ffmpeg            # sudo apt install ffmpeg
git clone https://github.com/JuneYaooo/rea-video && cd rea-video
bash scripts/install_skill.sh  # CLI 설치(pip, 안 되면 pipx / 로컬 .venv) 후 skill 연결 → ~/.claude, ~/.codex, ~/.agents
rea-video --help
```

</details>

이런 결과를 받을 수 있습니다.

- 한 줄 요약. 예를 들면 "AI 영상 41% + 코드 UI 59%, 실제 화면 녹화 8초, 122 BPM 라이브러리 음악"
- 무엇을 찍고, 무엇을 생성하고, 무엇을 코드로 짤지 나눠 놓은 리메이크 계획
- 샷별 프레임, 근거, 프롬프트, 카메라·조명 메모, 오디오 분석까지 다 들어 있는 `report.html`

영상을 볼 수 있는 모델(Gemini, Doubao 둘 다 됩니다)을 붙이고 싶다면 에이전트에게 엔드포인트와 키만 알려 주세요. 실사/AI/3D 판정이 더 정확해지고, 샷마다 역설계한 프롬프트도 써 줍니다. 모델이 없어도 돌아가고, 에이전트가 이미지를 볼 수 있으면 애매한 샷은 에이전트가 직접 확인합니다.

> 리포트는 질문한 언어(중국어 또는 영어)로 나옵니다. 아래 예시 리포트는 영어입니다.

## 분석할 수 있는 영상

| 영상 유형 | 예시 | 알 수 있는 것 |
|---|---|---|
| 실사 촬영 | 토킹헤드, 테이블탑, 핸드헬드 제품 시연, 브이로그, 매장 방문 | 세트와 카메라 위치, 프레이밍, 카메라 무빙, 조명(장비 목록까지 포함한 12가지 셋업), 색보정 |
| AI 영상 | 텍스트/이미지 투 비디오, AI 숏드라마, AI 뮤직비디오 | 근거, 샷별 역설계 프롬프트, 몇 번에 나눠 생성할지와 어떤 모델을 쓸지 |
| 아바타 | 오디오로 움직이는 인물 사진, 립싱크 | 어떤 샷이 아바타인지, 인물 사진과 오디오는 뭐가 필요한지 |
| 3D / 애니메이션 | Blender / C4D 설명 영상, 제품 애니메이션, 2D 애니메이션, 스톱모션 | 영상 모델로 생성할지, 3D 코드로 렌더링할지 |
| 코드 / 템플릿 | 키네틱 타이포그래피, UI 데모, 차트, 슬라이드형 카드 | 텍스트, 레이아웃, 모션 타이밍. 그대로 Remotion 프로젝트로 다시 만들 수 있음 |
| 화면 녹화 | 소프트웨어 튜토리얼, 웹 데모 | 어느 부분이 직접 녹화해야 하는 실제 소재인지 |
| 혼합 / 편집 | AI 캐릭터 + 코드 UI + 실제 화면 녹화, AI 편집이 들어간 실사 촬영 | 샷마다 따로 판정한 뒤 원본 타임라인대로 다시 조립 |

화면을 어떻게 만들었는지 말고도, 어떤 영상이든 아래 내용을 함께 뽑아 줍니다.

- 자막과 꾸밈 텍스트: 줄마다 시작·끝 시간(SRT / ASS로 내보내기), 색상, 외곽선, 글자가 어떻게 등장하는지
- 스티커, 이모지, PIP(화면 속 화면): 어디에 얼마나 오래 떠 있는지
- 편집: 어디서 컷했는지, 컷 속도, 비트에 맞췄는지
- 오디오: 사람 목소리인지 AI 음성인지, 음악이 AI인지 라이브러리 음원인지와 BPM, 효과음이 들어가는 위치
- 직접 준비해야 할 소재: 화면 녹화, 스크린샷, 제품 사진

## 예시

`docs/cases/videos/`에 있는 샘플 영상은 저장소 용량을 줄이려고 다시 압축해서 TikTok / Douyin 플랫폼 태그가 지워져 있습니다. 그래서 직접 돌려 보면 아래 리포트와 결과가 달라지고, 비전 모델 없이 돌리면 차이가 더 큽니다. 똑같이 재현하려면 플랫폼에서 받은 원본 파일을 쓰세요.

<table>
<tr>
<td width="50%" valign="top">
<a href="../docs/cases.md#2-混合片ai-人物对话--代码界面--真实录屏"><img src="../docs/cases/dual_role/thumb.jpg"></a><br>
<b>혼합 미디어 클립</b> · 19초 · 10샷<br>
AI 캐릭터 대화 + 코드로 만든 UI + 실제 화면 녹화 8초. 대화 샷 5개가 UI 구간 사이사이에 흩어져 있지만 세트가 같아서 한 번에 생성할 수 있습니다.<br>
<a href="../docs/cases/videos/dual_role.mp4">영상</a> · <a href="../docs/cases/dual_role/report_en.md">리포트</a>
</td>
<td width="50%" valign="top">
<a href="../docs/cases.md#3-3d-科普片咸鸭蛋为什么会流油"><img src="../docs/cases/salted_egg/thumb.jpg"></a><br>
<b>3D 설명 영상</b> · 67초 · 21샷<br>
전부 3D에 AI 내레이션. 영상 생성 10번이면 되고, LLM에게 Blender / Three.js 코드를 짜게 해도 됩니다.<br>
<a href="../docs/cases/videos/salted_egg.mp4">영상</a> · <a href="../docs/cases/salted_egg/report_en.md">리포트</a>
</td>
</tr>
<tr>
<td width="50%" valign="top">
<a href="../docs/cases.md#4-代码-ui-动效产品宣传片"><img src="../docs/cases/v10/thumb.jpg"></a><br>
<b>제품 홍보 영상</b> · 70초 · 12샷<br>
83%는 코드로 만든 모션 그래픽, 12%는 화면 녹화. 영상 모델 없이 Remotion 프로젝트 하나면 됩니다.<br>
<a href="../docs/cases/videos/v10_oiioii_gen_coding_first.mp4">영상</a> · <a href="../docs/cases/v10/report_en.md">리포트</a>
</td>
<td width="50%" valign="top">
<a href="../docs/cases.md#5-ai-音乐-mv歌是-ai-写的还是曲库的"><img src="../docs/cases/qing_mv/thumb.jpg"></a><br>
<b>AI 뮤직비디오</b> · 165초 · 86샷<br>
노래가 AI로 만든 곡이라는 걸 맞혔습니다(실제로 Suno로 만든 곡). 비전 모델은 일부 샷을 "실사 드라마"로 봤지만, 에이전트가 두루마리에 적힌 가짜 한자를 찾아내 AI로 판정했습니다.<br>
<a href="../docs/cases/videos/qing_mv.mp4">영상</a> · <a href="../docs/cases/qing_mv/report_en.md">리포트</a>
</td>
</tr>
<tr>
<td width="50%" valign="top">
<a href="../docs/cases.md#6-实拍带货沉浸式开箱"><img src="../docs/cases/unboxing/thumb.jpg"></a><br>
<b>실사 언박싱</b> · 72초 · 29샷<br>
전부 실제 촬영입니다. 부감 휴대폰 거치대, 러그 한 장, 카메라 위치 한 곳, 보이스오버 없이 현장음과 라이브러리 BGM. 플랫폼 트랜스코딩을 거친 탓에 오프라인 도구는 35%를 AI로 판정했는데, 에이전트가 검토한 뒤 97% 실사로 바로잡았습니다.<br>
<a href="../docs/cases/videos/unboxing.mp4">영상</a> · <a href="../docs/cases/unboxing/report_en.md">리포트</a>
</td>
<td width="50%" valign="top">
<a href="../docs/cases.md#7-ai-与真人混合用自己的出镜视频生成带货片"><img src="../docs/cases/ai_daihuo/thumb.jpg"></a><br>
<b>AI + 실제 인물 혼합</b> · 58초 · 21샷<br>
75%는 실제 촬영(토킹헤드 + 휴대폰 화면 촬영), 25%는 AI입니다. 크리에이터가 자기 출연 영상과 제품 사진 두 장을 Jimeng에 넣어 "실제 인물"이 나오는 제품 구간을 만들었습니다. AI 부분은 Jimeng 워터마크와 선물 상자에 깨진 글자로 잡아냈습니다.<br>
<a href="../docs/cases/videos/ai_daihuo.mp4">영상</a> · <a href="../docs/cases/ai_daihuo/report_en.md">리포트</a>
</td>
</tr>
</table>

## 리메이크

rea-video로 영상을 분석한 뒤 [capsule-cinema](https://github.com/JuneYaooo/capsule-cinema)의 리메이크 레시피로 새 버전을 만듭니다. 카메라, 움직임, 템포, 전환은 원본 그대로 두고 고른 요소만 바꿉니다.
아래 결과는 직접 띄운 MiniMax H3로 만들었습니다. 원본 샷은 모션 레퍼런스로, 요소를 바꾼 키프레임(gpt-image-2)은 룩 레퍼런스로 썼습니다.
OiiOii가 WeChat 글에서 보여 준 리메이크 세 편을 골라 편마다 두 버전씩 만들었습니다. 하나는 OiiOii와 똑같이 바꾼 버전, 다른 하나는 주인공·배경·소품까지 바꾼 버전입니다.
GIF마다 원본, OiiOii 리메이크, 우리 리메이크, 요소 교체 버전 네 개가 동시에 재생됩니다.

<table>
<tr><td>
<b>부감 의상 체인지</b> · 12초<br>
같은 교체: 여성 → 남성, 의상 세 벌 → 거기 맞춘 남성복. 요소 교체: 중국식 서재에서 역사 한푸 세 벌을 갈아입는 소녀, 리모컨은 둥근 부채로.<br>
<img src="../docs/cases/remake/outfit.gif"><br>
<a href="../docs/cases/remake/outfit_compare.mp4">HD 비교 영상(오디오 포함)</a> · <a href="../docs/cases/remake/outfit_sheet.jpg">같은 순간 스틸컷</a>
</td></tr>
<tr><td>
<b>페이퍼 크래프트 / 수채화 애니메이션</b> · 30초<br>
같은 교체: 새 점토 소녀를 주인공으로. 요소 교체: 여우, 숲 → 산호초, 구름 → 별이 빛나는 하늘, 노을 → 오로라.<br>
<img src="../docs/cases/remake/paper.gif"><br>
<a href="../docs/cases/remake/paper_compare.mp4">HD 비교 영상(오디오 포함)</a> · <a href="../docs/cases/remake/paper_sheet.jpg">같은 순간 스틸컷</a>
</td></tr>
<tr><td>
<b>핸드헬드 제품 영상</b> · 21초 · 11샷<br>
같은 교체: 오리지널 신제품, 영어 스티커 → 중국어 자막. 요소 교체: 분홍색 제품, 주방 → 캠핑 테이블, 새로운 재료.<br>
<img src="../docs/cases/remake/juicer.gif"><br>
<a href="../docs/cases/remake/juicer_compare.mp4">HD 비교 영상(오디오 포함)</a> · <a href="../docs/cases/remake/juicer_sheet.jpg">같은 순간 스틸컷</a>
</td></tr>
</table>

HD 비교 영상에는 원본 오디오를 썼습니다. 원본과 OiiOii 버전은 해당 글에서 가져왔고, 비교용으로만 보여 드립니다.

## 정확도

제작 방식 판정 정확도(샷 길이로 가중):

| | 튜닝 세트 (15) | 홀드아웃 (16) | 재인코딩된 WeChat 영상 (10) |
|---|---|---|---|
| 도구만(오프라인, 무료) | 98.3% | 99.6% / 98.9% | 88.6% |
| + 비전 모델(Gemini) | — | 99.6% / 99.8% | 99.6% |
| + 에이전트 시각 검토 | — | 99.6% / 99.8% | 100% |

홀드아웃 칸의 두 숫자는 각각 holdout(영상 9개), holdout2(영상 7개) 결과입니다.

원본 파일이라면 대부분 도구만으로 충분합니다. 플랫폼에서 내려받은 영상은 재압축되면서 노이즈 근거가 날아가기 때문에, 다시 99% 이상으로 올리려면 시각 검토가 필요합니다.

실제 소재 탐지율은 97–99%이고, 직접 라벨링한 9개 영상에서 샷 경계는 재현율 95%, 정밀도 94%입니다. 자세한 수치와 재현 방법은 [eval/RESULTS.md](../eval/RESULTS.md)에 있습니다.

## 작동 방식

![rea-video 파이프라인](../docs/rea-flow_ko.svg)

1. 분할: 영상을 샷 단위로 자르고, 오디오는 음성·음악·효과음으로 나눕니다.
2. 근거 수집: 프레임을 측정하고(프레임 케이던스, 센서 노이즈, 화면 전체가 하나의 평면처럼 패닝하는지, 메타데이터의 AIGC 태그), 이미지를 보고(손, 글자, 물리 법칙), 소리를 듣습니다(BPM, 키, 노래인지 말인지).
3. 판정: AIGC 태그나 프레임 케이던스 같은 확실한 근거가 "그래 보인다"보다 우선합니다. 근거끼리 부딪히면 표시해 두고 에이전트가 직접 보고 검토합니다.
4. 리메이크 계획: 대상 영상 모델이 실제로 할 수 있는 범위(최대 클립 길이, 멀티샷 지원 여부, 레퍼런스 이미지를 몇 장까지 받는지 등)에 맞춰 샷을 묶습니다.

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=JuneYaooo/rea-video&type=Date)](https://star-history.com/#JuneYaooo/rea-video&Date)

## FAQ

<details>
<summary>Hypit 같은 원클릭 리메이크 도구와는 뭐가 다른가요?</summary>

[Hypit](https://github.com/hypit-ai/hypit)은 레퍼런스 영상을 받아서 새 영상을 만들어 줍니다. 에이전트가 프레임 그리드를 읽어 원본을 파악하고, 지원하는 모델(Seedance, PixVerse, MiniMax, Wan 등)로 영상을 생성하고, 자막과 모션 그래픽은 HTML로 렌더링합니다.

원본을 어떻게 만들었는지는 따지지 않습니다. 실사 원본도 같은 파이프라인을 타기 때문에 카메라를 몇 대 썼는지, 조명을 어떻게 쳤는지는 알려 주지 않습니다. 어떤 AI 영상까지 따라 만들 수 있는지는 갖춘 모델에 달려 있습니다. Kling이나 Veo는 없고, 아바타나 3D 전용 경로도 없고, AI 음악도 없어서 음악은 직접 준비해야 합니다. 대본대로 가는 토킹헤드, 팟캐스트, 인터뷰 영상에 가장 강하고, 음악 중심 편집, 제품 모션 그래픽, 시네마틱 숏폼에는 약한 편입니다.

rea-video는 영상을 렌더링하지 않습니다. 샷마다 찍은 건지, AI로 생성한 건지, 코드로 만든 건지 가려낸 다음 각각에 맞는 촬영 계획, 프롬프트, 코드 접근법을 알려 줍니다. 비슷한 영상을 빨리 뽑고 싶다면 Hypit이 더 빠릅니다. 원본이 어떻게 만들어졌는지 이해하고 싸게 리메이크하고 싶다면 rea-video를 쓰세요. 둘을 같이 써도 괜찮습니다.

</details>

<details>
<summary>영상을 볼 수 있는 모델이 꼭 있어야 하나요? 비용은요?</summary>

없어도 됩니다. 도구만 쓰는 모드는 오프라인에 무료이고, 원본 파일이라면 이것만으로도 정확합니다. 재압축된 플랫폼 영상이라면 영상을 볼 수 있는 모델(Gemini, Doubao 둘 다 됩니다)을 붙이거나 이미지를 볼 수 있는 에이전트를 쓰세요. 비용은 그 서비스 요금만큼 나옵니다. 자동 영상 생성(capsule-cinema)은 먼저 무료로 드라이런을 돌려 보고, 확인한 뒤에만 유료 모델을 호출합니다.

</details>

<details>
<summary>영상 전체를 자동으로 리메이크할 수 있나요?</summary>

일부는 됩니다. [capsule-cinema](https://github.com/JuneYaooo/capsule-cinema)를 설치하면 AI 샷은 자동으로 생성해서 원본 타임라인에 다시 넣어 줍니다. 실사 샷은 촬영 계획을 보고 직접 찍고, 코드 샷은 에이전트가 Remotion 프로젝트로 짭니다. 자세한 건 [docs/replicate.md](../docs/replicate.md)를 보세요.

</details>

<details>
<summary>남의 영상을 그대로 다시 올려도 되나요?</summary>

안 됩니다. rea-video는 영상의 구조, 템포, 기법을 배워서 내가 권리를 가진 소재로 다시 만들기 위한 도구입니다. 다른 사람의 영상, 음악, 캐릭터, 초상은 가져다 쓰지 마세요. 올릴 때는 플랫폼 규정과 지역별 AI 콘텐츠 표시 규정을 지켜 주세요.

</details>

## 문서

- [docs/what-it-detects.md](../docs/what-it-detects.md): 탐지하는 항목 전체(10가지 화면 유형, 카메라, 조명, 색보정, 오디오)
- [docs/replicate.md](../docs/replicate.md): 리포트 보고 리메이크하기
- [docs/cases.md](../docs/cases.md): 사례 자세히 보기
- [docs/decompose.md](../docs/decompose.md): 판정 규칙
- [docs/cli.md](../docs/cli.md): CLI 사용법, capsule-cinema 연동
- [rea_video/capabilities/](../rea_video/capabilities/README.md): 영상 / 이미지 / 오디오 모델 능력표. 리메이크 계획에서 모델 고를 때 씀
- [eval/RESULTS.md](../eval/RESULTS.md): 평가 결과

문서는 아직 중국어로만 있습니다.

## 커뮤니티

질문, 분석 사례, 리메이크 아이디어는 [GitHub Discussions](https://github.com/JuneYaooo/rea-video/discussions)에 남겨 주세요. [Discord](https://discord.gg/dZj8D3GqWT)에서도 이야기 나눌 수 있습니다. 중국어 사용자라면 [linux.do](https://linux.do/)에서도 만날 수 있습니다.

분석해 봤으면 하는 영상이 있나요? 링크를 담아 [요청 이슈](https://github.com/JuneYaooo/rea-video/issues/new?template=request_breakdown.yml)를 열어 주시면 결과를 사례로 공개합니다.

## 크레딧

[REA (Reverse Engineer Anything)](https://github.com/morluto/rea)에서 영감을 받았습니다. 눈에 보이는 것에서 출발해 어떻게 만들었는지 거꾸로 따라가고, 모든 주장에는 근거를 달고, 측정으로 검증합니다.
