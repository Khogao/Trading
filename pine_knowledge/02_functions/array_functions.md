# Pine Script v6 `array` Namespace

## Overview

The `array` namespace provides functions for creating and manipulating one-dimensional arrays. Arrays in Pine Script are mutable, dynamic-sized collections of elements of the same type.

## Creating an Array

Use `array.new<type>(size, initial_value)` to create a new array.

```pine
// Create an array of 5 floats, all initialized to 0.0
var float[] floatArray = array.new<float>(5, 0.0)

// Create an empty integer array
var int[] intArray = array.new<int>()

// Create a string array
var string[] stringArray = array.new<string>(2, "default")
```

**Note:** It's common practice to declare arrays with `var` so they are created only once and persist across bars.

---

## Common `array` Functions

### Adding Elements

- **`array.push(id, value)`**: Adds a new element to the end of the array.
- **`array.unshift(id, value)`**: Adds a new element to the beginning of the array.

```pine
var prices = array.new<float>()

// Add the current close to the end of the array on each bar
array.push(prices, close)
```

### Removing Elements

- **`array.pop(id)`**: Removes the last element from the array and returns its value.
- **`array.shift(id)`**: Removes the first element from the array and returns its value.
- **`array.remove(id, index)`**: Removes the element at a specific index.
- **`array.clear(id)`**: Removes all elements from the array.

```pine
// Keep only the last 10 close prices
var prices = array.new<float>()
array.push(prices, close)
if array.size(prices) > 10
    array.shift(prices) // Remove the oldest element
```

### Accessing Elements

- **`array.get(id, index)`**: Retrieves the element at a specific index.
- **`array.set(id, index, value)`**: Changes the value of an element at a specific index.
- **`array.first(id)`**: Gets the first element.
- **`array.last(id)`**: Gets the last element.

```pine
float lastPrice = array.get(prices, array.size(prices) - 1)

// Update the first element
if array.size(prices) > 0
    array.set(prices, 0, high)
```

### Size & Information

- **`array.size(id)`**: Returns the number of elements in the array.
- **`array.is_empty(id)`**: Returns `true` if the array has no elements.

### Iterating & Slicing

- **`array.slice(id, from_index, to_index)`**: Creates a shallow copy of a portion of the array.
- **`for...in` loop**: The standard way to iterate over array elements.

```pine
float sum = 0
for price in prices
    sum += price

float average = sum / array.size(prices)
```

### Searching & Sorting

- **`array.includes(id, value)`**: Checks if a value exists in the array.
- **`array.indexof(id, value)`**: Returns the index of the first occurrence of a value.
- **`array.sort(id, order)`**: Sorts the array. `order.ascending` or `order.descending`.

### Statistical Functions

- **`array.avg(id)`**: Average of all values.
- **`array.sum(id)`**: Sum of all values.
- **`array.max(id)`**: Maximum value in the array.
- **`array.min(id)`**: Minimum value in the array.
- **`array.stdev(id)`**: Standard deviation.

**Example:**
```pine
// Calculate the average of the last 10 close prices
var prices = array.new<float>()
array.push(prices, close)
if array.size(prices) > 10
    array.shift(prices)

float avg_10_closes = array.avg(prices)
plot(avg_10_closes, "Array Avg Close")
```
