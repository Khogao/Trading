<#
.scripts/pine_lint_and_audit.ps1
Purpose: Heuristic lint & SR audit for pine scripts.
Outputs: docs/pine_audit_report.csv with columns: filename,path,syntax_errors,sr_flags,ready_for_product,notes

Usage: .\.scripts\pine_lint_and_audit.ps1
#>

param(
    [switch]$verbose
)

Set-StrictMode -Version Latest
$repoRoot = (Get-Location).ProviderPath
Push-Location $repoRoot

if (-not (Test-Path docs)) { New-Item -ItemType Directory -Path docs | Out-Null }

# Collect .pine files: prefer manifest target_path, fallback to scanning workspace
$manifestPaths = @()
if (Test-Path docs/reorg_manifest.csv) {
    try { $rows = Import-Csv docs/reorg_manifest.csv -ErrorAction Stop } catch { $rows = @() }
    foreach ($r in $rows) {
        if ($r.target_path -and (Test-Path $r.target_path)) { $manifestPaths += (Get-Item -LiteralPath $r.target_path).FullName }
        elseif ($r.current_path -and (Test-Path $r.current_path)) { $manifestPaths += (Get-Item -LiteralPath $r.current_path).FullName }
    }
}

# Add any .pine files not in manifest
$allPine = Get-ChildItem -Path . -Recurse -Filter *.pine -File -ErrorAction SilentlyContinue | ForEach-Object { $_.FullName }
$paths = ($manifestPaths + $allPine) | Select-Object -Unique

# Prepare report
$report = @()

function Check-SyntaxHeuristics {
    param($text, $path)
    $errors = @()

    # check version marker
    if ($text -notmatch '\/\/\s*\@?version\s*=\s*\d+') { $errors += 'missing-version-marker' }

    # parentheses/braces/brackets balance
    $lpar = ($text -split '\(').Count - 1
    $rpar = ($text -split '\)').Count - 1
    if ($lpar -ne $rpar) { $errors += "paren-mismatch($lpar/$rpar)" }
    $lcur = ($text -split '{').Count - 1
    $rcur = ($text -split '}').Count - 1
    if ($lcur -ne $rcur) { $errors += "curly-mismatch($lcur/$rcur)" }
    $lbr = ($text -split '\[').Count - 1
    $rbr = ($text -split '\]').Count - 1
    if ($lbr -ne $rbr) { $errors += "bracket-mismatch($lbr/$rbr)" }

    # quotes parity
    $double = ($text -split '"').Count - 1
    $single = ($text -split "'").Count - 1
    if (($double % 2) -ne 0) { $errors += "double-quote-odd($double)" }
    if (($single % 2) -ne 0) { $errors += "single-quote-odd($single)" }

    # suspicious consecutive dots (typos) or invisible characters
    if ($text -match '\.\.{2,}') { $errors += 'suspicious-ellipsis' }

    # very short or empty file
    if ($text.Trim().Length -lt 10) { $errors += 'too-short-or-empty' }

    return $errors
}

function Check-SRFlags {
    param($text)
    $found = @()
    if ($text -match 'strategy\.(entry|order|exit)') { $found += 'strategy-calls' }
    if ($text -match 'strategy\s*\(') { $found += 'strategy()' }
    if ($text -match 'alertcondition\s*\(') { $found += 'alertcondition' }
    if ($text -match 'request\.security\s*\(') { $found += 'request.security' }
    if ($text -match '@version\s*=?\s*6' -or $text -match '//\s*@version=6') { $found += 'pine-v6' }
    return $found
}

foreach ($p in $paths) {
    try {
        $text = Get-Content -LiteralPath $p -Raw -ErrorAction Stop
    } catch {
        $report += [PSCustomObject]@{
            filename = [System.IO.Path]::GetFileName($p)
            path = $p
            syntax_errors = 'could-not-read'
            sr_flags = ''
            ready_for_product = 'no'
            notes = 'could not open file'
        }
        continue
    }

    $syntaxErr = Check-SyntaxHeuristics -text $text -path $p
    $sr = Check-SRFlags -text $text

    $ready = 'yes'
    $notes = @()
    if ($syntaxErr.Count -gt 0) { $ready = 'no'; $notes += ('syntax:' + ($syntaxErr -join '|')) }
    if ($sr.Count -gt 0) { $ready = 'no'; $notes += ('sr:' + ($sr -join '|')) }

    $report += [PSCustomObject]@{
        filename = [System.IO.Path]::GetFileName($p)
        path = $p
        syntax_errors = ($syntaxErr -join ';')
        sr_flags = ($sr -join ';')
        ready_for_product = $ready
        notes = ($notes -join ' ; ')
    }
}

# Write CSV
$csvPath = 'docs/pine_audit_report.csv'
$report | Export-Csv -Path $csvPath -NoTypeInformation -Force

# Print summary
$total = $report.Count
$notReady = ($report | Where-Object { $_.ready_for_product -eq 'no' }).Count
Write-Output "Pine lint & SR audit complete. Scanned $total files. Not-ready (redflagged): $notReady"

if ($notReady -gt 0) {
    Write-Output "Redflagged files:"
    $report | Where-Object { $_.ready_for_product -eq 'no' } | ForEach-Object { Write-Output "$($_.filename) | $($_.path) | errors=$($_.syntax_errors) | sr=$($_.sr_flags) | notes=$($_.notes)" }
}

Write-Output "Report written to: $csvPath"

Pop-Location
