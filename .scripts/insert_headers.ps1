<#
.scripts/insert_headers.ps1
Inserts the conservative pine header template into production-candidate files that lack a header.
Modes:
 -dry  : show files that would be modified
 -apply: actually modify files and commit the changes
#>

param([switch]$dry, [switch]$apply)

Set-StrictMode -Version Latest
$repoRoot = (Get-Location).ProviderPath
Push-Location $repoRoot

if (-not (Test-Path docs/reorg_manifest.csv)) { Write-Error "docs/reorg_manifest.csv not found"; exit 1 }
if (-not (Test-Path templates/pine_header.template)) { Write-Error "templates/pine_header.template not found"; exit 1 }

$template = Get-Content templates/pine_header.template -Raw
$rows = Import-Csv docs/reorg_manifest.csv

$candidates = $rows | Where-Object { $_.flags -and ($_.flags -split ';') -contains 'production-candidate' }

$toModify = @()
foreach ($r in $candidates) {
    $p = $r.target_path
    if (-not (Test-Path $p)) { continue }
    $content = Get-Content $p -Raw
    # Detect simple header presence: look for @version or 'indicator(' in first 40 lines
    $head = ($content -split "`n", 40) -join "`n"
    if ($head -match '@version' -or $head -match 'indicator\s*\(' -or $head -match 'strategy\s*\(') {
        # assume header exists
        continue
    }
    $toModify += [PSCustomObject]@{ path = $p; filename = $r.filename }
}

if ($toModify.Count -eq 0) { Write-Output "No production-candidate files missing headers."; Pop-Location; exit 0 }

Write-Output "Files missing header: $($toModify.Count)";
foreach ($t in $toModify) { Write-Output "$($t.filename) -> $($t.path)" }

if ($dry) { Write-Output "Dry-run complete. No files modified."; Pop-Location; exit 0 }

foreach ($t in $toModify) {
    $orig = Get-Content $t.path -Raw
    $new = $template + "`n`n" + $orig
    Set-Content -Path $t.path -Value $new -Encoding UTF8
    Write-Output "Inserted header into $($t.path)"
}

git add -A
git commit -m "chore(sr): insert conservative opt-in headers into production-candidate Pine scripts"

Pop-Location
