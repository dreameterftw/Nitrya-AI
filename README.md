# Nritya AI

Nritya AI is a dance-learning MVP that compares a user's recorded attempt against a reference dancer/profile and returns a form/rhythm score. The project is built around a staged accuracy-first plan: prove scoring quality before UI polish, then wrap the pipeline in an async PWA.

## Current Status

The repo now contains all six core phases plus pilot-readiness should-have work:

- Phase 0: locked decisions, schema, repo structure
- Phase 1: pose extraction, normalization, alignment, validation gate
- Phase 2: rhythm/beat alignment scoring
- Phase 3: genre config and keyframe-aware scoring
- Phase 4: FastAPI + Celery backend and bare Next PWA plumbing
- Phase 5: pilot scaling instrumentation, GPU timing, optional Modal WHAM path
- Phase 6: dual-theme Western/Indian UI polish
- Should-have additions: progress UX, onboarding flow, Supabase Auth UI, analytics hooks, env examples, CI/testing strategy, and deployment/free-tier documentation

The product is still a pilot MVP, not a production launch. Real validation clips, Supabase/R2/Redis credentials, Modal setup, and live deployment configuration are still external setup steps.

## MVP Scope

Locked MVP genres:

- Bharatanatyam
- Kathak
- Hip-hop
- Freestyle

Folk is deliberately out of scope for MVP and can be revisited after the core scoring loop is proven.

Reference content model:

- Users create dancer/influencer profiles.
- Each profile has one reference video for MVP.
- Reference video pose sequences are extracted once, cached, and reused.
- Personal-use framing: uploaded references are not redistributed or shown to other users.

Phase 1 acceptance gate:

> "On a hand-labeled set of 10 good + 10 bad takes per genre (across all 4 genres), the pipeline's score correctly ranks good above bad in ≥80% of pairs."

## Architecture

```text
frontend/                 Next.js PWA
  app/                    App Router pages/routes
  components/             Theme-aware UI components
  lib/                    Theme, analytics, Supabase client helpers

backend/
  api/                    FastAPI app, Celery worker, R2/Supabase utilities
  pipeline/               Pose/rhythm/scoring/config logic

supabase/migrations/      Database schema migrations
tests/                    Python unit/API/regression tests
scripts/                  Utility scripts
docs/                     Phase notes and operating docs
```

Runtime flow:

1. User records or uploads an attempt in the PWA.
2. Frontend posts the video to `/attempts`.
3. FastAPI stores the raw video in R2 or local dev storage.
4. FastAPI inserts an attempt row and queues a Celery task.
5. Celery loads the profile reference pose sequence.
6. Pipeline extracts user pose, applies quality gates, scores form/rhythm with genre config, and writes the result back to Supabase.
7. Frontend polls `/attempts/{task_id}/status` and shows progress, cold-start messaging, errors, or themed results.

## Backend

Backend stack:

- FastAPI
- Celery
- Redis/Upstash-compatible broker
- Supabase Postgres/Auth
- Cloudflare R2 via S3-compatible API
- Modal optional GPU path for WHAM

Install:

```bash
python -m pip install -r requirements-dev.txt
```

Run API locally:

```bash
uvicorn backend.api.main:app --reload
```

Run worker locally:

```bash
celery -A backend.api.tasks worker --loglevel=info
```

Health check:

```bash
curl http://localhost:8000/health
```

Important backend env vars are listed in [.env.example](.env.example).

## Pipeline

Key modules:

- `backend/pipeline/pose_pipeline.py`: shared entry point for reference and attempt videos
- `backend/pipeline/lift.py`: local z=0 fallback or optional remote GPU lifting
- `backend/pipeline/normalize.py`: Procrustes-style normalization
- `backend/pipeline/align.py`: alignment and form scoring
- `backend/pipeline/rhythm.py`: musical/kinematic beat alignment
- `backend/pipeline/config.py`: genre weights and active submodels
- `backend/pipeline/keyframes.py`: keyframe strictness for classical forms
- `backend/pipeline/quality.py`: confidence/framing gate
- `backend/pipeline/profile_timing.py`: timing profiler before moving work to paid GPU

The local `lift_to_3d()` fallback preserves the pipeline contract but is not a real WHAM replacement. Use WHAM/Modal before judging final scoring quality.

## Frontend

Frontend stack:

- Next.js App Router
- PWA via `next-pwa`
- Framer Motion for score animation
- Supabase Auth UI
- Vercel Analytics
- Vitest for component tests
- Playwright config for E2E skeleton

Install:

```bash
cd frontend
npm install --legacy-peer-deps
```

Run locally:

```bash
npm run dev
```

