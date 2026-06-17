---
triggers: [architecture, module, package, layer, abstraction, dependency, boundary, contract]
requires: [CORE]
see-also: [REPO_GUIDE, PYTHON, PERSISTENCE, VALIDATION]
---

# Architecture And Modularization

**Kit layer contracts** — typed shapes, circular-import fixes, abstraction discipline. Project structural decisions live in `docs/adr/` (see **DOC-10**). Default codemap and dependency direction: [REPO_GUIDE](REPO_GUIDE.md) REPO-2.
Load when: defining contracts between layers, fixing circular imports, introducing abstractions, or resolving structural drift that is not answered by the default layout alone.

Framework-specific conventions (FastAPI routes, Typer CLI) live in [PYTHON](PYTHON.md) PY-13/PY-14.

## Rules

### ARCH-1 Cross boundaries with typed shapes [MUST]

When one layer hands results to another, use a schema or explicit return type. Do not pass raw `dict` objects or untyped tuples across public or layer boundaries.

```python
# good
def get_headlines(db: Session, *, limit: int) -> list[HeadlineSchema]: ...

# bad
def get_headlines(db, limit=100) -> dict: ...
```

Local dictionaries may exist inside small private functions when the shape does not escape that function.

### ARCH-2 Fix circular imports at the design level [MUST]

If two modules import from each other, one of them owns the wrong responsibility. Fix placement per [REPO_GUIDE](REPO_GUIDE.md) instead of hiding the problem with delayed imports or string annotations.

### ARCH-3 Avoid generic dumping grounds [SHOULD]

Do not create `utils.py`, `helpers.py`, or `common.py` as catch-all buckets. If code has a real responsibility, give it a real home per [REPO_GUIDE](REPO_GUIDE.md). See **CORE-7** (`CORE.md`).

## Anti-patterns

- Returning bare `dict` values across layer boundaries (see ARCH-1).
- Delayed imports instead of fixing module ownership (see ARCH-2).
- Introducing base classes or abstraction layers on the first repetition.
- Creating folders or modules before the boundary is actually needed.
- Business logic inside ORM models — see **PER-1** (`PERSISTENCE.md`).

## Project Overrides

Project-specific layer contracts: `docs/docs-guide.md` §3 and this section. Layout deltas: `docs/adr/`. See **DOC-6**, **DOC-10** (`DOCUMENTATION.md`).

## See also

- [REPO_GUIDE](REPO_GUIDE.md)
- [CORE](CORE.md)
- [PYTHON](PYTHON.md)
- [PERSISTENCE](PERSISTENCE.md)
- [VALIDATION](VALIDATION.md)
