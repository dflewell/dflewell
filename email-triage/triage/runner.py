"""The MVP loop: pull -> categorize -> propose -> store. Called when the exec
presses the button. Read-only against Gmail; proposes drafts but sends nothing.
"""
from . import gmail_client, classifier, store
import config


def run_triage(creds) -> dict:
    """Process overnight unread mail. Returns a small summary for the UI."""
    store.init_db()
    messages = gmail_client.fetch_overnight_unread(creds, config.MAX_MESSAGES)

    counts = {c: 0 for c in config.CATEGORIES}
    processed = 0
    skipped = 0

    for msg in messages:
        if store.already_seen(msg["id"]):
            skipped += 1
            continue
        result = classifier.classify(
            sender=msg["sender"], subject=msg["subject"], body=msg["body"]
        )
        store.save_message(
            gmail_id=msg["id"],
            received_at=msg["received_at"],
            sender=msg["sender"],
            category=result["category"],
            subject=msg["subject"],
            body=msg["body"],
            draft=result.get("draft", ""),
        )
        counts[result["category"]] += 1
        processed += 1

    return {
        "pulled": len(messages),
        "processed": processed,
        "skipped_already_seen": skipped,
        "counts": counts,
    }
