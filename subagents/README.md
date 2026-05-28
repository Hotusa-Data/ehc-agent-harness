# Subagents

This folder contains the subagent catalog used by the metarepo.

For the conceptual guide, see [guides/theory/subagents.md](../guides/theory/subagents.md).

## Purpose

`subagents/` contains specialist role definitions that can be used by an orchestrating agent when a task needs domain-specific judgment.

These roles are narrower than the main agent and should build on shared rules from `agent-kit/agent-rules/`.

## Current Catalog

### Coding Agents

| Subagent | Path | Typical use |
|---|---|---|
| `data-engineer` | [coding-agents/data-engineer.md](./coding-agents/data-engineer.md) | Pipelines, ingestion, ETL, transformation |
| `data-scientist` | [coding-agents/data-scientist.md](./coding-agents/data-scientist.md) | Features, models, scoring, notebook-heavy logic |
| `data-analyst` | [coding-agents/data-analyst.md](./coding-agents/data-analyst.md) | Metrics, dashboards, analytical queries, reporting logic |

### Review Agents

| Subagent | Path | Typical use |
|---|---|---|
| `code-reviewer` | [review-agents/code-reviewer.md](./review-agents/code-reviewer.md) | Thorough code review before merge (correctness, architecture, security, performance) |
| `test-engineer` | [review-agents/test-engineer.md](./review-agents/test-engineer.md) | Test strategy, writing tests, coverage gap analysis |

## Maintenance Rules

- keep role boundaries sharp
- avoid duplicating generic engineering principles here
- make routing descriptions specific
- keep this README focused on catalog and navigation
- keep shared theory in `guides/`, not here
