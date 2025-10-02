# request.security() - Multi-Timeframe Analysis

## Overview

`request.security()` fetches data from other symbols or timeframes. It is critical for MTF (Multi-Timeframe) strategies and analysis.

## Syntax

```pine
request.security(
    symbol,           // string: Symbol to fetch (e.g., "BINANCE:BTCUSDT")
    timeframe,        // string: Timeframe (e.g., "D", "240", "W")
    expression,       // series: What to fetch (close, ta.rsi(), custom calculation)
    gaps,            // barmerge_gaps: How to handle gaps
    lookahead,       // barmerge_lookahead: CRITICAL for anti-repaint
    ignore_invalid_symbol,  // bool: Continue if symbol invalid
    currency         // string: Currency conversion
)
```

## Parameters Explained

### symbol (string)
```pine
// Current chart symbol
request.security(syminfo.tickerid, "D", close)

// Specific symbol
request.security("BINANCE:BTCUSDT", "D", close)

// Different exchange
request.security("NASDAQ:AAPL", "W", close)
```

### timeframe (string)
```pine
"1"    // 1 minute
"5"    // 5 minutes
"15"   // 15 minutes
"60"   // 1 hour
"240"  // 4 hours
"D"    // Daily
"W"    // Weekly
"M"    // Monthly
```

### expression
Can be:
- Simple value: `close`, `high`, `low`, `open`, `volume`
- Calculation: `ta.rsi(close, 14)`
- Tuple: `[close, volume]`
- Custom function result

### gaps (barmerge_gaps)
```pine
barmerge.gaps_off  // Fill gaps with previous value (default)
barmerge.gaps_on   // Leave gaps (na values)
```

**Example:**
```pine
// Daily close on 1H chart
dailyClose_nogaps = request.security(syminfo.tickerid, "D", close, barmerge.gaps_off)
// Result: Daily close repeats for all 1H bars of that day

dailyClose_gaps = request.security(syminfo.tickerid, "D", close, barmerge.gaps_on)
// Result: Only has value on first 1H bar of new day, na otherwise
```

### lookahead (barmerge_lookahead) - CRITICAL

```pine
barmerge.lookahead_off  // No lookahead - realistic (USE THIS)
barmerge.lookahead_on   // Lookahead - unrealistic (AVOID)
```

**❌ WITH lookahead (WRONG):**
```pine
// On 1H chart, fetching daily data
dailyClose = request.security(syminfo.tickerid, "D", close, lookahead=barmerge.lookahead_on)
// Problem: On intraday bars, shows the daily close BEFORE the day actually closes
// = Looking into the future = Unrealistic backtest
```

**✅ WITHOUT lookahead (CORRECT):**
```pine
dailyClose = request.security(
    syminfo.tickerid, 
    "D", 
    close, 
    lookahead=barmerge.lookahead_off
)
// Only shows daily close after the daily bar confirms
// = Realistic backtest
```

---

## Common Patterns

### Pattern 1: Higher Timeframe Indicator

```pine
//@version=6
indicator("HTF RSI", overlay=false)

// Inputs
int rsiLength = input.int(14, "RSI Length")
string htf = input.timeframe("D", "Higher Timeframe")

// Current timeframe RSI
float currentRSI = ta.rsi(close, rsiLength)

// Higher timeframe RSI - NO REPAINT
float htfRSI = request.security(
    syminfo.tickerid,
    htf,
    ta.rsi(close, rsiLength),
    lookahead=barmerge.lookahead_off
)

// Plots
plot(currentRSI, "Current TF RSI", color.blue, 2)
plot(htfRSI, "HTF RSI", color.red, 2)
hline(70, "OB", color.red)
hline(30, "OS", color.green)
```

---

### Pattern 2: Multiple HTF Indicators

