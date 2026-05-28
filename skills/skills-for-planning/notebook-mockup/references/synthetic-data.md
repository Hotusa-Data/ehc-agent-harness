# Synthetic Data Reference

Guidelines for building synthetic data that is realistic enough to surface real bugs.

---

## The goal

Synthetic data must be:
- **Realistic** — realistic field values, correct data types, plausible distributions.
- **Explicit** — constructed inline at the top of the notebook, never loaded from files.
- **Intentional** — each record exists for a reason (happy path, edge case, boundary).
- **Safe** — no real names, emails, IDs, or credentials, even anonymized.

Trivial data (single rows, single-character strings, `id=1`) hides type errors and edge cases. It will fail review.

---

## Structure a synthetic dataset

### Step 1 — Identify the grain

What does one row represent? Use the domain term from the spec.

```python
# Grain: one row = one raw headline submitted by a source
raw_headlines = pd.DataFrame([...])
```

### Step 2 — List required fields and types

Pull from the spec's input contracts section. Match field names exactly to the domain vocabulary.

| Field | Type | Nullable | Example |
|---|---|---|---|
| `external_id` | str | No | `"H001"` |
| `source` | str | Yes (edge case) | `"reuters"` |
| `published_at` | str (ISO8601) | No | `"2024-01-15T08:30:00Z"` |
| `title` | str | No | `"Central bank raises rates"` |

### Step 3 — Build enough rows

| Scenario | Minimum rows | Why |
|---|---|---|
| Tabular validation logic | 5–10 | Covers happy path + all named edge cases |
| Aggregation / grouping | 10–20 | Needs multiple groups to be meaningful |
| Time-series logic | 1 full sequence | At least one rising trend, one flat, one with gaps |
| ML feature engineering | 20–50 | Needs enough variation to test distributions |

### Step 4 — Comment each row

```python
raw_headlines = pd.DataFrame([
    # Happy path — valid record with all required fields
    {"external_id": "H001", "source": "reuters",  "published_at": "2024-01-15T08:30:00Z", "title": "..."},
    # Happy path — different source to test source_id preservation
    {"external_id": "H002", "source": "ap",       "published_at": "2024-01-15T09:00:00Z", "title": "..."},
    # Edge case: AC1 — record with no source (must be rejected)
    {"external_id": "H003", "source": None,        "published_at": "2024-01-15T09:15:00Z", "title": "..."},
    # Edge case: boundary — published_at is exactly at the cutoff
    {"external_id": "H004", "source": "bloomberg", "published_at": "2024-01-01T00:00:00Z", "title": "..."},
])
```

---

## Realism guidelines

### Strings

Use plausible values, not placeholders.

| Bad | Better |
|---|---|
| `"test"`, `"string"`, `"aaa"` | `"reuters"`, `"ap"`, `"bloomberg"` |
| `"name1"`, `"name2"` | `"Central bank raises rates"`, `"Q4 earnings miss"` |
| `"2020-01-01"` for everything | Varied dates that span the relevant range |

### Numbers

Use values that reflect real magnitudes.

| Bad | Better |
|---|---|
| `1`, `2`, `3` | `14.50`, `14.75`, `9.99` (prices) |
| `100`, `200` | `142_500`, `98_300` (revenue in dollars) |
| `0.1`, `0.9` | `0.823`, `0.671` (model probabilities) |

### Dates and times

- Always use the timezone specified in the spec (usually UTC).
- Cover at least two different dates, not a single date repeated.
- Include a date at or near a boundary if the spec has time-based rules.

```python
import pandas as pd

dates = pd.to_datetime([
    "2024-01-15T08:30:00Z",
    "2024-01-15T14:00:00Z",
    "2024-01-16T09:00:00Z",
])
```

### IDs

Use a consistent prefix that reflects the entity. Avoid pure integers that look like row numbers.

```python
# Good
external_id = "H001"   # H = headline
customer_id = "C4821"  # C = customer
order_id    = "ORD-2024-001"

# Bad
id = 1
id = "id1"
```

---

## Edge case patterns

Cover each of these when the spec mentions them. Add a row comment explaining which edge case it represents.

| Edge case | How to construct it |
|---|---|
| Null required field | Set the field to `None` |
| Empty string | Set the field to `""` (if the spec distinguishes from null) |
| Duplicate record | Add a second row with the same `external_id` |
| Boundary value (lower) | Set a numeric field to exactly the minimum threshold |
| Boundary value (upper) | Set a numeric field to exactly the maximum threshold |
| Future date | Use a `published_at` that is ahead of the current date |
| Very old date | Use a `published_at` far in the past |
| Maximum length string | Construct a string at the field's length limit |
| Mixed types | Include a row where a numeric field contains a string |

---

## What not to do

| Anti-pattern | Problem |
|---|---|
| `pd.read_csv("data/export.csv")` | Real data in a mockup — forbidden |
| Single row datasets | Hides type errors, null handling, distribution issues |
| `{"field": "test"}` for all rows | Not realistic — hides production data shape bugs |
| Identical values across all rows | No variation — edge cases cannot be demonstrated |
| No comments on rows | Reviewer cannot tell which row tests which scenario |
| Synthetic data defined inside a function | Must be at the top of the notebook in Section 1 |
