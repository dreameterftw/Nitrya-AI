from __future__ import annotations

import numpy as np

from .normalize import posture_deviation


def keyframe_accuracy(
    ref_seq: list[np.ndarray | None],
    user_seq: list[np.ndarray | None],
    alignment_path: list[tuple[int, int]],
    keyframes: list[int],
) -> float | None:
    """Compute strict posture deviation at configured reference keyframes."""
    if not keyframes:
        return None

    deviations: list[float] = []
    for keyframe in keyframes:
        if keyframe >= len(ref_seq) or ref_seq[keyframe] is None:
            continue
        matched = [user_idx for ref_idx, user_idx in alignment_path if ref_idx == keyframe]
        if not matched:
            continue
        user_frame = user_seq[matched[0]]
        if user_frame is not None:
            deviations.append(posture_deviation(ref_seq[keyframe], user_frame))

    return float(np.mean(deviations)) if deviations else None
