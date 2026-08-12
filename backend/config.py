from __future__ import annotations

import os
from functools import lru_cache


@lru_cache(maxsize=1)
def get_settings() -> dict[str, str | bool]:
    env = os.getenv("APP_ENV", "development")
    return {
        "app_env": env,
        "supabase_url": os.getenv("SUPABASE_URL", ""),
        "supabase_key": os.getenv("SUPABASE_KEY", ""),
        "r2_bucket": os.getenv("R2_BUCKET", ""),
        "api_url": os.getenv("API_URL", "http://localhost:8000"),
        "redis_url": os.getenv("REDIS_URL", ""),
        "is_prod": env == "production",
    }
