# Plan

Defines **how** to build what `specs.md` specifies. The **Task List (§1)**, **Testing Plan (§2)**, and **Evidence (§3)** are the authoritative definition of work for Build — ordered, traceable to Req/AC, each task independently executable.

Other sections provide context; they do not replace tasks or the testing plan.

Use the smallest plan that preserves clarity. Use `unknown — needs confirmation` or `not applicable` instead of inventing content. Stop and ask if ambiguity affects scope, contracts, security, privacy, or acceptance criteria.

## Section guide (Harness mode)

Lightweight work in the working cycle (`AGENTS.md`) does **not** create a plan file — name what you skip in the PR or CHANGELOG.

| § | Section | standard | full |
|---|---|---|---|
| 0 | Metadata | required | required |
| 1 | Task List | required (≥1 row) | required |
| 2 | Testing Plan | required | required |
| 3 | Evidence And Commands | required | required |
| 4 | Approach | short | required |
| 5 | Contracts And Data | if any task needs it | required |
| 6 | External Dependencies | if other systems, teams, or features | required |
| 7 | Future TODOs | if scope is deferred to later | required |
| 8 | Documentation Impact | required | required |
| 9 | Risks, Assumptions, Decisions | if non-obvious | required |
| 10 | Operations And Rollout | omit | required |
| 11 | Task completion rules | required | required |

Sections marked omit: delete the heading or write `not applicable`.

> **During Build**, load and update primarily **§1 Task List**, **§2 Testing Plan**, and **§3 Evidence And Commands**.
> Other sections are Plan Review context — do not rewrite unless the approach changed.

## 0. Metadata

- Feature:
- Owner:
- Status: draft | ready-for-build | in-progress | implemented | superseded
- Source specs: `specs.md`
- Harness mode: standard | full
- Mode reason:
- Last reviewed:

Mode guidance:

- `standard`: normal behavior change with clear specs and limited blast radius; typically 1–4 tasks.
- `full`: new feature, business logic, migrations, public contracts, security/privacy impact; typically 5+ tasks or rollout steps.

`Harness mode` must match `specs.md` when both exist.

## 1. Task List

**Slice** = one coherent, reviewable unit of work that delivers a single layer or vertical behavior. A slice should be completable in one sitting and result in a passing test or observable signal before the next slice begins.

| ID | Task | Slice | Depends on | Req | AC | Files / areas | Test plan | Evidence | Kind | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| T1 |  | S1 | none | FR1 | AC1 |  | §2 AC1 | §3 AC1 | AFK | todo |

**Rules**
- Each task ties to ≥1 Req (`FR*`, `BR*`, `NFR*`) or AC from `specs.md`.
- Each `Must` FR has ≥1 task; risky discovery is its own task before dependents.
- **Test plan** and **Evidence** columns point to §2 and §3 rows — do not restate strategy in the task row.
- **Kind:** `AFK` (agent can proceed) | `HITL` (human decision required before `in-progress`).
- Tasks are atomic: completion is binary.
- Anti-patterns: generic tasks ("implement feature", "add tests") — each row names an observable outcome.

## 2. Testing Plan

How each AC is verified. Follow [`agent-kit/agent-rules/TESTING.md`](../agent-kit/agent-rules/TESTING.md) — do not duplicate TEST-1–TEST-12 here.

**One row per AC** (Must ACs required in standard; add Should ACs in full).

| AC | Task(s) | Level | Test module(s) | Behavior under test | Doubles / boundaries | Edge cases (from spec) | Notes |
|---|---|---|---|---|---|---|---|
| AC1 | T1 | unit | `tests/test_<pkg>_data_x.py` | When … then … | mock HTTP at fetch boundary (TEST-5) | empty input | red-first in T1 |

**Level:** `unit` | `integration` | `contract` | `notebook` | `manual` (TEST-10).

Evidence type in `specs.md` §8 must match **Level** here.

**Strategy summary** (standard: 3–5 bullets; full: expand as needed)

- Default test level for this feature:
- Persistence: real session vs dialect (TEST-4 + project override):
- API: TestClient + dependency overrides (TEST-11) — yes / no:
- Pipelines: stage tests (TEST-8) — yes / no:
- Gaps: ACs without automated tests → TEST-10 justification in the row:

