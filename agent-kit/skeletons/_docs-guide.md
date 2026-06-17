# Documentation Guide

Per-project inventory of required documents and any local deviations from `agent-kit/agent-rules/DOCUMENTATION.md`. Instantiate at `docs/docs-guide.md`.

This file lists **what this repo requires**. It does not restate load order, validation gates, creation-vs-update policy, or skeleton mapping — those live in [`agent-kit/agent-rules/DOCUMENTATION.md`](../agent-kit/agent-rules/DOCUMENTATION.md) and are the authoritative source. Add deviations only under §3 Project-Specific Overrides.

## 0. Metadata

- Project:
- Owner:
- Last reviewed:
- Related files: `AGENTS.md`, `agent-kit/agent-rules/REPO_GUIDE.md`

## 1. Required Docs

| Doc | Status | Purpose |
|---|---|---|
| `AGENTS.md` | required | Entrypoint: cycle, commands, boundaries, what to load, when to clarify |
| `docs/adr/` | required | Structural decisions; `adopt.py` scaffolds `changelog.md` (index) and `0001-system-context.md` — see **DOC-10** |
| `docs/glossary.md` | required | Canonical vocabulary |
| `docs/docs-guide.md` | required | This file |
| `docs/database.md` | optional | Required if the project persists data |
| `docs/features/<feature>/specs.md` | optional | One per feature; required for non-trivial work |
| `docs/features/<feature>/plan.md` | optional | One per feature; required when work spans multiple slices or needs a technical approach |
| `docs/features/<feature>/report.md` | optional | Created at cycle close |
| `docs/features/<feature>/changelog.md` | optional | Required when the feature has evolved beyond its initial commit |

Mark docs `required` only if this project actually expects them. Remove rows that do not apply.

## 2. Behavior Reference

For load order, validation gates, creation-vs-update policy, and skeleton-to-doc mapping, see [`agent-kit/agent-rules/DOCUMENTATION.md`](../agent-kit/agent-rules/DOCUMENTATION.md). Do not duplicate those tables here.

## 3. Project-Specific Overrides

Use this section for repository-specific deviations: stricter gates, extra required docs, alternative load order, command overrides, or local rules that take precedence over `agent-rules/DOCUMENTATION.md`. State each override explicitly so the agent can detect it.

- Example: work sizing — typo or one-file fix with obvious verification → **lightweight** (no specs/plan; name skips in PR).
- Example: behavior change with 2–3 slices → **non-trivial standard** (`Harness mode: standard` in specs/plan).
- Example: new API + migration + rollout → **non-trivial full** (`Harness mode: full` in specs/plan).
- Example: test command override — `uv run pytest tests/unit -xvs` (reason: integration tests need Docker; see AGENTS.md §Commands).
- Example: PR title format — `feat(<feature>): <description>` (reason: Conventional Commits; see AGENTS.md §Pull requests).
- Example: mark `docs/database.md` as `required` once the project persists data (reason: added SQLAlchemy layer).
- Example: **non-Python repo** — replace `AGENTS.md` §Commands; in §3 list skipped rules (`PERSISTENCE.md`, `PYTHON.md` PY-13–16, Pandera sections in `VALIDATION.md`); add layout ADR if folder tree differs from `REPO_GUIDE.md`.
- Example: **no database** — mark `docs/database.md` not applicable; skip `PERSISTENCE.md` unless touching external persistence.
-

## 4. Change Log

| Date | Change | Reason |
|---|---|---|
|  |  |  |

## Review Checklist

- [ ] Every required doc listed in §1 exists, or has a tracked task to create it.
- [ ] Root `.gitignore` excludes `.local-context/` (session handoffs and scratch notes).
- [ ] Base docs scaffolded from skeletons (or run `python agent-kit/adopt.py --dry-run` to preview what is missing).
- [ ] §3 overrides do not silently contradict `AGENTS.md` or `agent-rules/DOCUMENTATION.md`.
