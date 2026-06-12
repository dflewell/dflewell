"""Central config. Reads from .env so secrets never live in code."""
import os
from dotenv import load_dotenv

load_dotenv()

# --- Secrets / identity ---
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
EXEC_ID = os.environ.get("EXEC_ID", "test")
FERNET_KEY = os.environ.get("FERNET_KEY", "")
FLASK_SECRET = os.environ.get("FLASK_SECRET", "change-me")

# --- Behavior ---
# Default to the highest-quality model. Triage is high-volume, so this is a real
# cost lever — see .env.example for cheaper options (Sonnet 4.6 / Haiku 4.5).
TRIAGE_MODEL = os.environ.get("TRIAGE_MODEL", "claude-opus-4-8")
MAX_MESSAGES = int(os.environ.get("MAX_MESSAGES", "25"))

# --- Gmail OAuth ---
# Read/modify scope. At the Assisted rung we only ever READ + propose; the modify
# scope is present for later rungs (move/label) only if the exec opts in.
GMAIL_SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
]
CLIENT_SECRET_FILE = "client_secret.json"
TOKEN_FILE = f"token_{EXEC_ID}.json"
OAUTH_REDIRECT_URI = "http://localhost:5000/oauth2callback"

# --- Storage (per-exec, no commingling) ---
DB_PATH = os.path.join("data", f"triage_{EXEC_ID}.db")

# Categories the triage sorts into. Order = display priority.
CATEGORIES = ["client", "important", "shopping", "read_later"]


def missing_secrets() -> list[str]:
    """Return names of required secrets that aren't set, for a friendly startup check."""
    missing = []
    if not ANTHROPIC_API_KEY:
        missing.append("ANTHROPIC_API_KEY")
    if not FERNET_KEY:
        missing.append("FERNET_KEY")
    return missing
