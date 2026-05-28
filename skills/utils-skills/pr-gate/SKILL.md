---
name: pr-gate
phase: cross-cutting
description: |
  Run the PR Gate checklist before merging. Verifies that durable docs are updated, code and context do not contradict each other, skipped workflow steps are justified, and no session artifacts leak into the commit. Use before creating or merging a pull request.
allowed-tools:
  - Read
  - Bash
metadata:
  owner: Ignacio Freire
  last_reviewed: "2026-05-27"
  skill-version: "1.0.0"
---

# PR Gate

Before you merge, run this gate. If any check fails, loop back to Build or Document.

---

## Invocation

```text
/pr-gate
```

---

## Checklist

- [ ] **Required docs are updated** — CHANGELOG has an entry, glossary updated if vocabulary changed, feature docs reflect current state
- [ ] **Code and context do not contradict each other** — requirements, design, tasks, and CHANGELOG match what the code actually does
- [ ] **Skipped workflow steps are named and justified** — if you skipped Spec or Plan, that decision is explicit
- [ ] **`.local-context/` files are excluded from the commit** — no session artifacts in the repo
- [ ] **Assignee reviewed** (when required by the project policy)

---

## Rules

- Do not merge before this gate passes.
- If a check fails, do not push forward — loop back to Build or Document.
- The gate can be run by a human or by the AI on request. The checks are the same.
- Run [context-update](../context-update/SKILL.md) immediately before this gate — both cover complementary concerns (documentation up to date vs. the change is ready to merge).

---

## Related skills

- [`context-update`](../context-update/SKILL.md) — runs right before this gate to ensure docs reflect the change.
- [`pr-summary`](../../skills-for-docs/pr-summary/SKILL.md) — produces the PR description that this gate signs off on.
- [`build-slice`](../../skills-for-planning/build-slice/SKILL.md) — the work being merged.
