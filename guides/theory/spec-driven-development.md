# Spec-Driven Development

A practical introduction to SDD for developers working with data — what the concept is, how it differs from vibe coding or TDD, and **how this metarepo adapts it** into a five-phase lifecycle rather than copying any single SDD toolkit verbatim.

## TL;DR

**Spec-Driven Development (SDD)** is an industry pattern: make the **specification** — not the code — the anchor for intent. External toolkits (Spec Kit, Kiro, BMAD, etc.) typically chain markdown artifacts before implementation.

**This framework does not run pure SDD.** We borrow the core idea — intent before code, verifiable acceptance criteria, specs that stay alive — and wrap it in our own **five-phase cycle** with human review gates:

```text
Context → Spec → Plan → Build → Document
```

Work slices live inside `plan.md`; there is no separate `tasks.md` artifact. Full reference: [lifecycle.md](../onboarding/lifecycle.md).

## Why SDD Exists

LLMs ship plausible code in seconds. That speed creates a failure mode worth naming: **vibe coding** — code that drifts from intent, hallucinates APIs, and rots as the project scales. In data work the drift is *silent*: a pipeline still runs, just on the wrong shape, the wrong filter, or the wrong join. Making intent explicit before broad implementation keeps divergence visible at review — not at the next quarterly metric. That is the SDD insight we keep.

## SDD vs Vibe Coding vs TDD vs BDD

| Approach | Source of truth | Strength | Where it breaks |
|---|---|---|---|
| Vibe coding | The prompt | Speed on small things | Drift, hallucinated APIs, decaying code |
| TDD | Failing test | Granular regression safety | Tests mirror implementation, not intent |
| BDD | Scenario in business language | Stakeholder alignment | Scales poorly past a few features |
| **SDD (concept)** | Versioned spec | Intent traceable through plan → code | Overhead on tiny fixes; needs spec discipline |

The four are not mutually exclusive. SDD-style specs can sit on top of TDD-style tests, and BDD scenarios make good acceptance criteria inside a spec.

## What SDD Toolkits Typically Do

Most external SDD toolkits converge on a linear artifact chain before code. Ours is **inspired by** this shape but not identical:

| Toolkit phase | Typical artifact | Our equivalent |
|---|---|---|
| Spec | `specs.md` | **Spec** phase → `docs/features/<feature>/specs.md` |
| Plan | `plan.md` (+ sometimes separate tasks) | **Plan** phase → `plan.md` with ordered slices inside |
| Implement | code + evidence | **Build** phase → vertical slices + tests/notebooks |
| — | — | **Context** (load rules/docs first) and **Document** (close durable knowledge) — extra phases we add |

We also add **three human review stops** (post-Spec, post-Plan, post-Build/PR) that most pure-SDD toolkits leave implicit.

## Anatomy Of A Feature Folder

```text
docs/features/<feature>/
|-- specs.md
|-- plan.md
|-- report.md       (created at cycle close)
`-- changelog.md
```

A useful `specs.md` covers: problem statement, goals, non-goals, current behavior, target behavior, requirements, acceptance criteria, examples, and assumptions plus open questions.

For data projects, "acceptance criteria" means **observable evidence**: expected schema shape, row count bounds, data quality checks, before/after diffs on a sample, or notebook cells that must pass. If you can't observe it, it isn't a criterion — it's a wish.

## Core Principles

1. **Intent before execution** — the system should know what it is trying to achieve before it optimizes how.
2. **Separate artifacts** — specs (what + why), plan (how + execution). Mixing them blurs review.
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

## Skills In Cursor

Skills under `skills-for-planning/` and `skills-for-docs/` operationalize the **five-phase lifecycle** — not a pure SDD toolkit. Each phase has optional skills (`grill-me`, `spec-write`, `plan-write`, `build-slice`, `context-update`, etc.). See [lifecycle.md](../onboarding/lifecycle.md) for the per-phase map.

## Anti-patterns

- writing code before the target behavior is stable enough to spec
- hiding business rules only in implementation — the next engineer has to reverse-engineer them
- treating a generated plan as approved by default — review it like you'd review code
- acceptance criteria nobody can observe ("the system should be robust")
- letting the code drift away from the documented intent without updating the spec
- copying a spec template without filling in concrete examples — examples are what carry intent
- treating this framework as "Spec Kit with another name" — our Context and Document phases, review gates, and slice-in-plan model are deliberate differences

## Pre-flight Checklist

Before moving from Spec to Plan:

- [ ] Problem statement and goals named
- [ ] Non-goals listed — scope is bounded, not just stated
- [ ] At least one concrete input/output example (for data: a sample row)
- [ ] Acceptance criteria are observable
- [ ] Assumptions and open questions surfaced, not glossed over
- [ ] The spec answers *why*, not just *what*

## SDD Inspiration In This Framework

SDD is the **conceptual backbone**, not the operating model. The cycle we actually run is:

**Context → Spec → Plan → Build → Document**, with three human review points guarding progress between phases.

- **Context** loads rules and project truth before anyone writes a spec.
- **Spec / Plan / Build** carry the SDD-inspired intent → plan → evidence chain.
- **Document** closes durable knowledge (glossary, changelog, `report.md`) — a phase most pure-SDD toolkits under-specify.

Skills operationalize each phase; the spec stays the source of intent throughout Build.

See [../onboarding/lifecycle.md](../onboarding/lifecycle.md) for exit criteria and the full skill map.

## Where To Look Next

- [skills.md](skills.md)
- [subagents.md](subagents.md)

## References

- GitHub — [Spec Kit](https://github.com/github/spec-kit) (open-source toolkit — inspiration, not our runtime)
- GitHub Blog — [Spec-driven development with AI: get started](https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/)
- AWS Kiro — [Specs documentation](https://kiro.dev/docs/specs/) and [Best practices](https://kiro.dev/docs/specs/best-practices/)
- Martin Fowler — [Understanding Spec-Driven Development: Kiro, Spec Kit, Tessl](https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html)
- Towards Data Science — [From Vibe Coding to Spec-Driven Development](https://towardsdatascience.com/from-vibe-coding-to-spec-driven-development/)
