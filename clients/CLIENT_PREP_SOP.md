# New Client Prep — Research & Meeting SOP

Standard operating procedure for turning a **warm introduction** into a
researched, professional first meeting for **True North AI LLC**.

## Purpose
When Darrell is introduced to a prospective client, this routine gathers publicly
available intelligence on **the person** and **their company**, cross-references it
against True North's expertise, and produces a first-meeting **prep brief**.
The goal: walk in informed, credible, and with a tailored point of view.

## Positioning lens (how to "intermesh")
True North's primary offering is **AI strategy & adoption** — advising leadership on
*where* and *how* to deploy AI (use-case identification, roadmaps, build-vs-buy,
adoption). Darrell's differentiators / credibility anchors:
- **Finance depth** — inactive CMA; fluent in FP&A, unit economics, ROI/payback,
  management reporting. Lets him frame AI value in the language executives fund.
- **AWS certified** — Cloud Practitioner + AI Practitioner; can speak to feasibility,
  data/cloud readiness, and rough cost without overpromising.
- **Practitioner, not just advisor** — has personally built working AI automations
  (e.g. Gmail→Xero expense routines), so recommendations are grounded.

Every brief should end by answering: *"Given what this company does, where could AI
plausibly create value, and how does True North's mix (AI + finance + cloud) fit?"*

## Inputs (capture from the introduction)
- Person: name, role/title, company.
- Referrer + relationship (who introduced, how they know each other).
- Any context from the intro (their stated need, meeting date, format).
- Meeting logistics — if a calendar invite exists, pull it via Google Calendar
  (`list_events` / `get_event`) for time, attendees, and any agenda notes.

## Procedure
1. **Log the intake.** Note the inputs above. Confirm exact spelling of name/company
   (misspellings wreck search quality).

2. **Research the person** (use `WebSearch`, then `WebFetch` on promising results):
   - Search: `"<Full Name>" <Company>`, `"<Full Name>" LinkedIn`,
     `"<Full Name>" <Company> interview OR podcast OR article`.
   - Capture: current role & tenure, career arc, prior companies, education,
     stated focus areas, thought-leadership (posts, talks, bylined articles).
   - **LinkedIn caveat:** profile pages usually **cannot be fetched directly**
     (login wall / bot block). Rely on the **search-result snippets** and any
     cached/press coverage; don't burn time trying to scrape the profile page.
   - Note anything personal-professional that builds rapport (shared background,
     alma mater, prior industry) — but keep it professional, no private data.

3. **Research the company** (`WebSearch` + `WebFetch` the company site):
   - What they do (products/services), industry, business model, who they sell to.
   - Size signals: headcount range, revenue/funding if public, growth stage.
   - Recent news: funding, launches, leadership changes, expansion, layoffs, press.
   - **AI/tech maturity signals:** job postings (data/ML/AI roles), existing AI
     features, public statements on AI, tech stack hints, cloud provider if known.
   - Competitive/industry context: who they compete with, macro pressures.

4. **Intermesh with True North's expertise.** Synthesize research into:
   - **2–4 value hypotheses** — plausible places AI could help *this* company
     (frame in their terms: cost, speed, margin, risk, customer experience).
   - **Credibility anchors** — which of Darrell's angles (AI / finance / cloud) to
     lead with given the audience (e.g. finance framing for a CFO).
   - **Likely objections / constraints** — budget, data readiness, regulation, prior
     failed AI efforts — and a measured response to each.

5. **Prepare the meeting.**
   - **Discovery questions** — 5–8 open questions to validate the hypotheses and
     surface real pain (don't pitch; diagnose first).
   - **Talking points** — a crisp POV tailored to them; 1–2 relevant proof points.
   - **Suggested agenda** — intro/rapport → their goals → discovery → where TN could
     help → next steps.
   - **Watch-outs** — anything sensitive to avoid; unknowns to confirm live.

6. **Output the brief.** Fill `clients/BRIEF_TEMPLATE.md`. Save to **Google Drive**:
   folder path `Clients/<Company>/`, filename
   `<YYYY-MM-DD>-<Company>-prep.md` (date = meeting date if known, else today).
   Create via the Drive `create_file` tool. (Drive MCP is **create+read only** — one
   file per meeting; never expect to update in place.)
   - Cite sources inline (URLs) so claims are traceable and Darrell can dig deeper.
   - Flag anything **unverified / inferred** explicitly — do not state guesses as fact.

## Sourcing & integrity rules
- **Public information only.** Company sites, press, published articles, public
  profiles, search snippets. No paywalled scraping, no private/personal data.
- **Separate fact from inference.** Label hypotheses as hypotheses.
- **Cite as you go.** Every non-obvious claim gets a source URL in the brief.
- **Freshness.** Prefer recent sources; note the date of key facts (funding, headcount).

## Invocation
On-demand. Kick off with a prompt like:
_"New client prep per clients/CLIENT_PREP_SOP.md — I've been introduced to
<Name>, <Title> at <Company>. Meeting is <date>. Context: <what the referrer said>."_
