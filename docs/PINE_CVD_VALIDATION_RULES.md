# 🔥 CRITICAL: Pine Script CVD Validation Rules

## Rule Enforcement Levels

### CRITICAL (Blocks Commit)
1. **Pine Version v6+ Required for CVD**
   - Any file using CVD keywords MUST use `//@version=6` or higher
   - Keywords: `cvd`, `delta`, `order flow`, `buy sell pressure`, `divergence`
   
2. **TradingView/ta Import Required**
   - Must have `import TradingView/ta/8 as tav6` (or higher version)
   
3. **No Fake CVD Patterns**
   - FORBIDDEN: `close > close[1] ? volume : -volume`
   - FORBIDDEN: Using close direction as delta
   - REQUIRED: `tav6.requestVolumeDelta()` for accurate CVD

### WARNING (Reports but Doesn't Block)
1. No `ta.requestVolumeDelta()` found despite CVD usage
2. Old import versions (ta/7 or lower)

---

## How to Use

### 1. Manual Validation (VSCode Task)
Press `Ctrl+Shift+P` → "Run Task" → "🔥 CRITICAL: Validate Pine CVD Usage"

### 2. Quick Lint Current File
Press `Ctrl+Shift+P` → "Run Task" → "🔍 Quick Pine Lint (Current File)"

### 3. Pre-Commit Validation (Auto)
Git hook automatically runs before every commit in **STRICT MODE**
- ✅ Pass → Commit proceeds
- ❌ Fail → Commit BLOCKED

### 4. Command Line
```powershell
# Normal mode (report only)
.\scripts\validate_pine_cvd.ps1

# Strict mode (blocks on violations)
.\scripts\validate_pine_cvd.ps1 -Mode strict

# Single file
.\scripts\validate_pine_cvd.ps1 -FilePath "indicators/Production/CVD+.pine"
```

---

## Example Violations

### ❌ WRONG (Pine v5 with CVD)
```pine
//@version=5
indicator("My CVD", overlay=false)

f_cvd() =>
    var float cvd = 0.0
    delta = close > close[1] ? volume : -volume  // FAKE CVD!
    cvd := cvd + delta
    cvd
```

**Violations:**
- `PINE_VERSION`: v5 < 6
- `MISSING_TA_IMPORT`: No TradingView/ta import
- `FAKE_CVD`: Line 6 - Using close direction as delta

---

### ✅ CORRECT (Pine v6 with proper CVD)
```pine
//@version=6
indicator("My CVD", overlay=false)
import TradingView/ta/8 as tav6

f_cvd() =>
    [_o, _h, _l, _c] = tav6.requestVolumeDelta("1", "ALL")
    _c  // TRUE buy/sell delta from exchange
```

**Result:** All checks pass ✅

---

## Why This Matters

### Real Bug Example: PI34_Ultimate_AIO
**Before Fix (2025-10-03):**
- Used Pine v5 with fake CVD (close direction)
- All divergence signals were WRONG
- Alert system win rates were misleading
- Users got bad trade signals

**After Fix:**
- Upgraded to Pine v6
- Uses `tav6.requestVolumeDelta()`
- CVD now reflects TRUE institutional order flow
- Divergence signals accurate

### Impact
- **Bug Type:** CRITICAL - Data accuracy
- **Severity:** High - Affects all trading decisions
- **Detection:** Manual code review (now automated)
- **Prevention:** This validation system

---

## Files Validated

### Production Indicators (13 files)
1. ✅ Better CVD.pine - v6, proper CVD
2. ✅ CVD+.pine - v6, proper CVD
3. ✅ CVPZero.pine - v6, proper CVD
4. ✅ CVPZero_Lite.pine - v6, proper CVD
5. ✅ Pi34 Pro.pine - v6, proper CVD
6. ✅ PI34_Ultimate_AIO.pine - v6, proper CVD (FIXED 2025-10-03)
7. ⚠️ Greg_HiveScale_Unified.pine - Check needed
8. ⚠️ Greg_HiveScale_Unified_VPP.pine - Check needed
9. ⚠️ CVP314.pine - Check needed
10. ✅ Pi314.pine - No CVD, VP only
11. ✅ SMPA ORG.pine - No CVD, PA only
12. ✅ VPP5+.pine - No CVD, VP only
13. ✅ VPP6++.pine - No CVD, VP only

---

## Installation

### Enable Auto-Validation on Save (Optional)
1. Install VSCode extension: `emeraldwalk.RunOnSave`
2. Settings already configured in `.vscode/settings.json`
3. Every time you save a `.pine` file → auto-validates

### Test Validation
```powershell
# Test on known-good file
.\scripts\validate_pine_cvd.ps1 -FilePath "indicators/Production/Better CVD.pine"

# Should output:
# ✓ Pine version 6 >= 6
# ✓ TradingView/ta import found
# ✓ No fake CVD patterns
# ✓ Proper ta.requestVolumeDelta() usage
# ✅ ALL CHECKS PASSED
```

---

## Maintenance

### Add New CVD Keywords
Edit `validate_pine_cvd.ps1`:
```powershell
$CVD_KEYWORDS = @(
    'cvd',
    'delta',
    'your_new_keyword'  # Add here
)
```

### Add New Fake CVD Patterns
```powershell
$FAKE_CVD_PATTERNS = @(
    'close\s*>\s*close\[1\]\s*\?\s*volume',
    'your_new_pattern'  # Add here
)
```

### Update Pine Version Requirement
If Pine v7+ is released with breaking CVD changes:
```powershell
if ($version -lt 7) {  # Change from 6 to 7
    # violation...
}
```

---

## Future Enhancements

### Planned
1. **VSA Validation**: Ensure VSA uses z-score method consistently
2. **Divergence Validation**: Check pivot lookback ranges
3. **Volume Profile Validation**: Verify HVN/LVN thresholds
4. **Performance Checks**: Warn on excessive max_bars_back

### Stretch Goals
1. Python-based AST parser for deeper analysis
2. TradingView API integration for live testing
3. Auto-fix suggestions with diff preview

---

## Support

### Common Issues

**Q: Validation blocks commit but I don't see violations**
A: Run manually to see details:
```powershell
.\scripts\validate_pine_cvd.ps1 -Mode strict
```

**Q: How to bypass validation temporarily?**
A: Use `git commit --no-verify` (NOT RECOMMENDED!)

**Q: Validation too slow?**
A: Reduce file count or use `-FilePath` for specific files

**Q: False positive on keyword?**
A: Edit `$CVD_KEYWORDS` to refine regex patterns

---

## Credits

- **Created:** 2025-10-03
- **Author:** AI Assistant
- **Trigger:** PI34_Ultimate_AIO v5→v6 critical bug fix
- **Purpose:** Prevent future CVD calculation bugs
- **Enforcement:** VSCode Tasks + Git Pre-commit Hook

---

**Remember:** This isn't about bureaucracy - it's about **ACCURACY**. 
Fake CVD = Wrong signals = Lost money. Period. 🔥
