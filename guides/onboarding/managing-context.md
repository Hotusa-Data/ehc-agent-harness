# Managing Context

How to manage context when working with AI coding agents: what to load, where to keep it, when to compact, and how to keep the repo coherent before each commit.

Companion to [context-engineering theory](../theory/context-engineering.md) and the [development lifecycle](lifecycle.md).

## TL;DR

> Chat is workspace, not memory. Durable knowledge lives in `docs/`. Throwaway notes live in `.local-context/`. The smallest context that supports correct work always beats the largest one.

If another developer or agent will need it later as repository truth, it must be in `docs/` before the work is considered complete.

## Why This Matters

Imagine showing up to build a feature. You load the codebase, start prompting... and the agent has no idea what database you use, what "tenant" means on your project, or whether you deploy to AWS or Netlify. Every single question it gets wrong costs you a round trip.

That's what happens without context management. The agent is smart, but it works blind.

This framework gives you four layers of context, each with a clear home, so the agent always knows *where* to look and *when*. You stop guessing. The agent stops hallucinating.

## The Four Context Layers

| Layer | Lives in | What it tells the AI |
|---|---|---|
| **Framework** | `AGENTS.md`, `agent-kit/agent-rules/`, `agent-kit/skeletons/` | How to work in this metarepo |
| **Project** | `docs/docs-guide.md`, `docs/architecture.md`, `docs/database.md`, `docs/glossary.md` | What kind of project this is |
| **Feature** | `docs/features/<feature>/{specs,plan,CHANGELOG}.md` | What's happening in the feature being touched |
| **Session** | `.local-context/` (gitignored) | Temporary working state for the current session |

> [!TIP]
> A request only needs all four when it crosses every layer. Most don't. Start with the layer you're sure about, then expand.

## Where Each Kind Of Knowledge Belongs

Single source of truth. Use this table before creating anything new:

| Knowledge | Goes to | Example |
|---|---|---|
| Stable repo operating rules | `AGENTS.md` | "Use Conventional Commits" |
| Durable project truth | `docs/architecture.md`, `docs/docs-guide.md` | "We deploy to AWS via GitHub Actions" |
| Shared vocabulary | `docs/glossary.md` | "*Tenant* = a customer organization" |
| What a feature must do | `docs/features/<feature>/specs.md` | Acceptance criteria, scope |
| How a feature is built | `docs/features/<feature>/plan.md` | Approach, contracts, slices, evidence strategy |
| What a feature shipped | `docs/features/<feature>/report.md` | Business validation at cycle close |
| Evolution of a feature | `docs/features/<feature>/CHANGELOG.md` | Narrative of requirement / specs / scope changes |
| Handoffs and session notes | `.local-context/` | "Stopped mid-refactor, retry test X" |

**Decision rule:**

- If it only helps continue **local work** → `.local-context/`
- If it should survive as **repository truth** → `docs/`

> [!NOTE]
> When in doubt: will another developer or agent need this next week? If yes, it goes in `docs/`.

## Setting It Up

Minimal setup so context flows correctly in every session.

### `AGENTS.md` — Always Loaded Rules

Place at repo root. The AI loads it automatically:

```markdown
# Project rules
- Always read docs/docs-guide.md before touching code
- Update specs/plan/CHANGELOG in docs/features/<feature>/ when behavior changes
- Never commit .local-context/
```

### `.gitignore` — Keep Session State Out

```gitignore
.local-context/
```

### `docs/` Tree — Predictable Layout

A predictable layout lets the AI find things without guessing. Stick to this tree:

```text
docs/
├── architecture.md
├── database.md
├── glossary.md
├── docs-guide.md
└── features/
    └── <feature>/
        ├── specs.md
        ├── plan.md
        ├── report.md          (created at cycle close)
        └── CHANGELOG.md
```

### Optional Hooks

Automate reconciliation checks:

- Block commits that touch `.local-context/`
- Warn when a spec is older than the code it describes
- **350-line rule** — add a lint rule that flags files exceeding 350 lines. Short files fit in the model's Smart Zone (0–100k tokens) and prevent the agent from drowning in monolithic modules.

Configure hooks via `settings.json` or a pre-commit hook.

## `.local-context/` In Practice

A scratchpad that lives in the repo but never gets committed.

```text
.local-context/
├── handoff-2026-05-27.md      # what you left mid-flight
├── session-notes.md           # scratchpad for current session
├── debug-cache-issue.md       # hypotheses you're testing
└── investigation-auth.md      # findings not yet promoted to docs/
```

**Rules:**

