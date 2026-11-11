import re

from rea_video.i18n import LangDict, T, join, set_lang
from rea_video.classify import LABEL_ZH


def test_T_and_langdict_follow_language():
    try:
        set_lang("zh")
        assert T("实拍", "live action") == "实拍"
        assert LABEL_ZH["ai_video"] == "AI 生成视频"
        assert join(["a", "b"]) == "a、b"
        set_lang("en")
        assert T("实拍", "live action") == "live action"
        assert T("{n} 个镜头", "{n} shots", n=3) == "3 shots"
        assert T("只有中文") == "只有中文"  # no English yet: falls back
        assert LABEL_ZH["ai_video"] == "AI-generated video"
        assert dict(LABEL_ZH.items())["cg_3d"] == "3D render"
        assert join(["a", "b"]) == "a, b"
        d = LangDict({"x": "甲"}, en={})
        assert d["x"] == "甲" and "x" in d and len(d) == 1
    finally:
        set_lang("zh")


def test_unknown_language_rejected():
    import pytest

    with pytest.raises(ValueError):
        set_lang("fr")


def test_image_labels_follow_language():
    from rea_video.visual import LABEL_SHORT

    try:
        set_lang("en")
        assert LABEL_SHORT["code_render"] == "Code render"
        assert not any(re.search(r"[㐀-鿿]", v) for v in LABEL_SHORT.values())
        set_lang("zh")
        assert LABEL_SHORT["code_render"] == "代码渲染"
    finally:
        set_lang("zh")


def test_summary_without_tempo_prints_no_bpm(tmp_path, capsys):
    import json

    from rea_video.cli import main

    b = {"lang": "en", "source": {"filename": "x.mp4", "duration": 1.0, "width": 16, "height": 16, "fps": 1.0},
         "summary": {"verdict": "x", "confidence": 1.0, "vlm": "none"}, "shots": [],
         "audio": {"has_audio": True, "voice": {"present": True, "ratio": 0.8}, "music": {"present": False, "ratio": 0.0, "segments": []}}}
    p = tmp_path / "breakdown.json"
    p.write_text(json.dumps(b), encoding="utf-8")
    try:
        assert main(["summary", str(p)]) == 0
    finally:
        set_lang("zh")
    assert "NoneBPM" not in capsys.readouterr().out
