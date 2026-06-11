# How To Use Cursor

This guide covers the minimum Cursor setup and habits for safe day-to-day development: modes, models, context, rules, permissions, and team defaults.

For workflow depth, use [lifecycle.md](lifecycle.md). For context strategy, use [managing-context.md](managing-context.md).

## Quick Setup

Start here before asking the agent to change code.

1. Open `Cursor Settings` with `Ctrl+Shift+J`.
2. Import VS Code settings from `General > Account > VS Code Import`.
3. Set your default model in `Cursor Settings > Models`.
4. Enable `Privacy Mode` if your team requires prompts and code context not to be stored or trained on by model providers.
5. Let `Codebase Indexing` finish after opening a repo.
6. Set `Cursor Settings > Agents > Run Mode` to `Auto-review` or stricter.
7. Review keyboard shortcuts with `Preferences: Open Keyboard Shortcuts`.

Cursor can import VS Code extensions, themes, settings, and keybindings. Keep editor setup boring; spend the attention on model choice, privacy, indexing, and command permissions.

## Core Controls

| Control | Use |
| --- | --- |
| `Ctrl+I` | Open or toggle the Agent panel. |
| `Ctrl+L` | Open chat or send the current selection to chat. |
| `Ctrl+K` | Inline edit selected code, or open the terminal prompt bar when focus is in a terminal. |
| `Ctrl+/` | Open the model picker. |
| `Shift+Tab` | Switch between modes. |
| `Ctrl+.` | Open the mode menu. |
| `Ctrl+T` | Open a new chat tab. |
| `Tab` | Accept a completion suggestion. |
| `@` | Add files, folders, docs, terminals, diffs, branches, commits, browser context, or past chats. |
| `/` | Use available slash commands. Check the command menu before relying on a command name. |

Use `@file` or `@folder` when the source matters. Use `@diff` for reviews. Use terminal context only when the output is relevant.

## Modes

| Mode | What It Does | Use When |
| --- | --- | --- |
| `Ask` | Reads and explains. It should not edit files. | You are learning a repo, reviewing errors, or asking for architecture context. |
| `Agent` | Edits files and can run approved tools or commands. | The task is scoped and you know what should change. |
| `Plan` | Investigates and writes a plan before implementation. | The task is broad, risky, ambiguous, or multi-file. |
| `Debug` | Troubleshoots with runtime evidence. | A bug needs logs, repro steps, tests, or terminal output to diagnose correctly. |

Good default:

- Start in `Ask` in unfamiliar code.
- Use `Plan` before broad or risky work.
- Use `Agent` for scoped implementation.
- Use `Debug` when the problem is evidence-driven.
- Start a new chat when the task changes.

## Models And Privacy

Choose models deliberately.

- Use the model picker or `Ctrl+/` for one-off changes.
- Set the default model in `Cursor Settings > Models`.
- Use stronger models for specs, architecture, security-sensitive work, and hard debugging.
- Use faster or cheaper models for mechanical edits, summaries, and documentation polish.
- Use `Max Mode` only when a larger context window is worth the extra usage.

Cursor's current usage language includes the `Auto` and `Composer` pool, API pool, premium routing, and `Max Mode`. The exact model list changes often, so prefer Cursor Settings over hard-coded team docs.

If you bring your own API key, configure it in `Cursor Settings > Models`. BYOK applies to chat models, not necessarily to every Cursor feature such as Tab completion. Cursor's zero data retention guarantees for hosted models do not automatically apply to requests sent through your own provider key.

Use `Privacy Mode` for work where prompts, code context, or chat content should not be stored or used for training by model providers. Teams can enforce this centrally.

## Context And Indexing

Cursor builds context from visible chat history, attached files, indexed code, rules, tools, skills, MCP servers, subagents, and summaries. The context ring near the prompt shows how full the current context window is and what is consuming it.

Keep context small and relevant:

- Mention exact files before folders.
- Attach folders only when the whole area matters.
- Prefer `@diff` for code review.
- Remove stale references before changing tasks.
- Use a new chat when the previous task no longer matters.

`Codebase Indexing` powers semantic code search and repo-aware answers. It runs automatically when a repo opens and syncs periodically. Check indexing status or trigger a reindex from `Cursor Settings > Indexing` if search feels stale. On large repos, semantic search is unavailable until indexing reaches roughly 80%; within a team, Cursor can reuse a teammate's index to cut time-to-first-query from hours to seconds. See [Secure indexing of large codebases](https://cursor.com/es/blog/secure-codebase-indexing) for how Merkle trees, simhash matching, and content proofs keep that reuse safe.

