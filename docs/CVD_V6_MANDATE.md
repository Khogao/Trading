# CVD MANDATE: Pine Script v6 Required for Accurate CVD

**Date**: October 2, 2025  
**Author**: Khogao  
**Status**: MANDATED WORKSPACE RULE

---

## 🚨 CRITICAL REQUIREMENT

**ALL indicators/strategies using CVD (Cumulative Volume Delta) MUST use Pine Script v6 with `ta.requestVolumeDelta()` from TradingView/ta/8 library.**

### Why v6 is MANDATORY:

1. **Accuracy**: `ta.requestVolumeDelta()` is the OFFICIAL CVD function from TradingView
2. **Performance**: Native implementation is 10x faster than custom calculations
3. **Reliability**: Proper session reset handling, no data gaps
4. **Maintenance**: Future-proof against TradingView API changes

---

## 📋 Workspace CVD Files Audit

### ✅ COMPLIANT (v6 with ta.requestVolumeDelta)

| File | Status | Version | Notes |
|------|--------|---------|-------|
| `CVPZero.pine` | ✅ PROD | v6 | Uses `tav5.requestVolumeDelta()` |
| `CVD-Pro.pine` | ✅ PROD | v6 | Uses `ta.requestVolumeDelta()` |
| `CVD+VSA Pro.pine` | ✅ PROD | v6 | Clean implementation |
| `Pi34 Pro.pine` | 🔄 IN PROGRESS | v6 | Converting from v5, var init issues |

### ❌ NON-COMPLIANT (v5 or custom CVD)

| File | Status | Action Required |
|------|--------|----------------|
| `VP_CVD_Strategy_v1.pine` | ❌ v5 | Upgrade to v6 + import TradingView/ta/8 |
| Any new CVD indicators | ❌ N/A | MUST start with v6 template |

---

## 🔧 V6 CVD Template (STANDARD)

```pine
//@version=6
indicator("Your Indicator Name", "SHORT", overlay=false)
import TradingView/ta/8 as tav6

// === CVD ENGINE ===
const string GRP_CVD = "CVD Settings"
cvd_anchor = input.timeframe("D", "CVD Reset Anchor", group=GRP_CVD)

// Lower timeframe resolver
f_lowerTf() =>
    if timeframe.isseconds
        "1S"
    else if timeframe.isintraday
        "1"
    else if timeframe.isdaily
        "5"
    else
        "60"

// CVD calculation
f_cvd_close() =>
    [_o, _h, _l, _c] = tav6.requestVolumeDelta(f_lowerTf(), cvd_anchor)
    _c

[cvd_o, cvd_h, cvd_l, cvd_c] = tav6.requestVolumeDelta(f_lowerTf(), cvd_anchor)
cvd_source = f_cvd_close()

// Session reset tracking (CRITICAL for divergence accuracy!)
var int last_cvd_reset_bar = 0
cvd_new_session = ta.change(time(cvd_anchor)) != 0
if cvd_new_session
    last_cvd_reset_bar := bar_index

// Your CVD logic here...
```

---

## 🚫 BANNED PATTERNS

### ❌ DON'T: Custom CVD calculation
```pine
// OLD WAY (v5) - KHÔNG DÙNG NỮA!
cvd = 0.0
cvd := nz(cvd[1]) + (close > close[1] ? volume : -volume)
```

### ❌ DON'T: request.security for volume delta
```pine
// WRONG - request.security không có volumeDelta field!
cvd = request.security(syminfo.tickerid, "1", volumeDelta)
```

### ❌ DON'T: Pine v5 for new CVD indicators
```pine
//@version=5  // ❌ BANNED for CVD indicators!
```

---

## 📊 V5 → V6 Migration Checklist

### Breaking Changes to Fix:

1. **var initialization**
   - ❌ `var float x = na`
   - ✅ `var float x = 0.0`
   - ❌ `var line ln = na`
   - ✅ `var line ln = line(na)`
   - ❌ `var table tbl = na`
   - ✅ `var table tbl = table(na)`

2. **alertcondition() messages**
   - ❌ `alertcondition(cond, "Title", "Msg: " + dynamic_var)`
   - ✅ Use `alert()` function instead:
     ```pine
     if barstate.isconfirmed and cond
         alert("Msg: " + dynamic_var, alert.freq_once_per_bar_close)
     ```

3. **import library**
   - ✅ Add at top after `indicator()`:
     ```pine
     import TradingView/ta/8 as tav6
     ```

4. **Replace old CVD logic**
   - Delete custom CVD calculations
   - Use `tav6.requestVolumeDelta()` template above

---

## 🎯 CVD Best Practices

### 1. Session Reset Tracking (MANDATORY)
Always track CVD reset boundaries to avoid false divergence:
```pine
var int last_cvd_reset_bar = 0
if ta.change(time(cvd_anchor)) != 0
    last_cvd_reset_bar := bar_index

// Validate pivots in same cycle
cvd_same_cycle = (pivot_bar - last_cvd_reset_bar) >= 0
```

### 2. Divergence Detection
Only compare pivots within same CVD cycle:
```pine
cvd_bull_div = cvd_same_cycle and price_lower_low and cvd_higher_low
```

### 3. Lower Timeframe Selection
Use adaptive lower TF based on chart TF:
- Seconds chart → "1S"
- Intraday (1-60m) → "1" (1 minute)
- Daily → "5" (5 minutes)
- Weekly+ → "60" (1 hour)

### 4. Multi-Timeframe CVD
Use `request.security()` with `f_cvd_close()`:
```pine
cvd_15m = request.security(syminfo.tickerid, "15", f_cvd_close())
cvd_1h = request.security(syminfo.tickerid, "60", f_cvd_close())
```

---

## 🔍 Code Review Checklist

Before merging any CVD-related code:

- [ ] Pine v6 (`//@version=6`)
- [ ] Import `TradingView/ta/8`
- [ ] Use `tav6.requestVolumeDelta()` (not custom calc)
- [ ] Session reset tracking implemented
- [ ] Same-cycle validation for divergence
- [ ] All `var` initialized properly (no `na`)
- [ ] No `alertcondition()` with dynamic strings
- [ ] Lower TF resolver function included
- [ ] Multi-TF CVD uses `request.security()` correctly

---

## 📝 Git Commit Message Template

When upgrading CVD indicators to v6:

```
feat(cvd): Upgrade [IndicatorName] to Pine v6 for accurate CVD

- MANDATED: Use ta.requestVolumeDelta() from TradingView/ta/8
- Fix: var initialization (float=0.0, line=line(na))
- Fix: alertcondition → alert() for dynamic messages
- Add: Session reset tracking for divergence accuracy
- Perf: 10x faster CVD calculation vs custom implementation

Breaking: Requires Pine v6, not backward compatible with v5

Refs: CVD_V6_MANDATE.md
```

---

## 🚀 Future Work

1. Migrate `VP_CVD_Strategy_v1.pine` to v6
2. Create v6 CVD library module for reuse
3. Add CVD Z-Score normalization (% change from session open)
4. Test cumulative CVD (no reset) vs session-reset CVD

---

## 📚 References

- [TradingView Pine v6 Migration Guide](https://www.tradingview.com/pine-script-docs/migration-guides/v5_to_v6/)
- [ta.requestVolumeDelta() Docs](https://www.tradingview.com/pine-script-reference/v6/#fun_ta.requestVolumeDelta)
- CVD Reset Issue Analysis: `d:\Work\Coding\CLAUDE.md` (Phase 3 pending)

---

**REMEMBER: CVD without ta.requestVolumeDelta() = INACCURATE DATA = WRONG SIGNALS = LOSSES!**
