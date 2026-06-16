---
triggers: [docs, planning, feature-work]
requires: [CORE]
see-also: [ARCHITECTURE, TESTING]
---

# Documentation Rules

How the agent loads, creates, and updates durable documentation in a consumer repo. Authoritative source for load order, validation gates, creation-vs-update policy, and skeleton-to-doc mapping. `AGENTS.md` is a short map (cycle, commands, verification, pull requests, boundaries); rule details live in [`RULES.md`](RULES.md) and this file. `docs/docs-guide.md` holds per-project overrides.

Load when: any task that reads, writes, or relies on `docs/` artifacts, or that triggers a validation gate below.

## Rules

Rules are numbered **DOC-1** through **DOC-10**. Retired numbers are not reused.

### DOC-1 Load just-in-time, not eagerly [MUST]

Always load:
- `AGENTS.md`
- `agent-kit/agent-rules/CORE.md`
- `docs/docs-guide.md` (when present)

Load by task type:

| Task type | Add to load |
|---|---|
| Touches an existing feature | `docs/features/<feature>/{specs,plan,CHANGELOG}.md` |
| Uses business vocabulary | `docs/glossary.md` |
| Placement or structure unclear | `agent-kit/agent-rules/REPO_GUIDE.md` (default codemap), `docs/adr/README.md` + relevant ADR (layout deltas only) |
| Layer contracts, circular imports, or abstraction boundaries | `agent-kit/agent-rules/ARCHITECTURE.md` |
| Layout or system-boundary change in this repo | New or updated ADR under `docs/adr/`; `REPO_GUIDE.md` / `ARCHITECTURE.md` when kit rules apply |
| ORM, queries, migrations, sessions | `agent-kit/agent-rules/PERSISTENCE.md`, `docs/database.md` |
| Auth, secrets, trust boundaries, sensitive data | `agent-kit/agent-rules/SECURITY.md` |
| Tests | `agent-kit/agent-rules/TESTING.md` |
| Input checks, contracts, failure handling | `agent-kit/agent-rules/VALIDATION.md` |
| Logs, metrics, tracing | `agent-kit/agent-rules/OBSERVABILITY.md` |
| Python code | `agent-kit/agent-rules/PYTHON.md` |

Large context is not useful context. Do not load files whose content will not influence the current decision.

### DOC-2 Satisfy validation gates before broad implementation [MUST]

| Gate | Trigger | Required action |
|---|---|---|
| Specs exist | New or changed behavior | Create or update `specs.md` before broad implementation |
| Plan exists | Non-trivial or multi-slice work | Create or update `plan.md` before coding |
| Mode declared | Non-trivial feature work | `Harness mode` in specs/plan metadata, or PR/CHANGELOG states lightweight skip |
| Testing plan exists | Non-trivial Build after Plan Review | `plan.md` §2 has a row for every Must AC before broad implementation |
| Glossary covers vocabulary | Ambiguous or new terms appear | Update `docs/glossary.md` before using in specs or code |
| Placement is clear | About to create a new folder or file | Consult `agent-kit/agent-rules/REPO_GUIDE.md` |
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
| `agent-kit/skeletons/_adr-index.md` | `docs/adr/README.md` |
| `agent-kit/skeletons/_adr-0001-record-decisions.md` | `docs/adr/0001-record-architecture-decisions.md` |
| `agent-kit/skeletons/_adr-0002-system-context.md` | `docs/adr/0002-system-context.md` |
| `agent-kit/skeletons/_adr-entry.md` | Template only — copy to `docs/adr/NNNN-slug.md` for new ADRs |
| `agent-kit/skeletons/_database.md` | `docs/database.md` |
| `agent-kit/skeletons/_glossary.md` | `docs/glossary.md` |
| `agent-kit/skeletons/_docs-guide.md` | `docs/docs-guide.md` |
| `agent-kit/skeletons/_specs.md` | `docs/features/<feature>/specs.md` |
| `agent-kit/skeletons/_plan.md` | `docs/features/<feature>/plan.md` |
| `agent-kit/skeletons/_report.md` | `docs/features/<feature>/report.md` |
| `agent-kit/skeletons/_CHANGELOG.md` | `docs/features/<feature>/CHANGELOG.md` |

**Bootstrap shortcut:** After copying `agent-kit/` into a consumer repo, run `python agent-kit/adopt.py` from the project root. It instantiates the base rows in this table, ensures `.gitignore` excludes `.local-context/`, and optionally scaffolds `docs/features/<feature>/` or root `AGENTS.md`. Manual copy from skeletons remains valid when the script is not used.

### DOC-5 Treat `docs/docs-guide.md` as the project's authority on required docs [MUST]

If `docs/docs-guide.md` exists, defer to it for the per-project list of required docs and any local overrides of load order or gates. This rule defines the defaults; the project doc lists what is actually required and any deviations.

