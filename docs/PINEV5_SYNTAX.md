# Pine Script v5: Detailed Coding Requirements and Syntax Rules

Pine Script v5 is a powerful programming language from TradingView used to create custom trading indicators and strategies. This document provides a more comprehensive overview of its syntax and features.

## 1. Script Structure

Every Pine Script v5 script has a fundamental structure.

### 1.1. Version Declaration
All scripts **must** begin with the compiler directive that specifies the version. This is the very first line in the script.
```pinescript
//@version=5
```

### 1.2. Script Declaration
Following the version, you must declare the type of script you are creating. This determines the script's behavior and the functions it can use.
- **`indicator()`**: For scripts that calculate and plot data on a chart.
- **`strategy()`**: For scripts that can perform backtesting and execute simulated trades.
- **`library()`**: For creating reusable functions that can be imported into other scripts.

**Example:**
```pinescript
//@version=5
indicator("My Custom Indicator", shorttitle="MCI", overlay=true)
```
- `title`: The long name of the script.
- `shorttitle`: An abbreviated name shown on the chart.
- `overlay`: If `true`, the script is drawn directly on the main chart. If `false`, it's displayed in a separate pane.

## 2. Data Types

Pine Script v5 has a set of fundamental data types. While typing is often inferred, understanding these types is crucial.

### 2.1. Core Types
- **`int`**: Integer numbers (e.g., `10`, `-5`, `0`).
- **`float`**: Floating-point (decimal) numbers (e.g., `10.5`, `-0.001`).
- **`bool`**: Boolean values, which can be `true` or `false`.
- **`string`**: Textual data, enclosed in single or double quotes (e.g., `"Hello"`, `'World'`).
- **`color`**: Represents colors (e.g., `color.red`, `#FF0000`).

### 2.2. Specialized "Object" Types
These types act as references to objects created by drawing functions.
- **`line`**: A reference to a line drawn on the chart.
- **`linefill`**: A reference to a fill between two lines.
- **`label`**: A reference to a text label on the chart.
- **`box`**: A reference to a box drawing.
- **`table`**: A reference to a table for displaying data.

### 2.3. `void`
The `void` type signifies that a function does not return any value.

## 3. Variables

### 3.1. Declaration and Initialization
Variables are declared and assigned a value simultaneously. The type is inferred from the value and cannot be changed later.
```pinescript
myInteger = 10
myString = "Some text"
isBullish = close > open
```

### 3.2. `var` Keyword
The `var` keyword is used to declare a variable that should be initialized only once, on the first bar of the dataset. Its value is then persisted across subsequent bars.
```pinescript
var float highestHigh = high // Initialized with the 'high' of the first bar
if high > highestHigh
    highestHigh := high // Use ':=' to reassign value
```
- Use the assignment operator `=` for the initial declaration.
- Use the reassignment operator `:=` to update the value of a `var` variable on subsequent bars.

## 4. Series
A "series" is a fundamental concept in Pine Script. It's a continuous sequence of values that exists for each bar on the chart. Built-in variables like `open`, `high`, `low`, and `close` are series. Most calculations and functions operate on series.

## 5. Operators

### 5.1. Arithmetic
- `+` (Addition)
- `-` (Subtraction)
- `*` (Multiplication)
- `/` (Division)
- `%` (Modulo)

### 5.2. Comparison
- `==` (Equal)
- `!=` (Not Equal)
- `<` (Less than)
- `<=` (Less than or equal to)
- `>` (Greater than)
- `>=` (Greater than or equal to)

### 5.3. Logical
- `and` (Logical AND)
- `or` (Logical OR)
- `not` (Logical NOT)

### 5.4. Ternary Operator
A compact way to write a simple if-else statement.
`condition ? value_if_true : value_if_false`
```pinescript
barColor = close > open ? color.green : color.red
```

## 6. Control Structures

### 6.1. `if` Statements
Used for conditional execution of code.
```pinescript
if close > ta.sma(close, 20)
    // Do something if close is above 20-period SMA
```

### 6.2. Loops
- **`for` loops**: Iterate a specific number of times.
  ```pinescript
  float total = 0
  for i = 0 to 9
      total += close[i] // Sum of 'close' over the last 10 bars
  ```
- **`while` loops**: Iterate as long as a condition is true.
  ```pinescript
  int counter = 0
  while counter < 10
      // Do something
      counter := counter + 1
  ```

### 6.3. `switch` Statements
Provides a clean way to handle multiple conditions against a single expression.
```pinescript
string signal = "buy"
color signalColor = switch signal
    "buy"  => color.green
    "sell" => color.red
    => color.gray // Default case
```

## 7. Functions

### 7.1. Built-in Functions & Namespaces
Pine Script v5 organized its vast library of built-in functions into **namespaces**. This means functions are prefixed with a namespace identifier.
- **`ta.`**: Technical analysis (e.g., `ta.sma()`, `ta.rsi()`).
- **`math.`**: Mathematical operations (e.g., `math.abs()`, `math.max()`).
- **`str.`**: String manipulation (e.g., `str.tostring()`).
- **`array.`**: Array operations.
- **`matrix.`**: Matrix operations.
- **`line.`**, **`label.`**, **`box.`**, **`table.`**: Functions to manage drawing objects.

### 7.2. User-Defined Functions
You can create your own functions to encapsulate reusable logic.
```pinescript
// Function to calculate a smoothed moving average
f_smoothed_ma(source, length) =>
    ma = ta.sma(source, length)
    ta.sma(ma, length)

// Use the function
smoothedAverage = f_smoothed_ma(close, 10)
plot(smoothedAverage)
```

## 8. Libraries
Libraries are special scripts that contain only functions intended for reuse in other scripts.
- They start with `library("MyLibrary")`.
- Functions intended to be used by other scripts must be preceded by the `export` keyword.
- To use a library, you import it using the `import` statement with the script's published ID.

**Example Library (`MyLibrary`):**
```pinescript
//@version=5
library("MyLibrary")
export f_my_function(value) =>
    value * 2
```

**Example Indicator using the Library:**
```pinescript
//@version=5
indicator("My Indicator")
import MyTradingviewUsername/MyLibrary/1 as mylib
plot(mylib.f_my_function(close))
```

## 9. Key Changes from v4 to v5

- **`study()` is now `indicator()`**: The main declaration function was renamed.
- **Namespaces**: The introduction of `ta.`, `math.`, etc., is the most significant syntax change. `highest()` became `ta.highest()`.
- **Input Functions**: `input()` was restructured into more specific functions like `input.int()`, `input.float()`, `input.source()`.
- **Color Management**: The `transp` (transparency) parameter was deprecated in favor of using the `color.new(color, transp)` function.
- **Stricter Constants**: Functions now require specific built-in constants where applicable (e.g., `ta.valuewhen(condition, source, occurrence)` instead of using raw numbers for the occurrence).
