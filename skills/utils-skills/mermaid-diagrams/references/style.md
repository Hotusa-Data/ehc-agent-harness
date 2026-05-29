# Mermaid Style — single source of truth

Canonical rules for Mermaid syntax and styling across the entire skill catalog. Other skills (e.g. `business-reports`) point here instead of restating these rules. The diagram type catalog with full exemplars lives in [`diagrams.md`](./diagrams.md); the rules below apply to all eight covered types.

> **Markdown formatting rules** (heading hierarchy, lists, tables, `<details>`, separators, citations) live in [`skills-for-docs/business-reports/references/style.md`](../../../skills-for-docs/business-reports/references/style.md). This file is Mermaid-only.

---

## Mandatory frontmatter

Every diagram opens with a YAML config block that sets the visual theme. This is the only sanctioned way to control appearance globally; `%%{init}` is forbidden (see below).

```
---
config:
  theme: neutral
---
flowchart LR
    accTitle: ...
    accDescr: ...
```

- **`theme: neutral`** — Mermaid's official built-in monochrome theme. Black, white, grays. No blue, no decorative colour. Suitable for technical docs, business reports, and print.
- **Never `%%{init}`** — legacy directive, pre-dates the frontmatter API. The frontmatter `config:` block is the supported path.

`classDef` is reserved for **terminal outcome semantics** (success / failure). The neutral theme already handles every other node. Keep `classDef` to the two-class catalog below.

---

## Mandatory in every block

```
accTitle: Short 3-8 word title
accDescr: One or two sentences explaining what this diagram shows.
```

- **`accTitle` and `accDescr`** whenever the diagram type supports them. For Mermaid types outside the catalog that do not support them, place an italic paragraph just above the block: *"Diagram comparing X, Y, Z."*
- **No inline `style` on nodes** (`style nodeA fill:#abc`). Use `classDef` and apply with `class`. Exception: subgraphs cannot use `classDef`; style them with `style SubgraphName` instead (see below).
- **No emojis in node labels.** Labels are plain text — no icons, no pictograms.
- **Node IDs in `snake_case`**, semantically matching the label. `apply_tariff["Apply tariff"]`, not `n1["Apply tariff"]`.
- **Zero variable, function, or class names in labels.** Labels are domain. *"Compute pickup factor"*, not *"`calc_pickup_factor()`"*.

---

## Subgraph styling

`classDef` does not apply to subgraphs in Mermaid. Prefer leaving subgraphs unstyled — `theme: neutral` already renders them with a subtle border. Only `style SubgraphName` when you need a distinct stroke to separate areas. White fill, black text. Vary only the `stroke` colour — and **never use blue** (it reads as "link" in many viewers).

```
style Pricing     fill:#ffffff,stroke:#f97316,stroke-width:2px,color:#000000
style Inventory   fill:#ffffff,stroke:#16a34a,stroke-width:2px,color:#000000
style Overbooking fill:#ffffff,stroke:#ca8a04,stroke-width:2px,color:#000000
```

---

## `classDef` — two semantic classes, that's it

The whole catalog is two classes. Anything beyond `ok` and `ko` is noise — let `theme: neutral` render the rest. No `action`, no `start_end`, no `decision`, no `external`: those distinctions are already conveyed by node shape (`[]` vs `{}` vs `()`) and edge labels.

```
classDef ok fill:#f0fdf4,stroke:#16a34a,stroke-width:1.5px,color:#14532d
classDef ko fill:#fef2f2,stroke:#dc2626,stroke-width:1.5px,color:#7f1d1d
```

When to apply each:
- **`ok`** — terminal success outcomes (a confirmed booking, an accepted request, a passing gate).
- **`ko`** — terminal failure outcomes (a rejection, a hard failure, an expired state).
- **Everything else** — no class. The neutral theme renders it as plain monochrome.

Apply with `class node_id class_name` at the end of the block. Keep `classDef` declarations at the bottom of the diagram.

Minimal flowchart example:

```mermaid
---
config:
  theme: neutral
---
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

    classDef ok fill:#f0fdf4,stroke:#16a34a,stroke-width:1.5px,color:#14532d
    classDef ko fill:#fef2f2,stroke:#dc2626,stroke-width:1.5px,color:#7f1d1d

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