### DOC-6 Project overrides must not silently contradict this rule [MUST]

Project-specific deviations (stricter gates, extra required docs, alternative load order) belong in the "Project-Specific Overrides" section of `docs/docs-guide.md` and must be stated explicitly so the agent can detect the override. Silent divergence between `AGENTS.md`, `docs/docs-guide.md`, and this file is a bug — align them before adding new rules.

### DOC-7 Feature CHANGELOGs follow a single convention [MUST]

Every feature `CHANGELOG.md` must match the shape in `agent-kit/skeletons/_CHANGELOG.md` — do not invent local formats.

- **Filename:** always `CHANGELOG.md` (uppercase); metarepo lint enforces skeleton casing for Linux CI.
- In-flight work under `[Unreleased]`; use extension sections `Specs`, `Plan`, `Decided` for scope and deferred work.
- Promote to semver (`## [1.1.0] — YYYY-MM-DD`) only when the feature ships; reference `report.md` from the release entry.
- Narrative only — no git diffs. Full section list and examples: skeleton header and `_CHANGELOG.md` body.

### DOC-8 Reconcile docs with the diff before review [MUST]

Use the existing `docs/` tree only — no new registry files.

| Trigger | Required action |
|---|---|
| Behavior change | Update `specs.md`, or record the delta under `[Unreleased]` → `Specs` / `Changed` in CHANGELOG — do not add step-by-step flows to ADRs |
| New business term in spec or code | Update `docs/glossary.md` before opening the PR |
| New top-level folder, package layer, or module that changes the codemap | New ADR (or update existing layout ADR); name modules/folders in the Decision section |
| New external integration (architectural boundary) | New ADR with brief boundary rule; persistence-only detail → `docs/database.md` |
| Code change only within an existing layer | No ADR unless a new project-specific invariant must be recorded |
| Deferred or partial fix | Record under `[Unreleased]` → `Decided` in CHANGELOG with follow-up scope |
| AC or Req changed during build | Update `specs.md` §5/§8 or CHANGELOG `Specs`; update `plan.md` §1 Req/AC columns |
| Feature cycle closes | Add or update `report.md`; promote `[Unreleased]` to a semver release when shipping |

### DOC-9 Doc hygiene at session and PR close [MUST]

Before handoff or PR:

- [ ] Durable facts in `.local-context/` are promoted into `docs/` or discarded
- [ ] Feature CHANGELOG has a `[Unreleased]` entry when specs, plan, or scope moved
- [ ] Open assumptions are in `plan.md`, `specs.md`, or CHANGELOG `Decided` — not only in chat
- [ ] No parallel feature folder for the same scope — update the existing folder in place
- [ ] Docs touched by the change match the diff (DOC-8)

### DOC-10 Architecture decisions live in `docs/adr/` [MUST]

Structural decisions use numbered ADRs under `docs/adr/`, indexed in `docs/adr/README.md`.

| Write an ADR when | Do not write an ADR when |
|---|---|
| New top-level folder or layer that changes the codemap | Feature behavior or AC change → `specs.md` |
| External integration or trust boundary | Deferred slice → CHANGELOG `Decided` |
| Project-wide invariant that outlives one feature | Cycle-scoped choice → `plan.md` §9 |
| Superseding a prior structural choice | Restating `REPO_GUIDE.md` default layout |

- **Format:** copy `_adr-entry.md`; filename `NNNN-short-slug.md`; update the index in `README.md`.
- **Load:** read `docs/adr/README.md`, then only ADRs whose **Load when** matches the task (DOC-1).
- **System overview:** ADR-0002 (`_adr-0002-system-context.md`) — edit on adoption, revisit ~yearly.
- **Status:** `proposed`, `accepted`, `deprecated`, or `superseded by ADR-XXXX` — do not delete history.

## Anti-patterns

- Loading every doc in `docs/` regardless of task type.
- Creating a second feature folder because the existing one "feels off" instead of updating it.
- Writing freeform docs in a shape that does not match any skeleton.
- Restating load order or gates inside a feature doc instead of pointing at this rule.
- Leaving stale specs because "the code is the truth" — update the spec or CHANGELOG the delta.
- Recording deferred work only in chat or `.local-context/` — use CHANGELOG `Decided` (DOC-7).
- Restating the default codemap from `REPO_GUIDE.md` inside an ADR without recording a real deviation.
- Growing ADRs with runtime how-to or feature flows that belong in feature `plan.md` (DOC-8).
- Adding an ADR without a row in `docs/adr/README.md`.
- Filling every skeleton section in **standard** Harness mode when the Section guide marks sections omit — trim instead.

## Project Overrides

Doc load order and gate overrides: `docs/docs-guide.md` §3 and this section. See **DOC-6**.

## See also

- [CORE](CORE.md)
- [ARCHITECTURE](ARCHITECTURE.md)
- [TESTING](TESTING.md)
