from __future__ import annotations

import argparse
from pathlib import Path

from .align import align_sequences, compute_form_score
from .pose_pipeline import video_to_pose_sequence

GENRES = ("bharatanatyam", "kathak", "hip_hop", "freestyle")


def run_validation(genre_dir: str | Path, reference_path: str | Path) -> dict[str, list[float]]:
    ref_seq = video_to_pose_sequence(reference_path)["normalized"]
    results: dict[str, list[float]] = {"good": [], "bad": []}
    genre_path = Path(genre_dir)

    for label in ("good", "bad"):
        for clip_path in sorted(genre_path.glob(f"{label}_*.mp4")):
            user_seq = video_to_pose_sequence(clip_path)["normalized"]
            _, path = align_sequences(ref_seq, user_seq)
            score = compute_form_score(ref_seq, user_seq, path)
            results[label].append(score)
    return results


def check_separation(results: dict[str, list[float]], threshold_pairs: float = 0.8) -> bool:
    """Lower score = better. Check pairwise good < bad."""
    correct = sum(1 for good in results["good"] for bad in results["bad"] if good < bad)
    total = len(results["good"]) * len(results["bad"])
    if total == 0:
        raise ValueError("Validation requires at least one good and one bad score.")
    rate = correct / total
    print(f"Pairwise separation rate: {rate:.2%}")
    return rate >= threshold_pairs


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Phase 1 pairwise score validation.")
    parser.add_argument("--genre-dir", required=True)
    parser.add_argument("--reference", required=True)
    parser.add_argument("--threshold", type=float, default=0.8)
    args = parser.parse_args()

    results = run_validation(args.genre_dir, args.reference)
    return 0 if check_separation(results, args.threshold) else 1


if __name__ == "__main__":
    raise SystemExit(main())
