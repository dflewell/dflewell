# Deployment Intake Checklist (per executive)

_Last updated: 2026-06-12_

Run before any access or data handling. Doubles as the governance/consent conversation.

1. **Gmail type — ask first.** Workspace (custom domain) or consumer @gmail.com?
   - Workspace → service account + domain-wide delegation, authorized by their Workspace admin.
   - Consumer → button-initiated consumer OAuth (avoid CASA; exec re-auths at click-time if needed).
2. **Consent conversation.** Walk through: what is stored, where, how long, how it's deleted,
   where inference happens (Claude API), and that nothing acts without their button press.
3. **Scope grant.** Read/modify only; document exactly what was granted; confirm they can revoke.
4. **Isolated store.** Provision a dedicated encrypted SQLite DB for this exec — no commingling.
5. **Trust ladder rung.** Confirm starting at "Assisted" (review everything) unless they ask otherwise.
6. **Hand over artifacts.** Data-flow diagram + "what we store / where / how long / how to delete" sheet.
