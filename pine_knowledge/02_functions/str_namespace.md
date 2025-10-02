# Pine Script v6 `str` Namespace

## Overview

The `str` namespace provides essential functions for string manipulation, formatting, and conversion.

## Common `str` Functions

### Conversion to String

- **`str.tostring(value, format)`**: Converts a value (int, float, bool, etc.) into a string. The `format` parameter is optional and powerful.

**Example:**
```pine
// Basic conversion
string close_str = "Close: " + str.tostring(close)

// Formatting a float to 2 decimal places
string formatted_close = str.tostring(close, "#.##")

// Formatting as a percentage
float gain = (close - open) / open
string gain_str = str.tostring(gain, "#.##%")

// Formatting a timestamp (in milliseconds)
string time_str = str.tostring(time, "yyyy-MM-dd HH:mm")

if (barstate.islast)
    label.new(bar_index, high, time_str)
```

### Conversion from String

- **`str.tonumber(string)`**: Converts a string into a float. Returns `na` if the conversion fails.

**Example:**
```pine
string price_str = "123.45"
float price_float = str.tonumber(price_str) // Result: 123.45
```

### String Information

- **`str.length(string)`**: Returns the number of characters in a string.

**Example:**
```pine
bool is_htf_set = str.length(input.timeframe("D")) > 0
```

### String Manipulation

- **`str.split(string, separator)`**: Splits a string into an array of substrings based on a `separator`.
- **`str.join(array, separator)`**: Joins an array of strings into a single string, separated by a `separator`.
- **`str.replace_all(source, target, replacement)`**: Replaces all occurrences of a `target` substring with a `replacement`.

**Example:**
```pine
// Splitting
string csv = "BTC,ETH,XRP"
string[] coins = str.split(csv, ",") // Result: ["BTC", "ETH", "XRP"]

// Joining
string joined_str = str.join(coins, " | ") // Result: "BTC | ETH | XRP"

// Replacing
string original = "Hello World"
string replaced = str.replace_all(original, "World", "Pine Script") // Result: "Hello Pine Script"
```

### String Formatting (`str.format`)

This function provides powerful, C-style `printf` formatting.

**Syntax:** `str.format(format_string, arg0, arg1, ...)`

**Format Specifiers:**
- `{0}`, `{1}`, etc.: Positional placeholders.
- `{0,number,#.##}`: Formats a number with 2 decimal places.
- `{0,time,yyyy-MM-dd}`: Formats a timestamp.

**Example:**
```pine
// Simple positional formatting
string msg = str.format("The high was {0} and the low was {1}.", high, low)

// Formatting with number and time formats
string report = str.format("On {0,time,dd-MMM-yyyy}, {1} closed at {2,number,#.##}.", time, syminfo.ticker, close)

if (barstate.islast)
    label.new(bar_index, high, report)
```
