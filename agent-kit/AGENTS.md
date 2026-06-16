# AGENTS.md

Entry point for any AI coding agent working in this repository. Read this first.

You are the coding agent for this repo. Domain knowledge lives in `docs/` (consumer-repo artifacts). Engineering rules live in `agent-kit/agent-rules/`. Document skeletons live in `agent-kit/skeletons/`.

> **Metarepo note.** When this file is read inside the **ehc-agent-harness** metarepo itself, `docs/` usually does not exist yet — that tree is created on adoption in a consumer project. Here, load `agent-kit/agent-rules/` and `guides/` instead of project docs. Session scratch notes still use gitignored `.local-context/` at the repo root.

---

## Role and scope

This project follows a **Python data stack** (see [Assumed stack](#assumed-stack)). Work is organized by features under `docs/features/<feature>/`. Non-trivial changes follow the [working cycle](#working-cycle) below.

In monorepos, nested `AGENTS.md` files may exist in subpackages — the file closest to the edited path takes precedence over this one.

---

## Working cycle

Every non-trivial task follows five phases. Lightweight work may skip phases — name what you skip and why.

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

For task-specific loads (feature work, persistence, tests, security, etc.), see [`agent-kit/agent-rules/documentation.md` §DOC-1](agent-kit/agent-rules/documentation.md). Do not load files whose content will not influence the current decision.

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
- [ ] For non-trivial work: `specs.md`, `plan.md`, and `CHANGELOG.md` do not contradict the code
- [ ] No secrets, credentials, or `.local-context/` content in the diff
- [ ] Distinguish what you ran from what you only wrote (see `core.md` §COOP-3)

Lightweight work may skip lifecycle phases — name what you skipped and why (usually in the PR or CHANGELOG).

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

Project-specific knowledge lives in `docs/` in the **consumer repo** (created on demand, not shipped by this kit):

```text
docs/
├── architecture.md
├── database.md
├── glossary.md
├── docs-guide.md
└── features/<feature>/
    ├── specs.md
    ├── plan.md
    ├── CHANGELOG.md
    └── report.md
```

If a target doc does not exist, instantiate it from the matching skeleton — see [`agent-kit/agent-rules/documentation.md` §DOC-4](agent-kit/agent-rules/documentation.md).

### Session scratch (never committed)

Handoffs and throwaway notes live in `.local-context/` at the repo root — gitignored, never committed. Promote anything durable into `docs/` before closing the cycle.

---

## Rules index

All rules live in `agent-kit/agent-rules/`. Each file declares its own `Load when:` in front-matter — load just-in-time.

- `core.md` — engineering and collaboration principles (always)
- `documentation.md` — load order, validation gates, skeleton mapping
- `architecture.md` — module, layer, system-boundary decisions
- `python.md` — Python code
- `persistence.md` — ORM, queries, migrations, sessions
- `testing.md` — tests
- `validation.md` — input checks, contracts, failure handling
- `security.md` — auth, secrets, trust boundaries
- `observability.md` — logs, metrics, tracing
- `repo-guide.md` — file/folder placement

Ambiguity and stop-to-clarify rules: see `core.md` §COOP-1 and §COOP-2.

---

## Assumed stack

Python data-project stack: Python 3.x with `uv`/`pyproject.toml`, SQLAlchemy 2.0 + Alembic, Pydantic v2 + Pandera, FastAPI, Typer, `notebooks/` for exploration, `tests/` mirroring the package.

If the project deviates, record the deviation under `## Project Overrides` in the relevant rule file and in `docs/docs-guide.md` §3 before applying it.

---

## References

- Load order, validation gates, skeleton mapping: [`agent-kit/agent-rules/documentation.md`](agent-kit/agent-rules/documentation.md)
- File and folder placement: [`agent-kit/agent-rules/repo-guide.md`](agent-kit/agent-rules/repo-guide.md)
- Human onboarding (kit adoption, `adopt.py`): metarepo `README.md` Track 1, `guides/onboarding/lifecycle.md`, `guides/onboarding/managing-context.md`
- Skills by lifecycle phase: metarepo `skills/README.md`
