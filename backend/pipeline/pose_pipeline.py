from __future__ import annotations

from pathlib import Path
from typing import Any

import numpy as np

from .cache import save_pose_sequence
from .lift import lift_to_3d
from .normalize import normalize_sequence
from .quality import pose_quality_report

_YOLO_MODEL: Any | None = None


def _get_yolo_model() -> Any:
    global _YOLO_MODEL
    if _YOLO_MODEL is None:
        try:
            from ultralytics import YOLO
        except ImportError as exc:
            raise RuntimeError(
                "ultralytics is required for pose extraction. Install dependencies with "
                "`pip install -r backend/pipeline/requirements.txt`."
            ) from exc
        _YOLO_MODEL = YOLO("yolov8n-pose.pt")
    return _YOLO_MODEL


def extract_2d_pose(video_path: str | Path) -> list[np.ndarray | None]:
    """Return per-frame YOLO 2D keypoints as (n_joints, 2), preserving misses as None."""
    model = _get_yolo_model()
    results = model(str(video_path), stream=True)

    frames: list[np.ndarray | None] = []
    for result in results:
        if result.keypoints is not None and len(result.keypoints.xy) > 0:
            frames.append(result.keypoints.xy[0].cpu().numpy())
        else:
            frames.append(None)
    return frames


def video_to_pose_sequence(
    video_path: str | Path,
    *,
    cache_path: str | Path | None = None,
) -> dict[str, list[np.ndarray | None]]:
    """Single entry point for both profile reference uploads and user attempts."""
    pose_2d = extract_2d_pose(video_path)
    pose_3d = lift_to_3d(pose_2d)
    normalized = normalize_sequence(pose_3d)

    sequence = {
        "pose_2d": pose_2d,
        "pose_3d": pose_3d,
        "normalized": normalized,
        "quality": pose_quality_report(pose_2d),
    }
    if cache_path is not None:
        save_pose_sequence(sequence, cache_path)
    return sequence
