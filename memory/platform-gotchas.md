# Platform Gotchas (Claude.ai Projects + Claude Code)

_Last updated: 2026-06-12_

## Where things live (this engagement)
- **Claude.ai Project** = home for planning + this `memory/` set (Project knowledge + instructions).
- **Claude Code** = home for the actual codebase; drop the same `memory/` files into the repo
  (e.g. `/memory` or `/docs`) so the coding agent reads the same context.
- **Cowork** = NOT used here. Desktop-only, on the personal account; client work stays separate.

## Gotchas
- **Project description/instructions field is not reliably surfaced as "scope."** Text written
  into a Claude.ai Project's description doesn't always reach the model as labeled scope. Paste
  or upload key scope/requirements directly into the conversation instead of relying on the field.
- **Memory write-back is manual.** The assistant can read the `memory/` files at session start but
  cannot silently save changes back. When a file is updated mid-session, re-save the new version
  into the Project knowledge / repo (overwriting the old).
- **Sandbox filesystem resets between tasks.** Files created in the working directory during a
  session don't persist. Anything durable must be kept by the user (Project knowledge or repo).
