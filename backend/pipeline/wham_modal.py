from __future__ import annotations

import pickle

import numpy as np

try:
    import modal
except ImportError:
    modal = None


if modal is not None:
    app = modal.App("nritya-wham")
    image = modal.Image.debian_slim().pip_install("torch", "numpy").run_commands(
        "git clone https://github.com/yohanshin/WHAM.git /wham"
    )

    @app.function(image=image, gpu="T4", timeout=300)
    def lift_to_3d_remote(pose_2d_data: bytes) -> bytes:
        import sys

        sys.path.append("/wham")
        from wham_inference import run_lifting

        return run_lifting(pose_2d_data)
else:
    lift_to_3d_remote = None


def serialize_pose_2d(pose_2d: list[np.ndarray | None]) -> bytes:
    return pickle.dumps(pose_2d)


def deserialize_pose_3d(pose_3d_data: bytes) -> list[np.ndarray | None]:
    return pickle.loads(pose_3d_data)


def lift_to_3d_with_modal(pose_2d: list[np.ndarray | None]) -> list[np.ndarray | None]:
    if lift_to_3d_remote is None:
        raise RuntimeError("modal is required for remote WHAM inference.")
    result = lift_to_3d_remote.remote(serialize_pose_2d(pose_2d))
    return deserialize_pose_3d(result)
