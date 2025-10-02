# Pine Script v6 Operators

## Arithmetic Operators

- `+` : Addition
- `-` : Subtraction
- `*` : Multiplication
- `/` : Division
- `%` : Modulo (remainder of a division)

```pine
float result = (10 + 5) * 2 / 3 - 1 // result is 9.0
int remainder = 10 % 3 // remainder is 1
```

## Comparison Operators

Return a `bool` (`true` or `false`) value.

- `>` : Greater than
- `<` : Less than
- `>=` : Greater than or equal to
- `<=` : Less than or equal to
- `==` : Equal to
- `!=` : Not equal to

```pine
bool isBullish = close > open
bool isDoji = close == open
```

## Logical Operators

Used to combine boolean conditions.

- `and` : Logical AND (both conditions must be true)
- `or` : Logical OR (at least one condition must be true)
- `not` : Logical NOT (inverts the boolean value)

```pine
float rsi = ta.rsi(close, 14)
bool isOversold = rsi < 30
bool isOverbought = rsi > 70

bool buySignal = isOversold and ta.crossover(close, ta.sma(close, 10))
bool sellSignal = isOverbought or close < ta.lowest(low, 5)

bool noSignal = not (buySignal or sellSignal)
```

## Ternary Operator `?:`

A compact `if-else` statement. It returns one of two values based on a condition.

**Syntax:** `condition ? value_if_true : value_if_false`

```pine
// Assign color based on whether the bar is bullish or bearish
color barColor = close > open ? color.green : color.red
plot(close, color=barColor)

// Calculate a value conditionally
float adjustment = close > 100 ? 1.05 : 1.02
float adjustedPrice = close * adjustment
```

## Historical Reference Operator `[]`

This is one of the most important operators in Pine Script. It accesses historical values of a `series`.

- `series[0]` is the current value of the series.
- `series[1]` is the previous value.
- `series[n]` is the value `n` bars ago.

```pine
// Accessing historical close prices
float currentClose = close[0] // Same as `close`
float previousClose = close[1]
float closeTwoBarsAgo = close[2]

// CRITICAL for creating non-repainting signals
bool bullishEngulfing = close > open and close[1] < open[1] and close > open[1] and open < close[1]

// Check for a crossover on confirmed, closed bars
bool maCross = ta.crossover(ta.sma(close, 10)[1], ta.sma(close, 20)[1])
```

## Assignment Operators

- `=` : Standard assignment. Used to initialize a variable.
    ```pine
    int length = 14
    ```
- `:=` : Reassignment operator. Used to change the value of a variable that was declared with `var` or in a loop/conditional block.
    ```pine
    var int counter = 0
    if (close > open)
        counter := counter + 1 // Reassign the value of counter
    ```
