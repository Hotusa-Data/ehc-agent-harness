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

For other files, use [`RULES.md`](RULES.md) (load triggers + canonical topic owners). Common additions:

| Task type | Add to load |
|---|---|
| Touches an existing feature | `docs/features/<feature>/{specs,plan,changelog}.md` |
| Uses business vocabulary | `docs/glossary.md` |
| Placement or structure unclear | `REPO_GUIDE.md`, `docs/adr/changelog.md` + relevant ADR |
| Layer contracts or circular imports | `ARCHITECTURE.md` |
| ORM, migrations, sessions | `PERSISTENCE.md`, `docs/database.md` |
| Auth, secrets, sensitive data | `SECURITY.md` |
| Tests | `TESTING.md` |
| Input checks and contracts | `VALIDATION.md` |
| Logs and metrics | `OBSERVABILITY.md` |
| Python code | `PYTHON.md` |

Large context is not useful context. Do not load files whose content will not influence the current decision.

### DOC-2 Satisfy validation gates before broad implementation [MUST]

| Gate | Trigger | Required action |
|---|---|---|
| Specs exist | New or changed behavior | Create or update `specs.md` before broad implementation |
| Plan exists | Non-trivial or multi-slice work | Create or update `plan.md` before coding |
| Mode declared | Non-trivial feature work | `Harness mode` in specs/plan metadata, or PR/changelog states lightweight skip |
| Testing plan exists | Non-trivial Build after Plan Review | `plan.md` §2 has a row for every Must AC before broad implementation |
| Glossary covers vocabulary | Ambiguous or new terms appear | Update `docs/glossary.md` before using in specs or code |
| Placement is clear | About to create a new folder or file | Consult `agent-kit/agent-rules/REPO_GUIDE.md` |
| Changelog entry | Non-trivial change to specs / plan / scope | Append entry under `[Unreleased]` in the relevant changelog |
| Reconciliation done | Before commit | Code, specs, plan, changelog do not contradict each other |

### DOC-3 Update existing artifacts in place; create new only when distinct [MUST]

| Artifact | Create new when | Update existing when |
|---|---|---|
| Feature folder | Genuinely new feature with no existing folder | Always prefer updating in-place |
| `specs.md` | New feature | Scope or ACs change; implementation clarifies details |
| `plan.md` | New feature | Approach evolves; slices shift; status changes |
| `changelog.md` (feature) | New feature (created with the folder) | Append entry under `[Unreleased]` per non-trivial change |
| `docs/adr/changelog.md` | On adoption (`adopt.py`) | New ADR accepted; proposed/decided structural work |
| `report.md` | When the feature ships | Per cycle, not per micro-change |

Never create parallel folders for the same feature. Before creating a new feature folder, check whether `docs/features/<feature>/` already exists.

### DOC-4 Instantiate from skeletons, never improvise format [MUST]

If a target doc does not exist, create it from the matching skeleton in `agent-kit/skeletons/` rather than inventing a new shape.

| Skeleton | Target doc |
|---|---|
| `agent-kit/skeletons/_adr.md` | §Index → `docs/adr/changelog.md`; §Bootstrap → `docs/adr/0001-system-context.md`; copy §Entry for each new ADR |
| `agent-kit/skeletons/_database.md` | `docs/database.md` |
| `agent-kit/skeletons/_glossary.md` | `docs/glossary.md` |
| `agent-kit/skeletons/_docs-guide.md` | `docs/docs-guide.md` |
| `agent-kit/skeletons/_specs.md` | `docs/features/<feature>/specs.md` |
| `agent-kit/skeletons/_plan.md` | `docs/features/<feature>/plan.md` |
| `agent-kit/skeletons/_report.md` | `docs/features/<feature>/report.md` |
| `agent-kit/skeletons/_changelog.md` | `docs/features/<feature>/changelog.md` |

**Bootstrap shortcut:** After copying `agent-kit/` into a consumer repo, run `python agent-kit/adopt.py` from the project root. It instantiates the base rows in this table, ensures `.gitignore` excludes `.local-context/`, and optionally scaffolds `docs/features/<feature>/` or root `AGENTS.md`. Manual copy from skeletons remains valid when the script is not used.

### DOC-5 Treat `docs/docs-guide.md` as the project's authority on required docs [MUST]

If `docs/docs-guide.md` exists, defer to it for the per-project list of required docs and any local overrides of load order or gates. This rule defines the defaults; the project doc lists what is actually required and any deviations.

### DOC-6 Project overrides must not silently contradict this rule [MUST]

Project-specific deviations (stricter gates, extra required docs, alternative load order) belong in the "Project-Specific Overrides" section of `docs/docs-guide.md` and must be stated explicitly so the agent can detect the override. Silent divergence between `AGENTS.md`, `docs/docs-guide.md`, and this file is a bug — align them before adding new rules.

