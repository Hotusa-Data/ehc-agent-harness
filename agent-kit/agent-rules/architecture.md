---
triggers: [architecture, module, package, layer, structure, placement, abstraction, dependency]
requires: [core]
see-also: [python, persistence, validation]
severity-default: MUST
---

# Architecture And Modularization

Rules for dependency direction, abstraction boundaries, and layer responsibilities.

Load when: designing a new module, deciding where code belongs, introducing a new layer, or resolving structural drift.

Framework-specific conventions (FastAPI routes, Typer CLI) live in [python](python.md) PY-13/PY-14.

## Rules

### ARCH-1 Keep dependencies flowing downward [MUST]

Use a clear dependency direction (matches the template layout):

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

A lower layer must not import from a higher layer. Infrastructure belongs in `core/`; domain behavior does not. `notebooks/WIP/` is for exploration only — production code lives in the package.

### ARCH-2 Cross boundaries with typed shapes [MUST]

When one layer hands results to another, use a schema or explicit return type. Do not pass raw `dict` objects or untyped tuples across public or layer boundaries.

```python
# good
def get_headlines(db: Session, *, limit: int) -> list[HeadlineSchema]: ...

# bad
def get_headlines(db, limit=100) -> dict: ...
```

Local dictionaries may exist inside small private functions when the shape does not escape that function.

### ARCH-3 Fix circular imports at the design level [MUST]

If two modules import from each other, one of them owns the wrong responsibility. Fix placement instead of hiding the problem with delayed imports or string annotations.

### ARCH-4 Avoid generic dumping grounds [SHOULD]

Do not create `utils.py`, `helpers.py`, or `common.py` as catch-all buckets. If code has a real responsibility, give it a real home.

## Anti-patterns

- Domain logic inside ORM models because "the data is already there".
- Returning bare `dict` values across layer boundaries.
- Delayed imports instead of fixing module ownership.
- Introducing base classes or abstraction layers on the first repetition.
- Creating folders or modules before the boundary is actually needed.
- Importing from `api/` or `cli/` into `data/`, `crud/`, or `models/` (dependency direction is one-way).

## Project Overrides

Use this section for project-specific placement rules such as approved layer names, allowed adapter patterns, or repository-specific folder conventions.

## See also

- [core](core.md)
- [python](python.md)
- [persistence](persistence.md)
- [validation](validation.md)
