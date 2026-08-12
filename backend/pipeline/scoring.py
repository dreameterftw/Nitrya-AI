from __future__ import annotations

import numpy as np

from .align import align_sequences, compute_form_score
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
