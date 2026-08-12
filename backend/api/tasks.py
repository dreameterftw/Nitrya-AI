from __future__ import annotations

import os
import tempfile
import time
from pathlib import Path

from celery import Celery

from backend.api.storage import materialize_file, upload_to_r2
from backend.api.supabase_client import get_supabase
from backend.pipeline.cache import load_pose_sequence
from backend.pipeline.pose_pipeline import video_to_pose_sequence
from backend.pipeline.quality import require_pose_quality
from backend.pipeline.rhythm import extract_musical_beats
from backend.pipeline.scoring import score_attempt_with_config

celery_app = Celery(
    "nritya",
    broker=os.getenv("REDIS_URL", "memory://"),
    backend=os.getenv("CELERY_RESULT_BACKEND", os.getenv("REDIS_URL", "cache+memory://")),
)


@celery_app.task(name="backend.api.tasks.analyze_attempt")
def analyze_attempt(attempt_id: str, profile_id: str, video_url: str, fps: float = 30.0) -> dict:
    supabase = get_supabase()
    profile = (
        supabase.table("profiles")
        .select("*")
        .eq("id", profile_id)
        .single()
        .execute()
        .data
    )
    if not profile:
        raise ValueError(f"Profile {profile_id!r} was not found.")

    t0 = time.perf_counter()
    with tempfile.TemporaryDirectory() as tmpdir:
        attempt_path = materialize_file(video_url, Path(tmpdir) / f"{attempt_id}.mp4")
        pose_path = materialize_file(profile["pose_sequence_url"], Path(tmpdir) / f"{profile_id}_pose.npz")

        ref_seq = load_pose_sequence(pose_path)["normalized"]
        user_pose_data = video_to_pose_sequence(attempt_path)
        require_pose_quality(user_pose_data["pose_2d"])
        user_seq = user_pose_data["normalized"]
        musical_beats = extract_musical_beats(attempt_path)
        result = score_attempt_with_config(profile["genre"], ref_seq, user_seq, musical_beats, fps)

    gpu_seconds = time.perf_counter() - t0
    result["gpu_seconds_used"] = round(gpu_seconds, 3)

    supabase.table("attempts").update(
        {
            "score": result["total_score"],
            "feedback": result,
            "gpu_seconds_used": result["gpu_seconds_used"],
        }
    ).eq("id", attempt_id).execute()

    return result


def cache_profile_pose(profile_id: str, video_path: str | Path) -> str:
    with tempfile.TemporaryDirectory() as tmpdir:
        pose_data = video_to_pose_sequence(video_path)
        local_pose_path = Path(tmpdir) / f"{profile_id}_pose.npz"
        from backend.pipeline.cache import save_pose_sequence

        save_pose_sequence(pose_data, local_pose_path)
        return upload_to_r2(local_pose_path, f"profiles/{profile_id}_pose.npz")
