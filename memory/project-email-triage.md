# Project: Email Overload / Assisted Inbox Triage

_Last updated: 2026-06-12 — Status: scoping (MVP definition next)_

## Business context (why this exists)
- Vehicle for **True North AI LLC** — the user's consulting practice (governance focus).
- This is a **showcase / trust-building / executive-bonding** engagement, not a product line.
- Likely **unpaid** at first; the relationship and demonstrated discipline are the return.
- Volume: **3–5 deployments per year**, each **manually deployed one-on-one** per executive.
- Explicitly **NOT** a multi-tenant SaaS.

## Core reframe
**The governance wrapper is the product; the email tool is the demo.** Build it to *generate*
governance artifacts (data-flow diagram; "what we store / where / how long / how to delete"
sheet; consent script). These triple as the consent conversation, the trust moment, and
reusable marketing collateral.

## Problem
Inbox overload; years of history; fear of deleting; time-sensitive items (e.g. coupons with
expiry) getting lost; poor native search; inability to keep up. Target users: executives.

## DONE looks like
- Executive stops the relentless manual morning triage.
- Complete, searchable email history in a durable store, independent of the mail app.
- Incoming mail categorized (shopping / important / client / read-later); reply drafts proposed.
- Inbox reaches "zero" without manual sorting; clean weekly start — no data deleted (archive, not delete).

## Execution model (DECIDED)
- **Human-initiated "morning button," not unattended.** Exec clicks to start their day; the tool
  pulls overnight mail, categorizes, proposes drafts, shows a summary for review.
- Real goal is **relief from manual triage labor**, not autonomy — the button delivers that while
  keeping the exec in control. Strong governance line: "nothing touches your inbox unless you press it."
- **Trust ladder** (pitch this explicitly):
  1. Assisted — exec clicks, agent proposes, exec reviews everything before send/move. START HERE.
  2. Supervised — agent auto-handles safe categories (shopping, read-later); drafts/client mail still reviewed.
  3. Automated — scheduled runs, minimal review. Only if the client asks.

## Architecture (DECIDED / leaning)
- **Build artifact:** Claude Code codebase, configured & deployed per client. ✅
- **Delivery:** consultant manually deploys per exec; per-client isolation. ✅
- **Data store:** local **SQLite, one isolated DB per executive**, encrypted at rest. No commingling.
- **Inference:** email content → **Claude API** for triage. Document the data flow precisely.
- **Hosting:** on-demand (button-triggered) — no always-on cloud instance required.
- **Interface:** a thin **trigger + result-summary** surface is now in Phase 1 (one button, one clean
  view, no terminal for the exec). Full searchable-archive UI is later.

## Gmail access architecture (decision gate per deployment)
- **First intake question: Workspace (custom domain) or consumer @gmail.com?**
- **Workspace (most execs):** service account with **domain-wide delegation**, authorized by the
  client's own Workspace admin for scoped read/modify. No verification, no CASA, persistent,
  admin-revocable (great governance story). PREFERRED.
- **Consumer Gmail:** consumer OAuth. Testing mode = no CASA but refresh tokens expire ~7 days
  (would break unattended jobs — fine here because exec is present to re-auth at click-time).
  Production + restricted Gmail scopes = verification + CASA (cost/time; not worth it for a free
  trust-builder). So: keep it button-initiated; avoid CASA.
- Caveat: confirm current Google rules at deploy time (knowledge cutoff Jan 2026; CASA stable since ~2023).

## Test clients
- **Test client 1: user's wife** (trusted volunteer, real Gmail). Get explicit consent — rehearsal
  for the client consent conversation.
- User's own inbox near-empty (good for plumbing tests; wife's is the realistic triage testbed).

## Phasing
- Phase 0: governance + data-flow spec (doubles as client-facing artifact).
- Phase 1: thin button + read-only archive/search against one real account; the MVP triage loop
  (click → pull → categorize → propose → summary → exec approves). The showcase demo.
- Phase 2+: coupon/expiry extraction, deeper search UI, supervised auto-handling, optional scheduling.

## Build status (2026-06-12)
- Codebase lives in repo at **`email-triage/`** (dflewell repo). Stack: **Python + Flask + SQLite +
  Claude API**, chosen because it matches the accounting tool and is readable for a vibe coder.
- **Phase 0 governance DONE** — `email-triage/governance/`: `DATA_FLOW.md` (mermaid), `DATA_HANDLING.md`
  (store/where/how-long/how-to-delete), `CONSENT_SCRIPT.md`. These are the client-facing trust artifacts.
- **Phase 1 scaffold DONE** — thin web button (`Start my morning`) + summary view; real OAuth flow,
  Gmail pull, Claude structured-output classification, Fernet-encrypted SQLite store. Sends nothing.
- **Interface decision:** thin web button FIRST (Darrell's call, 2026-06-12), overriding the CLI-first rec.
- **Model DECIDED (2026-06-12): `claude-haiku-4-5`** — cheapest, fine for sorting; Darrell's call. Switch
  via `TRIAGE_MODEL` env var (Sonnet 4.6 / Opus 4.8 if quality lags). Revisit after testing on real mail.
- **Deletion: DONE** — one-click `/delete` route (confirm page) removes the per-exec DB file + OAuth token,
  backing the deletion promise in `governance/DATA_HANDLING.md`. Linked from the start page.
- **Consent deck: DONE** — `governance/consent-deck.html`, a self-contained 9-slide HTML deck (no deps,
  arrow-key nav, F=fullscreen) for presenting the consent walkthrough. Built here (not Claude.ai) so it's
  reusable, version-controlled collateral. Polish visuals in Claude.ai/slide tools later if wanted.
- **Drive-friendly PDF: DONE** — `governance/consent-deck.pdf` (16:9, 9 pages) + generator
  `governance/build_pdf.py` (reportlab; `pip install reportlab` then `python governance/build_pdf.py`).
  Drive retired HTML web-hosting (2016) so HTML won't render from Drive — PDF does. For a live HTML
  link instead, use Netlify Drop (not GitHub Pages — Pages would expose the whole repo).
- **Encryption:** email bodies/subjects/drafts encrypted at rest with Fernet (`FERNET_KEY` per exec).
  Metadata (sender, date, category) left queryable for de-dupe + summary.

## Next step
- Darrell: pick the triage model (cost vs quality) and set `TRIAGE_MODEL`.
- Run the loop against the wife's real Gmail (consent first) to test categorization quality.
- Phase 2 backlog: coupon/expiry extraction, move/label actions (rung 2), searchable-archive UI.
