import numpy as np

from backend.pipeline.align import align_sequences, compute_form_score
from backend.pipeline.cache import load_pose_sequence, save_pose_sequence
from backend.pipeline.normalize import normalize_sequence
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
