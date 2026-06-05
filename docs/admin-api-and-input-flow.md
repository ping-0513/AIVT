# Input Flow and Admin API Design

This document defines how AIVT separates the public user diagnosis flow from developer-only model API features.

AIVT should support both:

* a public, manual, login-free diagnosis flow for normal users
* protected developer/admin features for API-based model experiments

These two flows must be clearly separated.

---

## Core Decision

For the initial version, do not split the project into multiple repositories.

Use the same AIVT repository, but separate the routes and permissions:

* Public user pages:

  * normal public routes
  * no login required
  * no model API access
* Developer/admin pages:

  * protected `/admin` routes
  * Google authentication required
  * approved admin users only
* Model API execution:

  * server-side only
  * never expose API keys to the browser

Changing the URL is not security.

Security must come from:

* authentication
* authorization
* server-side checks
* environment variables
* Supabase Row Level Security if Supabase is used

---

## Repository Separation Policy

### Initial Phase

Use one public repository.

Reasons:

* Faster MVP development.
* Easier for Codex / AI coding agents to understand the whole app.
* Easier to keep public pages, question data, result logic, and admin tools consistent.
* Splitting too early can slow down development before the architecture is stable.

### Future Split Conditions

Consider a separate private repository or separate private Vercel project later if:

* admin tools become large
* developer-only features should remain private
* deployment permissions need to be fully separated
* automated API evaluation becomes expensive or operationally sensitive
* private research notes, unpublished question drafts, or API experiment logs should not live in the public repository
* provider API keys or model evaluation workflows become central to the admin system

---

# Public User Flow

## Principle

Normal users should not directly use AIVT-owned model API keys.

Reasons:

* API cost control is difficult.
* API keys cannot be exposed.
* Public API execution can be abused.
* The MVP should prioritize a simple and safe manual experience.
* Users may want to test models they personally use, including ChatGPT, Claude, Grok, Gemini, or other tools.

The public version should be a manual diagnostic tool first.

---

## Public User Input Methods

AIVT should support several manual input methods.

---

## Option A: Copy Prompt Chunks to the User’s AI

AIVT shows a small chunk of questions, such as 3 questions at a time.

The user copies the prompt, sends it to their own AI model, then brings the model’s answer back to AIVT.

### Benefits

* Simple to implement.
* No AIVT API cost.
* Users can test the AI service they already use.
* Works across ChatGPT, Claude, Grok, Gemini, and other models.
* Good for MVP.

### Downsides

* Requires user effort.
* Copy/paste mistakes may happen.
* Long tests may cause drop-off.
* The app needs clear instructions.

### MVP Decision

Use this method as one of the main MVP flows.

---

## Option B: Screenshot / Visual Question Flow

AIVT displays questions like a quiz site.

The user may show the screen or screenshot to an AI model and use the AI’s answer to continue the test.

### Benefits

* Feels playful and visual.
* Can test how models respond to visual input.
* May be interesting as a future experiment.

### Downsides

* Image recognition can introduce noise.
* The model may misread the question or choices.
* Screenshot-based workflows are heavy for users.
* The data is harder to structure.
* Results may be less reproducible.

### MVP Decision

Do not prioritize this for the initial MVP.

Keep it as a future or experimental idea.

---

## Option C: Paste AI Response into AIVT

AIVT gives the user one or more questions.

The user asks their AI model to answer.

The user pastes the AI’s response into AIVT.

AIVT then either:

* parses the answer automatically, or
* asks the user to confirm the selected choices manually.

### Benefits

* More structured than pure copy/paste.
* Useful for saving or exporting data.
* Easier to record model name, persona name, and answer metadata.
* Works well with CSV / JSON / Markdown workflows.

### Downsides

* Requires careful UI design.
* Needs validation and error handling.
* AI responses may be inconsistent.
* The app must handle ambiguous answers safely.

### MVP Decision

Use Option A and Option C together.

Recommended MVP flow:

1. AIVT shows 3 questions at a time.
2. User copies the prompt.
3. User sends it to their own AI model.
4. User pastes the AI’s response back into AIVT.
5. AIVT tries to parse the answers.
6. User confirms or corrects parsed choices.
7. AIVT records the selected choices.
8. AIVT continues to the next chunk.

---

# Recommended Public MVP Flow

The initial public MVP should work like this:

1. User selects or enters the model name.
2. User optionally enters persona name or memo.
3. User optionally records whether memory or history reference was enabled.
4. AIVT shows questions in small chunks.
5. Default chunk size is 3 questions.
6. User copies the prompt chunk.
7. User sends the prompt to their own AI model.
8. User pastes the model response into AIVT.
9. AIVT parses or helps the user select answers.
10. AIVT saves progress locally.
11. User completes all questions.
12. AIVT displays the result.
13. User may share the result.
14. User may export data.
15. User may consent to research data storage.
16. If the user does not consent, the result should not be stored as research data.

Automated model API execution is developer-only.

---

# Prompt Chunking

## Default Chunk Size

Use 3 questions per prompt chunk for MVP.

Reason:

* Small enough for weaker models.
* Easier to review manually.
* Reduces context and formatting errors.
* Easier for users to correct mistakes.
* Works well with the original user-input flow idea.

## Future Chunk Size Options

Later, allow users to choose chunk size:

* 1 question
* 3 questions
* 5 questions
* 10 questions
* all questions

Possible presets:

* conservative / weak model
* standard model
* long-context model
* custom chunk size

---

# Prompt Format

The prompt shown to users should be clear and strict.

