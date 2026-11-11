"""Edge cases from the 2026-11 review: low fps, damaged files, malformed VLM answers, engine, exports."""
import subprocess
from pathlib import Path

import pytest

from rea_video.media import extract_frame, video_info
from rea_video.packaging import _ts
from rea_video.probe import _scan_bytes, provenance
from rea_video.review import _tiles_cmd
from rea_video.vlm import VLMClient, VLMConfig, normalize_shot_result, normalize_whole


def _ff(*args):
    subprocess.run(["ffmpeg", "-v", "error", "-y", *args], check=True)


@pytest.fixture(scope="module")
def fps10(tmp_path_factory) -> Path:
    p = tmp_path_factory.mktemp("v") / "fps10.mp4"
    _ff("-f", "lavfi", "-i", "testsrc2=size=160x120:rate=10", "-t", "2", "-pix_fmt", "yuv420p", str(p))
    return p


def test_last_frame_past_final_pts_falls_back(fps10, tmp_path):
    # 10 fps: end - 0.08 s lies after the last frame's timestamp; used to abort decompose
    out = extract_frame(fps10, 1.95, tmp_path / "last.jpg", width=160)
    assert out.is_file() and out.stat().st_size > 0


def test_byte_scan_skips_mdat(tmp_path):
    p = tmp_path / "x.mp4"
    _ff("-f", "lavfi", "-i", "testsrc2=size=64x64:rate=5", "-t", "1", str(p))
    raw = p.read_bytes()
    i = raw.index(b"mdat") + 8
    p.write_bytes(raw[:i] + b"xxx Veo xxx" + raw[i + 11:])  # random-looking "veo" inside the frame data
    assert b"Veo" not in _scan_bytes(p)
    assert not provenance(video_info(p)).get("hints", {}).get("generator")


def test_normalize_whole_survives_bad_shapes():
    w = normalize_whole({"narration": "none", "music": ["x"], "sfx": [{"t": "00:03"}, {"t": None}, "pop"],
                         "segments": [{"start": "1:02.5", "end": "bad"}], "summary": 3})
    assert "narration" not in w and "music" not in w
    assert w["sfx"] == [{"t": 3.0}, {}]
    assert w["segments"] == [{"start": 62.5}]
    assert w["summary"] == "3"
    assert normalize_whole("oops") is None


def test_merge_audio_with_bad_whole_answer():
    from rea_video.audio import merge_audio_with_vlm

    w = normalize_whole({"narration": "none", "sfx": [{"t": "00:03"}, {"t": None}]})
    merge_audio_with_vlm({"has_audio": True, "sfx": {"events": [{"t": 3.1}]}}, w)


def test_normalize_shot_result_bad_types():
    r = normalize_shot_result({"label_probs": [0.5, 0.5], "evidence": "skin texture"})
    assert r["evidence"] == ["skin texture"] and not any(r["label_probs"].values())  # unusable probs = "no opinion"


def test_empty_choices_falls_back_to_next_model(monkeypatch):
    c = VLMClient(VLMConfig("https://example.invalid/v1", "k", ["m1", "m2"]))
    calls = []

    def fake_urlopen(req, timeout):
        import io
        import json

        model = json.loads(req.data)["model"]
        calls.append(model)
        body = {"choices": []} if model == "m1" else {"choices": [{"message": {"content": '{"ok": 1}'}}]}

        class R(io.BytesIO):
            def __enter__(self):
                return self

            def __exit__(self, *a):
                return False

        return R(json.dumps(body).encode())

    monkeypatch.setattr("rea_video.vlm.urllib.request.urlopen", fake_urlopen)
    monkeypatch.setattr("rea_video.vlm.time.sleep", lambda s: None)
    assert c.ask_json("p", [])["ok"] == 1
    assert calls[-1] == "m2"


def test_srt_timestamp_carries_into_seconds():
    assert _ts(3.9996) == "00:00:04,000"
    assert _ts(59.9997) == "00:01:00,000"
    assert _ts(1.5, ".") == "00:00:01.500"


def test_tiles_cmd_quotes_paths():
    assert "'/a/my video.mp4'" in _tiles_cmd("/a/my video.mp4", 1, 2, 0.2, "out/c.jpg")


