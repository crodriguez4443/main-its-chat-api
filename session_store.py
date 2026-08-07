"""
session_store.py - SQLite-backed session and exchange persistence.

Replaces the prior in-memory `sessions` dict and the JSONL-based
conversation_logger. Chosen for Railway deployments where the default
filesystem is ephemeral: the SQLite file must live on a mounted
persistent volume (configure via the DATABASE_PATH env var).

Tables:
  sessions   - one row per session (including in-flight conversation history)
  exchanges  - one row per user query/assistant response pair (audit log)

The module exposes dict-shaped session objects so existing call sites
in main.py continue to work with minimal changes: reads go through
get_or_create_session(), writes go through save_session(), and exchange
logging goes through log_exchange().
"""

import json
import os
import sqlite3
import uuid
from datetime import datetime, timedelta
from threading import Lock
from typing import Optional, Tuple

import config

DATABASE_PATH = config.DATABASE_PATH

# Serialize writes to avoid "database is locked" under FastAPI's thread pool.
# Reads still run concurrently thanks to WAL mode.
_write_lock = Lock()


def _connect() -> sqlite3.Connection:
    conn = sqlite3.connect(DATABASE_PATH, timeout=10.0, isolation_level=None)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=NORMAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def init_db() -> None:
    """Create tables if they don't exist. Call once at startup."""
    db_dir = os.path.dirname(os.path.abspath(DATABASE_PATH))
    if db_dir and not os.path.exists(db_dir):
        os.makedirs(db_dir, exist_ok=True)

    with _write_lock, _connect() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                session_id TEXT PRIMARY KEY,
                user_role TEXT,
                query_count INTEGER NOT NULL DEFAULT 0,
                conversation_query_count INTEGER NOT NULL DEFAULT 0,
                exchange_count INTEGER NOT NULL DEFAULT 0,
                conversation_history TEXT NOT NULL DEFAULT '[]',
                created_at TEXT NOT NULL,
                last_activity TEXT NOT NULL
            )
        """)
        # Cheap migration for DBs created before exchange_count existed.
        cols = {r["name"] for r in conn.execute("PRAGMA table_info(sessions)").fetchall()}
        if "exchange_count" not in cols:
            conn.execute("ALTER TABLE sessions ADD COLUMN exchange_count INTEGER NOT NULL DEFAULT 0")
        conn.execute("""
            CREATE TABLE IF NOT EXISTS exchanges (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                exchange_number INTEGER NOT NULL,
                timestamp TEXT NOT NULL,
                user_role TEXT,
                user_query TEXT NOT NULL,
                assistant_response TEXT NOT NULL,
                conversation_context_length INTEGER,
                chunks_retrieved INTEGER,
                response_time_ms INTEGER,
                FOREIGN KEY (session_id) REFERENCES sessions(session_id)
            )
        """)
        conn.execute("CREATE INDEX IF NOT EXISTS idx_exchanges_session ON exchanges(session_id)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_sessions_activity ON sessions(last_activity)")
    print(f"Session store initialized at {DATABASE_PATH}")


def _row_to_session(row: sqlite3.Row) -> dict:
    return {
        "session_id": row["session_id"],
        "user_role": row["user_role"],
        "query_count": row["query_count"],
        "conversation_query_count": row["conversation_query_count"],
        "exchange_count": row["exchange_count"],
        "conversation_history": json.loads(row["conversation_history"]),
        "created_at": datetime.fromisoformat(row["created_at"]),
        "last_activity": datetime.fromisoformat(row["last_activity"]),
    }


def get_session(session_id: str) -> Optional[dict]:
    with _connect() as conn:
        row = conn.execute(
            "SELECT * FROM sessions WHERE session_id = ?", (session_id,)
        ).fetchone()
    return _row_to_session(row) if row else None


def get_or_create_session(
    session_id: Optional[str],
    cleanup_hours: int,
) -> Tuple[str, dict]:
    """Get existing session or create a new one. Returns (session_id, session_data)."""
    cleanup_old_sessions(cleanup_hours)
    reset_midnight_sessions()

    if session_id:
        existing = get_session(session_id)
        if existing:
            now = datetime.now()
            existing["last_activity"] = now
            with _write_lock, _connect() as conn:
                conn.execute(
                    "UPDATE sessions SET last_activity = ? WHERE session_id = ?",
                    (now.isoformat(), session_id),
                )
            return session_id, existing

    new_id = str(uuid.uuid4())
    now = datetime.now()
    session_data = {
        "session_id": new_id,
        "user_role": None,
        "query_count": 0,
        "conversation_query_count": 0,
        "exchange_count": 0,
        "conversation_history": [],
        "created_at": now,
        "last_activity": now,
    }
    with _write_lock, _connect() as conn:
        conn.execute(
            """INSERT INTO sessions
                 (session_id, user_role, query_count, conversation_query_count,
                  exchange_count, conversation_history, created_at, last_activity)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (new_id, None, 0, 0, 0, "[]", now.isoformat(), now.isoformat()),
        )
    print(f"Created new session: {new_id}")
    return new_id, session_data


