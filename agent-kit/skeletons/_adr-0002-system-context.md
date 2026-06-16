# ADR-0002: System context

- **Status:** accepted
- **Date:** YYYY-MM-DD
- **Load when:** Onboarding, scope questions, stack or deployment constraints

## Context

Contributors and agents need a stable snapshot of what this system is, how it runs, and which technologies are structural — without loading the entire codebase or restating the kit default layout.

## Decision

Describe this project in 3–6 sentences (edit below for the real repo):

- **Purpose:** What the system does for users or downstream consumers.
- **Style:** Event-driven, request-response, batch, or hybrid.
- **Runtime:** Services, jobs, notebooks, containers, serverless, or mixed — and primary deployment target.
- **Stack:** Technologies that are structural (e.g. Python + FastAPI + PostgreSQL), not incidental scripts.
- **Constraints:** Regulatory, latency, multi-tenant, or data-volume limits that shape design.

**Domains:** If multiple bounded contexts exist, list them briefly (detail and vocabulary → `docs/glossary.md`; persistence → `docs/database.md`). If one domain covers the system, say so.

**Layout:** If this repo matches the kit default, state: "Matches `agent-kit/agent-rules/REPO_GUIDE.md` default layout." Otherwise, add dedicated ADRs (from ADR-0003 onward) for each layout or integration deviation — do not expand this file into a codemap.

## Consequences

- ADR-0002 is the first stop for "what kind of project is this?" after `docs/docs-guide.md`.
- Structural deviations get their own ADRs so this file stays short and stable.
- Revisit this ADR when the product purpose or deployment model changes materially (roughly yearly, not every PR).

## Related ADRs

- ADR-0001 — Record architecture decisions
