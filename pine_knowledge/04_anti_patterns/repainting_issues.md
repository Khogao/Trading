# Repainting Issues in Pine Script v6

## What is Repainting?

Repainting occurs when historical indicator/strategy values change as new bars form. This makes backtests unrealistic because the signals shown in history never actually occurred at that price/time in real-time.

**Impact:** Strategies look profitable in backtest but fail in live trading.

## Common Causes

### 1. Using Real-time Values in Conditions

#### ❌ WRONG - Repaints
```pine
//@version=6
strategy("Repaint Example", overlay=true)

float ma = ta.sma(close, 20)

// Uses current bar close (changes until bar closes)
if ta.crossover(close, ma)
    strategy.entry("Long", strategy.long)
```

**Why it repaints:**
- `close` = real-time value, updates continuously during bar formation
- Backtest uses final closed value
- Real-time would trigger/untrigger multiple times per bar

#### ✅ CORRECT - No Repaint
```pine
//@version=6
strategy("No Repaint", overlay=true)

float ma = ta.sma(close, 20)

// Uses previous confirmed bar
if ta.crossover(close[1], ma[1]) and barstate.isconfirmed
    strategy.entry("Long", strategy.long)
```

**Why it works:**
- `close[1]` = previous bar's final close (confirmed)
- `barstate.isconfirmed` = only true when current bar closes
- Backtest matches real-time behavior

---

### 2. request.security() Without Lookahead Protection

#### ❌ WRONG - Repaints
```pine
//@version=6
indicator("MTF Repaint", overlay=true)

// No lookahead parameter - uses future data!
float dailyClose = request.security(syminfo.tickerid, "D", close)
plot(dailyClose)
```

**Why it repaints:**
- Without `lookahead` parameter, uses future data in backtest
- Shows daily close value before the daily bar actually closed

#### ✅ CORRECT - No Repaint
```pine
//@version=6
indicator("MTF No Repaint", overlay=true)

// Lookahead protection
float dailyClose = request.security(
    syminfo.tickerid, 
    "D", 
    close[1],  // Use previous confirmed bar
    lookahead=barmerge.lookahead_off
)
plot(dailyClose)
```

---

### 3. Calculations Depending on Current Bar

#### ❌ WRONG
```pine
//@version=6
strategy("Repaint Calc", overlay=true)

// Highest high includes current forming bar
float highest = ta.highest(high, 20)

if close > highest
    strategy.entry("Long", strategy.long)
```

**Problem:** `highest` changes as current bar's high updates

#### ✅ CORRECT
```pine
//@version=6
strategy("No Repaint Calc", overlay=true)

// Highest high of previous 20 bars (confirmed)
float highest = ta.highest(high[1], 20)

if close[1] > highest and barstate.isconfirmed
    strategy.entry("Long", strategy.long)
```

---

### 4. Alert Conditions on Unconfirmed Data

#### ❌ WRONG
```pine
//@version=6
indicator("Repaint Alert", overlay=true)

float rsi = ta.rsi(close, 14)

// Fires multiple times as RSI fluctuates during bar
alertcondition(ta.crossover(rsi, 70), "Overbought", "RSI > 70")
```

#### ✅ CORRECT
```pine
//@version=6
indicator("No Repaint Alert", overlay=true)

float rsi = ta.rsi(close, 14)

// Only fires once when bar confirms
bool crossedOver = ta.crossover(rsi[1], 70) and barstate.isconfirmed
alertcondition(crossedOver, "Overbought", "RSI > 70 confirmed")
```

---

## Anti-Repainting Checklist

### ✅ Use These Patterns

1. **Historical Reference for Conditions**
```pine
// Use [1] for confirmed values
if ta.crossover(close[1], ma[1])
if ta.rsi(close, 14)[1] > 70
```

2. **barstate.isconfirmed for Entries**
```pine
if condition and barstate.isconfirmed
    strategy.entry("Long", strategy.long)
```

3. **request.security with Protection**
```pine
htfValue = request.security(
    symbol,
    timeframe,
    expression[1],  // Use confirmed bar from HTF
    lookahead=barmerge.lookahead_off
)
```

4. **Confirmed Calculations**
```pine
// Calculate on previous confirmed bars
float highest = ta.highest(high[1], 20)
float lowest = ta.lowest(low[1], 20)
```

### ❌ Avoid These Patterns

1. **Real-time Values in Logic**
```pine
// ❌ DON'T
if close > ma
if ta.rsi(close, 14) > 70
```

