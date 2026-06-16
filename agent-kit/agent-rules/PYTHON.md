---
triggers: [python, .py, function, class, import, type hint, pandas, dataclass, pydantic, fastapi, typer]
requires: [CORE]
see-also: [ARCHITECTURE, VALIDATION, TESTING]
---

# Python Conventions

Python-specific rules for typing, side effects, containers, pandas usage, framework conventions, error handling, and async discipline.

Load when: writing or reviewing Python code.

## Rules

### PY-1 Avoid `Any` unless it is truly unavoidable [SHOULD]

Use `Any` only when crossing into an untyped third-party boundary that cannot be modeled cleanly. Do not use it to silence uncertainty.

### PY-2 Keep side effects at the edges [MUST]

IO, database writes, logging, and network calls should live at workflow edges, not inside transformation helpers.

### PY-3 Pick containers deliberately [MUST]

Use **Pydantic v2** models for boundary crossing (API, CRUD inputs), `dataclass` for simple internal immutable structures, and **Pandera** schemas when DataFrame column contracts matter. Do not pass raw `dict` across meaningful boundaries — see **ARCH-1** (`ARCHITECTURE.md`). Use `obj.model_dump()` (Pydantic v2), not the deprecated `.dict()`.

### PY-4 Avoid chained pandas assignment [MUST]

Use `.loc` or an explicit `.copy()` when mutating DataFrame slices. Do not rely on view-vs-copy behavior.

### PY-5 Make DataFrame grain and shape obvious [SHOULD]

When returning a DataFrame, document the expected grain and prefer explicit column selection over positional behavior.

### PY-6 Pandas conventions [SHOULD]

Treat DataFrames like SQL tables: by columns, not by position. Ruff `PD` rules enforce most of this.

- `_df` suffix for named DataFrames; never `df` alone [SHOULD].
- Never `inplace=True`. Reassign instead [MUST].
- Never rely on row index identity. Use `.loc[...]` or `.query(...)` to filter; avoid `.iloc` outside genuinely positional cases [MUST].
- Single column: `df["col"]`. Multiple columns: `df.loc[:, ["a", "b"]]`. No dot access [MUST].
- Mutate columns via `.assign(...)`, not direct `df["new"] = ...` inside transformations [SHOULD].
- Chain operations top-to-bottom; avoid intermediate `*_tmp_df` variables [SHOULD].
- `merge()` over `join()` when keys matter [SHOULD]. `groupby(..., as_index=False)` to keep grouped columns as columns [SHOULD].
- Vectorized first, then `Series.map`. `apply` only when neither fits; `iterrows` only when the output is not a DataFrame [SHOULD].
- Persist with `to_csv` (human-readable) or `to_parquet` (round-trip). Always `index=False` unless the index carries meaning [MUST].

### PY-7 Dependency and pre-commit workflow [MUST]

Use **uv** for dependency management (`uv add <pkg>`, `uv add --dev <pkg>`, `uv sync`, `uv run <cmd>`). Commit `uv.lock`. Use **prek** for pre-commit hooks (`uv run prek install --install-hooks`). Do not bypass hooks; if one fails, fix the underlying issue. Reproducible resolution also applies to **SEC-8** (`SECURITY.md`).

### PY-8 Modern type syntax [MUST]

Use the syntax available in the project's `requires-python` (template targets Python 3.14):

- `list[X]`, `dict[K, V]`, `tuple[X, ...]` instead of `List`, `Dict`, `Tuple` from `typing` (PEP 585).
- `X | None` instead of `Optional[X]`; `X | Y` instead of `Union[X, Y]` (PEP 604).

Only import from `typing` what has no builtin form (`Annotated`, `TypeVar`, `Protocol`, `Generic`, etc.).

### PY-9 Linting and typechecking [MUST]

- Lint and format with **Ruff**. The template enables (among others) `ANN`, `D`, `PD`, `UP`, `N`, `TRY`, `SIM`, `RET`, `PTH`. Do not silence rules locally without a comment explaining why.
- Typecheck with **`ty`** (Astral), not mypy. Resolve typing issues; do not paper over them with `# type: ignore`.
- Audit dependencies with **deptry**: every imported package must be declared; unused declared deps must be removed or whitelisted in `[tool.deptry.per_rule_ignores]` with reason.

### PY-10 Docstrings: Google style, never empty [MUST]

- Every module: header docstring describing purpose. No authorship, email, or date metadata.
- Every public function, method, and class: Google-style docstring (one-liner summary, then `Args:` / `Returns:` / `Raises:` when applicable). Document **all** arguments or none — partial lists are not allowed.
- Empty placeholders like `"""."""` are forbidden.

