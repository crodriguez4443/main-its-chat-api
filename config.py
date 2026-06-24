"""
config.py - Per-deployment configuration.

Every deployment (NY, NJ, CA, ...) ships the same code but points this
config at different env vars. Defaults match the NY baseline so the app
boots cleanly in a fresh checkout.

All values read from environment variables — set them in your shell for
local dev, or in the Railway service settings for production.
"""

import os


def _getenv_int(name: str, default: int) -> int:
    raw = os.getenv(name)
    if raw is None or raw == "":
        return default
    try:
        return int(raw)
    except ValueError:
        print(f"Warning: {name}={raw!r} is not an int; using default {default}")
        return default


def _getenv_list(name: str, default: list[str]) -> list[str]:
    raw = os.getenv(name)
    if raw is None or raw == "":
        return default
    return [item.strip() for item in raw.split(",") if item.strip()]


# --- State identity ---------------------------------------------------------
# Used for UI labels and (optionally) prompt personalization in the future.
STATE_NAME = os.getenv("STATE_NAME", "Maine")
DOT_NAME = os.getenv("DOT_NAME", "MAINEDOT")

# --- Architecture website URL -----------------------------------------------
# Citations in responses link back to this site. Every state's ITS
# architecture lives under a different project slug on consystec.com —
# this is the full base URL including the /web suffix.
#
# Example NY:  https://www.consystec.com/nystate2025/web
# Example PR:  https://consystec.com/pr2026proto/web
#
# content_processor.py reads this when generating URLs for the search index.
ARCHITECTURE_BASE_URL = "https://www.consystec.com/maine2026/web"
os.environ["ARCHITECTURE_BASE_URL"] = ARCHITECTURE_BASE_URL

# --- Gemini models ----------------------------------------------------------
# Override per deployment if cost profile differs.
GEMINI_FLASH_MODEL = os.getenv("GEMINI_FLASH_MODEL", "gemini-3-flash-preview")
GEMINI_PRO_MODEL = os.getenv("GEMINI_PRO_MODEL", "gemini-3.1-pro-preview")
# Fallback used when GEMINI_PRO_MODEL returns 503 after retries.
GEMINI_PRO_FALLBACK_MODEL = os.getenv("GEMINI_PRO_FALLBACK_MODEL", "gemini-2.5-pro")

# --- Session limits ---------------------------------------------------------
MAX_QUERIES_PER_DAY = _getenv_int("MAX_QUERIES_PER_DAY", 10)
MAX_QUERIES_PER_CONVERSATION = _getenv_int("MAX_QUERIES_PER_CONVERSATION", 3)
SESSION_CLEANUP_HOURS = _getenv_int("SESSION_CLEANUP_HOURS", 48)

# --- Storage ----------------------------------------------------------------
# On Railway, point this at a mounted volume (e.g. /data/sessions.db).
DATABASE_PATH = os.getenv("DATABASE_PATH", "./sessions.db")

# --- HTTP -------------------------------------------------------------------
# Comma-separated in env: CORS_ORIGINS="https://dot.ny.gov,https://example.org"
CORS_ORIGINS = _getenv_list("CORS_ORIGINS", ["*"])
PORT = _getenv_int("PORT", 8001)
