# Data Handling — What We Store / Where / How Long / How to Delete

_Client-facing artifact. This is the sheet the executive keeps after the consent conversation._

## What we store
| Item | Stored? | Encrypted at rest? | Notes |
|---|---|---|---|
| Message ID, date, sender, subject | Yes | Subject yes (with body) | Used to avoid re-processing and to show the summary |
| Email body text | Yes | **Yes — Fernet** | Encrypted with a key only the operator holds |
| Assigned category | Yes | No (not sensitive) | `important / client / shopping / read_later` |
| Proposed reply draft | Yes | Yes (with body) | A suggestion only; never sent automatically |
| Attachments' contents | **No** | — | Out of scope for this MVP |
| Google OAuth token | Yes | Should be OS-protected | Lets the tool re-access Gmail at next button press; revocable by the exec |

## Where it's stored
- A **single SQLite database file per executive** (`data/triage_<EXEC_ID>.db`).
- **No commingling** — each exec's data is a separate file. No shared/multi-tenant database.
- The file lives on the machine the consultant runs the tool on (local-first; not in a shared cloud).

## How long
- Default: **kept until the exec asks us to delete it** (the point is a durable, searchable archive —
  the opposite of losing mail). No automatic expiry in the MVP.
- The OAuth token lives until revoked or it expires (consumer testing-mode tokens expire ~7 days,
  which is fine because access is re-granted at the next button press).

## Where inference happens
- Email subject + body text is sent to the **Claude API (Anthropic)** for categorization and draft
  suggestions. It is processed in transit and **not used to train models**. We send only what's needed
  to categorize — see `DATA_FLOW.md`.

## How to delete (the exec can ask for any of these)
1. **Delete all stored data for me.** Delete the file `data/triage_<EXEC_ID>.db`. That removes the
   entire categorized history and all stored bodies/drafts for that exec. Nothing else references it.
2. **Cut off access immediately.** The exec revokes the app in their Google Account →
   *Security → Third-party access*. The tool can no longer read Gmail, with no action needed from us.
3. **Destroy the encryption key.** Discard the `FERNET_KEY`. Without it, the encrypted bodies in any
   remaining DB copy are unrecoverable.
4. **Confirmation.** On request we confirm in writing that 1–3 are done.

## Operator responsibilities
- Keep the `FERNET_KEY` and `ANTHROPIC_API_KEY` out of the repo (they live in `.env`, git-ignored).
- One key per exec is recommended so deleting one exec's key never affects another.
- Store the DB on an encrypted disk / protected machine; Fernet protects the bodies, but OS-level
  protection guards the metadata and the token.
