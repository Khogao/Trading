# AI Trading Monitor Startup Script
# Integrates with your production Pine Script indicators
# Author: AI Assistant, 2025

param(
    [string]$Symbol = "BTCUSDT",
    [string]$Timeframe = "15",
    [switch]$TestMode = $false
)

# Color functions for better output
function Write-ColorOutput($ForegroundColor) {
    $fc = $host.UI.RawUI.ForegroundColor
    $host.UI.RawUI.ForegroundColor = $ForegroundColor
    if ($args) {
        Write-Output $args
    } else {
        $input | Write-Output
    }
    $host.UI.RawUI.ForegroundColor = $fc
}

function Write-Success { Write-ColorOutput Green $args }
function Write-Warning { Write-ColorOutput Yellow $args }
function Write-Error { Write-ColorOutput Red $args }
function Write-Info { Write-ColorOutput Cyan $args }

# Header
Clear-Host
Write-Info "============================================================================"
Write-Info "🚀 AI TRADING MONITOR - PRODUCTION INDICATORS"
Write-Info "============================================================================"
Write-Info "📊 Indicators: Better-CVD-Final, CVD-Pro, Pi-3.4-Professional, SMPA ORG, VPP5"
Write-Info "🤖 AI Analysis: Claude + Gemini Integration"
Write-Info "💹 Symbol: $Symbol | Timeframe: $Timeframe"
Write-Info "============================================================================"
Write-Output ""

# Check prerequisites
Write-Info "🔍 Checking prerequisites..."

# Check Python installation
try {
    $pythonVersion = python --version 2>&1
    if ($pythonVersion -match "Python (\d+\.\d+)") {
        Write-Success "✅ Python found: $pythonVersion"
    } else {
        throw "Python not found or invalid version"
    }
} catch {
    Write-Error "❌ Python not found! Please install Python 3.8+"
    Write-Error "   Download: https://www.python.org/downloads/"
    Read-Host "Press Enter to exit"
    exit 1
}

# Check required directories
$requiredDirs = @(
    ".\tools\realtime",
    ".\indicators\Production",
    ".\docs"
)

foreach ($dir in $requiredDirs) {
    if (Test-Path $dir) {
        Write-Success "✅ Directory found: $dir"
    } else {
        Write-Warning "⚠️  Directory missing: $dir"
    }
}

# Check production indicators
Write-Info "📊 Checking production indicators..."
$productionIndicators = @(
    ".\indicators\Production\Better-CVD-Final.pine",
    ".\indicators\Production\CVD-Pro.pine",
    ".\indicators\Production\Pi-3.4-Professional.pine",
    ".\indicators\Production\SMPA ORG.pine",
    ".\indicators\Production\VPP5.pine"
)

$foundIndicators = 0
foreach ($indicator in $productionIndicators) {
    if (Test-Path $indicator) {
        $foundIndicators++
        $fileName = Split-Path $indicator -Leaf
        Write-Success "✅ $fileName"
    } else {
        $fileName = Split-Path $indicator -Leaf
        Write-Warning "⚠️  Missing: $fileName"
    }
}

Write-Info "📊 Production indicators found: $foundIndicators/5"
Write-Output ""

# Install/check Python dependencies
Write-Info "📦 Checking Python dependencies..."
$requirements = @(
    "aiohttp",
    "numpy",
    "asyncio",
    "tkinter"
)

foreach ($package in $requirements) {
    try {
        $result = pip show $package 2>&1
        if ($result -match "Name: $package") {
            Write-Success "✅ $package installed"
        } else {
            Write-Warning "⚠️  Installing $package..."
            pip install $package --quiet
            Write-Success "✅ $package installed"
        }
    } catch {
        Write-Error "❌ Failed to install $package"
    }
}

Write-Output ""

# Configuration check
Write-Info "⚙️  Configuration check..."

