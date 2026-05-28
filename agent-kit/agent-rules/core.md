---
triggers: [always]
requires: []
see-also: [architecture, testing]
severity-default: MUST
---

# Core Engineering Principles

Universal rules for any non-trivial task.

Load when: always.

Severity convention follows RFC 2119:
- `[MUST]` required; violation is a bug.
- `[SHOULD]` strongly preferred; deviation requires justification.

`[MAY]` is reserved for optional guidance and used only when a rule truly is take-it-or-leave-it; if no current rule needs it, do not introduce it.

## Rules

### CORE-1 Prefer correctness over cleverness [MUST]

Choose clear, explainable behavior over compact or surprising implementations. Do not trade maintainability for optimization unless the need is proven.

```python
# good
def normalize_score(raw: float, lo: float, hi: float) -> float:
    if hi == lo:
        raise ValueError("range is zero")
    return (raw - lo) / (hi - lo)

# bad
normalize = lambda r, lo, hi: (r - lo) / (hi - lo)
```

### CORE-2 Make boundary contracts explicit [MUST]

Input/output schemas and data assumptions must be explicit at every system boundary. Validate where data enters or leaves the system, not deep inside business logic. See [validation](validation.md).

### CORE-3 Keep changes small and reviewable [MUST]

Prefer small vertical slices that deliver one cohesive behavior across the relevant layers. Do not mix behavior changes, refactors, and unrelated docs in the same change.

### CORE-4 Specify before building non-trivial behavior [MUST]

For new or non-trivial behavior, define what changes, why, and what acceptance looks like before writing code.

### CORE-5 Back claims with evidence [MUST]

Every non-trivial acceptance criterion must map to evidence such as a passing test, a reproducible example, a committed notebook re-run, or a before/after behavior note.

### CORE-6 Name lightweight shortcuts explicitly [SHOULD]

A low-risk change may skip a safeguard only if the skip is named, justified, and backed by at least one verification signal. Silent skipping is not lightweight.

## Collaboration Rules

### COOP-1 Stop when ambiguity can change the outcome [MUST]

Stop and clarify when ambiguity affects scope, expected inputs/outputs, business rules, acceptance criteria, data contracts, or privacy/security constraints. Do not invent missing rules, thresholds, or schemas.

### COOP-2 Surface assumptions when proceeding [MUST]

If you proceed with an assumption rather than asking, state it explicitly in the plan, spec, PR, or progress notes.

```text
Assumption: "recent" means last 30 days. Reject this if the product rule uses a different window.
```

### COOP-3 Distinguish ran from written [MUST]

Always separate:
- what you ran and what happened
- what you wrote but did not run
- what you tried to run but could not

Do not flatten these into "done".

## Anti-patterns

- Inventing business rules or thresholds not present in the spec or glossary.
- Adding "for now" workarounds without naming them as deferred decisions.
- Treating absence of failure as evidence of correctness.
- Reporting completion before verification exists.
- Mixing scope because several changes feel loosely related.

## Project Overrides

Use this section to record project-specific constraints such as naming language, approved storage backends, compliance rules, required quality gates, or required commands (lint, test, build, license checks). A task is not complete until every applicable check passes; do not bypass hooks.

## See also

- [architecture](architecture.md)
- [testing](testing.md)
