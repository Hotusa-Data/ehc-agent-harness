---
name: spec-write
phase: spec
description: |
  Synthesize the current conversation into the Spec-phase document (`specs.md`). Use when the conversation has converged on what to build and the team needs a durable spec before moving to Plan.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
metadata:
  owner: Ignacio Freire
  last_reviewed: "2026-05-28"
  skill-version: "1.2.0"
---

# Spec Write

Synthesize the current conversation and codebase understanding into `specs.md`. Do NOT interview the user — synthesize what is already known.

## When to use

- The conversation has converged on what to build and the user asks for a spec.
- Enough context exists to write the spec without further questions.
- The team needs a durable artifact to hand off to human Spec Review before Plan.

## When NOT to use

- The conversation still has open ambiguity — run [`grill-me`](../../utils-skills/grill-me/SKILL.md) first.
- The user wants to be interviewed to surface requirements — this skill synthesises. Use [`grill-me`](../../utils-skills/grill-me/SKILL.md) instead.
- The task is implementation decisions, module design, or task slicing — those belong in Plan. Use [`plan-write`](../plan-write/SKILL.md).
- The work is a small fix with no user-facing change — skip Spec per lifecycle.md lightweight mode.
- The output is for business stakeholders — use [`business-reports`](../../skills-for-docs/business-reports/SKILL.md).

## Process

### 1. Load context

Follow the DOC-1 load order. Always load `AGENTS.md` and `agent-kit/agent-rules/core.md`.

Then load by what the task requires:

| File | What to extract |
|---|---|
| `docs/docs-guide.md` | Required docs, project overrides, local load-order deviations |
| `docs/glossary.md` | Canonical vocabulary — use it verbatim in acceptance criteria |
| `docs/features/<feature>/` (if touching an existing feature) | Current specs, open questions, prior decisions |
| `docs/architecture.md` | System boundaries — where validation and contracts already live |

If the user referenced an external doc, read it before drafting.

### 2. Explore codebase

Read the modules affected by the change. Look for:

<codebase-signals>
- **Domain entities**: what shapes currently exist at the boundary (models, schemas, enums). Ground the spec examples in real types, not invented names.
- **Existing validation**: what the system already enforces — do not re-spec guarantees that are already in place.
- **Error vocabulary**: what errors or status codes the system already raises. AC edge cases should use these, not invent new ones.
- **Related feature behavior**: which existing flows the new behavior interacts with or replaces. State the delta, not a rewrite of what already works.
- **Glossary gaps**: terms used in the conversation that are not yet in `docs/glossary.md`. Flag them in "Assumptions and Open Questions" and add them after spec review.
</codebase-signals>

Mark unknowns as "unknown — needs confirmation before Plan" rather than inventing values.

### 3. Draft specs

Write the spec using the shape in `agent-kit/skeletons/_specs.md`. The spec answers *what* and *why* — not *how*. Implementation decisions belong in `plan-write`.

Use vocabulary from `docs/glossary.md` throughout. If a term appears in an AC but is absent from the glossary, add it to "Assumptions and Open Questions" — do not coin new terms in a spec without flagging them.

### 4. Write artifact

Save to `docs/features/<feature>/specs.md`, creating the directory and file if they don't exist. Instantiate from `agent-kit/skeletons/_specs.md` when the file is new. If the project uses an issue tracker, also publish with the appropriate triage label — after writing the file.

---

## Anti-patterns

| Anti-pattern | Why it fails |
|---|---|
| Asking the user clarifying questions | This skill synthesises — switch to `grill-me` if you need to interview. |
| Inventing requirements the conversation didn't establish | A spec is a contract; invented scope poisons the rest of the lifecycle. |
| Including implementation or testing decisions | Those belong in Plan (`plan.md`). Spec answers *what* and *why*. |
| Non-observable acceptance criteria | If you cannot observe it, you cannot verify it. |
| Publishing to the tracker before writing `specs.md` | The durable artifact lives in the repo. Always write the file first. |
| Using non-canonical vocabulary | Refresh the glossary before writing if it is in flux. |

---

## Related skills

- [`grill-me`](../../utils-skills/grill-me/SKILL.md) — run before this when ambiguity would weaken the spec.
- [`make-glossary`](../../skills-for-docs/make-glossary/SKILL.md) — refresh canonical vocabulary before writing.
- [`context-load`](../../utils-skills/context-load/SKILL.md) — ensure project and feature context is loaded.
- [`plan-write`](../plan-write/SKILL.md) — natural successor after Spec Review: specs → plan.
