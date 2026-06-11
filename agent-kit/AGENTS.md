# AGENTS.md

Entry point for any AI coding agent working in this repository. Read this first.

You are the coding agent for this repo. All durable knowledge lives in `docs/` (consumer-repo artifacts). All rules live in `agent-kit/agent-rules/`. All document skeletons live in `agent-kit/skeletons/`.

---

## Working cycle

Every non-trivial task follows five phases. Lightweight work may skip phases — name what you skip and why.

```
Context → Spec ──[Spec Review]──► Plan ──[Plan Review]──► Build ──[PR Review]──► Document ──► merge
```

Backward loops: if Spec is unclear, return to Context. If an assumption breaks during Build, return to Plan. If docs are stale after Build, return before closing.

| Phase | What you do | Key artifacts |
|---|---|---|
| **Context** | Load rules, project context, feature state | `AGENTS.md`, `docs/context/project.md`, `docs/glossary.md` |
| **Spec** | Define what must change and why | `docs/features/<feature>/requirements.md` |
| **Plan** | Decide how to implement, slice, test, document | `docs/features/<feature>/design.md`, `tasks.md` |
| **Build** | Implement in small, reviewable slices | code, tests, notebook mockups |
| **Document** | Update every durable doc the change touched | glossary, CHANGELOG, report |

**Human review stops** — a person must approve before the next phase begins.

| When | What is reviewed | Who |
|---|---|---|
| Post-Spec | `requirements.md` — scope, ACs, business rules | Domain expert or lead |
| Post-Plan | `design.md` + `tasks.md` — approach, slices, evidence strategy | Technical lead |
| Post-Build | PR diff — implementation, tests, docs | Reviewer assigned to the PR |

---

## What to load at the start of every session

Always:
1. `agent-kit/agent-rules/core.md` — universal engineering and collaboration rules
2. `docs/context/project.md` — project-level source of truth (when present)
3. `docs/docs-guide.md` — per-project required docs and local overrides (when present); authoritative over the defaults in this kit

For task-specific loads (feature work, persistence, tests, security, etc.), see [`agent-rules/documentation.md` §DOC-1](agent-rules/documentation.md). Do not load files whose content will not influence the current decision.

---

## Where durable knowledge lives

Project-specific knowledge lives in `docs/` in the **consumer repo** (created on demand, not shipped by this kit):

```text
docs/
├── context/project.md
├── architecture.md
├── database.md
├── glossary.md
├── docs-guide.md
└── features/<feature>/
    ├── requirements.md
    ├── design.md
    ├── tasks.md
    ├── CHANGELOG.md
    └── report.md
```

If a target doc does not exist, instantiate it from the matching skeleton in `agent-kit/skeletons/`. Skeleton-to-doc mapping: [`agent-rules/documentation.md` §DOC-4](agent-rules/documentation.md).

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

If the project deviates, record the deviation under `## Project Overrides` in the relevant rule file before applying it.
