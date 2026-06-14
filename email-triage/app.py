"""Thin web button + summary view. One exec, run on-demand, locally.

Routes:
  /                  the button (or a 'connect Google' prompt if not authed)
  /start             button press -> ensure auth -> run triage -> show summary
  /oauth2callback    Google OAuth redirect target
  /summary           review the categorized results (proposals only; nothing sent)
"""
from __future__ import annotations

import os

from flask import Flask, redirect, render_template, request, session, url_for
from google_auth_oauthlib.flow import Flow

import config
from triage import gmail_client, store
from triage.runner import run_triage

# Allow http://localhost for the OAuth redirect during local development.
os.environ.setdefault("OAUTHLIB_INSECURE_TRANSPORT", "1")

app = Flask(__name__)
app.secret_key = config.FLASK_SECRET


def _flow() -> Flow:
    return Flow.from_client_secrets_file(
        config.CLIENT_SECRET_FILE,
        scopes=config.GMAIL_SCOPES,
        redirect_uri=config.OAUTH_REDIRECT_URI,
    )


@app.route("/")
def index():
    store.init_db()
    missing = config.missing_secrets()
    authed = gmail_client.load_credentials() is not None
    return render_template(
        "index.html", exec_id=config.EXEC_ID, authed=authed, missing=missing,
        consent=store.active_consent(),
    )


@app.route("/consent", methods=["GET", "POST"])
def consent():
    """Consent gate. The tool will not pull any mail until this is recorded."""
    store.init_db()
    existing = store.active_consent()
    error = None
    if request.method == "POST" and existing is None:
        full_name = (request.form.get("full_name") or "").strip()
        agreed = request.form.get("agree") == "on"
        if full_name and agreed:
            store.record_consent(
                full_name, config.CONSENT_POLICY_VERSION, ", ".join(config.GMAIL_SCOPES)
            )
            return redirect(url_for("start"))
        error = "Please tick the box and type your full name to consent."
    return render_template(
        "consent.html", exec_id=config.EXEC_ID,
        policy_version=config.CONSENT_POLICY_VERSION, scopes=config.GMAIL_SCOPES,
        existing=existing, error=error,
    )


@app.route("/withdraw", methods=["POST"])
def withdraw():
    """Withdraw consent. The tool refuses to run until re-consented; data is kept
    unless the exec also uses Delete all my data."""
    store.init_db()
    store.withdraw_consent()
    return redirect(url_for("consent"))


@app.route("/start")
def start():
    """Button press. Consent first, then Google auth, then the triage loop."""
    store.init_db()
    if store.active_consent() is None:
        return redirect(url_for("consent"))
    creds = gmail_client.load_credentials()
    if creds is None:
        flow = _flow()
        auth_url, state = flow.authorization_url(
            access_type="offline", include_granted_scopes="true", prompt="consent"
        )
        session["oauth_state"] = state
        return redirect(auth_url)

    summary = run_triage(creds)
    session["last_summary"] = summary
    return redirect(url_for("summary"))


@app.route("/oauth2callback")
def oauth2callback():
    store.init_db()
    if store.active_consent() is None:  # never run without recorded consent
        return redirect(url_for("consent"))
    flow = _flow()
    flow.fetch_token(authorization_response=request.url)
    gmail_client.save_credentials(flow.credentials)
    # Now that we're authed, run the triage the button was asking for.
    summary = run_triage(flow.credentials)
    session["last_summary"] = summary
    return redirect(url_for("summary"))


@app.route("/summary")
def summary():
    store.init_db()
    messages = store.load_recent(limit=200)
    # Group by category in display-priority order.
    grouped = {c: [] for c in config.CATEGORIES}
    for m in messages:
        grouped.setdefault(m["category"], []).append(m)
    return render_template(
        "summary.html",
        exec_id=config.EXEC_ID,
        run=session.get("last_summary"),
        grouped=grouped,
        categories=config.CATEGORIES,
        model=config.TRIAGE_MODEL,
    )


@app.route("/delete", methods=["GET", "POST"])
def delete():
    """One-click delete of all stored data for this exec. GET shows a confirm
    page; POST performs it (DB file + OAuth token). See governance/DATA_HANDLING.md."""
    if request.method == "GET":
        return render_template("delete.html", exec_id=config.EXEC_ID, done=None)

    result = store.delete_all_data()
    token_removed = gmail_client.remove_credentials()
    session.pop("last_summary", None)
    return render_template(
        "delete.html",
        exec_id=config.EXEC_ID,
        done={"removed": result["removed"], "token_removed": token_removed},
    )


if __name__ == "__main__":
    store.init_db()
    app.run(host="127.0.0.1", port=5000, debug=True)
