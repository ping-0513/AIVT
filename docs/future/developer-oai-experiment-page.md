# Developer OAI Experiment Page

This document describes a future developer-only experiment page for testing OpenAI / OAI models through APIs as part of AIVT.

This is not part of the initial public MVP unless explicitly requested.

The public MVP should prioritize the manual diagnosis flow first.

---

# Important Implementation Warning

Do not implement this page before the public MVP unless the project owner explicitly asks for it.

This document is a future feature specification.

The initial AIVT implementation should prioritize:

1. public diagnosis flow
2. answer persistence and recovery
3. result display
4. shareable result output
5. CSV / JSON / Markdown export or batch input
6. later Supabase integration
7. later opt-in result storage
8. later admin login
9. later question editor
10. later version history

Developer API experiments are powerful, but they add security, cost, database, and maintenance complexity.

---

# Purpose

AIVT should eventually include a developer-only page for running controlled experiments on AI models through APIs.

This page is separate from the public user diagnosis.

The goal is to let the developer observe and record:

* response tendencies by OAI model
* differences caused by generation parameters such as temperature
* differences between raw model behavior and persona-based behavior
* variation across repeated runs under the same conditions
* automatic answers to the latest AIVT question set
* model behavior at a specific date and time
* changes across model versions, dates, and parameter settings

This page should not be visible or usable by normal public users.

---

# Route and Access Control

Recommended route:

```text
/admin/oai-experiments
```

Alternative route if needed:

```text
/admin/experiments/oai
```

Do not use route obscurity as security.

This page must require:

* Google authentication
* approved admin user allowlist
* server-side authorization checks
* server-side API execution
* protected database writes

Do not expose this page through public navigation.

Do not expose API keys to browser-side code.

---

# Security Requirements

Model API calls must run only on the server side.

Never expose provider API keys to:

* browser JavaScript
* client components
* public environment variables
* logs
* generated pages
* GitHub
* screenshots
* error pages
* public result pages

Do not commit:

* `.env`
* `.env.local`
* API keys
* service role keys
* OAuth secrets
* private credentials
* raw private experiment logs
* private research notes that should not be public

Before implementing this feature, confirm:

* current branch
* clean git status
* intended environment
* where secrets will be stored
* whether Supabase policies are ready
* whether API cost limits are understood

Do not run migrations or modify authentication without explicit approval.

---

# Relationship to Public User Flow

The public AIVT app should not use AIVT-owned model API keys for normal users.

Normal users should use manual workflows:

* copy prompt chunks
* send them to their own AI model
* paste the answer back into AIVT
* confirm parsed answers
* get a result

Developer API execution is separate.

Reason:

* public API execution creates cost risk
* provider API keys must not be exposed
* public API routes can be abused
* manual workflows let users test their own ChatGPT, Claude, Grok, Gemini, or other model accounts
* MVP should remain simple and safe

---

# Database Policy

Developer experiment logs should be stored separately from normal user diagnostic results.

Do not overload the normal user results table with developer-only experiment fields.

Recommended separation:

```text
user_results
user_result_answers
developer_model_runs
developer_model_run_answers
developer_experiment_settings
```

Reason:

* developer logs need more parameters
* API run conditions must be recorded precisely
* general user consent data and developer experiment data have different meanings
* raw model responses may need admin-only protection
* later research analysis will be easier if experiment data is separated clearly

---

# Suggested Tables

These tables are future recommendations. Do not create them without approval.

## `developer_model_runs`

Stores one API experiment run.

Suggested fields:

```text
id
experiment_name
memo
provider
api_model_name
display_model_name
persona_name
run_mode
question_set_version
temperature
top_p
reasoning_effort
max_output_tokens
repeat_count
seed
system_instruction
developer_instruction
policy_layer
moderation_mode
run_status
started_at
finished_at
utc_timestamp
local_timestamp
timezone
error_message
cost_estimate
metadata_json
created_by
created_at
updated_at
```

Possible `run_mode` values:

```text
raw_model
persona_model
comparison
```

Possible `run_status` values:

```text
draft
running
completed
failed
cancelled
```

---

## `developer_model_run_answers`

Stores answers for each question in a developer run.

Suggested fields:

