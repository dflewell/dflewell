# Google Drive Taxonomy — DRAFT for Wendy to react to

Proposed folder structure for Wendy's consolidated Google Drive. This is a
**starting point to edit, not a final answer** — the goal is findability, so it
should match how Wendy actually looks for things. Walk her through it, cut what
doesn't fit, rename to her words, then lock it.

## Design rules (why it looks like this)
1. **Two top-level worlds:** `Personal` and `Work`. Almost everything is clearly
   one or the other, and it's the first split Wendy's brain makes.
2. **Shallow.** Aim for 2–3 levels deep max. If you can't remember where something
   goes, the structure has failed.
3. **One obvious home per file.** Avoid categories that overlap (a file shouldn't
   plausibly belong in three folders).
4. **Dates in filenames, not deep folder trees.** Prefer `2019-tax-return.pdf` over
   burying it 5 folders deep by year/quarter/month. Use year folders only where
   volume demands it (photos, financials).
5. **A landing zone** (`_Inbox`) so new/unknown files have a home instead of the
   desktop. The leading underscore sorts it to the top.

## Proposed tree
```
Wendy (My Drive)
├── _Inbox/                      ← drop zone for un-filed items; empty it periodically
│
├── Personal/
│   ├── Financial/               ← taxes, banking, statements (by year inside)
│   │   ├── Taxes/
│   │   └── Statements/
│   ├── Health & Medical/
│   ├── Home & Property/         ← mortgage, insurance, repairs, warranties
│   ├── Legal & Identity/        ← IDs, passport, wills, vital records
│   ├── Family/                  ← per-person subfolders if useful
│   ├── Photos & Videos/         ← by year: 2019/, 2020/, ...
│   ├── Travel/
│   └── Misc/
│
└── Work/
    ├── True North (or Wendy's business)/
    │   ├── Admin & Finance/
    │   ├── Marketing/
    │   └── Templates/
    ├── Clients/
    │   ├── ClientA/             ← one folder per client
    │   │   ├── Deliverables/
    │   │   ├── Correspondence/
    │   │   └── Contracts/
    │   └── ClientB/
    ├── Projects/                ← cross-client or internal initiatives (e.g. CampB)
    ├── Reference & Resources/   ← industry docs, articles, boilerplate she reuses
    └── Archive/                 ← finished/old work she wants kept but out of the way
```

## Open questions for Wendy (these shape the tree)
1. **Work axis:** does she think by **client**, by **project**, or by **type of
   work**? The draft leads with Clients + Projects — right?
2. **Photos:** by **year** (draft) or by **event/trip**? Big libraries usually do
   year at top, event below.
3. **Business name:** what should the top Work folder be called?
4. **Retention:** is an `Archive/` split useful, or does she prefer everything live
   and searchable?
5. Any category above that's **empty for her**, or anything **missing**?

## How this connects to the inventory
- The Airtable **Destination folder** field = the path a file lands in here.
- During review, Wendy tags each keeper with its destination; migration (Phase 5)
  is then just moving files to the paths already decided.

## Maintenance rule (one line for Wendy, post-handoff)
> New file? Put it in `_Inbox` if unsure, then move it to its home within the week.
> When naming, lead with a date (`YYYY-MM-DD`) for anything time-based.
