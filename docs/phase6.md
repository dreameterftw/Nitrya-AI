# Phase 6 - Dual-Theme UI Polish

Goal: wrap the proven backend in Western and Indian visual worlds without
touching scoring logic.

## Theme Architecture

- `frontend/lib/theme-context.tsx` stores `western` or `indian` client-side.
- `ThemeProvider` persists the choice in `localStorage`.
- `frontend/tailwind.config.js` records the design token palette.
- `frontend/app/globals.css` applies the same tokens as CSS variables.

The component tree is shared. Results use one `ResultsView`; only theme-specific
detail blocks branch:

- Indian: keyframe accuracy and mudra readiness
- Western: flow/energy from beat alignment

## Views

- `/onboarding`: choose and persist theme
- `/discover`: Western vertical profile browser or Indian instructional list
- `/record`: unchanged plumbing flow, now inside theme shell
- `/results/[taskId]`: themed result display using the same fetched score data

## Verification

Frontend production build:

```bash
cd frontend
npm run build
```

Backend/pipeline tests:

```bash
python -m pytest tests -p no:cacheprovider --basetemp=.tmp\pytest
```

Known dependency note: the existing `next-pwa`/Next dependency chain still reports
npm audit warnings. Address that in a dedicated dependency upgrade pass so the UI
polish commit stays scoped to presentation.
