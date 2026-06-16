# Skills

This folder contains the skills catalog used by the metarepo.

For the conceptual guide, see [guides/theory/skills.md](../guides/theory/skills.md).

## Purpose

`skills/` contains reusable capabilities anchored by a `SKILL.md` file. Each skill declares one lifecycle `phase` (`context`, `spec`, `plan`, `build`, `document`, `cross-cutting`) and lives in its own folder.

## Development cycle map

Skills slot into the five-phase lifecycle. The arrows show the primary sequence; cross-cutting skills can be invoked at any point.

```
Context ──► Spec ──[Spec Review]──► Plan ──[Plan Review]──► Build ──[PR Review]──► Document
```

| Phase | Skill | What it produces |
|---|---|---|
| Context | [`context-load`](./utils-skills/context-load/SKILL.md) | Project and feature context loaded in the session |
| Spec | [`grill-me`](./utils-skills/grill-me/SKILL.md) | Ambiguity resolved; glossary updated inline |
| Spec | [`make-glossary`](./skills-for-docs/make-glossary/SKILL.md) | `docs/glossary.md` created or refreshed |
| Spec | [`spec-write`](./skills-for-planning/spec-write/SKILL.md) | `docs/features/<feature>/specs.md` |
| Plan | [`plan-write`](./skills-for-planning/plan-write/SKILL.md) | `docs/features/<feature>/plan.md`; optional tracker issues |
| Build | [`build-slice`](./skills-for-planning/build-slice/SKILL.md) | One vertical TDD slice from `plan.md` |
| Build | [`notebook-mockup`](./skills-for-planning/notebook-mockup/SKILL.md) | Validated logic notebook before production code |
| Document | [`context-update`](./utils-skills/context-update/SKILL.md) | All durable docs reconciled at cycle close |
| Document | [`business-reports`](./skills-for-docs/business-reports/SKILL.md) | Business-facing report at cycle close |
| Document | [`pr-summary`](./skills-for-docs/pr-summary/SKILL.md) | Structured PR description for the reviewer |
| Cross-cutting | [`handoff`](./utils-skills/handoff/SKILL.md) | Session handoff notes for the next agent |
| Cross-cutting | [`mermaid-diagrams`](./utils-skills/mermaid-diagrams/SKILL.md) | Architecture or flow diagrams |

See [guides/onboarding/lifecycle.md](../guides/onboarding/lifecycle.md) for the full per-phase guidance.

---

## Current Catalog

### Planning — `skills-for-planning/`

| Skill | Phase | Path |
|---|---|---|
| `spec-write` | spec | [skills-for-planning/spec-write/SKILL.md](./skills-for-planning/spec-write/SKILL.md) |
| `plan-write` | plan | [skills-for-planning/plan-write/SKILL.md](./skills-for-planning/plan-write/SKILL.md) |
| `build-slice` | build | [skills-for-planning/build-slice/SKILL.md](./skills-for-planning/build-slice/SKILL.md) |
| `notebook-mockup` | cross-cutting | [skills-for-planning/notebook-mockup/SKILL.md](./skills-for-planning/notebook-mockup/SKILL.md) |

### Documentation — `skills-for-docs/`

| Skill | Phase | Path |
|---|---|---|
| `make-glossary` | spec | [skills-for-docs/make-glossary/SKILL.md](./skills-for-docs/make-glossary/SKILL.md) |
| `business-reports` | document | [skills-for-docs/business-reports/SKILL.md](./skills-for-docs/business-reports/SKILL.md) |
| `pr-summary` | document | [skills-for-docs/pr-summary/SKILL.md](./skills-for-docs/pr-summary/SKILL.md) |

### Utilities — `utils-skills/`

| Skill | Phase | Path |
|---|---|---|
| `context-load` | context | [utils-skills/context-load/SKILL.md](./utils-skills/context-load/SKILL.md) |
| `context-update` | document | [utils-skills/context-update/SKILL.md](./utils-skills/context-update/SKILL.md) |
| `grill-me` | cross-cutting | [utils-skills/grill-me/SKILL.md](./utils-skills/grill-me/SKILL.md) |
| `handoff` | cross-cutting | [utils-skills/handoff/SKILL.md](./utils-skills/handoff/SKILL.md) |
| `mermaid-diagrams` | cross-cutting | [utils-skills/mermaid-diagrams/SKILL.md](./utils-skills/mermaid-diagrams/SKILL.md) |

## SKILL.md structure

Every `SKILL.md` opens with this frontmatter and follows the skeleton below. Section headings may use domain-specific names when clearer; what matters is that the intent is present.

```markdown
---
name: <kebab-case>                # required, matches folder name
phase: <one of the phases above>  # required
description: <one paragraph: what it does and when to invoke>
allowed-tools: [Read, Write, ...] # required, [] if none
metadata:
  owner: <name>
  last_reviewed: "YYYY-MM-DD"
  skill-version: "X.Y.Z"
# argument-hint: <only for slash-command skills>
---

# <Skill Name>                    (H1 matches `name:` in Title Case)

<purpose paragraph>                (required)

## When to use                     (required — triggers; "When NOT to use" optional)
## Workflow                        (required if multi-step; alt names OK)
## Rules                           (required if hard contracts; alt names OK)
## Anti-patterns                   (recommended — table)
## Reference index                 (required if references/, templates/, examples/, scripts/ exist)
## Related skills                  (required — at least 2 links)
```

Narrow skills (handoff) may ship with only purpose + workflow + Related.

When adding or editing a skill, run `python skills/lint.py` from the repo root to validate the `SKILL.md` frontmatter, required fields, folder/`name:` match, and internal links before committing. It does not scaffold a new skill — it only checks what already exists.

## Language policy

- Default to the user's language for conversation; glossary terms stay canonical.
- Generated artifacts follow the glossary's language (fall back to user's language).
- Frontmatter and code identifiers are always English (ASCII).

## Maintenance Rules

- folder names in `kebab-case`; `name:` must match the folder name
- mermaid rules live only in [utils-skills/mermaid-diagrams/references/style.md](./utils-skills/mermaid-diagrams/references/style.md) — reference, don't restate
- deprecate by replacing `SKILL.md` with a pointer and removing the folder next release
- keep this README a catalog — do not duplicate skill content here
