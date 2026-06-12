"""Categorize an email and propose a reply draft via the Claude API.

Uses structured outputs (a JSON schema) so the model must return one of our four
categories — no free-text parsing. Body text is truncated before sending so we
send the minimum needed to categorize (see governance/DATA_FLOW.md).
"""
import anthropic

import config

_client = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)

# Keep prompt input small and predictable: triage doesn't need the whole thread.
_BODY_CHARS = 2000

_SYSTEM = (
    "You triage an executive's inbox. For each email, assign exactly one category and, "
    "when a reply is warranted, propose a short, professional draft reply the executive "
    "could send. If no reply is needed (newsletters, receipts, FYI), leave the draft empty.\n\n"
    "Categories:\n"
    "- client: from or about a client; highest care.\n"
    "- important: time-sensitive or needs the executive's personal attention.\n"
    "- shopping: receipts, order confirmations, promotions, coupons.\n"
    "- read_later: newsletters, FYI, low-priority.\n"
)

_SCHEMA = {
    "type": "object",
    "properties": {
        "category": {"type": "string", "enum": config.CATEGORIES},
        "reason": {"type": "string"},
        "draft": {"type": "string"},
    },
    "required": ["category", "reason", "draft"],
    "additionalProperties": False,
}


def classify(*, sender: str, subject: str, body: str) -> dict:
    """Return {'category', 'reason', 'draft'} for one email."""
    user = (
        f"From: {sender}\n"
        f"Subject: {subject}\n\n"
        f"{(body or '')[:_BODY_CHARS]}"
    )
    resp = _client.messages.create(
        model=config.TRIAGE_MODEL,
        max_tokens=1024,
        system=_SYSTEM,
        messages=[{"role": "user", "content": user}],
        output_config={"format": {"type": "json_schema", "schema": _SCHEMA}},
    )
    import json

    text = next((b.text for b in resp.content if b.type == "text"), "{}")
    data = json.loads(text)
    # Defensive: never let an unexpected value through.
    if data.get("category") not in config.CATEGORIES:
        data["category"] = "read_later"
    return data
