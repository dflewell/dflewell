# Wendy Mather — File Organization Strategy

Strategy and SOP for inventorying, consolidating, and organizing Wendy Mather's
files across four sources so she can **find files when she needs them**. Related
to the CampB project; this piece is Wendy's personal + work file estate.

## North star
- **Primary goal: findability.** Wendy wants to locate files on demand. Storage
  size is *not* the driver — do not optimize for freeing quota.
- **Final home: Google Drive.** Everything consolidates here; Wendy owns and runs
  it after the project completes.
- **Roles:** Darrell runs the tooling and guides; Wendy reviews and decides
  (especially any deletions); Wendy takes ownership of Google Drive at the end.
- **Dedup is a byproduct, not the point.** Fewer duplicates = easier to find, so
  we flag and remove obvious dupes, but we never auto-delete — Wendy confirms.

## The four sources (mental model)
| Source | What it really is | Priority | Access path |
|---|---|---|---|
| **Carbonite** | Backup of a computer Wendy **no longer owns** | 🔴 URGENT — rescue first | Web restore / Carbonite app |
| **Dropbox** | Live library | Normal | Web + rclone (scriptable) |
| **Google Drive** | Live library **and the destination** | Normal | Web + rclone (scriptable) |
| **Apple iCloud** | Live library | Hardest to script | Must pull down via a Mac/Windows iCloud app first |

## Phase 0 — Carbonite rescue (do this FIRST, it can expire)
Carbonite backups are anchored to the original machine. On many plans, if that
computer hasn't checked in for a while (~30+ days), the backup is **flagged for
deletion**. Treat this as time-sensitive.
1. **Confirm the account & backup still exist** — log in at carbonite.com, verify
   the backup set for the old computer is present and not marked expiring.
2. **If it's expiring / already locked** — contact Carbonite support immediately;
   ask them to hold/extend the backup. Do not wait.
3. **Restore everything** to a known-safe location: an external drive (preferred
   for a first landing zone) or directly into a staging folder.
4. **Note the critical files** Wendy has been hunting — check they're in the
   restore. This is the emotional win that proves the project's value early.
5. Only after the restore is safe do we inventory it (Phase 2).

## Phase 1 — Triage each source
For each of the four sources, record on the tracker (see Inventory base below):
- Account/login confirmed, storage limit, current usage.
- Rough file count and what dominates (photos/video vs. documents).
- Access method that works (web, app, rclone remote configured).
- Any risk flags (expiring, locked, forgotten password, 2FA device gone).

## Phase 2 — Full inventory (the core deliverable)
Goal: **one searchable master catalog** of every file across every source, so
Wendy can search once instead of hunting four places.

**Tooling (Darrell runs):**
- **rclone** — connect Dropbox + Google Drive as remotes; use `rclone lsjson` to
  export a full file listing (path, size, modtime, hash) per remote.
- **iCloud** — install the iCloud app on a Mac/PC, sync iCloud Drive + Photos
  locally, then inventory that local folder.
- **Carbonite** — inventory the restored folder from Phase 0.
- Local scan of any restored/downloaded folders with the same listing approach.

**Catalog fields (per file):** source, full path, filename, type/extension,
size, date modified, content hash (for dedup), duplicate flag, "keep/review/
delete" status, and a free-text note.

**Where the catalog lives:** an **Airtable base** ("Wendy File Inventory") — it's
searchable, filterable, and Wendy-friendly for review. Alternative: a Google
Sheet. See `INVENTORY_SCHEMA.md` for the field list.

## Phase 3 — Design the taxonomy (built around how Wendy searches)
Before moving anything, agree on a folder structure that matches Wendy's mental
model — the point is findability.
- Top split: **Personal** vs. **Work/Projects**.
- Then the axis Wendy actually thinks in — likely **by client/project** for work
  and **by year or life-area** for personal. Confirm with Wendy.
- Keep it shallow and consistent. A structure she can't remember defeats the goal.
- Draft it, walk Wendy through it, adjust, then lock it.

## Phase 4 — Deduplicate + reorganize
1. **Surface duplicates** from the catalog's content-hash matches; for photos/
   video use near-duplicate detection (dupeGuru / Czkawka on the local copy, or
   Google Photos' own duplicate finder).
2. **Wendy reviews and confirms** every deletion — tools only *flag*.
3. **File survivors** into the Phase 3 taxonomy inside Google Drive.

## Phase 5 — Consolidate to Google Drive + maintain
1. Move everything into the agreed Google Drive structure.
2. Once a source is fully migrated and verified, downgrade/close the redundant
   paid plans (Dropbox, extra iCloud/Carbonite) — only after verification.
3. Hand off to Wendy with a one-page "how to file new stuff" rule so it stays
   organized.

## Key references / gotchas
- **Carbonite can purge backups from long-inactive computers** → Phase 0 is urgent.
- **iCloud has no good API** → must be pulled to a local machine before any tool
  can inventory it.
- **rclone** handles Dropbox + Google Drive well (listing, hashing, dedup within a
  remote); it does not cleanly do iCloud.
- **Never auto-delete.** Wendy confirms all deletions.
- Storage limits are real but **not the goal** — don't let "we're at the cap"
  push us into deleting before the inventory + Wendy's review.

## Status log
| Date | Phase | Notes |
|---|---|---|
| 2026-07-05 | 0 — planning | Strategy drafted. Decisions: goal=findability, home=Google Drive, Darrell tools / Wendy reviews. Carbonite rescue flagged urgent. |
