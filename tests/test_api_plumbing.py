from fastapi.testclient import TestClient

from backend.api.main import app
from backend.api.storage import materialize_file, upload_to_r2


def test_health_endpoint():
    client = TestClient(app)

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_pending_attempt_status_includes_stage_and_pct():
    client = TestClient(app)

    response = client.get("/attempts/not-a-real-task/status")

    assert response.status_code == 200
    assert response.json()["status"] in {"queued", "processing"}
    assert "pct" in response.json()


def test_local_storage_roundtrip(tmp_path, monkeypatch):
    monkeypatch.delenv("R2_ACCOUNT_ID", raising=False)
    monkeypatch.delenv("R2_ACCESS_KEY", raising=False)
    monkeypatch.delenv("R2_SECRET_KEY", raising=False)
    monkeypatch.delenv("R2_BUCKET", raising=False)
    monkeypatch.setenv("LOCAL_STORAGE_ROOT", str(tmp_path / "storage"))

    source = tmp_path / "clip.mp4"
    source.write_bytes(b"video")

    uri = upload_to_r2(source, "attempts/clip.mp4")
    target = tmp_path / "materialized.mp4"
    materialize_file(uri, target)

    assert target.read_bytes() == b"video"
