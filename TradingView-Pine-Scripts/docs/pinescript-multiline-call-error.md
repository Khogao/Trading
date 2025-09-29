# Pine Script Syntax Error Note

**Error:**

```
Error at line X: Mismatched input "end of line without line continuation" expecting ")"
```

**Cause:**

- Pine Script does not support multi-line function calls without explicit line continuation (\).
- For example, this will cause an error:

```pine
label.new(
    bar_index,
    y,
    txt,
    style=label.style_label_left,
    yloc=yloc_,
    color=na,
    textcolor=trendTextCol,
    size=size.small
)
```

**Fix:**

- Write the function call on a single line:

```pine
label.new(bar_index, y, txt, style=label.style_label_left, yloc=yloc_, color=na, textcolor=trendTextCol, size=size.small)
```

**Recommendation:**

- Always use single-line function calls for built-in Pine Script functions.
- If you need to break lines, use explicit line continuation (\) at the end of each line (rarely used in Pine Script).

---

**Snippet for correct label.new usage:**

```pine
label.new(bar_index, y, txt, style=label.style_label_left, yloc=yloc_, color=na, textcolor=trendTextCol, size=size.small)
```
