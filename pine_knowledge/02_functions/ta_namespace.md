# Pine Script v6 `ta` Namespace

This document provides a reference for common functions within the `ta` (Technical Analysis) namespace.

## Overview

The `ta` namespace contains most of the built-in indicators and technical analysis utilities in Pine Script. To use them, you must prefix the function call with `ta.`.

```pine
// Correct usage
float myRSI = ta.rsi(close, 14)

// Incorrect usage (will cause an error)
float myRSI = rsi(close, 14) 
```

---

## Common `ta` Functions

### Moving Averages

- **`ta.sma(source, length)`**: Simple Moving Average.
- **`ta.ema(source, length)`**: Exponential Moving Average.
- **`ta.wma(source, length)`**: Weighted Moving Average.
- **`ta.rma(source, length)`**: Relative Moving Average (similar to TradingView's RSI internal MA).
- **`ta.vwma(source, length)`**: Volume-Weighted Moving Average.

**Example:**
```pine
float simpleMA = ta.sma(close, 50)
float exponentialMA = ta.ema(close, 50)
plot(simpleMA, "SMA50", color.blue)
plot(exponentialMA, "EMA50", color.orange)
```

### Oscillators

- **`ta.rsi(source, length)`**: Relative Strength Index.
- **`ta.stoch(source, high, low, length)`**: Stochastic Oscillator. Returns the K value.
- **`ta.macd(source, fastlen, slowlen, siglen)`**: Moving Average Convergence Divergence. Returns a tuple: `[macdLine, signalLine, histLine]`.
- **`ta.cci(source, length)`**: Commodity Channel Index.

**Example:**
```pine
// RSI
float rsiValue = ta.rsi(close, 14)
plot(rsiValue, "RSI", color.purple)

// MACD
[macdLine, signalLine, histLine] = ta.macd(close, 12, 26, 9)
plot(macdLine, "MACD", color.blue)
plot(signalLine, "Signal", color.orange)
plot(histLine, "Histogram", color.gray, 2, plot.style_histogram)
```

### Volatility & Range

- **`ta.atr(length)`**: Average True Range.
- **`ta.bb(source, length, mult)`**: Bollinger Bands. Returns a tuple: `[basis, upper, lower]`.
- **`ta.kc(source, length, mult, useTrueRange)`**: Keltner Channels. Returns a tuple: `[basis, upper, lower]`.
- **`ta.tr(handleFillGaps)`**: True Range.

**Example:**
```pine
// Bollinger Bands
[bbBasis, bbUpper, bbLower] = ta.bb(close, 20, 2)
plot(bbBasis, "BB Basis", color.blue)
plot(bbUpper, "BB Upper", color.red)
plot(bbLower, "BB Lower", color.green)

// ATR
float atrValue = ta.atr(14)
plot(atrValue, "ATR", color.gray, 1, plot.style_area)
```

### Crossovers & Crossunders

- **`ta.crossover(series1, series2)`**: Returns `true` on the bar where `series1` crosses above `series2`.
- **`ta.crossunder(series1, series2)`**: Returns `true` on the bar where `series1` crosses below `series2`.

**Example (non-repainting):**
```pine
float fastMA = ta.ema(close, 12)
float slowMA = ta.ema(close, 26)

bool bullishCross = ta.crossover(fastMA[1], slowMA[1])
bool bearishCross = ta.crossunder(fastMA[1], slowMA[1])

plotshape(bullishCross, "Bullish Cross", shape.triangleup, location.belowbar, color.green)
plotshape(bearishCross, "Bearish Cross", shape.triangledown, location.abovebar, color.red)
```

### Highs & Lows

- **`ta.highest(source, length)`**: Highest value of `source` over the last `length` bars.
- **`ta.lowest(source, length)`**: Lowest value of `source` over the last `length` bars.
- **`ta.pivot_high(source, leftbars, rightbars)`**: Pivot High. Returns the price of the pivot, or `na`.
- **`ta.pivot_low(source, leftbars, rightbars)`**: Pivot Low. Returns the price of the pivot, or `na`.

**Example:**
```pine
// Donchian Channels
float upperChannel = ta.highest(high, 20)[1]
float lowerChannel = ta.lowest(low, 20)[1]

plot(upperChannel, "Upper Channel", color.red)
plot(lowerChannel, "Lower Channel", color.green)
```

### Other Utilities

- **`ta.barssince(condition)`**: Number of bars since `condition` was last `true`.
- **`ta.valuewhen(condition, source, occurrence)`**: Value of `source` when `condition` was `true` for the `occurrence`-th time.
- **`ta.change(source, length)`**: Difference between the current `source` value and its value `length` bars ago.

**Example:**
```pine
// How many bars since the last bullish cross?
int barsSinceCross = ta.barssince(ta.crossover(ta.ema(close,12), ta.ema(close,26)))

// Get the price of the last pivot high
float lastPivotHigh = ta.valuewhen(ta.pivot_high(high, 5, 5), high, 0)
```