def test_relocalize_rewrites_stored_labels():
    from rea_video.i18n import set_lang
    from rea_video.packaging import relocalize

    pack = {"text_cues": [{"kind": "subtitle", "kind_zh": "字幕", "line_h": 0.05,
                           "style": {"fill_name": "白", "stroke": True, "stroke_name": "黑"}, "style_zh": "白字、黑描边",
                           "anim_in": {"kind": "pop", "kind_zh": "缩放弹出"}}],
            "stickers": [{"kind": "static_sticker", "kind_zh": "静态贴纸/图片", "source": "pixels"},
                         {"kind": "static_sticker", "kind_zh": "一只猫的贴纸", "source": "vlm"}]}
    try:
        set_lang("en")
        relocalize(pack, 1920)
    finally:
        set_lang("zh")
    c = pack["text_cues"][0]
    assert c["kind_zh"] == "subtitle" and c["anim_in"]["kind_zh"] == "scale pop"
    assert c["style"]["fill_name"] == "white" and "black outline" in c["style_zh"] and "line height" in c["style_zh"]
    assert pack["stickers"][0]["kind_zh"] == "static sticker / image"
    assert pack["stickers"][1]["kind_zh"] == "一只猫的贴纸"  # free text from the VLM is kept


def test_variable_frame_rate_cuts_use_real_timestamps(tmp_path):
    """30 fps + 10 fps + 30 fps segments, 2 s each: cuts at 2 s and 4 s, not at frame / average-fps."""
    from rea_video.shots import build_track, detect_shots

    srcs = ["testsrc2=s=160x120:r=30:d=2", "mandelbrot=s=160x120:r=10", "testsrc2=s=160x120:r=30:d=2"]
    for k, src in enumerate(srcs):
        vf = ["-vf", "hue=h=180,vflip"] if k == 2 else []
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", src, "-t", "2", *vf, "-c:v", "libx264",
                        "-pix_fmt", "yuv420p", "-video_track_timescale", "90000", str(tmp_path / f"{k}.mp4")], check=True)
    (tmp_path / "list.txt").write_text("".join(f"file {k}.mp4\n" for k in range(3)))
    vfr = tmp_path / "vfr.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-i", str(tmp_path / "list.txt"), "-c", "copy", str(vfr)], check=True)
    shots = detect_shots(build_track(str(vfr), video_info(vfr)))
    assert [round(s.start, 2) for s in shots] == [0.0, 2.0, 4.0]
    assert abs(shots[-1].end - 6.0) < 0.05


def _tagged(tmp_path, **tags) -> Path:
    p = tmp_path / "t.mp4"
    meta = [x for k, v in tags.items() for x in ("-metadata", f"{k}={v}")]
    _ff("-f", "lavfi", "-i", "testsrc2=size=64x64:rate=5", "-t", "1", *meta, str(p))
    return p


def test_generator_named_in_typed_text_is_not_a_signature(tmp_path):
    p = _tagged(tmp_path, title="pikachu on the runway", description="Each individual clip compared with OpenAI Sora", comment="unresolved")
    prov = provenance(video_info(p))
    assert not prov["hints"].get("generator") and "DaVinci Resolve" not in prov["hints"].get("editor", [])
    assert any(e["kind"] == "generator_text" for e in prov["evidence"])


def test_generator_named_by_the_encoder_is_a_signature(tmp_path):
    p = tmp_path / "t.mp4"
    _ff("-f", "lavfi", "-i", "testsrc2=size=64x64:rate=5", "-t", "1", "-metadata:s:v", "handler_name=KlingAI video", str(p))
    assert "Kling" in provenance(video_info(p))["hints"].get("generator", [])


def test_shot_decode_starts_on_the_shot_first_frame(tmp_path):
    import numpy as np

    from rea_video.media import iter_frames

    p = tmp_path / "ramp.mp4"  # every frame is a flat grey of its own level, so the level read back names the frame
    _ff("-f", "lavfi", "-i", "color=black:size=64x64:rate=30000/1001,geq=lum='16+4*N':cb=128:cr=128", "-t", "2", "-pix_fmt", "yuv420p", str(p))
    info = video_info(p)
    level = [round(float(np.mean(f))) for f in iter_frames(p, info, width=64, gray=True)]
    assert len(set(level[:50])) == 50
    for k in range(1, 50):  # a third of these start times round to just past the frame's timestamp
        first = next(iter_frames(p, info, width=64, start=k / info.fps, duration=0.2, gray=True))
        assert level.index(round(float(np.mean(first)))) == k, k