Build:

```bash
npm run build
```

Frontend env vars are listed in [frontend/.env.example](frontend/.env.example).

## UI Themes

The UI uses one component tree and switches presentation through a client-side theme context:

- Western theme: dark, high-contrast, faster/snappier score reveal, flow-energy emphasis
- Indian theme: warm, instructional, measured score reveal, keyframe/mudra-readiness emphasis

Theme choice is stored in `localStorage` only. It does not alter scoring logic or backend data.

Important routes:

- `/signup`
- `/onboarding`
- `/onboarding/theme`
- `/onboarding/tutorial`
- `/onboarding/profile`
- `/discover`
- `/record`
- `/results/[taskId]`
- `/results-preview`

## Database

Migrations:

- `0001_init.sql`: `profiles` and `attempts`
- `0002_genre_config.sql`: genre weights, tolerances, keyframes, active submodels
- `0003_attempt_gpu_seconds.sql`: per-attempt GPU/cost tracking

After linking Supabase:

```bash
supabase db push
```

## Storage

Videos and pose artifacts should live in Cloudflare R2.

In local dev, if R2 env vars are absent, upload helpers copy files into `.local_storage/`, which is gitignored.

Use separate R2 buckets for dev/staging and production, for example:

- `nritya-videos-dev`
- `nritya-videos-prod`

## Environment Strategy

The original three-project Supabase plan was adjusted because the free tier only supports two active free projects comfortably.

Recommended pilot setup:

- Shared dev/staging Supabase project
- Separate production/pilot Supabase project
- Separate R2 dev and prod buckets
- Vercel Preview/Development env vars point to dev/staging
- Vercel Production env vars point to prod

See:

- [docs/environment.md](docs/environment.md)
- [docs/deployment-free-tier.md](docs/deployment-free-tier.md)

## Testing

Backend/pipeline tests:

```bash
python -m pytest tests -p no:cacheprovider --basetemp=.tmp\pytest
```

Coverage in CI:

```bash
pytest tests/ -v --cov=backend --cov-report=term-missing
```

Frontend tests:

```bash
cd frontend
npm run test
npm run build
```

Validation regression tests are present but skip until `validation_clips/` exists. Expected structure:

```text
validation_clips/
  bharatanatyam/reference.mp4
  bharatanatyam/good_01.mp4 ... bad_10.mp4
  kathak/reference.mp4 ...
  hip_hop/reference.mp4 ...
  freestyle/reference.mp4 ...
```

See [docs/testing.md](docs/testing.md).

## CI

GitHub Actions workflow:

- installs Python 3.11 deps
- runs backend tests with coverage
- installs frontend deps with `npm ci --legacy-peer-deps`
- runs frontend component tests
- runs Next production build

Workflow file: [.github/workflows/test.yml](.github/workflows/test.yml)

## Deployment

Frontend:

- Deploy to Vercel.
- Connect GitHub for auto-deploy on `main`.
- Hobby tier is appropriate for personal/pilot use, not commercial launch.

Backend:

- Deploy FastAPI web service and Celery worker to Render.
- `render.yaml` defines both services.
- Free Render services may cold-start after inactivity. The analysis progress UI includes a wake-up message so users understand first-run delay.

GPU:

- Modal is optional and enabled with `USE_REMOTE_GPU=true`.
- Use only after timing confirms WHAM/3D lifting is the bottleneck.

## Pilot Checklist

Before wider pilot use:

- Run `supabase db push` against the chosen Supabase projects.
- Configure Supabase Auth OAuth providers.
- Create R2 buckets and set credentials in service dashboards.
- Configure Redis/Upstash for Celery.
- Configure Vercel/Render env vars.
- Seed starter profiles with `scripts/seed_starter_profiles.py`.
- Capture real validation clips and confirm the ≥80% separation gate.
- Test camera capture on real iOS Safari and Android Chrome.
- Test low light, partial framing, bad angles, and slow networks.
- Monitor R2 storage, Supabase DB size, Render cold starts, and Modal GPU seconds.

## Known Gaps Before Public Launch

- Terms acceptance for uploaded reference videos
- Content report/takedown process
- Rate limiting for profile and attempt uploads
- Proper auth/session-aware profile ownership in the frontend
- Production-grade error states for every failed backend path
- Backups/export routine for pilot Supabase data
- Dependency upgrade pass for existing npm audit warnings, especially the pinned Next/next-pwa chain

## License and Usage Note

This repo is currently a pilot MVP scaffold. The content model assumes personal-use reference uploads. Do not deploy this publicly without terms of use, upload policy, reporting/takedown flow, and production auth/rate-limiting.
