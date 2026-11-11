import subprocess
import wave

import numpy as np
import pytest

from rea_video.audio import analyze_audio

SR = 22050


def _write_av(tmp_path, y: np.ndarray, name: str):
    wav = tmp_path / f"{name}.wav"
    with wave.open(str(wav), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((np.clip(y, -1, 1) * 32767).astype(np.int16).tobytes())
    mp4 = tmp_path / f"{name}.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", f"color=c=gray:s=160x90:d={len(y) / SR:.2f}",
                    "-i", str(wav), "-shortest", "-c:v", "libx264", "-c:a", "aac", str(mp4)], check=True)
    return mp4


def _music(dur=12.0, bpm=120.0):
    t = np.arange(int(dur * SR)) / SR
    y = 0.08 * sum(np.sin(2 * np.pi * f * t) for f in (261.63, 329.63, 392.0, 523.25))  # C major chord bed
    rng = np.random.default_rng(0)
    for k in np.arange(0, dur, 60 / bpm):  # kick + hat on every beat
        i = int(k * SR)
        n = int(0.08 * SR)
        env = np.exp(-np.arange(n) / (0.015 * SR))
        y[i:i + n] += 0.5 * env * np.sin(2 * np.pi * 70 * np.arange(n) / SR)
        y[i:i + n // 3] += 0.15 * rng.normal(size=n // 3) * env[: n // 3]
    return y


@pytest.fixture(scope="module")
def music_mp4(tmp_path_factory):
    return _write_av(tmp_path_factory.mktemp("a"), _music(), "music")


def test_music_tempo_key(music_mp4):
    a = analyze_audio(str(music_mp4))
    m = a["music"]
    assert m["present"] and not a["voice"]["present"]
    cands = [m["tempo_bpm"]] + m["tempo_alternatives"]
    assert any(abs(c - 120) < 4 for c in cands), cands
    assert m["key"]["tonic"] == "C" and m["key"]["mode"] == "major"


def test_cut_on_beat(music_mp4):
    cuts = [2.0, 4.0, 6.0, 8.0, 10.0]  # on the 120 BPM grid
    a = analyze_audio(str(music_mp4), cut_times=cuts)
    assert a["cuts_on_beat_ratio"] >= 0.8 and a["beat_synced_edit"]


def test_isolated_sfx_in_silence(tmp_path):
    y = np.zeros(int(6 * SR))
    for t0 in (1.0, 2.5, 4.0):  # three "dings" in an otherwise quiet track
        n = int(0.3 * SR)
        tt = np.arange(n) / SR
        y[int(t0 * SR):int(t0 * SR) + n] += 0.6 * np.exp(-tt / 0.08) * np.sin(2 * np.pi * 1800 * tt)
    y += 0.002 * np.random.default_rng(1).normal(size=len(y))
    a = analyze_audio(str(_write_av(tmp_path, y, "sfx")))
    ts = [e["t"] for e in a["sfx"]["events"]]
    assert all(any(abs(t - t0) < 0.08 for t in ts) for t0 in (1.0, 2.5, 4.0)), ts
    assert not a["music"]["present"]


def test_held_tone_has_no_beat_or_sfx(tmp_path):
    """A pure 440 Hz tone is a music-like bed with nothing percussive: no tempo, no sound effects."""
    t = np.arange(int(12 * SR)) / SR
    r = analyze_audio(str(_write_av(tmp_path, 0.3 * np.sin(2 * np.pi * 440 * t), "tone")))
    assert r["music"].get("tempo_bpm") is None and not r["music"]["present"]
    assert abs(r["music"]["steady_tone"]["hz"] - 440) < 25
    assert r["sfx"]["count"] == 0


def test_held_chord_is_still_music(tmp_path):
    """A sustained pad (several notes, no drums) is music, not a test tone."""
    t = np.arange(int(12 * SR)) / SR
    y = 0.08 * sum(np.sin(2 * np.pi * f * t) for f in (261.63, 329.63, 392.0, 523.25))
    r = analyze_audio(str(_write_av(tmp_path, y, "pad")))
    assert r["music"]["present"] and not r["music"].get("steady_tone")


@pytest.mark.parametrize("name", ["hum50", "hum100_peak", "square", "tone_in_hiss"])
def test_held_tones_beyond_a_clean_sine_are_not_music(tmp_path, name):
    """Mains hum (with harmonics, sometimes peaking at 100 Hz), a square-wave buzzer, and a tone under hiss
    are each one held pitch: not music and no tempo."""
    t = np.arange(int(12 * SR)) / SR
    rng = np.random.default_rng(0)
    y, hz = {
        "hum50": (sum(0.2 * 0.6 ** k * np.sin(2 * np.pi * 50 * (k + 1) * t) for k in range(5)), 50),
        "hum100_peak": (0.05 * np.sin(2 * np.pi * 50 * t) + 0.2 * np.sin(2 * np.pi * 100 * t)
                        + 0.1 * np.sin(2 * np.pi * 150 * t) + 0.01 * rng.normal(size=len(t)), 50),
        "square": (0.2 * np.sign(np.sin(2 * np.pi * 440 * t)), 440),
        "tone_in_hiss": (0.3 * np.sin(2 * np.pi * 440 * t) + 0.03 * rng.normal(size=len(t)), 440),
    }[name]
    r = analyze_audio(str(_write_av(tmp_path, y, name)))
    assert not r["music"]["present"] and r["music"].get("tempo_bpm") is None
    assert abs(r["music"]["steady_tone"]["hz"] - hz) < 0.05 * hz + 3


def test_two_held_notes_are_still_music(tmp_path):
    """A held fifth (C + G) is harmony, not a single tone with harmonics."""
    t = np.arange(int(12 * SR)) / SR
    y = 0.15 * (np.sin(2 * np.pi * 261.63 * t) + np.sin(2 * np.pi * 392.0 * t))
    r = analyze_audio(str(_write_av(tmp_path, y, "fifth")))
    assert r["music"]["present"] and not r["music"].get("steady_tone")


def test_pad_without_drums_reports_no_tempo(tmp_path):
    """A sustained chord with no percussion is music, but there is no beat to count."""
    t = np.arange(int(12 * SR)) / SR
    y = 0.08 * sum(np.sin(2 * np.pi * f * t) for f in (261.63, 329.63, 392.0, 523.25))
    r = analyze_audio(str(_write_av(tmp_path, y, "pad_nobeat")))
    assert r["music"]["present"] and r["music"].get("no_beat") and r["music"].get("tempo_bpm") is None


def test_beat_survives_percussive_floor(music_mp4):
    r = analyze_audio(str(music_mp4))
    assert not r["music"].get("no_beat") and r["music"].get("tempo_bpm")


def _syllables(pitches_hz, syl=0.25, gap=0.05, seed=0):
    """One voice: the same harmonic timbre throughout, a gliding pitch per syllable, short gaps between."""
    rng = np.random.default_rng(seed)
    out = []
    for f in pitches_hz:
        t = np.arange(int(syl * SR)) / SR
        glide = f * (1 + rng.uniform(-0.15, 0.15) * t / syl)
        ph = 2 * np.pi * np.cumsum(glide) / SR
        y = sum((0.7 ** k) * np.sin((k + 1) * ph) for k in range(8))
        out += [y * np.hanning(len(t)), np.zeros(int(gap * SR))]
    y = np.concatenate(out)
    return 0.3 * y / np.abs(y).max()


def test_vocal_repetition_separates_narration_from_repeated_lines():
    from rea_video.audio import N_FFT, vocal_repetition

    freqs = np.fft.rfftfreq(N_FFT, 1 / SR)
    rng = np.random.default_rng(1)
    speech = _syllables(rng.uniform(110, 190, 100))  # 30 s, the pitch never retraces a line
    line = rng.choice([220.0, 246.9, 261.6, 293.7, 329.6, 349.2, 392.0], 26)
    song = _syllables(np.tile(line, 4), syl=0.25, gap=0.05)  # an ~8 s line sung four times
    assert vocal_repetition(speech, freqs) <= 0.1
    assert vocal_repetition(song, freqs) > 0.3
