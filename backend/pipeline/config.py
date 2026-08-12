from __future__ import annotations

import os
from copy import deepcopy
from functools import lru_cache
from typing import Any

GENRE_CONFIGS: dict[str, dict[str, Any]] = {
    "bharatanatyam": {
        "genre": "bharatanatyam",
        "posture_weight": 0.6,
        "rhythm_weight": 0.4,
        "spatial_tolerance": "strict",
        "form_scale": 0.35,
        "active_submodels": ["keyframe_matcher", "mudra_layer"],
        "keyframes": [12, 45, 78, 110],
    },
    "kathak": {
        "genre": "kathak",
        "posture_weight": 0.55,
        "rhythm_weight": 0.45,
        "spatial_tolerance": "strict",
        "form_scale": 0.35,
        "active_submodels": ["keyframe_matcher"],
        "keyframes": [10, 40, 70],
    },
    "hip_hop": {
        "genre": "hip_hop",
        "posture_weight": 0.3,
        "rhythm_weight": 0.7,
        "spatial_tolerance": "loose",
        "form_scale": 0.5,
        "active_submodels": [],
        "keyframes": [],
    },
    "freestyle": {
        "genre": "freestyle",
        "posture_weight": 0.3,
        "rhythm_weight": 0.7,
        "spatial_tolerance": "loose",
        "form_scale": 0.5,
        "active_submodels": [],
        "keyframes": [],
    },
}


@lru_cache(maxsize=1)
def _supabase_client() -> Any | None:
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    if not url or not key:
        return None

    try:
        from supabase import create_client
    except ImportError as exc:
        raise RuntimeError(
            "supabase is required when SUPABASE_URL/SUPABASE_KEY are set. Install "
            "dependencies with `pip install -r backend/pipeline/requirements.txt`."
        ) from exc
    return create_client(url, key)


def get_genre_config(genre: str) -> dict[str, Any]:
    """Load genre config from Supabase when configured, otherwise use local defaults."""
    client = _supabase_client()
    if client is not None:
        result = client.table("genre_configs").select("*").eq("genre", genre).single().execute()
        if not result.data:
            raise ValueError(f"No genre config found for {genre!r}.")
        return result.data

    try:
        return deepcopy(GENRE_CONFIGS[genre])
    except KeyError as exc:
        raise ValueError(f"Unknown genre {genre!r}.") from exc
