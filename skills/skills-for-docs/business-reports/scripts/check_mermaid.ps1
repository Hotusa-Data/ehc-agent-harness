<#
.SYNOPSIS
    Lightweight Mermaid sanity checker for business-reports (PowerShell version).

.DESCRIPTION
    Surface-level checks per ```mermaid block:
      - accTitle present
      - accDescr present
      - No forbidden %%{init} directives
      - Balanced braces, brackets, parens
      - classDef shape: classDef <name> fill:#...

    Mirrors scripts/check_mermaid.sh. Does NOT invoke mmdc (no real parser).
    If mmdc is needed, run the bash version under WSL / Git Bash.

.PARAMETER ReportPath
    Path to the markdown file to check.

.EXAMPLE
    pwsh -File scripts/check_mermaid.ps1 docs/features/upgrade/report.md
    powershell -File scripts/check_mermaid.ps1 docs/features/upgrade/report.md

.NOTES
    Exit 0 if all blocks pass, 1 if any block fails, 2 on invocation errors.
#>
[CmdletBinding()]
param(
    [Parameter(Mandatory = $true, Position = 0)]
    [string]$ReportPath
)

$ErrorActionPreference = 'Stop'

if (-not (Test-Path -LiteralPath $ReportPath -PathType Leaf)) {
    Write-Error "File not found: $ReportPath"
    exit 2
}

# Read the file as a single string and extract ```mermaid ... ``` blocks
$content = Get-Content -LiteralPath $ReportPath -Raw

$pattern = '(?ms)^```mermaid\s*\r?\n(.*?)\r?\n```\s*$'
$matches = [regex]::Matches($content, $pattern)

if ($matches.Count -eq 0) {
    Write-Host "No mermaid blocks found in $ReportPath - nothing to check."
    exit 0
}

Write-Host ("Checking {0} mermaid block(s) in {1}" -f $matches.Count, $ReportPath)
Write-Host "  (surface checks only - install mmdc for full parser validation)"
Write-Host ""

$failed = 0

function Test-Block {
    param(
        [string]$BlockText,
        [string]$Label
    )

    $issues = [System.Collections.Generic.List[string]]::new()

    if ($BlockText -notmatch '(?m)^\s*accTitle:') {
        $issues.Add('missing accTitle') | Out-Null
    }
    if ($BlockText -notmatch '(?m)^\s*accDescr:') {
        $issues.Add('missing accDescr') | Out-Null
    }
    if ($BlockText -match '%%\{\s*init') {
        $issues.Add('contains forbidden %%{init} directive') | Out-Null
    }

    $openBrace = ([regex]::Matches($BlockText, '\{')).Count
    $closeBrace = ([regex]::Matches($BlockText, '\}')).Count
    $openBrack = ([regex]::Matches($BlockText, '\[')).Count
    $closeBrack = ([regex]::Matches($BlockText, '\]')).Count
    $openParen = ([regex]::Matches($BlockText, '\(')).Count
    $closeParen = ([regex]::Matches($BlockText, '\)')).Count

    if ($openBrace -ne $closeBrace) {
        $issues.Add("unbalanced {} - open=$openBrace close=$closeBrace") | Out-Null
    }
    if ($openBrack -ne $closeBrack) {
        $issues.Add("unbalanced [] - open=$openBrack close=$closeBrack") | Out-Null
    }
    if ($openParen -ne $closeParen) {
        $issues.Add("unbalanced () - open=$openParen close=$closeParen") | Out-Null
    }

    foreach ($line in $BlockText -split "`n") {
        if ($line -match '^\s*classDef\s') {
            if ($line -notmatch 'classDef\s+[A-Za-z_][A-Za-z0-9_]*\s+fill:') {
                $issues.Add("malformed classDef: $($line.Trim())") | Out-Null
            }
        }
    }

    if ($issues.Count -eq 0) {
        Write-Host "  [OK] $Label"
        return $true
    } else {
        Write-Host "  [FAIL] $Label"
        foreach ($issue in $issues) {
            Write-Host "      - $issue"
        }
        return $false
    }
}

for ($i = 0; $i -lt $matches.Count; $i++) {
    $blockText = $matches[$i].Groups[1].Value
    $label = "block $($i + 1)"
    if (-not (Test-Block -BlockText $blockText -Label $label)) {
        $failed++
    }
}

Write-Host ""
if ($failed -eq 0) {
    Write-Host "All $($matches.Count) block(s) passed surface checks."
    exit 0
} else {
    Write-Host "$failed of $($matches.Count) block(s) failed. Fix and re-run."
    exit 1
}
