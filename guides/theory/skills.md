# Skills

A practical introduction to Skills for developers who have never used one — what they are, when to reach for one, and how to set them up in Cursor.

## TL;DR

A Skill is a folder with a `SKILL.md` file inside. The file teaches an agent **when** to activate a workflow, **how** to execute it, and **how** to verify the result. Skills load on demand, so they turn "instructions I keep repeating in chat" into reusable, version-controlled capability.

```text
my-skill/
|-- SKILL.md          # required: metadata + instructions
|-- scripts/          # optional: executables the agent can run
|-- references/       # optional: deep documentation
|-- assets/           # optional: templates, fixtures
`-- examples/         # optional: input/output samples
```

## Why Skills Exist

Prompts are conversational and one-off. Repeating the same multi-step instructions in every chat is slow, drift-prone, and forgotten next session. A Skill captures that knowledge once, lives in the repo, and the agent loads it only when relevant.

What you get:
- consistent execution across sessions and teammates
- low prompt overhead — only metadata is always loaded
- testable, reviewable, version-controlled workflows
- domain expertise that travels with the code

## Skill vs Prompt vs Subagent vs Tool

| Concept | Main question | Role |
|---|---|---|
| Tool | What action can I take? | Single capability (run a script, call an API) |
| Prompt | What do I want right now? | One-off instruction |
| Skill | How should this kind of task be done? | Reusable workflow + context |
| Subagent | Where should this work run? | Isolated context for a bounded delegation |

Rules of thumb:
- repeatable workflow → **skill**
- isolated context or parallel delegation → **subagent** (see [subagents.md](subagents.md))
- single atomic action → **tool**
- one-time ask → **prompt**

A subagent can use one or more skills. They compose; they do not compete.

## Progressive Disclosure: How Skills Stay Cheap

Skills load in three stages so the context window never carries unused content.

| Level | What | Token cost | When it loads |
|---|---|---|---|
| 1. Metadata | `name` + `description` from frontmatter | ~100 tokens per Skill | Always (at session start) |
| 2. Instructions | Body of `SKILL.md` | Aim for under 500 lines / ~5k tokens | When the Skill is triggered |
| 3. Resources | `scripts/`, `references/`, `assets/`, `examples/` | Effectively unlimited | Only when the body references them |

Mental model: a Skill is like an onboarding guide. Metadata is the cover, `SKILL.md` is the table of contents, deep chapters are opened only if the task needs them. Scripts execute without their source code entering context — only the output costs tokens, so bundling a 2000-line API reference is free until something needs it.

## Anatomy of a SKILL.md

Minimum viable frontmatter (open standard fields):

```yaml
---
name: summarize-changes
description: Summarizes uncommitted changes and flags anything risky. Use when the user asks what changed, wants a commit message, or asks to review their diff.
allowed-tools:
  - Bash
  - Read
---
```

Frontmatter rules:
- `name`: lowercase letters, numbers, hyphens. Max 64 chars. No reserved words per the [open spec](https://agentskills.io/home). Prefer gerunds (`processing-pdfs`) or noun phrases (`pdf-processing`); avoid generic names like `helper` or `utils`.
- `description`: max 1024 chars. Write in **third person** ("Summarizes X", not "I can help with X"). Include **what it does and when to use it** — agents route on this field, so be specific.
- `allowed-tools`: explicit list of tools the skill may use. Use `[]` for read-only skills.

> This framework extends the open standard with additional fields (`phase`, `owner`, `last_reviewed`, `skill-version`). See [skills/README.md — SKILL.md structure](../../skills/README.md#skillmd-structure) for the full schema used here.

### Body skeleton

```markdown
# <Skill Name in Title Case>

<purpose>

## When to use
## When NOT to use
## Workflow
## Rules
## Anti-patterns
## Reference index
## Related skills
```

> How we apply this skeleton in this repo — section naming conventions, required vs. optional, and flexibility rules — is documented in [skills/README.md — Required sections](../../skills/README.md#required-sections-inside-skillmd).

## When To Write A Skill (And When Not To)

**Good candidates**
- you keep pasting the same instructions or checklist
- a section of `AGENTS.md` or `.cursor/rules/` has grown from a fact into a procedure
- the workflow is repeated, stable, and error-prone enough to deserve guardrails
- the result is verifiable

**Skip the skill if**
- the task is one-off
- the workflow is still highly unstable
- a clearer system prompt is enough
- the main value is an isolated context or parallel run — write a [subagent](subagents.md) instead
- the agent already handles it well without your help (test before assuming)

## Authoring Best Practices

### Be ruthless about context cost

Every token in `SKILL.md` competes with conversation history once loaded. The model is already smart — only write what it would get wrong without you.

```markdown
# Bad — restates what the model knows
PDF (Portable Document Format) files contain text and images. To extract
text you need a library. Many exist but pdfplumber is recommended because...

