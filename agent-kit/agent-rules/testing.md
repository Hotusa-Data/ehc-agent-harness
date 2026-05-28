---
triggers: [test, pytest, fixture, mock, assert, evidence]
requires: [core]
see-also: [validation, persistence]
severity-default: MUST
---

# Testing Strategy

Rules for verification, isolation, and what counts as evidence.

Load when: writing or reviewing tests, or choosing how to verify a change.

## Rules

### TEST-1 Test behavior, not implementation [MUST]

Assert what callers observe, not how the code happens to do it. Do not test framework internals, generated SQL shape, or private helpers callers cannot reach.

### TEST-2 Keep unit tests deterministic and isolated [MUST]

A unit test must not depend on the public internet, a shared database, a real clock, or external mutable state. If it does, it is not a unit test.

### TEST-3 Keep fixtures minimal [SHOULD]

Prefer factory fixtures or small local setup over large pre-populated fixtures when only a few records are needed.

### TEST-4 Use a real persistence boundary for persistence behavior [MUST]

Do not mock SQLAlchemy sessions for persistence behavior. Use a real engine and real sessions. For migrations, constraints, dialect-specific behavior, or production-like incidents, use the same database family as production.

```python
@pytest.fixture
def db_session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    Base.metadata.drop_all(engine)
```

### TEST-5 Mock at the boundary, not in the middle [MUST]

Mock external services such as HTTP, queues, or object storage. Do not mock persistence internals just to make tests easy. Anchor mocks at the seam that owns the IO call:

```python
@patch("<pkg>.data.scraping.fetch_url")
def test_get_headlines(mock_fetch):
    mock_fetch.return_value = b"<h2>Title</h2>"
    ...
```

### TEST-6 Inject time when time matters [MUST]

Time-dependent behavior should receive `now` or a clock dependency instead of reading the system clock internally.

### TEST-7 Cover transformation edge cases [SHOULD]

Common cases include empty input, all-null key columns, single-row input, duplicate data, identical values, and unexpected categories.

### TEST-8 Test pipeline stages independently when useful [SHOULD]

Large transformations are easier to trust when each stage can be verified in isolation as well as in end-to-end flow.

### TEST-9 Check idempotency where writes can repeat [SHOULD]

Upserts, sync jobs, event handlers, and retryable tasks should usually prove that repeated execution does not duplicate state or corrupt outcomes.

### TEST-10 Evidence without a formal test must be explicit [SHOULD]

When a formal automated test is impractical, cite concrete evidence such as a committed notebook re-run, an executable example, or before/after behavior notes with specific inputs and outputs.

### TEST-11 Test FastAPI routes via TestClient [SHOULD]

Use `fastapi.testclient.TestClient` against the app instance. Override DB and settings dependencies via `app.dependency_overrides[...]`; do not monkey-patch internals. Assert status code, response shape, and at least one business-meaningful field.

### TEST-12 Test file naming and layout [MUST]

One test module per source module. Filename pattern: `tests/test_<pkg>_<path>_<module>.py`. Mirrors the package layout so the relationship is mechanical (e.g. `<pkg>/data/scraping.py` → `tests/test_<pkg>_data_scraping.py`). Shared fixtures in `tests/conftest.py`; test-only helpers in `tests/utils.py`.

Test envs load from `.env.ci` via `pytest-dotenv` / `pytest-env` (`env_files` in `pyproject.toml`). No real credentials.

## Anti-patterns

- Tests that assert almost nothing.
- `assert result is not None` as the only signal.
- Mocking SQLAlchemy sessions instead of testing the real boundary.
- Relying on SQLite for behavior tied to a different production dialect.
- Hard-coding time inside logic and then working around it in tests.
- Test names like `test_function_works` instead of behavior-based names.

## Project Overrides

Default commands for this project template (Makefile wraps these):

```text
make test                                # full suite
uv run pytest tests/test_<...>.py        # single file
uv run pytest --cov-report term-missing --cov=<pkg> tests/
```

Use this section for repository-specific test commands, fixture policies, minimum coverage expectations, or required CI gates.

## See also

- [validation](validation.md)
- [persistence](persistence.md)
