---
name: make-glossary
phase: spec
description: |
  Create or refresh a DDD-style glossary aligned with Spec-Driven Development. Use when the user wants to define domain terms, build or update a glossary, resolve terminology drift, create a ubiquitous language, align specs/tests/notebooks/business reports around canonical terms, or mentions DDD, domain language, glossary, naming ambiguity, business terms, metrics, labels, lifecycle states, or bounded context.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
metadata:
  owner: Ignacio Freire
  last_reviewed: "2026-05-27"
  skill-version: "1.0.0"
---

# Make Glossary

Create or refresh a domain glossary that business experts, developers, analysts, notebooks, specs, tests, dashboards, and reports can share. Capture domain meaning in Definition columns; put code, schema, and report identifiers only in the skeleton's designated identifier columns.

The live glossary lives at `docs/glossary.md` in the target repo. If it exists, update it in place — never create a competing one. If it does not exist, create it at that path using the structure described under "Required Structure" below.

## Ownership of `docs/glossary.md`

Three skills touch the glossary. Each has a distinct role:

| Skill | Role | When it runs |
|---|---|---|
| **`make-glossary`** (this one) | **Owner.** Creates and refreshes the full glossary as a deliberate spec activity. | The user asks to build, refresh, or audit the glossary. |
| `grill-me` | Editor. Adds or refines individual terms inline as decisions crystallise during an interview. | Mid-interview, when a term is resolved. |
| `business-reports` | Consumer. Reads it as the translation layer. Only writes an **ad-hoc** glossary at `docs/features/<scope_slug>/glossary.md` when no root glossary exists and a report is being produced. | Phase 0–2 of a report. |

Conflicts in scope: the root glossary at `docs/glossary.md` is the source of truth; ad-hoc glossaries are scoped to a single report and never override the root. If `business-reports` creates an ad-hoc glossary that later proves to have project-wide value, promote it through `make-glossary`, not by editing in place.

## SDD Role

The glossary is a support artifact for Spec-Driven Development:

- Specs use glossary terms for problem statements, target behavior, requirements, acceptance criteria, examples, and business rules.
- Plans and tasks use glossary terms to preserve traceability from business language to implementation.
- Tests, notebooks, metrics, dashboards, and reports should use canonical terms where domain-visible.
- If a spec, test, report, or code label uses a non-canonical term, record the mapping or flag the drift.

Do not let the glossary introduce new feature scope. If terminology work reveals new behavior, business rules, constraints, or acceptance criteria, mark them as open questions or spec updates.

## Workflow

1. Find the existing glossary: check `docs/glossary.md`, `glossary.md`, `docs/`, `glossary/`.
2. Read relevant sources: current conversation, specs, tickets, business rules, notebooks, dashboards, user-facing docs, and business reports named by the user.
3. Extract domain-relevant nouns, verbs, roles, lifecycle states, events, metrics, labels, segments, scores, and derived concepts.
4. Remove generic programming terms unless they carry domain meaning.
5. Identify synonyms, aliases, overloaded terms, vague labels, translation mismatches, and naming drift between business language and code/docs.
6. Choose one canonical term per concept. Prefer the term domain experts use when precise; otherwise choose the clearest term.
7. Add definitions, identifiers (code, schema, display labels), aliases to avoid, relationships, cardinality, metrics constraints, legacy drift mappings, flagged ambiguities, open questions, and change log entries.
8. Write or update the glossary using the template structure. Follow the skeleton's Instantiation Guidance order when creating from scratch.
9. Summarize changes and call out blocking terminology questions.

Ask before writing only when ambiguity blocks a safe glossary update, such as two plausible canonical terms with different business meaning. Otherwise make a reasonable recommendation and mark the ambiguity as open.

## Output Location

- Use the existing glossary path when one exists.
- If none exists, create `docs/glossary.md` unless the user requests another path.

## Required Structure

Use the `agent-kit/skeletons/_glossary.md` skeleton as the canonical layout. Sections, in order:

