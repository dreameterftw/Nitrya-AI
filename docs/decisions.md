# Nritya AI - Locked Decisions (Phase 0)

Date: 2026-08-12

## Genres (MVP)
- Indian classical: Bharatanatyam, Kathak
- Western: hip-hop, freestyle
- Folk: dropped for MVP, revisit post-Phase 5

## Reference content
- User-created profiles (influencers/dancers of their choice)
- One reference video per profile for MVP
- Personal-use only, not redistributed, not shown to other users

## Acceptance criteria (Phase 1 exit gate)
"On a hand-labeled set of 10 good + 10 bad takes per genre (across all 4 genres), the pipeline's score correctly ranks good above bad in ≥80% of pairs."

## Infra
- DB/Auth/Storage: Supabase (chosen over Firebase - relational fit, open-source)
- Object storage: Cloudflare R2
- Compute (dev): Google Colab free T4
- Frontend hosting: Vercel
- API hosting: Render/Railway free tier