```pine
//@version=6
indicator("Multi-TF Trend", overlay=true)

// Inputs
int maLength = input.int(50, "MA Length")

// Current timeframe
float ma_current = ta.ema(close, maLength)

// Higher timeframes
float ma_1h = request.security(syminfo.tickerid, "60", ta.ema(close, maLength), lookahead=barmerge.lookahead_off)
float ma_4h = request.security(syminfo.tickerid, "240", ta.ema(close, maLength), lookahead=barmerge.lookahead_off)
float ma_daily = request.security(syminfo.tickerid, "D", ta.ema(close, maLength), lookahead=barmerge.lookahead_off)

// Plot
plot(ma_current, "Current", color.blue, 1)
plot(ma_1h, "1H", color.orange, 2)
plot(ma_4h, "4H", color.red, 2)
plot(ma_daily, "Daily", color.purple, 3)
```

---

### Pattern 3: HTF Trend Filter for Strategy

```pine
//@version=6
strategy("HTF Trend Filter", overlay=true)

// Inputs
int fastLen = input.int(10, "Fast EMA")
int slowLen = input.int(20, "Slow EMA")
int trendLen = input.int(50, "Trend MA")

// Current TF signals
float fastEMA = ta.ema(close, fastLen)
float slowEMA = ta.ema(close, slowLen)

// Daily trend filter - NO REPAINT
float dailyTrendMA = request.security(
    syminfo.tickerid,
    "D",
    ta.ema(close, trendLen),
    lookahead=barmerge.lookahead_off
)

float dailyClose = request.security(
    syminfo.tickerid,
    "D",
    close,
    lookahead=barmerge.lookahead_off
)

// Trend determination
bool dailyUptrend = dailyClose > dailyTrendMA
bool dailyDowntrend = dailyClose < dailyTrendMA

// Entry conditions with trend filter
bool longSignal = ta.crossover(fastEMA[1], slowEMA[1]) and dailyUptrend and barstate.isconfirmed
bool shortSignal = ta.crossunder(fastEMA[1], slowEMA[1]) and dailyDowntrend and barstate.isconfirmed

// Execution
if longSignal
    strategy.entry("Long", strategy.long)

if shortSignal
    strategy.close("Long")

// Visuals
plot(fastEMA, "Fast", color.blue)
plot(slowEMA, "Slow", color.red)
bgcolor(dailyUptrend ? color.new(color.green, 90) : color.new(color.red, 90))
```

---

### Pattern 4: Fetching Multiple Values (Tuple)

```pine
//@version=6
indicator("HTF OHLC", overlay=true)

string htf = input.timeframe("D", "HTF")

// Fetch multiple values at once
[htfOpen, htfHigh, htfLow, htfClose] = request.security(
    syminfo.tickerid,
    htf,
    [open, high, low, close],
    lookahead=barmerge.lookahead_off
)

// Plot HTF candle levels
plot(htfOpen, "HTF Open", color.blue, 2, plot.style_cross)
plot(htfHigh, "HTF High", color.green, 1)
plot(htfLow, "HTF Low", color.red, 1)
plot(htfClose, "HTF Close", color.orange, 2)
```

---

### Pattern 5: Custom Function in HTF

```pine
//@version=6
indicator("HTF Custom Calc", overlay=true)

// Custom calculation
calcBollinger() =>
    float basis = ta.sma(close, 20)
    float dev = ta.stdev(close, 20)
    float upper = basis + 2 * dev
    float lower = basis - 2 * dev
    [basis, upper, lower]

// Fetch from daily timeframe
[dailyBasis, dailyUpper, dailyLower] = request.security(
    syminfo.tickerid,
    "D",
    calcBollinger(),
    lookahead=barmerge.lookahead_off
)

// Plot
plot(dailyBasis, "Daily Basis", color.blue, 2)
plot(dailyUpper, "Daily Upper", color.green, 2)
plot(dailyLower, "Daily Lower", color.red, 2)
```

---

## Anti-Repaint Best Practices

### ✅ DO THIS

**1. Always use lookahead=barmerge.lookahead_off**
```pine
htfValue = request.security(
    symbol,
    tf,
    expression,
    lookahead=barmerge.lookahead_off  // CRITICAL
)
```