def save_session(session_data: dict) -> None:
    """Persist in-memory session mutations back to SQLite."""
    with _write_lock, _connect() as conn:
        conn.execute(
            """UPDATE sessions SET
                 user_role = ?,
                 query_count = ?,
                 conversation_query_count = ?,
                 exchange_count = ?,
                 conversation_history = ?,
                 last_activity = ?
               WHERE session_id = ?""",
            (
                session_data.get("user_role"),
                session_data["query_count"],
                session_data["conversation_query_count"],
                session_data.get("exchange_count", 0),
                json.dumps(session_data["conversation_history"], ensure_ascii=False),
                session_data["last_activity"].isoformat(),
                session_data["session_id"],
            ),
        )


def cleanup_old_sessions(cleanup_hours: int) -> None:
    cutoff = (datetime.now() - timedelta(hours=cleanup_hours)).isoformat()
    with _write_lock, _connect() as conn:
        conn.execute(
            "DELETE FROM exchanges WHERE session_id IN "
            "(SELECT session_id FROM sessions WHERE last_activity < ?)",
            (cutoff,),
        )
        cursor = conn.execute(
            "DELETE FROM sessions WHERE last_activity < ?", (cutoff,)
        )
        if cursor.rowcount:
            print(f"Cleaned up {cursor.rowcount} old sessions (inactive > {cleanup_hours}h)")


def reset_midnight_sessions() -> None:
    """Reset daily query_count for sessions created before today's midnight."""
    now = datetime.now()
    midnight = datetime(now.year, now.month, now.day, 0, 0, 0).isoformat()
    with _write_lock, _connect() as conn:
        cursor = conn.execute(
            """UPDATE sessions
                 SET query_count = 0, created_at = ?
               WHERE created_at < ?""",
            (now.isoformat(), midnight),
        )
        if cursor.rowcount:
            print(f"Reset daily count on {cursor.rowcount} sessions (pre-midnight)")


