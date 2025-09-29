<#
.scripts/normalize_filenames.ps1
Purpose: group similar files by family token (e.g., EZZ, PI, VPP, SMPA, KVS) and propose consistent numbering-based renames.
Modes:
 -dry  : print proposed renames
 -apply: perform git mv for the renames (commits the changes)

This script uses the `filename` field from docs/reorg_manifest.csv and the `target_path` to compute renames.
#>

param([switch]$dry, [switch]$apply)

Set-StrictMode -Version Latest
$repoRoot = (Get-Location).ProviderPath
Push-Location $repoRoot

if (-not (Test-Path docs/reorg_manifest.csv)) { Write-Error "docs/reorg_manifest.csv not found"; exit 1 }
$rows = Import-Csv docs/reorg_manifest.csv

# Heuristic: family token is the uppercase alphabetic prefix before first non-letter (e.g., EZZ, PI, VPP, SMPA, KVS)
$groups = @{}
foreach ($r in $rows) {
    $name = $r.filename
    if (-not $name) { continue }
    # Extract token
    $m = [regex]::Match($name, '^[A-Za-z]{2,5}')
    if (-not $m.Success) { continue }
    $token = $m.Value.ToUpper()
    if (-not $groups.ContainsKey($token)) { $groups[$token] = @() }
    $groups[$token] += $r
}

$proposals = @()
foreach ($k in $groups.Keys) {
    $list = $groups[$k]
    if ($list.Count -le 1) { continue }
    # Sort by filename length (shorter = canonical) then alphabetically
    $list = $list | Sort-Object { $_.filename.Length }, { $_.filename }
    # If canonical already matches pattern e.g., EZZ.pine, keep; else propose numbering
    $counter = 1
    foreach ($item in $list) {
        $ext = [IO.Path]::GetExtension($item.filename)
        $base = "$k-$([string]::Format('{0:D2}',$counter))"
        $newName = "$base$ext"
        $newPath = Join-Path (Split-Path $item.target_path -Parent) $newName
        if ($item.target_path -ne $newPath) {
            $proposals += [PSCustomObject]@{
                oldName = $item.filename
                oldPath = $item.target_path
                newName = $newName
                newPath = $newPath
                token = $k
            }
        }
        $counter++
    }
}

if ($proposals.Count -eq 0) { Write-Output "No normalization proposals generated."; Pop-Location; exit 0 }

Write-Output "Normalization proposals ($($proposals.Count)):`n"
foreach ($p in $proposals) { Write-Output "$($p.oldName) -> $($p.newName) ( $($p.oldPath) -> $($p.newPath) )" }

if ($dry) { Write-Output "Dry-run complete. No changes made."; Pop-Location; exit 0 }

if (-not $apply) { Write-Output "Run with -apply to perform git mv operations."; Pop-Location; exit 0 }

foreach ($p in $proposals) {
    $dstDir = Split-Path $p.newPath -Parent
    if (-not (Test-Path $dstDir)) { New-Item -ItemType Directory -Force -Path $dstDir | Out-Null }
    Write-Output "git mv '$($p.oldPath)' '$($p.newPath)'"
    git mv -- "$($p.oldPath)" "$($p.newPath)"
}

git add -A
git commit -m "chore(norm): normalize filenames by family token (automated)"

Pop-Location
