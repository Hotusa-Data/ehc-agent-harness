# Context Engineering

Context Engineering (CE) is the discipline of managing **what the model can see**. For coding agents, this matters as much as the prompt itself: the model can only reason from the instructions, tools, examples, files, retrieved notes, previous turns, and outputs that fit inside the current context window.

The core idea is simple:

> More context does not mean more wisdom. Good context is small, relevant, structured, and current.

Code has become cheap and abundant — you can generate thousands of lines for the price of a coffee. High-quality architecture, by contrast, is expensive and scarce. When code is free, the bottleneck shifts from syntax to the systems that steer it. Your job is not to write more code. It is to provide the constraints that make AI-produced code safe, coherent, and high-leverage. **Context engineering is how you do that.**

## TL;DR

Use CE to keep an agent in a sharp working state:

- give it the smallest high-signal context that can solve the task
- retrieve files and docs just in time instead of loading everything up front
- keep tools and MCP servers lean because their schemas also spend tokens
- write lasting decisions in markdown, not in a long chat thread
- clear noisy sessions often; compact only when continuity is worth the cost
- work in vertical slices with fast tests so the agent cannot drift for long

## The Mental Model

An AI chat is not memory. Each response is generated from the context available **right now**. A useful metaphor is a desk covered with notes: the model works from whatever has been placed in front of it for this turn.

That is not only a limitation. It is leverage. You can curate the model's working mind for the current job:

- **Human as strategist**: define intent, constraints, architecture, tests, and acceptance criteria.
- **Agent as tactical executor**: inspect, implement, run checks, summarize, and propose local fixes.

When the session gets noisy, starting clean often improves reasoning more than adding another instruction.

## What Fills The Context Window

The context window is the total working payload the model sees, including both input and the response it is about to produce. In a coding agent, it can contain:

- system and developer instructions
- current request and prior conversation
- files, snippets, diffs, logs, and test output
- tool definitions and parameter schemas
- MCP server descriptions
- tool results and command output
- memory files, summaries, retrieved docs, and examples

This is why coding agents fill up faster than normal chat. A thread may look short to the human while already carrying a large hidden load of rules, schemas, files, and results.

Reserve room for the answer. If the window is nearly full, the model may skip details, produce shallow plans, truncate edits, or sound confident while under-checking its work.

## The Physics of Context

The context window has hard constraints that directly impact model reasoning:

| Constraint | Description | Impact on engineering |
|---|---|---|
| **Input/Output limits** | Fixed memory per session | Requires strict token budgeting |
| **Primacy/Recency bias** | Model favors start and end of context | Critical instructions must go at the very top or bottom |
| **Quadratic attention** | Attention cost grows quadratically with length | Long threads inevitably degrade reasoning quality |
| **Retrospective hallucination** | Model forgets or fabricates early-session details | Fresh starts beat repeated compaction |

These aren't bugs to work around — they're the physics you design for.

## The Four Buckets

Anthropic groups model context into four practical buckets:

| Bucket | What it carries | Examples |
|---|---|---|
| **System prompt** | Role, tone, hard rules, conventions | SQL dialect, style guide, "never `SELECT *` on production" |
| **Tools** | Available capabilities and schemas | `query_bigquery`, `read_schema`, `run_tests` |
| **Examples** | Desired output shape | sample rows, reference queries, before/after snippets |
| **Retrieved info / history** | Just-in-time facts | docs, repo files, issue notes, recent conversation |

Most CE work is deciding what belongs in which bucket, when to refresh it, and when to remove it.

## Why Context Degrades

Large windows are useful, but they do not make every token equally useful. As context grows, attention spreads out and the model becomes worse at using specific facts. This is often called **context rot**.

### Smart Zone vs. Dumb Zone

While providers advertise massive context windows, there is a practical distinction:

| Zone | Token range | Model behavior |
|---|---|---|
| **Smart Zone** | 0–100k tokens | Sharp attention, reliable reasoning |
| **Dumb Zone** | 120k+ tokens | Degraded attention, lost in the middle |

Beyond ~120k tokens, attention mechanisms scale quadratically, straining relationships between tokens. The model exhibits **primacy bias** (favors the beginning) and **recency bias** (favors the end), often ignoring critical data buried in the middle.

