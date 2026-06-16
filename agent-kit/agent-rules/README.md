# Agent rules index

Engineering rules for the coding agent. Each file has `Load when:` in front-matter — load just-in-time per [`documentation.md` §DOC-1](documentation.md).

| File | Load when |
|---|---|
| `core.md` | Always (also loaded from `AGENTS.md` bootstrap) |
| `documentation.md` | Reading, writing, or gating on `docs/` artifacts (DOC-1–DOC-9) |
| `architecture.md` | Module, layer, or system-boundary decisions |
| `repo-guide.md` | New files, folders, or placement questions |
| `python.md` | Python code |
| `persistence.md` | ORM, queries, migrations, sessions |
| `testing.md` | Tests and verification strategy |
| `validation.md` | Input checks, contracts, failure handling |
| `security.md` | Auth, secrets, trust boundaries |
| `observability.md` | Logs, metrics, tracing |

Ambiguity and stop-to-clarify: `core.md` §COOP-1 and §COOP-2. Project overrides: `## Project Overrides` in each rule file and `docs/docs-guide.md` §3.
