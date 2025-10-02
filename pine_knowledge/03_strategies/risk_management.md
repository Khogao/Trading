# Pine Script v6 Strategy - Risk Management

## Overview

Risk management is arguably the most critical component of a successful trading strategy. Pine Script provides built-in functions to programmatically define and execute risk management rules, primarily through stop-loss and take-profit orders.

## 1. Stop-Loss Orders

A stop-loss is an order to close a position at a specific price to limit losses.

### `strategy.exit()` for Stop-Loss

The most common way to set a stop-loss is using the `stop` parameter in the `strategy.exit()` function. This creates a stop-market order that triggers when the specified price level is hit.

#### a) Fixed Percentage Stop-Loss

Set the stop-loss at a fixed percentage below the entry price.

```pine
float stopPercent = input.float(2.0, "Stop Loss %")

if (longCondition)
    strategy.entry("Long", strategy.long)
    
    // Set stop-loss after entry
    if (strategy.position_size > 0)
        float stopPrice = strategy.position_avg_price * (1 - stopPercent / 100)
        strategy.exit("Exit SL", from_entry="Long", stop=stopPrice)
```

#### b) ATR-Based Stop-Loss (Volatility-Adjusted)

This is a more robust method where the stop-loss distance is based on market volatility, measured by the Average True Range (ATR).

```pine
float atrLength = input.int(14, "ATR Length")
float atrMultiplier = input.float(2.5, "ATR Multiplier")

float atrValue = ta.atr(atrLength)

if (longCondition)
    strategy.entry("Long", strategy.long)

    if (strategy.position_size > 0)
        float stopDistance = atrValue * atrMultiplier
        float stopPrice = strategy.position_avg_price - stopDistance
        strategy.exit("Exit SL", from_entry="Long", stop=stopPrice)
```

#### c) Pivot-Based Stop-Loss

Place the stop-loss below the most recent swing low (for a long trade).

```pine
float lastPivotLow = ta.valuewhen(ta.pivot_low(low, 5, 5), low, 1)

if (longCondition and not na(lastPivotLow))
    strategy.entry("Long", strategy.long)

    if (strategy.position_size > 0)
        // Place stop slightly below the last pivot
        float stopPrice = lastPivotLow - syminfo.mintick * 5
        strategy.exit("Exit SL", from_entry="Long", stop=stopPrice)
```

## 2. Take-Profit Orders

A take-profit order closes a position once it reaches a certain level of profit.

### `strategy.exit()` for Take-Profit

Use the `limit` parameter in `strategy.exit()` to set a take-profit level. This creates a limit order.

#### a) Fixed Risk-to-Reward Ratio

Set the take-profit distance as a multiple of the stop-loss distance.

```pine
float riskRewardRatio = input.float(2.0, "Risk/Reward Ratio")

if (longCondition)
    strategy.entry("Long", strategy.long)

    if (strategy.position_size > 0)
        float stopDistance = close - (close * (1 - stopPercent / 100))
        float stopPrice = close - stopDistance
        float takeProfitPrice = close + stopDistance * riskRewardRatio
        strategy.exit("Exit SL/TP", from_entry="Long", stop=stopPrice, limit=takeProfitPrice)
```

#### b) Indicator-Based Take-Profit

Close the position when price reaches a key indicator level, like an upper Bollinger Band®.

```pine
[bbBasis, bbUpper, bbLower] = ta.bb(close, 20, 2)

if (longCondition)
    strategy.entry("Long", strategy.long)

// Use strategy.close() for conditional exits
if (strategy.position_size > 0 and ta.crossover(high, bbUpper))
    strategy.close("Long", comment="TP at Upper BB")
```

## 3. Trailing Stops

A trailing stop is a stop-loss order that moves in the direction of a profitable trade, locking in profits.

### `strategy.exit()` for Trailing Stops

Use the `trail_points` or `trail_offset` parameters.

- **`trail_points`**: The stop price trails the market price by a fixed number of *points* (price, not ticks).
- **`trail_offset`**: The stop price trails the market price by a fixed number of *ticks*.

```pine
float trailPercent = input.float(3.0, "Trailing Stop %")

if (longCondition)
    strategy.entry("Long", strategy.long)

    if (strategy.position_size > 0)
        // Calculate trail distance in points (price)
        float trailDistance = strategy.position_avg_price * (trailPercent / 100)
        strategy.exit("Trailing Exit", from_entry="Long", trail_points=trailDistance)
```

## Combining It All

The `strategy.exit()` function is powerful because it can place a Stop-Loss and a Take-Profit order simultaneously as a One-Cancels-All (OCA) group. The first one to be hit cancels the other.

```pine
//@version=6
strategy("Complete Risk Management", overlay=true)

// Inputs
float stopPercent = input.float(2.0, "Stop %")
float tpPercent = input.float(4.0, "TP %")

// Entry
bool longCondition = ta.crossover(ta.ema(close,10)[1], ta.ema(close,20)[1]) and barstate.isconfirmed

if (longCondition)
    strategy.entry("Long", strategy.long)

// Set SL and TP immediately after entering a trade
if (strategy.position_size > 0)
    float stopLossPrice = strategy.position_avg_price * (1 - stopPercent / 100)
    float takeProfitPrice = strategy.position_avg_price * (1 + tpPercent / 100)
    
    strategy.exit(
      id="Exit Long SL/TP", 
      from_entry="Long", 
      stop=stopLossPrice, 
      limit=takeProfitPrice
    )
```
