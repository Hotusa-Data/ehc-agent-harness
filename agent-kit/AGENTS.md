# AGENTS.md

Template for the agent entrypoint at **repo root**. `python agent-kit/adopt.py --agents` copies this file to `./AGENTS.md`. Paths below (`agent-kit/…`, `docs/…`) assume that layout — read this first every session.

Domain knowledge lives in `docs/`. Engineering rules in `agent-kit/agent-rules/`. Skeletons in `agent-kit/skeletons/`.

> **Note.** First bootstrap after copying `agent-kit/`: run `python agent-kit/adopt.py --agents` from the repo root (see [`agent-kit/agent-rules/DOCUMENTATION.md` §DOC-4](agent-kit/agent-rules/DOCUMENTATION.md)). `--feature` scaffolds `specs.md`, `plan.md`, and `changelog.md` only — `report.md` is created at cycle close. Session scratch: gitignored `.local-context/` at repo root.

---

## Role and scope

**Kit profile:** Python **data** stack (template). Override stack, commands, and layout in `docs/docs-guide.md` §3; non-Python guidance in [`agent-kit/README.md`](agent-kit/README.md).

Work is organized by features under `docs/features/<feature>/`. Non-trivial changes follow the [working cycle](#working-cycle). In monorepos, nested `AGENTS.md` in subpackages overrides this file for paths underneath.

---

## Working cycle

Every non-trivial task follows five phases. Lightweight work may skip phases — name what you skip and why (usually in the PR or changelog).

### Work sizing

| Size | When | Feature docs | Harness mode | Gates |
|---|---|---|---|---|
| **Lightweight** | Typo/tweak; no behavior or contract change | None — state skips in PR/changelog | _(none)_ | PR if opened |
| **Non-trivial standard** | Behavior change; limited blast radius (~1–4 slices) | `specs.md` + `plan.md` | `standard` | Spec, Plan, PR |
| **Non-trivial full** | Migrations, contracts, security, high blast radius | `specs.md` + `plan.md` (full skeleton) | `full` | Spec, Plan, PR |

Set `Harness mode` in specs/plan metadata. Section trim rules: [`DOCUMENTATION.md` §DOC-2](agent-kit/agent-rules/DOCUMENTATION.md).

```
Context → Spec ──[Spec Review]──► Plan ──[Plan Review]──► Build ──[PR Review]──► Document ──► merge
```

Backward loops: unclear Spec → Context; broken assumption in Build → Plan; stale docs after Build → Document before close.

| Phase | What you do | Key artifacts |
|---|---|---|
| **Context** | Load rules, project docs, feature state | `AGENTS.md`, `docs/docs-guide.md`, `docs/adr/changelog.md`, `docs/glossary.md` |
| **Spec** | Define what must change and why | `docs/features/<feature>/specs.md` |
| **Plan** | Decide how to implement, slice, test, document | `docs/features/<feature>/plan.md` |
| **Build** | Implement in small, reviewable slices | code, tests, notebook mockups |
| **Document** | Update every durable doc the change touched | glossary, `changelog.md`, `report.md` |

**Human review stops** — a person must approve before the next phase begins.

| When | What is reviewed | Who |
|---|---|---|
| Post-Spec | `specs.md` — scope, ACs, business rules | Domain expert or lead |
| Post-Plan | `plan.md` — §1 tasks, §2 testing plan, §3 evidence | Technical lead |
| Post-Build | PR diff — implementation, tests, docs | Reviewer assigned to the PR |

---

## Session bootstrap

Always load:

1. `agent-kit/agent-rules/CORE.md` — universal engineering and collaboration rules
2. `docs/docs-guide.md` — per-project required docs and local overrides (when present); authoritative over kit defaults

For other rules, use [`RULES.md`](agent-kit/agent-rules/RULES.md) (pick one file — do not load the whole index) and [`DOCUMENTATION.md` §DOC-1](agent-kit/agent-rules/DOCUMENTATION.md).

---

## Commands

Customize after `adopt.py --agents` (defaults below match the template). Overrides also live in `docs/docs-guide.md` §3.

| Action | Command |
|---|---|
| Install dependencies | `uv sync` _(adapt to project)_ |
| Run all tests | `uv run pytest` _(adapt path/flags)_ |
| Run one test | `uv run pytest path/to/test.py::test_name -xvs` |
| Lint | `uv run ruff check .` _(or project equivalent)_ |
| Format | `uv run ruff format .` _(or project equivalent)_ |
| Type-check | _(if applicable — e.g. `uv run mypy src/`)_ |
| Run app / notebook | _(project-specific)_ |

Scope commands to changed packages in monorepos. Stack defaults: [`PYTHON.md`](agent-kit/agent-rules/PYTHON.md), [`TESTING.md`](agent-kit/agent-rules/TESTING.md).

---

## Verification before PR

Before requesting review or marking work complete:

- [ ] Relevant tests for changed behavior pass (see [Commands](#commands))
- [ ] Lint/format checks pass on touched files
- [ ] For non-trivial work: feature docs and touched base docs match the code (see `agent-kit/agent-rules/DOCUMENTATION.md` §DOC-8)
- [ ] No secrets, credentials, or `.local-context/` content in the diff
- [ ] Distinguish what you ran from what you only wrote (see `agent-kit/agent-rules/CORE.md` §COOP-3)

---

## Pull requests

Customize after adoption. Title format and commit conventions may also be overridden in `docs/docs-guide.md` §3.

**Title format:** `[<feature>] <short user-facing impact>` _(adapt — e.g. Conventional Commits scope)_

**Description must include:**

- What changed and why (2–4 sentences)
- Feature link: `docs/features/<feature>/` when applicable
- Test evidence: commands run and outcome (see [Verification before PR](#verification-before-pr))
- Lifecycle: work size (lightweight / Harness mode), phases skipped and why, if any
- Open questions or follow-ups for the reviewer

A human opens and publishes the PR — do not push to remote (see [Boundaries](#boundaries)).

---

## Boundaries

Critical limits for every session. Collaboration detail: [`CORE.md`](agent-kit/agent-rules/CORE.md) (**COOP-1**–**COOP-3**).

**Ask first**

- Scope, acceptance criteria, or business-rule changes mid-build
- New dependencies, migrations, or destructive data operations
- Skipping a lifecycle phase on non-trivial work

**Never**

- Push to remote or bypass git hooks — a human publishes
- Commit secrets, credentials, or anything under `.local-context/`
- Invent business rules not in specs or glossary (**COOP-1**)
- Modify files unless the user requested the change or confirmed the plan

Human review gates (Spec, Plan, PR) are mandatory for non-trivial work — see [Working cycle](#working-cycle).

---

## Where durable knowledge lives

`docs/` holds project knowledge: `docs/adr/`, `docs/glossary.md`, `docs/docs-guide.md`, `docs/database.md`, and `docs/features/<feature>/{specs,plan,changelog,report}.md`. Instantiate missing docs from `agent-kit/skeletons/` — [`DOCUMENTATION.md` §DOC-4](agent-kit/agent-rules/DOCUMENTATION.md). Scratch: `.local-context/` (gitignored); promote durable facts into `docs/` before close.
