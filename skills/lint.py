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
`_changelog.md` vs `_CHANGELOG.md`) that break on Linux CI, and verifies
relative links from simulated consumer doc paths after materialization.

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


CHANGELOG_SKELETON = "_changelog.md"
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
            f"agent-kit/skeletons/: changelog skeleton must be named {CHANGELOG_SKELETON} "
            f"(DOCUMENTATION.md mapping; found {sorted(changelog_variants)})",
        )

    return errors


ADR_REQUIRED_SKELETONS = ("_adr.md",)
FORBIDDEN_SKELETONS = (
    "_architecture.md",
    "_adr-index.md",
    "_adr-entry.md",
    "_adr-0001-record-decisions.md",
    "_adr-0002-system-context.md",
)


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

    adr_path = skeleton_dir / "_adr.md"
    if adr_path.is_file():
        text = adr_path.read_text(encoding="utf-8-sig").replace("\r\n", "\n")
        for section in ("Index", "Entry", "Bootstrap"):
            if f"## §{section}" not in text:
                errors.append(
                    f"agent-kit/skeletons/_adr.md: missing ## §{section} section",
                )
        if "docs/adr/README.md" in text:
            errors.append(
                "agent-kit/skeletons/_adr.md: must target docs/adr/changelog.md, not README.md",
            )
        if "docs/adr/changelog.md" not in text:
            errors.append(
                "agent-kit/skeletons/_adr.md: must document docs/adr/changelog.md as §Index target",
            )

    return errors


MARKDOWN_LINK_RE = re.compile(r"\]\(([^)]+)\)")

SKELETON_CONSUMER_PATHS: dict[str, list[str]] = {
    "_database.md": ["docs/database.md"],
    "_docs-guide.md": ["docs/docs-guide.md"],
    "_glossary.md": ["docs/glossary.md"],
    "_specs.md": ["docs/features/example/specs.md"],
    "_plan.md": ["docs/features/example/plan.md"],
    "_report.md": ["docs/features/example/report.md"],
    "_changelog.md": ["docs/features/example/changelog.md"],
}

ADR_SECTION_CONSUMER_PATHS: dict[str, str] = {
    "index": "docs/adr/changelog.md",
    "entry": "docs/adr/0002-example-slug.md",
    "bootstrap": "docs/adr/0001-system-context.md",
}


def _parse_adr_skeleton_sections(path: Path) -> dict[str, str]:
    """Split _adr.md into §Index, §Entry, and §Bootstrap bodies."""
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
    return {key: "\n".join(lines) for key, lines in sections.items()}


def _markdown_links(text: str) -> list[str]:
    links: list[str] = []
    for raw in MARKDOWN_LINK_RE.findall(text):
        target = raw.strip().split()[0]
        if not target or target.startswith("#"):
            continue
        if target.startswith(("http://", "https://", "mailto:")):
            continue
        links.append(target)
    return links


def _agent_kit_markdown_links(text: str) -> list[str]:
    """Relative links into agent-kit/ from materialized consumer docs."""
    return [
        link
        for link in _markdown_links(text)
        if link.startswith("agent-kit/") or "/agent-kit/" in link
    ]


def _link_resolves_from(consumer_rel: str, link: str) -> bool:
    consumer = REPO_ROOT / consumer_rel
    target = (consumer.parent / link).resolve()
    try:
        target.relative_to(REPO_ROOT.resolve())
    except ValueError:
        return False
    return target.is_file()


def check_skeleton_links() -> list[str]:
    """Verify skeleton relative links from simulated post-adopt consumer paths."""
    errors: list[str] = []
    skeleton_dir = REPO_ROOT / "agent-kit" / "skeletons"
    if not skeleton_dir.is_dir():
        return errors

    for skel_name, consumer_paths in SKELETON_CONSUMER_PATHS.items():
        skel_path = skeleton_dir / skel_name
        if not skel_path.is_file():
            continue
        text = skel_path.read_text(encoding="utf-8")
        for link in _agent_kit_markdown_links(text):
            if not any(_link_resolves_from(rel, link) for rel in consumer_paths):
                errors.append(
                    f"agent-kit/skeletons/{skel_name}: link {link!r} broken from "
                    f"{consumer_paths[0]} (materialized path)",
                )

    adr_path = skeleton_dir / "_adr.md"
    if adr_path.is_file():
        parts = _parse_adr_skeleton_sections(adr_path)
        for section, consumer_rel in ADR_SECTION_CONSUMER_PATHS.items():
            body = parts.get(section, "")
            if not body:
                continue
            for link in _agent_kit_markdown_links(body):
                if not _link_resolves_from(consumer_rel, link):
                    errors.append(
                        f"agent-kit/skeletons/_adr.md §{section.title()}: link {link!r} "
                        f"broken from {consumer_rel}",
                    )

    return errors


