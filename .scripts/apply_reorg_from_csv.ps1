<#
apply_reorg_from_csv.ps1
- Reads docs/reorg_proposal_from_user.csv with headers: current_path,filename,classification,analysis,new_path
- Dry-run mode prints git mv commands and reports missing sources.
- With -Apply switch will run git mv and commit.
#>
param(
    [switch]$Apply = $false
)

Set-StrictMode -Version Latest
$repo = (Get-Location).ProviderPath
Push-Location $repo

$csv = 'docs/reorg_proposal_from_user.csv'
if (-not (Test-Path $csv)) { Write-Error "Missing $csv"; exit 1 }

$rows = Import-Csv $csv
$commands = @()
$missing = @()
$malformed = @()
$foundCount = 0

function Resolve-SourcePath {
    param($srcPath, $filename)
    # If explicit path exists, return it
    if ($srcPath -and (Test-Path $srcPath)) { return (Get-Item $srcPath).FullName }
    # Otherwise try to find by filename anywhere under the repo
    if (-not $filename) { return $null }
    $foundMatches = Get-ChildItem -Path $repo -Recurse -File -ErrorAction SilentlyContinue | Where-Object { $_.Name -ieq $filename }
    if ($foundMatches.Count -eq 1) { return $foundMatches[0].FullName }
    if ($foundMatches.Count -gt 1) {
        Write-Output "Ambiguous matches for $filename - choosing first and listing others in report"
        $foundMatches | ForEach-Object { Write-Output "  candidate: $($_.FullName)" }
        return $foundMatches[0].FullName
    }
    return $null
}

foreach ($r in $rows) {
    # Defensive: ensure expected headers exist
    $srcRaw = $r.current_path -as [string]
    $filename = $r.filename -as [string]
    $dstRaw = $r.new_path -as [string]

    if (-not $filename) {
        $malformed += @{ row = $r; reason = 'missing filename' }
        continue
    }

    # Resolve source: prefer explicit path, else search by filename
    $resolvedSrc = Resolve-SourcePath -srcPath $srcRaw -filename $filename
    if (-not $resolvedSrc) {
        if ($srcRaw -and $srcRaw.Trim() -ne '') { $missing += $srcRaw } else { $missing += $filename }
        continue
    }

    if (-not $dstRaw -or $dstRaw.Trim() -eq '') {
        $malformed += @{ row = $r; reason = 'missing new_path' }
        continue
    }

    $dst = $dstRaw.Trim()
    $dstDir = Split-Path $dst -Parent
    if (-not $dstDir -or $dstDir -eq '') {
        $malformed += @{ row = $r; reason = "invalid new_path: $dst" }
        continue
    }

    # ensure target dir exists (dry-run will create it in apply)
    $commands += @{ src = $resolvedSrc; dst = $dst; filename = $filename }
    $foundCount++
}

Write-Output "Dry-run: $foundCount planned moves, $($missing.Count) unresolved sources, $($malformed.Count) malformed rows."
if ($missing.Count -gt 0) {
    Write-Output "Unresolved sources (not found at given path and not found by filename):"
    $missing | ForEach-Object { Write-Output "  $_" }
}
if ($malformed.Count -gt 0) {
    Write-Output "Malformed CSV rows (skipped):"
    foreach ($m in $malformed) { Write-Output "  reason: $($m.reason) | row: $([string]::Join(',', ($m.row.PSObject.Properties | ForEach-Object { $_.Value })) )" }
}

if ($commands.Count -eq 0) { Write-Output 'No commands to run.'; Pop-Location; exit 0 }

Write-Output 'Planned git mv commands (dry-run):'
foreach ($c in $commands) { Write-Output "git mv -- '$($c.src)' '$($c.dst)'" }

if ($Apply.IsPresent) {
    Write-Output 'Applying moves...'
    foreach ($c in $commands) {
        $dstDir = Split-Path $c.dst -Parent
        if (-not (Test-Path $dstDir)) { New-Item -ItemType Directory -Force -Path $dstDir | Out-Null }
        git mv -- "$($c.src)" "$($c.dst)" 2>&1 | Write-Output
    }
    git add -A
    git commit -m "chore(reorg): apply user reorg mapping" 2>&1 | Write-Output
}

Pop-Location
