# Documentation Guide

Per-project inventory of required documents and any local deviations from `agent-kit/agent-rules/documentation.md`. Instantiate at `docs/docs-guide.md`.

This file lists **what this repo requires**. It does not restate load order, validation gates, creation-vs-update policy, or skeleton mapping — those live in [`agent-kit/agent-rules/documentation.md`](../agent-kit/agent-rules/documentation.md) and are the authoritative source. Add deviations only under §3 Project-Specific Overrides.

## 0. Metadata

- Project:
- Owner:
- Last reviewed:
- Related files: `AGENTS.md`, `docs/context/project.md`, `agent-kit/agent-rules/repo-guide.md`

## 1. Required Docs

| Doc | Status | Purpose |
|---|---|---|
| `AGENTS.md` | required | Entrypoint: how the agent works, what to load, when to clarify |
| `docs/context/project.md` | required | Project-level truth (mission, stack, features in scope, global decisions) |
| `docs/architecture.md` | required | System shape: components, runtime boundaries, integrations |
| `docs/glossary.md` | required | Canonical vocabulary |
| `docs/docs-guide.md` | required | This file |
| `docs/manifest.yaml` | required | Inventory of all generated artifacts in this repo |
| `docs/database.md` | optional | Required if the project persists data |
| `docs/features/<feature>/requirements.md` | optional | One per feature in active scope |
| `docs/features/<feature>/design.md` | optional | One per feature; required for non-trivial work |
| `docs/features/<feature>/tasks.md` | optional | One per feature; required when work spans multiple slices |
| `docs/features/<feature>/report.md` | optional | Created at cycle close |
| `docs/features/<feature>/CHANGELOG.md` | optional | Required when the feature has evolved beyond its initial commit |

Mark docs `required` only if this project actually expects them. Remove rows that do not apply.

## 2. Behavior Reference

For load order, validation gates, creation-vs-update policy, and skeleton-to-doc mapping, see [`agent-kit/agent-rules/documentation.md`](../agent-kit/agent-rules/documentation.md). Do not duplicate those tables here.

## 3. Project-Specific Overrides

Use this section for repository-specific deviations: stricter gates, extra required docs, alternative load order, or local rules that take precedence over `agent-rules/documentation.md`. State each override explicitly so the agent can detect it.

- Example: `requirements.md` is required even for single-slice changes in this repo (reason: regulatory).
-

## 4. Change Log

| Date | Change | Reason |
|---|---|---|
|  |  |  |

## Review Checklist

- [ ] Every required doc listed in §1 exists, or has a tracked task to create it.
- [ ] §3 overrides do not silently contradict `AGENTS.md` or `agent-rules/documentation.md`.
