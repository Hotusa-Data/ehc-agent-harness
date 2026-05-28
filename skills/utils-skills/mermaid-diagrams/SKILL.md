---
name: mermaid-diagrams
phase: cross-cutting
description: |
  Mermaid diagram creation guide — type selection, style rules, and exemplars for the 8 supported types (ER, C4, architecture-beta, block, flowchart, sequence, state, mindmap). Use when a diagram is needed in any document, when choosing between diagram types, or when another skill needs to embed a Mermaid block. Trigger phrases: "add a diagram", "visualize this", "show the flow", "diagram the architecture", "which diagram type should I use". Do NOT use for data charts with real numbers (bar, scatter, line, pie — use a charting library), photorealistic images, or Mermaid types outside the 8 covered (gantt, kanban, radar, sankey, timeline, class, xy_chart).
allowed-tools:
  - Read
  - Write
  - Edit
metadata:
  owner: Ignacio Freire
  last_reviewed: "2026-05-27"
  skill-version: "3.0.0"
---

# Mermaid Diagrams

Guide for creating Mermaid diagrams: when to use each type, mandatory style rules, and where to find exemplars.

---

## 🔍 Pick the right type

The most common mistake is defaulting to flowchart for everything. Match the content to the type before writing a single line.

| Use case | Type | Keyword |
|---|---|---|
| Data model / schema / entity relationships | ER | `erDiagram` |
| Layered system architecture (containers, contexts) | C4 | `C4Container` / `C4Context` |
| Cloud infrastructure / named services / topology | Architecture | `architecture-beta` |
| Spatial or component layout | Block | `block-beta` |
| Workflow / decision logic / conditional branches | Flowchart | `flowchart` |
| Temporal interactions between actors / API calls | Sequence | `sequenceDiagram` |
| State machine / object lifecycle | State | `stateDiagram-v2` |
| Concept hierarchy / topic breakdown | Mindmap | `mindmap` |

Read `references/diagrams.md` for the exemplar and type-specific rules of the chosen type.

**Outside the 8**: for gantt, pie, kanban, radar, sankey, timeline, class, xy_chart — use the dedicated tool for the job rather than forcing Mermaid.

---

## 🖼️ Mandatory rules for every diagram

Every Mermaid block must open with:

```
accTitle: Short Name 3-8 Words
accDescr: One or two sentences describing what this diagram shows.
```

**Never:**
- `%%{init}` directives — breaks GitHub dark mode
- Inline `style` — use `classDef` only
- Variable, function, or class names in labels — labels are domain language, not code

**Always:**
- Node IDs in `snake_case`, matching the label
- No emojis in node labels — keep diagrams clean and tool-renderable
- Edge labels on every decision branch — an unlabeled branch is ambiguous

Full syntax reference in `references/style.md` (Mermaid section only).

---

## ✅ Verify before delivering

- [ ] `accTitle` + `accDescr` present
- [ ] No `%%{init}`, no inline `style`, only `classDef`
- [ ] Decision branches have edge labels
- [ ] Labels use domain language, not code identifiers
- [ ] Right type chosen — not flowchart by default

---

## 📚 References

| File | What it covers |
|---|---|
| `references/diagrams.md` | 8 diagram types — exemplars and type-specific rules |
| `references/style.md` | Mermaid syntax and style rules — canonical source for the whole catalog |

---

## 📄 Document templates with embedded Mermaid

Pre-built markdown templates for full documents that integrate Mermaid blocks. Use as a starting point when the goal is a complete document, not a standalone diagram. Each template links back to `references/style.md` for formatting rules.

| Template | When to use |
|---|---|
| `templates/decision_record.md` | ADRs / RFCs — decisions that need context, options compared, and rationale preserved |
| `templates/issue.md` | Bug reports or feature requests stored as repo-resident markdown (bug + feature variants inside) |
| `templates/pull_request.md` | PR description as a persistent file — change inventory, testing evidence, rollback plan |
| `templates/kanban.md` | Sprint / project boards with Mermaid kanban diagram and work-item tables |
| `templates/status_report.md` | Weekly / monthly status updates and executive briefings with traffic-light health |
| `templates/presentation.md` | Slide-deck-style briefings, lectures, walkthroughs (reads as doc and as speaker notes) |
| `templates/research_paper.md` | Research papers, technical analyses, literature reviews — heavy citation, structured argument |
| `templates/how_to_guide.md` | Tutorials, runbooks, onboarding walkthroughs — verifiable step-by-step |
| `templates/project_documentation.md` | Main project README or `docs/index.md` — quick start, architecture, contribution guide |

[^1]: Mermaid. "Mermaid Diagramming and Charting Tool." https://mermaid.js.org/

---

## Related skills

- [`business-reports`](../../skills-for-docs/business-reports/SKILL.md) — heaviest consumer; its selection guide in [`references/diagrams.md`](../../skills-for-docs/business-reports/references/diagrams.md) points back here for syntax.
- [`implementation-planning`](../../skills-for-planning/implementation-planning/SKILL.md) — plans often embed flowcharts or sequence diagrams.
- [`to-prd`](../../skills-for-planning/to-prd/SKILL.md) — PRDs may include high-level decision flows or system context.
