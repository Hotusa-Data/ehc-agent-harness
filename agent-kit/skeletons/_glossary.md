# Domain Glossary

Shared domain language used by specs, plans, tests, notebooks, dashboards, business reports, and user-facing docs. Captures **meaning**, not implementation trivia.

Instantiate at `docs/glossary.md`. Update in place if it already exists; never create a competing file.

## 0. Metadata

- Scope / area:
- Owner:
- Business reviewer:
- Status: draft | reviewed | implemented | superseded
- Last reviewed:

## 1. Principles

- One canonical term per concept; one concept per canonical term.
- Prefer the term domain experts already use when precise.
- Define terms **before** using them in specs, ACs, tests, metrics, or output labels.
- Do not use the same word for different concepts inside the same scope. Split by context if needed.
- Avoid vague labels that hide thresholds, scoring rules, segments, or lifecycle states.
- Terminology work must not introduce new scope; if it reveals new behavior, route it to the spec.

## 2. Canonical Terms

Group by subdomain, lifecycle, or actor. Add tables as needed.

### Domain Objects

| Term | Definition | Aliases to avoid | Notes |
|---|---|---|---|
| **<Object>** | One-sentence definition. |  |  |

### Roles

| Term | Definition | Aliases to avoid |
|---|---|---|
| **<Role>** |  |  |

### Lifecycle States And Events

| Term | Kind | Definition | Aliases to avoid |
|---|---|---|---|
| **<State>** | State | Durable condition. |  |
| **<Event>** | Event | Fact that occurred. |  |

## 3. Domain Verbs

Business actions only. Skip generic verbs unless the domain uses them precisely.

| Verb | Definition | Actor | Object |
|---|---|---|---|
| **<Verb>** |  |  |  |

## 4. Metrics, Labels, Derived Concepts

Computed metrics, statuses, segments, scores, dashboard labels, exported columns.

| Term | Definition | Source / formula | Display label | Unit / grain / window / null handling |
|---|---|---|---|---|
| **<Metric>** |  |  |  |  |

- Define what the metric **means**, not only its formula.
- If it affects ACs, scoring, ranking, filtering, or segmentation, link the spec or business rule.

## 5. Relationships

- A **<Term A>** belongs to exactly one **<Term B>**.
- A **<Event>** changes a **<Object>** from **<State 1>** to **<State 2>**.

## 6. Code / Schema / Report Mapping

Only mappings that prevent naming drift. Not a class/module catalog.

| Domain term | Code / schema / report label | Notes (legacy? linked spec?) |
|---|---|---|
| **<Term>** | `<code_name>` |  |

## 7. Flagged Ambiguities

| Ambiguous term | Problem | Recommendation | Status |
|---|---|---|---|
| `<word>` | Used for both **<Concept A>** and **<Concept B>**. | Use **<A>** for ...; **<B>** for .... | open |

## 8. Example Dialogue

Short conversation (3-5 exchanges) using only canonical terms. Shows at least one boundary, relationship, or lifecycle rule.

> **Dev:** "When a **<Term A>** reaches **<State>**, do we create a **<Term B>**?"
>
> **Domain expert:** "No. A **<Term B>** is created only after **<Event>**."

## 9. Open Questions

| ID | Question | Terms affected | Blocking? | Owner |
|---|---|---|---|---|
| Q1 |  |  | yes / no |  |

Mark as blocking when it affects requirements, contracts, privacy, security, ACs, or stakeholder-visible behavior.

## 10. Change Log

| Date | Change | Reason |
|---|---|---|
|  |  |  |

## Review Checklist

- [ ] Every term is domain-relevant and defined in one sentence.
- [ ] Canonical terms are opinionated; aliases to avoid are listed where useful.
- [ ] Ambiguities are flagged explicitly.
- [ ] Metrics include meaning, source/formula, units, grain, window, constraints.
- [ ] Example dialogue uses terms naturally.
- [ ] New behavior or rules discovered while writing routed back to the spec.
