---
name: plan-write
phase: plan
description: |
  Translate approved specs into a technical plan: approach, contracts, test strategy, risks, and ordered task slices. Output: `plan.md`. Optionally publish to the issue tracker. Use when the user asks for a plan, implementation roadmap, or wants to de-risk a non-trivial change before coding.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
metadata:
  owner: Ignacio Freire
  last_reviewed: "2026-05-28"
  skill-version: "2.0.0"
---

# Plan Write

Translate approved specs into a concrete plan — approach, contracts, evidence strategy, and ordered work slices. Write `plan.md` as the primary artifact. Optionally publish each task as an issue on the project tracker.

The issue tracker and triage label vocabulary should have been provided in `docs/docs-guide.md`.

## When to use

- `specs.md` has been approved (Spec Review passed).
- The task involves non-trivial architecture decisions, module contracts, test strategy, or multiple slices.
- The team needs a plan to review before Build.

## When NOT to use

- The spec is still ambiguous — run [`grill-me`](../../utils-skills/grill-me/SKILL.md) and [`spec-write`](../spec-write/SKILL.md) first.
- The change is a single obvious fix — skip the plan and go straight to Build.
- The user wants only the what/why artifact — use [`spec-write`](../spec-write/SKILL.md).

## Process

### 1. Load context

Follow the DOC-1 load order. Always load:
- `docs/features/<feature>/specs.md` — read every AC; flag any that are ambiguous before planning
- `agent-kit/agent-rules/core.md`, `agent-kit/agent-rules/testing.md`

Load additionally when applicable:

| File | When to load | What to extract |
|---|---|---|
| `docs/architecture.md` | Architectural or system-boundary change | Which layers and boundaries are already drawn |
| `docs/glossary.md` | Business vocabulary in the specs | Canonical names for function signatures and variable names |
| `agent-kit/agent-rules/architecture.md` | Module or system-boundary decisions | Module rules and layer constraints |
| `agent-kit/agent-rules/persistence.md` | ORM, queries, migrations | Session and transaction patterns already in use |
| `agent-kit/agent-rules/security.md` | Auth, secrets, or trust boundary involved | Trust model and validation-placement rules |
| `docs/features/<related>/plan.md` | A similar prior feature exists | Architectural precedent — copy the pattern, don't reinvent |

If publishing to a tracker, load issue tracker and triage label vocabulary from `docs/docs-guide.md` §3.

### 2. Explore codebase

Read the affected modules, existing patterns, and nearby conventions.

<exploration-targets>
- **Call sites**: read the callers of each function you plan to change — they define the real interface contract, not the spec language.
- **Error types**: find the project's exception hierarchy or error enum. Use existing types; introduce new ones only when the AC requires a genuinely new failure case.
- **Test files for affected modules**: understand what is already covered and which patterns the project uses.
- **Similar features**: find the nearest existing feature that follows the same pattern. Read its `plan.md` if present.
- **Reusable helpers**: search for existing utilities before designing new functions.
- **Module and file groupings**: one vertical slice often maps to one module boundary.
- **Integration seams**: handler → service → repository, or pipeline stage → stage — each seam is a candidate slice line.
- **Data migrations or schema changes**: always their own slice, typically the first dependency.
</exploration-targets>

### 3. Draft plan

Propose **one** primary technical approach and break it into **tracer-bullet** vertical slices. Cover:

- **Approach** — chosen solution and rationale
- **Contracts** — API, schemas, models, migrations
- **Test strategy** — level, doubles, edge cases, test data
- **Evidence** — verification artifact per non-trivial AC
- **Risks and unknowns** — record gaps as "unknown — needs confirmation"
- **Task slices** — ordered, dependency-aware, AFK or HITL

Classify each slice as **AFK** (implementable without human interaction) or **HITL** (requires a human decision before proceeding). Prefer AFK.

<slice-rules>
- Each slice delivers a narrow but complete path through every layer
- A completed slice is demoable or verifiable on its own
- Prefer many thin slices over few thick ones
- Order by dependency: blockers first
- **Evidence first**: each slice must name its evidence type before Build starts
</slice-rules>

**HITL triggers** — pause for human decision when:
- A business rule or threshold the spec left open
- A UI/UX choice with no wireframe or mockup
- A performance, cost, or security threshold the spec did not specify
- A data migration or destructive operation requiring production sign-off

### 4. Confirm with user

Present the proposed approach and slice breakdown. For each slice show: title, type (HITL/AFK), blocked-by, and ACs covered.

Ask:
- Does the approach look right?
- Does the granularity feel right?
- Are the dependency relationships correct?
- Is the HITL/AFK classification correct?

Iterate until the user approves.

### 5. Write artifact

Save to `docs/features/<feature>/plan.md`, creating the file if it doesn't exist. Instantiate from `agent-kit/skeletons/_plan.md` when the file is new.

### 6. Publish to tracker (optional)

If the project uses an issue tracker, publish one issue per task in dependency order (blockers first).

<issue-template>
## What to build

The end-to-end behavior of this slice. Describe behavior, not implementation.

## Acceptance criteria

- [ ] Criterion 1

## Blocked by

Reference to blocking issue, or "None — can start immediately".

## Reference

Link to the corresponding entry in `plan.md`.
</issue-template>

Do NOT close or modify any parent issue.

---

## Anti-patterns

| Anti-pattern | Why it fails |
|---|---|
| Writing production code during planning | Planning mode only — code belongs in Build. |
| Proposing multiple approaches without a recommendation | Forces the reviewer to decide what you should have decided. |
| Horizontal slices (one task per layer) | Nothing is demoable until the last layer lands. Tracer bullets only. |
| Re-deriving slices without reading `specs.md` | Slicing diverges from the approved spec. |
| Publishing issues before writing `plan.md` | The durable artifact lives in the repo. Always write the file first. |
| Running before Spec Review passes | Plans from an unapproved spec carry unresolved decisions into Build. |
| No test strategy per contract | Build will start without a failing test to target. |

---

## Related skills

- [`spec-write`](../spec-write/SKILL.md) — predecessor: `specs.md` is the input.
- [`grill-me`](../../utils-skills/grill-me/SKILL.md) — resolve spec ambiguity before planning.
- [`notebook-mockup`](../notebook-mockup/SKILL.md) — validate logic with synthetic data before committing to the plan.
- [`build-slice`](../build-slice/SKILL.md) — consumer: each task in `plan.md` becomes one TDD slice.
