# First Session with Wendy — Afternoon Checklist

A single-sitting agenda to launch the file project. Darrell drives the MacBook;
Wendy watches, decides, and answers the taxonomy questions. Order matters — the
time-sensitive rescue comes first. Nothing here deletes anything.

Bring: Wendy's MacBook, logins/passwords for **Carbonite, Dropbox, Google Drive,
Apple ID** (and phones/devices for 2FA), and ideally an **external drive** for the
Carbonite restore.

---

## Block 1 — Carbonite rescue (do FIRST; it can expire) ⏱️ ~30–45 min
- [ ] Log in at carbonite.com as Wendy. Confirm the backup for the old computer
      still exists and is **not** flagged for deletion.
- [ ] If it's expiring or locked → call Carbonite support now; ask them to hold/
      extend before doing anything else.
- [ ] Start a **full restore** to a known folder (external drive or `~/CarboniteRestore`).
      (This can run in the background through the rest of the session.)
- [ ] Ask Wendy for the **specific files she's been hunting** — spot-check they're
      in the restore. Early win.

## Block 2 — Confirm access to the other three sources ⏱️ ~15 min
- [ ] **iCloud** — confirm Drive files show at
      `~/Library/Mobile Documents/com~apple~CloudDocs`; note if Photos library is separate.
- [ ] **Dropbox** — log in on the web; note storage used / limit.
- [ ] **Google Drive** — confirm the account that will be the final home; note storage.
- [ ] Jot each account's limit/usage into the strategy doc's status log.

## Block 3 — Set up rclone & run the inventory ⏱️ ~30 min hands-on, then it runs
Follow `RCLONE_RUNBOOK.md`:
- [ ] `brew install rclone` (+ `brew install jq`).
- [ ] `rclone config` → add `dropbox` and `gdrive` remotes (browser auth as Wendy).
- [ ] `rclone listremotes` and `rclone lsd` to confirm both authorized.
- [ ] Kick off the four `lsjson` exports (dropbox, gdrive, iCloud folder, Carbonite
      restore). **Let them run** — big libraries take a while.

## Block 4 — Taxonomy conversation (while inventory runs) ⏱️ ~30 min
Open `DRIVE_TAXONOMY.md` and walk Wendy through it. Get answers to the 5 questions:
- [ ] Work axis — client, project, or type of work?
- [ ] Photos — by year or by event/trip?
- [ ] Name of the top Work folder (business name)?
- [ ] Archive split, or everything live and searchable?
- [ ] Anything missing / any empty categories to cut?
- [ ] Edit the draft live to match her answers.

## Block 5 — Build the CSV & load Airtable ⏱️ ~20 min
- [ ] Run `tocsv.sh` → produces `inventory.csv`.
- [ ] Import into the **Wendy File Inventory** base → **Files** table (map columns
      per the runbook).
- [ ] Sanity check: row counts roughly match each source; hashes populated.

## Block 6 — First duplicate look & wrap ⏱️ ~15 min
- [ ] In Airtable, create a view **grouped by Content hash**; eyeball the biggest
      duplicate groups together so Wendy sees the payoff.
- [ ] Agree on homework: Wendy works the grouped view (Keep one / mark rest Delete)
      at her own pace; deletions happen only after her review.
- [ ] Confirm the Carbonite restore finished; verify her hunted-for files landed.

---

## Definition of done for session 1
- Carbonite backup rescued (or a support hold in place) and restore completed.
- All four sources inventoried into `inventory.csv` and loaded into Airtable.
- Taxonomy draft edited to Wendy's real preferences.
- Wendy knows exactly what her review homework is.

## What comes after (not today)
- Wendy reviews duplicates → confirms deletes.
- Assign each keeper a **Destination folder**.
- Phase 5: migrate to Google Drive, then downgrade/close the emptied plans.
