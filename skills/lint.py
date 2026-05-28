#!/usr/bin/env python3
"""
Lint the skill catalog.

Checks per SKILL.md:
  - Frontmatter exists and parses (top-level keys + 1-level metadata nesting).
  - Required fields are present: name, phase, description, allowed-tools,
    metadata.owner, metadata.last_reviewed, metadata.skill-version.
  - `name:` matches the parent directory name.
  - `phase:` is exactly one of {context, spec, plan, build, document, cross-cutting}.
  - Recommended sections present (warnings, not errors): When to use,
    When NOT to use, Related skills.
  - Internal links to other SKILL.md files resolve to existing files.

Run from the repo root:
    python skills/lint.py

Exit 0 if no errors, 1 otherwise. Warnings never fail the run.

No third-party dependencies — stdlib only.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

VALID_PHASES = {"context", "spec", "plan", "build", "document", "cross-cutting"}
REQUIRED_FIELDS = ("name", "phase", "description", "allowed-tools")
REQUIRED_METADATA = ("owner", "last_reviewed", "skill-version")
RECOMMENDED_SECTIONS = ("## When to use", "## When NOT to use", "## Related skills")

SKILLS_ROOT = Path(__file__).resolve().parent


def parse_frontmatter(text: str) -> dict | None:
    """Extract YAML frontmatter as a flat dict. Supports 1-level nesting under `metadata`."""
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        return None
    body = match.group(1)
    result: dict = {}
    current_parent: str | None = None
    for raw_line in body.splitlines():
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue
        indent = len(raw_line) - len(raw_line.lstrip())
        line = raw_line.strip()
        if indent == 0:
            if line.endswith(":"):
                # Section header (e.g. "metadata:" or "allowed-tools:")
                current_parent = line[:-1]
                result[current_parent] = {} if current_parent == "metadata" else []
            elif ":" in line:
                key, _, value = line.partition(":")
                value = value.strip().strip('"').strip("'")
                if value == "|" or value == ">":
                    result[key.strip()] = "<block>"
                else:
                    result[key.strip()] = value
                current_parent = None
            else:
                current_parent = None
        else:
            # Indented under current_parent
            if current_parent == "metadata" and ":" in line:
                key, _, value = line.partition(":")
                result["metadata"][key.strip()] = value.strip().strip('"').strip("'")
            elif current_parent == "allowed-tools" and line.startswith("- "):
                result["allowed-tools"].append(line[2:].strip())
    return result


def lint_skill(skill_md: Path) -> tuple[list[str], list[str]]:
    """Return (errors, warnings) for one SKILL.md file."""
    errors: list[str] = []
    warnings: list[str] = []

    text = skill_md.read_text(encoding="utf-8")
    fm = parse_frontmatter(text)
    if fm is None:
        errors.append("frontmatter missing or unparseable")
        return errors, warnings

    # Required fields
    for field in REQUIRED_FIELDS:
        if field not in fm or fm[field] in (None, "", []):
            errors.append(f"frontmatter missing required field: {field}")

    # name matches folder
    folder = skill_md.parent.name
    if fm.get("name") and fm["name"] != folder:
        errors.append(f"`name: {fm['name']}` does not match folder `{folder}`")

    # phase value
    phase = fm.get("phase")
    if phase and phase not in VALID_PHASES:
        errors.append(f"`phase: {phase}` is not in {sorted(VALID_PHASES)}")

    # metadata
    metadata = fm.get("metadata", {}) if isinstance(fm.get("metadata"), dict) else {}
    for key in REQUIRED_METADATA:
        if key not in metadata or not metadata[key]:
            errors.append(f"frontmatter.metadata missing required field: {key}")

    # Recommended sections (warnings only)
    for section in RECOMMENDED_SECTIONS:
        if section not in text:
            warnings.append(f"recommended section missing: {section!r}")

    # Internal SKILL.md links resolve
    for link in re.findall(r"\]\(([^)]*SKILL\.md)\)", text):
        target = (skill_md.parent / link).resolve()
        if not target.is_file():
            errors.append(f"broken link to {link} (resolved: {target})")

    return errors, warnings


def main() -> int:
    skill_files = sorted(SKILLS_ROOT.glob("**/SKILL.md"))
    if not skill_files:
        print("No SKILL.md files found under", SKILLS_ROOT)
        return 1

    total_errors = 0
    total_warnings = 0
    for skill_md in skill_files:
        rel = skill_md.relative_to(SKILLS_ROOT)
        errors, warnings = lint_skill(skill_md)
        if not errors and not warnings:
            print(f"  OK    {rel}")
            continue
        for err in errors:
            print(f"  ERROR {rel}: {err}")
            total_errors += 1
        for warn in warnings:
            print(f"  WARN  {rel}: {warn}")
            total_warnings += 1

    print()
    print(f"Checked {len(skill_files)} skill(s). "
          f"{total_errors} error(s), {total_warnings} warning(s).")
    return 0 if total_errors == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
