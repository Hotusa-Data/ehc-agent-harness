# Database Guide

Use this document to describe the real persistence layer of a consumer repository after inspecting its codebase. This file is for actual database architecture, not generic ORM advice — the generic rules live in [`agent-kit/agent-rules/persistence.md`](../agent-kit/agent-rules/persistence.md).

## Document Metadata

- Project:
- Owner:
- Last reviewed:
- Related context files:

## 1. Persistence Overview

Summarize the persistence setup:

- how many databases or data stores exist
- which libraries manage access
- which stores are owned by the repository versus external
- whether migrations exist and where
- how object and DataFrame validation fit into the stack

Write what is implemented now. If something is absent, say so explicitly.

## 2. Databases, Schemas, And Domains

Document each database or logical store separately.

| Domain / store | Engine | Purpose | Read | Write | Migrated here? | Notes |
|---|---|---|---|---|---|---|
|  |  |  | yes / no | yes / no | yes / no |  |

For each store, capture:

- connection type
- ownership boundary
- schema conventions
- whether tables are managed here or reflected from elsewhere

## 3. Connection And Session Management

Describe:

- where engines are created
- where sessions or factories live
- how callers are expected to open and close them
- any startup assumptions or failure behavior if config is missing

Include one short usage example if the project has a clear standard pattern.

## 4. ORM Model Conventions

Default conventions follow [`agent-kit/agent-rules/persistence.md`](../agent-kit/agent-rules/persistence.md) PER-10/11. Document only what this project overrides, adds, or deviates from.

- Base class and inheritance pattern:
- Primary key convention:
- Foreign key and cascade behavior:
- Timestamp conventions:
- Required / nullable policy:
- Index strategy:
- Multi-ORM-base setup (if any) and why:

If the project follows the defaults exactly, write: "Follows `persistence.md` defaults."

## 5. Migration Workflow

Default tool: **Alembic** per [`agent-kit/agent-rules/persistence.md`](../agent-kit/agent-rules/persistence.md) PER-7/8. Document only project-specific notes:

- migration folder(s) and any multi-schema split:
- known deviations from standard Alembic workflow:
- any stores that are intentionally not migrated here (and why):
- review expectations before merging a migration:

If the project follows the defaults exactly, write: "Standard Alembic workflow per `persistence.md`."

## 6. CRUD And Query Layer

Default pattern: `CRUDBase[Model, PydanticSchema, PanderaDFSchema]` per [`agent-kit/agent-rules/persistence.md`](../agent-kit/agent-rules/persistence.md) PER-11. Document only project-specific notes:

- any custom methods added to the base class:
- tables or domains that do not use `CRUDBase` and why:
- known query patterns or N+1 risks specific to this project:
- bulk-write conventions (if different from `create_multi`):

If the project follows the defaults exactly, write: "Standard `CRUDBase` pattern per `persistence.md`."

## 7. DataFrame Access And Validation

Default convention: Pandera schemas in `schemas_df/`, `CRUDBase.get_df()` with `@check_output` per [`agent-kit/agent-rules/validation.md`](../agent-kit/agent-rules/validation.md). Document only project-specific notes:

- schemas that use custom validation logic or non-standard Pandera features:
- tables or domains where DataFrame access is intentionally absent:
- known gaps or planned improvements:

If the project follows the defaults exactly, write: "Standard Pandera / `get_df()` pattern per `validation.md`."

## 8. Configuration, Credentials, And Security

Default convention: Pydantic `BaseSettings` with a package-level `ENV_PREFIX`, DSN assembled via `@field_validator`, credentials from `.env` (gitignored). Credentials are never read from `os.environ` in business code and never logged. See [`agent-kit/agent-rules/security.md`](../agent-kit/agent-rules/security.md) SEC-1.

Document only project-specific notes:

- env prefix used:
- local vs CI vs production credential sources:
- any approved deviations from the default settings pattern:

Never include real credentials.

## 9. Naming, Time, And Performance Conventions

Capture the persistence conventions contributors need to preserve:

- table and column naming
- timestamp and timezone expectations
- index strategy
- query style expectations
- known hot paths or N+1 risks
- pagination or batching patterns

Only document conventions that are visible in the code or explicitly agreed.

## 10. Backups, Recovery, And Operational Boundaries

Document what the repository knows about:

- backups
- restore ownership
- operational runbooks
- what is handled by infrastructure versus application code

If this is out of scope for the repo, say so explicitly.

## 11. Rules Of The Road

List the non-negotiable persistence rules contributors must follow in this project specifically. Do not restate generic rules from `persistence.md` — only project-specific ones.

Examples:

- only one domain is migrated here
- all new models must be imported into a package `__init__`
- sessions open at the edge and are passed inward
- credentials never live in the repo
- typed validation happens before writes

## 12. Open Decisions And Pending Improvements

List unresolved persistence decisions or technical debt discovered during inspection.

| ID | Area | Current state | Why it matters | Suggested next step |
|---|---|---|---|---|
| D1 |  |  |  |  |

## Authoring Rules

- This document describes the observed state of the codebase.
- Mark missing or not-yet-implemented pieces explicitly.
- Link to concrete file areas when helpful.
- Do not present speculation as architecture.
- Do not restate default patterns from `persistence.md` or `validation.md` — record only deviations and project-specific decisions.
