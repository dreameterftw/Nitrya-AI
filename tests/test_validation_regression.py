from pathlib import Path

import pytest

from backend.pipeline.validate import check_separation, run_validation

GENRES = ("bharatanatyam", "kathak", "hip_hop", "freestyle")


@pytest.mark.parametrize("genre", GENRES)
def test_genre_separation_holds_when_validation_clips_exist(genre):
    genre_dir = Path("validation_clips") / genre
    reference = genre_dir / "reference.mp4"
    if not reference.exists():
        pytest.skip(f"Validation clips for {genre} are not present yet.")

    results = run_validation(genre_dir, reference)

    assert check_separation(results, threshold_pairs=0.8)
