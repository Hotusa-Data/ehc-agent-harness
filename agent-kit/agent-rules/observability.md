---
triggers: [log, logger, metric, trace, monitor, alert, observability, instrumentation]
requires: [core]
see-also: [security, architecture]
severity-default: MUST
---

# Observability

Rules for logs, failure visibility, and safe operational signals.

Load when: adding instrumentation, defining failure surfaces, or reviewing runtime visibility.

## Rules

### OBS-1 Prefer structured logging [MUST]

Use structured fields instead of string-built log messages whenever possible.

### OBS-2 Keep one logger per module [SHOULD]

Use the shared **Loguru** logger from `<pkg>.core` instead of ad hoc loggers or `print()`:

```python
from <pkg>.core import logger

logger.info("Scraping started")
```

### OBS-3 Choose log levels deliberately [MUST]

Routine events should not be errors, and real failures should not be hidden at debug level.

### OBS-4 Log enough safe context to debug later [MUST]

Include safe identifiers, counts, timings, run IDs, and operation names where they help explain what happened.

### OBS-5 Never log secrets or PII [MUST]

Use safe identifiers, hashing, redaction, or omission when data is sensitive.

### OBS-6 Log workflow or pipeline boundaries [SHOULD]

For staged work, log start/end or in/out counts at stage boundaries so failures are localizable.

### OBS-7 Surface validation failures in aggregate [MUST]

When many records fail, log counts and safe identifiers rather than dumping raw payloads.

### OBS-8 Preserve exception context [MUST]

Log exceptions with stack traces and avoid replacing the original failure with a less informative generic one. When swallowing is intentional, log the exception before continuing:

```python
try:
    do_thing(x)
except SomeError as e:
    logger.error(e)
```

### OBS-9 Use metrics when logs are the wrong tool [SHOULD]

High-volume repetitive signals should often become counters, histograms, or traces rather than noisy logs. Record the chosen library under Project Overrides.

### OBS-10 Attach context with Loguru bind/contextualize [SHOULD]

Use `logger.bind(...)` for per-call enrichment and `logger.contextualize(...)` for a scope (request, task, batch) instead of string-building:

```python
with logger.contextualize(run_id=run_id, stage="scrape"):
    logger.info("Starting", count=len(items))
```

Avoid threading the same identifiers into every message manually.

### OBS-11 Use rich for human-facing CLI output [SHOULD]

When a Typer command's output is for human eyes (tables, progress, status), use **`rich`** (Console, Table, Progress). Logs still go through **Loguru**; do not mix the two as a substitute for logging. Server/library code logs only — no `rich` prints.

## Anti-patterns

- `print()` instead of structured logging.
- String-built logs that lose queryable fields.
- Logging full request bodies or raw records that may contain sensitive data.
- INFO logs inside hot loops.
- Logging an exception and then masking the original failure.

## Project Overrides

Use this section for project-specific logging stacks, required fields, metric libraries, alerting expectations, or metric naming conventions.

## See also

- [security](security.md)
- [architecture](architecture.md)
