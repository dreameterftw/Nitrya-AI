from __future__ import annotations

from backend.api.supabase_client import get_supabase

STARTER_PROFILES = [
    {"id": "starter-bharatanatyam", "dancer_name": "Bharatanatyam Starter", "genre": "bharatanatyam"},
    {"id": "starter-kathak", "dancer_name": "Kathak Starter", "genre": "kathak"},
    {"id": "starter-hip-hop", "dancer_name": "Hip-Hop Starter", "genre": "hip_hop"},
    {"id": "starter-freestyle", "dancer_name": "Freestyle Starter", "genre": "freestyle"},
]


def main() -> int:
    supabase = get_supabase()
    for profile in STARTER_PROFILES:
        supabase.table("profiles").upsert(profile).execute()
    print(f"Seeded {len(STARTER_PROFILES)} starter profiles.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
