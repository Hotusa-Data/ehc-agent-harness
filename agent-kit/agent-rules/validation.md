---
triggers: [pydantic, pandera, schema, validate, BaseModel, DataFrameModel, contract]
requires: [core]
see-also: [architecture, persistence]
severity-default: MUST
---

# Validation

Rules for where validation belongs and how to separate schema responsibilities.

Load when: defining or changing schemas, or designing a contract between layers or stages.

## Rules

### VAL-1 Validate at boundaries, not deep inside [MUST]

Validate where data crosses trust, ownership, persistence, or stage boundaries. Do not repeatedly validate data that is already proven correct inside the same trusted scope.

### VAL-2 Separate ORM, object, and DataFrame schemas [MUST]

Three tools, three folders:

- `models/` — SQLAlchemy ORM (table mapping only).
- `schemas/` — Pydantic v2 (API payloads, CRUD inputs).
- `schemas_df/` — Pandera (DataFrame column contracts).

Do not blur them. A single feature typically touches all three.

### VAL-3 Separate create, update, and response models [SHOULD]

Use distinct schemas when those roles have different requirements. Avoid one catch-all model that silently weakens the contract.

### VAL-4 Keep validators pure [MUST]

Validation functions should not call databases, filesystems, or remote services. IO-based checks belong in service logic.

### VAL-5 Use ORM-to-schema support deliberately [SHOULD]

When building response models from ORM objects, configure the schema layer so conversion is explicit and repeatable.

### VAL-6 Keep DataFrame schemas reusable [SHOULD]

If DataFrame validation matters, define schemas in reusable modules rather than inline inside transformations.

### VAL-7 Use coercion only when conversion is intentional [SHOULD]

If a schema coerces values, the conversion must be expected, documented, and covered by evidence that invalid values still fail clearly.

### VAL-8 Validate before major transformation or persistence [MUST]

Do not perform substantial work on untrusted tabular or object data and only validate afterwards. Canonical anchor points:

- DataFrame producers: `@pa.check_output(SomeDFSchema.to_schema())` on the function returning the DataFrame.
- FastAPI routes: declare `response_model=...` (or typed return) so payload is validated and documented.
- CRUD writes: pass Pydantic schema instances, not raw dicts.

### VAL-9 Use DataFrame validation where it catches real bugs [SHOULD]

Use stronger tabular contracts when downstream logic depends on stable columns, types, nullability, or stage handoffs.

### VAL-10 Pydantic v2 idioms [MUST]

- Use `field_validator` for single-field rules; `model_validator` for cross-field rules. Do not put cross-field logic inside `field_validator`.
- Use `Field(..., description=...)` on non-trivial fields — feeds OpenAPI docs and review.
- For schemas built from ORM objects, configure with `model_config = ConfigDict(from_attributes=True)`. Do not access ORM internals manually.
- Use `model_dump()` / `model_dump_json()`. The v1 `.dict()` / `.json()` are deprecated.

### VAL-11 Settings via BaseSettings [MUST]

Application config lives in `core/config/` as a `pydantic-settings.BaseSettings` subclass (or a project wrapper around it) with a package `ENV_PREFIX`. Assemble derived values (DSNs, paths) via `@field_validator(..., mode="before"|"after")`, not in business code. Never read `os.environ` directly outside `core/config/`. Credentials load from `.env` (gitignored) and `.env.ci` (test fixtures only — no real secrets).

## Anti-patterns

- Reusing one schema for create, update, and response.
- Performing IO inside validators.
- Defining tabular schemas inline where they cannot be reused.
- Turning on coercion just to make a failing schema pass.
- Calling data "internal" after it crossed a file, API, database, or stage boundary.

## Project Overrides

Use this section for project-specific schema libraries, folder conventions, coercion policy, or mandatory validation gates.

## See also

- [architecture](architecture.md)
- [persistence](persistence.md)
