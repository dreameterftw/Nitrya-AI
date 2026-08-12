from __future__ import annotations

import numpy as np

from .align import align_sequences, compute_form_score


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
