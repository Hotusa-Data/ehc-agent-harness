# Subagents

A practical introduction to subagents for developers — what they are, when they beat a skill or a plain prompt, and how to set them up in Cursor.

## TL;DR

A subagent is a **context tool**: a bounded worker that runs in its own context window, with its own system prompt, model, and tool restrictions. The parent agent delegates to it, the subagent works, and only the summary returns. Use one when a side task would flood your main conversation, when you need parallel investigations, or when you keep spawning the same kind of isolated worker.

The goal is **not** to anthropomorphize synthetic experts ("data engineer", "code reviewer"). The general model already carries domain knowledge; shared rules live in `agent-kit/agent-rules/` and `docs/`. Subagents exist to **delegate work with its own context** — not to simulate job titles.

```markdown
---
name: diff-scanner
description: Scans the current diff for correctness and security issues. Returns findings only — never edits files. Use after substantive edits.
tools: Read, Grep, Glob, Bash
model: sonnet
readonly: true
---

Scan the files changed in this task. Return specific, actionable findings.
Do not edit files. Do not restate unchanged code.
```

## Subagents Are Context Tools, Not Personas

Treat subagents as **isolated execution contexts**, not as synthetic team members.

| Wrong mental model | Right mental model |
|---|---|
| "I need a data-engineer subagent because this is pipeline work" | "I need an isolated context to explore three ingestion modules in parallel without flooding the main chat" |
| "The subagent is the expert; the parent is the manager" | "The subagent is a sandboxed run; the parent orchestrates and synthesizes" |
| "More personas = better coverage" | "More isolated contexts = cleaner parent context and optional parallelism" |

The general model already knows data engineering, testing, security review, and the rest. What it lacks in a long session is **room** — every search result, log dump, and exploration trace competes for the same window. Subagents buy space by moving verbose work off-stage.

What you get:
- **Context isolation** — exploration and high-volume output stay in a separate window; only the summary returns
- **Parallelism** — independent tasks dispatched simultaneously, each with its own context
- **Constraint enforcement** — restrict tools, permissions, or models per delegation unit
- **Reusability** — the same worker definition runs across sessions and projects
- **Cost control** — route cheap, repetitive exploration to a faster or cheaper model without touching the main session

What subagents are **not** for:
- replacing domain expertise the general model already has
- standing in for [skills](skills.md) that encode repeatable workflows
- creating a cast of job-title personas that duplicate `agent-kit/agent-rules/`

## Why Subagents Exist

The main conversation is a public good. Subagents move work off-stage so the parent stays focused on orchestration and synthesis.

Typical triggers:
- a task produces verbose output (test runs, log scans, wide repo searches)
- several independent investigations can run at once
- you want enforced tool restrictions for a bounded pass (read-only scan, no writes)
- you want a different model or prompt for one leg of work without changing the parent session

## Subagent vs Skill vs Prompt vs Tool

| Concept | Main question | Role |
|---|---|---|
| Tool | What action can I take? | Single capability (run a script, call an API) |
| Prompt | What do I want right now? | One-off instruction |
| Skill | How should this kind of task be done? | Reusable workflow + context |
| Subagent | Where should this work run? | Isolated context for a bounded delegation |

Rules of thumb:
- repeatable workflow → **skill** (see [skills.md](skills.md))
- isolated context or parallel delegation → **subagent**
- single atomic action → **tool**
- one-time ask → **prompt**

A subagent can use one or more skills — they compose. Cursor ships built-in subagents (Explore, generalPurpose, shell, and others); the official docs keep the current list.

## Anatomy Of A Subagent

A subagent is a markdown file with YAML frontmatter (config) followed by the system prompt (body).

```markdown
---
name: diff-scanner
description: Scans the current diff for correctness and security issues. Returns findings only — never edits files. Use after substantive edits.
tools: Read, Grep, Glob, Bash
model: sonnet
readonly: true
---

Scan the files changed in this task. Return specific, actionable findings.
Do not edit files. Do not restate unchanged code.
```

Frontmatter rules:
- `name`: lowercase letters and hyphens. Name the **task or context boundary**, not a job title. Unique within its scope.
- `description`: tells the parent agent **when to delegate**. Write in third person, name the trigger, add "use proactively" if you want automatic delegation.
- Body: becomes the subagent's system prompt — it *replaces* the default Cursor agent prompt rather than extending it. State the bounded task, output shape, and hard constraints (especially what the worker must not do).

## When To Use A Subagent (And When Not To)

**Good candidates**
- the task produces verbose output (test runs, log scans, doc fetching)
- the work is self-contained and can return a summary
- you want enforced tool restrictions (read-only research, no-Edit reviewer)
- you keep spawning the same worker with the same instructions
- you want to route routine work to a cheaper or faster model

**Skip the subagent if**
- the task needs frequent back-and-forth or user clarification
- the work is short enough to do inline
- the role boundary is fuzzy — a [skill](skills.md) is probably enough
- you need nested delegation: subagents cannot spawn other subagents

## Authoring Best Practices

### Bound the task narrowly

Each subagent should answer one question: "what bounded work gets its own context?". A worker that scans logs *and* edits code *and* writes tests has fuzzy routing and weak constraints. Split it.

Do not name subagents after org-chart roles (`data-engineer`, `test-engineer`). Name them after the delegation unit (`ingestion-explorer`, `diff-scanner`, `coverage-gap-finder`). Domain rules belong in `agent-kit/agent-rules/` (`RULES.md` index), not in persona prose.

### Restrict tools intentionally

Inheriting every tool by default is convenient and dangerous. A reviewer with `Write` quietly becomes an editor. Use `tools:` as an explicit allowlist for sensitive roles, or `disallowedTools:` to subtract from the inherited set.