Use `.cursorignore` and `.gitignore` to keep generated, private, or noisy files out of Cursor indexing and normal context. Use `.cursorindexingignore` when a file should be excluded from search indexing but remain available to other AI features. Do not treat ignore files as a security boundary: terminal commands, package scripts, and MCP tools can still access files outside Cursor's indexing controls.

For handoffs, compaction, and durable context rules, see [managing-context.md](managing-context.md).

## Rules, Skills, Subagents, MCP

Use the smallest mechanism that solves the problem.

| Mechanism | Lives In | Use For |
| --- | --- | --- |
| Project Rules | `.cursor/rules/*.mdc` | Persistent repo instructions for Agent, Ask, Plan, and Debug. |
| Cursor Plugins | `plugins/*/` | Packaged rules, skills, hooks, and scripts shared across repos. |
| User Rules | Cursor user settings | Personal preferences that should follow you across repos. |
| Team Rules | Team configuration | Organization-wide rules and safety defaults. |
| `AGENTS.md` | Repo root or nested directories | Plain-markdown agent guidance for the repo. |
| Agent Skills | `.cursor/skills/`, `.agents/skills/`, plugin `skills/`, or user-level equivalents | Reusable workflows with instructions and supporting files. |
| Subagents | `.cursor/agents/` or user-level equivalents | Specialist assistants with their own context windows. |
| MCP | `.cursor/mcp.json` or `~/.cursor/mcp.json` | External tools and data sources through the Model Context Protocol. |

Project Rules must use `.mdc`; plain `.md` files inside `.cursor/rules` are ignored. Keep each rule short and specific. Use `alwaysApply` for rules that should always load, `globs` for file-scoped rules, and `description` to help Cursor decide when a rule is relevant.

Rule precedence is team, then project, then user. Rules do not apply to Cursor Tab, and user rules do not apply to Inline Edit.

MCP servers can expose tools, prompts, resources, roots, elicitation, and MCP apps. Keep MCP enabled only when useful for the current work because tool schemas and server descriptions also consume context.

## Permissions And Run Mode

Run Mode controls shell, MCP, and fetch tool execution.

Open:

```text
Cursor Settings > Agents > Run Mode
```

| Run Mode | Meaning | Recommendation |
| --- | --- | --- |
| `Auto-review` | Cursor checks allowlists, sandbox support, and a command classifier before deciding whether to run or ask. | Good default for normal work. |
| `Allowlist` | Only allowlisted commands run automatically. | Good when you want stricter control. |
| `Allowlist (with Sandbox)` | Uses an allowlist plus sandbox where available. | Best conservative option when supported. |
| `Run Everything` | Runs commands automatically. | Avoid outside disposable sandboxes. |

Recommended protections:

- Enable file-deletion protection.
- Enable dotfile protection.
- Enable external-file protection.
- Enable browser protection.
- Require approval for package installs, migrations, deploys, releases, and publishing.
- Keep Git history-changing commands manual until the team explicitly changes this policy.

`Auto-review` is a convenience layer, not a security boundary. On Windows, sandbox support requires WSL2; otherwise Cursor may fall back to asking for approval.

## Team Safety Policy

This repository ships the safety policy through the Cursor plugin at `plugins/test-plugin/`:

| Component | Path | Role |
| --- | --- | --- |
| Rule | `plugins/test-plugin/rules/team-safety-policy.mdc` | Team instructions loaded by the plugin. |
| Hook registration | `plugins/test-plugin/hooks/hooks.json` | Plugin hook manifest; discovered automatically when the plugin is installed. |
| Hook script | `plugins/test-plugin/scripts/team-safety-policy.js` | Programmatic enforcement for shell commands (publish, deletion, subshells). |