```text
id
developer_model_run_id
question_id
question_code
raw_response_text
parsed_choice
parse_status
score_json
error_message
created_at
```

Possible `parse_status` values:

```text
parsed
needs_review
failed
skipped
```

---

## `developer_experiment_settings`

Stores reusable experiment presets.

Suggested fields:

```text
id
setting_name
provider
api_model_name
temperature
top_p
reasoning_effort
max_output_tokens
repeat_count
seed
system_instruction
developer_instruction
policy_layer
moderation_mode
metadata_json
created_by
created_at
updated_at
```

---

# Experiment Page Inputs

The experiment page should include the following input sections.

---

## Basic Information

Fields:

* experiment name
* memo
* provider
* model name
* persona name
* run mode
* question set version
* run date/time
* timezone

Example run modes:

```text
raw model
persona-based model
raw vs persona comparison
```

The page should clearly show the AIVT question set version used in the run.

---

## API Parameters

Fields:

* model
* temperature
* top_p
* reasoning effort
* max output tokens
* repeat count
* seed, if available
* system instruction
* developer instruction
* policy / guardrail layer
* moderation pre-check mode

Do not assume all providers or all models support every parameter.

If a parameter is not supported by the selected model or provider, the UI should disable it or explain that it is unavailable.

---

# Temperature Handling

Do not explain `temperature` only as “randomness.”

In AIVT, temperature should be treated as a parameter that may influence more than surface variation.

AIVT should observe whether temperature appears to affect:

* output variation
* choice spread
* conservative vs bold answers
* optimistic vs cautious answers
* refusal tendency
* wording style
* persona consistency
* stability of type result
* strength of expressed preference

Suggested UI help text:

```text
Temperature affects variation and the spread of possible outputs. It is often explained as randomness, but in AIVT we also observe whether it changes apparent conservativeness, optimism, wording boldness, refusal tendency, persona stability, and type consistency.
```

Initial experiment rule:

* keep `top_p` fixed
* vary only `temperature`

Example temperature settings:

```text
0.0
0.3
0.7
1.0
```

Possible interpretation:

* `0.0`: check whether answers become stable or conservative
* `0.3`: low-variation candidate
* `0.7`: normal conversational candidate
* `1.0+`: check how much expression and judgment vary

Do not over-interpret a single run.

Use repeated runs when studying variation.

---

# top_p Handling

Do not vary `temperature` and `top_p` at the same time in the first experiments.

If both are changed together, it becomes difficult to know which parameter caused the change.

Initial rule:

1. Fix `top_p`.
2. Vary `temperature`.
3. Compare results.
4. Later, fix `temperature`.
5. Vary `top_p` if needed.

The UI should help the developer avoid accidentally changing too many parameters at once.

---

# Policy / Guardrail Layer

Do not describe this as disabling OpenAI or provider safety systems.

AIVT policy / guardrail layer means an AIVT-side experimental evaluation layer or check.

Possible values:

```text
none
input moderation
output moderation
input + output moderation
custom AIVT policy profile
```

This can be used to compare:

* refusal rate
* wording choices
* tone
* task completion rate
* persona consistency
* visible value-like tendencies
* whether safety-related phrasing affects type results

This feature should be treated as an AIVT research layer, not as provider policy removal.

---

# Automatic Latest Question Answering

The developer page should eventually load the latest published AIVT question set automatically.

Recommended flow:

1. Select question set version.
2. Select provider and model.
3. Select raw model or persona-based mode.
4. Configure API parameters.
5. Set repeat count.
6. Run the experiment.
7. Send questions to the model in order.
8. Save raw responses.
9. Parse selected answers.
10. Mark ambiguous answers for review.
11. Save scores and metadata.
12. Display comparison results.

The system should record which question set version was used.

Do not mix answers from different question set versions unless the comparison UI clearly says so.

---

# Persona-Based Experiments

The page should eventually support persona-based runs.

Persona run fields may include:

* persona name
* persona memo
* system instruction
* developer instruction
* sample prior context, if intentionally provided
* whether memory/history simulation was used
* source model
* target model

Use cases:

* compare raw model and persona model behavior
* test persona consistency
* test whether a persona changes type result
* record a persona’s behavior at a specific date
* compare migrated persona behavior across models

