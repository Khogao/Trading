<#
.scripts/apply_p0_and_rename_v6.ps1
- Rename Pine v6 files to include ' V6' in filename (except exceptions)
- Move P0 files from docs/pine_priority_table.csv into production/ preserving history via git mv
- Commit changes
Usage: .\.scripts\apply_p0_and_rename_v6.ps1
#>
Set-StrictMode -Version Latest
$repo = (Get-Location).ProviderPath
Push-Location $repo

$priorityPath = 'docs/pine_priority_table.csv'
$summaryPath = 'docs/pine_family_summary.csv'
if (-not (Test-Path $priorityPath)) { Write-Error "$priorityPath missing"; exit 1 }
if (-not (Test-Path $summaryPath)) { Write-Error "$summaryPath missing"; exit 1 }

$priority = Import-Csv $priorityPath
$summary = Import-Csv $summaryPath

# canonical exceptions - do not rename these files even if v6
$exceptions = @('VPP5.pine','SMPA ORG.pine')

# build lookup for pine_version by filename
$pvLookup = @{}
foreach ($s in $summary) { $pvLookup[$s.filename] = $s.pine_version }

# First: rename v6 files across repo (only those present in summary and not exceptions)
$renameMap = @{}
foreach ($s in $summary) {
    if ($s.pine_version -eq '6') {
        $origName = $s.filename
        if ($exceptions -contains $origName) { continue }
        if ($origName -match 'V6') { continue }
        $base = [System.IO.Path]::GetFileNameWithoutExtension($origName)
        $newName = "$base V6.pine"
        if ($newName -eq $origName) { continue }
        # avoid conflict: if newName exists, append -v6 or numeric
        $newPath = Split-Path -Parent $s.path
        $dst = Join-Path $newPath $newName
        if (Test-Path $dst) {
            $i = 1
            do {
                $newNameTry = "$base V6-$i.pine"
                $dst = Join-Path $newPath $newNameTry
                $i++
            } until (-not (Test-Path $dst))
            $newName = [System.IO.Path]::GetFileName($dst)
        }
        $renameMap[$s.path] = (Join-Path $newPath $newName)
    }
}

Write-Output "Preparing to rename $($renameMap.Count) v6 files (skip exceptions)."
foreach ($kv in $renameMap.GetEnumerator()) {
    $src = $kv.Key
    $dst = $kv.Value
    if (-not (Test-Path $src)) { Write-Output "Skip rename - missing source: $src"; continue }
    $dstDir = Split-Path $dst -Parent
    if (-not (Test-Path $dstDir)) { New-Item -ItemType Directory -Force -Path $dstDir | Out-Null }
    Write-Output "git mv -- '$src' '$dst'"
    git mv -- "$src" "$dst" 2>&1 | Write-Output
}

# Second: move P0 files to production/
$prodDir = 'production'
if (-not (Test-Path $prodDir)) { New-Item -ItemType Directory -Force -Path $prodDir | Out-Null }

$moved = @()
foreach ($p in $priority | Where-Object { $_.priority -eq 'P0' }) {
    $fname = $p.filename
    # find current path - check if rename applied
    $possible = @()
    # check summary for path
    $s = $summary | Where-Object { $_.filename -eq $fname } | Select-Object -First 1
    if ($s) { $possible += $s.path }
    # also check if we renamed it earlier into same folder
    # look for renamed entries where path ends with filename
    foreach ($kv in $renameMap.GetEnumerator()) {
        $renSrc = $kv.Key
        $renDst = $kv.Value
        if ([System.IO.Path]::GetFileName($renDst) -eq $fname) { $possible += $renDst }
        if ([System.IO.Path]::GetFileName($renSrc) -eq $fname) { $possible += $renSrc }
    }
    # unique
    $possible = $possible | Sort-Object -Unique
    $srcPath = $possible | Where-Object { Test-Path $_ } | Select-Object -First 1
    if (-not $srcPath) {
        # try to find file by name anywhere
        $found = Get-ChildItem -Recurse -Filter $fname -File -ErrorAction SilentlyContinue | Select-Object -First 1
        if ($found) { $srcPath = $found.FullName }
    }
    if (-not $srcPath) { Write-Output "Skip move - cannot find source for $fname"; continue }
    $dst = Join-Path $prodDir $fname
    # if destination exists, append suffix
    if (Test-Path $dst) {
        $base = [System.IO.Path]::GetFileNameWithoutExtension($fname)
        $i=1
        do {
            $newName = "$base-$i.pine"
            $dst = Join-Path $prodDir $newName
            $i++
        } until (-not (Test-Path $dst))
    }
    $dstDir = Split-Path $dst -Parent
    if (-not (Test-Path $dstDir)) { New-Item -ItemType Directory -Force -Path $dstDir | Out-Null }
    Write-Output "git mv -- '$srcPath' '$dst'"
    git mv -- "$srcPath" "$dst" 2>&1 | Write-Output
    $moved += $dst
}

# stage and commit
Write-Output 'Staging and committing changes...'
git add -A
$commitMsg = 'chore(reorg): move P0 to production & append V6 to v6 scripts (Supreme Rule)'
# check if there are staged changes
$staged = (git diff --cached --name-only) -join "`n"
if ($staged -and $staged.Trim()) {
    git commit -m "$commitMsg" 2>&1 | Write-Output
    Write-Output 'Committed reorg changes.'
} else { Write-Output 'No changes to commit.' }

Pop-Location
