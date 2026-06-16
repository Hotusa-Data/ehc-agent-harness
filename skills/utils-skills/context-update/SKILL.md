---
name: context-update
phase: document
description: |
  Step-by-step documentation update at the end of a session. Reviews what was generated or decided, then updates each affected file — feature specs, plan, CHANGELOG, glossary, ADRs, docs-guide — one at a time, always asking the developer for confirmation before writing. Use this skill at the end of any session where artefacts were generated or decisions were made.
allowed-tools:
  - Read
  - Edit
  - Write
  - Glob
metadata:
  owner: Ignacio Freire
  last_reviewed: "2026-05-27"
  skill-version: "1.0.0"
---

# Context Update

Close the documentation loop after every productive session. Never auto-write - every change requires explicit developer confirmation.

---

## When to use

- At the end of any session where specs, plans, code, or decisions were produced or changed.
- Before opening a PR — pair with [`pr-summary`](../../skills-for-docs/pr-summary/SKILL.md) after reconciliation.
- When the session introduced new vocabulary that should land in `docs/glossary.md`.

## When NOT to use

- At session start — use [`context-load`](../context-load/SKILL.md) instead.
- When nothing durable changed (exploratory chat with no decisions or artifacts).
- To auto-write without developer confirmation — every file update requires explicit approval.

---

## Invocation

```text
/context-update
```

No arguments required. The skill reviews the current session automatically.

---

## Step 0 - Session review

Before touching any file, summarise what happened:

```text
Session summary:
- Feature worked on: <feature>
- Artefacts generated/modified: [list paths]
- Decisions made: [list key decisions]
- Files that may need updating: [list]
```

Ask: `Does this summary look right, or is anything missing?`

Wait for developer confirmation before proceeding.

---

## Step 1 - Feature specs (`docs/features/<feature>/specs.md`)

Check whether the specs need updating:
- Were any ACs resolved, deferred, or changed?
- Were open questions answered?
- Did scope or status change?

If yes, show the proposed changes and ask for confirmation.
If no, say: `Specs do not need updating - skipping.`

---

## Step 2 - Feature plan (`docs/features/<feature>/plan.md`)

Check whether the plan needs updating:
- Did the approach change?
- Were new contracts added or removed?
- Were any **§1** tasks completed, added, or removed (Status column)?
- Did **§2** testing plan or **§3** evidence rows need adjustment?
- Did **§6** external dependencies or **§7** future TODOs change?

If yes, show the proposed changes and ask for confirmation.
If no, say: `Plan does not need updating - skipping.`

When the feature cycle closes, confirm `report.md` **Build verification (internal)** matches final `plan.md` §1–§3 and §7.

---

## Step 3 - Feature CHANGELOG (`docs/features/<feature>/CHANGELOG.md`)

For every non-trivial change made above, append an entry under `[Unreleased]`:
- Use the right section (Specs / Plan / Decided / Added / Changed / Removed / Fixed)
- Include the **why**, not just the what
- One line per change

If the feature shipped this session, bump from `[Unreleased]` to a new version section (`[X.Y.Z] - YYYY-MM-DD`).

Show the proposed entries and ask for confirmation.

---

## Step 4 - Glossary (`docs/glossary.md`)

Check whether new vocabulary was introduced or clarified.

If yes, show the proposed additions and ask for confirmation.
If no, say: `No new glossary terms - skipping.`

---

## Step 5 - Project docs (`docs/adr/`, `docs/docs-guide.md`)

Check whether durable project knowledge changed:
- Structural decision (layout, integration, project-wide invariant)? → new or updated ADR + index row in `docs/adr/README.md`
- New required docs, stricter gates, or load-order overrides for this repo? → `docs/docs-guide.md`

If yes, show the proposed changes and ask for confirmation.
If no, say: `Project docs do not need updating - skipping.`

---

## Step 6 - Completion summary

```text
Documentation update complete.

Updated:
- docs/features/<feature>/specs.md ✓
- docs/features/<feature>/plan.md - skipped (no changes needed)
- docs/features/<feature>/CHANGELOG.md ✓
- docs/glossary.md ✓
- docs/adr/ - skipped
- docs/docs-guide.md - skipped

Remember: run /context-update at the end of every session.
```

---

## Rules

- **Never auto-write.** Every file change requires explicit developer approval.
- **One file at a time.** Complete each step before moving to the next.
- **Show diffs, not summaries.** The developer must see exactly what will change.
- **Skip gracefully.** If a file does not need updating, say so and move on.
- **CHANGELOG is non-negotiable** for non-trivial changes - that is the trazability mechanism.
- **Be specific.** Show concrete changes, not generic "updated context".
- **Do not rewrite existing content** unless correcting an error - append and update only.

---

## Related skills

- [`context-load`](../context-load/SKILL.md) — its opening counterpart at the start of the session.
- [`pr-summary`](../../skills-for-docs/pr-summary/SKILL.md) — runs after this when the session ends in a PR.
- [`make-glossary`](../../skills-for-docs/make-glossary/SKILL.md) — invoke when the session introduced enough vocabulary to warrant a full refresh, not a per-term inline edit.
