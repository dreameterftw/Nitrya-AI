from __future__ import annotations

import os
import shutil
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import urlretrieve

LOCAL_STORAGE_ROOT = Path(os.getenv("LOCAL_STORAGE_ROOT", ".local_storage"))


def _r2_configured() -> bool:
    return all(
        os.getenv(name)
        for name in (
            "R2_ACCOUNT_ID",
            "R2_ACCESS_KEY",
            "R2_SECRET_KEY",
            "R2_BUCKET",
        )
    )


def upload_to_r2(file_path: str | Path, object_key: str) -> str:
    """
    Upload a file to Cloudflare R2.

    In local dev without R2 env vars, copy to `.local_storage` and return a local
    file path. The worker can consume either path or remote URL.
    """
    source = Path(file_path)
    if not _r2_configured():
        target = LOCAL_STORAGE_ROOT / object_key
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        return str(target)

    import boto3

    account_id = os.environ["R2_ACCOUNT_ID"]
    bucket = os.environ["R2_BUCKET"]
    public_base_url = os.getenv("R2_PUBLIC_BASE_URL")
    endpoint_url = f"https://{account_id}.r2.cloudflarestorage.com"
    client = boto3.client(
        "s3",
        endpoint_url=endpoint_url,
        aws_access_key_id=os.environ["R2_ACCESS_KEY"],
        aws_secret_access_key=os.environ["R2_SECRET_KEY"],
        region_name="auto",
    )
    client.upload_file(str(source), bucket, object_key)

    if public_base_url:
        return f"{public_base_url.rstrip('/')}/{object_key}"
    return f"r2://{bucket}/{object_key}"


def materialize_file(uri: str, target_path: str | Path) -> Path:
    """Ensure a local copy exists for pipeline tools that expect filesystem paths."""
    target = Path(target_path)
    target.parent.mkdir(parents=True, exist_ok=True)

    parsed = urlparse(uri)
    if parsed.scheme in ("http", "https"):
        urlretrieve(uri, target)
        return target
    if parsed.scheme == "file":
        shutil.copyfile(Path(parsed.path), target)
        return target

    source = Path(uri)
    if source.exists():
        shutil.copyfile(source, target)
        return target

    raise ValueError(f"Cannot materialize unsupported file URI: {uri}")
