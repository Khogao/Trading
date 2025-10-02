# Pine Script v6 - Backtesting Best Practices

## Overview

Backtesting is the process of testing a trading strategy on historical data to determine its potential viability. A reliable backtest is crucial for gaining confidence in a strategy before risking real capital. This guide outlines best practices to ensure your Pine Script backtests are as realistic and trustworthy as possible.

## 1. Use Sufficient, High-Quality Data

- **Problem**: A strategy tested on a short or specific period (e.g., only a bull market) may not be robust.
- **Best Practice**: Test your strategy over a long period of historical data that includes various market conditions (bull, bear, sideways markets). TradingView's `Deep History` feature can be useful for this.

## 2. Prevent Repainting at All Costs

- **Problem**: Repainting strategies show misleadingly optimistic results because they make decisions based on information that would not have been available in real-time.
- **Best Practice**: Adhere strictly to non-repainting coding patterns.
    - **Use the historical operator `[1]`** for all conditions based on series values (`close[1]`, `rsi[1]`, etc.).
    - **Use `barstate.isconfirmed`** in `if` blocks for strategy execution to ensure the bar is closed.
    - **Use `lookahead=barmerge.lookahead_off`** in all `request.security()` calls.

*For a deep dive, see `../04_anti_patterns/repainting_issues.md`.*

## 3. Avoid Lookahead Bias

- **Problem**: Lookahead bias occurs when the backtest uses information from the future to make decisions. This is a subtle but critical error.
- **Best Practice**:
    - The primary source of lookahead bias is incorrect `request.security()` usage. Always use `lookahead=barmerge.lookahead_off`.
    - Do not use functions that implicitly look ahead, such as `ta.pivot_high` or `ta.pivot_low` with a `rightbars` value greater than 0, to make decisions on the current bar.

*For more details, see `../04_anti_patterns/lookahead_bias.md`.*

## 4. Account for Realistic Trading Costs

- **Problem**: Backtests that don't include commissions and slippage will overestimate profitability.
- **Best Practice**: Set realistic `commission_value` and `slippage` in your `strategy()` declaration. A good starting point is 0.05% - 0.1% for commission and 1-2 ticks for slippage, depending on the market.

```pine
strategy(
    "My Strategy",
    // ... other settings
    commission_type=strategy.commission.percent,
    commission_value=0.1, // 0.1% commission per trade
    slippage=2            // 2 ticks of slippage per order
)
```

## 5. Beware of Overfitting (Curve Fitting)

- **Problem**: Overfitting occurs when you optimize a strategy's parameters to perform exceptionally well on a specific historical dataset. The strategy learns the noise of the past data, not a robust underlying pattern, and will likely fail in live trading.
- **Best Practice**:
    - **Keep it Simple**: Strategies with fewer parameters and simpler rules tend to be more robust.
    - **Test on Out-of-Sample Data**: Divide your data into an "in-sample" period for optimization and an "out-of-sample" period for validation. The strategy should still be profitable on the data it wasn't trained on.
    - **Walk-Forward Analysis**: A more advanced method where you repeatedly optimize on one period and test on the next, sliding the window forward in time.

*For more details, see `../04_anti_patterns/overfitting.md`.*

## 6. Analyze Performance Metrics Holistically

- **Problem**: Looking only at "Net Profit" can be misleading.
- **Best Practice**: Evaluate a wide range of metrics from the Strategy Tester report:
    - **Profit Factor**: Gross Profit / Gross Loss. A value > 1.5 is often considered good.
    - **Max Drawdown**: The largest peak-to-trough drop in equity. This is a key measure of risk.
    - **Sharpe Ratio**: Measures risk-adjusted return. Higher is better.
    - **Average Trade**: The average profit or loss per trade. Ensure this is high enough to cover costs and still be profitable.
    - **Total Closed Trades**: A strategy with very few trades is not statistically significant.

## 7. Perform Robustness Checks

- **Problem**: A strategy might only work on a specific symbol or timeframe.
- **Best Practice**:
    - **Test on Different Symbols**: A truly robust strategy should show positive results on other, similar assets.
    - **Test on Different Timeframes**: Check if the underlying logic holds on higher or lower timeframes.
    - **Parameter Sensitivity**: Slightly change your parameters (e.g., MA length from 20 to 22). A robust strategy's performance should not fall apart completely with minor tweaks.