2. **request.security Without Lookahead**
```pine
// ❌ DON'T
htfClose = request.security(symbol, "D", close)
```

3. **Unconfirmed Alerts**
```pine
// ❌ DON'T
alertcondition(condition, ...)  // Fires multiple times
```

---

## Testing for Repainting

### Method 1: Bar Replay
1. Open TradingView chart
2. Click "Bar Replay" (bottom toolbar)
3. Step through bars one by one
4. Check if signals appear consistently

**Red flag:** Signals appear/disappear as you replay

### Method 2: Compare Timeframes
1. Backtest strategy on 1H chart
2. Note entry/exit points
3. Switch to 15M chart (same date range)
4. Check if signals align

**Red flag:** Signals at different times/prices

### Method 3: Real-time vs Historical
1. Run strategy in real-time for 1 week
2. Record all entries/exits (screenshots)
3. After 1 week, scroll back in history
4. Compare: do historical signals match real-time?

**Red flag:** Historical signals different from what you saw live

---

## Common Misconceptions

### "Using close[1] makes me miss opportunities"

**Reality:** Yes, you enter/exit 1 bar later. But:
- Backtest is realistic
- Live trading matches backtest
- Slightly delayed entry > false backtest

### "My strategy doesn't repaint because it works in backtest"

**Reality:** Repainting strategies LOOK good in backtest (that's the problem)
- Must test in real-time to verify
- Or use anti-repaint patterns from the start

### "I'll just be careful and watch the chart"

**Reality:** Automated trading = impossible to monitor 24/7
- Alerts fire incorrectly
- Strategies enter at wrong times
- Can't scale

---

## Example: Complete Anti-Repaint Strategy

```pine
//@version=6
strategy(
    "Anti-Repaint EMA Cross",
    overlay=true,
    default_qty_type=strategy.percent_of_equity,
    default_qty_value=10
)

// ============================================================================
// INPUTS
// ============================================================================
int fastLength = input.int(10, "Fast EMA", minval=1, group="Indicators")
int slowLength = input.int(20, "Slow EMA", minval=1, group="Indicators")
bool useStopLoss = input.bool(true, "Use Stop Loss", group="Risk")
float stopPercent = input.float(2.0, "Stop Loss %", minval=0.1, group="Risk")

// ============================================================================
// CALCULATIONS - Using confirmed data
// ============================================================================
float fastEMA = ta.ema(close, fastLength)
float slowEMA = ta.ema(close, slowLength)

// ============================================================================
// CONDITIONS - Using previous confirmed bars
// ============================================================================
bool longCondition = ta.crossover(fastEMA[1], slowEMA[1]) and barstate.isconfirmed
bool shortCondition = ta.crossunder(fastEMA[1], slowEMA[1]) and barstate.isconfirmed

// ============================================================================
// STRATEGY EXECUTION
// ============================================================================
if longCondition
    strategy.entry("Long", strategy.long)
    if useStopLoss
        stopPrice = close[1] * (1 - stopPercent/100)
        strategy.exit("Long SL", "Long", stop=stopPrice)

if shortCondition
    strategy.close("Long", comment="EMA Cross Down")

// ============================================================================
// VISUALS
// ============================================================================
plot(fastEMA, "Fast EMA", color.blue, 2)
plot(slowEMA, "Slow EMA", color.red, 2)

// Mark entry points on confirmed bars only
plotshape(
    longCondition,
    "Long Entry",
    shape.triangleup,
    location.belowbar,
    color.green,
    size=size.small
)

// ============================================================================
// ALERTS - Only on confirmed conditions
// ============================================================================
alertcondition(longCondition, "Long Signal", "EMA bullish crossover confirmed")
alertcondition(shortCondition, "Exit Signal", "EMA bearish crossover confirmed")
```

**Key anti-repaint features:**
1. Uses `[1]` for all condition checks
2. `barstate.isconfirmed` ensures bar is closed
3. Stop loss based on `close[1]` (confirmed price)
4. Alerts only fire on confirmed conditions
5. Visual markers only on confirmed bars

---

## Summary

**Golden Rule:** If it's used in a condition for entry/exit/alert, use the confirmed value with `[1]` and check `barstate.isconfirmed`.

**The price of realism:** Slightly delayed signals
**The benefit:** Backtest = real-time performance

**Remember:** A strategy that makes 30% in backtest but repaints is worth $0. A strategy that makes 15% without repainting is tradeable.
