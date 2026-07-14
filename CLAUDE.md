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
**`accounting/SWEEP_SOP.md`**.

**Output (changed 2026-07-14): a dated Google Sheet in the Drive `Accounting
Stuff` folder (`YYYY-MM-DD-sweep.csv` uploaded so it auto-converts to Sheets),
NOT a git-committed markdown file.** The old per-branch markdown approach
caused 10 reports to go stranded/invisible for weeks (see
`accounting/reports/2026-07-GAP-REVIEW.md` and `2026-07-consolidated.md` for
the recovery). Old dated `.md` reports in `accounting/reports/` are kept as
historical reference only — don't add new ones there.

Key facts (so future sessions don't re-discover):
- Gmail label name: `Accounting stuff`; label ID: `Label_3864205698836096106`.
  **Query by name** (`label:"Accounting stuff"`) — querying by the ID returned nothing.
- Filter keeps incoming receipts **UNREAD**, but this has proven unreliable —
  several items landed in the label without ever getting UNREAD and were
  missed for weeks. Each sweep should still run `is:unread` first, but also
  periodically diff the full label against previously-processed invoice
  numbers to catch stragglers (see gap review above for real examples: Zoom,
  Canva).
- Mode: **review-first (Option A)** — Darrell reviews before entering in Xero.
- Vendor→Xero mapping lives in SWEEP_SOP.md (Anthropic/Xero/Google = Software &
  Subscriptions; AWS/Cloudflare = Computer & Internet Expenses; Zoom/Airtable/
  Canva Pro = Software & Subscriptions). **Xero itself is a flat $5.00/month —
  confirmed by Darrell 2026-07-14, don't check the portal, just use $5.00.**
- **Attachment limitation:** the Gmail MCP exposes NO tool to download attachment
  bytes, so amounts living only in PDFs can't be read from email. **Workaround in
  use:** attachments are auto-saved to a Google Drive folder via Gmail filter /
  Apps Script; read them with the Drive `read_file_content` tool during the sweep.
  Note: some Drive PDFs (e.g. CA Secretary of State filing receipts) arrive
  with **no corresponding Gmail thread at all** — they were placed in the
  folder outside this pipeline and the Gmail-driven sweep structurally can't
  find them; check the Drive folder directly if Darrell mentions a document
  the sweep hasn't surfaced.
- Schedule: weekdays ~8:00 PM Pacific, configured in the Claude Code web app
  scheduling UI (not in code). Scheduled session needs the Gmail + Drive MCPs
  connected to work.
- **Git branch deletion is not available to Claude here:** `git push
  origin --delete <branch>` gets a 403 from this environment's git proxy, and
  the connected GitHub MCP has no delete-branch tool. Stale session branches
  must be deleted manually via the GitHub web UI (repo → Branches page).

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
## New client prep (research + first meeting)
Turns a warm introduction into a researched, professional first meeting. Full
procedure: **`clients/CLIENT_PREP_SOP.md`**; brief template: `clients/BRIEF_TEMPLATE.md`.
- **Positioning lens:** True North's core offering is **AI strategy & adoption**;
  finance depth (CMA) and AWS certs are credibility anchors, not separate service lines.
- Research is **public info only** (WebSearch/WebFetch); LinkedIn profile pages
  usually can't be fetched — rely on search snippets. Label facts vs. inferences; cite sources.
- Storage: finished brief goes to **Google Drive** under the shared **Clients**
  parent folder → `<Company>/<date>-<Company>-prep`, saved as a **Google Doc**
  (mobile-readable). Confidence markers in the Doc: `[OK]`/`[?]`/`[!]`.
  Drive MCP create+read only → one file per meeting.
- Intro PDF in the shared Drive folder is a valid kickoff input; runs in one session.
- On-demand. Kick off with: _"New client prep per clients/CLIENT_PREP_SOP.md — introduced to
  <Name>, <Title> at <Company>, meeting <date>, context: <...>."_
## CampB — Wendy Mather file organization
Project to inventory and organize Wendy Mather's files across **Carbonite,
Dropbox, Google Drive, iCloud**. Strategy: **`campb/FILE_ORG_STRATEGY.md`**;
catalog schema: `campb/INVENTORY_SCHEMA.md`.
- **Goal = findability**, not freeing storage. Wendy's pain point is locating files.
- **Final home = Google Drive** (Wendy owns/runs it after handoff).
- **Roles:** Darrell runs tooling + guides; Wendy reviews and confirms deletions.
- **Carbonite is urgent** — backup of a computer she no longer owns; may hold
  critical files and can be purged after long inactivity. Rescue/restore first.
- iCloud has no good API → inventoried as a **local folder on Wendy's MacBook**
  (`~/Library/Mobile Documents/com~apple~CloudDocs`); iCloud confirmed accessible.
- Inventory tooling: **rclone** on the MacBook (Dropbox + Drive listing/hashing);
  runbook `campb/RCLONE_RUNBOOK.md`. Catalog = **Airtable** base "Wendy File
  Inventory" (`app693hLQifCoMCWH`, table `Files` `tblIDqr87hVGHUTU5`), created.

## Git
- Development branch for web sessions: `claude/dreamy-bardeen-FNWgQ` (or as assigned).
