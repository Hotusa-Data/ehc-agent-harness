---
name: context-load
phase: context
description: |
  Load the right context for a session. Always loads the framework layer (agent-kit/agent-rules/CORE.md) and optional project-level overrides (docs/docs-guide.md). Loads the project layer (docs/adr/, docs/glossary.md) when the task touches the project domain. Loads the feature layer (docs/features/<feature>/) — inferred from the conversation if not provided as argument, or listed for the developer to choose from if inference is not possible. Checks the session layer (.local-context/) when handoff notes exist. Use this skill at the start of any session before doing meaningful work.
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

## When to use

- At the start of any session before meaningful work begins.
- When resuming work on a feature and durable docs may have changed since the last session.
- After receiving a handoff — load `.local-context/` and the referenced feature folder.

## When NOT to use

- Mid-session when context is already loaded and confirmed for the current feature.
- Purely mechanical edits with no feature, domain, or architectural implications (lightweight mode may skip).
- As a substitute for [`grill-me`](../grill-me/SKILL.md) when ambiguity blocks the work — load first, then grill if needed.

---

## Invocation

```text
/context-load [feature]
```

`feature` is optional. If omitted, the skill infers the feature from the conversation.

---

## Step 1 — Load framework context

Always loads (whether or not the task is related to a feature):

1. `agent-kit/agent-rules/CORE.md` — universal engineering and collaboration rules. Skip if already loaded in the session.
2. `docs/docs-guide.md` — per-project required docs and local overrides (when present). If it exists, defer to it for load order over the defaults in this kit (see `agent-kit/agent-rules/DOCUMENTATION.md` §DOC-5).

Optional index (when choosing JIT rules): `agent-kit/agent-rules/RULES.md`.

`AGENTS.md` is assumed already read — it is the session entry point.

---

## Step 2 — Load project docs

Read `docs/adr/README.md` and matching ADRs (by **Load when** in the index) when the task involves architectural or system-boundary decisions. Always read `docs/adr/0002-system-context.md` when onboarding or scope is unclear.

Read `docs/glossary.md` when the task uses business vocabulary.

For task-type-specific loads, use this table (authoritative source: `agent-kit/agent-rules/DOCUMENTATION.md` §DOC-1):

| Task type | Add to load |
|---|---|
| Touches an existing feature | `docs/features/<feature>/{specs,plan,CHANGELOG}.md` |
| Uses business vocabulary | `docs/glossary.md` |
| Placement or structure unclear | `REPO_GUIDE.md`, `docs/adr/README.md` + relevant ADR |
| Layer contracts, circular imports | `ARCHITECTURE.md` |
| ORM, queries, migrations, sessions | `PERSISTENCE.md`, `docs/database.md` |
| Auth, secrets, trust boundaries | `SECURITY.md` |
| Tests | `TESTING.md` |
| Input checks, contracts | `VALIDATION.md` |
| Logs, metrics, tracing | `OBSERVABILITY.md` |
| Python code | `PYTHON.md` |

Paths above are under `agent-kit/agent-rules/` unless noted.

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

1. `docs/features/<feature>/specs.md`
2. `docs/features/<feature>/plan.md`
3. `docs/features/<feature>/CHANGELOG.md`

Do not load `report.md` by default — it only exists for shipped cycles and is rarely needed during active work.

If the feature folder does not exist:
1. Notify the developer: `docs/features/<feature>/ does not exist.`
2. Ask: `Create it now from the templates?`
3. If yes, scaffold `specs.md`, `plan.md`, and `CHANGELOG.md` from skeletons — but do not write without developer confirmation.
4. If no, proceed without feature context and note the gap.

---

## Step 6 — Confirm and summarise

```text
Context loaded:
- Framework: agent-kit/agent-rules/CORE.md ✓
- Docs guide: docs/docs-guide.md ✓
- ADRs: docs/adr/README.md — (missing, skipped)
- Glossary: docs/glossary.md — (missing, skipped)
- Session: .local-context/ — (missing, skipped)
- Feature: docs/features/<feature>/ ✓
  - specs.md ✓  (status: active)
  - plan.md ✓  (3 of 7 tasks done)
  - CHANGELOG.md ✓  (last entry: YYYY-MM-DD)

Ready to work on: <feature or task description>
```

If anything was missing or skipped, say so explicitly.

---

## Rules

- Do not start meaningful work before this skill completes.
- Do not load context for unrelated features — one feature per session is the norm.
- If loaded project docs are significantly outdated (last updated > 30 days), flag it.
- Never invent project goals, feature scope, or decisions not found in the loaded files.

---

## Related skills

- [`context-update`](../context-update/SKILL.md) — its closing counterpart at the end of the session.
- [`make-glossary`](../../skills-for-docs/make-glossary/SKILL.md) — invoke if the glossary does not exist yet.
- [`grill-me`](../grill-me/SKILL.md) — invoke when loaded context surfaces ambiguity that blocks the work.
