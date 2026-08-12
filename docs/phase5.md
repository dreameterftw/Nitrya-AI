# Phase 5 - Scale / Pilot

Goal: pilot the Phase 4 PWA with real users and move only the confirmed expensive
step, WHAM/3D lifting, to usage-billed GPU.

## Profile Before Spending

Run timing on real pilot attempts:

```bash
python -c "from backend.pipeline.profile_timing import timed_pipeline_run; print(timed_pipeline_run('path/to/clip.mp4'))"
```

Do not route production traffic to paid GPU until timings confirm `wham_3d`
dominates.

## Remote WHAM

Set `USE_REMOTE_GPU=true` to route `lift_to_3d()` through Modal. Leave it unset
for local/Colab development. Modal requires account setup outside the repo.

## Cost Tracking

Migration `0003_attempt_gpu_seconds.sql` adds:

```sql
alter table attempts add column gpu_seconds_used numeric;
```

The Celery worker writes `gpu_seconds_used` into `attempts` and also includes it
in `feedback`.

## Silent Failure Protection

`pose_quality_report()` and `require_pose_quality()` guard against low valid-frame
ratios from poor camera framing or pose detection failures. The worker currently
requires at least 70% valid pose frames before scoring an attempt.

## Pilot Checks

- Review Supabase, R2, Vercel, and Render usage dashboards after real traffic.
- Do not upgrade free tiers until real usage demands it.
- Re-run Phase 1/2/3 separation checks on real pilot footage.
- Watch failures by genre; tune config weights only after comparing form-only and BAS-only separation.
