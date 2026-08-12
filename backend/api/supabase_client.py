from __future__ import annotations

import os
from functools import lru_cache
from typing import Any


@lru_cache(maxsize=1)
def get_supabase() -> Any:
    from backend.config import get_settings

    settings = get_settings()
    url = str(settings["supabase_url"])
    key = str(settings["supabase_key"])
    if not url or not key:
        raise RuntimeError("SUPABASE_URL and SUPABASE_KEY are required for API persistence.")

    from supabase import create_client

    return create_client(url, key)
