from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np

from .pose_pipeline import video_to_pose_sequence


def extract_musical_beats(audio_path: str | Path) -> np.ndarray:
    """Extract beat times in seconds with Librosa's beat tracker."""
    try:
        import librosa
    except ImportError as exc:
        raise RuntimeError(
            "librosa is required for musical beat detection. Install dependencies with "
            "`pip install -r backend/pipeline/requirements.txt`."
        ) from exc

    y, sr = librosa.load(str(audio_path))
    _, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
    return librosa.frames_to_time(beat_frames, sr=sr)


def extract_beats_madmom(audio_path: str | Path) -> np.ndarray:
    """Extract beat times in seconds with madmom for A/B validation on percussive clips."""
    try:
        import madmom
    except ImportError as exc:
        raise RuntimeError(
            "madmom is optional and is mainly for rhythm A/B validation. Install it "
            "manually in an environment where it supports your Python version."
        ) from exc

    processor = madmom.features.beats.RNNBeatProcessor()
    activation = processor(str(audio_path))
    tracker = madmom.features.beats.DBNBeatTrackingProcessor(fps=100)
    return np.asarray(tracker(activation), dtype=float)


def extract_kinematic_beats(
    pose_sequence: list[np.ndarray | None],
    fps: float,
    joint_idx: int = 0,
    min_interval_seconds: float = 0.15,
) -> np.ndarray:
    """Extract movement-peak times from normalized pose frames."""
    if fps <= 0:
        raise ValueError("fps must be positive.")

    valid: list[tuple[int, np.ndarray]] = [
        (idx, np.asarray(frame, dtype=float))
        for idx, frame in enumerate(pose_sequence)
        if frame is not None
    ]
    if len(valid) < 3:
        return np.asarray([], dtype=float)

    frame_indices = np.asarray([idx for idx, _ in valid])
    positions = np.asarray([frame[joint_idx] for _, frame in valid])
    velocity = np.linalg.norm(np.diff(positions, axis=0), axis=1)
    if len(velocity) < 3:
        return np.asarray([], dtype=float)

    min_distance = max(1, int(fps * min_interval_seconds))
    peaks = _find_local_peaks(velocity, min_distance)
    peak_source_indices = frame_indices[1:][peaks]
    return peak_source_indices / fps


def _find_local_peaks(values: np.ndarray, min_distance: int) -> np.ndarray:
    """Small local-max peak finder to avoid making SciPy mandatory for Phase 2."""
    candidates = [
        idx
        for idx in range(1, len(values) - 1)
        if values[idx] > values[idx - 1] and values[idx] >= values[idx + 1]
    ]
    if not candidates:
        return np.asarray([], dtype=int)

    ordered = sorted(candidates, key=lambda idx: values[idx], reverse=True)
    selected: list[int] = []
    for idx in ordered:
        if all(abs(idx - chosen) >= min_distance for chosen in selected):
            selected.append(idx)
    return np.asarray(sorted(selected), dtype=int)


def beat_alignment_score(
    musical_beats: np.ndarray,
    kinematic_beats: np.ndarray,
    tolerance: float = 0.15,
) -> float:
    """Return the fraction of musical beats with a nearby kinematic beat."""
    musical = np.asarray(musical_beats, dtype=float)
    kinematic = np.asarray(kinematic_beats, dtype=float)
    if len(musical) == 0:
        return 0.0
    if len(kinematic) == 0:
        return 0.0

    matched = 0
    for beat in musical:
        nearest_dist = np.min(np.abs(kinematic - beat))
        if nearest_dist <= tolerance:
            matched += 1
    return matched / len(musical)


def compute_full_score(form_score: float, bas: float, weights: dict[str, float]) -> float:
    """
    Combine Phase 1 form score with Phase 2 rhythm score.

    form_score is lower-is-better; BAS is higher-is-better. form_scale must be
    calibrated from the Phase 1 validation distribution before production use.
    """
    form_scale = weights.get("form_scale", 1.0)
    if form_scale <= 0:
        raise ValueError("form_scale must be positive.")

    form_component = max(0.0, min(1.0, 1.0 - form_score / form_scale))
    posture_weight = weights["posture"]
    rhythm_weight = weights["rhythm"]
    return posture_weight * form_component + rhythm_weight * bas


def validate_rhythm(
    genre_dir: str | Path,
    audio_path: str | Path,
    fps: float,
    joint_idx: int = 0,
    tolerance: float = 0.15,
) -> dict[str, list[float]]:
    musical_beats = extract_musical_beats(audio_path)
    results: dict[str, list[float]] = {"good": [], "bad": []}
    genre_path = Path(genre_dir)

    for label in ("good", "bad"):
        for clip_path in sorted(genre_path.glob(f"{label}_*.mp4")):
            pose_seq = video_to_pose_sequence(clip_path)["normalized"]
            kinematic_beats = extract_kinematic_beats(pose_seq, fps, joint_idx)
            bas = beat_alignment_score(musical_beats, kinematic_beats, tolerance)
            results[label].append(bas)
    return results


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Phase 2 rhythm validation.")
    parser.add_argument("--genre-dir", required=True)
    parser.add_argument("--audio", required=True)
    parser.add_argument("--fps", type=float, required=True)
    parser.add_argument("--joint-idx", type=int, default=0)
    parser.add_argument("--tolerance", type=float, default=0.15)
    args = parser.parse_args()

    results = validate_rhythm(args.genre_dir, args.audio, args.fps, args.joint_idx, args.tolerance)
    print(results)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
