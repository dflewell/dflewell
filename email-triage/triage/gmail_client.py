"""Gmail access via consumer OAuth, button-initiated.

The OAuth *flow* (redirect + callback) lives in app.py; this module just turns a
stored token into a Gmail service and pulls overnight unread messages.
"""
from __future__ import annotations

import base64
from email.utils import parsedate_to_datetime

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

import config


def load_credentials() -> Credentials | None:
    """Load saved creds; refresh if expired. Returns None if the exec hasn't authed yet."""
    try:
        creds = Credentials.from_authorized_user_file(config.TOKEN_FILE, config.GMAIL_SCOPES)
    except (FileNotFoundError, ValueError):
        return None
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
        save_credentials(creds)
    return creds if creds and creds.valid else None


def save_credentials(creds: Credentials) -> None:
    with open(config.TOKEN_FILE, "w") as f:
        f.write(creds.to_json())


def remove_credentials() -> bool:
    """Delete the stored OAuth token so the tool can no longer reach Gmail.
    The exec can also revoke independently in their Google security settings."""
    import os

    if os.path.exists(config.TOKEN_FILE):
        os.remove(config.TOKEN_FILE)
        return True
    return False


def _service(creds: Credentials):
    return build("gmail", "v1", credentials=creds, cache_discovery=False)


def _header(headers: list[dict], name: str) -> str:
    for h in headers:
        if h.get("name", "").lower() == name.lower():
            return h.get("value", "")
    return ""


def _extract_body(payload: dict) -> str:
    """Pull plain-text body from a Gmail message payload (handles multipart)."""
    def decode(data: str) -> str:
        return base64.urlsafe_b64decode(data.encode()).decode("utf-8", errors="replace")

    if payload.get("mimeType") == "text/plain" and payload.get("body", {}).get("data"):
        return decode(payload["body"]["data"])

    for part in payload.get("parts", []) or []:
        if part.get("mimeType") == "text/plain" and part.get("body", {}).get("data"):
            return decode(part["body"]["data"])
        # one level of nesting (multipart/alternative inside multipart/mixed)
        for sub in part.get("parts", []) or []:
            if sub.get("mimeType") == "text/plain" and sub.get("body", {}).get("data"):
                return decode(sub["body"]["data"])
    # fall back to the snippet if no plain-text part was found
    return ""


def fetch_overnight_unread(creds: Credentials, limit: int) -> list[dict]:
    """Return up to `limit` unread messages as dicts: id, received_at, sender, subject, body."""
    svc = _service(creds)
    listing = (
        svc.users()
        .messages()
        .list(userId="me", q="is:unread", maxResults=limit)
        .execute()
    )

    messages = []
    for ref in listing.get("messages", []):
        full = (
            svc.users()
            .messages()
            .get(userId="me", id=ref["id"], format="full")
            .execute()
        )
        headers = full.get("payload", {}).get("headers", [])
        date_raw = _header(headers, "Date")
        try:
            received_at = parsedate_to_datetime(date_raw).isoformat() if date_raw else ""
        except (TypeError, ValueError):
            received_at = ""
        body = _extract_body(full.get("payload", {})) or full.get("snippet", "")
        messages.append(
            {
                "id": full["id"],
                "received_at": received_at,
                "sender": _header(headers, "From"),
                "subject": _header(headers, "Subject"),
                "body": body,
            }
        )
    return messages
