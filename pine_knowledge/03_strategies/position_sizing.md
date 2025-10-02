# Pine Script v6 Strategy - Position Sizing

## Overview

Effective position sizing is a cornerstone of risk management. Pine Script strategies offer several ways to define the size of your trades, configured both in the `strategy()` declaration and dynamically in the script.

## `strategy()` Declaration Methods

You can set a default sizing method in the `strategy()` function. This is the simplest approach.

- **`default_qty_type`**: The method used to calculate quantity.
- **`default_qty_value`**: The value to use with the chosen method.

### 1. Fixed Quantity (`strategy.fixed`)

Trade the same number of contracts/shares/lots for every trade.

```pine
strategy(
    "Fixed Qty Strategy", 
    default_qty_type = strategy.fixed, 
    default_qty_value = 1  // Trade 1 contract per trade
)
```

### 2. Percentage of Equity (`strategy.percent_of_equity`)

Risk a certain percentage of your total strategy equity on each trade. The position size is calculated based on the current equity.

```pine
strategy(
    "Percent of Equity Strategy", 
    default_qty_type = strategy.percent_of_equity, 
    default_qty_value = 10 // Risk 10% of equity per trade
)
```
**Calculation:** `Position Size = (Strategy Equity * % Risk) / Entry Price`

### 3. Cash Amount (`strategy.cash`)

Allocate a fixed amount of cash for each trade.

```pine
strategy(
    "Cash Strategy", 
    default_qty_type = strategy.cash, 
    default_qty_value = 1000 // Use $1000 for each trade
)
```
**Calculation:** `Position Size = Cash Amount / Entry Price`

---

## Dynamic Position Sizing in Code

For more advanced control, you can calculate the quantity dynamically within your script and pass it to `strategy.entry()` using the `qty` parameter. This overrides the `default_qty_*` settings.

### 1. Risk-Based Sizing (ATR Stop Loss)

This is a very common and robust method. The position size is calculated based on a fixed risk amount and a dynamic stop loss distance (e.g., using ATR).

**Formula:** `Quantity = (Total Equity * % Risk per Trade) / (Stop Loss Distance in $)`

```pine
//@version=6
strategy("ATR Risk Sizing", overlay=true, initial_capital=10000)

// Inputs
float riskPercent = input.float(2.0, "Risk % per Trade", minval=0.1)
float atrLength = input.int(14, "ATR Length")
float atrMultiplier = input.float(2.0, "ATR Multiplier for SL")

// Calculations
float atrValue = ta.atr(atrLength)
float stopLossDistance = atrValue * atrMultiplier
float riskAmount = strategy.equity * (riskPercent / 100)
float positionSize = riskAmount / stopLossDistance

// Entry Condition
bool longCondition = ta.crossover(close[1], ta.sma(close, 50)[1]) and barstate.isconfirmed

if longCondition
    // Enter with dynamically calculated size
    strategy.entry("Long", strategy.long, qty = positionSize)
    
    // Set the stop loss
    float stopPrice = close - stopLossDistance
    strategy.exit("Exit SL/TP", "Long", stop = stopPrice)
```

### 2. Volatility-Adjusted Sizing

You can adjust position size based on market volatility. For example, take smaller positions when volatility is high and larger positions when it's low.

```pine
//@version=6
strategy("Volatility Adjusted Sizing", overlay=true)

float atrLength = input.int(14, "ATR Length")
float avgAtrLength = input.int(50, "Avg ATR Length")

float atrValue = ta.atr(atrLength)
float avgAtr = ta.sma(atrValue, avgAtrLength)

// Determine volatility state
bool isHighVolatility = atrValue > avgAtr * 1.2
bool isLowVolatility = atrValue < avgAtr * 0.8

// Adjust position size
float baseQty = 1.0
float finalQty = isHighVolatility ? baseQty * 0.5 : isLowVolatility ? baseQty * 1.5 : baseQty

// Entry
bool longCondition = ta.crossover(close[1], ta.sma(close, 20)[1]) and barstate.isconfirmed
if longCondition
    strategy.entry("Long", strategy.long, qty = finalQty)
```

---

## Key Considerations

- **Pyramiding**: If you allow multiple entries in the same direction (`pyramiding > 0` in the `strategy` declaration), your position sizing logic needs to account for this. The `qty` in `strategy.entry` will be *added* to the current position.
- **`strategy.equity` vs `strategy.initial_capital`**: `strategy.equity` includes the initial capital plus the net profit/loss of all closed trades. It represents your current account value. Use this for dynamic calculations.
- **Backtest vs. Live Trading**: Be aware that position sizing calculations in backtests are idealized. In live trading, factors like slippage, commissions, and order fill uncertainty will affect the final execution price and, therefore, the actual position size if calculated dynamically.
