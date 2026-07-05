# Wendy File Inventory — catalog schema

The master catalog for Phase 2. Home: the **Airtable base "Wendy File Inventory"**
(base `app693hLQifCoMCWH`, table `Files` `tblIDqr87hVGHUTU5`) — already created with
the fields below. A Google Sheet with the same columns would work too. One row =
one file. Load it via the `campb/RCLONE_RUNBOOK.md` steps.

## Fields
| Field | Type | Notes |
|---|---|---|
| Filename | Single line text | Base name, e.g. `2019-taxes.pdf` |
| Source | Single select | Carbonite / Dropbox / Google Drive / iCloud / Local |
| Full path | Long text | Original path within its source |
| Type | Single select | Document / Photo / Video / Audio / Archive / Other |
| Extension | Single line text | `pdf`, `jpg`, `mov`, … |
| Size (MB) | Number | From `rclone lsjson` / file listing |
| Date modified | Date | From source metadata |
| Content hash | Single line text | MD5/SHA from rclone; the key for dedup matching |
| Duplicate? | Checkbox | Set when hash (or near-dupe) matches another row |
| Duplicate group | Single line text | Shared tag/ID for all copies of the same file |
| Status | Single select | Keep / Review / Delete / Migrated |
| Destination folder | Single line text | Target path in Google Drive (Phase 3 taxonomy) |
| Notes | Long text | Free text — Wendy's or Darrell's remarks |

## How rows get created
- **Dropbox / Google Drive:** `rclone lsjson <remote>: --hash -R` → transform to
  the columns above (script maps JSON fields → row fields).
- **iCloud:** sync to a local folder via the iCloud app, then list that folder.
- **Carbonite:** list the restored folder from Phase 0.

## Dedup logic
1. Group rows by **Content hash** → exact duplicates (safe to flag).
2. For photos/video, run a near-duplicate pass (dupeGuru/Czkawka/Google Photos)
   and tag the **Duplicate group**.
3. Wendy reviews each group, keeps one, marks the rest **Delete**.
