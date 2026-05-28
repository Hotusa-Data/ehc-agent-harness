#!/usr/bin/env bash
# check_mermaid.sh — lightweight Mermaid sanity checker for business-reports
#
# What it DOES check (surface-level, no real Mermaid parser):
#   - Each ```mermaid block has matching ``` closing
#   - Balanced braces/brackets/parens within the block ({}, [], ())
#   - accTitle present
#   - accDescr present
#   - No forbidden %%{init} directives
#   - classDef lines have basic shape: `classDef <name> fill:#...,stroke:#...`
#   - If mmdc (@mermaid-js/mermaid-cli) is installed, runs real validation too
#
# What it DOES NOT check:
#   - Full Mermaid grammar (no AST parsing)
#   - Whether nodes referenced in edges are actually defined
#   - Whether the diagram renders meaningfully — only that it parses
#
# Usage: bash scripts/check_mermaid.sh <path-to-report.md>
# Exit: 0 if all blocks pass, 1 if any block fails

set -euo pipefail

if [[ $# -ne 1 ]]; then
    echo "Usage: $0 <path-to-report.md>" >&2
    exit 2
fi

report="$1"

if [[ ! -f "$report" ]]; then
    echo "File not found: $report" >&2
    exit 2
fi

# Detect mmdc availability AND a working browser (mmdc requires Chrome/Chromium to render)
has_mmdc=false
if command -v mmdc >/dev/null 2>&1; then
    if command -v google-chrome >/dev/null 2>&1 \
        || command -v chromium >/dev/null 2>&1 \
        || command -v chromium-browser >/dev/null 2>&1 \
        || [[ -n "${PUPPETEER_EXECUTABLE_PATH:-}" ]]; then
        has_mmdc=true
    fi
fi

# Extract mermaid blocks into temporary files
tmpdir=$(mktemp -d)
trap 'rm -rf "$tmpdir"' EXIT

awk '
    /^```mermaid[[:space:]]*$/ { in_block=1; block_num++; next }
    /^```[[:space:]]*$/ && in_block { in_block=0; next }
    in_block { print > ("'"$tmpdir"'/block_" block_num ".mmd") }
' "$report"

# If no mermaid blocks, exit cleanly with a note
shopt -s nullglob
blocks=("$tmpdir"/block_*.mmd)
if [[ ${#blocks[@]} -eq 0 ]]; then
    echo "No mermaid blocks found in $report — nothing to check."
    exit 0
fi

failed=0
echo "Checking ${#blocks[@]} mermaid block(s) in $report"
if $has_mmdc; then
    echo "  mmdc detected — will run real parser after surface checks"
elif command -v mmdc >/dev/null 2>&1; then
    echo "  mmdc installed but no Chrome/Chromium found — surface checks only"
else
    echo "  mmdc not installed — surface checks only (install @mermaid-js/mermaid-cli for full validation)"
fi
echo

check_block() {
    local file="$1"
    local label="$2"
    local content
    content=$(cat "$file")
    local issues=()

    # accTitle present
    if ! grep -q '^[[:space:]]*accTitle:' "$file"; then
        issues+=("missing accTitle")
    fi

    # accDescr present
    if ! grep -q '^[[:space:]]*accDescr:' "$file"; then
        issues+=("missing accDescr")
    fi

    # Forbidden %%{init} directives
    if grep -q '%%{[[:space:]]*init' "$file"; then
        issues+=("contains forbidden %%{init} directive")
    fi

    # Balanced braces/brackets/parens — counts only, not strict order
    local open_brace close_brace open_brack close_brack open_paren close_paren
    open_brace=$(grep -o '{' "$file" | wc -l)
    close_brace=$(grep -o '}' "$file" | wc -l)
    open_brack=$(grep -o '\[' "$file" | wc -l)
    close_brack=$(grep -o '\]' "$file" | wc -l)
    open_paren=$(grep -o '(' "$file" | wc -l)
    close_paren=$(grep -o ')' "$file" | wc -l)

    if [[ $open_brace -ne $close_brace ]]; then
        issues+=("unbalanced {} — open=$open_brace close=$close_brace")
    fi
    if [[ $open_brack -ne $close_brack ]]; then
        issues+=("unbalanced [] — open=$open_brack close=$close_brack")
    fi
    if [[ $open_paren -ne $close_paren ]]; then
        issues+=("unbalanced () — open=$open_paren close=$close_paren")
    fi

    # classDef shape: classDef <name> fill:#...
    while IFS= read -r line; do
        if [[ "$line" =~ ^[[:space:]]*classDef[[:space:]] ]]; then
            if ! [[ "$line" =~ classDef[[:space:]]+[a-zA-Z_][a-zA-Z0-9_]*[[:space:]]+fill: ]]; then
                issues+=("malformed classDef: $(echo "$line" | sed 's/^[[:space:]]*//')")
            fi
        fi
    done < "$file"

    # mmdc real validation
    if $has_mmdc; then
        local mmdc_out
        if ! mmdc_out=$(mmdc -i "$file" -o "$file.svg" 2>&1); then
            issues+=("mmdc parse error: $(echo "$mmdc_out" | head -3 | tr '\n' ' ')")
        fi
        rm -f "$file.svg"
    fi

    if [[ ${#issues[@]} -eq 0 ]]; then
        echo "  ✅ $label — ok"
        return 0
    else
        echo "  ❌ $label:"
        for issue in "${issues[@]}"; do
            echo "     - $issue"
        done
        return 1
    fi
}

for block in "${blocks[@]}"; do
    label="block $(basename "$block" .mmd | sed 's/block_//')"
    if ! check_block "$block" "$label"; then
        failed=$((failed + 1))
    fi
done

echo

if [[ $failed -eq 0 ]]; then
    echo "All ${#blocks[@]} block(s) passed surface checks."
    exit 0
else
    echo "$failed of ${#blocks[@]} block(s) failed. Fix and re-run."
    exit 1
fi
