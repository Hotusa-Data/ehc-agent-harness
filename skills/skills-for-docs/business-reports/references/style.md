# Markdown Style — single source of truth

Canonical rules for markdown formatting across the entire skill catalog. Other skills point here instead of restating these rules.

> **Mermaid syntax and style rules** live in [`utils-skills/mermaid-diagrams/references/style.md`](../../../utils-skills/mermaid-diagrams/references/style.md). This file is markdown-only.

---

## Heading hierarchy

- **One H1 per document** — the title. Never two.
- **H2 for top-level sections.** One emoji at the start, optional.
- **H3 for sub-sections.** No emoji.
- **H4 rarely** — only inside an H3 when it has clearly distinct parts.
- **Never H5 or H6.** Deeper nesting means the section is too dense; split it.

## Emphasis

- **Bold sparingly** — max 2-3 terms per paragraph, never whole sentences. Bolding everything highlights nothing.
- *Italics* for new domain terms on first appearance, or for short literal quotes in prose.
- `Inline code` (backticks) for code identifiers, file paths, commands. **Never for domain words** — domain words in prose are unmarked.

## Lists vs prose vs tables

- **Prose by default.** Documents read better as narrative than bullet-soup.
- **Lists** for N genuinely parallel items without order, or numbered steps.
- **Tables** for comparisons, business rules with multiple conditions, structured configurations.
- **Avoid single-item lists.** A single bullet is a paragraph.

## Collapsible `<details>` blocks

Used in `mixed` register only (this skill) to wrap technical zoom. Outside this skill, follow the same syntax when collapsible content is justified.

```html
<details>
<summary>Technical detail: how the cancellation probability is computed</summary>

Technical content here.
</details>

---
```

- **Descriptive summary** — not generic: `<summary>Technical detail: how X works</summary>`, not `<summary>More info</summary>`.
- **Mandatory `---` after every `</details>`** — without it some renderers merge the next paragraph with the block. This is the single most renderer-fragile pattern; always pair them.
- Blocks **default to collapsed**. Do not open them manually.

## Horizontal separators

- `---` between each H2 section.
- `---` after every `</details>` (mandatory, see above).
- Within an H2, H3 sub-sections flow without `---` between them — **except** in `system-narrative`, where each *"intention"* H3 is a self-contained unit and gets a closing `---` (the template marks it).
- Do not overuse — no `---` between H3s within the same section.

## Emoji in headings

- **One emoji per H2 at the start**, optional. E.g. `## 🎯 Executive summary`.
- **Zero emoji in H3 and H4.**
- Exception: 💡 and ⚠️ markers inside lists or prose are separate and may appear in any section.

## Citations

External claims use footnotes: `[^1]` in text, `[^1]: Full reference and URL` at the end. One footnote per reference, no duplicated URL in prose. No stray "see also" mid-text.

## Identifiers in prose

The `business` register forbids code identifiers in prose entirely. The `mixed` register confines them to `<details>` blocks. See [`registers.md`](./registers.md) for the full self-check.
