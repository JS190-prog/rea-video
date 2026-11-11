"""Local speech recognition: optional, checksummed model, sentence timing, and where the transcript is used."""
import hashlib
import io
import json
import tarfile

import pytest

from rea_video import speech
from rea_video.entities import script


def test_long_stretch_is_split_into_sentences_with_estimated_times():
    rows = speech._sentences(10.0, 20.0, "今天教大家做视频。先保存图片！然后打开工具")
    assert [r["text"] for r in rows] == ["今天教大家做视频。", "先保存图片！", "然后打开工具"]
    assert rows[0]["start"] == 10.0 and rows[-1]["end"] == 20.0 and all(r["timing"] == "estimated" for r in rows)
    assert all(a["end"] == b["start"] for a, b in zip(rows, rows[1:]))
    assert speech._sentences(1.0, 4.0, "短句。也短。") == [{"start": 1.0, "end": 4.0, "text": "短句。也短。"}]


def test_transcribe_without_the_extra_says_so(monkeypatch, tmp_path):
    monkeypatch.setattr(speech, "available", lambda: False)
    assert speech.transcribe(tmp_path / "x.wav") == {"ok": False, "reason": "not_installed"}


def _archive(files: dict) -> bytes:
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w:bz2") as tar:
        for name, data in files.items():
            info = tarfile.TarInfo(name)
            info.size = len(data)
            tar.addfile(info, io.BytesIO(data))
    return buf.getvalue()


def test_models_are_checked_and_only_the_needed_files_are_unpacked(monkeypatch, tmp_path):
    monkeypatch.setenv("REA_VIDEO_MODELS", str(tmp_path))
    arc = _archive({f"{speech.MODEL_DIR}/model.int8.onnx": b"model", f"{speech.MODEL_DIR}/tokens.txt": b"tok",
                    f"{speech.MODEL_DIR}/test_wavs/zh.wav": b"wav", "../escape.txt": b"x"})
    served = {speech.VAD_NAME: b"vad", f"{speech.MODEL_DIR}.tar.bz2": arc}
    monkeypatch.setattr(speech, "fetch", lambda url, dst, timeout=60: open(dst, "wb").write(served[url.rsplit("/", 1)[-1]]))
    monkeypatch.setattr(speech, "VAD_SHA256", hashlib.sha256(b"vad").hexdigest())
    with pytest.raises(OSError):  # the archive does not match the pinned checksum
        speech.ensure_models()
    assert sorted(p.name for p in tmp_path.iterdir()) == [speech.VAD_NAME]
    monkeypatch.setattr(speech, "ARCHIVE_SHA256", hashlib.sha256(arc).hexdigest())
    model, tokens, vad = speech.ensure_models()
    assert model.read_bytes() == b"model" and tokens.read_bytes() == b"tok" and vad.read_bytes() == b"vad"
    assert sorted(p.name for p in model.parent.iterdir()) == ["model.int8.onnx", "tokens.txt"]
    assert sorted(p.name for p in tmp_path.iterdir()) == sorted([speech.MODEL_DIR, speech.VAD_NAME]) and not (tmp_path.parent / "escape.txt").exists()
    monkeypatch.setattr(speech, "fetch", lambda *a, **k: pytest.fail("should not download again"))
    speech.ensure_models()


def test_script_uses_the_transcript_below_the_vlm_and_above_segment_copy():
    heard = {"ok": True, "lines": [{"start": 0.1, "end": 2.0, "text": "大家好"}]}
    b = {"speech": heard, "whole_video_vlm": {"segments": [{"start": 0, "end": 2, "copy": "分段文案"}]}}
    assert script(b) == [{"start": 0.1, "end": 2.0, "speaker": "", "text": "大家好", "source": "asr"}]
    b["whole_video_vlm"]["narration"] = {"lines": [{"start": 0, "end": 2, "speaker": "A", "text": "模型听到的"}]}
    assert script(b)[0]["text"] == "模型听到的"
    json.dumps(script(b))
