# Pine Script v6 - Lookahead Bias

## Overview

Lookahead bias is a subtle and dangerous error in backtesting where the strategy uses information that would not have been available at that point in time. It "looks ahead" into the future, leading to unrealistically good performance that is impossible to replicate in live trading.

While related to repainting, lookahead bias is specifically about future data leakage into the decision-making process.

## Primary Cause: Incorrect `request.security()` Usage

The most common source of lookahead bias in Pine Script is the `request.security()` function when the `lookahead` parameter is not set correctly.

- **`lookahead=barmerge.lookahead_on` (or omitting the parameter)**: This is the **DANGEROUS** setting. When you request daily data from an intraday chart (e.g., 1H), this setting will fill all the 1H bars of that day with the final, *closing* value of the daily bar. This means at 10:00 AM, your strategy already knows what the closing price of the day will be. This is looking into the future.

- **`lookahead=barmerge.lookahead_off`**: This is the **CORRECT** setting for backtesting. It ensures that data from a higher timeframe is only made available to your script *after* the higher timeframe bar has closed.

### Example of the Error

**❌ WRONG - Lookahead Bias:**
```pine
//@version=6
indicator("Lookahead Bias Example", overlay=true)

// Requesting daily close data without lookahead protection
float dailyClose = request.security(syminfo.tickerid, "D", close)

// On a 1H chart, this plots today's final closing price on all of today's 1H bars.
plot(dailyClose, "Daily Close with Lookahead")

// A strategy using this would be trading with future knowledge.
if close > dailyClose
    // This condition is flawed because `dailyClose` is future data.
    label.new(bar_index, high, "Above Daily Close?", color=color.red)
```

**✅ CORRECT - No Lookahead Bias:**
```pine
//@version=6
indicator("Correct MTF Example", overlay=true)

// Requesting daily close data CORRECTLY
float dailyClose = request.security(syminfo.tickerid, "D", close, lookahead=barmerge.lookahead_off)

plot(dailyClose, "Correct Daily Close")
```

## Other, More Subtle Causes

### 1. Using Pivots Incorrectly

The `ta.pivot_high` and `ta.pivot_low` functions require a certain number of bars to the left and right to confirm a pivot.

- **`ta.pivot_high(source, leftbars, rightbars)`**

If `rightbars` is greater than 0, the function can only identify a pivot `rightbars` *after* it has occurred. Using this information on the pivot bar itself is a form of lookahead.

**❌ WRONG - Lookahead Bias:**
```pine
// rightbars = 5 means the function can only know this was a pivot 5 bars later.
// However, the value is returned on the pivot bar itself.
float pivot = ta.pivot_high(high, 5, 5)

// If we act on this pivot value on the bar it appears, we are acting on future info.
if not na(pivot)
    strategy.entry("Short", strategy.short) // This entry is based on future knowledge
```

**✅ CORRECT - No Lookahead Bias:**
To use pivots safely, you must offset your signal.

```pine
float pivot = ta.pivot_high(high, 5, 5)

// The signal is `pivot[5]`. This checks if a pivot was confirmed 5 bars ago.
// This is now historical, confirmed information.
bool pivotWasConfirmed = not na(pivot[5])

if (pivotWasConfirmed and barstate.isconfirmed)
    strategy.entry("Short", strategy.short)
```

### 2. Inappropriate Use of `barstate` Variables

While less common, misusing `barstate` variables can lead to issues. For example, making a decision based on `barstate.islast` and assuming that logic would apply to historical bars is a form of lookahead (as only one bar is ever the last bar).

## How to Detect and Prevent Lookahead Bias

1.  **Always Use `lookahead=barmerge.lookahead_off`**: Make this a mandatory rule for all `request.security()` calls in strategies.
2.  **Be Wary of Pivots**: When using pivot functions for signals, ensure you are using an offset `[rightbars]` to act on *confirmed* pivots from the past.
3.  **Question Unusually Good Results**: If your backtest performance seems too good to be true (e.g., extremely high Sharpe ratio, perfectly timed entries at tops/bottoms), scrutinize your code for potential lookahead bias. It is a very common reason for such results.
4.  **Visualize Your Data**: Plot the data you are using for signals. If you are using `request.security`, plot the result. If it looks like a step function that only changes at the start of a new higher-timeframe period, it's likely correct. If it paints a straight line across current, unclosed bars, it has lookahead bias.
