"""Packaging layer: subtitle timeline + style, 花字, stickers / GIFs, SFX alignment, exports."""
import cv2
import numpy as np
import pytest

from conftest import _photo_like, _write
from rea_video import packaging as P
from rea_video.media import video_info

W, H, FPS = 360, 640, 30


def _outlined(img, text, org, scale, color, thick, outline=(0, 0, 0)):
    # the outline is the text stamped around the glyph (OpenCV 5 ignores thickness for anti-aliased text)
    r = max(2, int(round(3 * scale)))
    for dx in (-r, 0, r):
        for dy in (-r, 0, r):
            if dx or dy:
                cv2.putText(img, text, (org[0] + dx, org[1] + dy), cv2.FONT_HERSHEY_DUPLEX, scale, outline, thick, cv2.LINE_AA)
    cv2.putText(img, text, org, cv2.FONT_HERSHEY_DUPLEX, scale, color, thick, cv2.LINE_AA)


def _emoji(frame_no: int) -> np.ndarray:
    """A 2-frame looping 'GIF': a yellow face whose mouth opens / closes every 0.2 s, with a white sticker rim."""
    s = np.zeros((96, 96, 3), np.uint8)
    cv2.circle(s, (48, 48), 46, (255, 255, 255), -1)
    cv2.circle(s, (48, 48), 40, (40, 210, 250), -1)
    cv2.circle(s, (34, 38), 6, (30, 30, 30), -1)
    cv2.circle(s, (62, 38), 6, (30, 30, 30), -1)
    if (frame_no // 6) % 2:
        cv2.ellipse(s, (48, 64), (16, 12), 0, 0, 360, (30, 30, 160), -1)
    else:
        cv2.line(s, (32, 64), (64, 64), (30, 30, 30), 4)
    return s


def _paste(f, s, x, y):
    mask = s.sum(axis=2) > 0
    f[y:y + s.shape[0], x:x + s.shape[1]][mask] = s[mask]


@pytest.fixture(scope="module")
def packed(tmp_path_factory):
    d = tmp_path_factory.mktemp("pack")
    rng = np.random.default_rng(3)
    shot_a = np.clip(_photo_like(W + 120, H, 11).astype(np.int16) + 70, 0, 255).astype(np.uint8)  # light enough for a black outline
    shot_b = np.clip(_photo_like(W + 120, H, 12).astype(np.int16) + 70, 0, 255).astype(np.uint8)
    frames = []
    for i in range(6 * FPS):
        t = i / FPS
        src = shot_a if t < 3.0 else shot_b
        off = int(40 * (t % 3.0) / 3.0)  # slow pan: live-ish background, never still
        f = np.ascontiguousarray(src[:, off:off + W]).copy()
        f = np.clip(f.astype(np.int16) + rng.normal(0, 2, f.shape).astype(np.int16), 0, 255).astype(np.uint8)
        # subtitles: two lines in a fixed bottom lane, white with a black outline
        if 0.5 <= t < 2.0:
            _outlined(f, "HELLO WORLD", (70, 560), 0.9, (255, 255, 255), 2)
        elif 2.0 <= t < 3.5:
            _outlined(f, "SECOND LINE", (70, 560), 0.9, (255, 255, 255), 2)
        elif 3.5 <= t < 5.5:
            _outlined(f, "THIRD ONE", (90, 560), 0.9, (255, 255, 255), 2)
        # looping GIF sticker, appears and leaves mid-shot
        if 1.0 <= t < 2.4:
            _paste(f, _emoji(i), 230, 90)
        # 花字: big yellow word that pops in (scales up over 0.2 s)
        if 4.0 <= t < 5.2:
            k = min(1.0, 0.4 + 0.6 * (t - 4.0) / 0.2)
            _outlined(f, "WOW!", (int(120 - 30 * (k - 1)), 300), 2.2 * k, (0, 230, 255), 5)
        frames.append(f)
    path = _write(frames, d / "pack.mp4", fps=FPS)
    info = video_info(path)
    return P.analyze(path, info, cuts=[3.0], out_dir=d, ocr=True), d


def _ocr_ok():
    from rea_video.overlay import get_ocr
    return get_ocr() is not None


@pytest.mark.skipif(not _ocr_ok(), reason="rapidocr not installed")
def test_subtitle_timeline(packed):
    pack, _ = packed
    subs = [c for c in pack["text_cues"] if c["kind"] == "subtitle"]
    texts = [P._norm(c["text"]) for c in subs]
    assert any("helloworld" in t for t in texts) and any("secondline" in t for t in texts)
    hello = next(c for c in subs if "helloworld" in P._norm(c["text"]))
    assert abs(hello["t0"] - 0.5) <= 0.25 and abs(hello["t1"] - 2.0) <= 0.25
    st = hello["style"]
    assert st.get("fill_name") == "白" and st.get("stroke_name") == "黑"
    srt = P.to_srt(pack["text_cues"])
    assert "HELLOWORLD" in srt.upper().replace(" ", "") and "-->" in srt


@pytest.mark.skipif(not _ocr_ok(), reason="rapidocr not installed")
def test_huazi_pop(packed):
    pack, _ = packed
    wow = [c for c in pack["text_cues"] if "wow" in P._norm(c["text"])]
    assert wow, [c["text"] for c in pack["text_cues"]]
    c = wow[0]
    assert c["kind"] == "huazi", c
    assert c["style"].get("fill_name") == "黄"
    assert abs(c["t0"] - 4.0) <= 0.25


# without OCR the subtitle band is not recognized as text and shows up as a second "sticker"
@pytest.mark.skipif(not _ocr_ok(), reason="rapidocr not installed")
def test_gif_sticker(packed):
    pack, d = packed
    st = [s for s in pack["stickers"] if s["t0"] < 2.0 and s["t1"] > 1.2]
    assert st, pack["stickers"]
    s = st[0]
    assert s["kind"] == "animated_sticker" and s["looping"]
    assert abs(s["t0"] - 1.0) <= 0.2 and abs(s["t1"] - 2.4) <= 0.3
    x, y, w, h = s["bbox"]
    assert abs((x + w / 2) - (230 + 48) / W) < 0.08 and abs((y + h / 2) - (90 + 48) / H) < 0.06
    assert (d / s["image"]).exists()
    # nothing else is called a sticker: the subtitles and the 花字 are text, the pan is the picture
    assert len(pack["stickers"]) == 1, pack["stickers"]


def test_sfx_alignment():
    cues = [{"id": "text_001", "kind": "huazi", "kind_zh": "花字", "text": "WOW", "t0": 4.0, "t1": 5.0}]
    stickers = [{"id": "sticker_01", "kind_zh": "动态贴纸/GIF", "t0": 1.0, "t1": 2.4, "disappears_mid_shot": True}]
    ev = P.visual_events(cues, stickers, [3.0])
    sfx = [{"t": 4.05, "type": "pop"}, {"t": 1.02, "type": "pop"}, {"t": 3.01, "type": "whoosh"}, {"t": 0.3, "type": "ding"}]
    res = P.align_sfx(sfx, ev)
    assert sfx[0]["on"]["type"] == "huazi_in" and sfx[1]["on"]["type"] == "sticker_in" and sfx[2]["on"]["type"] == "cut"
    assert "on" not in sfx[3]
    assert res["events_with_sfx"]["huazi_in"] == {"with_sfx": 1, "total": 1}
    assert res["events_with_sfx"]["sticker_out"] == {"with_sfx": 0, "total": 1}


def _sub(i, t0, t1, text, lane=2):
    return {"id": f"text_{i:03d}", "kind": "subtitle", "kind_zh": "字幕", "text": text, "t0": t0, "t1": t1, "lane": lane}


def test_speech_anchors_and_persistent_layers():
    lines = [_sub(1, 0.0, 1.8, "这俩口红有啥区别"), _sub(2, 1.8, 3.8, "现在双11全场五折"), _sub(3, 4.0, 5.5, "给你安排上"),
             _sub(4, 6.0, 7.0, "错过就没有了")]
    filing = [_sub(10 + k, t, t + 1.5, "粤G妆网备字2026", lane=6) for k, t in enumerate((0.0, 3.0, 6.0))]  # one text repeated
    cues = lines + filing + [
        {"id": "text_020", "kind": "huazi", "kind_zh": "花字", "text": "五折", "t0": 3.2, "t1": 3.6},       # repeats a word of line 2
        {"id": "text_021", "kind": "huazi", "kind_zh": "花字", "text": "冲！", "t0": 5.7, "t1": 6.2},        # just after line 3
        {"id": "text_022", "kind": "label", "kind_zh": "文字标注", "text": "8uXrH", "t0": 2.0, "t1": 2.3},   # picture text: no shared word
        {"id": "text_023", "kind": "label", "kind_zh": "文字标注", "text": "使用效果因人而异", "t0": 0.0, "t1": 7.0},  # disclaimer across cuts
        {"id": "text_024", "kind": "label", "kind_zh": "文字标注", "text": "Q8xZ", "t0": 1.0, "t1": 6.5}]       # noise seen once
    stickers = [{"id": "sticker_01", "kind": "static_sticker", "kind_zh": "静态贴纸", "t0": 4.1, "t1": 4.9, "confidence": "medium"}]
    cuts = [2.0, 4.0, 6.0]
    assert [c["id"] for c in P.speech_lines(cues)] == ["text_001", "text_002", "text_003", "text_004"]
    P.anchor_layers(cues, stickers, cuts)
    by = {c["id"]: c for c in cues}
    assert by["text_020"]["anchor"]["line"] == "text_002" and by["text_020"]["anchor"]["word"] == "五折"
    assert by["text_021"]["anchor"] == {"line": "text_003", "text": "给你安排上", "rel": "after", "dt": 0.2, "word": None}
    assert stickers[0]["anchor"]["line"] == "text_003" and stickers[0]["anchor"]["rel"] == "during"
    assert "anchor" not in by["text_022"] and "anchor" not in by["text_023"]
    assert by["text_023"]["persistent"] == {"cuts": 3} and "persistent" not in by["text_024"]
    lines_out = P.summary_lines({"text_cues": [c for c in cues if c["kind"] != "subtitle"], "stickers": stickers})
    assert any("按台词定位 3 处" in l for l in lines_out)
    assert any(l.startswith("常驻图层 1 个") and "使用效果因人而异" in l for l in lines_out)
    P.anchor_layers(cues, [], [])  # a re-run drops stale marks
    assert not any(c.get("persistent") for c in cues)


def test_overlays_at_skips_picture_text():
    pack = {"text_cues": [{"kind": "subtitle", "kind_zh": "字幕", "t0": 0.0, "t1": 2.0},
                          {"kind": "label", "kind_zh": "文字标注", "t0": 0.0, "t1": 2.0, "part_of_picture": True}],
            "stickers": [{"t0": 1.0, "t1": 3.0, "confidence": "low"}]}
    assert P.overlays_at(pack, 0.0, 0.15) == ["字幕"]
    assert P.overlays_at(pack, 2.5, 2.6) == [] and P.overlays_at(None, 0, 1) == []


def test_ass_export():
    cues = [{"kind": "subtitle", "text": "a/b", "t0": 1.0, "t1": 2.5, "bbox": [0.2, 0.8, 0.6, 0.08], "line_h": 0.035, "angle": 0.0,
             "style": {"fill": "#ffffff", "stroke": "#000000", "stroke_ratio": 0.05}, "anim_in": {"kind": "pop"}},
            {"kind": "scene", "text": "x", "t0": 0, "t1": 1, "bbox": [0, 0, 0.1, 0.1], "line_h": 0.02, "angle": 0.0, "style": {}}]
    ass = P.to_ass(cues, 1080, 1920)
    assert "Dialogue: 0,0:00:01.00,0:00:02.50" in ass and "a\\Nb" in ass and "\\fscx60" in ass
    assert ass.count("Dialogue:") == 1  # scene text is not exported
    side = [{"kind": "label", "text": "效果因人而异", "t0": 0, "t1": 3, "bbox": [0.01, 0.8, 0.026, 0.08], "line_h": 0.08, "angle": 0.0, "style": {}},
            {"kind": "huazi", "text": "双十一福利五折", "t0": 0, "t1": 3, "bbox": [0.3, 0.5, 0.4, 0.05], "line_h": 0.08, "angle": 0.0, "style": {}}]
    ass = P.to_ass(side, 720, 1280)
    assert "效\\N果\\N因" in ass  # a narrow tall box is vertical text
    sizes = [int(l.split(",")[2]) for l in ass.splitlines() if l.startswith("Style:")]
    assert sizes[0] <= 19 and sizes[1] * 7 <= 0.4 * 720 * 1.06  # each fits its measured box


def test_clean_region():
    st = [{"bbox": [0.6, 0.1, 0.3, 0.15], "t0": 1.0, "t1": 3.0, "confidence": "medium", "appears_mid_shot": True}]
    x, y, w, h = P.clean_region(st, 1.0, 3.0)
    assert w * h >= 0.45 and (x + w <= 0.6 + 1e-6 or y >= 0.25 - 1e-6)  # the band avoids the sticker
    assert P.clean_region(st, 5.0, 8.0) is None                                 # not on this shot
    assert P.clean_region([dict(st[0], confidence="low")], 1.0, 3.0) is None    # unconfirmed: leave the shot alone
    # only survived a cut (no pop-in, no loop): may be content both shots share, keep the full frame
    cut_only = dict(st[0], appears_mid_shot=False, crosses_cut=True, looping=False)
    assert P.clean_region([cut_only], 1.0, 3.0) is None
    assert P.clean_region([dict(cut_only, looping=True)], 1.0, 3.0) is not None  # a looping GIF is a pasted layer


def test_review_overrides_stickers_and_kinds():
    pack = {"text_cues": [{"id": "text_001", "kind": "label", "kind_zh": "文字标注", "text": "WOW", "t0": 1, "t1": 2}],
            "stickers": [{"id": "sticker_01", "kind": "static_sticker", "kind_zh": "静态贴纸/图片", "t0": 1, "t1": 2,
                          "bbox": [0.1, 0.1, 0.2, 0.2], "confidence": "low"},
                         {"id": "sticker_02", "kind": "animated_sticker", "kind_zh": "动态贴纸/GIF", "t0": 3, "t1": 4,
                          "bbox": [0.5, 0.5, 0.2, 0.2], "confidence": "low"}],
            "review": {"by": "claude", "text": {"text_001": "huazi"},
                       "stickers": {"sticker_01": {"is_overlay": False, "what": ""}, "sticker_02": {"is_overlay": True, "what": "猫猫表情包"}},
                       "missed": [{"t0": 6, "t1": 7, "what": "GIF 动图", "where": "右下"}]}}
    P.apply_review(pack)
    assert pack["text_cues"][0]["kind"] == "huazi"
    s1, s2, s3 = pack["stickers"]
    assert s1["in_picture"] and s2["confidence"] == "confirmed" and s2["what"] == "猫猫表情包"
    assert s3["source"] == "agent" and s3["kind"] == "animated_sticker"
    rec = {"start": 0.0, "end": 8.0}
    kinds = [l["kind"] for l in P.shot_layers(pack, rec, "cg_3d")]
    # confirmed stickers stay even on a 3D picture; the rejected one is gone
    assert kinds.count("animated_sticker") == 2 and "static_sticker" not in kinds and "huazi" in kinds


def test_pipeline_writes_packaging(tmp_path, media):
    from rea_video.pipeline import decompose

    b = decompose(media["edit"], tmp_path / "edit", use_vlm=False, ocr=False, stems=False, memory=False)
    pk = b["packaging"]
    assert pk["version"] >= 1 and (tmp_path / "edit" / pk["files"]["timeline"]).is_file()
    # the code-render card sliding in is the picture's own content, not a sticker
    assert not [s for s in pk["stickers"] if not s.get("in_picture")]
    md = (tmp_path / "edit" / "report.md").read_text(encoding="utf-8")
    assert "剪辑包装层" in md


def test_numbered_labels_split_per_shot():
    """SHOT 01 … SHOT 03 at one place: three labels (not one cue spanning the video), and not a subtitle lane."""
    from rea_video.packaging import build_cues, classify_cues

    items = []
    for k in range(30):
        t = k * 0.5
        n = 1 + int(t // 5)
        text = f"SHOT 0{n}" if k != 4 else "SHOT 07"  # one frame misread stays inside its run
        items.append({"t": t, "text": text, "conf": 0.95, "bbox": [0.4, 0.48, 0.2, 0.03], "angle": 0.0, "style": None})
    cues = build_cues(items, 0.5)
    assert [c["text"] for c in cues] == ["SHOT 01", "SHOT 02", "SHOT 03"]
    assert cues[1]["t0"] == 5.0
    for c in cues:
        c.update(style={}, t1=c["t1"])
    classify_cues(cues, 15.0)
    assert all(c["kind"] == "label" for c in cues)


def test_page_text_in_a_screenshot_is_not_a_subtitle():
    """Words of a page at one height (tabs, a file list) change like a subtitle track but sit among other lines of
    the same size and are scattered left to right; the caption band under the screenshot stays a subtitle."""
    from rea_video.packaging import classify_cues

    def cue(i, t0, t1, x, y, w, text, h=0.025):
        return {"id": f"t{i}", "t0": t0, "t1": t1, "bbox": [x, y, w, h], "line_h": h, "angle": 0.0, "drift": 0.0,
                "samples": 3, "text": text, "style": {}}

    cues, i = [], 0
    captions = ["这条才发二十一分钟", "就被判九成扑街", "封面顺序反了", "带钩子那张埋在第三张", "先别删拿它查查"]
    words = ["docs", "Code", "main", "Pull requests", "README"]
    for k in range(5):
        t0, t1 = 2.0 * k, 2.0 * k + 1.6
        cues.append(cue(i := i + 1, t0, t1, 0.5 - 0.04 * len(captions[k]) / 2, 0.875, 0.04 * len(captions[k]), captions[k], 0.033))
        # one page word on the lane at y≈0.40, at a different place each time, with the page's other lines around it
        cues.append(cue(i := i + 1, t0, t1, [0.1, 0.9, 0.1, 0.6, 0.3][k], 0.39, 0.08, words[k]))
        for j, dy in enumerate((-0.06, -0.03, 0.03, 0.06)):
            cues.append(cue(i := i + 1, t0, t1, 0.05, 0.39 + dy, 0.5, f"2 weeks ago {k}{j}"))
    classify_cues(cues, 10.0)
    kinds = {c["text"]: c["kind"] for c in cues}
    assert all(kinds[t] == "subtitle" for t in captions)
    assert all(kinds[t] == "scene" for t in words)


def test_counter_ticking_every_frame_stays_one_cue():
    from rea_video.packaging import build_cues

    items = [{"t": k * 0.5, "text": f"第{k}名", "conf": 0.9, "bbox": [0.4, 0.1, 0.2, 0.03], "angle": 0.0, "style": None}
             for k in range(10)]
    assert len(build_cues(items, 0.5)) == 1


def test_low_confidence_sfx_are_counted_as_possible():
    from rea_video.packaging import align_sfx

    events = [{"t": 1.0, "type": "text_in", "what": "A", "ref": "text_001"}, {"t": 2.0, "type": "text_in", "what": "B", "ref": "text_002"}]
    al = align_sfx([{"t": 1.02, "source": "vlm"}, {"t": 2.01, "source": "deterministic_anchored", "confidence": "low"}], events)
    assert al["sfx_on"] == {"text_in": 1} and al["sfx_on_possible"] == {"text_in": 1}
