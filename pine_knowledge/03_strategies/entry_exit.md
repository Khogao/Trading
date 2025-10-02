# Strategy Entry & Exit Patterns

## Strategy Declaration

```pine
//@version=6
strategy(
    title,                          // string: Strategy name
    shorttitle,                     // string: Short name for chart
    overlay,                        // bool: true = on chart, false = separate
    format,                         // string: "price" or "volume"
    precision,                      // int: Decimal places
    scale,                          // scale: price scale behavior
    pyramiding,                     // int: Max pyramid orders (default: 0)
    calc_on_order_fills,           // bool: Recalc on fills vs bars
    calc_on_every_tick,            // bool: Recalc every tick in real-time
    max_bars_back,                 // int: Historical bars limit
    backtest_fill_limits_assumption, // int: Limit order fill logic
    default_qty_type,              // strategy.qty_type: Position sizing method
    default_qty_value,             // float: Position size value
    initial_capital,               // float: Starting capital
    currency,                      // string: Account currency
    slippage,                      // int: Slippage in ticks
    commission_type,               // strategy.commission: Commission type
    commission_value,              // float: Commission amount
    process_orders_on_close,       // bool: Process orders on bar close
    close_entries_rule,            // string: Close entries behavior
    margin_long,                   // float: Long margin %
    margin_short                   // float: Short margin %
)
```

### Common Configuration

```pine
//@version=6
strategy(
    "My Strategy",
    overlay=true,
    pyramiding=0,                                      // No pyramiding
    default_qty_type=strategy.percent_of_equity,      // Size by % of equity
    default_qty_value=10,                             // 10% per trade
    initial_capital=10000,                            // Start with $10k
    currency=currency.USD,
    slippage=2,                                       // 2 ticks slippage
    commission_type=strategy.commission.percent,
    commission_value=0.1,                             // 0.1% commission
    process_orders_on_close=true                      // More realistic
)
```

---

## Entry Functions

### strategy.entry()

Opens position or adds to existing position.

```pine
strategy.entry(
    id,              // string: Unique order ID
    direction,       // strategy.direction: long or short
    qty,            // float: Order quantity (optional)
    limit,          // float: Limit price (optional)
    stop,           // float: Stop price (optional)
    oca_name,       // string: OCA group name (optional)
    oca_type,       // strategy.oca_type: OCA behavior (optional)
    comment,        // string: Order comment (optional)
    when,           // bool: Condition to execute (optional)
    alert_message   // string: Alert text (optional)
)
```

### Basic Entry

```pine
//@version=6
strategy("Basic Entry", overlay=true)

int maLength = input.int(20, "MA Length")
float ma = ta.sma(close, maLength)

// Long entry when price crosses above MA
bool longCondition = ta.crossover(close[1], ma[1]) and barstate.isconfirmed

if longCondition
    strategy.entry("Long", strategy.long)

plot(ma, "MA", color.blue, 2)
```

---

### Entry with Quantity

```pine
// Fixed quantity
if longCondition
    strategy.entry("Long", strategy.long, qty=10)

// Dynamic quantity based on capital
float riskAmount = strategy.equity * 0.02  // Risk 2% of equity
float stopDistance = close - low[1]
float qty = riskAmount / stopDistance

if longCondition
    strategy.entry("Long", strategy.long, qty=qty)
```

---

### Limit Orders

```pine
// Enter long at limit price below current price
float limitPrice = close * 0.98  // 2% below current price

if longCondition
    strategy.entry("Long", strategy.long, limit=limitPrice)
```

---

### Stop Orders

```pine
// Enter long if price breaks above resistance
float breakoutLevel = ta.highest(high, 20)[1]

if close > breakoutLevel
    strategy.entry("Long", strategy.long, stop=breakoutLevel)
```

---

### Pyramiding

```pine
//@version=6
strategy(
    "Pyramiding Example",
    overlay=true,
    pyramiding=3  // Allow up to 3 entries
)

float ma = ta.sma(close, 20)
bool uptrend = close > ma

// First entry
if ta.crossover(close, ma) and barstate.isconfirmed
    strategy.entry("Long1", strategy.long, qty=1)

// Additional entries if trend continues
if uptrend and strategy.position_size > 0
    // Add if price makes new high
    if high > ta.highest(high[1], 5)
        strategy.entry("Long2", strategy.long, qty=1)
```

---

## Exit Functions

### strategy.close()

Close specific position by ID.

```pine
strategy.close(
    id,             // string: Entry ID to close
    when,           // bool: Condition (optional)
    comment,        // string: Exit comment (optional)
    qty,            // float: Partial close quantity (optional)
    qty_percent,    // float: Close % of position (optional)
    alert_message   // string: Alert text (optional)
)
```

### Basic Close

```pine
//@version=6
strategy("Basic Close", overlay=true)

float ma = ta.sma(close, 20)

// Entry
if ta.crossover(close[1], ma[1]) and barstate.isconfirmed
    strategy.entry("Long", strategy.long)

// Exit when price crosses below MA
if ta.crossunder(close[1], ma[1]) and barstate.isconfirmed
    strategy.close("Long", comment="MA Cross Exit")
```

---

### Partial Close

```pine
// Close 50% of position
if takeProfit Condition
    strategy.close("Long", qty_percent=50, comment="Partial TP")

// Close specific quantity
if takeProfit2
    strategy.close("Long", qty=5, comment="Take 5 contracts")
```

