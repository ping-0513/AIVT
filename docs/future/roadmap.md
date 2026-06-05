# AIVT Roadmap

This document defines the development roadmap for AIVT.

It should be read by Codex and other AI coding agents before implementation planning.

The roadmap is intentionally staged. Do not try to build everything at once.

---

# Core Principle

Build a stable public MVP first.

AIVT has many possible future features, including admin tools, Supabase-backed research storage, model API experiments, graph comparison, version history, and multilingual support.

However, the first priority is a reliable public diagnostic experience that does not break easily.

The initial implementation should focus on:

* public diagnosis flow
* answer persistence and recovery
* result display
* shareable output
* basic export
* clear version awareness

Do not start with the full database, full admin system, or automated model API experiments unless explicitly requested.

---

# Development Order

Build in this order unless the project owner changes the priority.

## 1. Build the MVP diagnosis flow

Create the basic public diagnosis flow.

This should include:

* question display
* answer selection
* model name input
* optional persona name or memo
* basic navigation through questions
* final submission to generate a result

The public MVP should work without login.

---

## 2. Add answer persistence and recovery

The test may become long, so answers must not disappear easily.

Add recovery behavior for:

* reload
* browser back
* tab restore
* interrupted session

Use `localStorage` for MVP if that is the simplest stable approach.

Save at least:

* current question or progress position
* selected answers
* selected model name
* optional persona name or memo
* selected AIVT version
* timestamp of saved progress

---

## 3. Build the result display

Create a result page after the user completes the diagnosis.

The result should show:

* type code
* type name or nickname
* short description
* score summary
* model name
* persona name or memo if provided
* diagnosis date/time
* timezone
* question set version
* AIVT version

Do not hide the version metadata, because reproducibility matters.

---

## 4. Create a shareable result card

Create a result format that is fun and easy to share.

This may include:

* SNS-friendly text
* visual result card
* type-specific color or background
* digital / AI-like visual style
* copy button
* image save support if practical

The result should be enjoyable for general users while still credible for research-oriented users.

---

## 5. Add CSV / JSON export

Add export options for users who want to keep or analyze their results.

Recommended formats:

* JSON for structured data
* CSV for spreadsheet workflows
* Markdown or plain text for easy sharing and review

Export should include:

* AIVT version
* question set version
* selected answers
* result type
* score data
* model metadata
* persona metadata if provided
* timestamp
* timezone

---

## 6. Add Supabase

Add Supabase only after the local MVP flow is stable enough.

Supabase may be used for:

* database
* authentication
* research-consented result storage
* admin user management
* question and choice management
* update history
* version management

Before implementing Supabase work, read:

* `docs/supabase-notes.md`
* `AGENTS.md`

Do not run migrations or modify database policies without approval.

---

## 7. Save diagnosis results only with consent

Normal users should be able to use AIVT without login and without contributing research data.

If the user explicitly consents, save diagnostic data for research.

If the user does not consent, avoid storing research data.

Consent-based stored data may include:

* model name
* persona name or memo if provided
* memory/history flags
* AIVT version
* question set version
* answers
* score data
* result type
* timestamp
* timezone

Do not store unnecessary personal information.

Do not ask for precise location.

Use time and timezone, not geolocation.

---

## 8. Add developer-only Google authentication

Developer/admin pages should require Google authentication.

Admin access should be limited to approved accounts.

Do not rely on:

* hidden buttons
* obscure routes
* client-side checks only

Admin authorization must be checked server-side.

---

## 9. Add question and choice editing from the admin page

Create an admin UI that allows editing:

* questions
* choices
* order
* active/inactive state
* Japanese text
* future English text
* scoring metadata if needed

The admin editor should not corrupt already-published historical versions.

Prefer draft editing and version publishing over direct mutation of published question sets.

---

## 10. Add version management for question sets and scoring logic

AIVT results must be tied to the version that produced them.

Versioning should apply to:

* question sets
* choices
* scoring logic
* type definitions
* result text if it changes meaningfully

Suggested semantic versioning:

* major version: large diagnostic design changes
* minor version: question additions, choice changes, UI changes that affect answering, scoring adjustments
* patch version: typo fixes, small wording corrections, minor display fixes

