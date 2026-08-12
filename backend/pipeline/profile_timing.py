from __future__ import annotations

import time
from pathlib import Path

from .lift import lift_to_3d
from .normalize import normalize_sequence
from .pose_pipeline import extract_2d_pose
from .quality import pose_quality_report


def timed_pipeline_run(video_path: str | Path) -> dict[str, float | dict]:
    """Profile the pipeline before moving any step to paid infrastructure."""
    timings: dict[str, float | dict] = {}

    t0 = time.perf_counter()
    pose_2d = extract_2d_pose(video_path)
    timings["yolo_2d"] = time.perf_counter() - t0
    timings["pose_quality"] = pose_quality_report(pose_2d)

    t0 = time.perf_counter()
    pose_3d = lift_to_3d(pose_2d)
    timings["wham_3d"] = time.perf_counter() - t0

    t0 = time.perf_counter()
    normalize_sequence(pose_3d)
    timings["procrustes"] = time.perf_counter() - t0

    timings["total"] = sum(
        value for key, value in timings.items() if key != "pose_quality" and isinstance(value, float)
    )
    return timings
