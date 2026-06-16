# Documentation Guide

Per-project inventory of required documents and any local deviations from `agent-kit/agent-rules/documentation.md`. Instantiate at `docs/docs-guide.md`.

This file lists **what this repo requires**. It does not restate load order, validation gates, creation-vs-update policy, or skeleton mapping — those live in [`agent-kit/agent-rules/documentation.md`](../agent-kit/agent-rules/documentation.md) and are the authoritative source. Add deviations only under §3 Project-Specific Overrides.

## 0. Metadata

- Project:
- Owner:
- Last reviewed:
- Related files: `AGENTS.md`, `agent-kit/agent-rules/repo-guide.md`

## 1. Required Docs

| Doc | Status | Purpose |
|---|---|---|
| `AGENTS.md` | required | Entrypoint: cycle, commands, boundaries, what to load, when to clarify |
| `docs/architecture.md` | required | Project overview, layout deltas (§3), project invariants — default codemap in `repo-guide.md` |
| `docs/glossary.md` | required | Canonical vocabulary |
| `docs/docs-guide.md` | required | This file |
| `docs/database.md` | optional | Required if the project persists data |
| `docs/features/<feature>/specs.md` | optional | One per feature; required for non-trivial work |
| `docs/features/<feature>/plan.md` | optional | One per feature; required when work spans multiple slices or needs a technical approach |
| `docs/features/<feature>/report.md` | optional | Created at cycle close |
| `docs/features/<feature>/CHANGELOG.md` | optional | Required when the feature has evolved beyond its initial commit |

Mark docs `required` only if this project actually expects them. Remove rows that do not apply.

## 2. Behavior Reference

For load order, validation gates, creation-vs-update policy, and skeleton-to-doc mapping, see [`agent-kit/agent-rules/documentation.md`](../agent-kit/agent-rules/documentation.md). Do not duplicate those tables here.

## 3. Project-Specific Overrides

Use this section for repository-specific deviations: stricter gates, extra required docs, alternative load order, command overrides, or local rules that take precedence over `agent-rules/documentation.md`. State each override explicitly so the agent can detect it.

- Example: `specs.md` required even for single-slice changes (reason: regulatory) — set Harness mode `full` or override gates in §3.
- Example: test command override — `uv run pytest tests/unit -xvs` (reason: integration tests need Docker; see AGENTS.md §Commands).
- Example: PR title format — `feat(<feature>): <description>` (reason: Conventional Commits; see AGENTS.md §Pull requests).
- Example: harness mode — full cycle for multi-slice features; lightweight work skips phases named in the PR (reason: small typo fix).
- Example: mark `docs/database.md` as `required` once the project persists data (reason: added SQLAlchemy layer).
-

## 4. Change Log

| Date | Change | Reason |
|---|---|---|
|  |  |  |

## Review Checklist

- [ ] Every required doc listed in §1 exists, or has a tracked task to create it.
- [ ] Root `.gitignore` excludes `.local-context/` (session handoffs and scratch notes).
- [ ] Base docs scaffolded from skeletons (or run `python agent-kit/adopt.py --dry-run` to preview what is missing).
- [ ] §3 overrides do not silently contradict `AGENTS.md` or `agent-rules/documentation.md`.
