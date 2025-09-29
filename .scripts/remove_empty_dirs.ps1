<#
.scripts/remove_empty_dirs.ps1
Purpose: Find and remove empty directories under the repo after reorg/normalization.
- Excludes core metadata folders (.git, .github, .scripts, .vscode)
- Runs on branch 'restructure/by-family' (created if missing)
- Commits filesystem cleanup if any changes detected
#>
param(
    [switch]$whatif
)

Set-StrictMode -Version Latest

$repoRoot = (Get-Location).ProviderPath
Push-Location $repoRoot

# Ensure we're on the restructure branch
if (git branch --list restructure/by-family) {
    git checkout restructure/by-family
} else {
    git checkout -b restructure/by-family
}

Write-Output "Current branch: $(git rev-parse --abbrev-ref HEAD)"

$excludeRegex = '\\.git|\\.github|\\.vscode|\\.scripts|templates|docs'

$empties = @()
Get-ChildItem -Directory -Recurse -Force | Where-Object { $_.FullName -notmatch $excludeRegex } | ForEach-Object {
    $dir = $_
    $hasFile = Get-ChildItem -Path $dir.FullName -File -Recurse -Force -ErrorAction SilentlyContinue | Select-Object -First 1
    if (-not $hasFile) {
        # Don't delete the repository root
        if ($dir.FullName -ne (Get-Location).ProviderPath) {
            $empties += $dir.FullName
        }
    }
}

if ($empties.Count -eq 0) {
    Write-Output "No empty directories found."
    Pop-Location
    exit 0
}

Write-Output "Empty directories found ($($empties.Count)):"
$empties | ForEach-Object { Write-Output " - $_" }

if ($whatif) {
    Write-Output "WhatIf: no deletions performed."
    Pop-Location
    exit 0
}

Write-Output "Removing empty directories..."
foreach ($p in $empties) {
    Write-Output "Removing: $p"
    Remove-Item -LiteralPath $p -Recurse -Force -ErrorAction SilentlyContinue
}

# Stage and commit any removals
Write-Output "Staging changes..."
git add -A
$porcelain = git status --porcelain
if (-not $porcelain) {
    Write-Output "No tracked changes after cleanup."
    Pop-Location
    exit 0
}

Write-Output "Committing cleanup..."
git commit -m "chore(clean): remove empty directories after normalization (automated)"

Write-Output "Cleanup committed on branch $(git rev-parse --abbrev-ref HEAD)."

Pop-Location
