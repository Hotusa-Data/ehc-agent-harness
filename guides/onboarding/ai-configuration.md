# Working With AI

This guide explains how to set up and use AI development tools in this framework.

It is written for a developer onboarding into a repo that may use Codex, Claude Code, Cursor, or a combination of them. The goal is practical: configure the tools, understand the differences, point agents at the right context, choose models and modes, and verify that the agent is working with the right information.

For the delivery workflow itself, see [lifecycle.md](lifecycle.md). For context theory, see [../theory/context-engineering.md](../theory/context-engineering.md).

## Quickstart

If you are configuring a new repository, start here.

| Step | What to do | Why it matters |
| --- | --- | --- |
| 1 | Add a short root instruction file: `AGENTS.md`, `CLAUDE.md`, or Cursor rules. | Gives the agent stable repo behavior without bloating every chat. |
| 2 | Add durable project context under `docs/`. | Keeps architecture, glossary, domain facts, and decisions outside chat memory. |
| 3 | Choose the tool-specific config surface. | Codex, Claude Code, and Cursor store settings differently. |
| 4 | Set conservative permissions first. | Let the agent read widely, edit locally, and ask before risky commands. |
| 5 | Choose a default model and reasoning level. | Avoid overpaying for mechanical tasks and underpowering ambiguous work. |
| 6 | Add skills or subagents only when a workflow repeats. | Do not turn every prompt into infrastructure too early. |
| 7 | Verify what context is loaded. | A confident answer from the wrong files is still wrong. |

Recommended first prompt after setup:

```text
Do not edit yet. Read the active repo instructions and the relevant docs.
Then list:
- instruction files you loaded
- project docs you loaded
- active model and reasoning setting, if visible
- permission or approval mode, if visible
- assumptions before doing work
```

## Choosing A Tool Surface

The tools overlap, but they are optimized for slightly different working styles.

| Tool | Best fit | Typical entry point | Main config surface |
| --- | --- | --- | --- |
| Codex | Terminal-first and repo-agent workflows with explicit sandboxing, skills, plugins, MCP, and subagents. | `codex` CLI or Codex app surfaces | `~/.codex/config.toml`, `AGENTS.md`, `.agents/skills/`, `.codex/agents/` |
| Claude Code | Terminal-first workflows with strong permission controls, plan mode, goals, skills, and subagents. | `claude` CLI | `~/.claude/settings.json`, `.claude/settings.json`, `CLAUDE.md` or `AGENTS.md`, `.claude/skills/`, `.claude/agents/` |
| Cursor | IDE-first workflows where file tabs, rules, composer/agent mode, and project context are central. | Cursor IDE or `cursor-agent` | `.cursor/rules/`, `AGENTS.md`, Cursor settings, `.cursor/skills/` or `.agents/skills/`, `.cursor/agents/` |

Use one shared repo convention when possible. A simple `AGENTS.md` plus durable docs under `docs/` is a good minimum that several tools can understand or be instructed to load.

## Core Concepts

Think of AI tooling as layers. Each layer should have one job.

| Concept | What it is for | Where it usually lives |
| --- | --- | --- |
| Instructions | Stable guidance the agent should always consider. | `AGENTS.md`, `CLAUDE.md`, `.cursor/rules/` |
| Project context | Durable facts about the product, architecture, features in scope, and vocabulary. | `docs/architecture.md`, `docs/context/project.md`, `docs/glossary.md` |
| Skills | Repeatable workflows loaded on demand. | `SKILL.md`, `.agents/skills/`, `.claude/skills/`, `.cursor/skills/` or `.agents/skills/` |
| Subagents | Specialist workers with their own role, model, and context. | `.codex/agents/`, `.claude/agents/`, `.cursor/agents/` |
| Plugins | Shareable bundles of skills, agents, hooks, MCP servers, or app integrations. | `.codex-plugin/plugin.json`, `.claude-plugin/plugin.json` |
| MCP / tools | Connections to external systems such as GitHub, databases, docs, Slack, or Figma. | MCP config, tool settings, plugin config |
| Permissions | Boundaries for reads, edits, shell commands, network access, and autonomous action. | Tool settings, session flags, allowlists, denylists |
| Plan mode | A reviewable planning phase before edits. | `/plan`, plan mode UI, explicit planning prompts, `agent-kit/skeletons/_design.md` |
| Goals | Persistent objectives or checklists for bounded loops. | `/goal`, prompt templates, skills, subagents |
| Model settings | Default model and temporary model overrides. | `/model`, `--model`, `model`, provider settings |
| Reasoning settings | How much extra thinking the model should spend. | `/effort`, `--effort`, `model_reasoning_effort`, thinking mode |

