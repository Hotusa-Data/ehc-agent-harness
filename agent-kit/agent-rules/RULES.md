# Agent rules index

Engineering rules for the coding agent — extensions of root `AGENTS.md`, loaded just-in-time per [`DOCUMENTATION.md` §DOC-1](DOCUMENTATION.md).

**Do not load this file whole.** Use **Files and load triggers** and **Canonical topics** below to pick the one rule file that owns the current decision — then open that file only.

## Naming convention

| Layer | Location | Filename pattern | Examples |
|---|---|---|---|
| Agent map | repo root | `AGENTS.md` | Always loaded |
| Harness rules | `agent-kit/agent-rules/` | `SCREAMING_SNAKE.md` | `CORE.md`, `TESTING.md` |
| Project docs | `docs/`, feature folders | lowercase | `adr/`, `specs.md`, `changelog.md` |

`agent-kit/agent-rules/ARCHITECTURE.md` (kit layer contracts) ≠ `docs/adr/` (project structural decisions).

## Files and load triggers

| File | Load when | Rule prefix |
|---|---|---|
| `CORE.md` | Always (also from `AGENTS.md` bootstrap) | CORE-, COOP- |
| `DOCUMENTATION.md` | Reading, writing, or gating on `docs/` (DOC-1–DOC-10) | DOC- |
| `REPO_GUIDE.md` | Default codemap, placement, dependency direction | REPO- |
| `ARCHITECTURE.md` | Layer contracts, typed boundaries, circular imports | ARCH- |
| `PYTHON.md` | Python code | PY- |
| `PERSISTENCE.md` | ORM, queries, migrations, sessions | PER- |
| `TESTING.md` | Tests and verification strategy | TEST- |
| `VALIDATION.md` | Input checks, contracts, failure handling | VAL- |
| `SECURITY.md` | Auth, secrets, trust boundaries | SEC- |
| `OBSERVABILITY.md` | Logs, metrics, tracing | OBS- |

Ambiguity and stop-to-clarify: **COOP-1**, **COOP-2** (`CORE.md`). Project overrides: `docs/docs-guide.md` §3 and `## Project Overrides` in each rule file.

When several files touch the same topic, load only the **Primary rule** from the table below — not every cross-reference.

## Canonical topics (load the owner, not every file)

| Topic | Primary rule | File |
|---|---|---|
| Typed shapes at layer boundaries | ARCH-1 | ARCHITECTURE.md |
| Schema trinity (models / schemas / schemas_df) | VAL-2 | VALIDATION.md |
| Session scope and commits | PER-4, PER-5 | PERSISTENCE.md |
| Settings and credentials | VAL-11 | VALIDATION.md |
| PII and secrets in logs | SEC-6 | SECURITY.md |
| Test file naming and layout | TEST-12 | TESTING.md |
| CLI human output vs logging | OBS-11 | OBSERVABILITY.md |
| Reproducible dependencies (uv.lock) | PY-7 | PYTHON.md |
| Doc load order and gates | DOC-1, DOC-2 | DOCUMENTATION.md |
| Structural decisions (ADRs) | DOC-10 | DOCUMENTATION.md + `docs/adr/changelog.md` |

## Rule ID index

