# Pine CVD Validator - Prevents v5 files from using CVD
param(
    [string]$FilePath = "",
    [ValidateSet("normal", "strict")][string]$Mode = "normal"
)

$workspaceRoot = "D:\Work\Coding\Trading"

Write-Host "PINE CVD VALIDATION" -ForegroundColor Cyan
Write-Host "===================" -ForegroundColor Cyan
Write-Host ""

$CVD_KEYWORDS = @("cvd", "delta", "divergence.*cvd")
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
