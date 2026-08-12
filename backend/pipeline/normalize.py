from __future__ import annotations

import numpy as np


def _canonical_pose(n_joints: int) -> np.ndarray:
    x = np.linspace(-1.0, 1.0, n_joints)
    y = np.zeros(n_joints)
    z = np.zeros(n_joints)
    return np.stack([x, y, z], axis=1)


def _center_scale(points: np.ndarray) -> np.ndarray:
    centered = points - np.mean(points, axis=0, keepdims=True)
    norm = np.linalg.norm(centered)
    if norm == 0.0:
        raise ValueError("Cannot align a degenerate pose with zero variance.")
    return centered / norm


def procrustes_align(reference: np.ndarray, candidate: np.ndarray) -> tuple[np.ndarray, float]:
    """Align candidate to reference and return aligned points plus disparity."""
    ref = _center_scale(np.asarray(reference, dtype=float))
    cand = _center_scale(np.asarray(candidate, dtype=float))
    u, _, vt = np.linalg.svd(cand.T @ ref)
    rotation = u @ vt
    aligned = cand @ rotation
    disparity = float(np.sum((ref - aligned) ** 2))
    return aligned, disparity


def normalize_sequence(pose_3d: list[np.ndarray | None]) -> list[np.ndarray | None]:
    """Remove scale, translation, and rotation per frame relative to a canonical pose."""
    normalized: list[np.ndarray | None] = []
    for frame in pose_3d:
        if frame is None:
            normalized.append(None)
            continue
        frame_array = np.asarray(frame, dtype=float)
        aligned, _ = procrustes_align(_canonical_pose(frame_array.shape[0]), frame_array)
        normalized.append(aligned)
    return normalized


def posture_deviation(ref_frame: np.ndarray, user_frame: np.ndarray) -> float:
    """Return Procrustes disparity for a matched pair of frames. Lower is better."""
    _, disparity = procrustes_align(np.asarray(ref_frame, dtype=float), np.asarray(user_frame, dtype=float))
    return float(disparity)
