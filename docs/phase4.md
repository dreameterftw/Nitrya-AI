# Phase 4 - PWA Plumbing

Goal: record, upload, queue async analysis, and display raw score. No visual
design work yet.

## Backend

Run locally:

```bash
pip install -r requirements.txt
uvicorn backend.api.main:app --reload
celery -A backend.api.tasks worker --loglevel=info
```

Required for real persistence/storage:

- `SUPABASE_URL`
- `SUPABASE_KEY`
- `REDIS_URL`
- `R2_ACCOUNT_ID`
- `R2_ACCESS_KEY`
- `R2_SECRET_KEY`
- `R2_BUCKET`

Without R2 env vars, uploads are copied to `.local_storage` for local plumbing
tests. Supabase env vars are required for profile/attempt persistence.

## Frontend

Run locally:

```bash
cd frontend
npm install
npm run dev
```

Set `NEXT_PUBLIC_API_BASE_URL` when the backend is not on `http://localhost:8000`.

## Exit Check

- Profile endpoint uploads reference video and caches pose sequence once.
- Attempt endpoint uploads video, creates attempt row, queues Celery job.
- Worker runs Phase 1-3 scoring and writes score/feedback to Supabase.
- Frontend records via `getUserMedia`, uploads, polls, and displays raw result.
- Deployment wiring is represented in `render.yaml`; Vercel deployment is still
  an environment/account action.