Per the [Cursor Plugins reference](https://cursor.com/docs/reference/plugins), hooks are a first-class plugin component. Cursor discovers them at `hooks/hooks.json` inside the plugin directory and runs hook scripts relative to the plugin root. No workspace-level `.cursor/hooks.json` is required when the plugin is installed from the team marketplace or loaded locally.

To test the plugin before publishing, symlink it into `~/.cursor/plugins/local/test-plugin` and run **Developer: Reload Window**. Hook command paths in `hooks/hooks.json` are relative to the plugin root (for example, `./scripts/team-safety-policy.js`).

The policy is:

- Cursor agents must never publish code to a remote. Do not run `git push`, `npm publish`, `docker push`, or similar commands. A human must always publish.
- Cursor agents must not run commands through subshells or interpreters (`bash -c`, `node -e`, `python -c`, etc.) without explicit human approval.
- Cursor agents should prefer reading the current contents of a file before editing it.
- Cursor agents must not modify files unless the user explicitly requests a change or confirms the plan.
- Destructive shell commands are gated by hooks that request human approval automatically. Agents should not ask for approval a second time when Cursor already shows an approval prompt.
- If a user request conflicts with the policy, the agent must stop and ask for clarification.

Hook enforcement details:

- **Publish commands** (`git push`, `npm publish`, `docker push`, `gh pr merge`, etc.) are blocked.
- **Deletion commands** (`rm`, `del`, `Remove-Item`, etc.) require human approval.
- **Indirect execution** (`bash -c`, `node -e`, `python -c`, etc.) requires human approval.
- **File edits** are not gated by plugin hooks. Cursor `Run Mode` (for example `Auto-review`) and team rules control when agents may change files. Reading files is unrestricted.

Note: `preToolUse` hooks cannot reliably gate file edits today. Cursor documents that `permission: "ask"` is not enforced for `preToolUse`; only `deny` is reliable. Do not use a `preToolUse` hook expecting approval prompts on `Write` or `StrReplace`.

For team-wide enforcement outside this repository, copy the same policy into `Cursor Dashboard > Team Rules`. Keep the plugin files in the repo as the reviewable source of truth, and use the dashboard rule to make the behavior consistent across workspaces.

## Team Defaults

Use this as the safe baseline for this repo:

- Import VS Code settings first.
- Keep `Privacy Mode` on when handling proprietary code or customer data.
- Use `Auto-review` or `Allowlist (with Sandbox)`.
- Keep allowlists narrow.
- Let indexing finish before broad codebase questions.
- Use `Ask` for exploration, `Plan` for risky changes, `Agent` for scoped edits, and `Debug` for evidence-heavy bugs.
- Keep `.cursor/rules/*.mdc` and plugin rules short and specific.
- In this metarepo, use the Cursor plugin at `plugins/test-plugin/` for shared team behavior:
  - `rules/entrypoint.mdc` points Cursor to `agent-kit/AGENTS.md`; do not duplicate the kit rules there.
  - `rules/team-safety-policy.mdc`, `hooks/hooks.json`, and `scripts/team-safety-policy.js` define the team safety policy.
  - `skills/` holds reusable agent workflows such as `grill-me`.
- Prefer `AGENTS.md` for simple, portable repo instructions.
- Enable MCP servers only when they are needed.
- Keep Git, releases, deployments, and package publishing as human-controlled steps.

Typical implementation prompt:

```text
Use @src/payments/session.ts and @tests/payments/session.test.ts.
Fix only token refresh behavior.
Do not edit unrelated files.
Before editing, explain the files you will touch.
After editing, list changed files, verification, and remaining risk.
```

Typical review prompt:

```text
Review @diff for bugs, missing tests, and risky behavior.
Prioritize findings.
Do not rewrite code unless I ask.
```

Avoid vague requests such as "fix everything", "look at the whole repo", or "make it better". Give the agent scope, evidence, and stopping conditions.

## References

Official Cursor docs:

- [Agent overview](https://cursor.com/docs/agent/overview)
- [Plan Mode](https://cursor.com/docs/agent/plan-mode)
- [Prompting and context](https://cursor.com/docs/agent/prompting)
- [Semantic and agentic search](https://cursor.com/docs/agent/tools/search)
- [Secure indexing of large codebases](https://cursor.com/es/blog/secure-codebase-indexing) (research blog — Merkle-tree sync, team index reuse, content proofs)
- [Terminal tools and Run Mode](https://cursor.com/docs/agent/tools/terminal)
- [Permissions reference](https://cursor.com/docs/reference/permissions)
- [Rules](https://cursor.com/docs/rules)
- [MCP](https://cursor.com/docs/mcp)
- [Models and pricing](https://cursor.com/docs/models-and-pricing)
- [Ignore files](https://cursor.com/docs/reference/ignore-file)
- [Keyboard shortcuts](https://cursor.com/docs/reference/keyboard-shortcuts)
- [Migrate from VS Code](https://cursor.com/docs/configuration/migrations/vscode)
