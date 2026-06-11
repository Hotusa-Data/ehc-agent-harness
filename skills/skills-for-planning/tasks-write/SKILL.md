---
name: tasks-write
phase: plan
description: |
  Break an approved design into ordered, independently-grabbable task slices. Output: `tasks.md`. Optionally publish to the issue tracker. Use when the user wants to slice the design into executable tasks or tracker tickets.
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
  skill-version: "1.0.0"
---

# Tasks Write

Break an approved design into ordered, independently-grabbable task slices. Write `tasks.md` as the primary artifact. Optionally publish each task as an issue on the project tracker.

The issue tracker and triage label vocabulary should have been provided in the project context.

## When to use

- `design.md` has been approved (Plan Review passed).
- The work spans more than one slice and needs ordered execution tracking.
- The team wants AFK-ready tasks another agent can grab without further context.

## When NOT to use

- The design is not yet approved — complete Plan Review first.
- The change is a single slice that ships as one PR — overkill; go straight to Build.
- The user needs a technical design — use [`design-write`](../design-write/SKILL.md) first.

## Process

### 1. Load context

Read `docs/features/<feature>/design.md` and `docs/features/<feature>/requirements.md`. Load any project-level issue tracker vocabulary from context if publishing to a tracker.

### 2. Explore codebase

If not already explored, read the affected areas to ground slice boundaries in the actual code structure. Look for:

<boundary-signals>
- **Module and file groupings**: one vertical slice often maps to one module boundary — a cohesive set of files that can be changed and tested together.
- **Integration seams**: where two components hand off data (handler → service → repository, or pipeline stage → stage). Each seam is a candidate slice line.
- **Test file structure**: if the project has one test file per module, one slice per test file is a natural default.
- **Data migrations or schema changes**: if present, these are always their own slice and typically the first dependency.
</boundary-signals>

### 3. Draft slices

Break the design into **tracer-bullet** vertical slices. Each slice cuts through ALL integration layers end-to-end — not a horizontal layer (schema-only, API-only, UI-only).

Classify each slice as **AFK** (can be implemented and merged without human interaction) or **HITL** (requires a human decision, design review, or sign-off before proceeding). Prefer AFK.

<slice-rules>
- Each slice delivers a narrow but complete path through every layer
- A completed slice is demoable or verifiable on its own
- Prefer many thin slices over few thick ones
- Order by dependency: blockers first
- **Size heuristic**: a well-scoped AFK slice touches one core module and one test module. If a slice touches more than three independent modules, split it.
- **Evidence first**: each slice must name its evidence type before Build starts — a test that passes, a notebook cell output, or a specific before/after diff. "Evidence: TBD" is not a slice.
</slice-rules>

**HITL triggers** — a slice must pause for human decision when:
- A business rule or threshold the spec left open ("TBD", "to be decided")
- A UI/UX choice with no wireframe or mockup
- A performance, cost, or security threshold the spec did not specify
- A data migration or destructive operation that requires production sign-off before running

**AFK indicators** — a slice can run end-to-end without pausing when:
- All acceptance criteria are observable and unambiguous
- The implementation approach follows an existing pattern in the codebase
- No irreversible action (migration, external API write, notification send) is performed without a test double

### 4. Confirm with user

Present the proposed breakdown as a numbered list. For each slice show: title, type (HITL/AFK), blocked-by, and user stories covered (if any).

Ask:
- Does the granularity feel right? (too coarse / too fine)
- Are the dependency relationships correct?
- Should any slices be merged or split?
- Is the HITL/AFK classification correct?

Iterate until the user approves the breakdown.

### 5. Write artifact

Save the approved slices to `docs/features/<feature>/tasks.md`, in dependency order.

<tasks-template>
# Tasks: [Feature Name]

Source: [link to design.md]

---

## Task 1: [Title]

**Type:** AFK | HITL
**Blocked by:** None | Task N

**Goal:** End-to-end behavior this slice delivers.

**Evidence:** How to verify completion — tests that pass, notebook output, or observable before/after diff.

**Documentation impact:** Docs that change when this ships. "None" only if truly no changes needed.

---

## Task 2: [Title]

...
</tasks-template>

### 6. Publish to tracker (optional)

If the project uses an issue tracker, publish one issue per task in dependency order (blockers first) so real issue IDs can be referenced in "Blocked by" fields.

<issue-template>
## What to build

The end-to-end behavior of this slice. No file paths or code snippets — describe behavior, not implementation.

## Acceptance criteria

- [ ] Criterion 1
- [ ] Criterion 2

## Blocked by

Reference to blocking issue, or "None — can start immediately".

## Reference

Link to the corresponding entry in `tasks.md`.
</issue-template>

Do NOT close or modify any parent issue.

---

## Anti-patterns

| Anti-pattern | Why it fails |
|---|---|
| Horizontal slices (one task per layer) | Nothing is demoable until the last layer lands. Tracer bullets only. |
| Re-deriving slices instead of reading `design.md` | Slicing diverges from the approved design. Always read `design.md` first. |
| Few thick slices | Hard to parallelise, hard to review. Prefer many thin slices. |
| Publishing issues before writing `tasks.md` | The durable artifact lives in the repo, not the tracker. Always write the file first. |
| Publishing issues in the wrong dependency order | "Blocked by" references break because the blocker has no real ID yet. |
| Skipping user confirmation on the breakdown | Granularity is the most opinionated part of this skill. Always confirm before writing. |
| Running before Plan Review passes | Tasks published from an unapproved design carry unresolved decisions into Build. |

---

## Related skills

- [`design-write`](../design-write/SKILL.md) — predecessor: `design.md` is the primary input.
- [`build-slice`](../build-slice/SKILL.md) — consumer: each task in `tasks.md` becomes one TDD slice.
- [`spec-write`](../spec-write/SKILL.md) — upstream Spec skill that produces `requirements.md`.
