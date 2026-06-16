# Reimbursable Client Expenses — SOP

Procedure for handling out-of-pocket costs (mostly travel) that **True North AI LLC
bills back to a client**. These are NOT True North operating expenses — they pass
through to the client, appear as a line item on the client invoice, and need
supporting documentation + an expense report the client can book.

## Design constraint (why it works this way)
The Drive MCP can **create and read** files but **cannot update or delete** them.
So there is no "running spreadsheet the sweep appends to." Instead, every write is
a **new file**: one file per expense, and a new report file per billing run. The
report generator figures out what's already billed by reading prior reports.

## Intake — Gmail labels
- One label per client: **`Reimbursable - ClientName`** (e.g. `Reimbursable - Acme`).
- As you incur a cost, label/forward the receipt email into that client's label.
- Receipts stay **UNREAD** until processed (same convention as the main sweep).
- Create the label in Gmail once per client (or ask Claude to create it).

## Drive folder layout (created on first use)
```
Accounting Stuff/
  Reimbursable/
    ClientName/
      items/      ← one file per expense (created by the sweep)
      reports/    ← expense reports + their PDFs (created at billing time)
      receipts/   ← PDF attachments auto-saved by the Apps Script
```

## Sweep step (runs with the daily sweep — see SWEEP_SOP.md step 9)
For each label matching `Reimbursable - *` with unread items:
1. **Find new items:** `label:"Reimbursable - ClientName" is:unread`.
2. **Read** each thread; extract: `date, vendor, description, category, amount,
   currency, receipt ref`. Travel categories: Airfare, Lodging, Ground transport,
   Meals, Other.
3. **Attachments:** PDF receipts are auto-saved to `…/ClientName/receipts/` by the
   Apps Script. Read them via Drive `search_files` + `read_file_content` if the
   amount isn't in the email body.
4. **Write one item file** to `…/ClientName/items/` named
   `YYYY-MM-DD-vendor-slug.csv` with a single data row:
   `Date,Vendor,Description,Category,Amount,Currency,ReceiptRef,ReceiptFile`
   (create-only; never overwrite — each expense is its own file).
5. **Mark processed:** remove `UNREAD` from the message (`unlabel_message`).
6. Note reimbursables in the daily report under a separate **"Reimbursable
   (client-billable)"** heading so they're not mixed with operating expenses.

## Expense report generation (separate, on demand)
Run when you're ready to bill a client. Prompt:
**`Generate expense report for ClientName`**
1. Read every file in `…/ClientName/items/`.
2. Read every prior report in `…/ClientName/reports/` to collect already-billed
   item filenames (each report lists its source items in a `SourceItem` column).
3. **Unbilled = items not in any prior report.** Build the report from those.
4. Create a CSV at `…/ClientName/reports/YYYY-MM-DD-expense-report.csv` with
   columns: `Date,Vendor,Description,Category,Amount,SourceItem` plus a **TOTAL**
   row. (text/csv auto-converts to a Google Sheet → opens in Sheets/Excel.)
5. Output a chat summary: line items, total, and the invoice line text, e.g.
   _"Reimbursable expenses (see attached report) — $X,XXX.XX"_.

## Sending to the client
- The report is a Google Sheet (from the CSV). Share the link, **or** in Sheets:
  **File → Download → PDF** to send a print, and **→ Microsoft Excel (.xlsx)** if
  they want the spreadsheet.
- Supporting docs live in `…/ClientName/receipts/` — share that folder or attach
  the relevant PDFs.

## Xero treatment
- Post each reimbursable cost to **Other Receivables — account 1310** (balance sheet).
- When the client pays the invoice line item, the receipt clears account 1310.
- Net P&L impact = zero; the cost never flows through the income statement.
- The client invoice carries the reimbursement as its own line item with the
  expense report attached as supporting documentation.

## Open enhancement
If volume grows, a Xero connected app (OAuth) could push these straight to Xero as
billable expenses. Not needed at 1–2 clients / occasional travel.