It should include:

* AIVT name
* AIVT version
* model/persona context if provided
* question IDs
* question text
* four choices
* instruction to choose exactly one choice per question
* required output format
* warning not to skip questions
* warning not to answer as an ideal human
* instruction to answer based on the model’s own behavioral tendency

Recommended output format:

```json
[
  { "question_id": "Q001", "choice": "A" },
  { "question_id": "Q002", "choice": "C" },
  { "question_id": "Q003", "choice": "D" }
]
```

Also support a simple text fallback:

```text
Q001:A
Q002:C
Q003:D
```

---

# AI Response Parsing

AIVT should support multiple pasted answer formats.

## Supported MVP Formats

### JSON

```json
[
  { "question_id": "Q001", "choice": "A" },
  { "question_id": "Q002", "choice": "C" }
]
```

### Simple Text

```text
Q001:A
Q002:C
```

### CSV-like Text

```csv
question_id,choice
Q001,A
Q002,C
```

## Parsing Rules

The parser should validate:

* question ID exists
* choice exists
* no duplicate question IDs
* required questions in the chunk are answered
* invalid lines are shown to the user
* ambiguous answers require user confirmation

The parser should not silently guess important answers.

If parsing is uncertain, show the user what was detected and ask for confirmation.

---

# Progress Persistence

The test may become long, so progress must not disappear easily.

Use localStorage for MVP.

Save:

* selected model
* persona name or memo
* memory/history flags
* current question or chunk
* answers already recorded
* selected AIVT version
* timestamp of saved progress

The app should recover progress if:

* the page reloads
* the browser tab is restored
* the user navigates back
* the session is interrupted

Provide clear controls:

* continue saved diagnosis
* restart diagnosis
* clear saved progress

---

# Research Consent

Normal users can complete the diagnosis without contributing research data.

Research data should only be stored when the user explicitly consents.

If consent is checked, AIVT may store:

* selected model metadata
* persona name or memo, if provided
* memory/history flags
* AIVT version
* answers
* result type
* score data
* timestamp
* timezone

If consent is not checked:

* show the result locally
* allow sharing/export
* avoid storing research data unless another feature explicitly requires it

Warn users not to submit private, sensitive, or confidential information.

---

# Developer / Admin Flow

Developer-only features should live under protected admin routes.

Recommended route:

```text
/admin
```

Avoid using `/dev` for the main protected route in production-facing documentation, because it may imply a development-only environment.

Possible future route:

```text
/admin/oai-experiments
```

---

## Admin Authentication

Admin pages require:

* Google authentication
* approved user allowlist
* server-side authorization checks

Do not rely on:

* hidden buttons
* obscure URLs
* client-side checks only

Admin authorization should be checked before:

* reading developer-only data
* running model API experiments
* writing experiment logs
* editing questions
* editing choices
* publishing versions
* changing scoring logic

---

# Developer Model API Features

Developer-only pages may later use model APIs to run controlled experiments.

Developer API features may include:

* load latest question set
* select model
* run the model through questions
* record raw model answers
* record persona-based model answers
* save model behavior at a specific date/time
* record model name
* record persona name
* record run timestamp
* record timezone
* record question set version
* compare answer differences
* compare raw model and persona model behavior
* compare the same model across dates
* compare repeat runs under the same settings

These features should not be part of the public MVP unless explicitly requested.

---

# Developer API Security

Model API calls must be server-side only.

Never expose API keys to:

* browser JavaScript
* public environment variables
* client components
* logs
* generated pages
* GitHub

Use server-only environment variables.

Do not commit:

* `.env`
* `.env.local`
* API keys
* service role keys
* OAuth secrets
* private credentials

---

# Data Separation

Public user results and developer experiment logs should be treated as different types of data.

Public user data:

* consent-based
* simpler metadata
* designed for user-facing results
* should avoid personal data

Developer experiment data:

* more detailed
* records API parameters
* records experiment conditions
* may include raw model responses
* should be admin-only
* may belong in separate tables

Recommended future separation:

```text
user_results
user_result_answers
developer_model_runs
developer_model_run_answers
developer_experiment_settings
```

Do not force developer experiment fields into the normal user result table if it makes the schema confusing.

---

# MVP Recommendation

For the initial MVP, implement:

1. model name input
2. optional persona name / memo input
3. manual prompt chunk display
4. 3-question chunk copy
5. pasted answer input
6. answer parsing or manual confirmation
7. localStorage progress saving
8. final result display
9. export or share
10. optional research consent

Do not implement full automated API execution in the public MVP.

Do not start with full admin API experiments.

---

# Future Questions to Resolve

These still need product decisions:

* exact chunk size options
* final prompt wording
* JSON vs CSV vs simple text priority
* how much free-form AI response parsing should be automatic
* how much user confirmation is required
* exact fields to save with consent
* result share format
* whether share pages are public, private-by-link, or local-only
* admin route naming
* Supabase RLS design
* developer experiment table design
* whether admin features eventually move to a private repo

---

# Important Implementation Notes for Codex / AI Coding Agents

Do not treat this document as permission to build the full admin/API system immediately.

Initial implementation should prioritize the public manual diagnosis MVP.

Before implementing admin or API features:

1. read `AGENTS.md`
2. read `docs/roadmap.md`
3. read `docs/aivt-16-design.md`
4. read `docs/supabase-notes.md` if database work is involved
5. propose a plan
6. list files likely to change
7. wait for approval for broad edits

Do not run migrations, add provider API calls, or change authentication without explicit approval.
