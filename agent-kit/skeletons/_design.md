# Design

Defines **how** to build what `requirements.md` specifies. Atomic work units go in `tasks.md`.

Use the smallest plan that preserves clarity. Use `unknown — needs confirmation` or `not applicable` instead of inventing content. Stop and ask if ambiguity affects scope, contracts, security, privacy, or acceptance criteria.

## 0. Metadata

- Feature:
- Owner:
- Status: draft | ready-for-build | in-progress | implemented | superseded
- Spec link:
- Mode: lightweight | standard | full
- Mode reason:
- Last reviewed:

Mode guidance:

- `lightweight`: docs-only, obvious fixes, mechanical refactors, low-risk config.
- `standard`: normal behavior change with clear requirements and limited blast radius.
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
- Cleanup follow-up (if any — create a task in `tasks.md` to track it):

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

## Ready Checklist

- [ ] Mode is justified.
- [ ] Plan traces to requirements and ACs; no unapproved scope.
- [ ] Tasks are documented separately in `tasks.md` when needed and remain small, ordered, evidence-backed.
- [ ] Contracts, migrations, security, privacy, observability impacts considered.
- [ ] Each non-deferred AC has evidence.
- [ ] Lightweight skipped steps are named and justified.

## Completion Checklist

- [ ] Implementation follows the planned slices (or deviations are explained).
- [ ] All non-deferred ACs have recorded evidence.
- [ ] Required checks ran; `ran` vs `written but not run` vs `tried but blocked` is distinguished.
- [ ] Spec and plan reflect any scope/design changes made during build.
- [ ] Documentation impact is resolved.
- [ ] Rollout and rollback notes are ready if applicable.
