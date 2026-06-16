---
triggers: [architecture, module, package, layer, abstraction, dependency, boundary, contract]
requires: [core]
see-also: [repo-guide, python, persistence, validation]
severity-default: MUST
---

# Architecture And Modularization

Rules for **layer contracts**: typed shapes across boundaries, circular-import fixes, and abstraction discipline. The default codemap and dependency direction live in [repo-guide](repo-guide.md) REPO-2 — load that file for placement questions.

Load when: defining contracts between layers, fixing circular imports, introducing abstractions, or resolving structural drift that is not answered by the default layout alone.

Framework-specific conventions (FastAPI routes, Typer CLI) live in [python](python.md) PY-13/PY-14.

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

If two modules import from each other, one of them owns the wrong responsibility. Fix placement per [repo-guide](repo-guide.md) instead of hiding the problem with delayed imports or string annotations.

### ARCH-3 Avoid generic dumping grounds [SHOULD]

Do not create `utils.py`, `helpers.py`, or `common.py` as catch-all buckets. If code has a real responsibility, give it a real home per [repo-guide](repo-guide.md).

## Anti-patterns

- Returning bare `dict` values across layer boundaries (see ARCH-1).
- Delayed imports instead of fixing module ownership (see ARCH-2).
- Introducing base classes or abstraction layers on the first repetition.
- Creating folders or modules before the boundary is actually needed.
- Business logic inside ORM models — see [persistence](persistence.md) PER-1.

## Project Overrides

Use this section for project-specific layer contracts such as approved adapter patterns, forbidden cross-layer calls, or repository-specific boundary rules. Layout deltas belong in `docs/architecture.md` §3 and `docs/docs-guide.md` §3.

## See also

- [repo-guide](repo-guide.md)
- [core](core.md)
- [python](python.md)
- [persistence](persistence.md)
- [validation](validation.md)
