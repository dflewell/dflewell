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
6. **Flag gaps** — if the amount lives only in a PDF attachment or vendor portal,
   mark it `TBD — check portal/attachment`. (See limitation below.)
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
| _Unknown vendor_ | Leave generic; flag for user to classify |

> These are defaults against Xero's standard chart of accounts. Darrell reclassifies
> in Xero as needed. Update this table as new recurring vendors appear.

## Known limitation — attachments
The Gmail MCP integration exposes **no tool to download attachment bytes**. Emails
where the dollar amount lives only in a PDF (e.g., Google Workspace, some Xero
invoices) cannot be fully parsed from the email alone. Workarounds:
- User supplies the amount, OR
- A Gmail filter / Apps Script saves attachments to a Google Drive folder, which
  *can* be read via the Drive `read_file_content` tool.

Until then, attachment-only amounts are reported as `TBD`.

## Schedule
Target cadence: each weekday, off-peak (≈ 8:00 PM Pacific). Configured via the
Claude Code web app scheduling/trigger UI (not in code). The scheduled session
prompt should be: _"Run the Accounting Stuff sweep per accounting/SWEEP_SOP.md."_
