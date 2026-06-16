---
name: business-reports
phase: document
description: |
  Produce structured markdown reports — with inline Mermaid diagrams — that explain what code does to non-developers. Use whenever someone wants to translate code into business language, hand off a feature or subsystem to a PM, analyst, or new joiner, or produce a document readable by both technical and business audiences. Trigger on phrases like "business flow", "system narrative", "handover", "context.md", "explica esta feature para negocio", "documenta este sistema para el PM", "explicar este módulo a negocio", or any equivalent request to explain code without using identifier names. Two types only: `business-flow` (one feature, step by step) and `system-narrative` (a subsystem organized by business intentions). Do NOT use for technical-only documentation (API references, class hierarchies, installation READMEs) — wrong audience.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
metadata:
  owner: Ignacio Freire
  last_reviewed: "2026-05-28"
  skill-version: "2.1.0"
---

# Business Reports

Produce markdown documents — with embedded Mermaid diagrams as the visual source of truth — that explain what code does to people who don't open the code. Two types, one shared frame, one non-negotiable rule: **no identifier names, no technical jargon, no open questions in the final output**.

---

## When to use

- The user wants to explain code to a PM, analyst, or new joiner in business language.
- A feature or subsystem needs a handover document readable without opening the codebase.
- Trigger phrases: "business flow", "system narrative", "handover", "explica esta feature para negocio", "documenta este sistema para el PM".

## When NOT to use

- Technical-only documentation (API references, class hierarchies, installation READMEs) — wrong audience.
- The request is still ambiguous — run [`grill-me`](../../utils-skills/grill-me/SKILL.md) or resolve terms via [`make-glossary`](../make-glossary/SKILL.md) first when vocabulary is missing.
- The user wants a PR review summary — use [`pr-summary`](../pr-summary/SKILL.md) instead.

---

## 📋 Report types

| Type | Anchor diagram | Register | What it covers |
|---|---|---|---|
| **`business-flow`** | Flowchart | `business` | A feature step by step — decision branches, business rules, outcomes. |
| **`system-narrative`** | Intention map (flowchart LR + subgraphs) | `mixed` | A subsystem organized by business intentions, readable by a PM without opening technical details. |

The list is **closed**. If the request doesn't fit either, stop and ask.

---

## 📐 Shared frame — six sections

Every report has six sections in this order. Section 4 varies by type; the rest are identical.

| § | Name | Content |
|---|---|---|
| 1 | **Frontmatter** | YAML: `report_type`, `scope`, `language`, `generated_at`, `glossary_version`, `code_commit` |
| 2 | **Executive summary** | 3-5 sentences in domain language — problem, audience, trigger, outcome |
| 3 | **Anchor diagram** | Mandatory for the type; always carries `accTitle` + `accDescr` |
| 4 | **Body** | Defined by `templates/<report_type>.md` |
| 5 | **Hypotheses 💡 and limitations ⚠️** | Flat list — domain language. `business-flow`: business-visible items only. `system-narrative`: both families, each tagged with its intention. |
| 6 | **Appendix — Code traceability** | Table: domain concept → file(s) → function/class. Prose never references it visibly. |

Deliberately absent: table of contents (renderers generate it), open questions (resolved before writing), changelog (lives in git). Inline glossary appears only as a fallback when ad-hoc terms can't be promoted to the root glossary.

---

## 🔤 Register and language

Register is **fixed by type, no override** (`business-flow` → `business`, `system-narrative` → `mixed`). Full rules and self-check in `references/registers.md` — read before writing any prose.

Language follows the glossary's default; if `glossary_version` is `ad-hoc-promoted` or `ad-hoc-inline`, follow the user's language. Frontmatter declares it as `language: <ISO 639-1>`. Don't mix languages within prose or within a single diagram.

---

## ⚙️ Workflow — five phases

**Hard contract: nothing gets written until the outline (phase 3) is confirmed.**

| Phase | What happens |
|---|---|
| **0 — Inputs** | Verify scope, report type, glossary, language. Stop and ask if missing. |
| **1 — Silent analysis** | Read glossary and code. Produce three internal lists: questions, commitments, tentative 💡/⚠️. |
| **2 — Grilling + summary** | Ask ambiguities with a recommendation each. Present an assumptions summary (4-8 items) for full confirmation. |
| **3 — Outline** | Present sections, diagrams, 💡/⚠️ count. Confirm before writing. |
| **4 — Write** | Compose following frame, template, register, style, and diagram rules. Hard-return to phase 2 if a new ambiguity surfaces. |

**Fast path** (auto-confirm signaled, or phase 1 found nothing to ask): skip phase 2, go to outline, append a brief assumptions note at the end of the report.

**Read `references/workflow.md`** for the full protocol — grilling format, assumptions structure, outline example, hard-return policy, glossary handling, code commit capture, size targets, refresh mode, output paths, and the contract.

> **Glossary ownership.** This skill **consumes** `docs/glossary.md` (read-only). Promote project-wide terms through [`make-glossary`](../make-glossary/SKILL.md) — never edit the root from here.

---

## 🖼️ Diagrams

Mermaid syntax, palette, exemplars, and per-type rules live in [`utils-skills/mermaid-diagrams`](../../utils-skills/mermaid-diagrams/SKILL.md) — that skill is the single source of truth. Read it before writing any diagram block.

`references/diagrams.md` is the **selection guide for this skill only**: which diagram type fits each report type, the intention-map composition pattern, and the business-register overlays (business actor names, business event labels, single-node system in C4Context).

Before including a Mermaid block, run the sanity checker: `scripts/check_mermaid.sh` (bash) or `scripts/check_mermaid.ps1` (PowerShell). If a block flags, fix once and re-run; if still broken, return to phase 2.

---

## Related skills

- [`mermaid-diagrams`](../../utils-skills/mermaid-diagrams/SKILL.md) — single source of truth for Mermaid syntax; this skill consumes it heavily.
- [`make-glossary`](../make-glossary/SKILL.md) — owner of `docs/glossary.md`. Promote ad-hoc terms here when they prove project-wide.
- [`grill-me`](../../utils-skills/grill-me/SKILL.md) — invoke when phase 2 surfaces enough ambiguity to warrant a structured interview.