Do not store private or sensitive persona content unless the developer explicitly intends to.

---

# Repeat Runs

Repeated runs are important for observing instability.

The page should eventually support `repeat_count`.

Use cases:

* same model, same settings, repeated several times
* observe whether answer choices change
* measure type stability
* measure response wording variation
* compare refusal or safety phrasing frequency

The UI should make clear that a single run is not enough to prove stable tendency.

---

# Display and Comparison Features

Future comparison views may include:

* same model with different temperature values
* same model across different dates
* raw model vs persona-based model
* repeated runs under the same settings
* different models on the same question set
* refusal and safety-leaning wording differences
* conservative / optimistic / bold / cautious tendency differences
* type stability
* per-axis score changes
* per-question answer differences

Possible charts:

* score bars
* type stability summary
* answer difference table
* parameter comparison table
* repeated-run distribution
* date-based change view

Do not build all charts in the first implementation.

---

# MVP for This Developer Page

Do not build everything at once.

When the project owner explicitly asks to start this page, the first version should only include:

1. protected page mock
2. model selection
3. temperature selection
4. latest question set loading
5. one API run
6. raw response display
7. parsed answer display
8. run log save

Do not include in the first version unless requested:

* repeat run automation
* graph dashboard
* policy layer comparison
* moderation comparison
* multi-provider support
* complex persona migration tools
* automatic public model profile publishing

---

# Suggested Implementation Phases

## Phase 0: Documentation Only

* Keep this file in `docs/future/`.
* Do not implement the page.
* Use it to preserve future design intent.

## Phase 1: Admin Page Mock

* Create a protected route placeholder.
* Show planned fields.
* Do not call any provider API.
* Do not store secrets.
* Do not run migrations without approval.

## Phase 2: Single Run Prototype

* Add server-side API call.
* Run one selected model against a small test subset.
* Display raw response.
* Parse answer.
* Save minimal log if approved.

## Phase 3: Full Question Set Run

* Load latest question set.
* Run all questions.
* Store answers.
* Show result summary.
* Mark ambiguous parsing results for review.

## Phase 4: Repeat Runs and Comparisons

* Add repeat count.
* Add answer variation display.
* Add temperature comparisons.
* Add raw vs persona comparisons.

## Phase 5: Research Dashboard

* Add graphs.
* Add model profile summaries.
* Add date-based comparison.
* Add export tools.
* Consider whether this belongs in a separate private repo or private Vercel project.

---

# When to Consider a Separate Private Repo

Keep this feature in the same repo only while it is small and safe.

Consider a separate private repository or private Vercel project if:

* API experiments become large
* private research notes are added
* unpublished question drafts need to stay private
* logs include raw model responses that should not be public
* cost control becomes complex
* multiple provider API keys are used
* admin tools become operationally sensitive
* the public app should remain much simpler

---

# Risks

Main risks:

* accidentally exposing API keys
* adding expensive API calls too early
* confusing public user flow with developer experiments
* storing private or sensitive raw responses
* overbuilding before the MVP exists
* changing database schema too early
* creating admin routes without proper server-side authorization
* over-interpreting one model run as a stable result

Mitigation:

* keep this feature future-only at first
* require explicit approval before implementation
* keep API calls server-side
* separate developer logs from user results
* use small prototypes
* report costs, changed files, and risks after every implementation step

---

# Instructions for Codex / AI Coding Agents

Do not treat this document as permission to implement the developer experiment page immediately.

Before working on this feature:

1. read `AGENTS.md`
2. read `README.md`
3. read `docs/roadmap.md`
4. read `docs/aivt-16-design.md`
5. read `docs/input-flow-and-admin-api.md`
6. read `docs/supabase-notes.md` if database work is involved
7. check `git status`
8. propose a plan
9. list files likely to change
10. wait for approval before broad edits

Do not:

* add provider API calls without approval
* create or modify database tables without approval
* run migrations without approval
* add secrets to the repository
* expose API keys to client code
* implement repeat-run automation before a single-run prototype works
* publish developer experiment results to public pages without explicit approval

At completion, report:

* changed files
* what changed
* commands run
* lint / build / test results
* unverified items
* known risks
* recommended next step