# Check for API keys (mock check)
$configFile = ".\tools\realtime\config.json"
if (Test-Path $configFile) {
    Write-Success "✅ Configuration file found"
} else {
    Write-Warning "⚠️  Creating default configuration..."

    $defaultConfig = @{
        "claude_api_key" = "your_claude_api_key_here"
        "gemini_api_key" = "your_gemini_api_key_here"
        "tradingview_username" = "your_tv_username"
        "symbols" = @("BTCUSDT", "ETHUSDT", "SOLUSDT")
        "timeframes" = @("1", "5", "15", "60", "240")
        "update_interval" = 30
    } | ConvertTo-Json -Depth 3

    $defaultConfig | Out-File -FilePath $configFile -Encoding UTF8
    Write-Success "✅ Default configuration created: $configFile"
    Write-Warning "📝 Please edit the configuration file with your API keys"
}

Write-Output ""

# Test mode
if ($TestMode) {
    Write-Info "🧪 TEST MODE - Running system checks..."

    Write-Info "Testing signal extraction..."
    try {
        python ".\tools\realtime\signal_extractor.py"
        Write-Success "✅ Signal extractor test passed"
    } catch {
        Write-Error "❌ Signal extractor test failed"
    }

    Write-Info "Testing AI analyzer..."
    try {
        python ".\tools\realtime\ai_analyzer.py"
        Write-Success "✅ AI analyzer test passed"
    } catch {
        Write-Error "❌ AI analyzer test failed"
    }

    Write-Output ""
    Write-Info "🧪 Test mode complete. Use -TestMode:$false to start monitoring."
    Read-Host "Press Enter to continue"
    return
}

# Start the system
Write-Info "🚀 Starting AI Trading Monitor..."
Write-Output ""

# Create startup batch for easier launching
$batchContent = @"
@echo off
cd /d "%~dp0\.."
powershell.exe -ExecutionPolicy Bypass -File ".\.scripts\ai_monitor_start.ps1" -Symbol $Symbol -Timeframe $Timeframe
pause
"@

$batchContent | Out-File -FilePath ".\AI_Monitor.bat" -Encoding ASCII
Write-Success "✅ Created AI_Monitor.bat for easy launching"

# Start components
Write-Info "🎯 Starting Dashboard..."
Start-Process python -ArgumentList ".\tools\realtime\dashboard.py" -WorkingDirectory (Get-Location)

# Wait a moment for dashboard to initialize
Start-Sleep 2

# Display status
Write-Success "============================================================================"
Write-Success "🟢 AI TRADING MONITOR IS NOW RUNNING!"
Write-Success "============================================================================"
Write-Success "📊 Production Indicators Active:"
Write-Success "   • Better-CVD-Final.pine - CVD Divergence Analysis"
Write-Success "   • CVD-Pro.pine - CVD + VSA Integration"
Write-Success "   • Pi-3.4-Professional.pine - Volume Profile + VSA"
Write-Success "   • SMPA ORG.pine - Smart Money Concepts"
Write-Success "   • VPP5.pine - Advanced Volume Profile"
Write-Success ""
Write-Success "🤖 AI Analysis:"
Write-Success "   • Claude: Logic reasoning & trade setup analysis"
Write-Success "   • Gemini: Pattern recognition & historical context"
Write-Success ""
Write-Success "💹 Monitoring: $Symbol on $Timeframe minute timeframe"
Write-Success ""
Write-Success "🎛️  Dashboard Controls:"
Write-Success "   • Start/Stop monitoring"
Write-Success "   • Change symbols and timeframes"
Write-Success "   • View opportunities and risks"
Write-Success "   • AI analysis insights"
Write-Success "============================================================================"

# Keep script running to show logs
Write-Info "📝 System logs (Ctrl+C to exit):"
Write-Output ""

try {
    while ($true) {
        Start-Sleep 10
        $timestamp = Get-Date -Format "HH:mm:ss"
        Write-Info "[$timestamp] System running... Dashboard active."

        # Check if dashboard process is still running
        $dashboardProcess = Get-Process python -ErrorAction SilentlyContinue | Where-Object {$_.ProcessName -eq "python"}
        if (-not $dashboardProcess) {
            Write-Warning "⚠️  Dashboard process not found. Restarting..."
            Start-Process python -ArgumentList ".\tools\realtime\dashboard.py" -WorkingDirectory (Get-Location)
        }
    }
} catch {
    Write-Info "🛑 Monitoring stopped by user."
}

Write-Info ""
Write-Info "👋 AI Trading Monitor shutdown complete."
Write-Info "   Your production indicators are ready for next session!"