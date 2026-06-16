---
name: notebook-mockup
phase: cross-cutting
description: |
  Create a structured, reproducible notebook that validates feature logic with synthetic data before any production code is written. The notebook is planned in the Plan phase and executed/approved during Build (hence cross-cutting). Use when a new feature, business rule, data transformation, or ML/scoring logic needs a proof of concept. Trigger on "notebook mockup", "notebook de validación", "prototipo notebook", "validar lógica antes de codificar", "exploratory notebook", or when the plan's first task is a notebook mockup. Do NOT use for modifications to existing behavior (start from build-slice directly), business-stakeholder reports (use business-reports skill), or final production modules.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
metadata:
  owner: Ignacio Freire
  last_reviewed: "2026-05-27"
  skill-version: "1.0.0"
---

# Notebook Mockup

Produce a structured, reproducible notebook that proves feature logic is correct before production code is written. The notebook is a technical document, not a scratch pad. It must be understandable on its own, run clean from top to bottom, and be approvable by a reviewer who has not seen the conversation.

**Contract with the rest of the lifecycle:**
- Input: approved spec + approved plan.
- Output: notebook committed to `notebooks/`, pending human reviewer approval.
- After approval: `build-slice` implements production code that matches what the notebook proved.

---

## When to use

Use when:
- The plan's first task is a notebook mockup (new feature flag is set).
- The user asks to validate logic or prototype behavior before writing production code.

Do NOT use when:
- The change modifies existing behavior with no new logic (go directly to `build-slice`).
- The output is a business-stakeholder report (use `business-reports` instead).
- The spec or plan have not been approved yet.

---

## Inputs required

Collect all of these before writing a single cell. If any are missing, ask — do not invent.

| Input | Where to find it | Why |
|---|---|---|
| Approved specs | `docs/features/<feature>/specs.md` | Requirements, ACs, business rules, contracts |
| Acceptance criteria | `specs.md` or `plan.md` | Every AC must map to at least one notebook section |
| Input / output contracts | `specs.md` §7 | Defines what synthetic data must look like |
| Edge cases | `specs.md` §9 | Must appear explicitly in Section 4 |
| Domain vocabulary | `docs/glossary.md`, or `specs.md` | Function and variable names must use domain terms |

---

## Workflow

### Phase 0 — Verify inputs

1. Read the approved spec. Extract: requirements, ACs, business rules, input/output data shapes, edge cases.
2. Find domain vocabulary: look for `docs/glossary.md` or `UBIQUITOUS_LANGUAGE.md` in the repo root, `docs/`, or `glossary/`. Note the terms you will use.
3. Confirm output path: `notebooks/<feature-slug>-mockup.ipynb`. Create `notebooks/` if missing.
4. If the spec is not approved or ACs are absent, stop and request them.

### Phase 1 — Plan silently before writing

Map these before producing any cells:

- Which synthetic records will cover the happy path inputs
- Which synthetic records will cover each edge case
- Which function names align with domain terms from the glossary
- Which ACs map to which sections
- What the expected outputs should be for each example

### Phase 2 — Write the notebook

Follow the five-section structure from `templates/notebook-sections.md`.

Write sections in order. Never skip a section. For every code cell, write a markdown cell immediately before it that explains: **what this cell does** and **why it matters for the spec**. See quality rules below.

### Phase 3 — Verify

After writing, confirm:

```text
- Notebook runs clean from top to bottom with no errors.
- Every AC from the spec appears in at least one cell output.
- No real production data is referenced or loaded.
- All function names match the domain vocabulary.
- Edge cases produce the outputs specified in the spec.
```

If `jupyter` is available in the environment, execute:

```bash
jupyter nbconvert --to notebook --execute notebooks/<feature-slug>-mockup.ipynb --output notebooks/<feature-slug>-mockup.ipynb
```

If not available, note it explicitly and ask the user to rerun manually before submitting for review.

---

## Quality rules

These are non-negotiable. A notebook that violates them goes back to draft.

| Rule | What it means |
|---|---|
| Markdown before every code cell | Every code cell has a markdown cell above it explaining what and why. No orphan code. |
| Synthetic data is explicit | All inputs are constructed at the top of the notebook. Never load from files, databases, or APIs. |
| Realistic, not trivial | Synthetic records must be plausible: realistic field values, correct data types, representative distribution. Single-row examples that hide type errors are not enough. |
| Domain names everywhere | Functions, variables, and DataFrame columns use names from the glossary or spec. No `df`, `x`, `result`, `temp`. |
| Functions are self-contained | Core functions take explicit inputs and return explicit outputs. No global state, no side effects. |
| Edge cases are prominent | Missing values, empty inputs, boundary values, invalid types — all appear in Section 4 with the same explanation quality as happy-path examples. |
| ACs are traceable | Each AC from the spec is referenced by ID in the relevant cell's markdown. |
| Clean top-to-bottom run | Restart kernel, run all cells in order, zero errors. Hidden state is a defect. |
| No real data | No paths to production files, no live API calls, no credentials. |

---

## AC traceability

Every AC from the plan must appear somewhere. Use this pattern in markdown cells:

```markdown
### AC2 — Accepted records preserve `source_id` and `published_date`

The function should return a DataFrame where all accepted records have non-null `source_id`
and a valid `published_date`. We verify this by checking both columns on the output.
```

If an AC cannot be demonstrated in the notebook (e.g., it requires persistence or an external service), flag it explicitly:

```markdown
> **AC4 — Not demonstrated here.** This AC depends on database write behavior
> and will be covered by the integration test in `build-slice`.
```

---

## Anti-patterns

| Anti-pattern | Why it fails |
|---|---|
| Code cell with no markdown above it | Reviewer cannot understand intent without reading the code |
| `df = pd.read_csv('data/prod_export.csv')` | Real data in a mockup notebook — forbidden |
| Functions named `process`, `run`, `helper` | No domain meaning — glossary drift starts here |
| One synthetic record for all examples | Hides type errors, null handling, and edge cases |
| Skipping edge cases because "the happy path is obvious" | Most bugs live in edge cases — reviewer will ask |
| Running cells out of order to fix a state problem | Hidden state — restart and rerun |
| "See AC1 in the tests later" without demonstrating it | The notebook must prove the logic, not defer it |

---

## Output

- **File:** `notebooks/<feature-slug>-mockup.ipynb`
- **Committed to repo** as part of the feature branch, linked from the plan.
- **Submitted to reviewer** for approval before `build-slice` starts.

After approval, the notebook becomes the reference document for `build-slice`. Production functions must preserve the names and contracts established in the notebook.

---

## Reference index

| File | What it covers |
|---|---|
| `templates/notebook-sections.md` | Five-section structure — what each section contains, markdown/code cell pattern, examples |
| `references/synthetic-data.md` | How to build good synthetic data: types, realism, edge-case coverage, common patterns |

---

## Related skills

- [`implementation-planning`](../implementation-planning/SKILL.md) — predecessor: the plan declares whether a notebook mockup is needed.
- [`build-slice`](../build-slice/SKILL.md) — direct consumer: the notebook's contracts (Section 5) become the production function signatures.
- [`make-glossary`](../../skills-for-docs/make-glossary/SKILL.md) — domain vocabulary used for function and variable names comes from here.
