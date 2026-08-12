# Phase 2 - Rhythm

Goal: separate off-tempo from wrong movement using musical beats plus kinematic
beats from the Phase 1 pose sequences.

## Signals

- Musical beats: `extract_musical_beats(audio_path)` uses Librosa and returns beat times in seconds.
- Optional A/B tracker: `extract_beats_madmom(audio_path)` is available for environments where madmom installs cleanly.
- Kinematic beats: `extract_kinematic_beats(pose_sequence, fps, joint_idx)` finds local peaks in joint velocity.
- BAS: `beat_alignment_score(musical_beats, kinematic_beats)` returns the fraction of musical beats matched within tolerance.

## Combined Score

`compute_full_score(form_score, bas, weights)` combines Phase 1 form and Phase 2 rhythm:

```python
weights = {"posture": 0.65, "rhythm": 0.35, "form_scale": 1.0}
```

`form_scale` is a calibration placeholder. Set it from the observed good/bad
Phase 1 form-score distribution, not by guessing.

## Validation

Reuse the Phase 1 labeled clips and run rhythm validation per genre:

```bash
python -m backend.pipeline.rhythm --genre-dir validation_clips/hip_hop --audio references/hip_hop.wav --fps 30
```

BAS alone is expected to separate good/bad more strongly for hip-hop and freestyle
than for posture-heavy classical forms. For Kathak and Bharatanatyam, compare
Librosa against madmom on percussive clips before locking the tracker.
