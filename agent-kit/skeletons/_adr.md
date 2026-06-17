# ADR skeleton

Single source for everything under `docs/adr/`. On adoption, `adopt.py` writes **§Index** → `docs/adr/changelog.md` and **§Bootstrap** → `docs/adr/0001-system-context.md`. For each new decision, copy **§Entry** to `docs/adr/NNNN-short-slug.md`, fill it, and update `changelog.md` (Index table + `[Unreleased]`).

Default codemap and placement rules: [`agent-kit/agent-rules/REPO_GUIDE.md`](../../agent-kit/agent-rules/REPO_GUIDE.md) — record **deviations** in ADRs, not copies of the default tree.

## §Index

# Changelog — architecture decisions

Durable structural decisions for this repository. Load this file first, then only ADRs whose **Load when** matches the task ([`DOCUMENTATION.md`](../../agent-kit/agent-rules/DOCUMENTATION.md) §DOC-1). Conventions: [`DOCUMENTATION.md`](../../agent-kit/agent-rules/DOCUMENTATION.md) §DOC-10.

## 0. Metadata

- Last reviewed:

## Index

| ID | File | Title | Status | Load when |
|---|---|---|---|---|
| 0001 | [0001-system-context.md](0001-system-context.md) | System context | accepted | Onboarding, scope, stack constraints |

Add a row for every accepted ADR. Keep **Load when** short and task-oriented.

## [Unreleased]

### Proposed
-

### Decided
-

### Added
-

### When to write an ADR

See **DOC-10** in [`DOCUMENTATION.md`](../../agent-kit/agent-rules/DOCUMENTATION.md). In short:

| Write an ADR | Do not write an ADR |
|---|---|
| Layout delta vs kit default | Feature behavior → `specs.md` |
| External integration boundary | Deferred work → feature `changelog.md` `Decided` |
| Project-wide invariant | Cycle-scoped choice → `plan.md` §9 |

### Creating a new ADR

1. Copy **§Entry** from [`agent-kit/skeletons/_adr.md`](../../agent-kit/skeletons/_adr.md) to `docs/adr/NNNN-short-slug.md` (next id, lowercase slug).
2. Fill **Context**, **Decision**, and **Consequences** from the real codebase — not aspirations.
3. Add a row to **Index** and an entry under `[Unreleased]` → `Added`.
4. Vocabulary → `docs/glossary.md`; persistence detail → `docs/database.md`; runtime how-to → feature `plan.md`.

### Authoring rules

- Describe the repository as it is today. Label planned-but-not-built items explicitly.
- Prefer concrete module and folder **names** over deep path links (symbol search finds them).
- Do not restate the default codemap from `REPO_GUIDE.md` unless this project overrides it.
- Supersede old ADRs (update **Status**) instead of silently rewriting history.

## §Entry

# ADR-NNNN: Short title

- **Status:** proposed | accepted | deprecated | superseded by [NNNN-slug.md](NNNN-slug.md)
- **Date:** YYYY-MM-DD
- **Load when:** One line — when an agent should read this file (e.g. "Adding top-level folders", "External API integrations")

## Context

What problem or constraint forced a decision? What alternatives were considered?

## Decision

What we decided — imperative, concrete. Name modules, folders, or boundaries involved.

For layout deltas: state what this project **adds**, **removes**, or **renames** vs `REPO_GUIDE.md` — do not paste the full default tree.

## Consequences

What becomes easier or harder? What must hold going forward?

## Related ADRs

- [0001-system-context.md](0001-system-context.md) — (if applicable)

## Notes

Optional. Domain terms → `docs/glossary.md`. Schema contracts → `docs/database.md`.

## §Bootstrap

# ADR-0001: System context

- **Status:** accepted
- **Date:** YYYY-MM-DD
- **Load when:** Onboarding, scope questions, stack or deployment constraints

## Context

Contributors and agents need a stable snapshot of what this system is, how it runs, and which technologies are structural — without loading the entire codebase or restating the kit default layout.

## Decision

Describe this project in 3–6 sentences (edit for the real repo):

- **Purpose:** What the system does for users or downstream consumers.
- **Style:** Event-driven, request-response, batch, or hybrid.
- **Runtime:** Services, jobs, notebooks, containers, serverless, or mixed — and primary deployment target.
- **Stack:** Technologies that are structural (e.g. Python + FastAPI + PostgreSQL), not incidental scripts.
- **Constraints:** Regulatory, latency, multi-tenant, or data-volume limits that shape design.

**Domains:** If multiple bounded contexts exist, list them briefly (vocabulary → `docs/glossary.md`; persistence → `docs/database.md`). If one domain covers the system, say so.

**Layout:** If this repo matches the kit default, write: "Matches `agent-kit/agent-rules/REPO_GUIDE.md` default layout." Otherwise add dedicated ADRs (from 0002 onward) for each layout or integration deviation — do not turn this file into a codemap.

## Consequences

- First stop for "what kind of project is this?" after `docs/docs-guide.md`.
- Structural deviations get their own ADRs so this file stays short and stable.
- Revisit when purpose or deployment changes materially (~yearly, not every PR).

## Related ADRs

_(none yet — link layout or integration ADRs here as you add them)_

## Notes

Open product decisions belong in feature `specs.md` / `plan.md`, not here.
