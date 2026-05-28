# Tasks

Atomic, dependency-ordered units of work. Each task ties to a requirement or AC from `requirements.md` and to an approach element from `design.md`.

## 0. Metadata

- Feature:
- Owner:
- Status: draft | active | implemented
- Source design: `design.md`
- Source requirements: `requirements.md`
- Last reviewed:

## 1. Task list

**Slice** = one coherent, reviewable unit of work that delivers a single layer or vertical behavior. A slice should be completable in one sitting and result in a passing test or observable signal before the next slice begins.

| ID | Task | Slice | Depends on | Files / areas | AC | Evidence | Status |
|---|---|---|---|---|---|---|---|
| T1 |  | S1 | none |  | AC1 |  | todo |

Rules:
- Each task ties to a requirement, AC, or risk-reduction need
- Risky discovery happens before dependent implementation
- Evidence is not deferred to the end without justification
- Tasks are atomic: completion is binary

## 2. Completion criteria

A task is `done` when:
- The named files / areas have the change
- The named evidence exists and was run
- Any documentation impact in `design.md` section 7 is resolved

## Ready Checklist

- [ ] Every task ties to a requirement or AC
- [ ] Dependencies are explicit
- [ ] Evidence is named per non-trivial task
- [ ] No task is larger than one reviewable slice