Rules of thumb:

- Put durable repository behavior in instructions.
- Put durable project truth in `docs/`.
- Put repeatable procedures in skills.
- Put specialist judgment in subagents.
- Put reusable bundles in plugins.
- Put external system access in MCP or tool config.

## Recommended Repo Baseline

Every consumer repository should start with a small, explicit structure.

```text
repo-root/
|-- AGENTS.md
|-- agent-kit/
|   |-- agent-rules/
|   `-- skeletons/
`-- docs/
    |-- architecture.md
    |-- database.md
    |-- glossary.md
    |-- repo-guide.md
    |-- docs-guide.md
    |-- context/
    |   `-- project.md
    `-- features/
        `-- <feature>/
            |-- requirements.md
            |-- design.md
            |-- tasks.md
            `-- CHANGELOG.md
```

`AGENTS.md` should stay short. It should tell the agent:

- how to work in this repository
- which project docs to load first
- which commands are safe and expected
- which decisions require human confirmation
- where feature docs, tests, and durable docs live

Do not put the whole handbook into the root instruction file. Large procedures should move into skills. Role-specific behavior should move into subagents. Long project truth should live in `docs/`, not in chat.

## Setup Matrix

Use this as the practical map when configuring tools.

| Need | Codex | Claude Code | Cursor |
| --- | --- | --- | --- |
| Root repo instructions | `AGENTS.md` | `CLAUDE.md` or `AGENTS.md` by instruction | `AGENTS.md` or `.cursor/rules/` |
| Personal settings | `~/.codex/config.toml` | `~/.claude/settings.json` | Cursor settings |
| Project settings | repo instructions, plugin config, MCP config, local conventions | `.claude/settings.json` | `.cursor/rules/`, MCP config, workspace settings |
| Local private overrides | personal config or ignored local files | `.claude/settings.local.json` | local Cursor settings |
| Skills | `.agents/skills/<name>/SKILL.md` | `.claude/skills/<name>/SKILL.md` | `.cursor/skills/` or `.agents/skills/` |
| Subagents | `.codex/agents/*.toml` | `.claude/agents/*.md` | `.cursor/agents/`, plus compatible agent dirs where supported |
| Plugins | `.codex-plugin/plugin.json` | `.claude-plugin/plugin.json` | usually rules, MCP, extensions, or workspace config |
| MCP | `codex mcp` and MCP config | `/mcp` and MCP config | `mcp.json` |
| Change model | `codex -m <model>` | `/model` or `claude --model <model>` | model picker or `cursor-agent --model <model>` |
| Change reasoning | `codex -c model_reasoning_effort=<level>` | `/effort <level>` where supported | model-dependent |
| Inspect context | Ask Codex to list loaded sources; inspect logs if enabled | `/context`, `/config`, `/cost` | Agent sidebar, explicit file mentions, ask for loaded sources |

