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
9. **Reimbursable expenses** — also check for any labels named `Reimbursable - *`
   (one per client) with unread items, and process them per
   **`accounting/REIMBURSABLE_SOP.md`**. These are client-billable costs, NOT True
   North operating expenses — handle them separately.

## Vendor → Xero account mapping (suggestions)
| Vendor | Suggested Xero account |
|---|---|
| Anthropic (Claude) | Software & Subscriptions |
| Xero | Software & Subscriptions |
| Google Workspace / Google LLC | Software & Subscriptions (or Computer & Internet Expenses) |
| AWS / Amazon Web Services | Computer & Internet Expenses |
| Zoom Communications | Software & Subscriptions |
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
// Helper: get a folder by name under a parent, creating it if missing.
function getOrCreateFolder(parent, name) {
  var it = parent.getFoldersByName(name);
  return it.hasNext() ? it.next() : parent.createFolder(name);
}

// Save PDF attachments from a thread into a target folder, de-duped by filename.
function savePdfs(thread, folder) {
  thread.getMessages().forEach(function (msg) {
    msg.getAttachments().forEach(function (att) {
      if (att.getContentType() !== 'application/pdf') return;
      if (!folder.getFilesByName(att.getName()).hasNext()) folder.createFile(att);
    });
  });
}

function saveAccountingAttachments() {
  // Root "Accounting Stuff" folder.
  var roots = DriveApp.getFoldersByName('Accounting Stuff');
  var root = roots.hasNext() ? roots.next() : DriveApp.createFolder('Accounting Stuff');

  // 1) Operating-expense receipts from the main label -> root folder.
  var main = GmailApp.getUserLabelByName('Accounting stuff');
  if (main) main.getThreads(0, 100).forEach(function (t) { savePdfs(t, root); });

  // 2) Reimbursable receipts: any label named "Reimbursable - ClientName"
  //    -> Reimbursable/ClientName/receipts/.
  var reimb = getOrCreateFolder(root, 'Reimbursable');
  GmailApp.getUserLabels().forEach(function (label) {
    var name = label.getName();
    if (name.indexOf('Reimbursable - ') !== 0) return;
    var client = name.substring('Reimbursable - '.length).trim();
    var receipts = getOrCreateFolder(getOrCreateFolder(reimb, client), 'receipts');
    label.getThreads(0, 100).forEach(function (t) { savePdfs(t, receipts); });
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
