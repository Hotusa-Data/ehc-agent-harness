#!/usr/bin/env python3
"""
Bootstrap a consumer repo after agent-kit/ is copied in.

Creates base docs from skeletons, optional feature folder, root AGENTS.md
from the kit template, and ensures .gitignore excludes .local-context/.

Run from the consumer repo root (where agent-kit/ lives):

    python agent-kit/adopt.py --agents
    python agent-kit/adopt.py --agents --feature my-feature
    python agent-kit/adopt.py --dry-run

`--agents` copies this kit's AGENTS.md to the repo root (recommended on first bootstrap).
`--feature` scaffolds specs.md, plan.md, and changelog.md only — not report.md
(report is created at cycle close from agent-kit/skeletons/_report.md).

Existing target files are skipped unless --force is passed.
No third-party dependencies — stdlib only.
"""
from __future__ import annotations

import argparse
import re
import shutil
import sys
from pathlib import Path

KIT_DIR = Path(__file__).resolve().parent
SKELETONS = KIT_DIR / "skeletons"
AGENTS_TEMPLATE = KIT_DIR / "AGENTS.md"
ADR_SKELETON = "_adr.md"
ADR_SECTIONS = ("index", "entry", "bootstrap")

BASE_DOC_MAP: dict[str, str] = {
    "_database.md": "docs/database.md",
    "_glossary.md": "docs/glossary.md",
    "_docs-guide.md": "docs/docs-guide.md",
}

FEATURE_DOC_MAP: dict[str, str] = {
    "_specs.md": "specs.md",
    "_plan.md": "plan.md",
    "_changelog.md": "changelog.md",
}

GITIGNORE_MARKER = ".local-context/"
GITIGNORE_BLOCK = """\
# Session scratchpad — local to the workspace, never committed
.local-context/
"""

FEATURE_SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def repo_root() -> Path:
    return KIT_DIR.parent


def validate_feature_slug(name: str) -> str | None:
    """Return an error message when NAME is not a safe single path segment."""
    if name in (".", ".."):
        return "feature name must not be . or .."
    if "/" in name or "\\" in name or ".." in name:
        return "feature name must be a single slug (no path separators)"
    if not FEATURE_SLUG_RE.fullmatch(name):
        return "feature name must match [a-z0-9]+(-[a-z0-9]+)* (lowercase slug)"
    return None


def summarize_actions(actions: list[str]) -> tuple[int, int, int]:
    """Count CREATE/WRITE/APPEND vs KEEP vs SKIP lines."""
    created = kept = skipped = 0
    for line in actions:
        head = line.split(maxsplit=1)[0] if line else ""
        if head in {"CREATE", "WRITE", "APPEND", "OVERWRITE"}:
            created += 1
        elif head == "KEEP":
            kept += 1
        elif head == "SKIP":
            skipped += 1
    return created, kept, skipped


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


def write_text_target(
    target: Path,
    content: str,
    *,
    label: str,
    force: bool,
    dry_run: bool,
) -> str:
    if target.is_file() and not force:
        return f"KEEP  {target} (already exists)"

    if dry_run:
        action = "OVERWRITE" if target.is_file() else "CREATE"
        return f"{action} {target} ({label})"

    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8", newline="\n")
    return f"WRITE {target}"


def parse_adr_skeleton(path: Path) -> dict[str, str]:
    """Split _adr.md into §Index, §Entry, and §Bootstrap sections."""
    text = path.read_text(encoding="utf-8-sig").replace("\r\n", "\n")
    sections: dict[str, list[str]] = {}
    current: str | None = None
    for line in text.splitlines():
        if line.startswith("## §"):
            current = line.removeprefix("## §").strip().lower()
            sections[current] = []
            continue
        if current is not None:
            sections[current].append(line)
    return {key: "\n".join(lines).strip() for key, lines in sections.items()}


def bootstrap_adr_folder(*, force: bool, dry_run: bool) -> list[str]:
    """Materialize docs/adr/ from §Index -> changelog.md and §Bootstrap in _adr.md."""
    adr_dir = repo_root() / "docs" / "adr"
    actions: list[str] = []
    skeleton_path = SKELETONS / ADR_SKELETON

    if not skeleton_path.is_file():
        actions.append(f"SKIP  {adr_dir}/ (skeleton missing: {ADR_SKELETON})")
        return actions

    parts = parse_adr_skeleton(skeleton_path)
    missing = [name for name in ADR_SECTIONS if not parts.get(name)]
    if missing:
        actions.append(
            f"SKIP  {adr_dir}/ ({ADR_SKELETON} missing sections: {', '.join(missing)})",
        )
        return actions

    actions.append(
        write_text_target(
            adr_dir / "changelog.md",
            parts["index"],
            label=f"{ADR_SKELETON} §Index -> changelog.md",
            force=force,
            dry_run=dry_run,
        ),
    )
    actions.append(
        write_text_target(
            adr_dir / "0001-system-context.md",
            parts["bootstrap"],
            label=f"{ADR_SKELETON} §Bootstrap",
            force=force,
            dry_run=dry_run,
        ),
    )
    return actions


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

    if args.feature:
        slug_error = validate_feature_slug(args.feature)
        if slug_error:
            print(f"ERROR: invalid --feature {args.feature!r}: {slug_error}", file=sys.stderr)
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

    actions.extend(bootstrap_adr_folder(force=args.force, dry_run=args.dry_run))

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

    created, kept, skipped = summarize_actions(actions)
    print()
    print(f"Summary: {created} to write, {kept} kept, {skipped} skipped")

    print()
    print("Next steps:")
    print("  - Onboarding: agent-kit/README.md")
    if not args.agents:
        print(
            "  - Re-run with --agents to copy agent-kit/AGENTS.md to repo root "
            "(recommended on first bootstrap)",
        )
    else:
        print(
            "  - Fill in AGENTS.md §Commands and §Pull requests; confirm §Boundaries; "
            "set overrides in docs/docs-guide.md §3",
        )
    if not args.feature:
        print(
            "  - Run again with --feature <name> to scaffold "
            "docs/features/<name>/{specs,plan,changelog}.md",
        )
    elif args.feature:
        print(
            "  - report.md is not scaffolded by --feature; create it from "
            "agent-kit/skeletons/_report.md at cycle close",
        )
    print("  - Edit docs/adr/0001-system-context.md for this project")
    print(
        "  - New ADRs: copy §Entry from agent-kit/skeletons/_adr.md; "
        "update docs/adr/changelog.md",
    )
    print("  - Session scratch: .local-context/ at repo root (gitignored, never committed)")
    print("  - Doc conventions: agent-kit/agent-rules/DOCUMENTATION.md §DOC-4")

    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Bootstrap docs/ and .gitignore after copying agent-kit/ into a project repo.",
    )
    parser.add_argument(
        "--feature",
        metavar="NAME",
        help=(
            "Scaffold docs/features/NAME/ with specs.md, plan.md, changelog.md "
            "(not report.md — create that at cycle close from skeletons/_report.md)"
        ),
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
