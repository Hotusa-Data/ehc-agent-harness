# Architecture Guide

Use this document to explain how a specific consumer repository is structured and where new code should live. Unlike `agent-kit/agent-rules/repo-guide.md`, which encodes the default placement rules of the kit, this file describes the **real** architecture of the project after inspecting its codebase.

## Document Metadata

- Project:
- Owner:
- Last reviewed:
- Related context files:

## 1. System Overview

Describe the system in 3-6 sentences:

- what the system does
- main architectural style
- main runtime environment or deployment model
- core technology stack
- major constraints that shape the design

Suggested prompts while filling this section:

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

## 3. Deviations From The Default Layout

The default top-level layout, package layers, and their responsibilities are defined in [`agent-kit/agent-rules/repo-guide.md`](../agent-kit/agent-rules/repo-guide.md). Do **not** restate that tree here.

Use this section only to record:

- Folders or layers this project **adds** beyond the default (e.g. a custom `ingest/` subsystem, an extra `alembic_<schema>/`).
- Folders the default lists but this project **does not use** (and why).
- Layer responsibilities that this project **renames or sharpens** (e.g. `crud/` here also owns cache invalidation).
- Multi-domain structure: if there are several ORM bases, services, or bounded contexts, name them and their boundaries.

If the project matches the default exactly, write: "Matches `agent-rules/repo-guide.md` default layout."

## 4. Key Runtime Flows

Document the most important runtime paths in the system. Add one subsection per meaningful flow, for example:

- ingestion flow
- event-processing flow
- request lifecycle
- model training or inference flow
- scheduled job execution

For each flow, include:

- trigger
- main steps
- key modules involved
- persistence or external-system touchpoints
- important decision points

Use Mermaid when it genuinely improves clarity.

## 5. Project-Specific Workflows

Default workflows (adding a table, an endpoint, a CLI command, an ETL step) follow the layer responsibilities in [`agent-kit/agent-rules/repo-guide.md`](../agent-kit/agent-rules/repo-guide.md). Do not restate them here.

Use this section only for workflows that **deviate from or extend** the defaults: cross-schema migrations, multi-step deployment ordering, regenerating a model registry, triggering a backfill, refreshing a materialized view, etc. For each, name: trigger, files touched, required evidence, and any ordering constraint.

If no project-specific workflows exist, write: "No deviations from default workflows."

## 6. Architectural Rules Of The Road

Generic placement and persistence rules (dependency direction, sessions at the edge, validation at boundaries, no raw `dict` across layers, exploration in `notebooks/WIP/`) live in [`agent-kit/agent-rules/repo-guide.md`](../agent-kit/agent-rules/repo-guide.md), [`agent-kit/agent-rules/validation.md`](../agent-kit/agent-rules/validation.md), and [`agent-kit/agent-rules/security.md`](../agent-kit/agent-rules/security.md).

Use this section only for rules **specific to this project** that sharpen, override, or add to those defaults — for example: "all writes to the `events` schema must go through `services/event_bus/`", or "no synchronous external HTTP calls inside request handlers".

Use short imperative statements. If there are no project-specific rules, write: "No deviations from default rules of the road."

## 7. External Integrations

Document third-party services and external APIs this system interacts with.

| Integration | Type | Direction | Contract | Notes |
|---|---|---|---|---|
|  | API / queue / storage / auth | inbound / outbound / both | REST / gRPC / SDK / webhook |  |

For each integration that matters: what data flows, who owns the contract, what happens when it is unavailable, and any auth/credential notes (without the credentials themselves).

If there are no external integrations, write: "No external integrations."

## 8. Operational And Technical Notes

Capture important runtime details not covered above:

- queues, schedulers, or background jobs
- feature flags and rollout controls
- model registry usage
- deployment ordering constraints
- observability entry points (log stream, dashboards, alert channels)

Mark unknown items explicitly rather than guessing.

## 9. Open Decisions And Pending Areas

List unresolved architectural items discovered during inspection.

| ID | Area | Current state | Why it matters | Suggested next step |
|---|---|---|---|---|
| A1 |  |  |  |  |

## Authoring Rules

- Describe the repository as it really is today.
- If something is planned but not implemented, label it clearly.
- Prefer concrete file areas and actual patterns over abstract principles.
- Do not duplicate the generic placement rules from `agent-kit/agent-rules/repo-guide.md` unless this project overrides or sharpens them.