```yaml
# Read-only research
tools: Read, Grep, Glob, Bash

# Or inherit everything except writes
disallowedTools: Write, Edit
```

### Pick the model on purpose

- **Haiku**: fast and cheap — good for high-volume exploration or routine checks
- **Sonnet**: balanced default
- **Opus**: deep reasoning, complex multi-step work
- **inherit**: when the subagent should track the parent session

Routing a noisy "find all usages and summarize" subagent to Haiku can cut cost dramatically without losing quality.

### Write the description for routing

The parent agent routes based on `description`. Specifics beat platitudes.

```yaml
# Bad — no trigger, no boundary
description: Helps with code

# Bad — persona label, not a delegation trigger
description: Acts as a senior data engineer for pipeline work

# Good — names the trigger, output, and constraints
description: Scans the current diff for correctness and security issues. Returns findings only — never edits files. Use after substantive edits.
```

The phrase "use proactively" is a known signal that increases automatic delegation.

### Context: fresh vs forked

A subagent starts with a **fresh context window** by default — it does not see conversation history, files the parent already read, or skills already invoked. `AGENTS.md`, `.cursor/rules/`, and project memory still load. When you delegate manually, include everything the worker needs in the task message: scope, files, constraints, and expected output shape. Forked subagents are the alternative: they inherit the parent context instead of starting clean.

## Common Patterns

| Pattern | When to use |
|---|---|
| **Isolate high-volume output** | Test runs, log scans, doc fetching. Verbose work stays in the subagent; only the summary returns. |
| **Parallel research** | Independent investigations on different modules dispatched simultaneously. |
| **Chain subagents** | `reviewer → optimizer`: each owns a stage, the parent orchestrates. |
| **Restrict tools** | Read-only researcher, no-edit reviewer, Bash-only DB reader with a `PreToolUse` hook. |
| **Preload skills** | Inject domain knowledge at startup with `skills: [api-conventions]` instead of waiting for discovery. |

## Setting Up In Cursor

Cursor added subagents in version 2.4 (January 2026). Subagents live in markdown files with YAML frontmatter. Discovered paths:

| Scope | Path |
|---|---|
| Project | `.cursor/agents/` |
| Personal | `~/.cursor/agents/` |
| Plugin | `<plugin>/agents/<name>.md` |

Frontmatter fields include `name`, `description`, `model` (`inherit` or an ID like `composer-2`), `readonly: true` for no-write roles, and `is_background: true` to run without blocking the parent.

```markdown
---
name: verifier
description: Confirms an auth flow end-to-end without modifying code.
model: inherit
readonly: true
---

You are a verifier. Read the touched files and report whether the flow
described actually works. Never edit anything.
```

Invocation:
- automatic — the parent Agent delegates based on `description` and task context
- explicit slash — `/verifier confirm the auth flow is complete`
- natural mention — "Use the verifier subagent to confirm the auth flow"

The parent dispatches subagents via parallel Task tool calls, so independent investigations run simultaneously. Each subagent starts with a clean context — include scope, files, constraints, and the expected output shape in the delegation message.

## Anti-patterns

- **persona catalogs** — `data-engineer`, `data-scientist`, `code-reviewer` as if the model needs a job title to do the work; use shared rules and skills instead
- vague descriptions that won't route (`description: Helps with code`)
- one giant subagent spanning unrelated jobs
- inheriting all tools when the task doesn't need them — a read-only scanner with `Write` is actually an editor
- spawning many parallel subagents that each return a long summary; the verbosity comes back into the main context
- treating subagents like skills — if the value is a repeatable workflow, write a skill
- expecting nested delegation: subagents cannot spawn other subagents
- using a subagent for tasks that need iterative back-and-forth with the user

## Pre-flight Checklist

Before shipping a subagent:

- [ ] `description` is specific, third person, names the trigger (with "use proactively" if you want auto-delegation)
- [ ] Tools are an explicit allowlist for sensitive roles
- [ ] Model chosen on purpose (cheap for noisy work, default for balance, expensive for deep reasoning)
- [ ] System prompt states the bounded task, output shape, and what the subagent must not do
- [ ] Tested both via `@-mention` and via natural-language delegation
- [ ] No assumption of nested delegation

## Subagents In This Framework

This metarepo does **not** ship a catalog of job-title subagents. Domain expertise lives in:

- the general model
- `agent-kit/agent-rules/RULES.md` — rule index; `agent-kit/agent-rules/` — engineering and collaboration rules
- `docs/` — project-specific knowledge in the consumer repo
- `skills/` — repeatable workflows

Create subagents in `.cursor/agents/` when a **task** needs an isolated context or parallel execution — for example, scanning three modules at once, running a read-only security pass, or exploring a noisy log file without polluting the parent chat.

The optional `subagents/` folder here is for team-specific templates, not predefined personas. See [subagents/README.md](../../subagents/README.md).

## Where To Look Next

- Optional subagent templates: [subagents/README.md](../../subagents/README.md)
- Reusable workflows: [skills.md](skills.md)
- Context strategy: [context-engineering.md](context-engineering.md)
- The lifecycle subagents support: [../onboarding/lifecycle.md](../onboarding/lifecycle.md)

## References

- Anthropic — [Create custom subagents (Claude Code)](https://code.claude.com/docs/en/sub-agents)
- Anthropic — [How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system) (engineering blog)
- Anthropic — [Agent Teams](https://code.claude.com/docs/en/agent-teams) (sustained parallelism beyond a single session)
- Anthropic — [Permission modes](https://code.claude.com/docs/en/permission-modes)
- Cursor — [Subagents](https://cursor.com/docs/subagents)
- Cursor — [Agent best practices](https://cursor.com/blog/agent-best-practices)