### PY-11 License headers on Python and bash files [MUST]

Every `.py` and `.sh` file carries the project license header from `.license.tmpl`. New files: run `make license-headers` before committing; `make license-check` verifies.

### PY-12 Visualization conventions [MUST]

- Use **Altair** or **Seaborn** for plots. Prefer them over raw matplotlib [SHOULD].
- Apply the project theme via the `viz/` subpackage — never style chart-by-chart [MUST].
- Labels, ticks, titles use the project language (not always English) and human-readable terms — no underscores in axis labels, include units [MUST].
- Naming: lowercase + underscores for variables; PascalCase for classes; UPPER_CASE for module constants — Ruff `N` enforces.

### PY-13 FastAPI route conventions [MUST]

- One file per feature under `api/routes/<feature>.py`. Create the router with `APIRouter(prefix="/<feature>", tags=["<Area>"])` and include it from `api/main.py` with `api_router.include_router(...)`.
- Every endpoint declares its response shape via `response_model=...` or a typed return annotation. Do not return raw ORM objects or `dict`.
- Inject dependencies with `Depends(...)` (DB session, settings, current user). Session scope: **PER-4** (`PERSISTENCE.md`).
- Raise `HTTPException` for HTTP-shaped failures at the route boundary. Inner layers raise domain exceptions (see PY-15); the route translates them.
- Status codes: `200` success, `201` created, `404` not found, `409` conflict, `422` validation error (Pydantic handles automatically), `500` unexpected failure. Never return `200` when the resource was not found.

### PY-14 Typer CLI conventions [MUST]

- Each command group lives in `cli/<group>.py` with `app = Typer(no_args_is_help=True)` and `@app.command()` functions.
- Compose groups in `cli/__init__.py` with `app.add_typer(subapp, name="<group>", help="...")`.
- Underscores in parameter names become dashes on the CLI (`file_name` → `--file-name`); keep Python names snake_case.
- Defaults that depend on runtime (timestamps, paths) belong in the function signature, not computed inside.
- Human-facing CLI output: **OBS-11** (`OBSERVABILITY.md`). Logs stay in Loguru.

### PY-15 Exception hierarchy and propagation [MUST]

Define domain exceptions in `core/exceptions.py`. Use a base `DomainError` and named subclasses per failure kind (`NotFoundError`, `ConflictError`, `ValidationError`). Never catch generic `Exception` to silence failures without logging and re-raising.

Use `raise X from Y` when translating exceptions across layer boundaries so the original cause is preserved. The API/CLI layer is responsible for converting domain exceptions to user-facing signals; inner layers must not import from `api/` or `cli/`.

```python
# core/exceptions.py
class DomainError(Exception): ...
class NotFoundError(DomainError): ...
class ConflictError(DomainError): ...

# api/routes/items.py — the route translates
@router.get("/{item_id}")
def read_item(item_id: int, db: Session = Depends(get_db)) -> ItemSchema:
    try:
        return crud.item.get_or_raise(db, item_id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
```

### PY-16 Async/sync discipline in FastAPI [MUST]

FastAPI routes can be `async def` or plain `def`. Choose deliberately:

- Plain `def` routes run in a thread pool automatically and are safe with synchronous SQLAlchemy sessions. This is the default for this stack.
- `async def` routes run on the event loop. Using synchronous SQLAlchemy inside an `async def` route **blocks the event loop** — do not do this.
- If the project adopts async database access, use `AsyncSession` consistently from the start. Do not mix sync and async sessions in the same application.
- Never perform blocking I/O (DB calls, file reads, `requests.get`) inside an `async def` handler without offloading via `asyncio.to_thread` or `run_in_executor`.

## Anti-patterns

- Using `Any` because the real type is inconvenient.
- Mixing IO and transformation logic in the same helper.
- Passing raw `dict` between layers instead of typed objects.
- Mutating DataFrame slices without `.loc` or `.copy()`.
- Writing empty or tautological docstrings.
- Saving DataFrames with meaningless default indexes.
- Catching `Exception` silently to avoid dealing with specific error types.
- Using `async def` with a synchronous SQLAlchemy session — blocks the event loop.
- Raising `HTTPException` inside a CRUD or service function — that is the route's responsibility.

## Project Overrides

Project-specific Python style: `docs/docs-guide.md` §3 and this section. See **DOC-6** (`DOCUMENTATION.md`).

## See also

- [ARCHITECTURE](ARCHITECTURE.md)
- [VALIDATION](VALIDATION.md)
- [TESTING](TESTING.md)
