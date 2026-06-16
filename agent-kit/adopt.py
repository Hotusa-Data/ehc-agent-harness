#!/usr/bin/env python3
"""
Bootstrap a consumer repo after agent-kit/ is copied in.

Creates base docs from skeletons, optional feature folder, root AGENTS.md
from the kit template, and ensures .gitignore excludes .local-context/.

Run from the consumer repo root (where agent-kit/ lives):

    python agent-kit/adopt.py
    python agent-kit/adopt.py --feature my-feature
    python agent-kit/adopt.py --dry-run

Existing target files are skipped unless --force is passed.
No third-party dependencies — stdlib only.
"""
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

KIT_DIR = Path(__file__).resolve().parent
SKELETONS = KIT_DIR / "skeletons"
AGENTS_TEMPLATE = KIT_DIR / "AGENTS.md"

BASE_DOC_MAP: dict[str, str] = {
    "_database.md": "docs/database.md",
    "_glossary.md": "docs/glossary.md",
    "_docs-guide.md": "docs/docs-guide.md",
}

ADR_DOC_MAP: dict[str, str] = {
    "_adr-index.md": "docs/adr/README.md",
    "_adr-0001-record-decisions.md": "docs/adr/0001-record-architecture-decisions.md",
    "_adr-0002-system-context.md": "docs/adr/0002-system-context.md",
}

FEATURE_DOC_MAP: dict[str, str] = {
    "_specs.md": "specs.md",
    "_plan.md": "plan.md",
    "_CHANGELOG.md": "CHANGELOG.md",
}

GITIGNORE_MARKER = ".local-context/"
GITIGNORE_BLOCK = """\
# Session scratchpad — local to the workspace, never committed
.local-context/
"""


def repo_root() -> Path:
    return KIT_DIR.parent


def copy_skeleton(
    skeleton_name: str,
    target: Path,
    *,
    force: bool,
    dry_run: bool,
) -> str:
    source = SKELETONS / skeleton_name
    if not source.is_file():
        return f"SKIP  {target} (skeleton missing: {skeleton_name})"

    if target.is_file() and not force:
        return f"KEEP  {target} (already exists)"

    if dry_run:
        action = "OVERWRITE" if target.is_file() else "CREATE"
        return f"{action} {target} <- {source.relative_to(KIT_DIR)}"

    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)
    return f"WRITE {target}"


def ensure_gitignore(*, force: bool, dry_run: bool) -> str:
    gitignore = repo_root() / ".gitignore"
    if gitignore.is_file():
        text = gitignore.read_text(encoding="utf-8")
        if GITIGNORE_MARKER in text:
            return f"KEEP  {gitignore} (already excludes {GITIGNORE_MARKER})"
        if dry_run:
            return f"APPEND {gitignore} (+ {GITIGNORE_MARKER} block)"
        with gitignore.open("a", encoding="utf-8", newline="\n") as handle:
            if not text.endswith("\n"):
                handle.write("\n")
            handle.write("\n")
            handle.write(GITIGNORE_BLOCK)
        return f"APPEND {gitignore} (+ {GITIGNORE_MARKER} block)"

    if dry_run:
        return f"CREATE {gitignore}"

    gitignore.write_text(GITIGNORE_BLOCK, encoding="utf-8", newline="\n")
    return f"WRITE {gitignore}"


def ensure_agents_md(*, force: bool, dry_run: bool) -> str:
    target = repo_root() / "AGENTS.md"
    if target.is_file() and not force:
        return f"KEEP  {target} (already exists; adapt manually or pass --force)"

    if not AGENTS_TEMPLATE.is_file():
        return f"SKIP  {target} (template missing at {AGENTS_TEMPLATE})"

    if dry_run:
        action = "OVERWRITE" if target.is_file() else "CREATE"
        return f"{action} {target} <- {AGENTS_TEMPLATE.relative_to(KIT_DIR)}"

    shutil.copyfile(AGENTS_TEMPLATE, target)
    return f"WRITE {target} (review and adapt to the project)"


def run(args: argparse.Namespace) -> int:
    root = repo_root()
    if not (root / "agent-kit").is_dir():
        print("ERROR: run from the consumer repo root (expected ./agent-kit/)", file=sys.stderr)
        return 1

    actions: list[str] = []

    actions.append(ensure_gitignore(force=args.force, dry_run=args.dry_run))

    if args.agents:
        actions.append(ensure_agents_md(force=args.force, dry_run=args.dry_run))

    for skeleton, rel_target in BASE_DOC_MAP.items():
        target = root / rel_target
        actions.append(
            copy_skeleton(skeleton, target, force=args.force, dry_run=args.dry_run),
        )

    for skeleton, rel_target in ADR_DOC_MAP.items():
        target = root / rel_target
        actions.append(
            copy_skeleton(skeleton, target, force=args.force, dry_run=args.dry_run),
        )

    if args.feature:
        feature_dir = root / "docs" / "features" / args.feature
        for skeleton, filename in FEATURE_DOC_MAP.items():
            target = feature_dir / filename
            actions.append(
                copy_skeleton(skeleton, target, force=args.force, dry_run=args.dry_run),
            )

    prefix = "DRY-RUN" if args.dry_run else "adopt"
    print(f"{prefix}: consumer repo at {root}")
    for line in actions:
        print(f"  {line}")

    print()
    print("Next steps:")
    if not args.agents:
        print("  - Create or adapt root AGENTS.md from agent-kit/AGENTS.md")
    else:
        print("  - Fill in AGENTS.md §Commands and §Pull requests; confirm §Boundaries; set overrides in docs/docs-guide.md §3")
    if not args.feature:
        print("  - Run again with --feature <name> to scaffold docs/features/<name>/")
    print("  - Edit docs/adr/0002-system-context.md for this project; add ADRs for layout or integration deltas")
    print("  - See README Track 1 and guides/onboarding/managing-context.md")

    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Bootstrap docs/ and .gitignore after copying agent-kit/ into a project repo.",
    )
    parser.add_argument(
        "--feature",
        metavar="NAME",
        help="Also scaffold docs/features/NAME/ with specs.md, plan.md, CHANGELOG.md",
    )
    parser.add_argument(
        "--agents",
        action="store_true",
        help="Copy agent-kit/AGENTS.md to repo root AGENTS.md when missing (or with --force)",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing target files",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print planned actions without writing files",
    )
    return run(parser.parse_args())


if __name__ == "__main__":
    sys.exit(main())
