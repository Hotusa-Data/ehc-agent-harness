# EHC AGENT HARNESS

> A Data Science harness for working with AI agents in a consistent, traceable, and reviewable way.

![Status](https://img.shields.io/badge/status-under%20construction-yellow)
![Scope](https://img.shields.io/badge/scope-agent%20harness-blue)
![Team](https://img.shields.io/badge/team-Eurostars%20Data%20Science-green)

This is the place where we capture how we want to work with AI agents in Data Science projects: shared context, rules, skills, utils, subagents, hooks, and, later on, an installer.

It is not meant to be a heavy framework or a closed methodology. The idea is simpler: **think better before asking, build in small steps, review with evidence, and leave useful documentation as we go**.

> [!IMPORTANT]
> This README is the initial contract for the repo. It should help anyone on the team understand what lives here, when to use it, how to contribute, and how it is expected to grow.

---

## TL;DR

| If you need to... | This repo helps with... |
|---|---|
| Start an AI-assisted task without guessing | Skills to clarify the problem, define the spec, and shape the plan |
| Keep projects consistent | Rules for naming, Python, SQL, Terraform, and shared context |
| Review work with repeatable criteria | Specialized subagents and QA checks |
| Document without leaving it for the end | Skills and templates aimed at both business and technical audiences |
| Automate useful reminders | Low-noise hooks for concrete guardrails |

The golden rule: **if a piece does not help solve a real team problem, it probably does not belong here yet**.

---

## Why This Exists

Working with AI can make us much faster. It can also make chaos much faster if we do not add a little structure.

This repo comes from four frictions that show up quickly when several people use agents every day.

### 1. AI Cannot Guess the Problem

If the goal, inputs, outputs, constraints, and success criteria are unclear, the agent will fill the gaps with assumptions. Sometimes it gets it right. Sometimes it gives us a long scenic route to a place nobody asked for.

The harness encourages a better starting conversation: what we want to solve, why it matters, what we know, what we do not know, which assumptions we are accepting, and how we will check that the solution works.

### 2. Speed Without Conventions Creates Debt

When several people solve similar problems in parallel, inconsistency appears quickly: different names for the same idea, duplicated queries, almost identical functions, modules that are hard to find, and patterns that change from repo to repo.

AI can amplify that if every agent works with different rules. That is why we need shared language, shared conventions, and reusable quality criteria.

### 3. Documentation Is Part of Development

Documentation should not be a final ceremony or a last-minute race before closing a task. Each development should leave a trace of what problem it solves, which decisions were made, how it is used, and how it translates into business value.

A feature can be implemented and still be unexplained. If the business side does not understand what changed or why it matters, part of the work is still missing.

### 4. Without Feedback Loops, Agents Work Blind

The goal is not to generate more code. The goal is to generate code that is more robust, more standard, and easier to maintain.

For that we need small steps, QA, tests, and evidence. An agent cannot improve what it cannot check.

---

## Principles

| Principle | What it means in practice |
|---|---|
| **Clarity before speed** | Define the problem first; implement second |
| **Small units of work** | Each change should be easy to understand, test, and correct |
| **Evidence over trust** | A change comes with checks, tests, review, or a clear validation note |
| **Document while building** | Decisions and functional impact are captured during development |
| **Shared conventions** | Rules are short, stable, and usable by any agent |
| **Low noise** | The harness should help us work better, not add ceremony |

---

## When to Use It

Use this repo when you want to:

- Prepare a task for AI-assisted work.
- Turn a vague idea into an actionable spec.
- Break an implementation into small steps.
- Review code, SQL, tests, or documentation with shared criteria.
- Create or improve a reusable skill, rule, subagent, or hook.
- Keep Data Science projects consistent across the team.

Do not use it to impose a rigid methodology. If something does not help with real team problems, we simplify it, rewrite it, or remove it. No drama.

---

## Architecture

The harness is organized in layers. Each layer has a clear responsibility.

```text
ds-agent-harness
│
├─ Shared context
│  └─ rules/
│     ├─ CONTEXT.md
│     ├─ naming-conventions.mdc
│     ├─ python-conventions.mdc
│     ├─ sql-conventions.mdc
│     └─ terraform-conventions.mdc
│
├─ Working processes
│  ├─ skills/      -> development lifecycle
│  └─ utils/       -> helper processes for working with AI
│
├─ Specialized review
│  └─ subagents/   -> expert reviewers by domain
│
├─ Automation
│  └─ hooks.json   -> executable guardrails
│
└─ Future distribution
   └─ plugin / installer
```

| Layer | Responsibility |
|---|---|
| **Rules** | Keep stable context and conventions available to the agent |
| **Core skills** | Guide the development workflow from idea to delivery |
| **Utils skills** | Support auxiliary tasks around AI-assisted work |
| **Subagents** | Bring domain-specific review criteria |
| **Hooks** | Automate low-noise checks and reminders |
| **Plugin/installer** | Distribute the harness reproducibly once it is mature |

> [!TIP]
> The priority is to build useful content before packaging it. The installer comes later, once we know what is worth installing.

---

## Lifecycle

The lifecycle is a taxonomy of work, not a mandatory sequence. It helps organize development and decide what kind of help to ask from the agent at each moment.

You can use one skill, several skills, or none. `DISCOVER` is optional and is useful when we still need to understand the domain before deciding what to build.

```text
  THINK          DISCOVER          DEFINE          PLAN            BUILD            QA            TEST          DOCUMENT
 ┌────────┐      ┌────────┐       ┌────────┐      ┌────────┐      ┌────────┐     ┌────────┐     ┌────────┐     ┌────────┐
 │Problem │ ───▶ │Research│  ───▶ │  Spec  │ ───▶ │  Plan  │ ───▶ │ Build  │ ──▶ │  Code  │ ──▶ │  Test  │ ──▶ │  Docs  │
 │Sketch  │      │Examples│  opt. │ Design │      │ Tasks  │      │  Code  │     │  QA    │     │ Pytest │     │Design  │
 └────────┘      └────────┘       └────────┘      └────────┘      └────────┘     └────────┘     └────────┘     └────────┘
   human         /discover          /spec           /plan           /build          /qa            /test         /document
```

> [!IMPORTANT]
> The most important step happens before talking to the AI: write what you want to solve, why it matters, what you know, what you do not know, and what a possible solution might look like.

Names starting with `/` are visual shorthand for skills. For now, they are placeholders for real skills, not commands.

| Phase | Question it answers | Expected output |
|---|---|---|
| **THINK** | What do I want to solve and why does it matter? | A human-written problem sketch |
| **DISCOVER** | What do I need to understand before deciding? | Simple explanation, examples, and reasonable options |
| **DEFINE** | What does “done well” mean? | Goal, inputs, outputs, constraints, and success criteria |
| **PLAN** | How do we split this into small work? | Implementable plan with dependencies, risks, and validation |
| **BUILD** | Which functional slice do we build now? | Working code in reviewable changes |
| **QA** | What can we simplify or harden? | Clearer, more robust, easier-to-change code |
| **TEST** | What evidence do we have? | Tests or checks executed |
| **DOCUMENT** | How do we explain this to the team and business? | Glossary, decisions, and functional documentation when relevant |

<details>
<summary>Quick usage example</summary>

1. Write a short problem sketch: goal, context, constraints, and success signal.
2. Use `/spec` to turn it into a clear specification.
3. Use `/plan` to split it into small tasks.
4. Use `/build` to implement the first functional slice.
5. Use `/qa` and `/test` to review with evidence.
6. Use `/document` to leave the functional and technical trace.

</details>

---

## Planned Content

### Core Skills

Each skill lives in its own folder with a `SKILL.md`. It should be small, actionable, and verifiable. It is not long-form documentation; it is a process an agent can follow.

If you are not familiar with skills, see <https://agentskills.io/home>.

| Skill | What it does | Expected output |
|---|---|---|
| `/discover` | Research a problem and explain it with simple examples | Options, trade-offs, and a reasoned recommendation |
| `/spec` | Turn a need into a clear specification | Goal, scope, inputs, outputs, and success criteria |
| `/plan` | Split a spec into small tasks | Ordered implementation plan |
| `/build` | Implement in small steps | Working code in reviewable slices |
| `/qa` | Improve quality, simplicity, and maintainability | Findings, improvements, and applied changes |
| `/test` | Test behavior with evidence | Tests, checks, or documented manual validation |
| `/document` | Translate a technical feature into useful documentation | Functional explanation, decisions, and glossary when relevant |

### Utils Skills

| Skill | What it does |
|---|---|
| `/create-skill` | Design a new skill without turning it into vague prose |
| `/compress-context` | Summarize a conversation or development so another AI can continue |

### Rules

Rules are background knowledge. They should be short, stable, and actionable.

| Rule | What it covers |
|---|---|
| `CONTEXT.md` | Ubiquitous language, domain glossary, and preferred names |
| `naming-conventions.mdc` | Names for modules, functions, tables, resources, and schemas |
| `python-conventions.mdc` | Pandera, configuration, logging, CLIs, Ruff, `ty`, and pytest |
| `sql-conventions.mdc` | SQL style and query conventions |
| `terraform-conventions.mdc` | Infrastructure conventions |

> [!NOTE]
> `CONTEXT.md` should stay short. What only applies to Python belongs in `python-conventions.mdc`; what only applies to SQL belongs in `sql-conventions.mdc`.

### Subagents

Subagents do not replace skills. A skill defines the process; a subagent brings expert judgment.

| Subagent | Reviews |
|---|---|
| `python-reviewer` | Python quality, typing, design, and maintainability |
| `sql-reviewer` | Queries, data models, duplication, and performance |
| `testing-reviewer` | Coverage, edge cases, and feedback loops |
| `docs-reviewer` | Glossary, functional design, and business clarity |
| `performance-reviewer` | Cost, complexity, and bottlenecks |

### Hooks

Hooks are an advanced layer. They are useful when an important rule can become a low-noise executable guardrail.

| Event | Possible action | Why |
|---|---|---|
| `afterFileEdit` | Check naming in `*pipeline*.py` or `*model*.py` | Consistency without relying only on prompts |
| `beforeShellExecution` | Warn if `pip install` is used without touching `pyproject.toml` | Dependency integrity |
| `stop` | Remind about documentation when a relevant feature changed | Traceability and business handoff |

---

## What Belongs Here

| Belongs here | Does not belong here |
|---|---|
| Rules we use across several projects | Personal preferences without evidence |
| Skills with clear steps and verifiable outputs | Long prompts nobody can maintain |
| Hooks that prevent repeated mistakes | Noisy or fragile automations |
| Subagents with specialized review criteria | Generic reviewers that repeat the same advice |
| Documentation that helps the business or the team | Decorative prose that does not change how we work |

---

## Definition of Done

A piece of the harness is ready when it:

- Solves a problem we have already seen.
- Is easy for an agent to read and apply.
- Has exit criteria or evidence.
- Is small enough to maintain.
- Fits with the rest of the harness without duplicating responsibilities.

---

## Planned Structure

```text
ds-agent-harness/
├── README.md
├── CONTEXT.md
├── CONTRIBUTING.md
│
├── skills/
│   ├── discover/SKILL.md
│   ├── spec/SKILL.md
│   ├── plan/SKILL.md
│   ├── build/SKILL.md
│   ├── qa/SKILL.md
│   ├── test/SKILL.md
│   └── document/SKILL.md
│
├── utils/
│   ├── create-skill/SKILL.md
│   └── compress-context/SKILL.md
│
├── rules/
│   ├── naming-conventions.mdc
│   ├── python-conventions.mdc
│   ├── sql-conventions.mdc
│   └── terraform-conventions.mdc
│
├── subagents/
│   ├── python-reviewer.md
│   ├── sql-reviewer.md
│   ├── testing-reviewer.md
│   └── docs-reviewer.md
│
└── hooks.json
```

---

## Roadmap

| Status | Phase | Outcome |
|---|---|---|
| ✅ | **0. README** | Initial repo contract |
| ⬜ | **1. Base rules** | `CONTEXT.md` plus naming, Python, SQL, and Terraform conventions |
| ⬜ | **2. Core skills** | `discover`, `spec`, `plan`, `build`, `qa`, `test`, `document` |
| ⬜ | **3. Utils skills** | `create-skill`, `compress-context`, and handoffs |
| ⬜ | **4. Subagents** | Expert reviewers for repeated tasks |
| ⬜ | **5. References/scripts** | Supporting material only when a skill needs it |
| ⬜ | **6. Hooks** | Low-noise automated guardrails |
| ⬜ | **7. Plugin/installer** | Reproducible harness distribution |

---

## Contributing

Contributions should improve the team’s real consistency, not add ceremony.

You can contribute in two ways:

- Improve an existing skill, rule, hook, or subagent.
- Create a new piece when there is a real problem that justifies it.

Before proposing something new, check that it:

- [ ] Solves a problem we have already seen.
- [ ] Is specific and actionable.
- [ ] Has exit criteria or evidence.
- [ ] Is small.
- [ ] Can be combined with the rest of the harness.

When a piece no longer reflects how we actually work, we change it through a PR. The harness is here to serve the team, not to become dramatic about itself.

---

## License

Private - internal use by Hotusa Data.

