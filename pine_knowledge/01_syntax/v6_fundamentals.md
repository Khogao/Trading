# Pine Script v6 Fundamentals

## Version Declaration
Every script must start with:
```pine
//@version=6
```

## Script Types

### Indicator
For studies, indicators, oscillators:
```pine
//@version=6
indicator("My Indicator", overlay=true, max_bars_back=500)
```

Parameters:
- `title` (string): Display name
- `overlay` (bool): true = on chart, false = separate pane
- `max_bars_back` (int): Historical bars to process
- `format` (string): "price" or "volume"
- `precision` (int): Decimal places

### Strategy
For backtestable strategies:
```pine
//@version=6
strategy(
    "My Strategy",
    overlay=true,
    default_qty_type=strategy.percent_of_equity,
    default_qty_value=10,
    commission_type=strategy.commission.percent,
    commission_value=0.1
)
```

## Variable Declarations

### Explicit Types (Recommended)
```pine
int length = 14
float price = 100.5
bool condition = true
color col = color.red
string timeframe = "D"
```

### Implicit Types
```pine
length = 14        // Inferred as int
price = 100.5      // Inferred as float
condition = true   // Inferred as bool
```

### Var Keyword
Maintains value across bars:
```pine
var int counter = 0
counter := counter + 1  // Increments each bar
```

## Series vs Simple Types

### Simple
Value doesn't change across bars:
```pine
int myLength = 14  // Same on all bars
```

### Series
Value can change per bar:
```pine
float myClose = close  // Different each bar
float mySMA = ta.sma(close, 14)  // Calculated each bar
```

## Operators

### Arithmetic
- `+` Addition
- `-` Subtraction
- `*` Multiplication
- `/` Division
- `%` Modulo

### Comparison
- `>` Greater than
- `<` Less than
- `>=` Greater or equal
- `<=` Less or equal
- `==` Equal
- `!=` Not equal

### Logical
- `and` Logical AND
- `or` Logical OR
- `not` Logical NOT

### Ternary
```pine
result = condition ? valueIfTrue : valueIfFalse
color myColor = close > open ? color.green : color.red
```

## Historical Reference Operator []

Access previous bar values:
```pine
close[0]   // Current bar close (same as close)
close[1]   // Previous bar close
close[2]   // 2 bars ago
high[5]    // 5 bars ago high
```

**CRITICAL for anti-repainting:**
```pine
// ❌ Repaints - uses real-time close
crossover = ta.crossover(close, ma)

// ✅ No repaint - uses confirmed close
crossover = ta.crossover(close[1], ma[1])
```

## Conditional Structures

### If Statement
```pine
if condition
    // code
else if otherCondition
    // code
else
    // code
```

### If Expression (returns value)
```pine
value = if condition
    100
else
    200
```

## Loops

### For Loop
```pine
sum = 0.0
for i = 0 to 9
    sum := sum + close[i]
average = sum / 10
```

### While Loop
```pine
int i = 0
float sum = 0
while i < 10
    sum := sum + close[i]
    i := i + 1
```

## Functions

### Built-in Functions
Must use namespace:
```pine
ta.rsi(source, length)
ta.sma(source, length)
math.abs(number)
str.tostring(value)
```

### User-Defined Functions
```pine
// Simple function
calcAverage(float value1, float value2) =>
    (value1 + value2) / 2

// Function with multiple statements
calcRange(float high, float low) =>
    float range = high - low
    float midpoint = (high + low) / 2
    [range, midpoint]  // Returns tuple

// Usage
avg = calcAverage(close, open)
[myRange, myMid] = calcRange(high, low)
```

## Arrays

### Declaration
```pine
var float[] prices = array.new<float>(10, 0.0)
var int[] counts = array.new<int>()
```

### Common Operations
```pine
array.push(prices, close)           // Add to end
array.unshift(prices, close)        // Add to beginning  
lastPrice = array.pop(prices)       // Remove from end
firstPrice = array.shift(prices)    // Remove from beginning
array.set(prices, 0, close)         // Set value at index
value = array.get(prices, 0)        // Get value at index
size = array.size(prices)           // Get array size
array.clear(prices)                 // Remove all elements
```

## Scope

### Local Scope
Variables declared in if/for/while are local:
```pine
if condition
    int localVar = 10  // Only exists in this block
```

### Global Scope  
Variables declared at script level:
```pine
//@version=6
indicator("Test")

int globalVar = 10  // Available everywhere
```

## Comments

### Single Line
```pine
// This is a comment
int length = 14  // Inline comment
```

### Multi-line
```pine
/* 
This is a
multi-line comment
*/
```

## Best Practices

1. **Always use explicit types**
2. **Use var for persistent variables**
3. **Add comments for complex logic**
4. **Use descriptive variable names**
5. **Organize code logically (inputs, calculations, plots)**
6. **Use historical reference [1] to avoid repainting**