Map each specs edge case to a §2 row — do not restate domain wording.

## 3. Evidence And Commands

Concrete verification per AC or task. Every §2 row must have a matching command or TEST-10 justification here.

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

## 4. Approach

One or two paragraphs. Architecture summary, layers touched, reused components, rejected alternatives.

- Main files / modules:
- New files / modules:
- New Python packages (`uv add ...`), if any:
- Key design choices:
- Alternatives rejected:

**standard:** keep brief — Post-Plan approval can rely on §1–§3 alone.

## 5. Contracts And Data

| Item | Change | Notes |
|---|---|---|
| API |  |  |
| Pydantic schemas (`schemas/`) |  |  |
| Pandera schemas (`schemas_df/`) |  |  |
| SQLAlchemy models (`models/`) |  |  |
| Alembic migration |  | required? yes / no |
| Backward compatibility |  |  |
| Data migration / backfill |  |  |

**standard:** omit section if no task touches contracts.

## 6. External Dependencies

Other **systems**, **teams**, or **features** this work depends on — not Python packages (those go in §4 Approach).

Task ordering between slices stays in §1 **Depends on**. List here what must exist, respond, or ship **outside this repo** (or in another feature folder) before or during Build.

| Dependency | Type | What we need | Status | Blocks (task) | Notes |
|---|---|---|---|---|---|
|  | system \| team \| feature |  | available \| blocked \| unknown |  |  |

**Type examples:** external API, data platform, queue, auth provider, ops runbook, another team's endpoint, another feature in `docs/features/`.

**standard:** omit if this feature stands alone with no external blockers.

## 7. Future TODOs

Work **intentionally left for later** — out of scope for this plan's Build, but worth tracking so it is not lost. These do not block current tasks unless promoted to §1.

| ID | Future work | Why deferred | When / where |
|---|---|---|---|
| F1 |  |  | next release \| feature X \| CHANGELOG Decided |

Promote to §1 when it becomes in-scope; otherwise close here and record in CHANGELOG `Decided` when the feature ships.

**standard:** omit if nothing is deferred beyond this plan.

## 8. Documentation Impact

| Doc | Change | Status |
|---|---|---|
| Glossary |  | todo |
| Business logic / report |  | todo |
| Repo / ADR(s) / docs-guide |  | todo |
| API / schema docs |  | todo |
| Runbook |  | todo |

## 9. Risks, Assumptions, Decisions

| Type | ID | Statement | Impact | Action / owner |
|---|---|---|---|---|
| Risk | R1 |  |  |  |
| Assumption | A1 |  |  |  |
| Decision | D1 |  |  |  |

HITL tasks must reference the blocking row here or CHANGELOG `Decided`.

## 10. Operations And Rollout (full)

- Logs / metrics / run IDs:
- Feature flag / config:
- Deployment or migration ordering:
- Backfill:
- Rollback:
- Cleanup follow-up (if any — add a task in §1):

## 11. Task Completion Rules

A task is `done` when:

1. The named **Files / areas** contain the change.
2. The matching **§2** row is implemented (tests exist and cover the declared behavior).
3. The matching **§3** row was executed with documented signal (COOP-3: ran vs written vs blocked).
4. Any documentation impact for that task in §8 is resolved.
5. Blocking **§6** dependencies are `available` or escalated (HITL / CHANGELOG `Decided`).

## Ready Checklist

**standard**
- [ ] Harness mode is justified and matches specs.
- [ ] §1 traces to specs Req/AC; no unapproved scope.
- [ ] Every Must AC has a §2 row and a §3 command (or TEST-10 justification).
- [ ] §1 tasks are ordered; dependencies and Kind (AFK/HITL) are explicit.
- [ ] Omitted sections are named and justified.

**full** — also verify:
- [ ] Contracts, migrations, external dependencies, and observability impacts considered.
- [ ] §7 future work is explicit — not hidden in chat or implied scope creep.
- [ ] §10 rollout and rollback notes are ready if applicable.
