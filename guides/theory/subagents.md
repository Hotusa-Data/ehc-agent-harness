# Subagents

A practical introduction to Subagents for developers — what they are, when they beat a skill or a plain prompt, and how to set them up in Claude Code and Cursor.

## TL;DR

A subagent is a specialized AI assistant that handles a bounded task in its own context window, with its own system prompt, model, and tool restrictions. The parent agent delegates to it, the subagent works, and only the summary returns. Use one when a side task would flood your main conversation, or when you keep spawning the same kind of worker.

```markdown
---
name: code-reviewer
description: Reviews recent code changes for quality, security and best practices. Use proactively after edits.
tools: Read, Grep, Glob, Bash
model: sonnet
---

You are a senior code reviewer. Analyze the diff and return specific,
actionable findings — never edit files yourself.
```

## Why Subagents Exist

The main conversation is a public good: every search result, log dump, and exploration trace competes for the same context window. Subagents move that work off-stage. The parent gets back a summary; the verbose work stays inside the subagent.

What you get:
- **Context preservation** — exploration and high-volume output stay isolated
- **Constraint enforcement** — restrict tools, permissions, or models per role
- **Reusability** — the same worker definition runs across sessions and projects
- **Cost control** — route cheap, repetitive work to Haiku without touching the main model
- **Specialization** — a focused system prompt makes the worker better at one thing

## Subagent vs Skill vs Prompt vs Tool

| Concept | Main question | Role |
|---|---|---|
| Tool | What action can I take? | Single capability (run a script, call an API) |
| Prompt | What do I want right now? | One-off instruction |
| Skill | How should this kind of task be done? | Reusable workflow + context |
| Subagent | Who should handle this task? | Specialist role with its own context |

Rules of thumb:
- repeatable workflow → **skill** (see [skills.md](skills.md))
- specialist judgment → **subagent**
- single atomic action → **tool**
- one-time ask → **prompt**

A subagent can use one or more skills — they compose. Claude Code ships built-in subagents (Explore, Plan, general-purpose, plus a couple of helper agents); the official docs keep the current list.

## Anatomy Of A Subagent

A subagent is a markdown file with YAML frontmatter (config) followed by the system prompt (body).

```markdown
---
name: code-reviewer
description: Reviews recent code changes for quality, security and best practices. Use proactively after edits.
tools: Read, Grep, Glob, Bash
model: sonnet
---

You are a senior code reviewer. When invoked, analyze the diff and return
specific, actionable findings — never edit files yourself.
```

Frontmatter rules:
- `name`: lowercase letters and hyphens. Unique within its scope.
- `description`: tells the parent agent **when to delegate**. Write in third person, name the trigger, add "use proactively" if you want automatic delegation.
- Body: becomes the subagent's system prompt — it *replaces* the default Claude Code prompt rather than extending it. Be explicit about role, tone, and what the subagent must not do.

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

### Bound the role narrowly

Each subagent should answer one question: "who owns this?". A subagent that does data engineering *and* code review *and* security has fuzzy routing and weak constraints. Split it.

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
# Bad — Claude won't know when to fire it
description: Helps with code

