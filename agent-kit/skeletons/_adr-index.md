# Architecture Decision Records

Index of durable structural decisions for this repository. The default codemap and placement rules live in [`agent-kit/agent-rules/REPO_GUIDE.md`](../../agent-kit/agent-rules/REPO_GUIDE.md) — do **not** restate that tree here.

Load `docs/adr/README.md` first, then only the ADR files whose **Load when** column matches the current task (see [`agent-kit/agent-rules/DOCUMENTATION.md`](../../agent-kit/agent-rules/DOCUMENTATION.md) §DOC-1).

## Index

| ID | File | Title | Status | Load when |
|---|---|---|---|---|
| 0001 | [0001-record-architecture-decisions.md](0001-record-architecture-decisions.md) | Record architecture decisions | accepted | Creating or changing ADR format |
| 0002 | [0002-system-context.md](0002-system-context.md) | System context | accepted | Onboarding, scope questions, stack constraints |

Add a row for every new ADR. Keep **Load when** short and task-oriented so agents can load just-in-time.

## Creating a new ADR

1. Copy [`agent-kit/skeletons/_adr-entry.md`](../../agent-kit/skeletons/_adr-entry.md) to `docs/adr/NNNN-short-slug.md` (next sequential number, lowercase slug).
2. Fill Context, Decision, and Consequences from the real codebase — not aspirations.
3. Add a row to the index table above.
4. Link related ADRs in **Related ADRs**; vocabulary → `docs/glossary.md`; persistence → `docs/database.md`.

**When to write an ADR** (see DOCUMENTATION.md §DOC-10): structural layout changes, external integration boundaries, project-specific invariants that outlive a single feature. **When not to:** feature behavior → `specs.md` / `plan.md`; deferred work → CHANGELOG `Decided`.

## Authoring rules

- Describe the repository as it is today. Label planned-but-not-built items explicitly.
- Prefer concrete module and folder **names** over deep path links (symbol search finds them).
- Do not duplicate the default codemap from `REPO_GUIDE.md` unless this project overrides it.
- Runtime how-to and slice-level decisions → feature `plan.md`, not ADRs.
