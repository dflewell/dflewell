"""Thin web button + summary view. One exec, run on-demand, locally.

Routes:
  /                  the button (or a 'connect Google' prompt if not authed)
  /start             button press -> ensure auth -> run triage -> show summary
  /oauth2callback    Google OAuth redirect target
  /summary           review the categorized results (proposals only; nothing sent)
"""
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
    missing = config.missing_secrets()
    authed = gmail_client.load_credentials() is not None
    return render_template(
        "index.html", exec_id=config.EXEC_ID, authed=authed, missing=missing
    )


@app.route("/start")
def start():
    """Button press. If not authed, send to Google; otherwise run the triage loop."""
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


if __name__ == "__main__":
    store.init_db()
    app.run(host="127.0.0.1", port=5000, debug=True)