# Good — names the trigger and the role
description: Reviews recent code changes for quality, security and best practices. Use proactively after edits.
```

The phrase "use proactively" is a known signal that increases automatic delegation.

### Context: fresh vs forked

A subagent starts with a **fresh context window** by default — it does not see conversation history, files Claude already read, or skills already invoked. `CLAUDE.md` and project memory still load (except for the built-in `Explore` and `Plan`). When you delegate manually, write the task message as if briefing a smart colleague who just walked into the room. Forked subagents are the alternative: they inherit the parent context instead of starting clean.

### Memory and isolation (advanced)

Two opt-in features worth knowing about:
- `memory: user|project|local` gives the subagent a persistent directory it reads and writes across sessions — useful for building institutional knowledge.
- `isolation: worktree` runs the subagent in a temporary git worktree, giving it an isolated copy of the repo — useful for risky changes that shouldn't touch the parent branch.

Both are detailed in the Anthropic docs linked at the bottom.

## Common Patterns

| Pattern | When to use |
|---|---|
| **Isolate high-volume output** | Test runs, log scans, doc fetching. Verbose work stays in the subagent; only the summary returns. |
| **Parallel research** | Independent investigations on different modules dispatched simultaneously. |
| **Chain subagents** | `reviewer → optimizer`: each owns a stage, the parent orchestrates. |
| **Restrict tools** | Read-only researcher, no-edit reviewer, Bash-only DB reader with a `PreToolUse` hook. |
| **Preload skills** | Inject domain knowledge at startup with `skills: [api-conventions]` instead of waiting for discovery. |

## Setting Up In Claude Code

Subagents live in markdown files. Five scopes, project < personal in everyday use:

| Scope | Path | Precedence |
|---|---|---|
| Managed (org) | `.claude/agents/` in managed settings | 1 (highest) |
| CLI session | `--agents '{...}'` JSON flag | 2 |
| Project | `.claude/agents/<name>.md` | 3 |
| Personal | `~/.claude/agents/<name>.md` | 4 |
| Plugin | `<plugin>/agents/<name>.md` | 5 |

Easiest path to create one: run `/agents` in Claude Code and let the wizard generate the file. Higher scopes win when names collide. Files added on disk need a session restart to load; subagents created through `/agents` take effect immediately.

**Invocation patterns**

| Trigger | What happens |
|---|---|
| Natural language ("use the code-reviewer to check this") | Claude decides whether to delegate |
| `@code-reviewer (agent)` | Forces that subagent for one turn |
| `claude --agent code-reviewer` | Whole session adopts the subagent's prompt, tools, and model |
| `"agent": "code-reviewer"` in `.claude/settings.json` | Default subagent for every session in the project |

## Setting Up In Cursor

Cursor added subagents in version 2.4 (January 2026) and follows the same open-standard layout — your existing `.claude/agents/` files are picked up natively. Discovered paths:

| Scope | Path |
|---|---|
| Project | `.cursor/agents/` (also reads `.claude/agents/` and `.codex/agents/`) |
| Personal | `~/.cursor/agents/` (also `~/.claude/agents/`, `~/.codex/agents/`) |

Frontmatter is a subset of Claude Code's — `name`, `description`, `model` (`inherit` or an ID like `composer-2`), `readonly: true` for no-write roles, and `is_background: true` to run without blocking the parent.

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

The parent dispatches subagents via parallel Task tool calls, so independent investigations run simultaneously. Each subagent starts with a clean context, so brief it like a colleague who just walked in.

## Anti-patterns

- vague descriptions that won't route (`description: Helps with code`)
- one giant subagent spanning unrelated jobs
- inheriting all tools when the role doesn't need them — a "reviewer" with `Write` is actually an editor
- spawning many parallel subagents that each return a long summary; the verbosity comes back into the main context
- treating subagents like skills — if there's no specialist role boundary, a skill is enough
- expecting nested delegation: subagents cannot spawn other subagents
- using a subagent for tasks that need iterative back-and-forth with the user

## Pre-flight Checklist

Before shipping a subagent:

- [ ] `description` is specific, third person, names the trigger (with "use proactively" if you want auto-delegation)
- [ ] Tools are an explicit allowlist for sensitive roles
- [ ] Model chosen on purpose (cheap for noisy work, default for balance, expensive for deep reasoning)
- [ ] System prompt states the role *and* what the subagent must not do
- [ ] Tested both via `@-mention` and via natural-language delegation
- [ ] No assumption of nested delegation

## Subagents In This Framework

This repo uses subagents mainly for role-specialized coding work. Current examples live under `subagents/coding-agents/` and cover roles such as:

- data engineer
- data scientist
- data analyst

They should build on shared rules from `agent-kit/agent-rules/` rather than duplicating generic engineering principles.

## Where To Look Next

- Subagent catalog in this repo: [subagents/README.md](../../subagents/README.md)
- Reusable workflows: [skills.md](skills.md)
- The lifecycle these roles operate in: [../onboarding/lifecycle.md](../onboarding/lifecycle.md)

## References

- Anthropic — [Create custom subagents (Claude Code)](https://code.claude.com/docs/en/sub-agents)
- Anthropic — [How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system) (engineering blog)
- Anthropic — [Agent Teams](https://code.claude.com/docs/en/agent-teams) (sustained parallelism beyond a single session)
- Anthropic — [Permission modes](https://code.claude.com/docs/en/permission-modes)
- Cursor — [Subagents](https://cursor.com/docs/subagents)
- Cursor — [Agent best practices](https://cursor.com/blog/agent-best-practices)
