# AIVT

AIVT is a web-based diagnostic tool for evaluating value-like tendencies in AI models.

AI models often show consistent behavioral biases that resemble human value preferences. These tendencies can affect which tasks a model handles well, where it fails, and how compatible it is with different users, workflows, and decision-making styles.

AIVT helps researchers, builders, and people choosing AI tools compare models through structured prompts and interpretable profiles. The goal is to make model selection less opaque by showing not only benchmark performance, but also the model’s behavioral fit for real-world use.

---

## What AIVT Does

AIVT is inspired by 16-type personality tests, but it is not intended to claim that AI models have human personalities.

Instead, AIVT treats model behavior as observable tendencies:

* judgment style
* wording bias
* support style
* refusal tendency
* persona consistency
* task compatibility
* user-workflow fit

The first diagnostic module is planned as **AIVT-16**, a 16-type test for roughly classifying AI models and AI personas.

---

## Project Goals

AIVT aims to:

* compare value-like tendencies across AI models
* make subjective impressions easier to score and reproduce
* help users choose AI tools that fit their workflow
* help researchers and builders observe model differences
* compare raw model behavior and persona-based behavior
* track model changes across versions and dates
* provide shareable, interpretable result profiles

---

## MVP Scope

The initial MVP should focus on a simple, reliable public diagnostic flow.

Planned MVP features:

* mobile-friendly web app
* no login required for normal users
* AIVT-16 diagnostic flow
* one-question-at-a-time answering
* progress saving with local storage
* result page with type, scores, and metadata
* copyable prompts for testing AI models manually
* batch answer support using simple text, CSV, or JSON
* shareable result text or result card

The MVP should not start with a full admin system, full database workflow, or automated API evaluation unless explicitly requested.

---

## User Flow

Normal users do not need an account.

A typical user flow:

1. Select or enter the AI model name.
2. Optionally enter a persona name or memo.
3. Answer questions one by one, or copy prompts to an AI model.
4. Paste or enter the AI’s selected answers.
5. Generate a result profile.
6. Optionally share the result.
7. Optionally consent to research data storage.

Research data should only be stored when the user explicitly agrees.

---

## Developer / Admin Features

Developer and admin features are planned separately from the public user flow.

Possible future admin features:

* protected `/admin` route
* Google authentication
* question and choice editor
* version management
* update history
* developer-only model API experiments
* raw API model comparison
* temperature / parameter comparison
* model behavior logs over time

API keys must never be exposed in browser-side code.

Automated model API execution should be developer-only.

---

## Data and Privacy Policy

AIVT should avoid storing unnecessary personal data.

Initial policy:

* normal users can complete the test without login
* in-progress answers can be saved locally in the browser
* research data is saved only when the user explicitly consents
* users should not submit private, sensitive, or confidential information
* diagnostic results should be linked to the AIVT question set version

---

## Versioning

AIVT results should always be linked to the diagnostic version that produced them.

Suggested versioning:

* major version: scoring logic or test structure changed
* minor version: questions or choices changed
* patch version: typo fixes or minor wording corrections

Example:

```text
1.0.0
1.1.0
1.1.1
2.0.0
```

---

## Planned Tech Stack

Recommended initial stack:

* Next.js
* React
* TypeScript
* Vercel
* Supabase, planned for database and authentication
* localStorage for MVP answer persistence

Supabase should be added carefully, with Row Level Security and permissions considered from the start.

---

## Security Notes

This is intended to be a public repository.

Do not commit:

* `.env`
* `.env.local`
* API keys
* service role keys
* OAuth secrets
* private credentials
* production database data
* private research notes that should not be public

Admin features must be protected by authentication and server-side authorization checks, not by hidden buttons or obscure URLs.

---

## Documentation

Project notes and implementation plans are kept in `docs/`.

Recommended docs structure:

```text
docs/
  roadmap.md
  aivt-16-design.md
  input-flow-and-admin-api.md
  supabase-notes.md

docs/future/
  developer-oai-experiments.md
  agent-tooling-notes.md
```

Coding agents should read `AGENTS.md` before making changes.

---

## Development Status

AIVT is currently in early planning and MVP design.

The first priority is to build a stable public diagnostic flow before adding database-backed research storage, admin editing, or automated API experiments.
