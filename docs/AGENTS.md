# AGENTS.md

This file contains instructions for Codex and other AI coding agents working on AIVT.

AIVT is an AI Value Tendencies Test: a web app for comparing AI model tendencies, wording bias, judgment style, persona consistency, and task fit.

## Highest Priority

Do not silently destroy, rewrite, or over-simplify the project.

User control, reversibility, and reviewability are more important than speed.

Do not summarize away project intent. Details that look informal, repetitive, or minor may still be important to the project owner.

## Required Workflow

For any non-trivial task:

1. Read the relevant files first.
2. Explain the current structure.
3. Propose a plan.
4. List the files likely to change.
5. Wait for user approval before broad edits.
6. Make small, focused edits.
7. Run available checks.
8. Report changed files, commands run, results, remaining risks, and recommended next step.

For small typo fixes or small documentation edits, direct edits are acceptable, but still report what changed.

## Do Not

* Do not delete files unless explicitly instructed.
* Do not rewrite the whole app unless explicitly instructed.
* Do not replace working code with a new architecture without approval.
* Do not refactor unrelated code.
* Do not modify unrelated files.
* Do not install new dependencies without explaining why.
* Do not change authentication, database, deployment, or billing settings without approval.
* Do not run migrations without approval.
* Do not commit or push unless explicitly instructed.
* Do not claim completion without checking the result.
* Do not implement future/admin/API experiment features before the public MVP unless explicitly requested.

## Sensitive Files and Data

Do not read, create, print, or modify secrets unless explicitly instructed.

Treat these as sensitive:

* `.env`
* `.env.*`
* `.env.local`
* `secrets/**`
* API keys
* service role keys
* OAuth secrets
* private credentials
* production database data
* private research notes that should not be public

API secrets must never be exposed in browser-side code.

## Git Rules

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

## Project Docs to Read First

Before implementation, read:

* `README.md`
* `docs/roadmap.md`
* `docs/aivt-16-design.md`
* `docs/input-flow-and-admin-api.md`

Before database or Supabase work, also read:

* `docs/supabase-notes.md`

Future developer-only experiments are documented separately and should not be implemented during the initial public MVP unless requested:

* `docs/future/developer-oai-experiments.md`

## Product Direction

AIVT is the overall project.

AIVT-16 is the first diagnostic module.

AIVT-16 should preserve these ideas:

* 16-type diagnostic structure.
* 31-question initial question set.
* Four-choice questions.
* Q-FINAL as a special final question.
* Result page with type code, nickname, catch copy, score bars, tags, Q-FINAL comment, reproduction prompt, copy function, retry option, and sharing.
* Versioned question sets.
* localStorage-based progress recovery.
* Manual input and batch input support.

Do not treat AIVT-16 as the whole project. It is the first module inside the larger AIVT project.

## MVP Priority

Build in this order unless the user changes the priority:

1. Basic public diagnosis flow.
2. Answer persistence and recovery.
3. Result display.
4. Shareable result card or shareable result text.
5. CSV / JSON / Markdown export or batch input support.
6. Supabase integration.
7. Opt-in result storage.
8. Developer-only admin login.
9. Question and choice editor.
10. Version and update history.

Do not start with the full database/admin/API system unless the user asks.

## User Flow Rules

Normal users should not need login.

Normal users should not directly use model API keys through the public app.

The public MVP should prioritize manual workflows:

* user selects or enters model name
* user optionally enters persona name or memo
* AIVT shows questions or prompt chunks
* user sends prompts to their own AI model
* user pastes or enters the AI answer back into AIVT
* AIVT records the selected choices
* AIVT displays the result
* data is saved only if the user explicitly consents

API-based automatic model execution is developer-only.

## Browser and State Handling

The quiz may become long.

Design so answers do not disappear easily when:

* the user reloads
* the user goes back
* the tab is restored
* the session is interrupted

Use local persistence first if that is the simplest MVP path.

## Supabase Rules

AIVT may use Supabase, but do not add it before the MVP needs it.

Before creating or using Supabase tables, read:

* `docs/supabase-notes.md`

Important points:

* New tables may need explicit permissions before Data API access works.
* RLS and policies must be considered from the start.
* Store diagnostic results only when the user has agreed.
* Admin-only tables must not be publicly writable.
* If PostgREST returns `42501`, check database permissions and policies before assuming code is broken.
* Do not run migrations without approval.

## Admin and Developer Features

Admin features should be protected by authentication and server-side authorization.

Do not rely on:

* hidden buttons
* obscure URLs
* client-side route guards only

Developer-only model API experiments should be separate from the normal user flow.

Future API experiment features may include:

* raw model runs
* persona-based runs
* temperature comparison
* top_p comparison
* repeat count comparison
* model behavior logs over time

Do not implement these before the public MVP unless explicitly requested.

## Code Style and Comments

Write code that is understandable to a Japanese-speaking beginner.

Prefer clear, boring, maintainable code over clever code.

Add comments where they help explain:

* file responsibility
* temporary implementation choices
* scoring logic
* localStorage behavior
* security-sensitive behavior
* future replacement points

Example:

```ts
// このファイルはAIVT-16の質問データを扱います。
// 将来的にSupabaseから取得する予定ですが、MVPではローカルデータを使います。
```

## Error Recovery

If an error occurs, do not immediately give up.

First check:

* exact error message
* current branch
* current permissions
* current account
* whether external state changed
* whether retrying after refresh or reconnect is appropriate

Then propose the next safest action.

## Completion Report Format

At the end of a task, report:

* changed files
* what changed
* commands run
* lint / build / test results
* unverified items
* known risks
* recommended next step