- Keep entries scoped and disposable
- Never treat it as the source of truth
- Promote durable findings into `docs/` before closing the session
- Never commit it

> [!CAUTION]
> If a finding from `.local-context/` will matter to another dev or agent next week, it belongs in `docs/` — copy it over, then the local note can die.

## What To Load And When

**Default load (most sessions):**

- `AGENTS.md`
- Relevant project docs (`docs/docs-guide.md`, `docs/architecture.md`, `docs/glossary.md`)
- Relevant feature context (if the feature is known)
- Existing specs, plan, or CHANGELOG for the same area
- The code and tests being touched

**When to load more:**

| Signal | Load |
|---|---|
| Task touches an existing feature | `docs/features/<feature>/{specs,plan,CHANGELOG}.md` |
| Request uses business terms ("tenant", "billing cycle") | `docs/glossary.md` |
| Placement or architecture unclear | `agent-kit/agent-rules/repo-guide.md`, `docs/architecture.md` |
| Existing behavior must be compared | The feature's current `specs.md` |
| Unclear whether a feature exists | List `docs/features/` first |

> [!TIP]
> Retrieve **just in time**. Large context is not the same as useful context — every irrelevant doc lowers signal.

**Research first** — before jumping into implementation, have the agent cache external knowledge (API docs, library references, schema snapshots) into a `research.md` file. This avoids burning context rediscovering facts the agent should only need to load once per feature.

## Context Hygiene: Clear, Compact, Handoff

Three moves for managing session state.

> [!TIP]
> Monitoring context size? The **Smart Zone** is 0–100k tokens. Beyond ~120k tokens attention degrades quickly and the model enters the "Dumb Zone." If your session feels heavy, check your token count. If you're approaching 100k, write a handoff and start fresh rather than compacting — every compact adds a layer of distortion. A clean session reasons better than a long one.

| Move | Use when | Signal |
|---|---|---|
| **`/clear`** | The goal changed | Starting a new task; current session has drifted; noisy debugging just ended |
| **`/compact`** | Continuity still matters but context is heavy | Same task continues; conversation is long; recent details still relevant |
| **handoff** | A fresh session picks up a focused slice | Switching agents; resuming tomorrow; want a clean restart without the token load |

**Practical cues:**

- Approaching token limits → `/compact`
- Pivoting to unrelated work → `/clear`
- Done for the day, work continues later → write a handoff in `.local-context/` and `/clear`

**Handoff storage rule:** write handoff files to `.local-context/`. They are gitignored and never committed. See the [`handoff`](../../skills/utils-skills/handoff/SKILL.md) skill for the full template.

> [!NOTE]
> See [context-engineering theory](../theory/context-engineering.md#hygiene-clear-compact-handoff-notes) for the full conceptual model. This file covers the practical application.

## Before The Commit: Reconcile

Before commit, code and durable context must not contradict each other.

### Reconciliation Checklist

- [ ] Implemented behavior matches the current `specs.md`
- [ ] Current `plan.md` reflects what actually happened
- [ ] `CHANGELOG.md` has an entry for each non-trivial change made this cycle
- [ ] Architecture or docs-guide updated if durable project knowledge changed
- [ ] Glossary updated if vocabulary changed
- [ ] Nothing important exists only in chat or `.local-context/`
- [ ] `.local-context/` files are excluded from the commit

> [!WARNING]
> The work is not closed if the code is correct but the durable context is stale. Stale context is technical debt that compounds every session.

### Real-World Scenario

You just implemented billing for multi-tenant orgs. The code works, tests pass. Before committing:

1. Does `specs.md` still say "billing per user" or did you update it to "billing per org"? → Update specs.
2. Did you add a `tenantId` field to the schema? → Update `docs/database.md` and `docs/glossary.md`.
3. Did the approach change along the way? → Update `plan.md`.
4. Is there a `.local-context/investigation-pricing.md` with findings that should live in `docs/`? → Promote it.

## Anti-patterns

- Starting work without reading project docs (`docs/docs-guide.md`, `docs/architecture.md`)
- Loading every feature folder regardless of scope
- Treating chat memory as project memory
- Treating `.local-context/` as durable documentation
- Creating duplicate feature folders for the same work
- Leaving stale feature docs after implementation changed direction
- Committing local handoffs or session artifacts
- Treating specs as compile targets and ignoring the actual code

## Related

- [ai-configuration.md](ai-configuration.md) — tool setup, permissions, models
- [lifecycle.md](lifecycle.md) — the full development workflow
- [../theory/context-engineering.md](../theory/context-engineering.md) — deep theory behind context management
