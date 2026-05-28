---
name: context-update
phase: document
description: |
  Step-by-step documentation update at the end of a session. Reviews what was generated or decided, then updates each affected file — feature requirements, design, tasks, CHANGELOG, glossary, project context — one at a time, always asking the developer for confirmation before writing. Use this skill at the end of any session where artefacts were generated or decisions were made.
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

## Step 1 - Feature requirements (`docs/features/<feature>/requirements.md`)

Check whether requirements need updating:
- Were any ACs resolved, deferred, or changed?
- Were open questions answered?
- Did the status change?

If yes, show the proposed changes and ask for confirmation.
If no, say: `Requirements do not need updating - skipping.`

---

## Step 2 - Feature design (`docs/features/<feature>/design.md`)

Check whether the design needs updating:
- Did the approach change?
- Were new contracts added or removed?
- Did risks or assumptions shift?

If yes, show the proposed changes and ask for confirmation.
If no, say: `Design does not need updating - skipping.`

---

## Step 3 - Feature tasks (`docs/features/<feature>/tasks.md`)

Check whether tasks need updating:
- Were any tasks completed, added, or removed?
- Did dependencies shift?
- Did slice ordering change?

If yes, show the proposed changes and ask for confirmation.
If no, say: `Tasks do not need updating - skipping.`

---

## Step 4 - Feature CHANGELOG (`docs/features/<feature>/CHANGELOG.md`)

For every non-trivial change made above, append an entry under `[Unreleased]`:
- Use the right section (Requirements / Design / Tasks / Decided / Added / Changed / Removed / Fixed)
- Include the **why**, not just the what
- One line per change

If the feature shipped this session, bump from `[Unreleased]` to a new version section (`[X.Y.Z] - YYYY-MM-DD`).

Show the proposed entries and ask for confirmation.

---

## Step 5 - Glossary (`docs/glossary.md`)

Check whether new vocabulary was introduced or clarified.

If yes, show the proposed additions and ask for confirmation.
If no, say: `No new glossary terms - skipping.`

---

## Step 6 - Project context (`docs/context/project.md`)

Check whether project-level truth changed:
- New features in scope?
- Global decisions made?
- Stack changes?

If yes, show the proposed changes and ask for confirmation.
If no, say: `Project context does not need updating - skipping.`

---

## Step 7 - Completion summary

```text
Documentation update complete.

Updated:
- docs/features/<feature>/requirements.md ✓
- docs/features/<feature>/design.md - skipped (no changes needed)
- docs/features/<feature>/tasks.md ✓
- docs/features/<feature>/CHANGELOG.md ✓
- docs/glossary.md ✓
- docs/context/project.md - skipped

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
- [`pr-gate`](../pr-gate/SKILL.md) — runs immediately after this when the session ends in a PR.
- [`make-glossary`](../../skills-for-docs/make-glossary/SKILL.md) — invoke when the session introduced enough vocabulary to warrant a full refresh, not a per-term inline edit.
