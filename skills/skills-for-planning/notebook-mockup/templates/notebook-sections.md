# Notebook Sections Template

Five required sections in this exact order. Each section starts with a level-2 markdown cell (`## Section N — Title`). Never merge or reorder sections.

---

## Section 1 — Datos (Synthetic Data)

**Purpose:** Define the inputs explicitly. Anyone who opens this notebook must understand what the data looks like before reading a single function.

**Structure:**

```
[markdown] ## Section 1 — Datos (Synthetic Data)
[markdown] Brief description of what this section establishes and why.
           Reference the spec's input contract (field names, types, grain).

[code]     # Imports
           import pandas as pd
           import numpy as np
           # etc.

[markdown] ### Synthetic data — <entity name>
           Explain the data shape: grain, required fields, field types.
           State which spec requirement or AC this data covers.

[code]     # Build the synthetic dataset explicitly.
           # Use realistic values, correct types, and enough rows to
           # demonstrate variation (minimum 5–10 records for tabular data).
           raw_headlines = pd.DataFrame([
               {"external_id": "H001", "source": "reuters", "published_at": "2024-01-15T08:30:00Z", "title": "..."},
               {"external_id": "H002", "source": "ap",      "published_at": "2024-01-15T09:00:00Z", "title": "..."},
               # At least one record per edge case scenario (null, missing, boundary)
               {"external_id": "H003", "source": None,      "published_at": "2024-01-15T09:15:00Z", "title": "..."},
           ])

[markdown] Preview of the synthetic data and notes on what each row represents.

[code]     raw_headlines.head()
```

**Rules:**
- All synthetic data must be built here, at the top. No loading from files.
- Use the domain terms from the glossary for field names and variable names.
- Include at least one row that will fail validation (for use in Section 4).
- Add a brief comment on each row explaining its role.

---

## Section 2 — Funciones (Core Functions)

**Purpose:** Implement the logic as clean, testable functions. These are the functions that [`build-slice`](../../build-slice/SKILL.md) will productionize. Their names and signatures become the contract.

**Structure:**

```
[markdown] ## Section 2 — Funciones (Core Functions)

[markdown] ### `<function_name>(<args>) → <return type>`
           Describe what this function does in one sentence.
           State the business rule it implements (quote from the spec if short).
           List inputs and outputs with their types and domain meaning.

[code]     def validate_and_filter(records: pd.DataFrame) -> pd.DataFrame:
               """
               Reject records with no source. Return accepted records with
               source_id and published_date preserved.

               Business rule: FR1 — records without source are rejected.
               """
               rejected = records[records["source"].isna()]
               if not rejected.empty:
                   rejected_ids = rejected["external_id"].tolist()
                   print(f"Rejected {len(rejected)} records: {rejected_ids}")
               return records[records["source"].notna()].copy()

[markdown] Notes on design decisions, tradeoffs, or constraints from the spec.
           If you chose one approach over another, say why briefly.
```

**Rules:**
- Functions take explicit inputs and return explicit outputs. No global state.
- Function names must use domain terms from the glossary, not technical names.
- Each function has a docstring with: one-sentence purpose, business rule reference, inputs/outputs.
- Keep functions small — each implements one business rule or transformation step.
- If a function has subtlety (a null-handling edge, a rounding rule), note it in the markdown cell.

---

## Section 3 — Ejemplos (Worked Examples)

**Purpose:** Show the expected behavior end-to-end for the normal case, step by step. The reviewer should be able to follow the logic without reading any function code.

**Structure:**

```
[markdown] ## Section 3 — Ejemplos (Worked Examples)
           State which ACs this section demonstrates. Example:
           "This section demonstrates AC1 and AC2 using the valid records
           from the synthetic dataset."

[markdown] ### Example 1 — <short name describing the scenario>
           Explain what this example tests and what the expected outcome is.
           Reference the AC by ID: "AC1: when source is present, the record is accepted."

[code]     # Call the functions defined in Section 2 on the happy-path records.
           # Use only the valid rows from Section 1.
           valid_records = raw_headlines[raw_headlines["source"].notna()]
           result = validate_and_filter(valid_records)
           result

[markdown] Interpret the output: what does it prove? Which part of the spec does it satisfy?
           If the output is a DataFrame, explain the expected row count and key column values.

[code]     # Assertions that make the expectation explicit.
           assert len(result) == 2, "Expected 2 valid records"
           assert result["source_id"].notna().all(), "All accepted records must have source_id"
           print("AC1 ✓ — valid records accepted")
           print("AC2 ✓ — source_id preserved")
```

