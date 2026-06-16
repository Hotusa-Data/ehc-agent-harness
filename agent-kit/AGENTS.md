# AGENTS.md

Entry point for any AI coding agent working in this repository. Read this first.

You are the coding agent for this repo. Domain knowledge lives in `docs/` (consumer-repo artifacts). Engineering rules live in `agent-kit/agent-rules/`. Document skeletons live in `agent-kit/skeletons/`.

> **Note.** If `docs/` is missing, bootstrap with `python agent-kit/adopt.py` or instantiate from `agent-kit/skeletons/` (see [`agent-kit/agent-rules/documentation.md` §DOC-4](agent-kit/agent-rules/documentation.md)). Session scratch notes use gitignored `.local-context/` at the repo root.

---

## Role and scope

This project follows a **Python data stack**: Python 3.x with `uv`/`pyproject.toml`, SQLAlchemy 2.0 + Alembic, Pydantic v2 + Pandera, FastAPI, Typer, `notebooks/` for exploration, `tests/` mirroring the package. Record deviations under `## Project Overrides` in the relevant rule file and in `docs/docs-guide.md` §3.

Work is organized by features under `docs/features/<feature>/`. Non-trivial changes follow the [working cycle](#working-cycle) below.

In monorepos, nested `AGENTS.md` files may exist in subpackages — the file closest to the edited path takes precedence over this one.

---

## Working cycle

Every non-trivial task follows five phases. Lightweight work may skip phases — name what you skip and why (usually in the PR or CHANGELOG).

```
Context → Spec ──[Spec Review]──► Plan ──[Plan Review]──► Build ──[PR Review]──► Document ──► merge
```

Backward loops: if Spec is unclear, return to Context. If an assumption breaks during Build, return to Plan. If docs are stale after Build, return before closing.

| Phase | What you do | Key artifacts |
|---|---|---|
| **Context** | Load rules, project docs, feature state | `AGENTS.md`, `docs/docs-guide.md`, `docs/architecture.md`, `docs/glossary.md` |
| **Spec** | Define what must change and why | `docs/features/<feature>/specs.md` |
| **Plan** | Decide how to implement, slice, test, document | `docs/features/<feature>/plan.md` |
| **Build** | Implement in small, reviewable slices | code, tests, notebook mockups |
| **Document** | Update every durable doc the change touched | glossary, `CHANGELOG.md`, `report.md` |

**Human review stops** — a person must approve before the next phase begins.

| When | What is reviewed | Who |
|---|---|---|
| Post-Spec | `specs.md` — scope, ACs, business rules | Domain expert or lead |
| Post-Plan | `plan.md` — approach, slices, evidence strategy | Technical lead |
| Post-Build | PR diff — implementation, tests, docs | Reviewer assigned to the PR |

---

## Session bootstrap

Always load:

1. `agent-kit/agent-rules/core.md` — universal engineering and collaboration rules
2. `docs/docs-guide.md` — per-project required docs and local overrides (when present); authoritative over kit defaults

For other rules, see [`agent-kit/agent-rules/README.md`](agent-kit/agent-rules/README.md) and [`agent-kit/agent-rules/documentation.md` §DOC-1](agent-kit/agent-rules/documentation.md). Do not load files whose content will not influence the current decision.

---

## Commands

Fill in during adoption. List copy-paste commands the agent should run to build, test, lint, and run the app. Authoritative overrides may also live in `docs/docs-guide.md` §3 Project-Specific Overrides.

| Action | Command |
|---|---|
| Install dependencies | `uv sync` _(adapt to project)_ |
| Run all tests | `uv run pytest` _(adapt path/flags)_ |
| Run one test | `uv run pytest path/to/test.py::test_name -xvs` |
| Lint | `uv run ruff check .` _(or project equivalent)_ |
| Format | `uv run ruff format .` _(or project equivalent)_ |
| Type-check | _(if applicable — e.g. `uv run mypy src/`)_ |
| Run app / notebook | _(project-specific)_ |

Scope commands to changed packages in monorepos. See [`agent-kit/agent-rules/testing.md`](agent-kit/agent-rules/testing.md) and [`agent-kit/agent-rules/python.md`](agent-kit/agent-rules/python.md) for conventions.

---

## Verification before PR

Before requesting review or marking work complete:

- [ ] Relevant tests for changed behavior pass (see [Commands](#commands))
- [ ] Lint/format checks pass on touched files
- [ ] For non-trivial work: feature docs and touched base docs match the code (see `agent-kit/agent-rules/documentation.md` §DOC-8)
- [ ] No secrets, credentials, or `.local-context/` content in the diff
- [ ] Distinguish what you ran from what you only wrote (see `core.md` §COOP-3)

---

## Pull requests

Fill in during adoption. Title format and commit conventions may also be overridden in `docs/docs-guide.md` §3.

**Title format:** `[<feature>] <short user-facing impact>` _(adapt — e.g. Conventional Commits scope)_

**Description must include:**

- What changed and why (2–4 sentences)
- Feature link: `docs/features/<feature>/` when applicable
- Test evidence: commands run and outcome (see [Verification before PR](#verification-before-pr))
- Lifecycle: phases skipped and why, if any
- Open questions or follow-ups for the reviewer

**Commits:** _(adapt — e.g. imperative subject line; one logical change per commit)_

A human opens and publishes the PR — do not push to remote (see [Boundaries](#boundaries)). Draft the description from specs, plan, and diff before handoff to the reviewer.

---

## Boundaries

**Ask first**

- Scope, acceptance criteria, or business-rule changes mid-build
- New dependencies, database migrations, or destructive data operations
- Skipping a lifecycle phase on non-trivial work
- Running commands through subshells or one-liner interpreters (`bash -c`, `python -c`, etc.)

**Never**

- Push to remote, publish packages, or bypass git hooks (`--no-verify`, etc.) — a human publishes
- Commit secrets, credentials, tokens, or anything under `.local-context/`
- Invent business rules, thresholds, or schemas not in specs or glossary (see `core.md` §COOP-1)
- Edit generated artifacts by hand when a generator workflow exists
- Modify files unless the user requested the change or confirmed the plan

Human review gates (Spec, Plan, PR) are mandatory for non-trivial work — see [Working cycle](#working-cycle).

---

## Where durable knowledge lives

Project-specific knowledge lives in `docs/` (created on demand via `adopt.py` or skeletons):

`docs/architecture.md`, `docs/database.md`, `docs/glossary.md`, `docs/docs-guide.md`, and `docs/features/<feature>/{specs,plan,CHANGELOG,report}.md`.

If a target doc does not exist, instantiate it from the matching skeleton — see [`agent-kit/agent-rules/documentation.md` §DOC-4](agent-kit/agent-rules/documentation.md).

Handoffs and throwaway notes live in `.local-context/` at the repo root — gitignored, never committed. Promote anything durable into `docs/` before closing the cycle.
