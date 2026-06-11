---
name: grill-me
phase: cross-cutting
description: |
  Interview the user relentlessly about a plan, design, or proposal, walking down each branch of the decision tree and resolving dependencies one question at a time, with a recommendation for each question. Also challenges the plan against existing domain docs (docs/glossary.md and docs/adr/), sharpens terminology, and updates documentation inline as decisions crystallise. Use whenever the user says "grill me", asks to stress-test or be challenged on a design, wants every aspect of a proposal questioned, or wants to align a plan with the project's documented language and decisions.
allowed-tools:
  - Read
  - Edit
  - Write
  - Glob
  - Grep
metadata:
  owner: Ignacio Freire
  last_reviewed: "2026-05-27"
  skill-version: "2.0.0"
---

# Grill Me

The user has invited a hard interview. Soft-pedalling wastes their time.

- **One question per turn.** Never bundle.
- **Resolve in dependency order.** Upstream choices constrain downstream ones; settle them first.
- **Recommend an answer with its trade-off**, even when listing options. The user's job is to confirm, override, or push back — not to choose blindly.
- **Resolve from sources before asking.** If a question can be answered by reading the codebase, fetching a spec, or running a tool, do that instead of asking the user.
- **Make questions answerable in a sentence** or with a single option choice when choices are pre-enumerated.
- **Acknowledge when an answer changes earlier assumptions**, then move on. Don't re-litigate.
- **End the interview explicitly** when the decision tree is exhausted. Summarise resolved decisions and offer next steps.

---

## Domain awareness

During the interview, also load existing documentation for context:

- `docs/glossary.md` — canonical domain vocabulary
- `docs/adr/` — architectural decisions made previously
- `docs/context/project.md` — project-level truth

If the repo has multiple contexts (indicated by a `docs/context-map.md`), load the relevant one.

---

## Challenge against the glossary

When the user uses a term that conflicts with the existing language in `docs/glossary.md`, call it out immediately. *"The glossary defines 'cancellation' as X, but you seem to mean Y — which is it?"*

## Sharpen fuzzy language

When the user uses vague or overloaded terms, propose a precise canonical term. *"You're saying 'account' — do you mean the Customer or the User? Those are different things."*

## Discuss concrete scenarios

When domain relationships are being discussed, stress-test them with specific scenarios. Invent scenarios that probe edge cases and force the user to be precise about the boundaries between concepts.

## Cross-reference with code

When the user states how something works, check whether the code agrees. If you find a contradiction, surface it: *"Your code cancels entire Orders, but you just said partial cancellation is possible — which is right?"*

## Update docs/glossary.md inline

When a term is resolved, update `docs/glossary.md` right there. Don't batch these up — capture them as they happen. Use the format in `agent-kit/skeletons/_glossary.md`: meaning in Definition columns; code, schema, and display identifiers in the designated identifier columns only.

Do not put classes, modules, file paths, or implementation decisions in Definition columns. Do not treat the glossary as a spec or scratch pad. Canonical identifiers belong in §2–§4; legacy or conflicting names belong in §6 only.

> **Ownership note.** This skill is the **editor** of `docs/glossary.md`; it adds or refines individual terms during interviews. Wholesale creation and refresh of the glossary is owned by [`make-glossary`](../../skills-for-docs/make-glossary/SKILL.md) — defer there when the request is "build the glossary" rather than "resolve this term".

## Offer ADRs sparingly

Only offer to create an ADR in `docs/adr/` when all three are true:

1. **Hard to reverse** — the cost of changing your mind later is meaningful
2. **Surprising without context** — a future reader will wonder "why did they do it this way?"
3. **The result of a real trade-off** — there were genuine alternatives and you picked one for specific reasons

If any of the three is missing, skip the ADR.

---

## Reference index

| File | What it covers |
|---|---|
| `agent-kit/skeletons/_glossary.md` | Format for `docs/glossary.md` entries |

---

## Related skills

- [`make-glossary`](../../skills-for-docs/make-glossary/SKILL.md) — wholesale glossary creation. Defer here when the request is "build the glossary" rather than "resolve this term".
- [`spec-write`](../../skills-for-planning/spec-write/SKILL.md) — often invoked **after** grill-me to crystallise the conversation into a spec.
- [`design-write`](../../skills-for-planning/design-write/SKILL.md) — run grill-me first when the plan has open ambiguity that would otherwise burn slices.
