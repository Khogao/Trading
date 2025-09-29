param(
    [string]$Root = "d:\Work\Coding\Trading",
    [switch]$DryRun
)

$docs = Join-Path $Root 'docs'
$planPath = Join-Path $docs 'reorg_move_plan.csv'
$outActions = Join-Path $docs 'reorg_move_actions.csv'

if (-not (Test-Path $planPath)) { Write-Error "Move plan not found: $planPath"; exit 1 }

$plan = Import-Csv -Path $planPath

$actions = @()
foreach ($row in $plan) {
    if ($row.action_suggested -ne 'move_candidate') { continue }
    $src = $row.current_path
    $tgt = $row.target_abs
    $tgtDir = Split-Path $tgt -Parent

    if (-not (Test-Path $src)) {
        $actions += [PSCustomObject]@{ current_path=$src; target_abs=$tgt; result='source_missing'; note='skipped' }
        continue
    }

    if (-not (Test-Path $tgtDir)) {
        if ($DryRun) { $actions += [PSCustomObject]@{ current_path=$src; target_abs=$tgt; result='dir_would_be_created'; note=$tgtDir } }
        else { New-Item -ItemType Directory -Path $tgtDir -Force | Out-Null; $actions += [PSCustomObject]@{ current_path=$src; target_abs=$tgt; result='dir_created'; note=$tgtDir } }
    }

    if (Test-Path $tgt) {
        $actions += [PSCustomObject]@{ current_path=$src; target_abs=$tgt; result='target_exists'; note='skipped' }
        continue
    }

    if ($DryRun) {
        $actions += [PSCustomObject]@{ current_path=$src; target_abs=$tgt; result='would_copy'; note='dryrun' }
    } else {
        Copy-Item -LiteralPath $src -Destination $tgt -Force
        $actions += [PSCustomObject]@{ current_path=$src; target_abs=$tgt; result='copied'; note='ok' }
    }
}

$actions | Export-Csv -Path $outActions -NoTypeInformation -Encoding UTF8
Write-Host "Wrote actions log to $outActions"
