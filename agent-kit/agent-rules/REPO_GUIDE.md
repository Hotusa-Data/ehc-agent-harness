---
triggers: [placement, structure, new-file, new-folder, codemap, layout]
requires: [CORE]
see-also: [ARCHITECTURE, DOCUMENTATION]
---

# Repository Layout And Placement

Default **codemap** for the kit's **Python data stack** profile: where files and folders live and how package layers depend on each other. For typed contracts across layers, circular imports, and abstraction boundaries, see [ARCHITECTURE](ARCHITECTURE.md). Project-specific layout deltas belong in `docs/adr/` (layout ADRs) and `docs/docs-guide.md` §3. Non-Python or different layouts: override in §3 and see [`../README.md`](../README.md).

Load when: about to create a new file or folder, deciding which layer owns a change, or answering "where does X go?".

Unlike a project-instantiated doc, this file encodes the **default layout** the agent-kit assumes. Project-specific deviations belong in `docs/docs-guide.md` §3 "Project-Specific Overrides" and `docs/adr/` (one ADR per structural deviation).

## Default Top-Level Map

```text
repo-root/
|-- AGENTS.md         # agent entrypoint (from agent-kit/AGENTS.md template)
|-- agent-kit/        # rules, skeletons, adopt.py
|-- docs/
|   |-- features/
|   |-- adr/
|   |-- database.md
|   |-- glossary.md
|   `-- docs-guide.md
|-- notebooks/
|-- pyscripts/      # optional — exploratory scripts (see REPO-3)
|-- scripts/
|-- tests/
|-- <package_name>/
|-- pyproject.toml
`-- Makefile
```

If the real repo deviates, override in `docs/docs-guide.md` §3 and record deltas in `docs/adr/` (new ADR per deviation).

## Rules

### REPO-1 Feature folders are the unit of scope [MUST]

Each feature lives in `docs/features/<feature>/` with:

| File | Purpose |
|---|---|
| `specs.md` | What and why |
| `plan.md` | How and atomic work units |
| `report.md` | What was actually built (created at cycle close) |
| `changelog.md` | Narrative of evolution |

`docs/adr/changelog.md` indexes structural ADRs (see **DOC-10**). Same lowercase `changelog.md` convention; different skeleton (`_adr.md` §Index).

"Feature" covers user-facing features, subsystems, or substantial refactors. Never split one coherent scope into parallel folders.

### REPO-2 Package layers have fixed responsibilities [MUST]

Default package layout for the Python data-project template:

```text
<package_name>/
|-- api/          # FastAPI routes (response_model, Depends)
|-- cli/          # Typer commands (app.add_typer composition)
|-- core/         # config (BaseSettings), logger, types, exceptions
|-- data/         # ETL, ingestion, transformations
|-- db/           # engine, SessionLocal, base
|-- models/       # SQLAlchemy 2.0 (Mapped, mapped_column) — by domain
|-- schemas/      # Pydantic v2 (API + CRUD payloads) — mirrors models/
|-- schemas_df/   # Pandera DataFrame contracts — mirrors models/
|-- crud/         # CRUDBase[Model, Schema, DFSchema] subclasses
|-- ml/           # training, evaluation, inference (when present)
`-- viz/          # plotting helpers (when present)
```

Responsibilities:

| Folder | Owns | Does not own |
|---|---|---|
| `models/` | SQLAlchemy table mappings | API payloads, business logic |
| `schemas/` | Pydantic API/CRUD contracts | DB column definitions |
| `schemas_df/` | Pandera DataFrame contracts | Row-level ORM access |
| `crud/` | Reusable persistence queries | Session creation, request parsing |
| `db/` | Engine, sessions, declarative base | Domain queries |
| `api/routes/` | Request parsing, response wiring | Raw SQL, business decisions |
| `cli/` | Typer command surface | Heavy logic (delegate to `data/` or `crud/`) |
| `core/` | Config, logging, shared types, exceptions | Domain code |

Schema separation across `models/`, `schemas/`, `schemas_df/`: **VAL-2** (`VALIDATION.md`).

Only keep folders that exist in the project. If `ml/` or `viz/` is absent, do not invent it.

**Dependency direction** — lower layers must not import from higher layers:

```text
api/ (FastAPI routes)  |  cli/ (Typer commands)
  ->
data/ (workflows, ETL)
  ->
crud/ (reusable queries)
  ->
models/ (SQLAlchemy)  |  schemas/ (Pydantic)  |  schemas_df/ (Pandera)
  ->
core/ (config, logger, exceptions)  |  db/ (session, engine)
```

Infrastructure belongs in `core/` and `db/`; domain behavior does not live there. Production code lives in the package; exploration stays in `notebooks/WIP/` or `pyscripts/` (see REPO-3).

### REPO-3 Exploration stays out of the package [SHOULD]

- Prototypes and exploration live in `notebooks/WIP/` or `pyscripts/`.
- Productionized code moves into the package before reuse from `api/`, `cli/`, or `crud/`.
- Utility/CI scripts live in `scripts/`, not in the package.

### REPO-4 Tests mirror package layout [MUST]

- `tests/` mirrors `<package_name>/` one-to-one.
- Naming and layout: **TEST-12** (`TESTING.md`).
- New layer → matching test folder. Do not scatter tests into the package.

### REPO-5 Consult before creating a new top-level folder [MUST]

Before adding a folder that does not appear in the default map or the project's overrides, stop and confirm. A new top-level folder is a structural decision, not a placement decision — record it in a new ADR under `docs/adr/` and `docs/docs-guide.md` §3, not only in an implicit commit.

## Quick Placement Map

| Need | Goes in |
|---|---|
| Maps a Python class to a DB table | `models/` |
| Validates an HTTP payload | `schemas/` |
| Validates a DataFrame | `schemas_df/` |
| Reusable persistence read/write | `crud/` |
| Engine / session setup | `db/` |
| FastAPI route | `api/routes/` |
| Typer command | `cli/` |
| ETL transformation | `data/` |
| Domain exceptions | `core/exceptions.py` |
| Exploration not yet productionized | `notebooks/WIP/` or `pyscripts/` |
| Utility / CI script | `scripts/` |

### REPO-6 Nested AGENTS.md in monorepos [SHOULD]

In monorepos, place an additional `AGENTS.md` in a subpackage when that package needs different commands, boundaries, or layout than the repo root. The file closest to the edited path takes precedence. Subpackage files should reference root `AGENTS.md` for shared cycle and doc rules rather than duplicating them.

## Anti-patterns

- Raw SQL in routes or CLI commands.
- Opening a `Session` inside a CRUD function — see **PER-4** (`PERSISTENCE.md`).
- Importing from `api/` or `cli/` into `data/`, `crud/`, or `models/` (dependency direction is one-way — REPO-2).
- Creating a new top-level folder without recording the decision in `docs/adr/`.

## Project Overrides

Repository-specific deviations: `docs/docs-guide.md` §3 and this section. See **DOC-6** (`DOCUMENTATION.md`).

## See also

- [ARCHITECTURE](ARCHITECTURE.md)
- [DOCUMENTATION](DOCUMENTATION.md)
- [PERSISTENCE](PERSISTENCE.md)
- [CORE](CORE.md)
