# Pine CVD Validator - SMART detection (không máy móc nữa!)
param(
    [string]$FilePath = "",
    [ValidateSet("normal", "strict")][string]$Mode = "normal"
)

$workspaceRoot = "D:\Work\Coding\Trading"

Write-Host "PINE CVD VALIDATION (Smart Detection)" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

# SMART KEYWORDS - chỉ match CVD THẬT, không phải PA divergence hay VP delta
$CVD_KEYWORDS = @(
    '\bcvd\b',                          # Cumulative Volume Delta
    'requestVolumeDelta',               # Pine v6 CVD function
    'cumulative.*volume.*delta',        # CVD full name
    'order.*flow.*delta',               # Order flow context
    'buy.*sell.*pressure.*cumulative'   # Institutional flow
)

# EXCLUSIONS - files không cần check (không có CVD)
$EXCLUDED_FILES = @(
    'SMPA',           # Smart Money PA - không có CVD, chỉ PA divergence
    'VPP',            # Volume Profile - delta là volume distribution, không phải CVD
    'Pi314.pine'      # Context engine - không có CVD
)

$FAKE_CVD = @("close\s*>\s*close\[1\]\s*\?\s*volume")

if ($FilePath) {
    $files = @(Get-Item (Join-Path $workspaceRoot $FilePath))
} else {
    $files = Get-ChildItem "$workspaceRoot\indicators\Production\*.pine"
}

$violations = 0
$checked = 0

foreach ($f in $files) {
    $checked++
    
    # Skip excluded files (SMPA, VPP - không có CVD thật)
    $skip = $false
    foreach ($excl in $EXCLUDED_FILES) {
        if ($f.Name -like "*$excl*") {
            Write-Host "Skipping: $($f.Name) (excluded - no real CVD)" -ForegroundColor Gray
            $skip = $true
            break
        }
    }
    if ($skip) { continue }
    
    $content = Get-Content $f.FullName -Raw
    
    $usesCVD = $false
    foreach ($kw in $CVD_KEYWORDS) {
        if ($content -match $kw) { $usesCVD = $true; break }
    }
    
    if (-not $usesCVD) { continue }
    
    Write-Host "Checking: $($f.Name)" -ForegroundColor Yellow
    
    if ($content -match "//@version=(\d+)") {
        $ver = [int]$Matches[1]
        if ($ver -lt 6) {
            Write-Host "  [X] Pine v$ver < 6" -ForegroundColor Red
            $violations++
        } else {
            Write-Host "  [OK] Pine v$ver" -ForegroundColor Green
        }
    }
    
    if (-not ($content -match "import\s+TradingView/ta/\d+")) {
        if ($content -match "//@version=(\d+)" -and [int]$Matches[1] -ge 6) {
            Write-Host "  [X] Missing TradingView/ta import" -ForegroundColor Red
            $violations++
        }
    } else {
        Write-Host "  [OK] Has TA import" -ForegroundColor Green
    }
    
    foreach ($pattern in $FAKE_CVD) {
        if ($content -match $pattern) {
            Write-Host "  [X] Fake CVD pattern found" -ForegroundColor Red
            $violations++
        }
    }
}

Write-Host ""
Write-Host "Checked: $checked files" -ForegroundColor Cyan
Write-Host "Violations: $violations" -ForegroundColor $(if ($violations -eq 0) { "Green" } else { "Red" })

if ($violations -gt 0 -and $Mode -eq "strict") {
    Write-Host ""
    Write-Host "COMMIT BLOCKED!" -ForegroundColor Red
    exit 1
}

exit 0
