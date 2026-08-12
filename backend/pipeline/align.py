from __future__ import annotations

import numpy as np

from .normalize import posture_deviation


def _valid_frames(sequence: list[np.ndarray | None]) -> tuple[np.ndarray, list[int]]:
    valid = [(idx, frame) for idx, frame in enumerate(sequence) if frame is not None]
    if not valid:
        raise ValueError("No valid pose frames were found.")
    indices = [idx for idx, _ in valid]
    flat = np.asarray([np.asarray(frame, dtype=float).reshape(-1) for _, frame in valid])
    return flat, indices


def _dtw_path(ref: np.ndarray, user: np.ndarray) -> list[tuple[int, int]]:
    distances = np.linalg.norm(ref[:, None, :] - user[None, :, :], axis=2)
    n_ref, n_user = distances.shape
    costs = np.full((n_ref + 1, n_user + 1), np.inf)
    costs[0, 0] = 0.0

    for i in range(1, n_ref + 1):
        for j in range(1, n_user + 1):
            costs[i, j] = distances[i - 1, j - 1] + min(
                costs[i - 1, j],
                costs[i, j - 1],
                costs[i - 1, j - 1],
            )

    path: list[tuple[int, int]] = []
    i, j = n_ref, n_user
    while i > 0 and j > 0:
        path.append((i - 1, j - 1))
        step = int(np.argmin([costs[i - 1, j - 1], costs[i - 1, j], costs[i, j - 1]]))
        if step == 0:
            i -= 1
            j -= 1
        elif step == 1:
            i -= 1
        else:
            j -= 1
    path.reverse()
    return path


def align_sequences(
    ref_seq: list[np.ndarray | None],
    user_seq: list[np.ndarray | None],
    gamma: float = 1.0,
) -> tuple[float, list[tuple[int, int]]]:
    """
    Return alignment cost and frame-index path mapping reference frames to user frames.

    Uses tslearn Soft-DTW when available. Falls back to classic DTW so validation
    and tests still run in lightweight environments.
    """
    ref_flat, ref_indices = _valid_frames(ref_seq)
    user_flat, user_indices = _valid_frames(user_seq)

    try:
        from tslearn.metrics import soft_dtw, dtw_path

        valid_path, cost = dtw_path(ref_flat, user_flat)
        soft_cost = float(soft_dtw(ref_flat, user_flat, gamma=gamma))
        path = [(ref_indices[i], user_indices[j]) for i, j in valid_path]
        return soft_cost, path
    except ImportError:
        valid_path = _dtw_path(ref_flat, user_flat)
        path = [(ref_indices[i], user_indices[j]) for i, j in valid_path]
        cost = float(sum(np.linalg.norm(ref_flat[i] - user_flat[j]) for i, j in valid_path))
        return cost, path


def compute_form_score(
    ref_seq: list[np.ndarray | None],
    user_seq: list[np.ndarray | None],
    path: list[tuple[int, int]],
) -> float:
    """Compute mean posture deviation along the aligned frame path."""
    deviations = [
        posture_deviation(ref_seq[i], user_seq[j])
        for i, j in path
        if ref_seq[i] is not None and user_seq[j] is not None
    ]
    if not deviations:
        raise ValueError("Alignment path contained no valid comparable frames.")
    return float(np.mean(deviations))