DEPRECATED_ADR_README = "docs/adr/README.md"
ADR_CHANGELOG_SCAN_ROOTS = (
    REPO_ROOT / "agent-kit",
    REPO_ROOT / "guides",
    REPO_ROOT / "skills",
    REPO_ROOT / "README.md",
)


def check_deprecated_adr_readme_refs() -> list[str]:
    """Fail if kit docs still reference the old docs/adr/README.md index."""
    errors: list[str] = []
    paths: list[Path] = []
    for root in ADR_CHANGELOG_SCAN_ROOTS:
        if root.is_file():
            paths.append(root)
        elif root.is_dir():
            paths.extend(root.rglob("*.md"))
            paths.extend(root.rglob("*.py"))

    for path in paths:
        if not path.is_file():
            continue
        if path.resolve() == Path(__file__).resolve():
            continue
        try:
            text = path.read_text(encoding="utf-8-sig")
        except OSError:
            continue
        if DEPRECATED_ADR_README in text:
            rel = path.relative_to(REPO_ROOT).as_posix()
            errors.append(
                f"{rel}: replace deprecated {DEPRECATED_ADR_README!r} with docs/adr/changelog.md",
            )
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
RULES_INDEX_ROW_PATTERN = re.compile(
    r"^\| ((?:CORE|COOP|DOC|REPO|ARCH|PY|PER|TEST|VAL|SEC|OBS)-\d+) \| .+ \| ([A-Z_]+\.md) \|",
    re.MULTILINE,
)


def collect_defined_rule_ids() -> dict[str, str]:
    """Map rule ID to the file that defines it (repo-relative path)."""
    defined: dict[str, str] = {}
    rules_dir = AGENT_RULES_DIR
    if not rules_dir.is_dir():
        return defined
    for path in rules_dir.glob("*.md"):
        if path.name == "RULES.md":
            continue
        rel = path.relative_to(REPO_ROOT).as_posix()
        text = path.read_text(encoding="utf-8-sig").replace("\r\n", "\n")
        for match in RULE_ID_PATTERN.finditer(text):
            defined[match.group(1)] = rel
    return defined


def parse_rules_md_index() -> dict[str, str]:
    """Map rule ID to file column from RULES.md §Rule ID index."""
    rules_md = AGENT_RULES_DIR / "RULES.md"
    if not rules_md.is_file():
        return {}
    text = rules_md.read_text(encoding="utf-8-sig").replace("\r\n", "\n")
    indexed: dict[str, str] = {}
    for match in RULES_INDEX_ROW_PATTERN.finditer(text):
        indexed[match.group(1)] = match.group(2)
    return indexed


def check_rules_index_sync() -> list[str]:
    """Ensure RULES.md index matches rule IDs defined in agent-rules/."""
    errors: list[str] = []
    defined = collect_defined_rule_ids()
    indexed = parse_rules_md_index()
    if not indexed and defined:
        errors.append("agent-kit/agent-rules/RULES.md: Rule ID index missing or unparseable")
        return errors

    for rule_id, source in sorted(defined.items()):
        if rule_id not in indexed:
            errors.append(
                f"agent-kit/agent-rules/RULES.md: missing index row for {rule_id} (defined in {source})",
            )
            continue
        prefix = rule_id.split("-", 1)[0]
        expected_file = RULE_PREFIX_TO_FILE.get(prefix)
        indexed_file = indexed[rule_id]
        if expected_file and indexed_file != expected_file:
            errors.append(
                f"agent-kit/agent-rules/RULES.md: {rule_id} indexed as {indexed_file}, "
                f"expected {expected_file}",
            )

    for rule_id in sorted(indexed):
        if rule_id not in defined:
            errors.append(
                f"agent-kit/agent-rules/RULES.md: stale index row for {rule_id} (not defined in any rule file)",
            )
    return errors


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

    errors.extend(check_rules_index_sync())
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

    skeleton_link_errors = check_skeleton_links()
    if skeleton_link_errors:
        for err in skeleton_link_errors:
            print(f"  ERROR skeleton-links: {err}")
        total_errors += len(skeleton_link_errors)
    else:
        print("  OK    agent-kit/skeletons/ consumer-path links")

    adr_ref_errors = check_deprecated_adr_readme_refs()
    if adr_ref_errors:
        for err in adr_ref_errors:
            print(f"  ERROR adr-refs: {err}")
        total_errors += len(adr_ref_errors)
    else:
        print("  OK    docs/adr/changelog.md references")

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
