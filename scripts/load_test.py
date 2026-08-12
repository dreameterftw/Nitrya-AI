from __future__ import annotations

import argparse
import concurrent.futures
from pathlib import Path

import requests


def submit_attempt(api_base_url: str, profile_id: str, video_path: Path) -> int:
    with video_path.open("rb") as video:
        response = requests.post(
            f"{api_base_url.rstrip('/')}/attempts",
            files={"video": video},
            data={"profile_id": profile_id},
            timeout=60,
        )
    return response.status_code


def main() -> int:
    parser = argparse.ArgumentParser(description="Submit concurrent attempts for queue/cost smoke testing.")
    parser.add_argument("--api-base-url", default="http://localhost:8000")
    parser.add_argument("--profile-id", required=True)
    parser.add_argument("--video", required=True, type=Path)
    parser.add_argument("--requests", type=int, default=50)
    parser.add_argument("--workers", type=int, default=10)
    args = parser.parse_args()

    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = [
            executor.submit(submit_attempt, args.api_base_url, args.profile_id, args.video)
            for _ in range(args.requests)
        ]
        statuses = [future.result() for future in futures]

    print({status: statuses.count(status) for status in sorted(set(statuses))})
    return 0 if all(200 <= status < 500 for status in statuses) else 1


if __name__ == "__main__":
    raise SystemExit(main())
