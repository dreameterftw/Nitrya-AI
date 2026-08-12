from __future__ import annotations

from pathlib import Path

import numpy as np


def _sequence_to_object_array(sequence: list[np.ndarray | None]) -> np.ndarray:
    return np.asarray(sequence, dtype=object)


def save_pose_sequence(sequence: dict[str, list[np.ndarray | None]], path: str | Path) -> Path:
    """Serialize pose data locally; upload this artifact to R2 for profile caching."""
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(
        output_path,
        pose_2d=_sequence_to_object_array(sequence.get("pose_2d", [])),
        pose_3d=_sequence_to_object_array(sequence["pose_3d"]),
        normalized=_sequence_to_object_array(sequence["normalized"]),
    )
    return output_path


def load_pose_sequence(path: str | Path) -> dict[str, list[np.ndarray | None]]:
    loaded = np.load(Path(path), allow_pickle=True)
    return {
        "pose_2d": loaded.get("pose_2d", np.asarray([], dtype=object)).tolist(),
        "pose_3d": loaded["pose_3d"].tolist(),
        "normalized": loaded["normalized"].tolist(),
    }