Example:

```text
1.0.0
1.0.1
1.1.0
2.0.0
```

---

## 11. Create an update history page

Create a public update history page.

It should show users:

* what changed
* when it changed
* which AIVT version changed
* whether the change affects scoring
* whether the change is only wording or UI

This helps users understand why results may differ between versions.

---

## 12. Allow update history registration from both UI and code

Later, support update history entries from:

* admin UI
* code-side changes
* release notes
* migration-related updates

This should help keep the public version history aligned with the actual implementation.

---

## 13. Add graphs, tags, and day-by-day variation comparison

After the MVP and versioning are stable, add richer analysis.

Possible features:

* score graphs
* type tags
* per-axis score bars
* day-by-day result changes
* model update comparison
* raw model vs persona comparison
* repeated-run variation
* model family comparison

Do not build advanced graph dashboards before the basic result flow is stable.

---

## 14. Add English support

Add English support after the Japanese MVP is stable.

Future multilingual behavior:

* Japanese and English text fields
* language switcher
* globe icon for language switching
* ability to switch language at any time
* translated questions
* translated choices
* translated result text
* translated documentation where useful

Do not make multilingual support block the first MVP unless requested.

---

## 15. Prepare for public release, applications, and demos

Before public release or campaign submission, prepare:

* polished README
* demo flow
* screenshots
* example results
* usage explanation
* privacy explanation
* version history
* known limitations
* public deployment
* basic usage data if available
* explanation of why AIVT is useful

This may be useful for public sharing, research explanation, and developer campaigns.

---

# Important Implementation Notes

## Do not build everything at once

The project has a wide scope, but the first implementation should be narrow.

Prioritize a stable MVP over a large unfinished system.

## Protect user progress

The test may have many questions.

The app should protect against losing answers when:

* the user reloads
* the user presses back
* the browser restores the tab
* the session is interrupted

For MVP, use localStorage first.

Database-backed progress can be added later.

## Store time and timezone, not location

Results should record:

* diagnosis timestamp
* timezone
* question set version
* model name
* persona name if provided

Do not use geolocation for this.

AIVT does not need the user’s physical location.

## Support both fun sharing and structured export

AIVT should support both:

* SNS-friendly result sharing
* CSV / JSON / Markdown data export

The fun share format helps users enjoy the tool.

The structured export helps reproducibility and research.

## English support is future work

English support is planned, but not required for the first MVP unless the project owner changes the priority.

---

# Versioning Policy

Use a version format like:

```text
1.0.2
```

Recommended meaning:

## Patch version

The third number is for small updates.

Examples:

* typo fixes
* small wording corrections
* minor text cleanup
* small display corrections that do not affect diagnosis meaning

Example:

```text
1.0.1
```

## Minor version

The second number is for medium updates.

Examples:

* question additions
* question edits
* choice edits
* UI improvements that affect answering
* diagnostic logic adjustments
* new export options
* meaningful result display improvements

Example:

```text
1.1.0
```

## Major version

The first number is for large updates.

Examples:

* major diagnostic design change
* scoring system redesign
* type system redesign
* changes that make old and new results difficult to compare directly

Example:

```text
2.0.0
```

---

# Instructions for Codex / AI Coding Agents

Before implementing anything, read:

* `AGENTS.md`
* `README.md`
* `docs/roadmap.md`
* `docs/aivt-16-design.md`
* `docs/input-flow-and-admin-api.md`

Before database work, also read:

* `docs/supabase-notes.md`

Do not begin by implementing the entire roadmap.

For any broad change, first report:

* files likely to change
* implementation plan
* impact on database design
* impact on answer persistence
* security concerns
* assumptions
* open questions

After implementation, report:

* changed files
* what changed
* commands run
* lint result
* build result
* test result if available
* unverified items
* known risks
* recommended next step

Do not run migrations, change authentication, add provider API calls, commit, or push unless explicitly approved.

---

# Current Priority

The current priority is:

1. public MVP diagnosis flow
2. local answer persistence
3. result display
4. share/export
5. then database and admin features

Keep the implementation small, reversible, and reviewable.
