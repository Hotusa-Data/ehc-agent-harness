# agent-kit

Portable harness for coding agents: rules, doc skeletons, and a bootstrap script. Copy this folder into a **consumer repo root** (alongside your application code).

## Quick start

From the consumer repo root (after copying `agent-kit/`):

```bash
python agent-kit/adopt.py --dry-run --agents
python agent-kit/adopt.py --agents
python agent-kit/adopt.py --agents --feature my-feature
```

- `--agents` — copies `agent-kit/AGENTS.md` to `./AGENTS.md` and scaffolds base `docs/`.
- `--feature <slug>` — adds `docs/features/<slug>/{specs,plan,changelog}.md` (not `report.md`; create that at cycle close).
- Existing files are kept unless you pass `--force`.

## After bootstrap

1. Edit root `AGENTS.md` §Commands and §Pull requests for your toolchain.
2. Fill `docs/docs-guide.md` §1 (required docs) and §3 (overrides).
3. Edit `docs/adr/0001-system-context.md` for this project.
4. Read `agent-kit/agent-rules/DOCUMENTATION.md` §DOC-4 for skeleton mapping.

Session scratch lives in `.local-context/` at repo root (gitignored).

## Kit profile (template default)

This kit assumes a **Python data stack**: `uv`, SQLAlchemy + Alembic, Pydantic + Pandera, FastAPI, Typer, package layout in `REPO_GUIDE.md`, mirrored `tests/`.

Always load `agent-kit/agent-rules/CORE.md`. Load other rule files just-in-time via `agent-kit/agent-rules/RULES.md` — do not load the whole index.

## Non-Python or different layout

Record deviations in `docs/docs-guide.md` §3. Typical overrides:

| Area | Action |
|---|---|
| Stack / commands | Replace `AGENTS.md` §Commands; note toolchain in §3 |
| Layout | ADR under `docs/adr/` + `REPO_GUIDE.md` overrides in §3 |
| ORM / API rules | Skip or demote `PERSISTENCE.md`, `PYTHON.md` PY-13–16 when N/A |
| DataFrame rules | Skip `VALIDATION.md` VAL-2/6/9 when no Pandera |
| Feature docs | Keep `docs/features/` cycle; skeletons are stack-agnostic |

When unsure, treat work as non-trivial and document overrides explicitly (**DOC-6**).

## Layout

```
agent-kit/
├── README.md          ← this file
├── AGENTS.md          ← template for repo root
├── adopt.py           ← bootstrap script
├── agent-rules/       ← engineering rules (SCREAMING_SNAKE.md)
└── skeletons/         ← templates for docs/
```

Canonical rule index: `agent-kit/agent-rules/RULES.md`.
