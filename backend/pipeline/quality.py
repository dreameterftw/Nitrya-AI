from __future__ import annotations

import numpy as np


def pose_quality_report(
    pose_sequence: list[np.ndarray | None],
    min_valid_frame_ratio: float = 0.7,
) -> dict[str, float | bool]:
    """Report whether enough pose frames were detected for a trustworthy score."""
    total_frames = len(pose_sequence)
    valid_frames = sum(1 for frame in pose_sequence if frame is not None)
    valid_frame_ratio = valid_frames / total_frames if total_frames else 0.0
    return {
        "total_frames": float(total_frames),
        "valid_frames": float(valid_frames),
        "valid_frame_ratio": round(valid_frame_ratio, 3),
        "passes_confidence_gate": valid_frame_ratio >= min_valid_frame_ratio,
    }


def require_pose_quality(
    pose_sequence: list[np.ndarray | None],
    min_valid_frame_ratio: float = 0.7,
) -> dict[str, float | bool]:
    report = pose_quality_report(pose_sequence, min_valid_frame_ratio)
    if not report["passes_confidence_gate"]:
        raise ValueError(
            "Pose detection confidence gate failed: "
            f"{report['valid_frame_ratio']:.1%} valid frames."
        )
    return report
