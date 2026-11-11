"""The scorer behind every published number: label lookup, cut matching, and what it does with missing or stale inputs."""
import yaml

from rea_video import evaluate as E
from rea_video.classify import LABELS


def test_label_lookup_by_time():
    entry = {"segments": [[0, 2, "ai_video"], [2, 5, ["live_action", "film_footage"]]]}
    assert E.gt_at(entry, 1.0) == {"ai_video"} and E.gt_at(entry, 2.0) == {"live_action", "film_footage"}
    assert E.gt_at(entry, 5.0) is None and E.gt_at({"audio": {}}, 1.0) is None
    assert E.gt_at({"label": "cg_3d"}, 9.0) == {"cg_3d"}


def test_real_material_lookup():
    assert E.real_at({}, 1.0) is None and E.real_at({"real_material": True}, 1.0) is True
    assert E.real_at({"real_material": [[0, 2, True], [2, 4, False]]}, 3.0) is False
    assert E.real_at({"real_material": [[0, 2, True]]}, 3.0) is None


def test_cut_matching_counts_each_true_cut_once_and_takes_the_nearest():
    r = E.boundary_f1([1.0, 2.0, 2.05, 7.0], [1.02, 2.04, 5.0], tol=0.1)
    assert (r["tp"], r["fp"], r["fn"]) == (2, 2, 1) and r["precision"] == 0.5 and r["recall"] == 0.667
    # two true cuts inside the tolerance of one prediction: it takes the nearer, leaving the other for the next
    assert E.boundary_f1([1.08, 1.0], [1.0, 1.09], tol=0.1)["tp"] == 2
    assert E.boundary_f1([3.0], [], ignore=[3.02])["fp"] == 0
    assert E.boundary_f1([], [])["f1"] == 1.0


def test_missing_files_are_reported_and_stale_breakdowns_are_decoded_again(media, tmp_path, monkeypatch):
    labels = tmp_path / "labels.yaml"
    labels.write_text(yaml.safe_dump({"videos": [{"id": "here", "path": str(media["edit"]), "label": list(LABELS)},
                                                 {"id": "gone", "path": str(tmp_path / "gone.mp4"), "label": "ai_video"}]}), encoding="utf-8")
    out = tmp_path / "out"
    s = E.evaluate(labels, out, ocr=False)["summary"]
    assert s["videos"] == 1 and s["videos_listed"] == 2 and s["missing"] == ["gone"] and s["duration_weighted_accuracy"] == 1.0

    calls = []
    real = E.decompose
    monkeypatch.setattr(E, "decompose", lambda *a, **k: calls.append(1) or real(*a, **k))
    E.evaluate(labels, out, ocr=False)
    assert calls == []  # same measuring code: the stored breakdown is reused
    monkeypatch.setattr(E, "decode_fingerprint", lambda: "changed")
    E.evaluate(labels, out, ocr=False)
    assert calls == [1]
