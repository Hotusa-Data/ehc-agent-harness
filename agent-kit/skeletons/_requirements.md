# Requirements

Defines **what** must change and **why**. The **how** belongs in `design.md`; the **work units** belong in `tasks.md`.

Fill what is known. Use `unknown — needs confirmation` instead of guessing. Use `not applicable` with a short reason when a section does not apply.

## 0. Metadata

- Feature:
- Owner:
- Status: draft | ready-for-build | in-progress | implemented | superseded
- Spec link / tickets:
- Related modules:
- Last reviewed:

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

## 4. Target Behavior

Intended behavior in domain language. Cover: happy path, empty state, invalid input.

## 5. Requirements

One requirement per row. Observable and using glossary terms.

| ID | Type | Requirement | Priority |
|---|---|---|---|
| FR1 | Functional | When ..., the system shall ... | Must |
| NFR1 | Non-functional | The system shall ... measured by ... | Should |

Patterns: `When <trigger>, the system shall <response>` / `If <condition>, then the system shall <response>`.

## 6. Business Rules

| ID | Rule | Inputs | Outcome |
|---|---|---|---|
| BR1 |  |  |  |

## 7. Inputs / Outputs

| Direction | Name | Source / consumer | Schema | Notes |
|---|---|---|---|---|
| in |  |  |  |  |
| out |  |  |  |  |

Contract notes: nulls, units, timezones, PII classification, backward compatibility.

## 8. Acceptance Criteria

Every non-trivial AC maps to evidence before build.

| ID | Requirement | Criterion | Evidence (test / notebook / example) |
|---|---|---|---|
| AC1 | FR1 | When ..., the system ... |  |

## 9. Edge Cases

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

## 11. Documentation Impact

Glossary / business logic / repo guide / API docs / runbook — list only what changes.

## Ready Checklist

- [ ] Problem, users, and outcome are clear.
- [ ] Goals and non-goals protect scope.
- [ ] Requirements are verifiable and use glossary terms.
- [ ] Inputs, outputs, contracts, and edge cases are explicit.
- [ ] Each non-trivial AC has named evidence.
- [ ] Blocking questions are resolved or explicitly marked.
