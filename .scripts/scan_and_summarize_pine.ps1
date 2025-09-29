<#
.scripts/scan_and_summarize_pine.ps1
Scans all .pine files, extracts metadata and relationships, outputs docs/pine_family_summary.csv
#>
param()
Set-StrictMode -Version Latest
$repo = (Get-Location).ProviderPath
Push-Location $repo

$outPath = 'docs/pine_family_summary.csv'

$files = Get-ChildItem -Recurse -Filter *.pine | Sort-Object FullName

# collect functions map
$funcMap = @{}
$fileRecords = @()

foreach ($f in $files) {
    $content = Get-Content -Raw -ErrorAction SilentlyContinue -Path $f.FullName
    if ($null -eq $content) { $content = '' }
    $lower = $content.ToLower()

    # detect version
    $pv = ''
    if ($content -match "//@version\s*=?\s*(\d+)") { $pv = $matches[1] }
    elseif ($content -match "//\s*pine\s*v(\d)+") { $pv = $matches[1] }
    elseif ($content -match "@version\s*=\s*(\d+)") { $pv = $matches[1] }
    else { $pv = '' }

    # detect type
    $detectedType = ''
    if ($content -match '\bstrategy\s*\(' -or $content -match '\bstrategy\.') { $detectedType = 'strategy' }
    elseif ($content -match '\bindicator\s*\(' -or $content -match '\bstudy\s*\(') { $detectedType = 'indicator' }
    else { $detectedType = 'indicator' }

    # detect SR related constructs
    $srFlags = @()
    if ($content -match 'alertcondition\s*\(') { $srFlags += 'alertcondition' }
    if ($content -match 'request\.security\s*\(') { $srFlags += 'request.security' }
    if ($content -match 'strategy\s*\(') { $srFlags += 'strategy()' }
    if ($content -match 'strategy\.') { $srFlags += 'strategy.' }
    if ($content -match 'pine\s*-?v6' -or $content -match '//@version\s*=?\s*6') { $srFlags += 'pine-v6' }

    # family heuristics from path
    $family = 'other'
    $p = $f.FullName.ToLower()
    if ($p -match '\\wyckoff\\') { $family = 'wyckoff' }
    elseif ($p -match '\\cvd\\') { $family = 'cvd' }
    elseif ($p -match '\\vp\\' -or $p -match 'value-area' -or $p -match '\\vp-' -or $p -match '\\vpp') { $family = 'PA' }
    elseif ($p -match '\\composite\\' -or $p -match 'composite' -or $p -match 'c\+v\+d') { $family = 'composite' }
    elseif ($p -match '\\vsa\\') { $family = 'vsa' }

    # extract user-defined functions (pattern: name(...) => )
    $funcs = @()
    $funcPattern = '([A-Za-z_][A-Za-z0-9_]*)\s*\([^\)]*\)\s*=>'
    foreach ($m in ([regex]::Matches($content,$funcPattern))) { $fn = $m.Groups[1].Value; if ($fn -ne '') { $funcs += $fn } }
    $funcs = $funcs | Select-Object -Unique

    # also collect top-level identifiers (simple heuristic) - names before := or = or var
    $idents = @()
    foreach ($line in ($content -split "\r?\n")) {
        if ($line -match '^[\s\/]*/' ) { continue }
        if ($line -match "^[\s]*([A-Za-z_][A-Za-z0-9_\- ]{0,50})\s*=") { $idents += $matches[1].Trim() }
    }
    $idents = ($idents | Where-Object { $_ -and $_ -ne 'if' -and $_ -ne 'for' } ) | Select-Object -Unique

    $rec = [PSCustomObject]@{
        filename = $f.Name
        path = $f.FullName -replace ([regex]::Escape((Get-Location).ProviderPath + '\\')) , ''
        pine_version = $pv
        detected_type = $detectedType
        family = $family
        sr_flags = ($srFlags -join ';')
        functions = ($funcs -join ';')
        identifiers = ($idents -join ';')
        content_sample = ($content -split "\r?\n")[0..([math]::Min(9, ($content -split "\r?\n").Count-1))] -join ' | '
    }

    $fileRecords += $rec

    # add to func map
    foreach ($fn in $funcs) {
        if (-not $funcMap.ContainsKey($fn)) { $funcMap[$fn] = @() }
        $funcMap[$fn] += $f.Name
    }
}

# determine related files by shared function names (>1 shared func)
foreach ($rec in $fileRecords) {
    $funcs = @()
    if ($rec.functions) { $funcs = $rec.functions -split ';' }
    $related = @{}
    foreach ($fn in $funcs) {
        if ($fn -and $funcMap.ContainsKey($fn)) {
            foreach ($other in $funcMap[$fn]) { if ($other -ne $rec.filename) { if (-not $related.ContainsKey($other)) { $related[$other]=0 }; $related[$other]++ } }
        }
    }
    $relList = $related.GetEnumerator() | Where-Object { $_.Value -ge 1 } | Sort-Object -Property Value -Descending | Select-Object -First 10 | ForEach-Object { $_.Key + '(' + $_.Value + ')' }
    $rec | Add-Member -NotePropertyName related_files -NotePropertyValue ($relList -join ';')

    # suggested rename for v6
    if ($rec.pine_version -eq '6') {
        if ($rec.filename -notmatch 'V6') {
            $base = [System.IO.Path]::GetFileNameWithoutExtension($rec.filename)
            $suggest = "$base V6.pine"
        } else { $suggest = $rec.filename }
    } else { $suggest = '' }
    $rec | Add-Member -NotePropertyName suggested_v6_name -NotePropertyValue $suggest
}

# export CSV
$fileRecords | Select-Object filename,path,pine_version,detected_type,family,sr_flags,functions,identifiers,related_files,suggested_v6_name,content_sample | Export-Csv -Path $outPath -NoTypeInformation -Force
Write-Output "Wrote $outPath with $($fileRecords.Count) records."

Pop-Location
