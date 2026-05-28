---
name: spec-write
phase: spec
description: |
  Synthesize the current conversation into the Spec-phase requirements document (`requirements.md`). Use when the conversation has converged on what to build and the team needs a durable spec before moving to Plan.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
metadata:
  owner: Ignacio Freire
  last_reviewed: "2026-05-28"
  skill-version: "1.1.0"
---

# Spec Write

Synthesize the current conversation and codebase understanding into `requirements.md`. Do NOT interview the user — synthesize what is already known.

## When to use

- The conversation has converged on what to build and the user asks for a spec.
- Enough context exists to write the spec without further questions.
- The team needs a durable artifact to hand off to human Spec Review before Plan.

## When NOT to use

- The conversation still has open ambiguity — run [`grill-me`](../../utils-skills/grill-me/SKILL.md) first.
- The user wants to be interviewed to surface requirements — this skill synthesises. Use [`grill-me`](../../utils-skills/grill-me/SKILL.md) instead.
- The task is implementation decisions or module design — those belong in Plan. Use [`design-write`](../design-write/SKILL.md).
- The work is a small fix with no user-facing change — skip Spec per lifecycle.md lightweight mode.
- The output is for business stakeholders — use [`business-reports`](../../skills-for-docs/business-reports/SKILL.md).

## Process

### 1. Load context

Follow the DOC-1 load order. Always load `AGENTS.md` and `agent-kit/agent-rules/core.md`.

Then load by what the task requires:

| File | What to extract |
|---|---|
| `docs/context/project.md` | Project goals, out-of-scope areas, approved tech stack |
| `docs/glossary.md` | Canonical vocabulary — use it verbatim in acceptance criteria |
| `docs/features/<feature>/` (if touching an existing feature) | Current requirements, open questions, prior decisions |
| `docs/architecture.md` | System boundaries — where validation and contracts already live |

If the user referenced an ADR or external doc, read it before drafting.

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

### 3. Draft requirements

Write the spec using the template below. The spec answers *what* and *why* — not *how*. Implementation decisions belong in `design-write`.

Use vocabulary from `docs/glossary.md` throughout. If a term appears in an AC but is absent from the glossary, add it to "Assumptions and Open Questions" — do not coin new terms in a spec without flagging them.

<requirements-template>

## Problem Statement

The problem from the user's perspective. Include goals: what success looks like and why it matters.

## Current vs Target Behavior

| | Current | Target |
|---|---|---|
| **What happens** | How the system behaves today | How the system behaves after the change |
| **Who is affected** | Who experiences the problem | Who benefits from the fix |
| **When** | When the problem manifests | When the new behavior applies |

## Solution

The proposed solution from the user's perspective. What changes for the user, not how the code changes internally.

## Acceptance Criteria

A numbered list. Each criterion must be **observable** — verifiable via a test, a notebook output, or a before/after diff.

## Concrete Examples

At least one input/output example illustrating the feature end-to-end.

**Input:** (what the user or system provides)

**Output:** (what the system produces or how behavior changes)

**Notes:** (edge cases, variations, or clarifications)

## Out of Scope / Non-goals

What is deliberately not covered. Bounding scope is as important as defining it.

## Assumptions and Open Questions

**Assumptions** — things believed to be true but not verified. Each is a risk if wrong.

**Open Questions** — flag which ones block Plan vs. which can be resolved during implementation.

## Further Notes

Additional context, historical decisions, or references.

</requirements-template>

### 4. Write artifact

Save to `docs/features/<feature>/requirements.md`, creating the directory and file if they don't exist. If the project uses an issue tracker, also publish with the appropriate triage label — after writing the file.

---

## Anti-patterns

| Anti-pattern | Why it fails |
|---|---|
| Asking the user clarifying questions | This skill synthesises — switch to `grill-me` if you need to interview. |
| Inventing requirements the conversation didn't establish | A spec is a contract; invented scope poisons the rest of the lifecycle. |
| Including implementation or testing decisions | Those belong in Plan (`design.md`). Spec answers *what* and *why*. |
| Non-observable acceptance criteria | If you cannot observe it, you cannot verify it. |
| Publishing to the tracker before writing `requirements.md` | The durable artifact lives in the repo. Always write the file first. |
| Using non-canonical vocabulary | Refresh the glossary before writing if it is in flux. |

---

## Related skills

- [`grill-me`](../../utils-skills/grill-me/SKILL.md) — run before this when ambiguity would weaken the requirements.
- [`make-glossary`](../../skills-for-docs/make-glossary/SKILL.md) — refresh canonical vocabulary before writing.
- [`context-load`](../../utils-skills/context-load/SKILL.md) — ensure project and feature context is loaded.
- [`design-write`](../design-write/SKILL.md) — natural successor after Spec Review: spec → technical design.
