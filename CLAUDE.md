# Project memory — dflewell

## Owner / context
- Darrell Lewell, runs **True North AI LLC** (consulting). Inactive CMA — deep
  finance/accounting background. Intermediate technical; beginner "vibe coder".
  AWS Cloud Practitioner + AI Practitioner certified.
- Prefers succinct, step-by-step responses. Offer artifacts; don't create by default.
- Accounting platform: **Xero** (default chart of accounts).

## Accounting "Stuff" email sweep
Routine that sweeps the Gmail **"Accounting stuff"** label for receipts /
subscription renewals and produces a Xero-ready expense review. Full procedure:
**`accounting/SWEEP_SOP.md`**. Report template: `accounting/reports/REPORT_TEMPLATE.md`.
Dated reports land in `accounting/reports/YYYY-MM-DD-sweep.md`.

Key facts (so future sessions don't re-discover):
- Gmail label name: `Accounting stuff`; label ID: `Label_3864205698836096106`.
  **Query by name** (`label:"Accounting stuff"`) — querying by the ID returned nothing.
- Filter keeps incoming receipts **UNREAD**. Sweep processes `is:unread`, then
  removes the `UNREAD` label per message (`unlabel_message`) so the next sweep
  only sees new items.
- Mode: **review-first (Option A)** — Darrell reviews before entering in Xero.
- Vendor→Xero mapping lives in SWEEP_SOP.md (Anthropic/Xero/Google = Software &
  Subscriptions; AWS = Computer & Internet Expenses).
- **Attachment limitation:** the Gmail MCP exposes NO tool to download attachment
  bytes, so amounts living only in PDFs can't be read from email. **Workaround in
  use:** attachments are auto-saved to a Google Drive folder via Gmail filter /
  Apps Script; read them with the Drive `read_file_content` tool during the sweep.
- Schedule: weekdays ~8:00 PM Pacific, configured in the Claude Code web app
  scheduling UI (not in code). Scheduled session needs the Gmail + Drive MCPs
  connected to work.

## Reimbursable client expenses
Out-of-pocket costs (mostly travel) that True North bills back to a client. Full
procedure: **`accounting/REIMBURSABLE_SOP.md`**. NOT operating expenses — they
pass through to the client invoice as a line item.
- Intake: one Gmail label per client, **`Reimbursable - ClientName`**.
- Storage: **Drive only** (no repo CSV). Layout under `Accounting Stuff/Reimbursable/
  ClientName/`: `items/` (one file per expense), `reports/` (billing reports),
  `receipts/` (PDFs auto-saved by the Apps Script).
- **Drive MCP is create+read only** (no update/delete) → design is create-only:
  one file per expense; billed status derived by reading prior reports.
- Sweep handles these in SWEEP_SOP.md step 9; reports generated on demand via
  prompt `Generate expense report for ClientName`.
- Apps Script (in SWEEP_SOP.md) now also saves reimbursable receipt PDFs per client.

## CampB — Wendy Mather file organization
Project to inventory and organize Wendy Mather's files across **Carbonite,
Dropbox, Google Drive, iCloud**. Strategy: **`campb/FILE_ORG_STRATEGY.md`**;
catalog schema: `campb/INVENTORY_SCHEMA.md`.
- **Goal = findability**, not freeing storage. Wendy's pain point is locating files.
- **Final home = Google Drive** (Wendy owns/runs it after handoff).
- **Roles:** Darrell runs tooling + guides; Wendy reviews and confirms deletions.
- **Carbonite is urgent** — backup of a computer she no longer owns; may hold
  critical files and can be purged after long inactivity. Rescue/restore first.
- iCloud has no good API → pull down via a Mac/PC iCloud app before inventorying.
- Inventory tooling: **rclone** (Dropbox + Drive listing/hashing/dedup); catalog
  lives in an **Airtable** base "Wendy File Inventory" (or a Google Sheet).

## Git
- Development branch for web sessions: `claude/dreamy-bardeen-FNWgQ` (or as assigned).