Two failure modes matter most:

- **Lost in the middle**: the model tends to use the beginning and the end of the context better than the buried middle.
- **Context bloat**: too many files, tools, logs, examples, or old decisions compete for attention.

The result is familiar: the agent ignores an important rule, repeats an already-fixed mistake, forgets a design decision, or writes plausible but messy code.

A practical rule of thumb: keep demanding reasoning comfortably below 100k tokens. A 200k or 1M-token window is not a promise of 200k or 1M tokens of reliable reasoning.

## Hygiene: Clear, Compact, Handoff, Notes

Long work needs context hygiene. Use four moves deliberately.

Think of an LLM session like the protagonist in *Memento* — each turn resets to a base state. The model doesn't "remember" your earlier conversation; it re-reads it every time. This is why compaction creates **sediment**: each summary adds a layer of distortion. The cleaner the session, the sharper the reasoning. A fresh start almost always beats a long compaction chain.

| Move | Use it when | Watch out for |
|---|---|---|
| **Clear** | Starting a new task, after noisy debugging, or when the agent misses obvious things | Save important decisions first |
| **Compact** | A long session has useful state that can be summarized inside the same session | Repeated summaries can drop or distort details |
| **Handoff** | A fresh agent should continue a focused slice without inheriting the old token load | Keep it scoped, temporary, and free of secrets |
| **Durable notes** | Knowledge should survive across sessions | Notes must stay curated |

Write long-lived knowledge to markdown: `research.md`, `glossary.md`, `architecture.md`, specs, issues, or task notes. The chat is a workspace, not a database.

Treat chat history like code: refactor it. When it gets tangled, extract the important decisions and restart from a clean, focused state.

### Handoff for session compression

The `handoff` skill turns the critical state of a session into a portable markdown file for a fresh agent. It is different from compaction: compaction keeps working inside the same conversation, while handoff starts a new session with only the goal, current state, constraints, next steps, and verification plan.

Use handoff when you want to:

- move from "Grill Me" planning into a separate prototype or implementation session
- pass a bug, sub-task, or GitHub issue to another agent without polluting the original thread
- treat separate sessions as lightweight subagents working on different slices
- move work between AI tools or ask another agent for adversarial review
- reset into a fresh, focused session while preserving the few facts that matter

A good handoff is disposable and specific. Store it in the OS temporary directory (`/tmp/` on Linux/macOS, `%TEMP%` on Windows), **not** the project workspace. This prevents "doc rot" — stale plans left in the repo that silently influence future sessions. Include suggested skills such as TDD or Diagnose when useful, and redact secrets like API keys or credentials.

## Patterns That Work

### Ask before building

For ambiguous work, make the agent interview you before implementation:

```text
Interview me before implementation. Surface missing requirements,
name trade-offs, and keep asking until the acceptance criteria are concrete.
```

This prevents the model from filling gaps with confident guesses.

### Build tracer bullets (vertical slices)

Agents naturally build horizontally: database first, then API, then UI. This leaves them "coding blind" for too long. Push toward a small end-to-end slice — a **tracer bullet** — instead:

```text
DB -> API -> UI -> test -> visible behavior
```

Like a phosphorescent round that shows your aim before committing to battle, a tracer bullet provides immediate green-red feedback across the full stack. Vertical slices keep feedback close and reveal integration mistakes early.

### Graybox: design the boundary, delegate the blob

Use your domain knowledge to design the public interface — the boundary — and delegate implementation inside the blob to the agent. As long as the interface is stable and the tests pass, you don't need to inspect the internals.

This is the "staff engineer" move: you provide the contract, the agent fills the implementation.

### Test before expanding

Use red-green-refactor when risk matters:

1. Identify or write the failing check.
2. Make the smallest change that passes it.
3. Refactor while the test protects behavior.

The agent can produce code quickly. Your leverage is making tests and checks answer quickly.

## Practical Rules

### Retrieve just in time

Do not load the whole repo, schema catalog, or documentation set "just in case." Start with the task, inspect the relevant files, then expand only when the evidence says you need more.

### Keep tools and MCP lean

Every tool definition and MCP server consumes context before it is used. Enable only what the current job needs. Tool responses should return what the model needs to answer, not the full raw API payload.

