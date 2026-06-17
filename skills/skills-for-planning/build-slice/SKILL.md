---
name: build-slice
phase: build
description: |
  Implement one vertical task slice from an approved plan using TDD — red, green, refactor — with evidence tied to acceptance criteria. Use when Plan Review has passed, a slice from plan.md is ready to start, or the user asks to implement the next task, build a slice, or run the TDD loop. Do NOT use before plan.md is approved, for planning or spec work, or for notebook mockups (use notebook-mockup first when the plan declares one).
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
metadata:
  owner: Ignacio Freire
  last_reviewed: "2026-06-16"
  skill-version: "1.0.0"
---

# Build Slice

Implement **one** tracer-bullet slice from `docs/features/<feature>/plan.md` — narrow scope, full vertical path, explicit evidence. Each invocation completes at most one slice; stop for human review before starting the next.

**Contract with the rest of the lifecycle:**
- Input: approved `specs.md`, approved `plan.md`, and (when declared) an approved notebook mockup whose function contracts must be preserved.
- Output: working code, passing tests or cited evidence, slice marked done in `plan.md`, drift from spec documented — not hidden.
- After all slices: hand off to [`pr-summary`](../../skills-for-docs/pr-summary/SKILL.md) and [`context-update`](../../utils-skills/context-update/SKILL.md).

## When to use

- Plan Review passed and the next unblocked slice in `plan.md` is ready.
- The user asks to implement a task, build the next slice, or run TDD on a planned change.
- A notebook mockup was approved and production code must match its contracts.

## When NOT to use

- `specs.md` or `plan.md` are missing or not yet approved — use [`spec-write`](../spec-write/SKILL.md) or [`plan-write`](../plan-write/SKILL.md) first.
- The plan's first task is a notebook mockup and it is not yet approved — use [`notebook-mockup`](../notebook-mockup/SKILL.md).
- The slice is classified **HITL** and the human decision is still open — pause until resolved.
- Scope spans multiple slices — split and implement one at a time.

## Workflow

### 1. Select the slice

1. Read `docs/features/<feature>/plan.md` **§1 Task List** and pick the **next unblocked** task (dependencies satisfied, HITL resolved).
2. Load the matching **§2 Testing Plan** row (test module, level, doubles) and **§3 Evidence** row (command, expected signal) for that task's AC(s).
3. Read the AC criteria in `specs.md` §8 for domain wording only — do not re-derive test strategy from specs.
4. If a notebook mockup exists for this feature, read its Section 5 contract table — production function names and signatures must match.
5. Do not start Red without a §2 row for the task's AC(s). Confirm with the user which task you are implementing before writing code.

### 2. Load rules

Always load:
- `agent-kit/agent-rules/CORE.md`
- `agent-kit/agent-rules/TESTING.md`

Load additionally when applicable (see `agent-kit/agent-rules/DOCUMENTATION.md` §DOC-1): `PYTHON.md`, `PERSISTENCE.md`, `VALIDATION.md`, `SECURITY.md`, `ARCHITECTURE.md`.

### 3. TDD loop

For the selected slice:

1. **Red** — write a failing test in the **module path from plan §2** that expresses the **behavior under test** from that row (not implementation detail). See TEST-1 in `TESTING.md`.
2. **Green** — write the minimum production code to pass. Use glossary terms for domain-visible names.
3. **Refactor** — clean up while tests stay green. Do not expand scope beyond the slice.

Run the project's test command after each step (`make test` or the slice-local path from `TESTING.md` §Project Overrides).

### 4. Verify evidence

Each slice must satisfy **plan.md §3** for its AC(s), implementing the strategy in **§2**:
- Automated test passing
- Notebook re-run (when the slice implements notebook-proven logic)
- Explicit before/after notes when formal tests are impractical (TEST-10)

If behavior diverges from `specs.md`, stop and either loop back to [`plan-write`](../plan-write/SKILL.md) or document the drift explicitly in the slice summary.

### 5. Close the slice

Before claiming done:

- [ ] All tests for this slice pass (or evidence is cited per TEST-10)
- [ ] Diff is reviewable — one slice, no unrelated changes
- [ ] Drift from spec is explicit if any
- [ ] `plan.md` §1 task **Status** updated (ask user, or run [`context-update`](../../utils-skills/context-update/SKILL.md))
- [ ] Feature `changelog.md` entry proposed if the change is non-trivial

Present a short slice summary: what was built, which ACs are satisfied, what remains, and whether the next slice is unblocked.

## Rules

- **One slice per invocation.** Do not start slice N+1 in the same turn without user approval.
- **Vertical only.** Each slice crosses every layer the behavior needs — no horizontal "all models, then all services" tasks.
- **Tests first.** No production code without a failing test targeting the slice behavior, unless TEST-10 applies and evidence is named upfront.
- **Preserve notebook contracts.** When a mockup exists, function names and signatures from Section 5 are the interface contract.
- **Stop on broken assumptions.** If the plan or spec is wrong, loop back — do not patch silently.

## Anti-patterns

| Anti-pattern | Why it fails |
|---|---|
| Implementing multiple slices in one diff | Unreviewable; hides which ACs each change satisfies |
| Starting a slice without plan §2 row for its AC | No agreed test module, level, or doubles — violates TEST-1 |
| Writing production code before a failing test | No proof the test targets the right behavior |
| Mocking persistence internals | Violates TEST-4/TEST-5 — test the real boundary |
| Renaming notebook functions without updating the mockup | Breaks the approved contract |
| Fixing spec gaps in code without updating `plan.md` | Drift accumulates invisibly |
| Continuing when a HITL trigger fires | Builds on an unresolved human decision |

## Related skills

- [`plan-write`](../plan-write/SKILL.md) — predecessor: produces the slices this skill implements.
- [`notebook-mockup`](../notebook-mockup/SKILL.md) — optional upstream: supplies function contracts when the plan declares a mockup.
- [`context-update`](../../utils-skills/context-update/SKILL.md) — update `plan.md`, `changelog.md`, and related docs after the slice.
- [`pr-summary`](../../skills-for-docs/pr-summary/SKILL.md) — run when the branch is ready for human PR review.
