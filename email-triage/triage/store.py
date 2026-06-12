"""Per-executive SQLite store. Email bodies/subjects/drafts are encrypted at rest
with Fernet; metadata used for de-duplication and the summary is left queryable.

One DB file per exec (config.DB_PATH) — no commingling. See governance/DATA_HANDLING.md.
"""
import os
import sqlite3
from cryptography.fernet import Fernet

import config


def _fernet() -> Fernet:
    if not config.FERNET_KEY:
        raise RuntimeError("FERNET_KEY is not set — cannot encrypt at rest. See .env.example.")
    return Fernet(config.FERNET_KEY.encode())


def init_db() -> None:
    """Create the data dir + table if needed. Safe to call on every startup."""
    os.makedirs(os.path.dirname(config.DB_PATH), exist_ok=True)
    with sqlite3.connect(config.DB_PATH) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS messages (
                gmail_id     TEXT PRIMARY KEY,   -- de-dupe: never re-process the same message
                received_at  TEXT,               -- ISO date (metadata, not sensitive)
                sender       TEXT,               -- metadata
                category     TEXT,               -- client/important/shopping/read_later
                subject_enc  BLOB,               -- encrypted
                body_enc     BLOB,               -- encrypted
                draft_enc    BLOB,               -- encrypted proposed reply (may be empty)
                processed_at TEXT DEFAULT (datetime('now'))
            )
            """
        )


def already_seen(gmail_id: str) -> bool:
    with sqlite3.connect(config.DB_PATH) as conn:
        row = conn.execute(
            "SELECT 1 FROM messages WHERE gmail_id = ?", (gmail_id,)
        ).fetchone()
    return row is not None


def save_message(*, gmail_id, received_at, sender, category, subject, body, draft) -> None:
    f = _fernet()
    with sqlite3.connect(config.DB_PATH) as conn:
        conn.execute(
            """
            INSERT OR REPLACE INTO messages
                (gmail_id, received_at, sender, category, subject_enc, body_enc, draft_enc)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                gmail_id,
                received_at,
                sender,
                category,
                f.encrypt((subject or "").encode()),
                f.encrypt((body or "").encode()),
                f.encrypt((draft or "").encode()),
            ),
        )


def delete_all_data() -> dict:
    """Delete this executive's entire stored history (the DB file). Backs the
    deletion promise in governance/DATA_HANDLING.md item 1. Returns what was removed.
    """
    removed = []
    if os.path.exists(config.DB_PATH):
        os.remove(config.DB_PATH)
        removed.append(config.DB_PATH)
    return {"removed": removed}


def load_recent(limit: int = 100) -> list[dict]:
    """Decrypt and return the most recently processed messages for the summary view."""
    f = _fernet()
    with sqlite3.connect(config.DB_PATH) as conn:
        rows = conn.execute(
            """
            SELECT gmail_id, received_at, sender, category, subject_enc, body_enc, draft_enc
            FROM messages ORDER BY processed_at DESC LIMIT ?
            """,
            (limit,),
        ).fetchall()

    out = []
    for gmail_id, received_at, sender, category, subj_enc, body_enc, draft_enc in rows:
        out.append(
            {
                "gmail_id": gmail_id,
                "received_at": received_at,
                "sender": sender,
                "category": category,
                "subject": f.decrypt(subj_enc).decode() if subj_enc else "",
                "body": f.decrypt(body_enc).decode() if body_enc else "",
                "draft": f.decrypt(draft_enc).decode() if draft_enc else "",
            }
        )
    return out
