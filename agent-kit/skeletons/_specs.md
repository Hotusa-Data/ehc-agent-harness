# Specs

Defines **what** must change and **why**. The **how**, **tasks**, **testing plan**, and **commands** belong in `plan.md`.

Fill what is known. Use `unknown — needs confirmation` instead of guessing. Use `not applicable` with a short reason when a section does not apply.

## Section guide (Harness mode)

Lightweight work in the working cycle (`AGENTS.md`) does **not** create a spec file — name what you skip in the PR or changelog.

| § | Section | standard | full |
|---|---|---|---|
| 0 | Metadata | required | required |
| 1 | Problem | required | required |
| 2 | Goals / Non-Goals | required | required |
| 3 | Current Behavior | if behavior change | required |
| 4 | Target Behavior | required | required |
| 5 | Requirements | required | required |
| 6 | Business Rules | if domain rules | required |
| 7 | Domain Boundaries | omit | required |
| 8 | Acceptance Criteria | required | required |
| 9 | Edge Cases | fold into §4 / §8 | required |
| 10 | Assumptions / Questions | required | required |

Sections marked omit: delete the heading or write `not applicable — see plan.md`.

## 0. Metadata

- Feature:
- Owner:
- Status: draft | ready-for-plan | in-progress | implemented | superseded
- Harness mode: standard | full
- Mode reason:
- Spec link / tickets:
- Related modules:
- Last reviewed:

Mode guidance:

- `standard`: normal behavior change with clear scope and limited blast radius.
- `full`: new feature, business logic, migrations, public contracts, security/privacy impact.

If both `specs.md` and `plan.md` exist, `Harness mode` must match unless justified in changelog `Decided`.

## 1. Problem

- Who is affected:
- Current pain / gap:
- Desired outcome:

## 2. Goals And Non-Goals

**Goals**
- G1:

**Non-Goals**
- NG1:

## 3. Current Behavior

What happens today. Add a concrete example if it is a bug or behavior change.

**standard:** omit if this is new capability with no prior behavior.

## 4. Target Behavior

Intended behavior in domain language. Cover: happy path, empty state, invalid input.

**standard:** fold edge cases here (bullets) instead of a separate §9.

## 5. Requirements

One requirement per row. Observable and using glossary terms.

| ID | Type | Requirement | Priority |
|---|---|---|---|
| FR1 | Functional | When ..., the system shall ... | Must |
| NFR1 | Non-functional | The system shall ... measured by ... | Should |

Patterns: `When <trigger>, the system shall <response>` / `If <condition>, then the system shall <response>`.

Every `Must` requirement needs ≥1 AC in §8.

## 6. Business Rules

| ID | Rule | Inputs | Outcome |
|---|---|---|---|
| BR1 |  |  |  |

**standard:** omit if no domain rules beyond §5.

## 7. Domain Boundaries (full)

Domain inputs and outputs only — no API routes, SQL table names, or schema class names.

| Direction | Name | Consumer / provider | Shape (domain) | Notes |
|---|---|---|---|---|
| in |  |  |  |  |
| out |  |  |  |  |

Contract notes: nulls, units, timezones, PII classification, backward compatibility.

## 8. Acceptance Criteria

Every non-trivial AC maps to a testing-plan row in `plan.md` §2 before Build.

| ID | Requirement | Criterion | Evidence type (planned) |
|---|---|---|---|
| AC1 | FR1 | When ..., the system ... | unit |

**Evidence type (planned):** `unit` | `integration` | `contract` | `notebook` | `manual` — no test paths or commands here; those live in `plan.md` §2–§3.

## 9. Edge Cases (full)

| Case | Expected behavior |
|---|---|
| Empty input |  |
| Invalid input |  |
| Duplicate input |  |
| External dependency failure |  |

## 10. Assumptions And Open Questions

| ID | Statement / question | Impact if wrong | Blocking? |
|---|---|---|---|
| A1 |  |  |  |
| Q1 |  |  |  |

## Ready Checklist

**standard**
- [ ] Problem, users, and outcome are clear.
- [ ] Goals and non-goals protect scope.
- [ ] Every `Must` requirement has ≥1 AC.
- [ ] Blocking questions are resolved or explicitly marked.
- [ ] Documentation impact tracked in `plan.md` §8 — not duplicated here.

**full** — also verify:
- [ ] Domain boundaries (§7) and edge cases (§9) are explicit.
- [ ] Inputs, outputs, contracts, and glossary terms are consistent.

## Maintaining this spec (spec-anchored)

- During build: scope or AC changes → edit this file or changelog `[Unreleased]` → `Specs` (DOC-7).
- Partial or deferred work → changelog `Decided`, not a parallel doc.
- When behavior permanently changes → update §3–§5 in place; set Status `superseded` only when replaced by a new feature folder.
- Do not duplicate technical contracts here after Plan Review — they live in `plan.md` §4–§5.
