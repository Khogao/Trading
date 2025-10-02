# Pine Script v6 Type System

Pine Script v6 has a strong type system. Declaring types explicitly is highly recommended to prevent common errors.

## Primitive Types

- **`int`**: Integer numbers (e.g., `14`, `-1`, `0`).
- **`float`**: Floating-point numbers (e.g., `100.5`, `-2.5`, `3.14`).
- **`bool`**: Boolean values (`true` or `false`).
- **`color`**: Color constants and values (e.g., `color.red`, `#FF5733`).
- **`string`**: Text strings (e.g., `"Hello"`, `'World'`).

### Explicit Type Declaration (Recommended)
```pine
int length = 14
float price = 100.5
bool condition = true
color bullColor = color.green
string timeframe = "D"
```

### Implicit Type Declaration
While possible, it's less safe.
```pine
length = 14        // Inferred as int
price = 100.5      // Inferred as float
condition = true   // Inferred as bool
```

## Series vs Simple

This is a crucial concept in Pine Script.

- **`simple`**: The value is constant and does not change on each bar. Typically used for inputs or constants.
    - `simple int`, `simple float`, etc.
- **`series`**: The value can be different on each bar. Most built-in variables (`close`, `high`) and function results (`ta.sma`) are series.
    - `series int`, `series float`, etc.

```pine
// Simple type (constant on all bars)
simple int myLength = 14

// Series type (can change on each bar)
series float myClose = close
series float mySMA = ta.sma(close, 14)
```

## Special Types

- **`plot`**: Represents a plot on the chart, returned by `plot()`.
- **`hline`**: Represents a horizontal line, returned by `hline()`.
- **`label`**: Represents a text label, returned by `label.new()`.
- **`line`**: Represents a drawn line, returned by `line.new()`.
- **`table`**: Represents a table on the chart, returned by `table.new()`.

## Data Structures

- **`array`**: A collection of elements of the same type.
    - `array<int>`, `array<float>`, `array<string>`
    ```pine
    var int[] myArray = array.new<int>(5, 0) // Creates an array of 5 integers
    ```
- **`matrix`**: A two-dimensional array.
    - `matrix<int>`, `matrix<float>`
    ```pine
    var float[][] myMatrix = matrix.new<float>(2, 2, 0.0) // Creates a 2x2 matrix
    ```
- **`map`**: A collection of key-value pairs.
    - `map<int, string>`, `map<string, float>`
    ```pine
    var myMap = map.new<string, float>()
    map.put(myMap, "BTC", 50000.5)
    ```
- **`tuple`**: An ordered, immutable collection of elements that can have different types. Often used to return multiple values from a function.
    ```pine
    myFunction() =>
        [1, "hello", true] // Returns a tuple [int, string, bool]

    [myInt, myString, myBool] = myFunction()
    ```

## `void` Type

Represents the absence of a value. Functions that do not return anything have a `void` return type.

## Type Casting

You can convert between types using built-in functions:

- `int(value)`
- `float(value)`
- `string(value)` or `str.tostring(value)`
- `bool(value)`

```pine
float myFloat = 14.8
int myInt = int(myFloat) // myInt is 14

string myString = str.tostring(myInt) // myString is "14"
```
