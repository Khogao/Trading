<#
.scripts/sr_audit.ps1
Scan Pine scripts (per docs/reorg_manifest.csv) for constructs that may violate the Supreme Rule
Reports files that contain strategy.entry/strategy.order/strategy.exit or auto-order patterns, and files that are Pine v6.

Usage:
  -dry : print report only
  -fix : not implemented (audit-only)
#>

param([switch]$dry)

Set-StrictMode -Version Latest
$repoRoot = (Get-Location).ProviderPath
Push-Location $repoRoot

if (-not (Test-Path docs/reorg_manifest.csv)) { Write-Error "docs/reorg_manifest.csv not found"; exit 1 }
$rows = Import-Csv docs/reorg_manifest.csv

$issues = @()
foreach ($r in $rows) {
    $file = $r.target_path
    if (-not $file) { continue }
    if (-not (Test-Path $file)) { continue }
    $text = Get-Content $file -Raw -ErrorAction SilentlyContinue
    if (-not $text) { continue }

    $found = @()
    if ($text -match 'strategy\.(entry|order|exit)') { $found += 'strategy-calls' }
    if ($text -match 'strategy\.') { $found += 'strategy' }
    if ($text -match 'alertcondition\s*\(') { $found += 'alertcondition' }
    if ($text -match 'request\.security\s*\(') { $found += 'request.security' }
    if ($text -match '@version\s*=\s*6' -or $text -match '\/\/\@version=6') { $found += 'pine-v6' }

    if ($found.Count -gt 0) {
        $issues += [PSCustomObject]@{
            filename = $r.filename
            path = $file
            flags = ($r.flags)
            detections = ($found -join ',')
        }
    }
}

if ($issues.Count -eq 0) { Write-Output "SR audit: no immediate issues detected."; Pop-Location; exit 0 }

Write-Output "SR audit: found $($issues.Count) files with potential SR concerns:`n"
foreach ($i in $issues) {
    Write-Output "$($i.filename) | $($i.path) | flags=$($i.flags) | detections=$($i.detections)"
}

Pop-Location
