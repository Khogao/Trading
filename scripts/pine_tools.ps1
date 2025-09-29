<#
Simple Pine tooling script:
- Generates a mapping status CSV comparing docs/reorg_mapping_reconstructed.csv to actual files
- Scans all .pine files and performs light heuristic lint checks
- Outputs two CSVs into docs/: reorg_mapping_status.csv and pine_lint_report.csv
#>
param(
    [string]$Root = "d:\Work\Coding\Trading"
)

Set-StrictMode -Version Latest

$docs = Join-Path $Root 'docs'
if (-not (Test-Path $docs)) { New-Item -ItemType Directory -Path $docs | Out-Null }

$mappingCsv = Join-Path $docs 'reorg_mapping_reconstructed.csv'
$outMapping = Join-Path $docs 'reorg_mapping_status.csv'

if (-not (Test-Path $mappingCsv)) {
    Write-Error "Mapping CSV not found: $mappingCsv"
    exit 1
}

$mapping = Import-Csv -Path $mappingCsv -Header current_path, filename, new_path | ForEach-Object {
    $_ | Add-Member -NotePropertyName source_exists -NotePropertyValue $false -Force
    $_ | Add-Member -NotePropertyName target_exists -NotePropertyValue $false -Force
    $_
}

$results = @()
foreach ($row in $mapping) {
    $source = $row.current_path
    $targetRel = $row.new_path
    $sourceExists = Test-Path $source
    $targetAbs = Join-Path $Root $targetRel
    $targetDir = Split-Path $targetAbs -Parent
    $targetExists = Test-Path $targetAbs

    $results += [PSCustomObject]@{
        current_path      = $source
        filename          = $row.filename
        new_path          = $targetRel
        source_exists     = $sourceExists
        target_exists     = $targetExists
        target_dir_exists = (Test-Path $targetDir)
        target_abs        = $targetAbs
    }
}

$results | Export-Csv -Path $outMapping -NoTypeInformation -Encoding UTF8
Write-Host "Wrote mapping status to $outMapping"

# Lightweight lint over all .pine files
$pineFiles = Get-ChildItem -Path $Root -Recurse -Include *.pine -File | Select-Object -ExpandProperty FullName
$lintOut = Join-Path $docs 'pine_lint_report.csv'

$lintResults = @()
foreach ($f in $pineFiles) {
    $text = Get-Content -LiteralPath $f -Raw -ErrorAction SilentlyContinue
    if ($null -eq $text) { $text = "" }
    $text = [string]$text
    $hasVersion = $text -match "@version\s*=\s*\d+"
    # parentheses and bracket balance — use Measure-Object for stable numeric counts
    $chars = @($text.ToCharArray())
    $openParens = ($chars | Where-Object { $_ -eq '(' } | Measure-Object).Count
    $closeParens = ($chars | Where-Object { $_ -eq ')' } | Measure-Object).Count
    $openBrack = ($chars | Where-Object { $_ -eq '[' } | Measure-Object).Count
    $closeBrack = ($chars | Where-Object { $_ -eq ']' } | Measure-Object).Count
    $openCurl = ($chars | Where-Object { $_ -eq '{' } | Measure-Object).Count
    $closeCurl = ($chars | Where-Object { $_ -eq '}' } | Measure-Object).Count
    $nonAscii = ($chars | Where-Object { ([int]$_) -gt 127 } | Measure-Object).Count

    $issues = @()
    if (-not $hasVersion) { $issues += 'missing_version' }
    if ($openParens -ne $closeParens) { $issues += 'paren_mismatch' }
    if ($openBrack -ne $closeBrack) { $issues += 'bracket_mismatch' }
    if ($openCurl -ne $closeCurl) { $issues += 'curl_mismatch' }
    if ($nonAscii -gt 0) { $issues += 'non_ascii_chars' }

    $lintResults += [PSCustomObject]@{
        path            = $f
        has_version     = $hasVersion
        paren_open      = $openParens
        paren_close     = $closeParens
        bracket_open    = $openBrack
        bracket_close   = $closeBrack
        curl_open       = $openCurl
        curl_close      = $closeCurl
        non_ascii_chars = $nonAscii
        issues          = ($issues -join ';')
    }
}

$lintResults | Export-Csv -Path $lintOut -NoTypeInformation -Encoding UTF8
Write-Host "Wrote lint report to $lintOut"

Write-Host "Done."
