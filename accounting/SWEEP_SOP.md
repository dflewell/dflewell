# Accounting Stuff — Email Sweep SOP

Standard operating procedure for sweeping the Gmail **"Accounting stuff"** label
and producing a Xero-ready expense review for **True North AI LLC**.

## Purpose
Receipts, subscription renewals, and purchase confirmations are filtered into the
Gmail label `Accounting stuff`. This routine reviews new (unread) items, extracts
expense data, suggests a Xero account by vendor, and outputs a review report.
The user (Darrell) reviews first, then enters into Xero manually until trust is
established (Option A — review-first).

## Key references
- **Gmail label name:** `Accounting stuff`
- **Gmail label ID:** `Label_3864205698836096106`
  - NOTE: querying by `label:Label_38...` (ID) returned nothing; query by the
    **label name** instead: `label:"Accounting stuff"`.
- **Entity:** True North AI LLC (domain truenorthai.consulting)
- **Accounting platform:** Xero (default chart of accounts)

## Sweep procedure
1. **Find new items.** Search threads with query:
   `label:"Accounting stuff" is:unread`
   (Going forward, the Gmail filter keeps incoming receipts UNREAD, so each sweep
   focuses only on unread = unprocessed items.)
2. **Read each thread** with `get_thread` (FULL_CONTENT) to get the body.
   - Large HTML bodies overflow the tool result — extract fields from
     `plaintextBody` using jq on the saved tool-result file when needed.
3. **Extract** per item: date, vendor, description, amount, currency, invoice/
   receipt number, billing period, payment method.
4. **Classify** — suggest a Xero account by vendor (see mapping below).
5. **Tax** — note whether US sales tax / GST may apply; confirm on the invoice.
6. **Attachments** — for items whose amount lives only in a PDF, look in the
   Google Drive folder **`Accounting Stuff`** (attachments are auto-saved there by
   the Gmail→Drive Apps Script). Find the PDF with the Drive `search_files` tool
   (match by invoice number or vendor + date) and read it via `read_file_content`.
   If the PDF isn't found, mark the amount `TBD — check portal/attachment`.
7. **Output** the report using `reports/REPORT_TEMPLATE.md`. Save a dated copy to
   `accounting/reports/YYYY-MM-DD-sweep.md`.
8. **Mark processed** — remove the `UNREAD` label from each processed message via
   `unlabel_message` with `labelIds: ["UNREAD"]`. The next sweep then ignores them.

## Vendor → Xero account mapping (suggestions)
| Vendor | Suggested Xero account |
|---|---|
| Anthropic (Claude) | Software & Subscriptions |
| Xero | Software & Subscriptions |
| Google Workspace / Google LLC | Software & Subscriptions (or Computer & Internet Expenses) |
| AWS / Amazon Web Services | Computer & Internet Expenses |
| Zoom / Zoom Communications, Inc. | Software & Subscriptions |
| _Unknown vendor_ | Leave generic; flag for user to classify |

> These are defaults against Xero's standard chart of accounts. Darrell reclassifies
> in Xero as needed. Update this table as new recurring vendors appear.

## Attachments — Gmail→Drive bridge
The Gmail MCP exposes **no tool to download attachment bytes**, so amounts that
live only in a PDF can't be read from the email. **Solution in use:** a Google
Apps Script auto-saves attachments from the `Accounting stuff` label into a Drive
folder named **`Accounting Stuff`**, which the sweep reads via the Drive tools.

### One-time setup (Apps Script)
1. Go to https://script.google.com → **New project**.
2. Paste the script below, save.
3. Run `saveAccountingAttachments` once and grant permissions when prompted.
4. **Triggers** (clock icon) → add a time-driven trigger, e.g. every 1 hour,
   so new attachments land in Drive before the evening sweep.

```javascript
function saveAccountingAttachments() {
  var labelName = 'Accounting stuff';
  var folderName = 'Accounting Stuff';
  var label = GmailApp.getUserLabelByName(labelName);
  if (!label) return;

  // Find/create the Drive folder.
  var folders = DriveApp.getFoldersByName(folderName);
  var folder = folders.hasNext() ? folders.next() : DriveApp.createFolder(folderName);

  // Only process threads that still have an attachment we haven't saved.
  var threads = label.getThreads(0, 100);
  threads.forEach(function (thread) {
    thread.getMessages().forEach(function (msg) {
      msg.getAttachments().forEach(function (att) {
        if (att.getContentType() !== 'application/pdf') return;
        // De-dupe by filename so re-runs don't pile up copies.
        var existing = folder.getFilesByName(att.getName());
        if (!existing.hasNext()) folder.createFile(att);
      });
    });
  });
}
```

> The sweep no longer marks Google/Xero amounts as `TBD` once their PDFs are in
> the `Accounting Stuff` Drive folder. Only flag `TBD` if the PDF is genuinely
> missing from Drive at sweep time.

## Schedule
Target cadence: each weekday, off-peak (≈ 8:00 PM Pacific). Configured via the
Claude Code web app scheduling/trigger UI (not in code). The scheduled session
prompt should be: _"Run the Accounting Stuff sweep per accounting/SWEEP_SOP.md."_
