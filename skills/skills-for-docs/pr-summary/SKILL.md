---
name: pr-summary
phase: document
description: |
  Generate a clear technical-functional summary of a pull request or branch diff by cross-checking the actual code changes against the approved plan, feature specs, and any local-context handoff. The summary separates what changed, why it changed, what impact it has, and — critically — where the implementation diverges from the plan, which open questions remain, and which declared dependencies were touched. Use when the user asks for a PR summary, handoff note, review context, or business-readable explanation of a branch before merge.
allowed-tools:
  - Read
  - Write
  - Bash
  - Glob
  - Grep
metadata:
  owner: Ignacio Freire
  last_reviewed: "2026-05-28"
  skill-version: "2.1.0"
---

# PR Summary

Produce a reviewable change summary that **reconciles three sources of truth**:

1. The **plan and specs** in `docs/features/<feature>/` (specs, plan, CHANGELOG).
2. The **local session context** in `.local-context/` (handoff notes, open questions, decisions taken mid-session).
3. The **actual diff** against the comparison base.

The goal is not a file inventory — it's a document that tells the reviewer: *what the branch was supposed to do, what it actually does, where those two diverge, and what remains open*.

This skill is **read-only on production code**.

## When to use

Use when: the user asks for a PR summary, branch summary, handoff, or wants to verify plan alignment before opening a PR.

## When NOT to use

- Planning or implementation work — use [`plan-write`](../../skills-for-planning/plan-write/SKILL.md) or Build slices instead.
- Line-by-line code review — this skill reconciles intent vs diff, not style or correctness per line.
- Business-facing reports — use [`business-reports`](../business-reports/SKILL.md) instead.

## Input sources

| Input | Where | Why |
|---|---|---|
| Feature specs | `docs/features/<feature>/specs.md` | ACs, scope, business rules the diff must satisfy |
| Feature plan | `docs/features/<feature>/plan.md` | Approach, slices, tasks marked done vs. what the diff shows |
| Local handoff / session notes | `.local-context/` (any `*.md`) | Decisions, deviations, open questions |
| Branch diff | `git diff <base>...HEAD` | The actual change |
| Commit list | `git log <base>..HEAD` | Author's narrative |

If the feature folder is missing, ask the user which feature this branch belongs to. If `.local-context/` is missing, note it — do not invent context.

## Workflow

### Step 1 — Gather intent

1. Identify the feature. If unclear, ask the user.
2. Read `specs.md`, `plan.md`, `CHANGELOG.md` (skip missing ones, note the gap).
3. Read everything under `.local-context/`.
4. Confirm the comparison base (default `main`; ask if stacked).

### Step 2 — Collect branch context

```bash
git log <base>..HEAD --oneline
git diff <base>...HEAD --stat
git diff <base>...HEAD --name-only
```

Pull full diffs only where stat is ambiguous or the spec flagged risk.

### Step 3 — Read code, not the diff

For each meaningful changed file, read enough of the surrounding code at HEAD to explain **behaviour**, not line churn.

### Step 4 — Reconcile plan ↔ code

Build three columns: **planned**, **delivered**, **delta**. Walk through:

- Each AC in `specs.md` — satisfied? Partially? Not at all?
- Each slice/task in `plan.md` — does the diff match? Touch anything unplanned?
- Each decision or question in `.local-context/` — resolved? Left open? Changed?
- Each declared dependency — present in the diff? Any undeclared ones?

**Delta** is the most valuable content — reviewers cannot recover it from the diff alone.

### Step 5 — Separate concerns in output

- **Functional changes** — what a user or stakeholder would observe.
- **Technical changes** — refactors, contracts, infra.
- **Risks and open questions** — known unknowns, deferred work, items from `.local-context/`.

### Step 6 — Mermaid (optional)

Include one Mermaid block only if a decision or data flow changed materially. Otherwise skip.

### Step 7 — Write the document

Write to `PR_info.md` (or the path requested). Use this section order:

1. **Summary** — 2–3 sentences a non-technical reader can understand.
2. **Task description** — feature + plan reference (`docs/features/<feature>/`).
3. **Plan ↔ Code alignment** — table from Step 4. This is what reviewers read first.
4. **Functional changes**
5. **Technical changes**
6. **Affected modules or domains**
7. **Dependencies touched** — mark each as `declared in plan` or `new — not in plan`.
8. **Risks and sensitive points**
9. **Open questions** — unresolved items from `.local-context/`, each marked `still open` or `resolved`.
10. **Tests run or recommended**
11. **Follow-up actions**

For empty sections: write `Not specified` (missing inputs) or `None`. Never delete the heading.

### Step 8 — Verify before finishing

- Plan ↔ Code table cites concrete AC IDs / slice names, not paraphrases.
- Every behaviour claim traces to a file in the diff.
- Every open question has a status or is explicitly carried over.
- The summary stands alone — a reviewer can decide whether to dig deeper without opening the diff.
- No production code was modified.

## Anti-patterns

| Anti-pattern | Why it fails |
|---|---|
| Pasting the full diff | The reviewer already has it; explain *why* it changed |
| File inventory without behaviour | Does not help evaluate impact |
| Mixing functional & technical changes | Different audiences; keep separated |
| Skipping plan reconciliation | Cannot tell whether the branch did what it was supposed to |
| Ignoring `.local-context/` | Ships unknowns silently into review |
| Inventing rationale | Write `Not specified`, never guess |
| Undeclared dependencies as ordinary lines | A new package or migration not in the plan is a review-blocking event |
| Modifying production code | This skill is read-only on code |
| Final-state migration description that hides risk | Describe outcomes *and* what could go wrong |

## Related skills

- [`context-load`](../../utils-skills/context-load/SKILL.md) — load feature spec before running this skill
- [`handoff`](../../utils-skills/handoff/SKILL.md) — produces the local-context notes reconciled here
- [`context-update`](../../utils-skills/context-update/SKILL.md) — runs right before to align durable docs with the diff
- [`plan-write`](../../skills-for-planning/plan-write/SKILL.md) — produces the plan reconciled here
- [`business-reports`](../business-reports/SKILL.md) — different audience; do not mix
