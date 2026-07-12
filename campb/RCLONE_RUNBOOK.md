# rclone Inventory Runbook (macOS / Wendy's MacBook)

Step-by-step commands to inventory every source into a CSV that imports into the
**Wendy File Inventory** Airtable base (`app693hLQifCoMCWH`, table `Files`).

Run these on Wendy's MacBook (all four sources are reachable from it: iCloud is
signed in, and rclone connects Dropbox + Google Drive). Darrell drives; Wendy
watches. Nothing here deletes anything — it only **reads and lists**.

> **Do Phase 0 (Carbonite rescue) in `FILE_ORG_STRATEGY.md` first.** Restore those
> files to a local folder before inventorying them here.

## 1. Install rclone
```bash
# macOS, Homebrew:
brew install rclone
rclone version   # confirm it installed
```
No Homebrew? `curl https://rclone.org/install.sh | sudo bash`.

## 2. Connect the cloud sources (one-time each)
rclone calls each connection a "remote". Run the interactive config:
```bash
rclone config
```
Create these remotes (choose `n` for new remote each time):

- **Dropbox** → name it `dropbox`, storage type `dropbox`. It opens a browser to
  authorize; log in as Wendy. Accept defaults otherwise.
- **Google Drive** → name it `gdrive`, storage type `drive`. Authorize in browser
  as Wendy. When asked for scope, `1` (full access) is fine. This is BOTH a source
  (existing Drive files) and the final destination.

Verify:
```bash
rclone listremotes            # should show dropbox: and gdrive:
rclone lsd dropbox:           # top-level folders, confirms auth works
rclone lsd gdrive:
```

iCloud and Carbonite are **not** rclone remotes — they're local folders:
- **iCloud Drive** lives at `~/Library/Mobile Documents/com~apple~CloudDocs`
  (iCloud Photos export separately from the Photos app if needed — see note below).
- **Carbonite** = the folder you restored to in Phase 0, e.g. `~/CarboniteRestore`.

## 3. Export a file listing per source (with hashes for dedup)
`lsjson` walks a source recursively and emits JSON with path, size, modtime, and
hash. Save one file per source:
```bash
mkdir -p ~/wendy-inventory && cd ~/wendy-inventory

rclone lsjson -R --hash dropbox: > dropbox.json
rclone lsjson -R --hash gdrive:  > gdrive.json

# Local folders (iCloud + Carbonite restore):
rclone lsjson -R --hash "$HOME/Library/Mobile Documents/com~apple~CloudDocs" > icloud.json
rclone lsjson -R --hash "$HOME/CarboniteRestore" > carbonite.json
```
Notes:
- `--hash` gives content hashes — the key to finding true duplicates across sources
  regardless of filename. Google Drive returns hashes for real files but not native
  Google Docs/Sheets; those get flagged blank and matched by name/size instead.
- Large libraries take a while — let it run.

## 4. Turn the JSON into one import CSV
Each `lsjson` entry looks like:
`{"Path","Name","Size","MimeType","ModTime","IsDir","Hashes":{...}}`.
Flatten all four into a single CSV with columns matching the Airtable fields.
Save this as `~/wendy-inventory/tocsv.sh` and run `bash tocsv.sh`:
```bash
#!/usr/bin/env bash
# Requires jq: brew install jq
set -euo pipefail
cd ~/wendy-inventory
out=inventory.csv
echo "Filename,Source,Full path,Extension,Size (MB),Date modified,Content hash" > "$out"

emit () {  # $1 = json file, $2 = Source label
  jq -r --arg src "$2" '
    .[] | select(.IsDir==false) |
    [ .Name,
      $src,
      .Path,
      (.Name | capture("(?<e>[^.]+)$").e // ""),
      ((.Size // 0) / 1048576 | (.*100|floor)/100),
      (.ModTime | split("T")[0]),
      (.Hashes.md5 // .Hashes.MD5 // .Hashes.sha1 // "")
    ] | @csv' "$1" >> "$out"
}

emit dropbox.json  "Dropbox"
emit gdrive.json   "Google Drive"
emit icloud.json   "iCloud"
emit carbonite.json "Carbonite"

echo "Wrote $out  ($(wc -l < "$out") rows)"
```

## 5. Load into Airtable
1. Open the **Wendy File Inventory** base → **Files** table.
2. Use Airtable's CSV import (Add/paste or the CSV import extension) and map:
   `Filename → Filename`, `Source → Source`, `Full path → Full path`,
   `Extension → Extension`, `Size (MB) → Size (MB)`, `Date modified → Date modified`,
   `Content hash → Content hash`. Leave Type/Status/Duplicate blank for now.
   - Alternatively Darrell can bulk-load via the Airtable API/MCP in batches.
3. Set **Type** by extension with a quick filter+bulk-edit pass (jpg/png/heic→Photo,
   mov/mp4→Video, pdf/docx/xlsx→Document, etc.), or precompute it in the script.

## 6. Find duplicates (still no deletion)
- **Exact dupes:** group by **Content hash**. In Airtable, create a view grouped by
  Content hash; any group with >1 row = duplicates. Tag the **Duplicate?** box and a
  shared **Duplicate group** id.
- **Photo/video near-dupes** (same shot, different size/format — hashes won't match):
  run **dupeGuru** (free) or **Czkawka** on the local iCloud/Carbonite folders in
  "picture" mode; feed its groupings back into Duplicate group.
- iCloud **Photos** (not Photos in iCloud Drive) live in the Photos app library —
  use the Photos app's built-in **Duplicates** album, or export the library to a
  folder first, then include it in the scan.

## 7. Hand to Wendy for review
Wendy works the grouped view: for each duplicate group she keeps one (**Status =
Keep**) and marks the rest **Delete**. Everything else stays **Review** until she
decides its **Destination folder** (the Phase 3 taxonomy). Nothing is deleted until
she says so.

## Gotchas
- Google native Docs/Sheets/Slides have no byte hash → matched by name+size, not
  content. Don't treat a blank hash as "unique".
- HEIC/Live Photos from iPhone can appear as two files (`.heic` + `.mov`) — expected,
  not a duplicate.
- Re-running `lsjson` later is cheap; the inventory can be refreshed anytime.
