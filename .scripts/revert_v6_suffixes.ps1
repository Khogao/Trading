<#
Revert V6 suffixes: rename files ending with ' V6.pine' to remove the suffix,
preserve original names if conflicts by appending -1, -2, ... and commit.
#>
Set-StrictMode -Version Latest
$repo = (Get-Location).ProviderPath
Push-Location $repo

$files = Get-ChildItem -Recurse -Filter '* V6.pine' -File -ErrorAction SilentlyContinue
if (-not $files) { Write-Output "No '* V6.pine' files found."; Pop-Location; exit 0 }

foreach ($f in $files) {
    $orig = $f.FullName
    $dir = $f.DirectoryName
    $nameNoExt = [System.IO.Path]::GetFileNameWithoutExtension($f.Name)
    # remove trailing ' V6'
    $newBase = $nameNoExt -replace '\s+V6$',''
    if (-not $newBase) { Write-Output "Skipping weird filename: $orig"; continue }
    $dst = Join-Path $dir ($newBase + '.pine')
    $suffix = 1
    while (Test-Path $dst) {
        # if destination is the same as source, break
        if ((Get-Item $dst).FullName -eq $orig) { $dst = $orig; break }
        $dst = Join-Path $dir ($newBase + "-$suffix.pine")
        $suffix++
    }
    Write-Output "Renaming:`n  $orig -> $dst"
    try {
        git mv -- "${orig}" "${dst}" 2>&1 | Write-Output
    } catch {
        Write-Output "git mv failed for $orig : $_"
    }
}

# stage and commit
Write-Output 'Staging changes...'
git add -A
$staged = (git diff --cached --name-only) -join "`n"
if ($staged -and $staged.Trim()) {
    Write-Output "Committing changes (files changed):`n$staged"
    git commit -m "chore(reorg): revert V6 suffixes per user request" 2>&1 | Write-Output
} else {
    Write-Output 'No staged changes to commit.'
}

Pop-Location
