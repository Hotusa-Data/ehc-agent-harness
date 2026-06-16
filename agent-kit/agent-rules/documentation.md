---
triggers: [docs, planning, feature-work]
requires: [core]
see-also: [architecture, testing]
severity-default: MUST
---

# Documentation Rules

How the agent loads, creates, and updates durable documentation in a consumer repo. Authoritative source for load order, validation gates, creation-vs-update policy, and skeleton-to-doc mapping. `AGENTS.md` is a short map (cycle, commands, verification, pull requests, boundaries); rule details live in [`agent-rules/README.md`](README.md) and this file. `docs/docs-guide.md` holds per-project overrides.

Load when: any task that reads, writes, or relies on `docs/` artifacts, or that triggers a validation gate below.

## Rules

Rules are numbered **DOC-1** through **DOC-7**. Retired numbers are not reused.

### DOC-1 Load just-in-time, not eagerly [MUST]

Always load:
- `AGENTS.md`
- `agent-kit/agent-rules/core.md`
- `docs/docs-guide.md` (when present)

Load by task type:

| Task type | Add to load |
|---|---|
| Touches an existing feature | `docs/features/<feature>/{specs,plan,CHANGELOG}.md` |
| Uses business vocabulary | `docs/glossary.md` |
| Placement or structure unclear | `agent-kit/agent-rules/repo-guide.md`, `docs/architecture.md` |
| Architectural or system-boundary change | `agent-kit/agent-rules/architecture.md`, `docs/architecture.md` |
| ORM, queries, migrations, sessions | `agent-kit/agent-rules/persistence.md`, `docs/database.md` |
| Auth, secrets, trust boundaries, sensitive data | `agent-kit/agent-rules/security.md` |
| Tests | `agent-kit/agent-rules/testing.md` |
| Input checks, contracts, failure handling | `agent-kit/agent-rules/validation.md` |
| Logs, metrics, tracing | `agent-kit/agent-rules/observability.md` |
| Python code | `agent-kit/agent-rules/python.md` |

Large context is not useful context. Do not load files whose content will not influence the current decision.

### DOC-2 Satisfy validation gates before broad implementation [MUST]

| Gate | Trigger | Required action |
|---|---|---|
| Specs exist | New or changed behavior | Create or update `specs.md` before broad implementation |
| Plan exists | Non-trivial or multi-slice work | Create or update `plan.md` before coding |
| Glossary covers vocabulary | Ambiguous or new terms appear | Update `docs/glossary.md` before using in specs or code |
| Placement is clear | About to create a new folder or file | Consult `agent-kit/agent-rules/repo-guide.md` |
| CHANGELOG entry | Non-trivial change to specs / plan / scope | Append entry under `[Unreleased]` in feature CHANGELOG |
| Reconciliation done | Before commit | Code, specs, plan, CHANGELOG do not contradict each other |

### DOC-3 Update existing artifacts in place; create new only when distinct [MUST]

| Artifact | Create new when | Update existing when |
|---|---|---|
| Feature folder | Genuinely new feature with no existing folder | Always prefer updating in-place |
| `specs.md` | New feature | Scope or ACs change; implementation clarifies details |
| `plan.md` | New feature | Approach evolves; slices shift; status changes |
| `CHANGELOG.md` | New feature (created with the folder) | Append entry under `[Unreleased]` per non-trivial change |
| `report.md` | When the feature ships | Per cycle, not per micro-change |

Never create parallel folders for the same feature. Before creating a new feature folder, check whether `docs/features/<feature>/` already exists.

### DOC-4 Instantiate from skeletons, never improvise format [MUST]

If a target doc does not exist, create it from the matching skeleton in `agent-kit/skeletons/` rather than inventing a new shape.

| Skeleton | Target doc |
|---|---|
| `agent-kit/skeletons/_architecture.md` | `docs/architecture.md` |
| `agent-kit/skeletons/_database.md` | `docs/database.md` |
| `agent-kit/skeletons/_glossary.md` | `docs/glossary.md` |
| `agent-kit/skeletons/_docs-guide.md` | `docs/docs-guide.md` |
| `agent-kit/skeletons/_specs.md` | `docs/features/<feature>/specs.md` |
| `agent-kit/skeletons/_plan.md` | `docs/features/<feature>/plan.md` |
| `agent-kit/skeletons/_report.md` | `docs/features/<feature>/report.md` |
| `agent-kit/skeletons/_CHANGELOG.md` | `docs/features/<feature>/CHANGELOG.md` |

**Bootstrap shortcut:** After copying `agent-kit/` into a consumer repo, run `python agent-kit/adopt.py` from the project root (see metarepo README Track 1). It instantiates the base rows in this table, ensures `.gitignore` excludes `.local-context/`, and optionally scaffolds `docs/features/<feature>/` or root `AGENTS.md`. Manual copy from skeletons remains valid when the script is not used.

### DOC-5 Treat `docs/docs-guide.md` as the project's authority on required docs [MUST]

If `docs/docs-guide.md` exists, defer to it for the per-project list of required docs and any local overrides of load order or gates. This rule defines the defaults; the project doc lists what is actually required and any deviations.

### DOC-6 Project overrides must not silently contradict this rule [MUST]

Project-specific deviations (stricter gates, extra required docs, alternative load order) belong in the "Project-Specific Overrides" section of `docs/docs-guide.md` and must be stated explicitly so the agent can detect the override. Silent divergence between `AGENTS.md`, `docs/docs-guide.md`, and this file is a bug — align them before adding new rules.

### DOC-7 Feature CHANGELOGs follow a single convention [MUST]

Every feature `CHANGELOG.md` (instantiated from `agent-kit/skeletons/_CHANGELOG.md`) follows the same shape so reviewers do not have to re-learn the format per feature.

- **Filename:** always `CHANGELOG.md` (uppercase) — [Keep a Changelog](https://keepachangelog.com/) convention; do not use `changelog.md`. The metarepo lint enforces skeleton casing for Linux CI.
- Format based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
- Most recent version on top.
- One line per change; include the **why** (e.g. `Removed X (why: deprioritized)`).
- Standard Keep-a-Changelog sections: `Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`, `Security`.
- Feature-work extension sections: `Specs`, `Plan`, `Decided`. Use these under `[Unreleased]` to track in-flight scope and approach changes.
- In-flight work always lives under `[Unreleased]`. Do **not** use date-only headers (`## [2026-05-27]`) as a substitute — promote to a semver release (`## [1.1.0] — YYYY-MM-DD`) only when the feature actually ships.
- Bump the semver section when shipping a meaningful new release of the feature; reference `report.md` from the release entry.
- Do not duplicate git diffs — narrative only.

A CHANGELOG that drifts from this shape is a bug; fix the CHANGELOG rather than inventing local conventions.

## Anti-patterns

- Loading every doc in `docs/` regardless of task type.
- Creating a second feature folder because the existing one "feels off" instead of updating it.
- Writing freeform docs in a shape that does not match any skeleton.
- Restating load order or gates inside a feature doc instead of pointing at this rule.

## See also

- [core](core.md)
- [architecture](architecture.md)
- [testing](testing.md)
