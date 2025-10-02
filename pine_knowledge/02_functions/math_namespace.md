# Pine Script v6 `math` Namespace

## Overview

The `math` namespace provides a collection of common mathematical constants and functions.

## Constants

- **`math.pi`**: The mathematical constant Pi (π ≈ 3.14159).
- **`math.e`**: The mathematical constant e (Euler's number ≈ 2.71828).

## Common `math` Functions

### Basic Arithmetic

- **`math.abs(number)`**: Returns the absolute (non-negative) value of a number.
- **`math.pow(base, exponent)`**: Returns the `base` raised to the power of the `exponent`.
- **`math.sqrt(number)`**: Returns the square root of a number.
- **`math.sign(number)`**: Returns the sign of a number: `1` if positive, `-1` if negative, `0` if zero.

**Example:**
```pine
float distance = math.abs(close - open)
float squared = math.pow(distance, 2)
```

### Logarithmic & Exponential

- **`math.log(number)`**: Returns the natural logarithm (base e) of a number.
- **`math.log10(number)`**: Returns the base-10 logarithm of a number.
- **`math.exp(number)`**: Returns e raised to the power of a number.

**Example:**
```pine
// Calculate log-return
float logReturn = math.log(close / close[1])
plot(logReturn)
```

### Min, Max, and Clamping

- **`math.max(number1, number2, ...)`**: Returns the largest value from a set of numbers.
- **`math.min(number1, number2, ...)`**: Returns the smallest value from a set of numbers.
- **`math.clamp(number, min_val, max_val)`**: Constrains a `number` to be within a specific range `[min_val, max_val]`.

**Example:**
```pine
// Find the max of high and previous close
float maxVal = math.max(high, close[1])

// Keep RSI value between 10 and 90 for coloring
float rsi = ta.rsi(close, 14)
float clampedRSI = math.clamp(rsi, 10, 90)
```

### Rounding

- **`math.round(number)`**: Rounds to the nearest integer.
- **`math.round_to_precision(number, precision)`**: Rounds to a specified number of decimal places.
- **`math.ceil(number)`**: Rounds up to the nearest integer.
- **`math.floor(number)`**: Rounds down to the nearest integer.

**Example:**
```pine
float price = 123.456
float roundedPrice = math.round_to_precision(price, 2) // Result: 123.46

int roundedUp = math.ceil(99.1) // Result: 100
int roundedDown = math.floor(99.9) // Result: 99
```

### Random Number Generation

- **`math.random(min, max, seed)`**: Generates a pseudo-random number. The `seed` is optional but useful for creating reproducible sequences.

**Example:**
```pine
// Generate a random float between 0 and 1
float randomVal = math.random(0, 1)

// Generate a random integer between 1 and 100
int randomInt = math.floor(math.random(1, 101))
```

### Trigonometric Functions

The `math` library also includes standard trigonometric functions, which can be useful for cyclical analysis.

- **`math.sin(angle)`**
- **`math.cos(angle)`**
- **`math.tan(angle)`**
- **`math.asin(value)`**
- **`math.acos(value)`**
- **`math.atan(value)`**

**Example:**
```pine
// Create a simple sine wave indicator
float sineWave = math.sin(2 * math.pi * bar_index / 20) // 20-bar cycle
plot(sineWave, "Sine Wave")
```
