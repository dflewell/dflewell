# Setup

_Last updated: 2026-06-12_

## Prior builds (experience baseline)
- ~10 Claude Cowork projects for personal use.
- Email monitoring tool for accounting (built with Claude Code) — reusable pattern for
  email access; check how provider auth was handled there before re-solving it.
- Chess tracker web app (Claude Code).

## Cloud / tooling
- AWS background available (Cloud Practitioner, AI Practitioner). S3 + a search layer is a
  viable data-store path if cloud is chosen over local SQLite.

## Open setup decisions
- Data-store location for the email archive: local (SQLite) vs cloud (AWS). TBD.
- Where AI inference happens on email content (privacy-sensitive). TBD.

## Business
- Operates **True North AI LLC** — consulting practice with a governance focus.
- Email project is a showcase/trust-builder for that practice, not a product line.
