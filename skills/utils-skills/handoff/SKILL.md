---
name: handoff
phase: cross-cutting
description: |
  Compact the current conversation into a handoff document so another agent can pick up the work. Saves the doc under `.local-context/` in the workspace (gitignored), redacts sensitive data, references external artifacts by path instead of duplicating them, and includes a "suggested skills" section. Use when a session is ending and the next agent needs to continue with full context.
allowed-tools:
  - Write
  - Read
argument-hint: "What will the next session be used for?"
metadata:
  owner: Ignacio Freire
  last_reviewed: "2026-06-16"
  skill-version: "1.1.0"
---

Write a handoff document summarising the current conversation so a fresh agent can continue the work. Save to `.local-context/` in the **current workspace** — for example `.local-context/handoff-YYYY-MM-DD.md`. This directory is gitignored and must never be committed.

Include a "suggested skills" section in the document, which suggests skills that the agent should invoke.

Do not duplicate content already captured in other artifacts (PRDs, plans, specs, issues, commits, diffs). Reference them by path or URL instead.

Redact any sensitive information, such as API keys, passwords, or personally identifiable information.

If the user passed arguments, treat them as a description of what the next session will focus on and tailor the doc accordingly.

---

## When to use

- A session is ending and another agent (or a fresh chat) must continue the work.
- Context would be lost without a compact summary of decisions, blockers, and next steps.
- The user explicitly asks for a handoff document.

## When NOT to use

- At session start — the next agent should run [`context-load`](../context-load/SKILL.md) first.
- When [`context-update`](../context-update/SKILL.md) can reconcile durable docs in the same project — handoff complements, not replaces, repo artifacts.
- To duplicate content already in specs, plans, or commits — reference by path instead.

---

## Related skills

- [`context-update`](../context-update/SKILL.md) — closes the loop for the **same** project across sessions; `handoff` is the cross-agent equivalent within a single session.
- [`context-load`](../context-load/SKILL.md) — the next agent should run this first; the handoff doc's "suggested skills" section typically starts with it.