**Rules:**
- Work through one example at a time. Each example is one scenario.
- End each example with explicit assertions and a print statement that names the AC.
- The reviewer must be able to read only the markdown cells and understand the flow.
- Functions from Section 2 are already defined and available for use.

---

## Section 4 — Edge Cases and Failures

**Purpose:** Prove the behavior for every edge case listed in the spec. This is as important as Section 3 — most bugs live here.

**Structure:**

```
[markdown] ## Section 4 — Edge Cases and Failures

[markdown] ### Edge case: <name from spec>
           Quote or paraphrase the spec: "When <condition>, the system shall <response>."
           Reference the AC or requirement ID.
           State what we expect to see in the output.

[code]     # Use the rows from Section 1 that were designed for this edge case.
           missing_source_record = raw_headlines[raw_headlines["external_id"] == "H003"]
           result_edge = validate_and_filter(missing_source_record)
           result_edge

[markdown] Interpret the output. Confirm it matches the spec.

[code]     assert len(result_edge) == 0, "Record with no source must be rejected"
           print("Edge case ✓ — missing source is rejected")

[markdown] ### Edge case: empty input
           What should happen when the input DataFrame has zero rows?

[code]     empty_input = pd.DataFrame(columns=raw_headlines.columns)
           result_empty = validate_and_filter(empty_input)
           assert len(result_empty) == 0
           print("Edge case ✓ — empty input returns empty output")
```

**Required edge cases to cover (at minimum):**
- Empty input (zero rows)
- Missing / null required fields
- Duplicate records (if the spec mentions deduplication)
- Boundary values (if the spec mentions thresholds or limits)
- Invalid types (if the spec mentions type validation)
- Any edge case explicitly listed in the spec

**Rules:**
- Every edge case in the spec must appear here. If you cannot demonstrate one (e.g., requires a database), flag it explicitly with a note explaining why and which test will cover it.
- Use the same assertion pattern as Section 3: assert + print with AC/edge-case reference.
- Do not invent edge cases that are not in the spec. If you think one is missing, flag it for the reviewer.

---

## Section 5 — Resumen (Summary)

**Purpose:** Give the reviewer a single place to confirm what was proved, what is still open, and what the production implementation must match.

**Structure:**

```
[markdown] ## Section 5 — Resumen (Summary)

[markdown] ### What this notebook proves

           | AC / Requirement | Section | Result |
           |---|---|---|
           | AC1 — records without source are rejected | Section 3 + Section 4 | ✓ Proved |
           | AC2 — accepted records preserve source_id | Section 3 | ✓ Proved |
           | AC3 — empty input returns empty output | Section 4 | ✓ Proved |

[markdown] ### Open questions for reviewer

           List anything that could not be demonstrated or is ambiguous.
           Number each item. If nothing is open, write "None."

           1. AC4 (database write behavior) is not demonstrated here — covered by integration test in [`build-slice`](../../build-slice/SKILL.md).

[markdown] ### Contract for build-slice

           Functions defined in this notebook:

           | Function | Signature | Business rule |
           |---|---|---|
           | `validate_and_filter` | `(records: DataFrame) → DataFrame` | FR1 — reject records without source |

           Production code in [`build-slice`](../../build-slice/SKILL.md) must preserve these function names and signatures.
           Behavioral changes require updating this notebook and re-requesting reviewer approval.
```

**Rules:**
- The AC table must be complete — every AC from the spec appears with a status.
- Open questions must be numbered and explicit. An empty open questions section is valid.
- The contract table becomes the interface contract for TDD in [`build-slice`](../../build-slice/SKILL.md).
