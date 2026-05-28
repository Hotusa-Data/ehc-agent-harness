---
name: context-load
phase: context
description: |
  Load the right context for a session. Always loads the framework layer (agent-kit/agent-rules/core.md) and optional project-level overrides (docs/docs-guide.md). Loads the project layer (docs/context/project.md, docs/architecture.md) when the task touches the project domain. Loads the feature layer (docs/features/<feature>/) — inferred from the conversation if not provided as argument, or listed for the developer to choose from if inference is not possible. Checks the session layer (.local-context/) when handoff notes exist. Use this skill at the start of any session before doing meaningful work.
allowed-tools:
  - Read
  - Glob
metadata:
  owner: Ignacio Freire
  last_reviewed: "2026-05-27"
  skill-version: "2.0.0"
---

# Context Load

Load context before working, following the four-layer model defined in `guides/onboarding/lifecycle.md`. An AI that skips this step invents decisions already made.

---

## Invocation

```text
/context-load [feature]
```

`feature` is optional. If omitted, the skill infers the feature from the conversation.

---

## Step 1 — Load framework context

Always loads (whether or not the task is related to a feature):

1. `agent-kit/agent-rules/core.md` — universal engineering and collaboration rules. Skip if already loaded in the session.
2. `docs/docs-guide.md` — per-project required docs and local overrides (when present). If it exists, defer to it for load order over the defaults in this kit (see `agent-kit/agent-rules/documentation.md` §DOC-5).

`AGENTS.md` is assumed already read — it is the session entry point.

---

## Step 2 — Load project context

Read `docs/context/project.md` if it exists. If the task touches the project domain (scope, stack, global decisions) and the file is missing, notify the developer:

```text
docs/context/project.md is missing.
Create it from the skeleton: it must describe the project scope, stack, and global decisions in domain language.
```

Read `docs/architecture.md` if it exists and the task involves architectural or system-boundary decisions.

For task-type-specific loads (persistence, tests, security, Python, etc.), see `agent-kit/agent-rules/documentation.md` §DOC-1.

---

## Step 3 — Check session context

Read all files under `.local-context/` if the directory exists. These contain handoff notes, partial work, or decisions from a previous session that the current session should inherit.

---

## Step 4 — Identify the feature

If a feature argument was provided, use it.

If no argument was provided, infer the feature from the conversation:
- Look at the task description, file paths mentioned, feature names.
- Match against existing folders in `docs/features/`.

If inference is not possible, list available features and ask the developer to select one:

```text
Available features:
- user-import   -> docs/features/user-import/
- billing-export -> docs/features/billing-export/
- auth-rewrite  -> docs/features/auth-rewrite/

Which feature are you working on?
```

If the developer selects "none" or confirms no existing feature applies, ask whether to create a new feature folder. If yes, scaffold from the skeletons. If no, proceed without feature context and note the gap.

---

## Step 5 — Load feature context

Read these in order, skipping any that do not exist:

1. `docs/features/<feature>/requirements.md`
2. `docs/features/<feature>/design.md`
3. `docs/features/<feature>/tasks.md`
4. `docs/features/<feature>/CHANGELOG.md`

Do not load `report.md` by default — it only exists for shipped cycles and is rarely needed during active work.

If the feature folder does not exist:
1. Notify the developer: `docs/features/<feature>/ does not exist.`
2. Ask: `Create it now from the templates?`
3. If yes, scaffold `requirements.md`, `design.md`, `tasks.md`, and `CHANGELOG.md` from skeletons — but do not write without developer confirmation.
4. If no, proceed without feature context and note the gap.

---

## Step 6 — Confirm and summarise

```text
Context loaded:
- Framework: agent-kit/agent-rules/core.md ✓
- Project: docs/context/project.md ✓  (last updated: YYYY-MM-DD)
- Architecture: docs/architecture.md — (missing, skipped)
- Docs guide: docs/docs-guide.md — (missing, skipped)
- Session: .local-context/ — (missing, skipped)
- Feature: docs/features/<feature>/ ✓
  - requirements.md ✓  (status: active)
  - design.md ✓  (status: active)
  - tasks.md ✓  (3 of 7 tasks done)
  - CHANGELOG.md ✓  (last entry: YYYY-MM-DD)

Ready to work on: <feature or task description>
```

If anything was missing or skipped, say so explicitly.

---

## Rules

- Do not start meaningful work before this skill completes.
- Do not load context for unrelated features — one feature per session is the norm.
- If the project context is significantly outdated (last updated > 30 days), flag it.
- Never invent project goals, feature scope, or decisions not found in the loaded files.

---

## Related skills

- [`context-update`](../context-update/SKILL.md) — its closing counterpart at the end of the session.
- [`make-glossary`](../../skills-for-docs/make-glossary/SKILL.md) — invoke if the glossary referenced by project context does not exist yet.
- [`grill-me`](../grill-me/SKILL.md) — invoke when loaded context surfaces ambiguity that blocks the work.
