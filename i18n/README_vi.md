<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../docs/brand/logo-light.svg">
  <img src="../docs/brand/logo-dark.svg" width="400" alt="rea-video">
</picture>

Phân tích ngược mọi video.

Soi từng shot xem cảnh đó quay thật, tạo bằng AI hay render từ code — và chỉ cách làm lại.

[Trang web](https://www.reavideo.ai) | [中文](README_zh.md) | [English](../README.md) | [Русский](README_ru.md) | [日本語](README_ja.md) | [한국어](README_ko.md) | [Español](README_es.md) | [Português](README_pt.md) | [Français](README_fr.md) | [Deutsch](README_de.md) | Tiếng Việt

[![Stars](https://img.shields.io/github/stars/JuneYaooo/rea-video?style=flat)](https://github.com/JuneYaooo/rea-video/stargazers)
![Python](https://img.shields.io/badge/python-%E2%89%A53.10-blue)
![Agent](https://img.shields.io/badge/runs%20in-Claude%20Code%20%7C%20Codex-8A2BE2)

<a href="https://trendshift.io/repositories/334878" target="_blank"><img src="https://trendshift.io/api/badge/trendshift/repositories/334878/daily" alt="JuneYaooo/rea-video | Trendshift" width="250" height="55"></a>

[![Visit our website](https://img.shields.io/badge/Visit%20our%20website-6644D8?style=for-the-badge)](https://www.reavideo.ai) [![Join our Discord](https://img.shields.io/badge/Join%20our%20Discord-5865F2?style=for-the-badge&logo=discord&logoColor=white)](https://discord.gg/dZj8D3GqWT) [![Follow on X](https://img.shields.io/badge/Follow%20%40yao__june12106-000000?style=for-the-badge&logo=x&logoColor=white)](https://x.com/yao_june12106)

⭐ *Thấy hữu ích thì tặng repo một Star để nhiều người biết đến rea-video hơn nhé!*

<img src="../docs/cases/demo.gif" width="440" alt="Trái: video gốc trên TikTok quay bằng điện thoại; phải: bản làm lại bằng AI với sản phẩm khác">

Bên trái là quảng cáo TikTok quay bằng điện thoại. Bên phải là bản remake bằng AI với một sản phẩm khác. Kết luận của rea-video: bên trái 100% quay thật với 1 bối cảnh và 2 góc máy; bên phải 100% là AI, gồm 8 shot trong 3 lần tạo.

</div>

## Bắt đầu nhanh

rea-video được thiết kế cho AI agent. Trong Claude Code, Codex hoặc bất kỳ agent nào chạy được lệnh terminal, bạn chỉ cần nhắn:

```text
Cài https://github.com/JuneYaooo/rea-video rồi phân tích video này giúp tôi: /path/to/video.mp4
```

Agent sẽ tự cài CLI, đọc quy trình làm việc và chạy trọn bộ từ đầu đến cuối. Bạn chỉ cần cài sẵn ffmpeg và Python 3.10+.

<details><summary>Cài thủ công</summary>

```bash
brew install ffmpeg            # hoặc: sudo apt install ffmpeg
git clone https://github.com/JuneYaooo/rea-video && cd rea-video
bash scripts/install_skill.sh  # cài CLI (qua pip, hoặc pipx / .venv cục bộ nếu pip bị chặn) và liên kết skill vào ~/.claude, ~/.codex, ~/.agents
rea-video --help
```

</details>

Kết quả nhận được:

- kết luận tóm tắt trong 1 dòng, ví dụ: "41% video AI + 59% giao diện code, 8 giây quay màn hình thật, nhạc kho 122 BPM"
- kế hoạch làm lại (remake), tách rõ phần nào cần tự quay, phần nào tạo bằng AI và phần nào viết code
- file báo cáo đầy đủ `report.html` gồm ảnh từng shot, bằng chứng nhận định, prompt, ghi chú góc máy & ánh sáng cùng phần bóc tách âm thanh

Bạn cũng có thể đấu nối thêm một model hiểu video (cả Gemini lẫn Doubao đều dùng được) bằng cách đưa endpoint và API key cho agent. Khi có model này, kết quả phân loại quay thật / AI / 3D sẽ chính xác hơn và mỗi shot đều được suy ngược ra prompt gốc. Không gắn thêm vẫn chạy tốt — nếu agent của bạn xem được ảnh, nó sẽ tự kiểm tra lại những shot chưa chắc chắn.

> Báo cáo được xuất theo ngôn ngữ bạn yêu cầu (tiếng Trung hoặc tiếng Anh). Các báo cáo ví dụ bên dưới là bản tiếng Anh.

## Phân tích được những gì

| Loại video | Ví dụ | Kết quả nhận được |
|---|---|---|
| Quay thật | Talking-head, quay trên bàn (tabletop), cầm tay giới thiệu sản phẩm, vlog, review cửa hàng | Số bối cảnh và vị trí đặt máy, cỡ cảnh, chuyển động máy, ánh sáng (12 kiểu setup kèm danh sách thiết bị), chỉnh màu (color grade) |
| Video AI | Text/image-to-video, phim ngắn AI, MV nhạc AI | Bằng chứng nhận định, prompt suy ngược cho từng shot, cách gộp shot theo từng lượt tạo và nên dùng model nào |
| Avatar | Chân dung nói theo file âm thanh, khớp môi (lip-sync) | Xác định shot nào là avatar, cần chuẩn bị ảnh chân dung và file âm thanh gì |
| 3D / hoạt hình | Video giải thích bằng Blender / C4D, animation sản phẩm, hoạt hình 2D, stop-motion | Nên tạo bằng model video hay render từ code 3D |
| Code / template | Chữ động (kinetic type), demo UI, biểu đồ, thẻ kiểu slide | Nội dung chữ, bố cục và nhịp chuyển động, sẵn sàng dựng lại thành project Remotion |
| Quay màn hình | Video hướng dẫn phần mềm, demo web | Chỉ rõ đoạn nào là tư liệu thật bạn phải tự quay lấy |
| Hỗn hợp / cắt ghép | Nhân vật AI + UI viết bằng code + quay màn hình thật; cảnh quay thật có chèn hiệu ứng AI | Đánh giá riêng từng shot rồi ghép lại đúng theo timeline gốc |

Ngoài cách tạo phần hình ảnh, mỗi lượt phân tích còn bóc tách thêm:

- Phụ đề và text hiệu ứng: thời điểm bắt đầu và kết thúc từng câu (xuất ra SRT / ASS), kèm màu sắc, viền chữ và kiểu xuất hiện
- Sticker, emoji, hình trong hình (PiP): nằm ở đâu và hiển thị bao lâu
- Dựng phim: vị trí các điểm cắt, nhịp cắt nhanh hay chậm, cắt có khớp nhịp nhạc không
- Âm thanh: giọng người thật hay AI, nhạc nền do AI tạo hay lấy từ kho nhạc kèm BPM, vị trí từng hiệu ứng âm thanh (SFX)
- Tư liệu bạn cần tự chuẩn bị: đoạn quay màn hình, ảnh chụp màn hình, ảnh sản phẩm

## Các ví dụ

Các video mẫu trong `docs/cases/videos/` đã được nén lại để giữ repo gọn nhẹ, nên các thẻ metadata của TikTok / Douyin không còn nữa. Vì vậy nếu bạn tự chạy lại trên các file này, kết quả sẽ khác với báo cáo bên dưới, nhất là khi không bật vision model. Muốn tái hiện đúng kết quả, hãy dùng file gốc tải trực tiếp từ nền tảng.

<table>
<tr>
<td width="50%" valign="top">
<a href="../docs/cases.md#2-混合片ai-人物对话--代码界面--真实录屏"><img src="../docs/cases/dual_role/thumb.jpg"></a><br>
<b>Video hỗn hợp</b> · 19 giây · 10 shot<br>
Nhân vật AI nói chuyện + UI dựng bằng code + 8 giây quay màn hình thật. 5 shot đối thoại bị ngắt quãng bởi các đoạn UI nhưng chung 1 bối cảnh, nên chỉ cần 1 lượt tạo là phủ trọn tất cả.<br>
<a href="../docs/cases/videos/dual_role.mp4">Video</a> · <a href="../docs/cases/dual_role/report_en.md">Báo cáo</a>
</td>
<td width="50%" valign="top">
<a href="../docs/cases.md#3-3d-科普片咸鸭蛋为什么会流油"><img src="../docs/cases/salted_egg/thumb.jpg"></a><br>
<b>Video giải thích 3D</b> · 67 giây · 21 shot<br>
Toàn bộ là 3D kèm lời bình AI. Bạn có thể tạo trong 10 lượt video AI, hoặc nhờ LLM viết code Blender / Three.js.<br>
<a href="../docs/cases/videos/salted_egg.mp4">Video</a> · <a href="../docs/cases/salted_egg/report_en.md">Báo cáo</a>
</td>
</tr>
<tr>
<td width="50%" valign="top">
<a href="../docs/cases.md#4-代码-ui-动效产品宣传片"><img src="../docs/cases/v10/thumb.jpg"></a><br>
<b>Video quảng bá sản phẩm</b> · 70 giây · 12 shot<br>
83% là motion graphics chạy bằng code, 12% quay màn hình. Không cần dùng model tạo video; chỉ một project Remotion là xử lý xong.<br>
<a href="../docs/cases/videos/v10_oiioii_gen_coding_first.mp4">Video</a> · <a href="../docs/cases/v10/report_en.md">Báo cáo</a>
</td>
<td width="50%" valign="top">
<a href="../docs/cases.md#5-ai-音乐-mv歌是-ai-写的还是曲库的"><img src="../docs/cases/qing_mv/thumb.jpg"></a><br>
<b>MV nhạc AI</b> · 165 giây · 86 shot<br>
Bắt đúng bài hát do AI tạo (làm bằng Suno). Vision model từng nhận nhầm vài shot là "phim cổ trang người đóng"; agent soi ra chữ Hán giả trên cuộn giấy nên kết luận là AI.<br>
<a href="../docs/cases/videos/qing_mv.mp4">Video</a> · <a href="../docs/cases/qing_mv/report_en.md">Báo cáo</a>
</td>
</tr>
<tr>
<td width="50%" valign="top">
<a href="../docs/cases.md#6-实拍带货沉浸式开箱"><img src="../docs/cases/unboxing/thumb.jpg"></a><br>
<b>Mở hộp quay thật</b> · 72 giây · 29 shot<br>
100% quay thật: điện thoại gắn giá quay từ trên xuống, một tấm thảm, một góc máy, không thu lời bình, chỉ có tiếng phòng và nhạc nền từ kho. Sau khi bị nền tảng nén lại, công cụ offline đoán nhầm 35% là AI; qua bước agent rà soát ảnh thì kết quả về đúng 97% quay thật.<br>
<a href="../docs/cases/videos/unboxing.mp4">Video</a> · <a href="../docs/cases/unboxing/report_en.md">Báo cáo</a>
</td>
<td width="50%" valign="top">
<a href="../docs/cases.md#7-ai-与真人混合用自己的出镜视频生成带货片"><img src="../docs/cases/ai_daihuo/thumb.jpg"></a><br>
<b>Kết hợp AI + người thật</b> · 58 giây · 21 shot<br>
75% quay thật (người dẫn nói trước ống kính + quay màn hình điện thoại) và 25% AI: tác giả đưa clip tự quay và 2 ảnh sản phẩm vào Jimeng để tạo đoạn giới thiệu "người thật". Phần AI bị lộ qua watermark Jimeng và chữ trên hộp quà bị biến dạng.<br>
<a href="../docs/cases/videos/ai_daihuo.mp4">Video</a> · <a href="../docs/cases/ai_daihuo/report_en.md">Báo cáo</a>
</td>
</tr>
</table>

## Kết quả remake

Sau khi rea-video bóc tách xong, công thức remake trong [capsule-cinema](https://github.com/JuneYaooo/capsule-cinema) sẽ tạo ra phiên bản mới giữ nguyên góc máy, chuyển động, nhịp điệu và chuyển cảnh của bản gốc, chỉ thay những thành phần bạn chọn.
Các bản dưới đây được tạo bằng MiniMax H3 tự triển khai, lấy shot gốc làm tham chiếu chuyển động và dùng các keyframe đã thay đổi thành phần (gpt-image-2) để định hình phần nhìn.
Dưới đây là 3 bài remake mà OiiOii từng giới thiệu trong các bài viết WeChat. Chúng tôi làm 2 phiên bản cho mỗi bài: một bản thay đúng thành phần như OiiOii, và một bản thay luôn cả chủ thể, bối cảnh lẫn đạo cụ.
Mỗi ảnh GIF phát đồng bộ 4 phiên bản: bản gốc, bản remake của OiiOii, bản remake của chúng tôi và bản thay đổi thành phần.

<table>
<tr><td>
<b>Thay trang phục góc quay từ trên xuống</b> · 12 giây<br>
Thay tương đương: nữ → nam, 3 bộ đồ → trang phục nam tương ứng. Thay thành phần: cô gái mặc 3 bộ Hán phục cổ trang trong thư phòng Trung Hoa; điều khiển từ xa biến thành quạt tròn.<br>
<img src="../docs/cases/remake/outfit.gif"><br>
<a href="../docs/cases/remake/outfit_compare.mp4">Video đối chiếu HD (có âm thanh)</a> · <a href="../docs/cases/remake/outfit_sheet.jpg">ảnh cắt cùng thời điểm</a>
</td></tr>
<tr><td>
<b>Hoạt hình cắt giấy / màu nước</b> · 30 giây<br>
Thay tương đương: cô bé đất sét mới làm nhân vật chính. Thay thành phần: một chú cáo; rừng → rạn san hô, mây → bầu trời sao, hoàng hôn → cực quang.<br>
<img src="../docs/cases/remake/paper.gif"><br>
<a href="../docs/cases/remake/paper_compare.mp4">Video đối chiếu HD (có âm thanh)</a> · <a href="../docs/cases/remake/paper_sheet.jpg">ảnh cắt cùng thời điểm</a>
</td></tr>
<tr><td>
<b>Video sản phẩm cầm tay</b> · 21 giây · 11 shot<br>
Thay tương đương: một sản phẩm mới hoàn toàn, nhãn dán tiếng Anh → chú thích tiếng Trung. Thay thành phần: sản phẩm màu hồng, nhà bếp → bàn cắm trại, nguyên liệu mới.<br>
<img src="../docs/cases/remake/juicer.gif"><br>
<a href="../docs/cases/remake/juicer_compare.mp4">Video đối chiếu HD (có âm thanh)</a> · <a href="../docs/cases/remake/juicer_sheet.jpg">ảnh cắt cùng thời điểm</a>
</td></tr>
</table>

Các video đối chiếu HD sử dụng âm thanh gốc. Bản gốc và các bản của OiiOii được trích từ bài viết để tiện đối chiếu.

## Độ chính xác

Độ chính xác khi kết luận cách dựng video, tính trọng số theo thời lượng từng shot:

| | Tập tinh chỉnh (15) | Tập kiểm thử (16) | Video WeChat bị nén lại (10) |
|---|---|---|---|
| Chỉ dùng công cụ (offline, miễn phí) | 98.3% | 99.6% / 98.9% | 88.6% |
| + vision model (Gemini) | — | 99.6% / 99.8% | 99.6% |
| + agent rà soát bằng ảnh | — | 99.6% / 99.8% | 100% |

Cột Tập kiểm thử hiển thị hai con số: holdout (9 video) và holdout2 (7 video).

Với file gốc, riêng bộ công cụ thường đã đủ chuẩn. Video tải từ các nền tảng mạng xã hội đã bị nén lại làm mất dấu vết nhiễu cảm biến, nên cần kiểm tra thêm bằng hình ảnh để đưa độ chính xác lên lại trên 99%.

Nhận diện tư liệu thật đạt 97–99%; trên 9 clip gắn nhãn thủ công, nhận diện điểm cắt cảnh đạt recall 95% và precision 94%. Chi tiết số liệu và cách chạy lại phép đo: [eval/RESULTS.md](../eval/RESULTS.md).

## Cơ chế hoạt động

![Quy trình rea-video](../docs/rea-flow_vi.svg)

1. Tách lớp: cắt video thành từng shot và tách âm thanh thành 3 track gồm lời thoại, nhạc nền và hiệu ứng.
2. Thu thập bằng chứng: đo đạc thông số (nhịp lặp khung hình, nhiễu cảm biến, xem toàn khung hình có chuyển động như một mặt phẳng hay không, thẻ AIGC trong metadata), nhìn ảnh (bàn tay, chữ viết, quy luật vật lý) và lắng nghe âm thanh (BPM, giọng điệu, hát hay nói).
3. Kết luận: bằng chứng cứng như thẻ AIGC hay nhịp khung hình luôn được ưu tiên hơn cảm giác "trông giống". Những chỗ các nguồn cho kết quả trái ngược sẽ được đánh dấu để agent xem ảnh kiểm tra lại.
4. Lên kế hoạch remake: gom nhóm các shot theo đúng giới hạn thực tế của model video mục tiêu — như thời lượng tối đa mỗi clip, khả năng xuất đa shot và số ảnh tham chiếu đầu vào.

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=JuneYaooo/rea-video&type=Date)](https://star-history.com/#JuneYaooo/rea-video&Date)

## Câu hỏi thường gặp

<details>
<summary>Công cụ này khác gì với các công cụ remake một chạm như Hypit?</summary>

[Hypit](https://github.com/hypit-ai/hypit) lấy một video tham chiếu rồi dựng ngay thành video mới: agent đọc lưới khung hình để hiểu bản gốc, tạo cảnh bằng các model mà nó hỗ trợ (Seedance, PixVerse, MiniMax, Wan...), rồi render phụ đề và motion graphics bằng HTML.

Nó không quan tâm bản gốc được làm bằng cách nào. Một video quay thật cũng đi qua đúng một quy trình đó; nó sẽ không cho bạn biết cảnh gốc dùng mấy góc máy hay đánh đèn ra sao. Mức độ khớp với bản gốc của phần video AI phụ thuộc vào các model nó tích hợp: chưa có Kling hay Veo, không có luồng riêng cho avatar hay 3D, và không tạo nhạc AI (bạn phải tự chuẩn bị nhạc). Hypit làm tốt nhất với video nói trước ống kính, podcast và phỏng vấn bám sát kịch bản; còn với video cắt dựng theo nhạc, motion graphics sản phẩm hay phim ngắn mang chất điện ảnh thì yếu hơn.

rea-video không trực tiếp xuất ra video. Nó phân tích từng shot xem cảnh nào được quay thật, tạo bằng AI hay dựng bằng code, rồi đưa ra phương án quay, bộ prompt hoặc hướng viết code cho từng phần. Nếu chỉ muốn nhái nhanh một bản na ná, Hypit sẽ nhanh hơn. Còn muốn hiểu rõ bản gốc được làm thế nào và remake với chi phí tối ưu, hãy dùng rea-video. Cả hai kết hợp với nhau rất ổn.

</details>

<details>
<summary>Có bắt buộc phải dùng model hiểu video không? Chi phí thế nào?</summary>

Không. Chế độ chỉ dùng công cụ chạy hoàn toàn offline, miễn phí và đã rất chính xác trên file gốc. Với các video tải từ nền tảng đã qua nén lại, bạn nên gắn thêm một model hiểu video (Gemini hoặc Doubao đều được) hoặc dùng agent có khả năng xem ảnh; khi đó bạn chỉ trả phí theo mức giá của dịch vụ bạn chọn. Tính năng tự động tạo video (capsule-cinema) luôn chạy thử miễn phí (dry run) trước và chỉ gọi các model trả phí sau khi bạn xác nhận.

</details>

<details>
<summary>Nó có tự động remake toàn bộ video được không?</summary>

Một phần. Khi cài thêm [capsule-cinema](https://github.com/JuneYaooo/capsule-cinema), các shot AI sẽ được tạo và đặt lại đúng vị trí trên timeline gốc một cách tự động. Các shot quay thật bạn sẽ tự quay theo kế hoạch quay, còn các shot dựng bằng code sẽ do agent viết thành project Remotion. Xem thêm [docs/replicate.md](../docs/replicate.md).

</details>

<details>
<summary>Tôi có thể lấy video của người khác rồi đăng lại nguyên bản không?</summary>

Không. rea-video sinh ra để bạn học hỏi cấu trúc, nhịp dựng và kỹ thuật của một video, sau đó tự làm lại bằng tư liệu mà bạn có bản quyền. Đừng tái sử dụng cảnh quay, âm nhạc, nhân vật hay hình ảnh cá nhân của người khác. Khi xuất bản, hãy tuân thủ quy định của nền tảng và yêu cầu gắn nhãn nội dung AI tại địa phương.

</details>

## Tài liệu

- [docs/what-it-detects.md](../docs/what-it-detects.md): mọi thứ công cụ phát hiện được (10 loại hình ảnh, góc máy, ánh sáng, chỉnh màu, âm thanh)
- [docs/replicate.md](../docs/replicate.md): hướng dẫn remake từ báo cáo
- [docs/cases.md](../docs/cases.md): chi tiết từng ví dụ mẫu
- [docs/decompose.md](../docs/decompose.md): bộ quy tắc phân tích
- [docs/cli.md](../docs/cli.md): cách dùng CLI và tích hợp capsule-cinema
- [rea_video/capabilities/](../rea_video/capabilities/README.md): bảng năng lực các model video / ảnh / âm thanh dùng để chọn model cho kế hoạch remake
- [eval/RESULTS.md](../eval/RESULTS.md): kết quả đánh giá

Hiện tại bộ tài liệu chi tiết mới có bản tiếng Trung.

## Cộng đồng

Đặt câu hỏi, trao đổi case phân tích và ý tưởng remake tại [GitHub Discussions](https://github.com/JuneYaooo/rea-video/discussions). Bạn cũng có thể trò chuyện trên [Discord](https://discord.gg/dZj8D3GqWT). Cộng đồng tiếng Trung có thể ghé qua [linux.do](https://linux.do/).

Muốn nhờ bóc tách một video nào đó? Hãy mở một [issue yêu cầu](https://github.com/JuneYaooo/rea-video/issues/new?template=request_breakdown.yml) kèm đường link, chúng tôi sẽ công bố kết quả thành một case mẫu.

## Ghi nhận

Lấy cảm hứng từ [REA (Reverse Engineer Anything)](https://github.com/morluto/rea): đi ngược từ những gì quan sát được để truy ra cách chế tác, mọi kết luận đều có bằng chứng đi kèm và được kiểm chứng bằng đo đạc.
