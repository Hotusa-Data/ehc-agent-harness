# ADR-0001: Record architecture decisions

- **Status:** accepted
- **Date:** YYYY-MM-DD
- **Load when:** Creating or changing ADR format in this repo

## Context

This project uses the agent-kit harness. Structural choices (layout deltas, integration boundaries, project-wide invariants) must survive beyond chat and individual feature cycles. A single monolithic architecture doc tends to grow into an unmaintainable atlas.

We adopt the [Architecture Decision Record](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions) pattern: numbered, immutable-ish entries under `docs/adr/`, indexed in `docs/adr/README.md`.

## Decision

- Store ADRs as `docs/adr/NNNN-short-slug.md` (four-digit id, lowercase slug).
- Maintain the index in `docs/adr/README.md` with **Load when** hints for just-in-time loading.
- New ADRs are created from `agent-kit/skeletons/_adr-entry.md`.
- Default codemap stays in `agent-kit/agent-rules/REPO_GUIDE.md`; record **deviations** as ADRs, not copies of the default tree.
- Feature-scoped behavior stays in `docs/features/<feature>/` — not in ADRs.

## Consequences

- Agents load `README.md` plus relevant ADRs instead of a single growing architecture file.
- Layout and boundary changes require a new ADR (or updating status on a superseded one), improving auditability.
- Teams must keep the index table current when adding ADRs.

## Related ADRs

- ADR-0002 — System context for this repository
