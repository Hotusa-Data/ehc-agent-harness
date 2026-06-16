# Plan

Defines **how** to build what `specs.md` specifies and the **atomic work units** to execute it.

Use the smallest plan that preserves clarity. Use `unknown — needs confirmation` or `not applicable` instead of inventing content. Stop and ask if ambiguity affects scope, contracts, security, privacy, or acceptance criteria.

## 0. Metadata

- Feature:
- Owner:
- Status: draft | ready-for-build | in-progress | implemented | superseded
- Source specs: `specs.md`
- Mode: lightweight | standard | full
- Mode reason:
- Last reviewed:

Mode guidance:

- `lightweight`: docs-only, obvious fixes, mechanical refactors, low-risk config.
- `standard`: normal behavior change with clear specs and limited blast radius.
- `full`: new feature, business logic, migrations, public contracts, security/privacy impact.

## 1. Approach

One or two paragraphs. Architecture summary, layers touched, reused components, rejected alternatives.

- Main files / modules:
- New files / modules:
- New dependencies (`uv add ...`):
- Key design choices:
- Alternatives rejected:

## 2. Contracts And Data

| Item | Change | Notes |
|---|---|---|
| API |  |  |
| Pydantic schemas (`schemas/`) |  |  |
| Pandera schemas (`schemas_df/`) |  |  |
| SQLAlchemy models (`models/`) |  |  |
| Alembic migration |  | required? yes / no |
| Backward compatibility |  |  |
| Data migration / backfill |  |  |

## 3. Validation, Security, Privacy

| Case / risk | Planned behavior | Where handled | Evidence |
|---|---|---|---|
| Empty / invalid / duplicate input |  |  |  |
| External dependency failure |  |  |  |
| Untrusted input / injection |  |  |  |
| PII / sensitive data |  |  |  |
| Authorization |  |  |  |

Checklist:

- [ ] No secrets or PII in code, tests, fixtures, logs, or notebooks.
- [ ] Untrusted inputs validated and bounded.
- [ ] Logs use safe identifiers only.

## 4. Evidence And Commands

For each non-trivial AC, name the verification artifact **before** implementation.

| AC | Evidence type | Location / command | Expected signal |
|---|---|---|---|
| AC1 | Unit test |  |  |

Valid evidence: unit / integration / contract test, committed notebook re-run, executable example, before/after note with concrete inputs.

Commands (discover from the repo; do not assume):

| Purpose | Command | Required? |
|---|---|---|
| Format / lint / type-check |  |  |
| Tests |  |  |
| Migration |  |  |
| Docs build |  |  |

If a check cannot run, record why and what alternative evidence exists.

## 5. Operations And Rollout

- Logs / metrics / run IDs:
- Feature flag / config:
- Deployment or migration ordering:
- Backfill:
- Rollback:
- Cleanup follow-up (if any — add a task in section 8):

## 6. Risks, Assumptions, Decisions

| Type | ID | Statement | Impact | Action / owner |
|---|---|---|---|---|
| Risk | R1 |  |  |  |
| Assumption | A1 |  |  |  |
| Decision | D1 |  |  |  |

## 7. Documentation Impact

| Doc | Change | Status |
|---|---|---|
| Glossary |  | todo |
| Business logic / report |  | todo |
| Repo / architecture guide |  | todo |
| API / schema docs |  | todo |
| Runbook |  | todo |

## 8. Task List

**Slice** = one coherent, reviewable unit of work that delivers a single layer or vertical behavior. A slice should be completable in one sitting and result in a passing test or observable signal before the next slice begins.

| ID | Task | Slice | Depends on | Files / areas | AC | Evidence | Status |
|---|---|---|---|---|---|---|---|
| T1 |  | S1 | none |  | AC1 |  | todo |

Rules:
- Each task ties to a requirement, AC, or risk-reduction need from `specs.md`
- Risky discovery happens before dependent implementation
- Evidence is not deferred to the end without justification
- Tasks are atomic: completion is binary

## 9. Completion Criteria

A task is `done` when:
- The named files / areas have the change
- The named evidence exists and was run
- Any documentation impact in section 7 is resolved

## Ready Checklist

- [ ] Mode is justified.
- [ ] Plan traces to specs and ACs; no unapproved scope.
- [ ] Contracts, migrations, security, privacy, observability impacts considered.
- [ ] Each non-deferred AC has evidence.
- [ ] Tasks are small, ordered, and evidence-backed.
- [ ] Dependencies are explicit.
- [ ] Lightweight skipped steps are named and justified.

## Completion Checklist

- [ ] Implementation follows the planned slices (or deviations are explained).
- [ ] All non-deferred ACs have recorded evidence.
- [ ] Required checks ran; `ran` vs `written but not run` vs `tried but blocked` is distinguished.
- [ ] Specs and plan reflect any scope or approach changes made during build.
- [ ] Documentation impact is resolved.
- [ ] Rollout and rollback notes are ready if applicable.
