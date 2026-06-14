"""Central config. Reads from .env so secrets never live in code."""
from __future__ import annotations

import os
from dotenv import load_dotenv

load_dotenv()

# --- Secrets / identity ---
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
EXEC_ID = os.environ.get("EXEC_ID", "test")
FERNET_KEY = os.environ.get("FERNET_KEY", "")
FLASK_SECRET = os.environ.get("FLASK_SECRET", "change-me")

# --- Behavior ---
# Default is Haiku 4.5 (Darrell's call, 2026-06-12) — triage is high-volume and
# simple, so the cheapest model is the right economics for a free trust-builder.
# Bump to Sonnet 4.6 or Opus 4.8 via TRIAGE_MODEL if categorization quality lags.
TRIAGE_MODEL = os.environ.get("TRIAGE_MODEL", "claude-haiku-4-5")
MAX_MESSAGES = int(os.environ.get("MAX_MESSAGES", "25"))

# --- Gmail OAuth ---
# Read/modify scope. At the Assisted rung we only ever READ + propose; the modify
# scope is present for later rungs (move/label) only if the exec opts in.
GMAIL_SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
]
CLIENT_SECRET_FILE = "client_secret.json"
TOKEN_FILE = f"token_{EXEC_ID}.json"
# Port the app runs on. 5001 avoids macOS AirPlay Receiver, which occupies 5000.
APP_PORT = int(os.environ.get("APP_PORT", "5001"))
OAUTH_REDIRECT_URI = f"http://localhost:{APP_PORT}/oauth2callback"

# --- Storage (per-exec, no commingling) ---
DB_PATH = os.path.join("data", f"triage_{EXEC_ID}.db")

# Categories the triage sorts into. Order = display priority.
CATEGORIES = ["client", "important", "shopping", "read_later"]

# Consent policy version the exec agrees to. Bump this date when the governance
# docs change materially, so consent records show exactly what was agreed to.
CONSENT_POLICY_VERSION = "2026-06-14"


def missing_secrets() -> list[str]:
    """Return names of required secrets that aren't set, for a friendly startup check."""
    missing = []
    if not ANTHROPIC_API_KEY:
        missing.append("ANTHROPIC_API_KEY")
    if not FERNET_KEY:
        missing.append("FERNET_KEY")
    return missing
