# Claude Code Instructions for AIVT

Claude Code must read this file before working on AIVT.

AIVT is an AI Value Tendencies Test: a web app for comparing AI model tendencies, wording bias, judgment style, persona consistency, and task fit.

## Highest priority

Do not silently destroy or rewrite the project.

Claude Code may help build the project, but user control, reversibility, and reviewability are more important than speed.

## Required workflow

For any non-trivial task:

1. Read the relevant files first.
2. Explain the current structure.
3. Propose a plan.
4. List the files likely to change.
5. Wait for user approval before broad edits.
6. Make small edits.
7. Run available checks.
8. Report changed files, commands run, results, and remaining risks.

For small typo fixes or documentation edits, direct edits are acceptable, but still report what changed.

## Do not

- Do not delete files unless explicitly instructed.
- Do not rewrite the whole app unless explicitly instructed.
- Do not replace working code with a new architecture without approval.
- Do not refactor unrelated code.
- Do not modify unrelated files.
- Do not install new dependencies without explaining why.
- Do not change authentication, database, deployment, or billing settings without approval.
- Do not run migrations without approval.
- Do not commit or push unless explicitly instructed.
- Do not claim completion without checking the result.

## Sensitive files and data

Do not read, create, print, or modify secrets unless explicitly instructed.

Treat these as sensitive:

- `.env`
- `.env.*`
- `secrets/**`
- API keys
- service role keys
- private credentials
- production database data

API secrets must never be exposed in browser-side code.

## Git rules

Before editing, check:

```bash
git status
```

Before reporting completion, check:

```bash
git diff
```

If the working tree is not clean at the start, stop and explain what changed files already exist.

Do not use destructive Git commands unless explicitly instructed.

## Supabase rules

AIVT may use Supabase.

Before creating or using tables, read:

- `docs/supabase-model-notes.md`

Important points:

- New tables may need explicit permissions before Data API access works.
- RLS and policies must be considered from the start.
- Store diagnostic results only when the user has agreed.
- Admin-only tables must not be publicly writable.
- If PostgREST returns `42501`, check database permissions and policies before assuming code is broken.

## Project docs to read first

Before implementation, read:

- `README.md`
- `docs/future-work.md`
- `docs/admin-api-and-input-flow.md`
- `docs/supabase-model-notes.md`

Then produce a staged MVP plan before editing code.

## MVP priority

Build in this order:

1. Basic diagnosis flow.
2. Answer persistence and recovery.
3. Result display.
4. Shareable result card.
5. CSV or JSON export.
6. Supabase integration.
7. Opt-in result storage.
8. Developer-only admin login.
9. Question and choice editor.
10. Version and update history.

Do not start with the full database/admin system unless the user asks.

## Browser and state handling

The quiz may become long.

Design so answers do not disappear easily when:

- the user reloads
- the user goes back
- the tab is restored
- the session is interrupted

Use local persistence first if that is the simplest MVP path.

## Model and workflow caution

Before using Claude Code features that increase autonomy, first confirm:

- current model
- effort setting
- whether Dynamic Workflow is enabled
- whether git status is clean
- exact task scope

Do not use Dynamic Workflow for the first MVP build.

Dynamic Workflow may be used later only for narrow review, audit, or planning tasks after user approval.

## Error recovery

If an error occurs, do not immediately give up.

First check:

- exact error message
- current account
- current branch
- current permissions
- whether external state changed
- whether retrying after refresh or reconnect is appropriate

Then propose the next safest action.

## Completion report format

At the end of a task, report:

- changed files
- what changed
- commands run
- test, lint, or build results
- unverified items
- known risks
- recommended next step
