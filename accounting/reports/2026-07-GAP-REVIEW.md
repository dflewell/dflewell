# Accounting Sweep — Gap Review (2026-07-14)

Darrell noticed PDFs in the Drive "Accounting Stuff" folder (Zoom, Secretary of
State) with no matching sweep report. Investigation found **two separate root
causes**, both now fixed or flagged below.

## Root cause 1 — sweep reports stranded on unmerged branches (fixed)

Each scheduled sweep runs in a fresh Claude Code web session on its own
throwaway git branch. Only some of those branches were ever merged to `main`
via PR, so **10 sweep reports existed in git history but were invisible on
`main`** (where Darrell actually looks). Recovered and merged to `main`:

| Date | Branch it was stranded on | New items that day |
|---|---|---|
| 2026-06-05 | claude/confident-clarke-l3IE0 | none (all TBD carryover) |
| 2026-06-11 | claude/confident-clarke-6kqq8p | Zoom $169.90 |
| 2026-06-12 | claude/confident-clarke-qwr8v0 | Zoom $169.90 (**duplicate of 6/11 — see note in that file**) |
| 2026-06-15 | claude/confident-clarke-yq8ssq | Anthropic $10.00 |
| 2026-06-18 | claude/confident-clarke-gxkd6m | Zoom + Anthropic (**both duplicates of 6/11 and 6/15**) |
| 2026-06-22 | claude/confident-clarke-6enife | Xero TBD, Cloudflare $160.00 |
| 2026-07-03 | claude/confident-clarke-gbg0av | Google Workspace $59.40 |
| 2026-07-06 | claude/confident-clarke-u8yar2 | Airtable $72.00 |
| 2026-07-09 | claude/confident-clarke-hr7kp8 | Anthropic $45.00 |
| 2026-07-13 | claude/confident-clarke-go8q87 | Akismet $14.95 |

Going forward, `CLAUDE.md` now instructs the sweep to fast-forward `main` in
the same run it commits the report (see the "Merge reports straight to main"
note), so this shouldn't recur.

**The Zoom invoice (INV357691838, $169.90) was independently rediscovered and
reported three times** (6/11, 6/12, 6/18) because each session didn't know
about the others' work. **It is one charge, not three** — enter it once.
Same for the Anthropic $10.00 credit (reported 6/15 and again 6/18).

## Root cause 2 — items that never went through the Gmail sweep at all

The sweep is driven entirely by the Gmail `Accounting stuff` label
(`is:unread`, then a full-label scan for anything missed). Two kinds of items
fall outside that:

**A) Emails that landed in the label but were never marked UNREAD** — caught
this time, added retroactively:
- Canva "print items" invoice, $52.80, June 16, 2026 (invoice 04914-68353152)
  — flagged for business/personal confirmation, see 2026-07-14-sweep.md Item 4.
- Canva Pro subscription, $15.00, July 13, 2026 (invoice 04941-51965078) —
  this one *was* UNREAD but arrived after the day's first sweep pass; added
  as Item 3 in 2026-07-14-sweep.md.

This is the same Gmail-filter reliability issue flagged in the 6/12 and 6/18
reports (items landing in the label without staying UNREAD). **Recommend
checking Gmail Settings → Filters for the "Accounting stuff" rule** to confirm
"Never mark as read" / "Mark as unread" is still applied consistently.

**B) Two Secretary of State PDFs that never came through Gmail at all:**
- `Cal Statement of Info Receipt 2026.pdf` — CA Secretary of State, LLC
  Statement of Information filing fee, **$20.00**, receipt #14110428, entity
  **TRUE NORTH AI LLC**, paid 06/17/2026 (card ending 0697). **This is a
  legitimate True North expense** — never reported because no Gmail message
  under the "Accounting stuff" label exists for it (Drive search found no
  matching thread). Suggested Xero account: **Filing Fees / Government Fees**
  (not Software & Subscriptions) — please confirm against your chart of accounts.
- `Secretary of State for California Annual Filing of Macromoecelium, LLC.pdf`
  — same $20.00 filing fee, receipt #14299890, but for **Macromoecelium, LLC**
  — a **different entity**, not True North AI LLC (paid 07/07/2026, card
  ending 1910). **Do not enter this in True North's books** — flagging only
  so it isn't mistaken for a True North expense during cleanup.

These two PDFs must have been placed directly in the Drive "Accounting Stuff"
folder outside the Gmail→Drive Apps Script pipeline (no source email found),
so the Gmail-driven sweep structurally cannot see this category. **If more
Secretary of State / government filings should be tracked this way going
forward, recommend either (a) forwarding the confirmation email to the
`Accounting stuff` label so it flows through the normal pipeline, or (b)
telling Claude to check the Drive folder directly during each sweep for
files with no corresponding processed invoice number** — happy to add that
as a standing step in SWEEP_SOP.md if you want it.

## Net effect
- All recoverable historical reports are now on `main`.
- Two live gaps (Canva items) have been processed and added to today's report.
- The two Secretary of State fees are surfaced here since they don't fit the
  existing report-per-email format; the True North one ($20, 6/17) is ready
  to enter once you confirm the Xero account, the Macromoecelium one is out
  of scope.
