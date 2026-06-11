---
name: design-write
phase: plan
description: |
  Translate an approved spec into a technical design: approach, module contracts, test strategy, and risks. Output: `design.md`. Use when the user asks for a plan, implementation roadmap, or wants to de-risk a non-trivial change before coding.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
metadata:
  owner: Ignacio Freire
  last_reviewed: "2026-05-28"
  skill-version: "1.0.0"
---

# Design Write

Translate an approved spec into a concrete technical design. Stay in planning mode — inspect the repo, synthesize context, surface blockers, and produce `design.md`. Do not write production code.

## When to use

- `requirements.md` has been approved (Spec Review passed).
- The task involves non-trivial architecture decisions, module contracts, or test strategy.
- The team needs a technical design to review before slicing work into tasks.

## When NOT to use

- The spec is still ambiguous — run [`grill-me`](../../utils-skills/grill-me/SKILL.md) and [`spec-write`](../spec-write/SKILL.md) first.
- The change is a single obvious fix — skip design and go straight to [`tasks-write`](../tasks-write/SKILL.md) or Build directly.
- The user wants task breakdown or tracker tickets — use [`tasks-write`](../tasks-write/SKILL.md) after design is approved.

## Process

### 1. Load context

Follow the DOC-1 load order. Always load:
- `docs/features/<feature>/requirements.md` — read every AC; flag any that are ambiguous before designing
- `agent-kit/agent-rules/core.md`, `agent-kit/agent-rules/testing.md`

Load additionally when applicable:

| File | When to load | What to extract |
|---|---|---|
| `docs/architecture.md` | Architectural or system-boundary change | Which layers and boundaries are already drawn; don't re-design what is settled |
| `docs/glossary.md` | Business vocabulary in the requirements | Canonical names for function signatures and variable names |
| `agent-kit/agent-rules/architecture.md` | Module or system-boundary decisions | Module rules and layer constraints |
| `agent-kit/agent-rules/persistence.md` | ORM, queries, migrations | Session and transaction patterns already in use |
| `agent-kit/agent-rules/security.md` | Auth, secrets, or trust boundary involved | Trust model and validation-placement rules |
| `docs/features/<related>/design.md` | A similar prior feature exists | Architectural precedent — copy the pattern, don't reinvent |

### 2. Explore codebase

Read the affected modules, existing patterns, and nearby conventions.

<exploration-targets>
- **Call sites**: read the callers of each function you plan to change — they define the real interface contract, not the spec language.
- **Error types**: find the project's exception hierarchy or error enum. Use existing types; introduce new ones only when the AC requires a genuinely new failure case.
- **Test files for affected modules**: understand what is already covered and which patterns the project uses (fixture layout, mock strategy, parametrize style).
- **Similar features**: find the nearest existing feature that follows the same pattern (e.g. another CRUD endpoint, another validation pipeline). Read its `design.md` if present. Let architectural precedent drive your approach.
- **Reusable helpers**: search for existing utilities in the affected area before designing new functions. Duplication at the design stage becomes tech debt in Build.
</exploration-targets>

Identify likely areas of change. Prefer module/area names over speculative file paths — mark unknowns explicitly.

### 3. Draft design

Propose **one** primary technical approach. Cover:

- **Approach** — the chosen solution and its rationale. Note alternatives only when the tradeoff is significant.
- **Affected areas** — modules, layers, and boundaries involved. No speculative file paths.
- **Function contracts** — for each new or modified function, capture: name, inputs/types, outputs/types, error conditions, and business rules. Derive these from the actual code, not from spec language: input types from the model/schema the caller already constructs; output types from what the downstream consumer reads; errors from the exception types callers already handle.
- **Test strategy** — feature-level: test level (unit / integration / both), what to mock and what to keep real, key edge cases beyond happy path, test data approach.
- **Risks and unknowns** — technical risks, contract or migration impact, external dependencies. Record gaps as "unknown — needs confirmation".
- **Documentation impact** — which durable docs this change touches.

<function-contract-table>
| Element | Source |
|---|---|
| Function name | Derived from AC + domain vocabulary |
| Inputs and types | Spec acceptance criteria or contracts section |
| Outputs and types | Spec worked examples |
| Error conditions | Spec edge cases |
| Business rules | Spec or domain glossary |
</function-contract-table>

### 4. Write artifact

Save to `docs/features/<feature>/design.md`, creating the file if it doesn't exist.

<design-template>

## Approach

The chosen technical approach and why. One primary option; alternatives only when the tradeoff matters.

## Affected Areas

Modules, layers, and system boundaries involved. No speculative filenames.

## Function Contracts

For each new or modified function:

| Function | Inputs | Outputs | Errors | Business rules |
|---|---|---|---|---|
| `name()` | type, type | type | ErrorType | rule |

## Test Strategy

- **Level:** unit / integration / both
- **Doubles:** what to mock, what to keep real
- **Edge cases:** beyond happy path
- **Test data:** fixture location and approach

## Risks and Unknowns

- Risk or unknown — mitigation or confirmation needed

## Documentation Impact

- List of docs that need updating when this ships

</design-template>

---

## Anti-patterns

| Anti-pattern | Why it fails |
|---|---|
| Writing production code during planning | Design mode only — code belongs in Build. |
| Proposing multiple approaches without a recommendation | Forces the reviewer to make a decision you should have made. Propose one; note tradeoffs when they matter. |
| Speculative file paths | They go stale before the design is reviewed. Use module/area names instead. |
| Skipping unknowns | Hidden assumptions become bugs. Record gaps explicitly. |
| Mixing slice ordering into the design | Slicing and task sequencing belong in `tasks-write`. |
| No test strategy per contract | Build will start without a failing test to target. |

---

## Related skills

- [`spec-write`](../spec-write/SKILL.md) — predecessor: `requirements.md` is the input to this design.
- [`grill-me`](../../utils-skills/grill-me/SKILL.md) — resolve spec ambiguity before designing.
- [`notebook-mockup`](../notebook-mockup/SKILL.md) — validate logic with synthetic data before committing to the design.
- [`tasks-write`](../tasks-write/SKILL.md) — successor: approved design → ordered task slices.
