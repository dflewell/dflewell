# Consent Conversation Script

_Run this with the executive before any access is granted. It doubles as the trust moment and as
reusable collateral. Pair it with `DATA_FLOW.md` and `DATA_HANDLING.md` (hand both over)._

## Before you start
Complete `../memory/deployment-intake.md` question 1 first: **Workspace or consumer Gmail?**
This script is written for the Assisted rung (the exec reviews everything). Adjust only if the exec
explicitly asks to start higher.

## The script

**1. Frame it.**
> "Before I touch anything, I want to walk you through exactly what this does, what it stores, and
> how you stay in control. You can stop me at any point, and you can revoke my access yourself at any
> time without involving me."

**2. The one-sentence promise.**
> "Nothing touches your inbox unless you press the button. There's no background process reading your
> mail — it runs only when you click 'Start my morning.'"

**3. What it does, in order** (show `DATA_FLOW.md`):
> "When you click the button, it: pulls your overnight unread mail, sorts it into four buckets —
> important, client, shopping, read-later — and drafts suggested replies. Then it shows you a summary.
> At this stage it only **proposes**. It does not send, delete, or move anything. You review everything."

**4. Where your data goes** (show `DATA_HANDLING.md`):
> "Three places, no more. Your mail stays in Gmail. To sort it, the text of each message is sent to
> Anthropic's Claude API — in transit only, and it's not used to train their models. And a categorized
> copy is kept in a private database that's yours alone — no sharing with any other person I work with —
> with the message bodies encrypted."

**5. How long / how to delete.**
> "I keep the categorized history so you get a durable, searchable archive — the goal is that you never
> lose an email again, so nothing is auto-deleted. But on a single request from you I'll delete your
> entire database, and you can cut off my access yourself in your Google security settings in about
> thirty seconds. I'll confirm any deletion in writing."

**6. The scope grant.**
> "I'll request read-and-modify access, but at this starting stage I only ever propose — the modify
> permission is there for later, only if and when you decide you want it. We'll move at your pace:
> review-everything now, automate more only when you ask."

**7. Explicit consent.**
> "Are you comfortable with that? Any questions before we connect your account?"

## After consent
- Note the date and what was agreed (rung, Gmail type, scopes) in the engagement record.
- Hand over `DATA_FLOW.md` + `DATA_HANDLING.md`.
- Proceed with the remaining `deployment-intake.md` steps (scope grant, isolated store, artifacts).

## The trust ladder (state explicitly; start at rung 1)
1. **Assisted** — exec clicks, tool proposes, exec reviews everything before send/move. **START HERE.**
2. **Supervised** — tool auto-handles safe categories (shopping, read-later); drafts and client mail still reviewed.
3. **Automated** — scheduled runs, minimal review. Only if the client asks.
