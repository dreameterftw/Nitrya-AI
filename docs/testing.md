# Testing Strategy

## Automated Tests

- Pipeline unit tests cover Procrustes behavior, alignment, scoring, rhythm, config, and confidence gates.
- API plumbing tests cover health and local storage materialization.
- Validation regression tests are present but skip until `validation_clips/` is populated with real clips.
- Frontend unit tests cover reusable presentation components.
- GitHub Actions runs backend tests with coverage, frontend component tests, and the Next production build.

Run locally:

```bash
python -m pytest tests/ --cov=backend --cov-report=term-missing
cd frontend
npm run test
npm run build
```

## Validation Regression

Populate this structure to enable the skipped regression tests:

```text
validation_clips/
  bharatanatyam/reference.mp4
  bharatanatyam/good_01.mp4 ... bad_10.mp4
  kathak/reference.mp4 ...
  hip_hop/reference.mp4 ...
  freestyle/reference.mp4 ...
```

These checks should run whenever scoring logic changes.

## Manual Checklist

- Real iOS Safari and Android Chrome camera capture.
- Low light, partial body in frame, phone angle, and poor background tests.
- Slow network upload and polling behavior.
- PWA install behavior on iOS and Android.
- Terms acceptance, content report/takedown path, and upload error states before real users.

## Launch Gaps

- Supabase Auth UI and session handling.
- User-visible error states for failed upload/analysis/camera permission.
- Terms of use for uploaded reference videos.
- Content report/flag flow.
- Rate limiting on `/profiles` and `/attempts`.