- **0. Metadata** — scope/area, owner, business reviewer, business language, code/schema language, naming notes, status (`draft | reviewed | implemented | superseded`), last reviewed.
- **1. Principles** — naming principles for this scope, plus **Naming Conventions** (project overrides for Python, SQL, API, reports, suffixes, acronyms).
- **2. Canonical Terms** — grouped into Domain Objects, Roles, Lifecycle States and Events. Each row includes term, one-sentence definition, code identifier, schema label (when applicable), display label, and aliases to avoid inline.
- **3. Domain Verbs** — business actions with actor, object, code action, and event name (if any).
- **4. Metrics, Labels, Derived Concepts** — with source/formula, code/SQL alias, display label, grain, window, unit, and null handling when relevant.
- **5. Relationships** — structured table with from, to, cardinality, trigger/rule, and code/FK hint.
- **6. Legacy And Drift Mapping** — only when canonical identifiers in §2–§4 differ from existing code, schema, or reports; not a class/module catalog.
- **7. Flagged Ambiguities** — term, problem, recommendation, status.
- **8. Example Dialogue** — short conversation using canonical terms, showing at least one boundary, relationship, or lifecycle rule.
- **9. Open Questions** — with blocking status and owner.
- **10. Change Log** — date, change, reason.
- **Instantiation Guidance** — suggested fill order when creating from scratch.
- **Review Checklist** — see below.

Canonical identifiers live in §2–§4 columns. §6 records legacy exceptions only. Aliases to avoid live inline in the canonical-terms tables, not as a separate section. Keep sections that do not apply as `not applicable` with a short reason when creating a formal glossary. For a small refresh, preserve the existing structure and add only what is needed.

## Rules

- Be opinionated: one canonical term per concept, one concept per canonical term.
- Define what the term is in one sentence; avoid defining only by behavior or formula.
- Use domain language. Skip classes, functions, endpoints, files, and frameworks unless the name is domain-visible.
- Keep translations explicit when business language and code language differ.
- Do not use the same word for different concepts inside one scope.
- Include aliases to avoid when synonyms are common or risky.
- Flag vague terms that hide business rules, thresholds, labels, or decision criteria.
- Include examples for edge cases, lifecycle boundaries, metrics, and overloaded terms.
- Put canonical identifiers in §2–§4 columns; use §6 only for legacy or drift exceptions.
- Do not restate implementation trivia in Definition columns — classes, modules, and file paths belong in identifier columns or §6 when they prevent drift.
- If a blocking assumption affects requirements, contracts, privacy, or acceptance criteria, surface it as a question for the spec.

## Review Checklist

- [ ] Every term is domain-relevant and defined in one sentence.
- [ ] Canonical terms are opinionated; aliases to avoid are listed where useful.
- [ ] Ambiguities are flagged explicitly.
- [ ] Relationships and cardinality are documented where useful.
- [ ] Every code-visible term has a Code identifier (or explicit `not applicable`).
- [ ] Verbs that become functions or events have Code action / Event name filled.
- [ ] Metrics include meaning, source/formula, grain, window, unit, and null handling when applicable.
- [ ] Legacy mappings in §6 are exceptions, not duplicates of §2–§4.
- [ ] Example dialogue uses canonical terms naturally.
- [ ] Specs, ACs, tests, notebooks, dashboards, reports, and code labels can reference the glossary without drift.
- [ ] Open questions are marked blocking or safe-to-defer.
- [ ] New behavior or rules discovered while writing are routed back to the spec.
- [ ] Change log records meaningful updates.

## Re-Running

When updating an existing glossary:

1. Read the current glossary first.
2. Add terms from new conversation, specs, tickets, notebooks, dashboards, reports, or code labels.
3. Update definitions when understanding changes.
4. Re-flag new or unresolved ambiguities.
5. Update relationships, metrics, mappings, and aliases.
6. Rewrite the example dialogue only if new terms change the domain story.
7. Add a change log entry.

---

## Related skills

- [`grill-me`](../../utils-skills/grill-me/SKILL.md) — editor of `docs/glossary.md`. Run it when the goal is to resolve individual terms, not to refresh the whole glossary.
- [`business-reports`](../business-reports/SKILL.md) — consumer of the glossary. Ad-hoc glossaries it creates can be promoted here.
- [`to-prd`](../../skills-for-planning/to-prd/SKILL.md) — PRDs use glossary terms throughout; refresh the glossary before writing the PRD when vocabulary is in flux.
