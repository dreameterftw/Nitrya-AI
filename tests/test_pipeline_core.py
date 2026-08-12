import numpy as np

from backend.pipeline.align import align_sequences, compute_form_score
from backend.pipeline.cache import load_pose_sequence, save_pose_sequence
from backend.pipeline.normalize import normalize_sequence
from backend.pipeline.rhythm import (
    beat_alignment_score,
    compute_full_score,
    extract_kinematic_beats,
)
from backend.pipeline.validate import check_separation


def _frame(offset: float = 0.0) -> np.ndarray:
    return np.asarray(
        [
            [0.0 + offset, 0.0, 0.0],
            [1.0 + offset, 0.0, 0.0],
            [0.0 + offset, 1.0, 0.0],
        ]
    )


def test_alignment_and_form_score_are_scalar():
    ref = normalize_sequence([_frame(), _frame(0.1)])
    user = normalize_sequence([_frame(), _frame(0.2)])

    _, path = align_sequences(ref, user)
    score = compute_form_score(ref, user, path)

    assert path
    assert isinstance(score, float)
    assert score >= 0.0


def test_check_separation_passes_pairwise_threshold():
    assert check_separation({"good": [0.1, 0.2], "bad": [0.8, 0.9]}, threshold_pairs=0.8)


def test_pose_sequence_cache_roundtrip(tmp_path):
    sequence = {
        "pose_2d": [np.asarray([[0.0, 0.0]])],
        "pose_3d": [_frame()],
        "normalized": normalize_sequence([_frame()]),
    }
    path = save_pose_sequence(sequence, tmp_path / "pose.npz")

    loaded = load_pose_sequence(path)

    assert np.allclose(loaded["pose_3d"][0], sequence["pose_3d"][0])


def test_kinematic_beats_find_velocity_peaks():
    sequence = [
        np.asarray([[0.0, 0.0, 0.0]]),
        np.asarray([[1.0, 0.0, 0.0]]),
        np.asarray([[1.1, 0.0, 0.0]]),
        np.asarray([[3.0, 0.0, 0.0]]),
        np.asarray([[3.1, 0.0, 0.0]]),
        np.asarray([[5.0, 0.0, 0.0]]),
        np.asarray([[5.1, 0.0, 0.0]]),
    ]

    beats = extract_kinematic_beats(sequence, fps=10.0, joint_idx=0, min_interval_seconds=0.1)

    assert np.allclose(beats, np.asarray([0.3, 0.5]))


def test_beat_alignment_score_counts_nearby_motion_beats():
    musical = np.asarray([0.5, 1.0, 1.5, 2.0])
    kinematic = np.asarray([0.52, 1.48])

    assert beat_alignment_score(musical, kinematic, tolerance=0.05) == 0.5


def test_compute_full_score_combines_form_and_rhythm():
    score = compute_full_score(
        form_score=0.25,
        bas=0.8,
        weights={"posture": 0.6, "rhythm": 0.4, "form_scale": 1.0},
    )

    assert score == 0.77
