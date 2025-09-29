param(
    [string]$Root = "d:\Work\Coding\Trading"
)

$docs = Join-Path $Root 'docs'
$mapping = Import-Csv (Join-Path $docs 'reorg_mapping_status.csv') -ErrorAction Stop
$lint = Import-Csv (Join-Path $docs 'pine_lint_report.csv') -ErrorAction SilentlyContinue

$movePlan = @()
foreach ($row in $mapping) {
    $source = $row.current_path
    if ($source -eq 'current_path') { continue } # skip header duplicated row
    $lintRow = $lint | Where-Object { $_.path -eq $source }
    $issues = if ($null -ne $lintRow) { $lintRow.issues } else { '' }
    $status = if ($row.source_exists -eq 'True' -and $row.target_exists -eq 'False') { 'move_candidate' } elseif ($row.source_exists -eq 'True' -and $row.target_exists -eq 'True') { 'already_at_target' } elseif ($row.source_exists -eq 'False') { 'source_missing' } else { 'unknown' }

    $movePlan += [PSCustomObject]@{
        current_path = $row.current_path
        filename = $row.filename
        new_path = $row.new_path
        target_abs = $row.target_abs
        source_exists = $row.source_exists
        target_exists = $row.target_exists
        target_dir_exists = $row.target_dir_exists
        lint_issues = $issues
        action_suggested = $status
    }
}

$out = Join-Path $docs 'reorg_move_plan.csv'
$movePlan | Export-Csv -Path $out -NoTypeInformation -Encoding UTF8
Write-Host "Wrote move plan to $out"
