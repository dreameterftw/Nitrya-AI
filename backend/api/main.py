from __future__ import annotations

import tempfile
import uuid
from pathlib import Path

from celery.result import AsyncResult
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from backend.api.storage import upload_to_r2
from backend.api.supabase_client import get_supabase
from backend.api.tasks import analyze_attempt, cache_profile_pose, celery_app

app = FastAPI(title="Nritya AI API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/profiles")
async def create_profile(
    dancer_name: str = Form(...),
    genre: str = Form(...),
    owner_user_id: str = Form(...),
    video: UploadFile = File(...),
) -> dict[str, str]:
    profile_id = str(uuid.uuid4())

    with tempfile.TemporaryDirectory() as tmpdir:
        suffix = Path(video.filename or "reference.mp4").suffix or ".mp4"
        video_path = Path(tmpdir) / f"{profile_id}_ref{suffix}"
        video_path.write_bytes(await video.read())

        video_url = upload_to_r2(video_path, f"profiles/{profile_id}{suffix}")
        pose_url = cache_profile_pose(profile_id, video_path)

    get_supabase().table("profiles").insert(
        {
            "id": profile_id,
            "owner_user_id": owner_user_id,
            "dancer_name": dancer_name,
            "genre": genre,
            "reference_video_url": video_url,
            "pose_sequence_url": pose_url,
        }
    ).execute()

    return {"profile_id": profile_id, "status": "ready"}


@app.post("/attempts")
async def create_attempt(
    profile_id: str = Form(...),
    user_id: str | None = Form(default=None),
    video: UploadFile = File(...),
) -> dict[str, str]:
    attempt_id = str(uuid.uuid4())

    with tempfile.TemporaryDirectory() as tmpdir:
        suffix = Path(video.filename or "attempt.mp4").suffix or ".mp4"
        video_path = Path(tmpdir) / f"{attempt_id}{suffix}"
        video_path.write_bytes(await video.read())
        video_url = upload_to_r2(video_path, f"attempts/{attempt_id}{suffix}")

    get_supabase().table("attempts").insert(
        {
            "id": attempt_id,
            "user_id": user_id,
            "profile_id": profile_id,
            "video_url": video_url,
        }
    ).execute()

    task = analyze_attempt.delay(attempt_id, profile_id, video_url)
    return {"attempt_id": attempt_id, "task_id": task.id, "status": "processing"}


@app.get("/attempts/{task_id}/status")
async def get_status(task_id: str) -> dict:
    result = AsyncResult(task_id, app=celery_app)
    if result.state == "PENDING":
        return {"status": "queued", "stage": "queued", "pct": 0}
    if result.state == "PROGRESS":
        info = result.info if isinstance(result.info, dict) else {}
        return {"status": "processing", **info}
    if result.state == "SUCCESS":
        return {"status": "done", "result": result.result}
    if result.state == "FAILURE":
        return {"status": "failed", "error": str(result.info)}
    return {"status": result.state.lower()}
