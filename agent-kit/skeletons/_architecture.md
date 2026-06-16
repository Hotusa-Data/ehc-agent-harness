# Architecture Guide

Use this document for the **real** shape of a specific consumer repository: what the system does, how it deviates from the kit default, and project-specific invariants. The default codemap and placement rules live in [`agent-kit/agent-rules/repo-guide.md`](../agent-kit/agent-rules/repo-guide.md) — do **not** restate that tree here.

## Document Metadata

- Project:
- Owner:
- Last reviewed:
- Related context files:

## 1. System Overview

Describe the system in 3–6 sentences:

- what the system does
- main architectural style
- main runtime environment or deployment model
- core technology stack
- major constraints that shape the design

Suggested prompts:

- Is the system event-driven, request-response, batch, or hybrid?
- Is it deployed as services, jobs, notebooks, Lambdas, containers, or something else?
- Which technologies are structural rather than incidental?

## 2. Data Or Business Domains

List the major domains the codebase works with. If the project uses multiple databases, APIs, or bounded contexts, describe them here.

| Domain | Description | Main ownership | Read | Write | Notes |
|---|---|---|---|---|---|
|  |  |  | yes / no | yes / no |  |

Rules:

- Describe actual domains found in the code, not aspirational ones.
- If domain isolation matters, state the boundary rule explicitly.
- If a domain is external or read-only, say so.
- Vocabulary details belong in `docs/glossary.md`; persistence contracts in `docs/database.md`.

If a single domain covers the whole system, one row is enough.

## 3. Deviations From The Default Layout

The default top-level layout, package layers, dependency direction, and placement map are in [`agent-kit/agent-rules/repo-guide.md`](../agent-kit/agent-rules/repo-guide.md). Do **not** restate that tree here.

Use this section only to record:

- Folders or layers this project **adds** beyond the default (e.g. a custom `ingest/` subsystem, an extra `alembic_<schema>/`).
- Folders the default lists but this project **does not use** (and why).
- Layer responsibilities this project **renames or sharpens** (e.g. `crud/` here also owns cache invalidation).
- Multi-domain structure: several ORM bases, services, or bounded contexts — **name modules and folders** (symbol search finds them; avoid deep path links that go stale).

If the project matches the default exactly, write: "Matches `agent-rules/repo-guide.md` default layout."

## 4. Project-Specific Rules Of The Road

Generic placement, dependency direction, sessions at the edge, validation at boundaries, and exploration rules live in [`agent-kit/agent-rules/repo-guide.md`](../agent-kit/agent-rules/repo-guide.md), [`agent-kit/agent-rules/architecture.md`](../agent-kit/agent-rules/architecture.md), [`agent-kit/agent-rules/persistence.md`](../agent-kit/agent-rules/persistence.md), [`agent-kit/agent-rules/validation.md`](../agent-kit/agent-rules/validation.md), and [`agent-kit/agent-rules/security.md`](../agent-kit/agent-rules/security.md).

Use this section only for rules **specific to this project** — for example: "all writes to the `events` schema must go through `services/event_bus/`", or "no synchronous external HTTP calls inside request handlers".

Use short imperative statements. If there are no project-specific rules, write: "No deviations from default rules of the road."

## 5. Cross-Cutting And External Boundaries

Brief notes on integrations and transversal concerns that affect **where code may live** or **what must not cross a boundary**. Keep this section short; revisit a couple of times a year rather than syncing every PR.

| Integration or concern | Type | Direction | Boundary rule | Notes |
|---|---|---|---|---|
|  | API / queue / storage / auth / jobs / observability | inbound / outbound / both |  |  |

Cover only what matters for navigation and invariants: external APIs, queues, schedulers, auth entry points, deployment ordering that constrains module boundaries. Persistence schema detail → `docs/database.md`. Step-by-step runtime flows → `docs/features/<feature>/plan.md`.

If nothing applies, write: "No external integrations or cross-cutting notes beyond kit defaults."

## Optional: Runtime Flows

Add subsections here **only** when a flow is system-wide and does not belong in a single feature's `plan.md` (e.g. a global ingestion pipeline spanning several domains). For each flow: trigger, named modules, external touchpoints — not a full how-to.

If all flows are feature-scoped, write: "See feature plans under `docs/features/`."

## Authoring Rules

- Describe the repository as it really is today.
- If something is planned but not implemented, label it clearly.
- Prefer concrete module and folder names over abstract principles.
- Do not duplicate the default codemap from `repo-guide.md` unless this project overrides or sharpens it.
- Open decisions and deferred work → feature `plan.md`, CHANGELOG `Decided`, or `.local-context/` — not a standing table in this file.
