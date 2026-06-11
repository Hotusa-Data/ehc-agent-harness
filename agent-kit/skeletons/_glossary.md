# Domain Glossary

Shared domain language for specs, plans, tests, notebooks, dashboards, reports, and code labels.

Instantiate at `docs/glossary.md`. Update in place if it already exists; never create a competing file.

Fill what is known. Use `unknown — needs confirmation` instead of guessing. Use `not applicable` with a short reason when a subsection does not apply. Remove empty placeholder rows once real terms exist.

Meaning lives in Definition columns. Code, schema, and report identifiers live only in the designated identifier columns — not in definitions, not as a class or module catalog.

## 0. Metadata

- Scope / area:
- Owner:
- Business reviewer:
- Business language (prose, ACs, reports):
- Code / schema language (identifiers):
- Naming notes (project overrides to agent-kit python/persistence rules):
- Status: draft | reviewed | implemented | superseded
- Last reviewed:

## 1. Principles

- One canonical term per concept; one concept per canonical term.
- Prefer the term domain experts already use when precise.
- Define terms **before** using them in specs, ACs, tests, metrics, or output labels.
- Do not use the same word for different concepts inside the same scope. Split by context if needed.
- Avoid vague labels that hide thresholds, scoring rules, segments, or lifecycle states.
- Terminology work must not introduce new scope; if it reveals new behavior, route it to the spec.

### Naming Conventions

Fill once per project. Point to agent-kit rules for defaults; record only overrides.

- Python modules / classes / functions:
- SQL tables / columns:
- API / JSON fields:
- Report / dashboard labels:
- Standard suffixes (`_id`, `_at`, `_df`, …):
- Acronyms (allowed / spell out once):
- Aliases never to use in code:

## 2. Canonical Terms

Group by subdomain, lifecycle, or actor. Add tables as needed.

Suggested prompts while filling:

- Which nouns appear in requirements, dashboards, or stakeholder docs?
- Which terms already exist in code or schema with a different spelling?
- Which concepts need a Display label different from the canonical Term?

### Domain Objects

| Term | Definition | Code identifier | Schema label | Display label | Aliases to avoid | Notes |
|---|---|---|---|---|---|---|
| **<Object>** | One-sentence definition. | `<snake_case>` | `<table.column>` | Human label |  |  |

### Roles

| Term | Definition | Code identifier | Display label | Aliases to avoid |
|---|---|---|---|---|
| **<Role>** |  | `<snake_case>` | Human label |  |

### Lifecycle States And Events

| Term | Kind | Definition | Code identifier | Display label | Aliases to avoid |
|---|---|---|---|---|---|
| **<State>** | State | Durable condition. | `<enum_value>` | Human label |  |
| **<Event>** | Event | Fact that occurred. | `<event_name>` | Human label |  |

## 3. Domain Verbs

Business actions only. Skip generic verbs unless the domain uses them precisely.

| Verb | Definition | Actor | Object | Code action | Event name (if any) |
|---|---|---|---|---|---|
| **<Verb>** |  |  |  | `<function_or_command>` | `<Event>` |

## 4. Metrics, Labels, Derived Concepts

Computed metrics, statuses, segments, scores, dashboard labels, exported columns.

| Term | Definition | Source / formula | Code / SQL alias | Display label | Grain | Window | Unit | Null handling |
|---|---|---|---|---|---|---|---|---|
| **<Metric>** |  |  | `<column_or_key>` |  |  |  |  |  |

- Define what the metric **means**, not only its formula.
- If it affects ACs, scoring, ranking, filtering, or segmentation, link the spec or business rule.

## 5. Relationships

| From | To | Cardinality | Trigger / rule | Code / FK hint |
|---|---|---|---|---|
| **<Term A>** | **<Term B>** | 1:1 / 1:N / N:M |  |  |
| **<Event>** | **<Object>** | — | Changes **<State 1>** to **<State 2>**. |  |

## 6. Legacy And Drift Mapping

Use only when the canonical identifier in §2–§4 differs from existing code, schema, or reports. Not a catalog of every class or module.

| Domain term | Legacy label | Canonical (see §2–§4) | Notes |
|---|---|---|---|
| **<Term>** | `<old_name>` | `<canonical_identifier>` |  |

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

## Instantiation Guidance

Suggested order:

1. §0 Metadata + §1 Naming Conventions
2. §2 Domain Objects (minimum viable glossary: 5–10 core terms with Code identifier)
3. §3 Verbs for actions that become functions or events
4. §4 Metrics only if the project exposes computed labels
5. §5 Relationships where cardinality affects design
6. §6 only for legacy or conflicting names found in the codebase

Subsections with no terms yet: keep the heading, write `not applicable — <reason>`, remove placeholder rows.

## Review Checklist

- [ ] Every term is domain-relevant and defined in one sentence.
- [ ] Canonical terms are opinionated; aliases to avoid are listed where useful.
- [ ] Every code-visible term has a Code identifier (or explicit `not applicable`).
- [ ] Verbs that become functions or events have Code action / Event name filled.
- [ ] Ambiguities are flagged explicitly.
- [ ] Metrics include meaning, source/formula, grain, window, unit, and null handling when applicable.
- [ ] Legacy mappings in §6 are exceptions, not duplicates of §2–§4.
- [ ] Example dialogue uses terms naturally.
- [ ] New behavior or rules discovered while writing routed back to the spec.
