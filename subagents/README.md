# Subagents

This folder is reserved for project-specific subagent definitions that developers configure in their IDE.

For the conceptual guide — what subagents are for, when to use them, and how to author them — see [guides/theory/subagents.md](../guides/theory/subagents.md).

> **WIP** — We are still defining and creating subagents for this framework. This folder is intentionally empty for now; expect templates and examples to land here as patterns emerge from real use.

## Purpose

Subagents are **context tools**, not persona catalogs. Use them to delegate bounded work into an isolated context window — with its own prompt, tools, and model — so the parent conversation stays lean and independent tasks can run in parallel.

This metarepo does not ship predefined role profiles (data engineer, code reviewer, etc.). Domain expertise already lives in the general model plus `agent-kit/agent-rules/` and `docs/`. Create subagents when a **task** needs its own context, not when you want a synthetic colleague.

## Where to put definitions

| Scope | Path |
|---|---|
| Project | `.cursor/agents/` |
| Personal | `~/.cursor/agents/` |

Definitions here are optional reference material for teams that want shared, versioned subagent templates. Most teams define subagents directly in the IDE paths above.

## Maintenance rules

- name subagents after the **task or context boundary**, not a job title
- keep each definition narrowly scoped to one delegation unit
- do not duplicate rules from `agent-kit/agent-rules/` — point workers at shared rules instead
- keep routing `description` specific so the parent knows when to delegate
- keep shared theory in `guides/`, not here