**2. For strategies, use confirmed HTF bars**
```pine
// Fetch previous confirmed HTF bar
htfClose = request.security(
    syminfo.tickerid,
    "D",
    close[1],  // Previous confirmed daily close
    lookahead=barmerge.lookahead_off
)
```

**3. Combine with barstate.isconfirmed**
```pine
bool htfCrossover = request.security(
    syminfo.tickerid,
    "D",
    ta.crossover(close[1], ma[1]),
    lookahead=barmerge.lookahead_off
)

if htfCrossover and barstate.isconfirmed
    strategy.entry("Long", strategy.long)
```

### ❌ DON'T DO THIS

**1. Using lookahead_on**
```pine
// ❌ WRONG - looks into future
htfValue = request.security(symbol, tf, close, lookahead=barmerge.lookahead_on)
```

**2. Omitting lookahead parameter**
```pine
// ❌ WRONG - defaults can vary
htfValue = request.security(symbol, tf, close)
```

**3. Using real-time HTF values in strategy**
```pine
// ❌ WRONG - uses forming HTF bar
htfClose = request.security(syminfo.tickerid, "D", close)
if close > htfClose
    strategy.entry("Long", strategy.long)
```

---

## Common Errors & Solutions

### Error 1: "Cannot call request.security with 'expression' of series type"

**Problem:** Trying to pass series value where simple expected

**Solution:** Wrap in function or use different approach
```pine
// ❌ WRONG
htfValue = request.security(syminfo.tickerid, "D", close[1])

// ✅ CORRECT
htfValue = request.security(syminfo.tickerid, "D", close)[1]
// Or
getClose() => close
htfValue = request.security(syminfo.tickerid, "D", getClose())
```

---

### Error 2: "Timeframe must be explicitly provided"

**Problem:** Trying to use variable timeframe without proper setup

**Solution:** Use input.timeframe()
```pine
// ❌ WRONG
string tf = "D"
htfValue = request.security(syminfo.tickerid, tf, close)

// ✅ CORRECT
string tf = input.timeframe("D", "Timeframe")
htfValue = request.security(syminfo.tickerid, tf, close, lookahead=barmerge.lookahead_off)
```

---

### Error 3: Getting 'na' values unexpectedly

**Problem:** Using gaps_on when you want continuous values

**Solution:** Use gaps_off
```pine
// ❌ Getting na values
htfValue = request.security(
    syminfo.tickerid,
    "D",
    close,
    gaps=barmerge.gaps_on,
    lookahead=barmerge.lookahead_off
)

// ✅ Continuous values
htfValue = request.security(
    syminfo.tickerid,
    "D",
    close,
    gaps=barmerge.gaps_off,  // Fill gaps
    lookahead=barmerge.lookahead_off
)
```

---

## Performance Considerations

### Limit request.security() Calls

Each call adds computation overhead.

**❌ INEFFICIENT:**
```pine
// Multiple calls for same symbol/timeframe
htfClose = request.security(syminfo.tickerid, "D", close, lookahead=barmerge.lookahead_off)
htfOpen = request.security(syminfo.tickerid, "D", open, lookahead=barmerge.lookahead_off)
htfHigh = request.security(syminfo.tickerid, "D", high, lookahead=barmerge.lookahead_off)
htfLow = request.security(syminfo.tickerid, "D", low, lookahead=barmerge.lookahead_off)
```

**✅ EFFICIENT:**
```pine
// Single call fetching tuple
[htfOpen, htfHigh, htfLow, htfClose] = request.security(
    syminfo.tickerid,
    "D",
    [open, high, low, close],
    lookahead=barmerge.lookahead_off
)
```

---

## Testing HTF Strategies

### Method 1: Timeframe Consistency Check

Test strategy on multiple timeframes:
```
1. Backtest on 15M chart
2. Note entry at 2024-01-15 10:30
3. Switch to 5M chart
4. Check if entry still at same time
```

If entries shift = possible repaint issue

### Method 2: Bar Replay

1. Use Bar Replay feature
2. Step through bars watching HTF signals
3. Signals should NOT disappear/change as you progress

### Method 3: Real-time Verification

