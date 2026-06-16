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

Plugin skills under plugins/*/skills/ are linted too. Mapped copies must match
their canonical source in skills/utils-skills/ (link paths rewritten). Run
`python skills/lint.py --sync-plugin` after editing a canonical skill that is
shipped in the team plugin.

Run from the repo root:
    python skills/lint.py
    python skills/lint.py --sync-plugin

Also checks `agent-kit/skeletons/` for case-only filename collisions (e.g.
`_changelog.md` vs `_CHANGELOG.md`) that break on Linux CI.

Validates `agent-kit/AGENTS.md` carries the required entrypoint sections
(Commands, Boundaries, Pull requests, etc.), forbids a duplicated rules index,
and enforces a maximum line count. Delegates doc rules to
`agent-kit/agent-rules/DOCUMENTATION.md`. Validates `agent-kit/agent-rules/`
(SCREAMING_SNAKE filenames, frontmatter, unique rule IDs, internal links).

Exit 0 if no errors, 1 otherwise. Warnings never fail the run.

No third-party dependencies — stdlib only.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

VALID_PHASES = {"context", "spec", "plan", "build", "document", "cross-cutting"}
REQUIRED_FIELDS = ("name", "phase", "description", "allowed-tools")
REQUIRED_METADATA = ("owner", "last_reviewed", "skill-version")
RECOMMENDED_SECTIONS = ("## When to use", "## When NOT to use", "## Related skills")

SKILLS_ROOT = Path(__file__).resolve().parent
REPO_ROOT = SKILLS_ROOT.parent

# plugin skill dir (relative to repo root) -> canonical utils-skills dir
PLUGIN_SKILL_SOURCES: dict[str, str] = {
    "plugins/test-plugin/skills/grill-me": "skills/utils-skills/grill-me",
    "plugins/test-plugin/skills/handoff": "skills/utils-skills/handoff",
}


def parse_frontmatter(text: str) -> dict | None:
    """Extract YAML frontmatter as a flat dict. Supports 1-level nesting under `metadata`."""
    text = text.lstrip("\ufeff").replace("\r\n", "\n")
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
            if current_parent == "metadata" and ":" in line:
                key, _, value = line.partition(":")
                result["metadata"][key.strip()] = value.strip().strip('"').strip("'")
            elif current_parent == "allowed-tools" and line.startswith("- "):
                result["allowed-tools"].append(line[2:].strip())
    return result


def canonical_to_plugin_skill(text: str) -> str:
    """Rewrite intra-repo skill links for plugin copy layout."""
    text = text.replace(
        "../../skills-for-planning/",
        "../../../../skills/skills-for-planning/",
    )
    text = text.replace(
        "../../skills-for-docs/",
        "../../../../skills/skills-for-docs/",
    )
    text = re.sub(
        r"\]\(\.\./([^/)]+)/SKILL\.md\)",
        r"](../../../../skills/utils-skills/\1/SKILL.md)",
        text,
    )
    return text


def discover_skill_files() -> list[Path]:
    """All SKILL.md files under skills/ and plugins/*/skills/."""
    files = sorted(SKILLS_ROOT.glob("**/SKILL.md"))
    files.extend(sorted(REPO_ROOT.glob("plugins/*/skills/**/SKILL.md")))
    # dedupe while preserving order
    seen: set[Path] = set()
    unique: list[Path] = []
    for path in files:
        resolved = path.resolve()
        if resolved not in seen:
            seen.add(resolved)
            unique.append(path)
    return unique


def lint_skill(skill_md: Path) -> tuple[list[str], list[str]]:
    """Return (errors, warnings) for one SKILL.md file."""
    errors: list[str] = []
    warnings: list[str] = []

    text = skill_md.read_text(encoding="utf-8")
    fm = parse_frontmatter(text)
    if fm is None:
        errors.append("frontmatter missing or unparseable")
        return errors, warnings

    for field in REQUIRED_FIELDS:
        if field not in fm or fm[field] in (None, "", []):
            errors.append(f"frontmatter missing required field: {field}")

    folder = skill_md.parent.name
    if fm.get("name") and fm["name"] != folder:
        errors.append(f"`name: {fm['name']}` does not match folder `{folder}`")

    phase = fm.get("phase")
    if phase and phase not in VALID_PHASES:
        errors.append(f"`phase: {phase}` is not in {sorted(VALID_PHASES)}")

    metadata = fm.get("metadata", {}) if isinstance(fm.get("metadata"), dict) else {}
    for key in REQUIRED_METADATA:
        if key not in metadata or not metadata[key]:
            errors.append(f"frontmatter.metadata missing required field: {key}")

    for section in RECOMMENDED_SECTIONS:
        if section not in text:
            warnings.append(f"recommended section missing: {section!r}")

    for link in re.findall(r"\]\(([^)]*SKILL\.md)\)", text):
        target = (skill_md.parent / link).resolve()
        if not target.is_file():
            errors.append(f"broken link to {link} (resolved: {target})")

    return errors, warnings


def check_plugin_sync() -> list[str]:
    """Return errors when plugin copies drift from canonical utils-skills sources."""
    errors: list[str] = []
    for plugin_rel, canonical_rel in PLUGIN_SKILL_SOURCES.items():
        canonical = REPO_ROOT / canonical_rel / "SKILL.md"
        plugin = REPO_ROOT / plugin_rel / "SKILL.md"
        if not canonical.is_file():
            errors.append(f"{plugin_rel}: canonical missing at {canonical_rel}/SKILL.md")
            continue
        if not plugin.is_file():
            errors.append(f"{plugin_rel}: plugin copy missing (run --sync-plugin)")
            continue
        expected = canonical_to_plugin_skill(
            canonical.read_text(encoding="utf-8"),
        )
        actual = plugin.read_text(encoding="utf-8")
        if expected != actual:
            errors.append(
                f"{plugin_rel}: out of sync with {canonical_rel}/SKILL.md "
                f"(run python skills/lint.py --sync-plugin)",
            )
    return errors


CHANGELOG_SKELETON = "_CHANGELOG.md"
AGENTS_MD_MAX_LINES = 140

REQUIRED_AGENTS_SECTIONS = (
    "## Role and scope",
    "## Working cycle",
    "## Session bootstrap",
    "## Commands",
    "## Verification before PR",
    "## Pull requests",
    "## Boundaries",
    "## Where durable knowledge lives",
)

FORBIDDEN_AGENTS_SECTIONS = (
    "### Adopting the kit",
    "## Adopting the kit",
    "## Rules index",
    "## Assumed stack",
    "## References",
)


def check_agents_md() -> list[str]:
    """Validate agent-kit/AGENTS.md structure for the consumer entrypoint template."""
    errors: list[str] = []
    agents = REPO_ROOT / "agent-kit" / "AGENTS.md"
    if not agents.is_file():
        errors.append("agent-kit/AGENTS.md missing")
        return errors

    text = agents.read_text(encoding="utf-8")
    line_count = len(text.splitlines())
    if line_count > AGENTS_MD_MAX_LINES:
        errors.append(
            f"agent-kit/AGENTS.md: {line_count} lines exceeds max {AGENTS_MD_MAX_LINES} "
            "(keep entrypoint a map; move detail to agent-kit/agent-rules/)",
        )
    for section in REQUIRED_AGENTS_SECTIONS:
        if section not in text:
            errors.append(
                f"agent-kit/AGENTS.md: missing required section {section!r}",
            )
    for section in FORBIDDEN_AGENTS_SECTIONS:
        if section in text:
            errors.append(
                "agent-kit/AGENTS.md: adoption/bootstrap content belongs in "
                f"README/guides, not {section!r}",
            )
    if "agent-kit/agent-rules/DOCUMENTATION.md" not in text:
        errors.append(
            "agent-kit/AGENTS.md: must link to agent-kit/agent-rules/DOCUMENTATION.md",
        )
    if "agent-kit/agent-rules/RULES.md" not in text:
        errors.append(
            "agent-kit/AGENTS.md: must link to agent-kit/agent-rules/RULES.md",
        )
    return errors


def check_skeleton_path_casing() -> list[str]:
    """Detect case-only mismatches under agent-kit/skeletons/ (Linux CI safety)."""
    errors: list[str] = []
    skeleton_dir = REPO_ROOT / "agent-kit" / "skeletons"
    if not skeleton_dir.is_dir():
        return errors

    try:
        result = subprocess.run(
            ["git", "ls-files", "agent-kit/skeletons/"],
            capture_output=True,
            text=True,
            check=True,
            cwd=REPO_ROOT,
        )
    except (FileNotFoundError, subprocess.CalledProcessError):
        return errors

    tracked = [line.strip() for line in result.stdout.splitlines() if line.strip()]
    by_lower: dict[str, set[str]] = {}

    for rel in tracked:
        name = Path(rel).name
        by_lower.setdefault(name.lower(), set()).add(name)

    for path in skeleton_dir.iterdir():
        if path.is_file():
            by_lower.setdefault(path.name.lower(), set()).add(path.name)

    for lower, variants in sorted(by_lower.items()):
        if len(variants) > 1:
            errors.append(
                "agent-kit/skeletons/: case collision for "
                f"{lower!r}: {sorted(variants)} — pick one canonical spelling",
            )

    changelog_variants = by_lower.get(CHANGELOG_SKELETON.lower(), set())
    if changelog_variants and CHANGELOG_SKELETON not in changelog_variants:
        errors.append(
            f"agent-kit/skeletons/: CHANGELOG skeleton must be named {CHANGELOG_SKELETON} "
            f"(DOCUMENTATION.md mapping; found {sorted(changelog_variants)})",
        )

    return errors


ADR_REQUIRED_SKELETONS = (
    "_adr-index.md",
    "_adr-entry.md",
    "_adr-0001-record-decisions.md",
    "_adr-0002-system-context.md",
)
FORBIDDEN_SKELETONS = ("_architecture.md",)


def check_adr_skeletons() -> list[str]:
    """Ensure ADR skeletons exist and legacy architecture skeleton is removed."""
    errors: list[str] = []
    skeleton_dir = REPO_ROOT / "agent-kit" / "skeletons"
    if not skeleton_dir.is_dir():
        return errors

    for name in FORBIDDEN_SKELETONS:
        if (skeleton_dir / name).is_file():
            errors.append(
                f"agent-kit/skeletons/: remove deprecated skeleton {name} (use ADR skeletons)",
            )

    for name in ADR_REQUIRED_SKELETONS:
        if not (skeleton_dir / name).is_file():
            errors.append(f"agent-kit/skeletons/: missing required ADR skeleton {name}")

    return errors


AGENT_RULES_DIR = REPO_ROOT / "agent-kit" / "agent-rules"
RULE_FILE_PATTERN = re.compile(r"^[A-Z][A-Z0-9_]*\.md$")
RULE_ID_PATTERN = re.compile(
    r"^### ((?:CORE|COOP|DOC|REPO|ARCH|PY|PER|TEST|VAL|SEC|OBS)-\d+)\s",
    re.MULTILINE,
)
RULE_PREFIX_TO_FILE: dict[str, str] = {
    "CORE": "CORE.md",
    "COOP": "CORE.md",
    "DOC": "DOCUMENTATION.md",
    "REPO": "REPO_GUIDE.md",
    "ARCH": "ARCHITECTURE.md",
    "PY": "PYTHON.md",
    "PER": "PERSISTENCE.md",
    "TEST": "TESTING.md",
    "VAL": "VALIDATION.md",
    "SEC": "SECURITY.md",
    "OBS": "OBSERVABILITY.md",
}
REQUIRED_RULE_FRONTMATTER = ("triggers:", "requires:", "see-also:")
FORBIDDEN_RULE_FRONTMATTER = ("severity-default:",)
RELATIVE_LINK_PATTERN = re.compile(r"\]\(([A-Za-z0-9_]+\.md)\)")


def check_agent_rules() -> list[str]:
    """Validate agent-kit/agent-rules/ naming, frontmatter, IDs, and links."""
    errors: list[str] = []
    rules_dir = AGENT_RULES_DIR
    if not rules_dir.is_dir():
        errors.append("agent-kit/agent-rules/ missing")
        return errors

    rule_files = sorted(rules_dir.glob("*.md"))
    if not rule_files:
        errors.append("agent-kit/agent-rules/: no rule files found")
        return errors

    seen_ids: dict[str, str] = {}

    for path in rule_files:
        rel = path.relative_to(REPO_ROOT).as_posix()
        name = path.name
        if name == "RULES.md":
            continue
        if not RULE_FILE_PATTERN.match(name):
            errors.append(
                f"{rel}: filename must be SCREAMING_SNAKE.md (harness rule convention)",
            )

        text = path.read_text(encoding="utf-8-sig").replace("\r\n", "\n")
        if not text.startswith("---\n"):
            errors.append(f"{rel}: missing YAML frontmatter")
            continue

        end = text.find("\n---\n", 4)
        frontmatter = text[4:end] if end != -1 else ""
        for key in REQUIRED_RULE_FRONTMATTER:
            if key not in frontmatter:
                errors.append(f"{rel}: frontmatter missing {key!r}")
        for key in FORBIDDEN_RULE_FRONTMATTER:
            if key in frontmatter:
                errors.append(f"{rel}: remove deprecated frontmatter {key!r}")

        for link_target in RELATIVE_LINK_PATTERN.findall(text):
            if link_target == "RULES.md":
                continue
            if not (rules_dir / link_target).is_file():
                errors.append(f"{rel}: broken link to {link_target!r}")

        for match in RULE_ID_PATTERN.finditer(text):
            full_id = match.group(1)
            prefix = full_id.split("-", 1)[0]
            expected_file = RULE_PREFIX_TO_FILE.get(prefix)
            if expected_file and name != expected_file:
                errors.append(
                    f"{rel}: rule {full_id} belongs in agent-kit/agent-rules/{expected_file}",
                )
            if full_id in seen_ids:
                errors.append(
                    f"{rel}: duplicate rule id {full_id} (also in {seen_ids[full_id]})",
                )
            else:
                seen_ids[full_id] = rel

    required_rule_files = {
        "CORE.md",
        "DOCUMENTATION.md",
        "REPO_GUIDE.md",
        "ARCHITECTURE.md",
        "PYTHON.md",
        "PERSISTENCE.md",
        "TESTING.md",
        "VALIDATION.md",
        "SECURITY.md",
        "OBSERVABILITY.md",
        "RULES.md",
    }
    present = {p.name for p in rule_files}
    missing = sorted(required_rule_files - present)
    if missing:
        errors.append(
            "agent-kit/agent-rules/: missing expected files: "
            + ", ".join(missing),
        )

    return errors


def sync_plugin_skills() -> int:
    """Regenerate plugin SKILL.md copies from canonical utils-skills sources."""
    written = 0
    for plugin_rel, canonical_rel in PLUGIN_SKILL_SOURCES.items():
        canonical = REPO_ROOT / canonical_rel / "SKILL.md"
        plugin = REPO_ROOT / plugin_rel / "SKILL.md"
        if not canonical.is_file():
            print(f"  SKIP  {plugin_rel}: canonical missing at {canonical_rel}/SKILL.md")
            continue
        content = canonical_to_plugin_skill(canonical.read_text(encoding="utf-8"))
        plugin.parent.mkdir(parents=True, exist_ok=True)
        plugin.write_text(content, encoding="utf-8", newline="\n")
        print(f"  SYNC  {plugin_rel} <- {canonical_rel}/SKILL.md")
        written += 1
    print()
    print(f"Synced {written} plugin skill(s).")
    return 0 if written == len(PLUGIN_SKILL_SOURCES) else 1


def main() -> int:
    parser = argparse.ArgumentParser(description="Lint skill catalog and plugin copies.")
    parser.add_argument(
        "--sync-plugin",
        action="store_true",
        help="Regenerate plugin SKILL.md copies from skills/utils-skills/ sources",
    )
    args = parser.parse_args()

    if args.sync_plugin:
        return sync_plugin_skills()

    skill_files = discover_skill_files()
    if not skill_files:
        print("No SKILL.md files found under skills/ or plugins/*/skills/")
        return 1

    total_errors = 0
    total_warnings = 0
    for skill_md in skill_files:
        try:
            rel = skill_md.relative_to(REPO_ROOT)
        except ValueError:
            rel = skill_md
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

    for err in check_plugin_sync():
        print(f"  ERROR plugin-sync: {err}")
        total_errors += 1

    casing_errors = check_skeleton_path_casing()
    if casing_errors:
        for err in casing_errors:
            print(f"  ERROR skeleton-casing: {err}")
        total_errors += len(casing_errors)
    else:
        print("  OK    agent-kit/skeletons/ path casing")

    adr_skeleton_errors = check_adr_skeletons()
    if adr_skeleton_errors:
        for err in adr_skeleton_errors:
            print(f"  ERROR adr-skeletons: {err}")
        total_errors += len(adr_skeleton_errors)
    else:
        print("  OK    agent-kit/skeletons/ ADR skeletons")

    agents_errors = check_agents_md()
    if agents_errors:
        for err in agents_errors:
            print(f"  ERROR agents-md: {err}")
        total_errors += len(agents_errors)
    else:
        print("  OK    agent-kit/AGENTS.md entrypoint sections")

    agent_rules_errors = check_agent_rules()
    if agent_rules_errors:
        for err in agent_rules_errors:
            print(f"  ERROR agent-rules: {err}")
        total_errors += len(agent_rules_errors)
    else:
        print("  OK    agent-kit/agent-rules/ naming, IDs, and links")

    print()
    print(
        f"Checked {len(skill_files)} skill(s). "
        f"{total_errors} error(s), {total_warnings} warning(s).",
    )
    return 0 if total_errors == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
