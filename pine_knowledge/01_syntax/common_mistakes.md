# Common Pine v6 Mistakes & Fixes

This document lists common mistakes when migrating from Pine Script v5 or learning v6, and how to fix them.

## Mistake 1: Using `study()` instead of `indicator()`

**Problem:** `study()` is deprecated in v6.

**❌ WRONG (v5):**
```pine
//@version=5
study("My Indicator", overlay=true)
```

**✅ CORRECT (v6):**
```pine
//@version=6
indicator("My Indicator", overlay=true)
```

---

## Mistake 2: Using `input()` instead of `input.*` functions

**Problem:** The generic `input()` function is replaced by typed functions like `input.int()`, `input.float()`, etc.

**❌ WRONG (v5):**
```pine
length = input(14, "Length")
source = input(close, "Source")
```

**✅ CORRECT (v6):**
```pine
length = input.int(14, "Length", minval=1)
source = input.source(close, "Source")
```

---

## Mistake 3: Using `security()` instead of `request.security()`

**Problem:** The `security()` function has been moved to the `request` namespace and has a different signature (especially regarding repainting).

**❌ WRONG (v5):**
```pine
dailyClose = security(syminfo.tickerid, "D", close)
```

**✅ CORRECT (v6):**
```pine
// Use lookahead=barmerge.lookahead_off to prevent repainting
dailyClose = request.security(syminfo.tickerid, "D", close, lookahead=barmerge.lookahead_off)
```

---

## Mistake 4: Calling built-in functions without a namespace (`ta`, `math`, `str`)

**Problem:** Most built-in technical analysis, math, and string functions now reside within namespaces.

**❌ WRONG (v5):**
```pine
rsiValue = rsi(close, 14)
smaValue = sma(close, 50)
```

**✅ CORRECT (v6):**
```pine
rsiValue = ta.rsi(close, 14)
smaValue = ta.sma(close, 50)
```

---

## Mistake 5: Creating Repainting Strategy Signals

**Problem:** Using real-time, unconfirmed data (`close`, `high`, etc.) for strategy conditions leads to unrealistic backtest results.

**❌ WRONG (Repaints):**
```pine
longCondition = ta.crossover(close, ta.sma(close, 20))
if longCondition
    strategy.entry("Long", strategy.long)
```

**✅ CORRECT (No Repainting):**
```pine
// Use historical operator [1] to get the value from the previously closed bar
longCondition = ta.crossover(close[1], ta.sma(close, 20)[1])

// And use barstate.isconfirmed to ensure the current bar is closed before executing
if longCondition and barstate.isconfirmed
    strategy.entry("Long", strategy.long)
```

---

## Mistake 6: Incorrect Variable Reassignment

**Problem:** Using `=` to change a variable's value inside a local block, or forgetting `var` for variables that need to persist across bars.

**❌ WRONG:**
```pine
// This will not compile or will reset on every bar
counter = 0
if close > open
    counter = counter + 1 // Error or incorrect logic
```

**✅ CORRECT:**
```pine
// Use `var` to declare a variable that persists its value across bars
var int counter = 0

if close > open
    counter := counter + 1 // Use `:=` to reassign the value
```

---

## Mistake 7: Incorrect Array Declaration

**Problem:** The syntax for creating new arrays has changed to use generics.

**❌ WRONG (v5):**
```pine
myArray = array.new_float(5, 0.0)
```

**✅ CORRECT (v6):**
```pine
myArray = array.new<float>(5, 0.0)
```
