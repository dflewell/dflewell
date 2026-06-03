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

## Git
- Development branch for web sessions: `claude/dreamy-bardeen-FNWgQ` (or as assigned).
