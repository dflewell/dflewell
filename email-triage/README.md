# Email Triage — True North AI

Governance-first, **button-initiated** inbox triage for executives. The exec clicks
one button; the tool pulls overnight mail, categorizes it, proposes reply drafts, and
shows a review summary. **Nothing touches the inbox unless the exec presses the button**,
and at the starting trust rung the exec reviews everything before anything is sent or moved.

> The governance wrapper is the product; this tool is the demo. See `governance/` first.

## Status
Phase 1 MVP scaffold — Assisted rung (review-everything). Built per `../memory/project-email-triage.md`.

## Architecture (this build)
- **Interface:** thin Flask web app — one button + one summary view (no terminal for the exec).
- **Mail access:** Gmail API, consumer OAuth, button-initiated (first testbed = a consumer @gmail.com).
- **Triage:** Claude API, structured-output classification into `shopping / important / client / read_later`.
- **Store:** per-executive SQLite, **email bodies encrypted at rest** (Fernet). One DB per exec, no commingling.
- **Hosting:** on-demand — runs only while the exec is using it. No always-on cloud instance.

## Categories
| Category | Meaning |
|---|---|
| `important` | Time-sensitive / needs the exec's attention |
| `client` | From or about a client — highest care, always reviewed |
| `shopping` | Receipts, promos, coupons (expiry extraction is Phase 2) |
| `read_later` | Newsletters / FYI / low-priority |

## Run it (local)
1. **Python 3.11+.** Create a venv and install deps:
   ```
   cd email-triage
   python -m venv .venv && source .venv/bin/activate
   pip install -r requirements.txt
   ```
2. **Google OAuth (consumer Gmail).** In Google Cloud Console: create an OAuth 2.0 Client ID
   (type *Web application*), add redirect URI `http://localhost:5000/oauth2callback`, download
   the client secret JSON to `email-triage/client_secret.json`. Add the exec's Gmail as a test user.
3. **Secrets.** Copy `.env.example` to `.env` and fill in:
   - `ANTHROPIC_API_KEY` — your Claude API key.
   - `EXEC_ID` — short label for whose inbox this is (drives the DB filename; no commingling).
   - `FERNET_KEY` — run `python -c "from cryptography.fernet import Fernet;print(Fernet.generate_key().decode())"` and paste the output.
4. **Start:**
   ```
   python app.py
   ```
   Open `http://localhost:5000`, click **Start my morning**, approve Google access once,
   then review the summary.

## What's stubbed vs real
- **Real:** OAuth flow, Gmail pull, Claude classification, encrypted SQLite store, the button + summary UI.
- **Stub / Phase 2:** sending drafts (they're proposed only, never sent), moving/archiving mail,
  coupon-expiry extraction, the searchable-archive UI, supervised auto-handling, scheduling.

## Per-deployment checklist
Run `../memory/deployment-intake.md` before touching any real account. Hand the exec the three
`governance/` artifacts as the consent conversation.