### DOC-7 Feature changelogs follow a single convention [MUST]

Every feature `changelog.md` must match the shape in `agent-kit/skeletons/_changelog.md` — do not invent local formats.

- **Filename:** always `changelog.md` (lowercase); metarepo lint enforces skeleton casing for Linux CI.
- In-flight work under `[Unreleased]`; use extension sections `Specs`, `Plan`, `Decided` for scope and deferred work.
- Promote to semver (`## [1.1.0] — YYYY-MM-DD`) only when the feature ships; reference `report.md` from the release entry.
- Narrative only — no git diffs. Full section list and examples: skeleton header and `_changelog.md` body.

### DOC-8 Reconcile docs with the diff and close the session [MUST]

Use the existing `docs/` tree only — no new registry files.

| Trigger | Required action |
|---|---|
| Behavior change | Update `specs.md`, or record the delta under `[Unreleased]` → `Specs` / `Changed` in feature changelog — do not add step-by-step flows to ADRs |
| New business term in spec or code | Update `docs/glossary.md` before opening the PR |
| New top-level folder, package layer, or module that changes the codemap | New ADR (or update existing layout ADR); update `docs/adr/changelog.md` Index |
| New external integration (architectural boundary) | New ADR with brief boundary rule; persistence-only detail → `docs/database.md` |
| Code change only within an existing layer | No ADR unless a new project-specific invariant must be recorded |
| Deferred or partial fix | Feature changelog `Decided`; structural deferral → `docs/adr/changelog.md` `[Unreleased]` → `Decided` |
| AC or Req changed during build | Update `specs.md` §5/§8 or feature changelog `Specs`; update `plan.md` §1 Req/AC columns |
| Feature cycle closes | Add or update `report.md`; promote `[Unreleased]` to a semver release when shipping |

Before handoff or PR:

- [ ] Durable facts in `.local-context/` are promoted into `docs/` or discarded
- [ ] Relevant changelog has a `[Unreleased]` entry when specs, plan, scope, or ADRs moved
- [ ] Open assumptions are in `plan.md`, `specs.md`, or changelog `Decided` — not only in chat
- [ ] No parallel feature folder for the same scope — update the existing folder in place
- [ ] Docs touched by the change match the diff (table above)

### DOC-9 Doc hygiene at session and PR close [MUST]

Complete the checklist in **DOC-8** before handoff or PR.

### DOC-10 Architecture decisions live in `docs/adr/` [MUST]

Structural decisions use numbered ADRs under `docs/adr/`, indexed in `docs/adr/changelog.md` (same lowercase convention as feature changelogs; shape from `_adr.md` §Index).

| Write an ADR when | Do not write an ADR when |
|---|---|
| New top-level folder or layer that changes the codemap | Feature behavior or AC change → `specs.md` |
| External integration or trust boundary | Deferred slice → feature `changelog.md` `Decided` |
| Project-wide invariant that outlives one feature | Cycle-scoped choice → `plan.md` §9 |
| Superseding a prior structural choice | Restating `REPO_GUIDE.md` default layout |

- **Format:** copy **§Entry** from `_adr.md` to `docs/adr/NNNN-short-slug.md`; update `docs/adr/changelog.md` (Index + `[Unreleased]`).
- **Load:** read `docs/adr/changelog.md`, then only ADRs whose **Load when** matches the task (DOC-1).
- **System overview:** `docs/adr/0001-system-context.md` — edit on adoption, revisit ~yearly.
- **Status:** `proposed`, `accepted`, `deprecated`, or superseded — do not delete history.

## Anti-patterns

- Loading every doc in `docs/` regardless of task type.
- Creating a second feature folder because the existing one "feels off" instead of updating it.
- Writing freeform docs in a shape that does not match any skeleton.
- Restating load order or gates inside a feature doc instead of pointing at this rule.
- Leaving stale specs because "the code is the truth" — update the spec or changelog the delta.
- Recording deferred work only in chat or `.local-context/` — use changelog `Decided` (DOC-7 / DOC-10).
- Restating the default codemap from `REPO_GUIDE.md` inside an ADR without recording a real deviation.
- Growing ADRs with runtime how-to or feature flows that belong in feature `plan.md` (DOC-8).
- Adding an ADR without a row in `docs/adr/changelog.md`.
- Filling every skeleton section in **standard** Harness mode when the Section guide marks sections omit — trim instead.

## Project Overrides

Doc load order and gate overrides: `docs/docs-guide.md` §3 and this section. See **DOC-6**.

## See also

- [CORE](CORE.md)
- [ARCHITECTURE](ARCHITECTURE.md)
- [TESTING](TESTING.md)
