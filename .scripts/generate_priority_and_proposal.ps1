<#
.scripts/generate_priority_and_proposal.ps1
- Merge docs/pine_audit_report.csv and docs/reorg_manifest.csv
- Heuristics to assign priority and recommended action
- Generate docs/pine_priority_table.csv and docs/reorg_proposal.csv
- Usage: .\.scripts\generate_priority_and_proposal.ps1 [-apply]
#>
param([switch]$apply)

Set-StrictMode -Version Latest
$repo = (Get-Location).ProviderPath
Push-Location $repo

$reportPath = 'docs/pine_audit_report.csv'
$manifestPath = 'docs/reorg_manifest.csv'
if (-not (Test-Path $reportPath)) { Write-Error "$reportPath missing"; exit 1 }
if (-not (Test-Path $manifestPath)) { Write-Error "$manifestPath missing"; exit 1 }

$report = Import-Csv $reportPath
$manifest = Import-Csv $manifestPath

# helper: find manifest row by filename
function Get-ManifestRow([string]$fname) {
    return $manifest | Where-Object { $_.filename -eq $fname } | Select-Object -First 1
}

$out = @()
$proposal = @()

foreach ($r in $report) {
    $name = $r.filename
    $row = Get-ManifestRow -fname $name
    $path = if ($row) { $row.target_path } else { $r.path }

    # default priority rules
    # - P0: ready_for_product=yes AND no sr_flags AND no syntax errors
    # - P1: ready_for_product=yes but has sr_flags (needs SR review) OR minor syntax
    # - P2: ready_for_product=no with fixable syntax or medium SR
    # - P3: needs archive/delete (legacy, duplicates, corrupted)

    $priority = 'P2'
    if ($r.ready_for_product -eq 'yes') { $priority = 'P0' }
    if ($r.sr_flags) {
        # if any strategy-calls or request.security => escalate
        if ($r.sr_flags -match 'strategy' -or $r.sr_flags -match 'request.security') { $priority = 'P1' }
        else { if ($priority -eq 'P0') { $priority = 'P1' } }
    }
    if ($r.syntax_errors) {
        $priority = 'P2'
    }

    # family heuristics: PI* and SMPA* are family clusters the user warned about
    $family = 'other'
    if ($name -match '^(PI|Pi|PICE)') { $family = 'PI' }
    if ($name -match '^SMPA' -or $name -match 'SMPA') { $family = 'SMPA' }
    if ($name -match '^VPP|^VPP') { $family = 'VPP' }

    # recommended action
    $action = 'review'
    switch ($priority) {
        'P0' { $action = 'keep-production' }
        'P1' { $action = 'sr-review-and-fix' }
        'P2' { $action = 'repair-or-archive' }
        'P3' { $action = 'archive-or-delete' }
    }

    # if family is SMPA or PI and name contains ORG or high-production tokens, prefer keep
    if ($family -eq 'SMPA' -and ($name -match 'ORG' -or $name -match 'SMPA ORG' -or $name -match "SMPA\\+")) { $action = 'keep-production'; $priority='P0' }
    if ($family -eq 'PI' -and ($name -match 'PI 32' -or $name -match 'PI 33' -or $name -match 'PI 34')) { $action = 'keep-production'; $priority='P0' }

    $notes = $r.notes
    $out += [PSCustomObject]@{
        filename = $name
        path = $path
        family = $family
        syntax_errors = $r.syntax_errors
        sr_flags = $r.sr_flags
        ready_for_product = $r.ready_for_product
        priority = $priority
        recommended_action = $action
        notes = $notes
    }

    # proposal: target_path which depends on action
    $targetDir = ''
    switch ($action) {
        'keep-production' { $targetDir = 'production' }
        'sr-review-and-fix' { $targetDir = 'work/sr-review' }
        'repair-or-archive' { $targetDir = 'archive/needs-fix' }
        'archive-or-delete' { $targetDir = 'archive/old' }
        default { $targetDir = 'archive/old' }
    }
    $proposal += [PSCustomObject]@{
        filename = $name
        current_path = $path
        recommended_action = $action
        proposed_target = "$targetDir/$name"
    }
}

$outPath = 'docs/pine_priority_table.csv'
$proposalPath = 'docs/reorg_proposal.csv'
$out | Export-Csv -Path $outPath -NoTypeInformation -Force
$proposal | Export-Csv -Path $proposalPath -NoTypeInformation -Force

Write-Output "Priority table written to $outPath. Proposal written to $proposalPath."

if ($apply) {
    Write-Output 'Applying proposal: performing git mv for keep-production => keep in place, repair/archive => move to archive dirs'
    foreach ($p in $proposal) {
        if ($p.recommended_action -eq 'keep-production') { continue }
        $src = $p.current_path
        $dst = $p.proposed_target
        if (-not (Test-Path $src)) { Write-Output "Skip missing: $src"; continue }
        $dstDir = Split-Path $dst -Parent
        if (-not (Test-Path $dstDir)) { New-Item -ItemType Directory -Force -Path $dstDir | Out-Null }
        Write-Output "git mv '$src' '$dst'"
        git mv -- "$src" "$dst"
    }
    git add -A
    git commit -m 'chore(reorg): apply priority-based reorg (automated)'
    Write-Output 'Applied proposal and committed changes.'
} else {
    Write-Output 'Dry-run completed. Use -apply to perform moves.'
}

Pop-Location
