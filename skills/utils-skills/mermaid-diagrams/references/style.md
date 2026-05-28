# Mermaid Style — single source of truth

Canonical rules for Mermaid syntax and styling across the entire skill catalog. Other skills (e.g. `business-reports`) point here instead of restating these rules. The diagram type catalog with full exemplars lives in [`diagrams.md`](./diagrams.md); the rules below apply to all eight covered types.

> **Markdown formatting rules** (heading hierarchy, lists, tables, `<details>`, separators, citations) live in [`skills-for-docs/business-reports/references/style.md`](../../../skills-for-docs/business-reports/references/style.md). This file is Mermaid-only.

---

## Mandatory in every block

```
accTitle: Short 3-8 word title
accDescr: One or two sentences explaining what this diagram shows.
```

- **`accTitle` and `accDescr`** whenever the diagram type supports them. For Mermaid types outside the catalog that do not support them, place an italic paragraph just above the block: *"Diagram comparing X, Y, Z."*
- **No `%%{init}` directives** — breaks dark-mode rendering on GitHub and forks. For color customization use `classDef` (below).
- **No inline `style` on nodes** (`style nodeA fill:#abc`). Use `classDef` and apply with `class`. Exception: subgraphs cannot use `classDef`; style them with `style SubgraphName` instead (see below).
- **No emojis in node labels.** Labels are plain text — no icons, no pictograms.
- **Node IDs in `snake_case`**, semantically matching the label. `apply_tariff["💰 Apply tariff"]`, not `n1["💰 Apply tariff"]`.
- **Zero variable, function, or class names in labels.** Labels are domain. *"Compute pickup factor"*, not *"`calc_pickup_factor()`"*.

---

## Subgraph styling

`classDef` does not apply to subgraphs in Mermaid. Use `style SubgraphName` instead. Always **white background and black text** — guarantees readability on any theme. Vary the `stroke` colour to distinguish areas.

```
style Pricing     fill:#ffffff,stroke:#2563eb,stroke-width:2px,color:#000000
style Inventory   fill:#ffffff,stroke:#16a34a,stroke-width:2px,color:#000000
style Overbooking fill:#ffffff,stroke:#ca8a04,stroke-width:2px,color:#000000
```

---

## `classDef` — standard palette

Three to five `classDef` per diagram is enough; more starts to look like a coloured spreadsheet. Standard palette for flowcharts — works on light and dark GitHub themes:

```
classDef start_end   fill:#1e293b,stroke:#1e293b,stroke-width:2px,color:#f1f5f9
classDef action      fill:#f8fafc,stroke:#94a3b8,stroke-width:1px,color:#0f172a
classDef decision    fill:#f1f5f9,stroke:#475569,stroke-width:1.5px,color:#1e293b
classDef ok          fill:#f0fdf4,stroke:#16a34a,stroke-width:1.5px,color:#15803d
classDef ko          fill:#fef2f2,stroke:#dc2626,stroke-width:1.5px,color:#991b1b
classDef external    fill:#f8fafc,stroke:#94a3b8,stroke-width:1px,color:#64748b,stroke-dasharray:5
```

Apply with `class node_id class_name` at the end of the block. Keep `classDef` declarations at the bottom of the diagram.

Minimal flowchart example:

```mermaid
flowchart LR
    accTitle: Booking Acceptance
    accDescr: Decision flow for accepting or rejecting a booking request.

    start_node(["Booking request"])
    decision{"Room available?"}
    end_ok(["Confirmed"])
    end_ko(["Rejected"])

    start_node --> decision
    decision -->|yes| end_ok
    decision -->|no|  end_ko

    classDef start_end fill:#1e293b,stroke:#1e293b,stroke-width:2px,color:#f1f5f9
    classDef decision  fill:#f1f5f9,stroke:#475569,stroke-width:1.5px,color:#1e293b
    classDef ok        fill:#f0fdf4,stroke:#16a34a,stroke-width:1.5px,color:#15803d
    classDef ko        fill:#fef2f2,stroke:#dc2626,stroke-width:1.5px,color:#991b1b

    class start_node start_end
    class decision decision
    class end_ok ok
    class end_ko ko
```

---

## Edge labels and thresholds

- **Every decision `{}` has labeled branches** (`|yes|`, `|no|`, `|> 80%|`). An unlabeled branch is disguised ambiguity.
- **Every threshold with its unit**: *"90 days"*, *"> 80%"*, *"€4.5"*. Values without units are rejected.
- **Linear flows without decisions**: label an edge only if it adds information (a triggering event, a state transition). Otherwise leave it bare.

---

## When NOT to add a diagram

- Prose says it all and the diagram only adds visual weight.
- A section has no substance to diagram — omit silently, no comment.
- What you want to represent is actually a table. A matrix of business rules reads better as a table than a flowchart.

**Default conservative**: when in doubt, omit. A wrong or redundant diagram is worse than prose alone.
