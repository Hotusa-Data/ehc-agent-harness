---
name: handoff
phase: cross-cutting
description: |
  Compact the current conversation into a handoff document so another agent can pick up the work. Saves the doc to the user's OS temporary directory, redacts sensitive data, references external artifacts by path instead of duplicating them, and includes a "suggested skills" section. Use when a session is ending and the next agent needs to continue with full context.
allowed-tools:
  - Write
  - Read
argument-hint: "What will the next session be used for?"
metadata:
  owner: Ignacio Freire
  last_reviewed: "2026-05-27"
  skill-version: "1.0.0"
---

Write a handoff document summarising the current conversation so a fresh agent can continue the work. Save to the temporary directory of the user's OS - not the current workspace.

Include a "suggested skills" section in the document, which suggests skills that the agent should invoke.

Do not duplicate content already captured in other artifacts (PRDs, plans, ADRs, issues, commits, diffs). Reference them by path or URL instead.

Redact any sensitive information, such as API keys, passwords, or personally identifiable information.

If the user passed arguments, treat them as a description of what the next session will focus on and tailor the doc accordingly.

---

## Related skills

- [`context-update`](../context-update/SKILL.md) — closes the loop for the **same** project across sessions; `handoff` is the cross-agent equivalent within a single session.
- [`context-load`](../context-load/SKILL.md) — the next agent should run this first; the handoff doc's "suggested skills" section typically starts with it.