# Good — jumps to the project-specific thing
Use pdfplumber for text extraction. For scanned PDFs, fall back to
pdf2image + pytesseract.
```

### Match prescriptiveness to fragility

- **High freedom** (text guidance) when multiple approaches are valid: code reviews, exploratory analysis.
- **Low freedom** (exact commands) when consistency is critical: migrations, deploys, destructive ops.

Think open field → general direction; narrow bridge with cliffs → exact guardrails.

### Provide a default, not a menu

> "You can use pypdf, pdfplumber, PyMuPDF, or pdf2image..." — confusing.
> "Use pdfplumber. For scanned PDFs, use pdf2image + pytesseract." — clear default, escape hatch.

### Paths and references

Use forward slashes (`scripts/helper.py`, never `scripts\helper.py`) so the skill works on every OS. Link from `SKILL.md` directly to every reference doc — agents sometimes only partially read files referenced indirectly, so never chain `SKILL.md → advanced.md → details.md`.

### Patterns that pay off

| Pattern | When to use |
|---|---|
| **Gotchas section** | Non-obvious facts the agent will get wrong without being told (soft deletes, naming mismatches, `/health` vs `/ready` endpoints). Highest-value content in many skills. |
| **Checklists** | Multi-step workflows where skipping a step is costly. Tell the agent to copy the checklist and tick boxes as it progresses. |
| **Validation loops** | Run validator → fix → repeat. Catches errors before they propagate. |
| **Plan-validate-execute** | Batch or destructive ops. Build a plan file, validate it against the source of truth, then execute. |
| **Templates** | When output format is fixed. A concrete template beats prose description. |
| **Examples** | When the desired style is hard to describe. Input/output pairs work like few-shot prompting. |

### Build evals before extensive docs

Run the task without the skill, log where the agent fails, write just enough to plug those gaps, then re-run and compare. Read execution traces, not just final outputs — if the agent wandered, your instructions were probably vague or offered too many options without a default.

```text
identify gap -> write minimal skill -> test -> observe trace -> refine
```

## Setting Up Skills In Cursor

Cursor discovers skills from the filesystem — no upload, no API call. Drop the folder into one of these paths:

| Scope | Path |
|---|---|
| Project | `.cursor/skills/` or `.agents/skills/` |
| Personal | `~/.cursor/skills/` or `~/.agents/skills/` |

Cursor recursively discovers any `SKILL.md` under those folders, so you can group by category:

```text
.cursor/skills/
|-- shipping/
|   `-- land-it/SKILL.md
`-- debugging/
    `-- using-datadog-mcp/SKILL.md
```

Create one in 60 seconds — `mkdir -p .cursor/skills/summarize-changes`, then drop `SKILL.md` inside. Cursor loads it automatically when the user's request matches the `description`, or you can invoke it manually with `/summarize-changes`.

**Useful frontmatter knobs:**

| Field | What it does |
|---|---|
| `disable-model-invocation: true` | Only the user can run it (good for `/deploy`, `/commit`) |
| `user-invocable: false` | Only the agent can load it (good for background context the user shouldn't trigger) |
| `allowed-tools: Read Grep` | Pre-approve tools while the skill is active |
| `paths: "src/**/*.ts"` | Auto-load only when working in matching files |
| `model: inherit` / model ID | Override model for this skill |
| `context: fork` | Run the skill in a forked subagent context |

Activation: the agent picks skills based on the `description` and any `paths` glob. Type `/` to invoke one manually. Run `/migrate-to-skills` to convert legacy Rules and slash commands — Skills are the modern replacement, though older Rules still work.

Cursor watches skill directories live: edits take effect inside a running session without restart.

## Anti-patterns

- vague descriptions that won't route (`description: Helps with documents`)
- one giant skill spanning unrelated jobs
- deep chains of references (`SKILL.md → a.md → b.md → c.md`)
- time-sensitive content baked in (`"After August 2025 use the new API"`) — quarantine deprecated info in an "old patterns" section instead
- restating common knowledge to inflate the file
- offering five tools as equal options instead of picking a default
- writing in first person ("I can help you...") — agents route worse on it

## Pre-flight Checklist

Before shipping a skill:

- [ ] `description` is specific, third person, includes both **what** and **when**
- [ ] `SKILL.md` body is under ~500 lines
- [ ] References are one level deep from `SKILL.md`
- [ ] Concrete examples, not abstract guidance
- [ ] Validation/verification step on critical paths
- [ ] No time-sensitive claims in the main body
- [ ] Forward slashes everywhere
- [ ] Tested with at least one real task end-to-end

## Language policy

- Skills default to the user's language for conversation, prompts, and questions.
- Glossary terms stay in their canonical form regardless of conversation language.
- Generated artifacts (PRDs, reports, plans) follow the glossary's language by default; if the glossary is missing, follow the user's language. The user may override per artifact.
- Frontmatter values and code identifiers are always in English (ASCII).

## Maintaining the catalog (metarepo)

When editing skills in this repository:

1. Edit canonical files under `skills/` — for plugin-shipped utils, edit `skills/utils-skills/<name>/SKILL.md`, not the copy under `plugins/test-plugin/skills/`.
2. Regenerate plugin copies: `python skills/lint.py --sync-plugin`
3. Validate locally: `python skills/lint.py` (also checks skeleton filename casing under `agent-kit/skeletons/`).
4. CI (`.github/workflows/lint.yml`) runs the same lint on every push to `main` and on pull requests.

See [skills/README.md](../../skills/README.md) for the full catalog conventions, including **phase vs invocation** (e.g. `notebook-mockup` is `cross-cutting` in frontmatter but invoked during Build).

## Where To Look Next

- Skill catalog and repo conventions: [skills/README.md](../../skills/README.md)
- Development workflow they support: [../onboarding/lifecycle.md](../onboarding/lifecycle.md)
- Specialist delegation: [subagents.md](subagents.md)

## References

- Anthropic — [Agent Skills overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
- Anthropic — [Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- Anthropic — [Equipping agents for the real world with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills) (engineering blog)
- Anthropic — [The Complete Guide to Building Skills for Claude](https://resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf) (PDF)
- Claude Code — [Extend Claude with skills](https://code.claude.com/docs/en/skills)
- Cursor — [Skills documentation](https://cursor.com/docs/context/skills)
- Open standard — [agentskills.io](https://agentskills.io/home)
- Open standard — [Best practices for skill creators](https://agentskills.io/skill-creation/best-practices)
- Open-source skills — [github.com/anthropics/skills](https://github.com/anthropics/skills)
