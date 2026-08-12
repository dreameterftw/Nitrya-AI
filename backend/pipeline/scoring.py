from __future__ import annotations

import numpy as np

from .align import align_sequences, compute_form_score
from .config import get_genre_config
from .keyframes import keyframe_accuracy
from .rhythm import beat_alignment_score, compute_full_score, extract_kinematic_beats


def score_attempt(
    reference_sequence: list[np.ndarray | None],
    attempt_sequence: list[np.ndarray | None],
) -> dict[str, float]:
    """Return the scalar form score and alignment cost. Lower score is better."""
    alignment_cost, path = align_sequences(reference_sequence, attempt_sequence)
    form_score = compute_form_score(reference_sequence, attempt_sequence, path)
    return {
        "score": form_score,
        "alignment_cost": alignment_cost,
        "matched_frames": float(len(path)),
    }


def score_attempt_with_rhythm(
    reference_sequence: list[np.ndarray | None],
    attempt_sequence: list[np.ndarray | None],
    musical_beats: np.ndarray,
    fps: float,
    weights: dict[str, float],
    joint_idx: int = 0,
) -> dict[str, float]:
    """Return form, rhythm, and weighted combined score. Higher full_score is better."""
    form_result = score_attempt(reference_sequence, attempt_sequence)
    kinematic_beats = extract_kinematic_beats(attempt_sequence, fps, joint_idx)
    bas = beat_alignment_score(musical_beats, kinematic_beats)
    full_score = compute_full_score(form_result["score"], bas, weights)
    return {
        **form_result,
        "beat_alignment_score": bas,
        "full_score": full_score,
    }


def score_attempt_with_config(
    profile_genre: str,
    reference_sequence: list[np.ndarray | None],
    attempt_sequence: list[np.ndarray | None],
    musical_beats: np.ndarray,
    fps: float,
    joint_idx: int = 0,
) -> dict[str, float | list[str] | list[int] | bool | None]:
    """Score an attempt using genre-specific weights and active submodels."""
    cfg = get_genre_config(profile_genre)
    alignment_cost, path = align_sequences(reference_sequence, attempt_sequence)
    form_score = compute_form_score(reference_sequence, attempt_sequence, path)
    kinematic_beats = extract_kinematic_beats(attempt_sequence, fps, joint_idx)
    bas = beat_alignment_score(musical_beats, kinematic_beats)

    form_component = max(0.0, min(1.0, 1.0 - form_score / cfg["form_scale"]))
    total = (
        cfg["posture_weight"] * form_component
        + cfg["rhythm_weight"] * bas
    )

    result: dict[str, float | list[str] | list[int] | bool | None] = {
        "total_score": round(float(total), 3),
        "form_component": round(float(form_component), 3),
        "form_score": round(float(form_score), 3),
        "bas": round(float(bas), 3),
        "alignment_cost": round(float(alignment_cost), 3),
        "matched_frames": float(len(path)),
        "active_submodels": cfg["active_submodels"],
        "keyframes_used": cfg["keyframes"],
    }

    if "keyframe_matcher" in cfg["active_submodels"]:
        result["keyframe_accuracy"] = keyframe_accuracy(
            reference_sequence,
            attempt_sequence,
            path,
            cfg["keyframes"],
        )

    if "mudra_layer" in cfg["active_submodels"]:
        result["mudra_layer_available"] = True

    return result


def validate_with_config(
    genre: str,
    results_form: dict[str, list[float]],
    results_bas: dict[str, list[float]],
) -> dict[str, float | bool]:
    """Check pairwise separation for config-weighted score. Higher is better."""
    cfg = get_genre_config(genre)
    scores: dict[str, list[float]] = {"good": [], "bad": []}
    for label in ("good", "bad"):
        for form_score, bas in zip(results_form[label], results_bas[label]):
            form_component = max(0.0, min(1.0, 1.0 - form_score / cfg["form_scale"]))
            score = cfg["posture_weight"] * form_component + cfg["rhythm_weight"] * bas
            scores[label].append(score)

    correct = sum(1 for good in scores["good"] for bad in scores["bad"] if good > bad)
    total = len(scores["good"]) * len(scores["bad"])
    if total == 0:
        raise ValueError("Validation requires at least one good and one bad score.")

    rate = correct / total
    print(f"{genre}: {rate:.2%} pairwise separation with combined score")
    return {"rate": rate, "passed": rate >= 0.8}
