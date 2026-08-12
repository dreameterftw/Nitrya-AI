# Environment Configuration

Use env files locally, but never commit real values.

Committed examples:

- `.env.example` for backend/API/worker
- `frontend/.env.example` for the PWA

Recommended free-tier layout:

- `development` and `staging`: one shared Supabase project, separate starter/test
  data conventions, and an R2 dev bucket.
- `production`: separate Supabase project and R2 prod bucket.

This avoids depending on three active Supabase free projects.

Required backend variables:

```text
APP_ENV=
SUPABASE_URL=
SUPABASE_KEY=
R2_ACCOUNT_ID=
R2_ACCESS_KEY=
R2_SECRET_KEY=
R2_BUCKET=
REDIS_URL=
```

Required frontend variables:

```text
NEXT_PUBLIC_API_BASE_URL=
NEXT_PUBLIC_SUPABASE_URL=
NEXT_PUBLIC_SUPABASE_ANON_KEY=
```