---

### strategy.close_all()

Close ALL open positions.

```pine
// Close everything on market crash
bool crashDetected = close < ta.lowest(low, 50) * 0.95

if crashDetected
    strategy.close_all(comment="Emergency Exit")
```

---

### strategy.exit()

Advanced exit with stop loss and take profit.

```pine
strategy.exit(
    id,              // string: Exit order ID
    from_entry,      // string: Which entry to exit (optional)
    qty,            // float: Quantity to exit (optional)
    qty_percent,    // float: % of position to exit (optional)
    profit,         // float: Take profit in ticks (optional)
    limit,          // float: Take profit price (optional)
    loss,           // float: Stop loss in ticks (optional)
    stop,           // float: Stop loss price (optional)
    trail_price,    // float: Trailing stop activation price (optional)
    trail_points,   // float: Trailing stop distance in ticks (optional)
    trail_offset,   // float: Trailing stop offset in ticks (optional)
    oca_name,       // string: OCA group (optional)
    comment,        // string: Exit comment (optional)
    when,           // bool: Condition (optional)
    alert_message   // string: Alert text (optional)
)
```

---

### Exit with Fixed Stop Loss & Take Profit

```pine
//@version=6
strategy("SL/TP Example", overlay=true)

// Inputs
float stopPercent = input.float(2.0, "Stop Loss %", minval=0.1)
float tpPercent = input.float(4.0, "Take Profit %", minval=0.1)

// Entry
bool longCondition = ta.crossover(close[1], ta.sma(close, 20)[1]) and barstate.isconfirmed

if longCondition
    float entryPrice = close[1]
    float stopPrice = entryPrice * (1 - stopPercent/100)
    float tpPrice = entryPrice * (1 + tpPercent/100)
    
    strategy.entry("Long", strategy.long)
    strategy.exit(
        "Long Exit",
        "Long",
        stop=stopPrice,
        limit=tpPrice,
        comment="SL/TP Exit"
    )
```

---

### Trailing Stop

```pine
//@version=6
strategy("Trailing Stop", overlay=true)

// Inputs
float trailPercent = input.float(3.0, "Trailing Stop %", minval=0.1)
float trailOffset = input.float(0.5, "Trail Offset %", minval=0)

// Entry
if ta.crossover(close[1], ta.sma(close, 20)[1]) and barstate.isconfirmed
    strategy.entry("Long", strategy.long)
    
    // Trailing stop activates immediately
    // Trails price by trailPercent, with offset
    float trailTicks = close * (trailPercent/100) / syminfo.mintick
    float offsetTicks = close * (trailOffset/100) / syminfo.mintick
    
    strategy.exit(
        "Trail Exit",
        "Long",
        trail_points=trailTicks,
        trail_offset=offsetTicks,
        comment="Trailing Stop Hit"
    )
```

---

### Multiple Exit Conditions

```pine
//@version=6
strategy("Multiple Exits", overlay=true)

float stopPercent = input.float(2.0, "Stop Loss %")
float tp1Percent = input.float(2.0, "TP1 %")
float tp2Percent = input.float(4.0, "TP2 %")

// Entry
bool longEntry = ta.crossover(close[1], ta.sma(close, 20)[1]) and barstate.isconfirmed

if longEntry
    float entry = close[1]
    strategy.entry("Long", strategy.long)
    
    // Exit 50% at TP1, let rest run
    strategy.exit(
        "TP1",
        "Long",
        qty_percent=50,
        limit=entry * (1 + tp1Percent/100),
        stop=entry * (1 - stopPercent/100),
        comment="TP1 Hit"
    )
    
    // Exit remaining 50% at TP2
    strategy.exit(
        "TP2",
        "Long",
        qty_percent=50,
        limit=entry * (1 + tp2Percent/100),
        stop=entry * (1 - stopPercent/100),
        comment="TP2 Hit"
    )
```

---

## Position Management

### Position Information

```pine
// Check if in position
bool inLong = strategy.position_size > 0
bool inShort = strategy.position_size < 0
bool flat = strategy.position_size == 0

// Position details
float posSize = strategy.position_size          // Current position size
float avgPrice = strategy.position_avg_price    // Average entry price
float openPL = strategy.openprofit             // Open P/L in currency
float openPLPercent = strategy.openprofit / strategy.position_avg_price * 100

// Entry bar information
int barsInTrade = barstate.isconfirmed ? bar_index - strategy.opentrades.entry_bar_index(0) : 0
```

---

### Conditional Exits Based on Position

```pine
//@version=6
strategy("Position-Based Exit", overlay=true)

// Entry logic
if ta.crossover(close[1], ta.sma(close, 20)[1]) and barstate.isconfirmed
    strategy.entry("Long", strategy.long)

// Time-based exit
int barsInTrade = if strategy.position_size > 0
    bar_index - strategy.opentrades.entry_bar_index(0)
else
    0

if barsInTrade > 10
    strategy.close("Long", comment="Time-based exit")

// Profit-based exit
float openPL = strategy.openprofit
float initialCapital = strategy.initial_capital
float profitPercent = (openPL / initialCapital) * 100

if profitPercent > 5
    strategy.close_all(comment="Total profit target hit")
```
