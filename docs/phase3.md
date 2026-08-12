# Phase 3 - Personalization / Genre Config

Goal: move scoring weights, tolerances, and active submodels out of scoring code
and into genre-level data.

## Supabase Config

Migration: `supabase/migrations/0002_genre_config.sql`

The table is keyed by locked Phase 0 genres:

- `bharatanatyam`
- `kathak`
- `hip_hop`
- `freestyle`

Run after linking the Supabase project:

```bash
supabase db push
```

The seeded `form_scale` values are placeholders. Replace them with calibrated
values from Phase 1/2 validation distributions before claiming Phase 3 exit.

## Pipeline Usage

`get_genre_config(genre)` loads from Supabase when `SUPABASE_URL` and
`SUPABASE_KEY` are present. Without those env vars, it uses local defaults so
tests and offline validation still run.

`score_attempt_with_config(...)` returns:

- `total_score`, higher is better
- `form_component`
- `bas`
- `active_submodels`
- `keyframes_used`
- optional `keyframe_accuracy`
- optional `mudra_layer_available`

## Exit Check

- `genre_configs` table live in Supabase with all 4 genres populated
- Config-driven scoring works end-to-end
- Combined weighted score re-validates at ≥80% pairwise separation
- Keyframe accuracy runs for Bharatanatyam/Kathak
- Mudra layer flag exists for Bharatanatyam, with real detection deferred