1. Run strategy in real-time for 1 week
2. Screenshot every entry/exit
3. After 1 week, compare with historical signals
4. They should match exactly

---

## Complete Example: MTF Momentum Strategy

```pine
//@version=6
strategy(
    "MTF Momentum Strategy",
    overlay=true,
    default_qty_type=strategy.percent_of_equity,
    default_qty_value=10
)

// ============================================================================
// INPUTS
// ============================================================================
int rsiLength = input.int(14, "RSI Length", minval=1, group="Indicators")
int maLength = input.int(50, "MA Length", minval=1, group="Indicators")
string htf = input.timeframe("D", "Higher Timeframe", group="MTF")

float rsiOB = input.float(70, "RSI Overbought", group="Levels")
float rsiOS = input.float(30, "RSI Oversold", group="Levels")

bool useStopLoss = input.bool(true, "Use Stop Loss", group="Risk")
float stopPercent = input.float(2.0, "Stop Loss %", minval=0.1, group="Risk")

// ============================================================================
// CURRENT TIMEFRAME CALCULATIONS
// ============================================================================
float rsi = ta.rsi(close, rsiLength)
float ma = ta.ema(close, maLength)

// ============================================================================
// HIGHER TIMEFRAME DATA - NO REPAINT
// ============================================================================
// Fetch HTF trend
float htfMA = request.security(
    syminfo.tickerid,
    htf,
    ta.ema(close, maLength),
    lookahead=barmerge.lookahead_off
)

float htfClose = request.security(
    syminfo.tickerid,
    htf,
    close,
    lookahead=barmerge.lookahead_off
)

// Determine HTF trend
bool htfUptrend = htfClose > htfMA
bool htfDowntrend = htfClose < htfMA

// ============================================================================
// ENTRY CONDITIONS - Using confirmed bars
// ============================================================================
// Long: RSI oversold bounce + HTF uptrend
bool longSetup = rsi[1] < rsiOS and rsi > rsiOS and htfUptrend
bool longEntry = longSetup and close[1] > ma[1] and barstate.isconfirmed

// Exit: RSI overbought or HTF trend reversal
bool longExit = (rsi[1] > rsiOB or not htfUptrend) and barstate.isconfirmed

// ============================================================================
// STRATEGY EXECUTION
// ============================================================================
if longEntry
    strategy.entry("Long", strategy.long)
    
    if useStopLoss
        float stopPrice = close[1] * (1 - stopPercent/100)
        strategy.exit("Long Exit", "Long", stop=stopPrice)

if longExit
    strategy.close("Long", comment="Exit Signal")

// ============================================================================
// VISUALS
// ============================================================================
// Plot MAs
plot(ma, "MA", color.blue, 2)
plot(htfMA, "HTF MA", color.purple, 3, plot.style_stepline)

// Background color for HTF trend
bgcolor(htfUptrend ? color.new(color.green, 95) : color.new(color.red, 95), title="HTF Trend BG")

// Entry markers
plotshape(
    longEntry,
    "Long Entry",
    shape.triangleup,
    location.belowbar,
    color.green,
    size=size.small,
    text="LONG"
)

plotshape(
    longExit,
    "Long Exit",
    shape.triangledown,
    location.abovebar,
    color.red,
    size=size.small,
    text="EXIT"
)

// ============================================================================
// RSI PANEL (separate indicator overlay)
// ============================================================================
// Note: In real usage, this would be a separate indicator
// Shown here for completeness
```

---

## Key Takeaways

1. **ALWAYS use `lookahead=barmerge.lookahead_off`**
2. **Combine HTF data with `barstate.isconfirmed` for strategy entries**
3. **Use `[1]` historical reference for confirmed HTF bars in strategies**
4. **Fetch multiple values in single call (tuple) for efficiency**
5. **Test thoroughly using bar replay and timeframe consistency checks**
6. **Remember: HTF bar isn't "confirmed" until that timeframe's bar closes**

**Golden Rule:** If backtest looks too good with HTF data, it's probably repainting. Verify with real-time testing.
