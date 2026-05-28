---
name: plan-gate
phase: cross-cutting
description: |
  Run the Plan Gate checklist before starting implementation. Verifies that blocking ambiguity is resolved, scope and slices match the spec, the technical approach is sound, tests are planned, and documentation impact is known. Use after the Plan phase and before any Build work begins.
allowed-tools:
  - Read
metadata:
  owner: Ignacio Freire
  last_reviewed: "2026-05-27"
  skill-version: "1.0.0"
---

# Plan Gate

Before you start coding, run this gate. If any check fails, loop back to Spec or Plan.

---

## Invocation

```text
/plan-gate
```

---

## Checklist

- [ ] **Blocking ambiguity resolved or explicitly deferred** — no open questions that could change the approach
- [ ] **Scope and slices match the spec** — every slice traces back to an acceptance criterion
- [ ] **Technical approach is understandable and justified** — tradeoffs named, alternatives considered
- [ ] **Tests and evidence are planned** — at least one verification signal per slice
- [ ] **Documentation impact is known** — which docs will change, which are out of scope

---

## Rules

- Do not start Build work before this gate passes.
- If a check fails, do not push forward — loop back to the relevant phase.
- The gate can be run by a human or by the AI on request. The checks are the same.
- If the task is lightweight (obvious fix, no spec), the gate is optional — but name that decision explicitly.

---

## Related skills

- [`implementation-planning`](../../skills-for-planning/implementation-planning/SKILL.md) — the plan being gated. Loop back here if any check fails.
- [`notebook-mockup`](../../skills-for-planning/notebook-mockup/SKILL.md) — when the plan includes a notebook, its approval is part of "tests and evidence are planned".
- [`build-slice`](../../skills-for-planning/build-slice/SKILL.md) — runs immediately after this gate passes.
