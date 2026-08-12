# Phase 1 - Accuracy Core

Do not touch UI until this exit gate passes:

"On a hand-labeled set of 10 good + 10 bad takes per genre (across all 4 genres), the pipeline's score correctly ranks good above bad in ≥80% of pairs."

## Pipeline Contract

- `video_to_pose_sequence(video_path, cache_path=None)` is the shared entry point for profile uploads and user attempts.
- Profile upload path: extract once, save the `.npz` artifact, upload it to R2, and store the object URL in `profiles.pose_sequence_url`.
- User attempt path: extract every time, load the cached profile sequence, align, and score.
- Lower scalar form score means closer form.

## Validation Clips

Expected local structure:

```text
validation_clips/
  bharatanatyam/good_01.mp4 ... bad_10.mp4
  kathak/good_01.mp4 ... bad_10.mp4
  hip_hop/good_01.mp4 ... bad_10.mp4
  freestyle/good_01.mp4 ... bad_10.mp4
```

Run one genre:

```bash
python -m backend.pipeline.validate --genre-dir validation_clips/bharatanatyam --reference references/bharatanatyam.mp4
```

If a genre fails 80%, debug missing frames first, then reference quality, then alignment/normalization.