Tool details change over time. Prefer the official docs linked in [References](#references) for exact flag names and newly supported settings.

## Configuring Codex

Use Codex when you want a terminal-first coding agent with explicit sandboxing, approvals, skills, plugins, MCP, and subagents.

Common personal config lives in:

```text
~/.codex/config.toml
```

Example:

```toml
model = "<default-coding-model>"
model_reasoning_effort = "medium"
model_reasoning_summary = "auto"
approval_policy = "on-request"
sandbox_mode = "workspace-write"
```

Use `AGENTS.md` for repo instructions. Codex can also load nested instruction files closer to the current working directory. Keep them short and specific.

Useful commands:

| Need | Command |
| --- | --- |
| Start Codex | `codex` |
| Use a model for one run | `codex -m <model>` |
| Override reasoning effort once | `codex -c model_reasoning_effort=high` |
| Work from a subdirectory | `codex --cd <path>` |
| List available models | `codex debug models` |
| Manage MCP servers | `codex mcp` |
| Open plugins | `/plugins` |
| Invoke skills explicitly | `$skill-name` or `/skills` where available |

Verify setup:

```bash
codex --ask-for-approval never "Summarize the current instructions and list the instruction files you loaded."
codex --cd services/payments --ask-for-approval never "Show which instruction files are active."
```

Use Codex plugins when you want to package skills, MCP config, hooks, or app integrations for reuse. A plugin has a required `.codex-plugin/plugin.json`; keep plugin-owned `skills/`, `hooks/`, `.mcp.json`, `.app.json`, and `assets/` at the plugin root.

## Configuring Claude Code

Use Claude Code when you want a terminal-first workflow with strong permission controls, planning, goals, skills, and subagents.

Claude Code settings are scoped. Pick the narrowest scope that matches the intent.

| Scope | Location | Use for |
| --- | --- | --- |
| User | `~/.claude/settings.json` | Personal defaults across projects |
| Project | `.claude/settings.json` | Team-shared settings committed to the repo |
| Local | `.claude/settings.local.json` | Personal repo-specific overrides, usually gitignored |
| Managed | Admin-managed settings | Organization policy |

Typical project settings:

```json
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "model": "sonnet",
  "effortLevel": "medium",
  "permissions": {
    "allow": [
      "Bash(npm run lint)",
      "Bash(npm run test *)"
    ],
    "deny": [
      "Read(./.env)",
      "Read(./secrets/**)"
    ]
  }
}
```

Use `CLAUDE.md`, `.claude/CLAUDE.md`, or `AGENTS.md` for project memory. Use `.claude/skills/<skill-name>/SKILL.md` for reusable workflows and `.claude/agents/<agent-name>.md` for subagents.

Useful commands:

| Need | Command |
| --- | --- |
| Inspect active configuration | `/config` |
| Change model during session | `/model` |
| Change reasoning effort | `/effort` |
| Create or manage subagents | `/agents` |
| Manage plugins | `/plugin` |
| Manage MCP servers | `/mcp` |
| Visualize context | `/context` |
| Check token usage and cost | `/cost` |
| Create or pursue a goal | `/goal` |

Use Claude Code plugins when standalone `.claude/` configuration is ready to be shared. Plugins use `.claude-plugin/plugin.json` and can include `skills/`, `agents/`, `hooks/`, `.mcp.json`, `.lsp.json`, `monitors/`, `bin/`, and `settings.json`.

## Configuring Cursor

Use Cursor when you want an IDE-first agent that benefits from open files, selected code, diagnostics, project rules, and interactive editing.

Cursor supports persistent instructions through:

- Project Rules in `.cursor/rules/`
- User Rules in Cursor settings
- root `AGENTS.md` for simple project-wide guidance
- legacy `.cursorrules`, which should be migrated when possible

Use `.cursor/rules/` when instructions need metadata, file globs, or composition. Use `AGENTS.md` when the project only needs a simple readable instruction file.

Rule types:

| Rule type | When it loads |
| --- | --- |
| Always | Included in every relevant agent context |
| Auto Attached | Included when matching file globs are referenced |
| Agent Requested | Available for the agent to pull in when relevant |
| Manual | Used when explicitly invoked |

Good Cursor rules are:

- focused
- concrete enough to act on
- scoped with globs when possible
- split instead of becoming one giant handbook
- short enough that the agent can reliably follow them

Cursor CLI can be used with `cursor-agent`.

```bash
cursor-agent
cursor-agent "refactor the auth module to use JWT tokens"
cursor-agent -p "review these changes for security issues" --model "<model>"
cursor-agent resume
cursor-agent --version
```

Cursor can also connect tools through MCP using `mcp.json`. Use MCP when you repeatedly copy data from another system into chat.

## Modes And Permissions

Permissions decide how far the agent can move without stopping. Start narrow, expand only for the current task, and keep destructive or secret-touching actions behind explicit approval.

| Mode | Use when | Avoid when |
| --- | --- | --- |
| Read-only or restrictive | Exploring a new repo, reviewing, planning, threat modeling, or working near secrets. | The task is already scoped and needs straightforward edits. |
| Workspace-write with approvals | Normal repo work where files are known and verification commands are expected. | The agent needs to mutate global config, install packages, or touch production systems. |
| Auto-edit / accept-edits | The plan is approved, edits are mechanical, and verification is fast. | The change is ambiguous, cross-cutting, or security-sensitive. |
| Full-auto / bypass-style | Disposable branch, worktree, container, or sandbox with no secrets and clear stop condition. | Normal application repos, production-like environments, or unclear goals. |

Practical defaults for this repo:

- Use repo-local writes for changes under `guides/`, `skills/`, `subagents/`, and `agent-kit/`.
- Ask before installing packages, accessing private services, mutating global configuration, or touching files outside the workspace.
- Keep reviewer subagents mostly read-only unless the user explicitly asks them to patch.
- Treat `agent-kit/agent-rules/security.md`, `agent-kit/agent-rules/testing.md`, and `agent-kit/agent-rules/validation.md` as policy anchors when deciding whether more autonomy is appropriate.

Tool-specific notes:

| Tool | Permission language to know |
| --- | --- |
| Codex | `sandbox_mode`, `approval_policy`, writable roots, command approvals, network restrictions. |
| Claude Code | permission modes, allow/deny rules, plan mode, `acceptEdits`, hooks, managed settings. |
| Cursor | agent modes, project rules, model/tool permissions, IDE-mediated file edits, MCP trust boundaries. |

## Planning And Goals

Use planning when the cost of the wrong edit is higher than the cost of a short thinking pass.

Use plan mode for:

- ambiguous user requests
- multi-file changes
- migrations
- architecture changes
- security-sensitive work
- tasks that cross from theory docs into implementation

Skip formal plan mode for:

- typos
- tiny documentation edits
- one-line fixes with obvious verification
- questions where the user only wants an explanation

A good plan should include:

- context loaded
- assumptions
- files or areas likely to change
- ordered steps
- verification strategy
- stop conditions

For this repo, tie plans back to:

- [managing-context.md](managing-context.md)
- [lifecycle.md](lifecycle.md)
- [agent-kit/skeletons/_design.md](../../agent-kit/skeletons/_design.md)

This repo uses two AI-run gate skills at transition points in the delivery cycle:

| Gate | When to run | Skill |
| --- | --- | --- |
| Plan Gate | Before starting Build | `/plan-gate` |
| PR Gate | Before merging | `/pr-gate` |

These gates verify that the plan or PR meets defined quality criteria. A failing gate means looping back, not pushing forward. See [AGENTS.md](../../agent-kit/AGENTS.md) for the full working cycle.

Goals are useful when an agent needs a bounded objective active through several turns. Claude Code exposes this directly with `/goal`; in other tools, the same pattern can be written as a prompt, skill, or task checklist.

Example:

```text
Goal: Make the auth session tests pass.
Context: Read guides/onboarding/lifecycle.md, src/auth/session.ts, and tests/auth/session.test.ts first.
Constraints: Only edit src/auth/ and tests/auth/.
Stop when: The auth test command passes, or a blocker is found.
Report: Changed files, verification output, and any residual risk.
```

Use goals when success can be checked with tests, lint, screenshots, docs diffs, or explicit acceptance criteria. Avoid goals like "improve the architecture" because the stop condition is subjective.

## Models And Reasoning

Do not pick the largest model by habit. Match the model and reasoning effort to the task.

| Task | Good default |
| --- | --- |
| Small docs edits, formatting, obvious fixes | Fast or cheaper model |
| Routine coding with local tests | Balanced coding model |
| Architecture, ambiguous requirements, migrations | Stronger reasoning model |
| Security, data contracts, business-critical behavior | Stronger model plus explicit verification |
| Large repo exploration | Balanced model with tight file targeting or subagents |
| Noisy parallel research | Cheaper subagents with narrow summaries |

Reasoning effort is a cost, latency, and quality knob.

| Use lower effort for | Use higher effort for |
| --- | --- |
| straightforward edits | ambiguous requirements |
| known patterns | architectural tradeoffs |
| formatting | debugging failures with weak signals |
| docs cleanup | security-sensitive changes |
| command output summarization | data correctness and business rules |

Higher effort is not a substitute for context. If the agent lacks the right files, docs, or acceptance criteria, more thinking often just makes a wrong path more polished.

Model examples:

```bash
codex -m <model>
codex -c model_reasoning_effort=high
claude --model <model>
cursor-agent -p "review this diff for security issues" --model "<model>"
```

Prefer model aliases for everyday work when you want provider improvements automatically. Pin exact models only when reproducibility matters.

## Pointing AI At Specific Files

Good file targeting saves context and improves answers. Be explicit about both the files and what role each file plays.

Instead of:

```text
Review the auth flow.
```

Use:

```text
Review the auth flow using:
- src/auth/session.ts as the implementation
- tests/auth/session.test.ts as expected behavior
- docs/features/auth/ as feature context

Focus on token refresh behavior. Do not review unrelated login UI.
```

Useful targeting patterns:

| Need | Prompt pattern |
| --- | --- |
| Explain one file | `Explain @path/to/file.ts, especially the error handling around <function>.` |
| Compare implementation and tests | `Compare @src/foo.py with @tests/test_foo.py and identify behavior not covered by tests.` |
| Update docs from code | `Use @src/domain/rules.py and @docs/features/<feature>/requirements.md. Update only the feature docs that are now stale.` |
| Limit scope | `Only inspect files under src/payments/ and tests/payments/ unless you find a direct dependency.` |
| Ask for placement | `Before editing, inspect repo structure and tell me where this behavior should live.` |
| Preserve reviewability | `Make the smallest cohesive change and list every file you touched.` |

When the tool supports file mentions, use them. When it does not, provide paths in plain text and ask the agent to read them first.

Avoid:

- "look at everything"
- dumping long files into chat when the agent can read them
- attaching stale snippets without naming the source path
- asking for broad implementation and broad review in the same prompt

## Verifying Context

The agent does not automatically know the repo. The harness selects what the model sees on each turn. Verify setup directly when the task matters.

Useful prompts:

```text
Before answering, list the instruction files, rules, skills, and project docs you loaded for this task.
```

```text
Show the active model, reasoning setting, sandbox or approval mode, and any project-specific instruction files you are using.
```

```text
Do not edit yet. Read AGENTS.md, docs/context/project.md, and docs/features/payments/requirements.md, then summarize the constraints that matter for this task.
```

Tool-specific checks:

| Tool | How to verify |
| --- | --- |
| Codex | Ask it to list loaded instruction sources; use `codex --cd <subdir>` to test nested instruction behavior; inspect logs/session files if enabled. |
| Claude Code | Use `/config`, `/context`, `/cost`, `/model`, and `/effort`. |
| Cursor | Check the Agent sidebar, use explicit file mentions, ask for loaded files, and split rules by scope. |

If the conversation becomes noisy, start a fresh session or write a handoff. For the underlying theory, see [../theory/context-engineering.md](../theory/context-engineering.md).

## Skills, Subagents, Plugins, And MCP

Use the smallest abstraction that solves the problem.

| Need | Use | Why |
| --- | --- | --- |
| One-off instruction | Prompt | Fastest and lowest ceremony. |
| Repeatable workflow | Skill | Captures steps, references, scripts, examples, and validation. |
| Specialist role | Subagent | Isolates context and can use a different model or permissions. |
| External system access | MCP / tool | Gives the agent structured access to systems outside the repo. |
| Reusable package across repos | Plugin | Bundles skills, agents, hooks, MCP config, and assets. |
| New durable doc | Skeleton | Starting template for a required doc; live in `agent-kit/skeletons/`. |

Use a skill when:

- you keep pasting the same checklist
- the workflow is stable enough to version
- the result is verifiable
- the instructions are procedural rather than role-based

Use a subagent when:

- the work is noisy and should not flood the main context
- the role has a clear specialty
- the role should have narrower tools or a different model
- the parent agent only needs a concise summary back

Use MCP when:

- the agent repeatedly needs data from GitHub, Slack, databases, docs, Figma, or another system
- copying data manually into chat is error-prone
- the tool can return compact, task-specific results

Do not connect MCP servers casually. Every enabled tool schema consumes context, and every external tool adds trust and prompt-injection risk.

For deeper guides:

- [../theory/skills.md](../theory/skills.md)
- [../theory/subagents.md](../theory/subagents.md)

## Shell Command Practices

Shell access is a capability boundary. It can read, write, execute, fetch, delete, and chain other programs.

Use shell commands for:

- repo inspection such as `rg`, `ls`, `git status`, `git diff`, and `git log`
- project-owned scripts such as `npm test`, `pytest`, `cargo test`, or `make lint`
- deterministic build, test, format, and codegen commands
- one-off diagnostics when the command is easy to review

Prefer built-in file tools over shell when:

- reading or editing specific files
- applying small patches
- searching a known path
- the command needs complex quoting, globbing, or control operators

Be careful with:

- compound commands using `&&`, `||`, `;`, pipes, or newlines
- wrappers such as `npx`, `docker exec`, `devbox run`, `mise exec`, `timeout`, `xargs`, or `find -exec`
- broad globs such as `**/*`
- network commands such as `curl`, `wget`, package installs, or custom download scripts
- commands that mutate state indirectly, such as generators, migrations, cleanup scripts, and snapshot tests

PowerShell note: on Windows, prefer native PowerShell commands end-to-end for file operations. Do not enumerate paths in PowerShell and pass them to another shell for deletion or moving. Resolve paths first and keep destructive actions approval-gated.

Practical rules:

- Use `rg` for search when available.
- Ask before installing packages, running network commands, or changing global config.
- Keep command approval narrow: approve `npm test` or `pytest tests/foo`, not a broad shell prefix.
- Do not let reviewer subagents run destructive commands.
- When a command produces evidence, summarize the exact command and result in the final report.

## Workflow Fit

Use permissions, planning, goals, skills, and subagents inside the development lifecycle, not as separate habits.

| Repo phase | Best AI setup | Why |
| --- | --- | --- |
| Intake | Short prompt, clarify scope, identify risk. | Avoid solving the wrong problem. |
| Context | Restrictive permissions, read-heavy prompts, explicit file references. | The agent should understand local conventions before changing anything. |
| Spec | Plan mode or explicit planning prompt. | Ambiguity is cheaper to resolve before code exists. |
| Plan | Written plan for broad work. | Name affected files, assumptions, test strategy, and documentation updates. |
| Build | Workspace-write permissions with approvals for commands outside the repo. | Most implementation work needs edits but still benefits from boundaries. |
| Verify | Test-focused prompts or specialist subagents. | Use focused review and evidence before claiming completion. |
| Document | Skills and repo guides. | When a workflow repeats, promote it from prompt memory into a durable asset. |

The lifecycle in [lifecycle.md](lifecycle.md) is the spine. Permissions become more capable only when the task is understood. Goals or autonomous loops belong after the plan is clear and the stop condition is verifiable.

## Installation And Updates

Keep installation details in official docs rather than copying full vendor instructions here.

| Tool | Install / setup | Configuration docs |
| --- | --- | --- |
| Codex | [Codex CLI](https://developers.openai.com/codex/cli) | [Config basics](https://developers.openai.com/codex/config-basic), [AGENTS.md](https://developers.openai.com/codex/guides/agents-md) |
| Claude Code | [Advanced setup](https://code.claude.com/docs/en/setup) | [Settings](https://code.claude.com/docs/en/settings), [Model configuration](https://code.claude.com/docs/en/model-config) |
| Cursor | [Cursor CLI installation](https://docs.cursor.com/en/cli/installation) | [Rules](https://docs.cursor.com/en/context), [MCP](https://docs.cursor.com/context/model-context-protocol), [Models](https://docs.cursor.com/models) |

Check versions regularly:

```bash
codex --version
claude --version
claude doctor
cursor-agent --version
```

## Best Practices

- Keep always-loaded instructions short.
- Move workflows into skills once they repeat.
- Use subagents for bounded specialist work, especially noisy research or review.
- Use plugins when a workflow needs to travel across repositories or teams.
- Start with restrictive permissions and expand only for the current task.
- Use plan mode for ambiguous, risky, or multi-file changes before edits begin.
- Convert approved plans into bounded goals only when success is verifiable.
- Prefer explicit file paths over vague scope.
- Ask the agent to name assumptions before implementing.
- Give autonomous loops clear stop conditions.
- Ask for evidence before accepting "done".
- Start a new session when the task changes substantially.
- Keep durable decisions in `docs/`, not only in chat.

## Anti-patterns

- one giant instruction file that tries to be the whole handbook
- broad prompts with no files, acceptance criteria, or constraints
- expensive models for mechanical changes
- high reasoning effort without enough context
- auto or bypass permissions in a repo that contains secrets or production access
- pursue-goal loops with vague objectives or no stop condition
- plan mode used as theater, with no files, assumptions, tests, or acceptance criteria
- subagents that are really just vague prompts
- skills that contain long theory instead of operational steps
- plugins before the underlying workflow has been tested locally
- MCP servers connected without considering trust and prompt-injection risk
- copying proprietary prompts, source, or harness logic into a project
- running unofficial cloned agent binaries with shell access

## Related Guides

- [managing-context.md](managing-context.md)
- [lifecycle.md](lifecycle.md)
- [../theory/context-engineering.md](../theory/context-engineering.md)
- [../theory/skills.md](../theory/skills.md)
- [../theory/subagents.md](../theory/subagents.md)

## References

Official docs first:

- Codex: [Config basics](https://developers.openai.com/codex/config-basic)
- Codex: [Configuration reference](https://developers.openai.com/codex/config-reference)
- Codex: [Custom instructions with AGENTS.md](https://developers.openai.com/codex/guides/agents-md)
- Codex: [Permissions](https://developers.openai.com/codex/permissions)
- Codex: [Agent Skills](https://developers.openai.com/codex/skills)
- Codex: [Plugins](https://developers.openai.com/codex/plugins)
- Codex: [Subagents](https://developers.openai.com/codex/subagents)
- Claude Code: [Settings](https://code.claude.com/docs/en/settings)
- Claude Code: [Permissions](https://code.claude.com/docs/en/permissions)
- Claude Code: [Goal](https://code.claude.com/docs/en/goal)
- Claude Code: [Model configuration](https://code.claude.com/docs/en/model-config)
- Claude Code: [Extend Claude with skills](https://code.claude.com/docs/en/skills)
- Claude Code: [Create custom subagents](https://code.claude.com/docs/en/sub-agents)
- Claude Code: [Connect to tools via MCP](https://code.claude.com/docs/en/mcp)
- Claude Code: [Create plugins](https://code.claude.com/docs/en/plugins)
- Cursor: [Rules](https://docs.cursor.com/en/context)
- Cursor: [Plan Mode](https://cursor.com/blog/plan-mode)
- Cursor: [Agent best practices](https://cursor.com/blog/agent-best-practices/)
- Cursor: [Cursor CLI installation](https://docs.cursor.com/en/cli/installation)
- Cursor: [Model Context Protocol](https://docs.cursor.com/context/model-context-protocol)
- Cursor: [Models](https://docs.cursor.com/models)

Further reading:

- Anthropic: [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- Anthropic: [Claude Code auto mode](https://www.anthropic.com/engineering/claude-code-auto-mode)
- Open standard: [Agent Skills](https://agentskills.io/home)