def log_exchange(
    session_id: str,
    exchange_number: int,
    user_role: str,
    user_query: str,
    assistant_response: str,
    conversation_context_length: int,
    chunks_retrieved: int,
    response_time_ms: int,
) -> None:
    """Append one audit-log row. Errors are caught so they never fail a request.

    exchange_number is passed in (typically session_data['exchange_count'] after
    the caller has incremented it) so we avoid an O(n) COUNT per request.
    """
    try:
        with _write_lock, _connect() as conn:
            conn.execute(
                """INSERT INTO exchanges
                     (session_id, exchange_number, timestamp, user_role,
                      user_query, assistant_response, conversation_context_length,
                      chunks_retrieved, response_time_ms)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    session_id,
                    exchange_number,
                    datetime.utcnow().isoformat() + "Z",
                    user_role,
                    user_query,
                    assistant_response,
                    conversation_context_length,
                    chunks_retrieved,
                    response_time_ms,
                ),
            )
        print(f"Logged exchange {exchange_number} for session {session_id[:8]}...")
    except Exception as e:
        print(f"ERROR: Failed to log exchange: {e}")


def reset_conversation(session_id: str, clear_role: bool = False) -> Optional[dict]:
    """Clear conversation state on the session row. Returns updated session or None."""
    session = get_session(session_id)
    if session is None:
        return None
    session["conversation_history"] = []
    session["conversation_query_count"] = 0
    session["last_activity"] = datetime.now()
    if clear_role:
        session["user_role"] = None
    save_session(session)
    return session


def get_total_exchanges() -> int:
    with _connect() as conn:
        row = conn.execute("SELECT COUNT(*) AS n FROM exchanges").fetchone()
    return row["n"] if row else 0


def get_unique_sessions() -> int:
    with _connect() as conn:
        row = conn.execute("SELECT COUNT(*) AS n FROM sessions").fetchone()
    return row["n"] if row else 0


# ---------------------------------------------------------------------------
# Admin data helpers (called by /api/data/* endpoints in main.py)
# ---------------------------------------------------------------------------

def parse_range(
    range_: str,
    date_from: Optional[str],
    date_to: Optional[str],
) -> Tuple[str, str]:
    """Return (start, end) ISO strings for the requested range.

    Custom from/to are used as-is. Preset ranges are relative to UTC now.
    Timestamps in the exchanges table are stored as UTC with a 'Z' suffix so
    string comparison works correctly as long as all values use the same format.
    """
    now = datetime.utcnow()
    if date_from and date_to:
        return date_from, date_to
    offsets = {"day": 1, "week": 7, "month": 30, "year": 365}
    days = offsets.get(range_, 1)
    start = now - timedelta(days=days)
    return start.isoformat() + "Z", now.isoformat() + "Z"


def get_stats(start: str, end: str) -> dict:
    """Summary counts for exchanges whose timestamp falls in [start, end]."""
    with _connect() as conn:
        total_sessions = conn.execute(
            "SELECT COUNT(DISTINCT session_id) AS n FROM exchanges"
            " WHERE timestamp >= ? AND timestamp <= ?",
            (start, end),
        ).fetchone()["n"]
        agg = conn.execute(
            "SELECT COUNT(*) AS n, AVG(response_time_ms) AS avg_rt"
            " FROM exchanges WHERE timestamp >= ? AND timestamp <= ?",
            (start, end),
        ).fetchone()
        role_rows = conn.execute(
            "SELECT user_role, COUNT(*) AS n FROM exchanges"
            " WHERE timestamp >= ? AND timestamp <= ? GROUP BY user_role",
            (start, end),
        ).fetchall()
    exchanges_by_role = {(r["user_role"] or "unknown"): r["n"] for r in role_rows}
    return {
        "start": start,
        "end": end,
        "total_sessions": total_sessions,
        "total_exchanges": agg["n"],
        "avg_response_time_ms": agg["avg_rt"],
        "exchanges_by_role": exchanges_by_role,
    }


def count_exchanges(start: str, end: str, role: Optional[str] = None) -> int:
    """Count exchanges in [start, end], optionally filtered by role."""
    with _connect() as conn:
        if role:
            row = conn.execute(
                "SELECT COUNT(*) AS n FROM exchanges"
                " WHERE timestamp >= ? AND timestamp <= ? AND user_role = ?",
                (start, end, role),
            ).fetchone()
        else:
            row = conn.execute(
                "SELECT COUNT(*) AS n FROM exchanges"
                " WHERE timestamp >= ? AND timestamp <= ?",
                (start, end),
            ).fetchone()
    return row["n"] if row else 0


def list_exchanges(
    start: str,
    end: str,
    role: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
) -> list:
    """Paginated list of exchanges, newest first."""
    with _connect() as conn:
        if role:
            rows = conn.execute(
                "SELECT * FROM exchanges"
                " WHERE timestamp >= ? AND timestamp <= ? AND user_role = ?"
                " ORDER BY timestamp DESC LIMIT ? OFFSET ?",
                (start, end, role, limit, offset),
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT * FROM exchanges"
                " WHERE timestamp >= ? AND timestamp <= ?"
                " ORDER BY timestamp DESC LIMIT ? OFFSET ?",
                (start, end, limit, offset),
            ).fetchall()
    return [dict(r) for r in rows]


def iter_exchanges(start: str, end: str, role: Optional[str] = None):
    """Yield exchange rows in ascending timestamp order (for streaming export)."""
    with _connect() as conn:
        if role:
            rows = conn.execute(
                "SELECT * FROM exchanges"
                " WHERE timestamp >= ? AND timestamp <= ? AND user_role = ?"
                " ORDER BY timestamp ASC",
                (start, end, role),
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT * FROM exchanges"
                " WHERE timestamp >= ? AND timestamp <= ?"
                " ORDER BY timestamp ASC",
                (start, end),
            ).fetchall()
    for row in rows:
        yield dict(row)


def get_session_with_history(session_id: str) -> Optional[dict]:
    """Full session record with ISO string timestamps, for the detail endpoint."""
    session = get_session(session_id)
    if session is None:
        return None
    return {
        "session_id": session["session_id"],
        "user_role": session["user_role"],
        "query_count": session["query_count"],
        "conversation_query_count": session["conversation_query_count"],
        "exchange_count": session["exchange_count"],
        "created_at": session["created_at"].isoformat(),
        "last_activity": session["last_activity"].isoformat(),
        "conversation_history": session["conversation_history"],
    }