Good tool design filters noisy fields, aggregates in the tool layer, and exposes raw detail only through explicit follow-up parameters.

### Structure context for navigation

Markdown headings, short sections, tables, examples, and named files help both humans and models navigate. A structured page beats one long undifferentiated section.

### Prefer interfaces over implementation dumps

If the task only needs the contract, provide the contract: endpoint schema, public interface, test fixture, or architecture note. Make deep implementation available on demand.

### Keep files short (350-line rule)

Short files are easier for agents to process within the Smart Zone. Use a lint rule or test to enforce that no file exceeds 350 lines. This reduces the cognitive load on the attention mechanism and keeps each file focused on a single responsibility.

### Prefer deep modules

Drawing on John Ousterhout's *A Philosophy of Software Design*, prioritize **deep modules** — significant functionality hidden behind a simple, stable interface. Shallow modules (complex interfaces with little logic) force the agent to "bounce" between too many files, burning tokens and inducing confusion. Deep modules are your only effective containment strategy against AI-accelerated entropy.

## Anti-patterns

- loading whole repos, schemas, docs, or logs up front
- assuming a huge context window means reliable recall
- burying critical instructions in the middle of a long thread
- keeping every MCP server enabled by default
- returning full raw API payloads when a compact result would do
- compacting repeatedly until summaries become stale
- writing vague prompts like "be careful" instead of concrete constraints
- building broad foundations without a working vertical slice
- treating retrieved docs as ground truth without provenance
- treating PRDs as compile targets and ignoring the actual code (Specs-to-Code Fallacy)
- trusting the model's training data over live, retrievable sources — use your search tool

## Pre-flight Checklist

Before running an agent on meaningful work:

- [ ] The task has concrete acceptance criteria.
- [ ] The session is clean enough for the current job.
- [ ] Only relevant tools and MCP servers are enabled.
- [ ] Files and docs are retrieved just in time.
- [ ] Important rules are near the start or restated near the current task.
- [ ] Durable decisions live in markdown, specs, or issues.
- [ ] Long-running work has a handoff plan before the session gets bloated.
- [ ] The next step is a vertical slice with an observable result.
- [ ] There is a test, check, or QA loop before calling it done.

## Context Engineering In This Framework

CE is the layer underneath the rest of this repo:

- **Skills** use progressive disclosure: metadata is always visible, deeper instructions load only when needed.
- **Subagents** isolate noisy work and return summaries instead of full traces.
- **Handoff skills** let a fresh session continue a focused slice without inheriting token bloat.
- **SDD** turns decisions into durable, versioned context.
- **Memory files** preserve reusable notes outside the chat.
- **Testing rules** keep feedback fast enough to catch drift.

The discipline is staying conscious of what each token is doing, what it costs, and whether it still deserves attention.

## Where To Look Next

- [skills.md](skills.md) - progressive disclosure as a CE technique
- [subagents.md](subagents.md) - sub-agent architectures for context isolation
- [spec-driven-development.md](spec-driven-development.md) - specs as durable context
- [../onboarding/lifecycle.md](../onboarding/lifecycle.md)

## References

- Anthropic - [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- Anthropic Cookbook - [Context engineering: memory, compaction, and tool clearing](https://platform.claude.com/cookbook/tool-use-context-engineering-context-engineering-tools)
- Matt Pocock - [Most devs don't understand how context windows work](https://www.youtube.com/watch?v=-uW5-TaVXu4)
- Matt Pocock - [Claude Code for Real Engineers](https://github.com/mattpocock/ai-hero-skills)
- Andrej Karpathy - [tweet coining the framing](https://x.com/karpathy/status/1937902205765607626)
- Simon Willison - [Context engineering](https://simonwillison.net/2025/Jun/27/context-engineering/)
- Manus - [Context Engineering for AI Agents: Lessons from Building Manus](https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus)
- Inkeep - [Fighting Context Rot](https://inkeep.com/blog/fighting-context-rot)
- John Ousterhout - *A Philosophy of Software Design* (deep vs. shallow modules)
- Ryan Lopopolo - "Harness Engineering" at OpenAI
- Andrew Hunt & David Thomas - *The Pragmatic Programmer* (tracer bullets, software entropy)
- Frederick P. Brooks - *The Design of Design* (design concept and design tree)