def test_normalize_shot_result_coerces_text_fields():
    r = normalize_shot_result({"label_probs": {"ai_video": 1}, "description": ["a cat", "jumps"], "style": None, "embedded_assets": "logo",
                               "ai_edits": [{"kind": "face_swap"}, "x"], "overlay_text": "SALE", "replication": {"video_prompt": ["a", "b"]},
                               "aspects": "n/a"})
    assert isinstance(r["description"], str) and "a cat" in r["description"] and r["style"] == ""
    assert r["embedded_assets"] == [] and r["ai_edits"] == [{"kind": "face_swap"}] and r["overlay_text"] == ["SALE"]
    assert isinstance(r["replication"]["video_prompt"], str) and "aspects" not in r


def _http_error(code, body=b'{"error": "video input is not supported"}', headers=None):
    import io
    import urllib.error

    return urllib.error.HTTPError("https://example.invalid/v1", code, "err", headers or {}, io.BytesIO(body))


def test_rejected_request_is_not_retried_and_does_not_stop_the_vlm(monkeypatch):
    c = VLMClient(VLMConfig("https://example.invalid/v1", "k", ["m1"]))
    calls = []

    def fake_urlopen(req, timeout):
        calls.append(1)
        raise _http_error(400)

    monkeypatch.setattr("rea_video.vlm.urllib.request.urlopen", fake_urlopen)
    monkeypatch.setattr("rea_video.vlm.time.sleep", lambda s: None)
    for _ in range(3):
        with pytest.raises(RuntimeError, match="not supported"):
            c.ask_json("p", [])
    assert len(calls) == 3 and not c.gave_up


def test_server_errors_still_stop_the_vlm(monkeypatch):
    c = VLMClient(VLMConfig("https://example.invalid/v1", "k", ["m1"]))
    monkeypatch.setattr("rea_video.vlm.urllib.request.urlopen", lambda req, timeout: (_ for _ in ()).throw(_http_error(503)))
    monkeypatch.setattr("rea_video.vlm.time.sleep", lambda s: None)
    for _ in range(2):
        with pytest.raises(RuntimeError):
            c.ask_json("p", [])
    assert c.gave_up


def test_truncated_cache_file_is_asked_again(tmp_path, monkeypatch):
    import io
    import json

    c = VLMClient(VLMConfig("https://example.invalid/v1", "k", ["m1"]), tmp_path)

    class R(io.BytesIO):
        def __enter__(self):
            return self

        def __exit__(self, *a):
            return False

    monkeypatch.setattr("rea_video.vlm.urllib.request.urlopen",
                        lambda req, timeout: R(json.dumps({"choices": [{"message": {"content": '{"ok": 1}'}}]}).encode()))
    assert c.ask_json("p", [])["ok"] == 1
    (cached,) = tmp_path.glob("*.json")
    cached.write_text('{"ok": ', encoding="utf-8")
    assert c.ask_json("p", [])["ok"] == 1
    assert json.loads(cached.read_text(encoding="utf-8"))["ok"] == 1 and not list(tmp_path.glob("*.part"))


def test_failed_clip_is_one_line_not_a_traceback(tmp_path):
    from rea_video.media import MediaError, cut_clip

    with pytest.raises(MediaError):
        cut_clip(tmp_path / "missing.mp4", 0, 1, tmp_path / "c.mp4")


def test_vlm_note_says_when_shots_were_left_out():
    from rea_video.i18n import set_lang
    from rea_video.vlm import vlm_note

    set_lang("zh")
    assert "60/200" in vlm_note({"status": "ok", "model": "m", "asked_shots": 60, "total_shots": 200})
    assert "/" not in vlm_note({"status": "ok", "model": "m", "asked_shots": 5, "total_shots": 5})