| ID | Summary | File |
|---|---|---|
| ARCH-1 | Cross boundaries with typed shapes | ARCHITECTURE.md |
| ARCH-2 | Fix circular imports at design level | ARCHITECTURE.md |
| ARCH-3 | Avoid generic dumping grounds | ARCHITECTURE.md |
| COOP-1 | Stop when ambiguity can change outcome | CORE.md |
| COOP-2 | Surface assumptions when proceeding | CORE.md |
| COOP-3 | Distinguish ran from written | CORE.md |
| CORE-1 | Prefer correctness over cleverness | CORE.md |
| CORE-2 | Make boundary contracts explicit | CORE.md |
| CORE-3 | Keep changes small and reviewable | CORE.md |
| CORE-4 | Specify before building | CORE.md |
| CORE-5 | Back claims with evidence | CORE.md |
| CORE-6 | Name lightweight shortcuts explicitly | CORE.md |
| CORE-7 | Prefer shared utilities over one-off helpers | CORE.md |
| CORE-8 | Promote repeated violations to durable rules | CORE.md |
| DOC-1 | Load just-in-time | DOCUMENTATION.md |
| DOC-2 | Validation gates before broad implementation | DOCUMENTATION.md |
| DOC-3 | Update in place; create when distinct | DOCUMENTATION.md |
| DOC-4 | Instantiate from skeletons | DOCUMENTATION.md |
| DOC-5 | docs-guide.md is project authority | DOCUMENTATION.md |
| DOC-6 | Overrides must not silently contradict | DOCUMENTATION.md |
| DOC-7 | Feature changelog convention | DOCUMENTATION.md |
| DOC-8 | Reconcile docs with diff; session/PR close checklist | DOCUMENTATION.md |
| DOC-10 | Architecture decisions in docs/adr/ | DOCUMENTATION.md |
| OBS-1 | Prefer structured logging | OBSERVABILITY.md |
| OBS-2 | One logger per module (Loguru) | OBSERVABILITY.md |
| OBS-3 | Choose log levels deliberately | OBSERVABILITY.md |
| OBS-4 | Log enough safe context | OBSERVABILITY.md |
| OBS-5 | Never log secrets or PII (see SEC-6) | OBSERVABILITY.md |
| OBS-6 | Log workflow boundaries | OBSERVABILITY.md |
| OBS-7 | Surface validation failures in aggregate | OBSERVABILITY.md |
| OBS-8 | Preserve exception context | OBSERVABILITY.md |
| OBS-9 | Use metrics when logs are wrong tool | OBSERVABILITY.md |
| OBS-10 | Loguru bind/contextualize | OBSERVABILITY.md |
| OBS-11 | rich for CLI human output | OBSERVABILITY.md |
| PER-1 | ORM models focused on mapping (see VAL-2) | PERSISTENCE.md |
| PER-2 | Required columns explicit | PERSISTENCE.md |
| PER-3 | Index filter/join paths | PERSISTENCE.md |
| PER-4 | Open sessions at the edge | PERSISTENCE.md |
| PER-5 | Commit ownership explicit | PERSISTENCE.md |
| PER-6 | Reusable queries in CRUD | PERSISTENCE.md |
| PER-7 | Schema change needs migration | PERSISTENCE.md |
| PER-8 | Review autogenerated migrations | PERSISTENCE.md |
| PER-9 | Load relationships explicitly | PERSISTENCE.md |
| PER-10 | Holy trinity when adding a table | PERSISTENCE.md |
| PER-11 | CRUD inherits CRUDBase | PERSISTENCE.md |
| PER-12 | SQLite for local only | PERSISTENCE.md |
| PY-1 | Avoid Any unless unavoidable | PYTHON.md |
| PY-2 | Side effects at edges | PYTHON.md |
| PY-3 | Pick containers deliberately (see ARCH-1) | PYTHON.md |
| PY-4 | Avoid chained pandas assignment | PYTHON.md |
| PY-5 | DataFrame grain and shape obvious | PYTHON.md |
| PY-6 | Pandas conventions | PYTHON.md |
| PY-7 | uv and pre-commit workflow | PYTHON.md |
| PY-8 | Modern type syntax | PYTHON.md |
| PY-9 | Ruff, ty, deptry | PYTHON.md |
| PY-10 | Google docstrings | PYTHON.md |
| PY-11 | License headers | PYTHON.md |
| PY-12 | Visualization conventions | PYTHON.md |
| PY-13 | FastAPI routes (sessions: PER-4) | PYTHON.md |
| PY-14 | Typer CLI (output: OBS-11) | PYTHON.md |
| PY-15 | Exception hierarchy | PYTHON.md |
| PY-16 | Async/sync in FastAPI | PYTHON.md |
| REPO-1 | Feature folders are unit of scope | REPO_GUIDE.md |
| REPO-2 | Package layers and dependency direction | REPO_GUIDE.md |
| REPO-3 | Exploration stays out of package | REPO_GUIDE.md |
| REPO-4 | Tests mirror layout (see TEST-12) | REPO_GUIDE.md |
| REPO-5 | Consult before new top-level folder | REPO_GUIDE.md |
| REPO-6 | Nested AGENTS.md in monorepos | REPO_GUIDE.md |
| SEC-1 | Never commit secrets (settings: VAL-11) | SECURITY.md |
| SEC-2 | Never build SQL from untrusted strings | SECURITY.md |
| SEC-3 | Never shell=True with untrusted input | SECURITY.md |
| SEC-4 | Name, isolate, minimize PII | SECURITY.md |
| SEC-5 | Validate and bound external input | SECURITY.md |
| SEC-6 | Never log secrets or PII | SECURITY.md |
| SEC-7 | Treat third-party data as untrusted | SECURITY.md |
| SEC-8 | Reproducible deps (see PY-7) | SECURITY.md |
| SEC-9 | Permissive licenses only | SECURITY.md |
| SEC-10 | Prefer least privilege | SECURITY.md |
| SEC-11 | Keep notebook outputs safe | SECURITY.md |
| TEST-1 | Test behavior not implementation | TESTING.md |
| TEST-2 | Unit tests deterministic | TESTING.md |
| TEST-3 | Fixtures minimal | TESTING.md |
| TEST-4 | Real persistence boundary | TESTING.md |
| TEST-5 | Mock at boundary | TESTING.md |
| TEST-6 | Inject time | TESTING.md |
| TEST-7 | Transformation edge cases | TESTING.md |
| TEST-8 | Pipeline stages independently | TESTING.md |
| TEST-9 | Idempotency where writes repeat | TESTING.md |
| TEST-10 | Evidence without formal test explicit | TESTING.md |
| TEST-11 | FastAPI via TestClient | TESTING.md |
| TEST-12 | Test file naming and layout | TESTING.md |
| VAL-1 | Validate at boundaries | VALIDATION.md |
| VAL-2 | Separate ORM, object, DataFrame schemas | VALIDATION.md |
| VAL-3 | Separate create/update/response models | VALIDATION.md |
| VAL-4 | Validators pure | VALIDATION.md |
| VAL-5 | ORM-to-schema support deliberate | VALIDATION.md |
| VAL-6 | DataFrame schemas reusable | VALIDATION.md |
| VAL-7 | Coercion only when intentional | VALIDATION.md |
| VAL-8 | Validate before major transform/persist | VALIDATION.md |
| VAL-9 | DataFrame validation where it catches bugs | VALIDATION.md |
| VAL-10 | Pydantic v2 idioms | VALIDATION.md |
| VAL-11 | Settings via BaseSettings | VALIDATION.md |
