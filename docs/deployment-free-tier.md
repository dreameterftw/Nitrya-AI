# Deployment, Storage, and Auth

This project can run through pilot on free tiers, but not all "free" pieces behave
the same way.

## Deployment

- Frontend: Vercel Hobby is fine for personal pilots. Move to a paid plan before
  commercial/paying-user use.
- Backend: Render free services can spin down after inactivity. The first API or
  worker request after idle time may take 30-60 seconds. The analysis UI includes
  a wake-up message so this reads as expected delay, not a broken pipeline.
- GPU inference: Modal remains usage-billed and scales to zero. Keep
  `USE_REMOTE_GPU` off for dev and enable it only for pilot traffic once timing
  confirms WHAM is the bottleneck.

## Storage

- Keep video files in Cloudflare R2. The 10GB free tier is useful, but short video
  attempts can fill it faster than database rows.
- Supabase Storage is smaller and should stay minimal unless there is a specific
  reason to use it.

## Auth and Database

- Supabase Auth is generous enough for pilot scale.
- Supabase free projects are limited. Instead of assuming separate free
  `dev`, `staging`, and `prod` projects, use two active projects:
  `nritya-dev-staging` and `nritya-prod`.
- Free projects may pause after inactivity, which is tolerable for dev/staging
  but not for anything you rely on during a scheduled pilot.
- Free tier has no automatic backups. Export pilot data before wider testing.

## Environment Plan

- Development/preview: shared Supabase project and `nritya-videos-dev`.
- Production/pilot: separate Supabase project and `nritya-videos-prod`.
- Vercel should map preview/development env vars to the shared dev/staging
  backend and production env vars to prod.

## Before Pilot

- Confirm Render cold starts are acceptable with the UI warning.
- Monitor R2 storage usage weekly.
- Export Supabase data manually before real pilot sessions.
- Add rate limiting before opening uploads beyond the initial pilot group.
