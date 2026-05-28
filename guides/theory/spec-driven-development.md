# Spec-Driven Development

A practical introduction to SDD for developers working with data — what it is, the workflow shape, and how it differs from vibe coding or TDD.

## TL;DR

SDD makes the **specification** — not the code — the single source of truth. You describe what to build and why in a versioned artifact, derive a plan, break it into tasks, and only then let an agent generate code. For data work specifically, the spec also pins down schemas, contracts, and the evidence (notebook outputs, quality checks) that proves the result.

```text
Spec  →  Plan  →  Tasks  →  Implement
what+why    how    atomic units   code + evidence
```

## Why SDD Exists

LLMs ship plausible code in seconds. That speed creates a failure mode worth naming: **vibe coding** — code that drifts from intent, hallucinates APIs, and rots as the project scales. In data work the drift is *silent*: a pipeline still runs, just on the wrong shape, the wrong filter, or the wrong join. SDD makes intent explicit before broad implementation so divergence becomes visible at review — not at the next quarterly metric.

## SDD vs Vibe Coding vs TDD vs BDD

| Approach | Source of truth | Strength | Where it breaks |
|---|---|---|---|
| Vibe coding | The prompt | Speed on small things | Drift, hallucinated APIs, decaying code |
| TDD | Failing test | Granular regression safety | Tests mirror implementation, not intent |
| BDD | Scenario in business language | Stakeholder alignment | Scales poorly past a few features |
| **SDD** | Versioned spec | Intent traceable through plan → tasks → code | Overhead on tiny fixes; needs spec discipline |

The four are not mutually exclusive. SDD can sit on top of TDD-style tests, and BDD scenarios make good acceptance criteria inside an SDD spec.

## The Canonical Workflow

Most SDD toolkits (GitHub Spec Kit, AWS Kiro, BMAD, and others) converge on the same four phases. Each produces a markdown artifact that feeds the next:

| Phase | Produces | Answers |
|---|---|---|
| **Spec** | `requirements.md` | What and why — user stories, scope, acceptance criteria |
| **Plan** | `design.md` | How — approach, dependencies, tradeoffs |
| **Tasks** | `tasks.md` | The work — atomic units in dependency order |
| **Implement** | code + evidence | The result — implementation plus verification |

The larger the risk, the more explicit each phase should be. Tiny fixes can collapse Spec and Plan into a single paragraph.

## Anatomy Of A Spec

```text
docs/features/<feature>/
|-- requirements.md
|-- design.md
|-- tasks.md
|-- report.md       (created at cycle close)
`-- CHANGELOG.md
```

A useful `requirements.md` covers: problem statement, goals, non-goals, current behavior, target behavior, requirements, acceptance criteria, examples, and assumptions plus open questions.

For data projects, "acceptance criteria" means **observable evidence**: expected schema shape, row count bounds, data quality checks, before/after diffs on a sample, or notebook cells that must pass. If you can't observe it, it isn't a criterion — it's a wish.

## Core Principles

1. **Intent before execution** — the system should know what it is trying to achieve before it optimizes how.
2. **Separate artifacts** — spec (what + why), plan (how), tasks (execution). Mixing them blurs review.
3. **Verifiable requirements** — a requirement is incomplete if nobody can tell whether it passed. Point at the evidence.
4. **Examples are part of the spec** — for data work, a sample input row plus its expected output row removes more ambiguity than a paragraph of business rules.
5. **Specs evolve** — update them when assumptions break, incidents surface missing intent, or implementation exposes hidden constraints.

## When To Spec (And When To Skip)

**Spec it when**
- the change carries business intent that won't be obvious from the diff
- behavior is observable downstream (outputs, contract changes, dashboards)
- multiple people or agents will touch the work
- the cost of getting it wrong is asymmetric (silent data drift, compliance, downstream contracts)

**Skip the ceremony if**
- the fix is a one-line correction with obvious intent
- the change is reversible and contained
- you'd be the only reader of the spec

## Best Practices

### Make intent granular near the area of change

A whole-codebase spec is useless. The useful spec is dense around the slice you're touching now — schema, contract, transformation — and shallow everywhere else.

### Prefer notebook examples over prose

For data work, "show the before/after on a 5-row sample" beats two paragraphs of business rules. Notebooks double as both spec evidence and the verification step.

### Keep specs alive, or accept they'll lie

A static spec from sprint 1 will diverge from production by sprint 3. Either commit to updating the spec when behavior changes, or treat it as historical context — not as truth. There's no honest middle ground.

### Gate at the spec, not at the PR

Catching "this isn't what we wanted" at PR review is too late — the implementation cost is already sunk. The cheap moment to redirect is **after the spec, before the plan**.

## SDD In Claude Code And Cursor

The workflow is tool-agnostic. The most direct way to adopt it in either tool is **GitHub Spec Kit**, which installs slash commands for the four phases and works across Claude Code, Cursor, Copilot, Codex, Gemini, and others. In this metarepo, skills under `skills-for-planning/` and `skills-for-docs/` operationalize the same phases natively — no separate toolkit required.

## Anti-patterns

- writing code before the target behavior is stable enough to spec
- hiding business rules only in implementation — the next engineer has to reverse-engineer them
- treating a generated plan as approved by default — review it like you'd review code
- acceptance criteria nobody can observe ("the system should be robust")
- letting the code drift away from the documented intent without updating the spec
- copying a spec template without filling in concrete examples — examples are what carry intent

## Pre-flight Checklist

Before moving from Spec to Plan:

- [ ] Problem statement and goals named
- [ ] Non-goals listed — scope is bounded, not just stated
- [ ] At least one concrete input/output example (for data: a sample row)
- [ ] Acceptance criteria are observable
- [ ] Assumptions and open questions surfaced, not glossed over
- [ ] The spec answers *why*, not just *what*

## SDD In This Framework

SDD is the conceptual backbone of the development lifecycle in this metarepo. The cycle runs: **Context → Spec → Plan → Build → Document**, with two validation gates (Plan Gate, PR Gate) and three human review points guarding progress between phases. Skills operationalize each phase — spec grilling, plan generation, slice implementation, docs closure — and the spec stays the source of intent throughout.

See [../onboarding/lifecycle.md](../onboarding/lifecycle.md) for the full cycle, gate criteria, and skill map.

## Where To Look Next

- [skills.md](skills.md)
- [subagents.md](subagents.md)

## References

- GitHub — [Spec Kit](https://github.com/github/spec-kit) (open-source toolkit, Spec → Plan → Tasks → Implement)
- GitHub Blog — [Spec-driven development with AI: get started](https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/)
- AWS Kiro — [Specs documentation](https://kiro.dev/docs/specs/) and [Best practices](https://kiro.dev/docs/specs/best-practices/)
- Martin Fowler — [Understanding Spec-Driven Development: Kiro, Spec Kit, Tessl](https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html)
- Towards Data Science — [From Vibe Coding to Spec-Driven Development](https://towardsdatascience.com/from-vibe-coding-to-spec-driven-development/)
