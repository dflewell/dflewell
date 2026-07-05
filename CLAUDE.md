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

## CampB / CAMBP work (UC Davis)
Consulting work for the **California Master Beekeeper Program** (UC Davis, Wendy
Mather `wmather@ucdavis.edu`). Recurring ad-hoc tasks — e.g. waiver/safety-policy
analysis, and matching event attendees to loaner **bee suits & equipment**.
- Source docs arrive as PDFs/spreadsheets in a shared **Google Drive** folder
  (e.g. "Bee Suits and Equipment", folder ID `1cGJpBwXxFaUsPucJt5c1Q1suv5H4KU5q`).
  Test the Drive connector and read the folder at the start of each such task.
- **Suit-matching deliverables** Darrell likes: (1) a Google **Sheet** pull list
  in the same folder, (2) a **Gmail draft** to Wendy (never auto-send), (3) a
  **printable labels PDF**, 4 labels per Letter page, cut-and-tape to suits.

### Gotchas learned
- **Labels PDF, keep it small.** Headless-Chrome `--print-to-pdf` embeds full
  system fonts → ~700 KB, too big to inline as base64 for the Drive MCP upload.
  Instead generate with **reportlab** using base-14 fonts (Helvetica/-Bold,
  ZapfDingbats for the ▲) → ~14 KB, no font embedding. `pip install reportlab`
  works here; render/verify pages with `pymupdf` (get_pixmap) then Read the PNG.
- **Drive MCP is create+read only** (no update/delete). Can't replace/delete a
  file → uploaded HTML+PDF both linger; just point Wendy at the PDF. Same reason
  the **Gmail draft can't be updated** — creating a v2 leaves the v1 draft behind
  (tell Darrell to discard the earlier one).
- Upload non-Google files with `contentMimeType` + `disableConversionToGoogleType:true`
  (else text/CSV/HTML get converted to Google Docs/Sheets). CSV uploaded *with*
  conversion becomes a clean Google Sheet — quote every field (names are "Last, First").

## Git
- Development branch for web sessions: `claude/dreamy-bardeen-FNWgQ` (or as assigned).
