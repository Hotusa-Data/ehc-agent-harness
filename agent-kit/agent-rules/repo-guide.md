---
triggers: [placement, structure, new-file, new-folder]
requires: [core]
see-also: [architecture, documentation]
severity-default: SHOULD
---

# Repository Layout And Placement

How code is organized in a consumer repo and where new code belongs. Complements `architecture.md` (dependency direction and abstraction boundaries) — this file is strictly about **placement**: which folder, which layer, which file gets the new code.

Load when: about to create a new file or folder, deciding which layer owns a change, or reviewing placement of existing code.

Unlike a project-instantiated doc, this rule encodes the **default layout** the agent-kit assumes (Python data-project template). Project-specific deviations belong in `docs/docs-guide.md` §3 "Project-Specific Overrides".

## Default Top-Level Map

```text
repo-root/
|-- docs/
|   |-- context/
|   |-- features/
|   |-- architecture.md
|   |-- database.md
|   |-- glossary.md
|   `-- docs-guide.md
|-- notebooks/
|-- scripts/
|-- tests/
|-- <package_name>/
|-- pyproject.toml
`-- Makefile
```

If the real repo deviates, override in `docs/docs-guide.md` §3 and link from there.

## Rules

### REPO-1 Feature folders are the unit of scope [MUST]

Each feature lives in `docs/features/<feature>/` with:

| File | Purpose |
|---|---|
| `requirements.md` | What and why |
| `design.md` | How |
| `tasks.md` | Atomic, ordered work units |
| `report.md` | What was actually built (created at cycle close) |
| `CHANGELOG.md` | Narrative of evolution |

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

Only keep folders that exist in the project. If `ml/` or `viz/` is absent, do not invent it.

### REPO-3 Exploration stays out of the package [SHOULD]

- Prototypes and exploration live in `notebooks/WIP/` or `pyscripts/`.
- Productionized code moves into the package before reuse from `api/`, `cli/`, or `crud/`.
- Utility/CI scripts live in `scripts/`, not in the package.

### REPO-4 Tests mirror package layout [MUST]

- `tests/` mirrors `<package_name>/` one-to-one.
- Test files named `test_<pkg>_<path>_<mod>.py`.
- New layer → matching test folder. Do not scatter tests into the package.

### REPO-5 Consult before creating a new top-level folder [MUST]

Before adding a folder that does not appear in the default map or the project's overrides, stop and confirm. A new top-level folder is a structural decision, not a placement decision — it belongs in `architecture.md` and the project's overrides, not in an implicit commit.

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

## Anti-patterns

- Raw SQL in routes or CLI commands.
- Opening a `Session` inside a CRUD function (see [persistence](persistence.md) PER-4).
- Importing from `api/` or `cli/` into `data/`, `crud/`, or `models/` (dependency direction is one-way).
- Creating a new top-level folder without recording the decision in `architecture.md`.

## Project Overrides

Repository-specific deviations belong in `docs/docs-guide.md` §3. State each override explicitly so the agent can detect it.

## See also

- [architecture](architecture.md)
- [documentation](documentation.md)
- [persistence](persistence.md)
- [core](core.md)
