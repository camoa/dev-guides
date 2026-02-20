---
description: Convert JavaScript array methods to Twig for loops
drupal_version: "11.x"
---

# Loops & Iteration

## When to Use

> Use this when converting JavaScript array methods (`.map()`, `.filter()`, `.reduce()`, `.slice()`) to Twig `{% for %}` loops and filters.

## Decision

| JSX Pattern | Twig Equivalent | Notes |
|---|---|---|
| `{items.map(item => <Item />)}` | `{% for item in items %}<Item />{% endfor %}` | Basic iteration |
| `{items.map((item, i) => ...)}` | `{% for item in items %}` + `loop.index0` | `loop.index0` is 0-based, `loop.index` is 1-based |
| `{items.filter(i => i.active).map(...)}` | `{% for item in items if item.active %}` | Inline filter on `{% for %}` |
| `{items.slice(0, 3).map(...)}` | `{% for item in items\|slice(0, 3) %}` | `slice` filter takes offset + length |
| `{items.slice(-2).map(...)}` | `{% for item in items\|slice(-2) %}` | Negative offset works same as JS |
| `{Object.entries(obj).map(([k, v]) => ...)}` | `{% for key, val in obj %}` | Destructured key-value iteration |
| `{Object.keys(obj).map(k => ...)}` | `{% for key in obj\|keys %}` | Keys-only iteration |
| `{items.length === 0 && <Empty />}` | `{% for item in items %}...{% else %}<Empty />{% endfor %}` | `{% else %}` on `{% for %}` handles empty case |
| `{items.reduce((sum, i) => sum + i.count, 0)}` | Preprocess in PHP | No `reduce` in Twig -- compute aggregations in preprocess |
| `{items.flatMap(i => i.children).map(...)}` | Preprocess in PHP | No `flatMap` -- flatten data before passing to Twig |

## Pattern: Loop with Index and Separators

**React**
```jsx
{items.map((item, index) => (
  <Fragment key={item.id}>
    {index > 0 && <Divider />}
    <ListItem item={item} />
  </Fragment>
))}
```

**Twig**
```twig
{% for item in items %}
  {% if not loop.first %}
    <hr class="divider">
  {% endif %}
  {% include 'ui_suite_daisyui:list_row' with {
    title: item.title,
    description: item.description,
  } %}
{% endfor %}
```

## Loop Variable Reference

| Twig Variable | JS Equivalent | Description |
|---|---|---|
| `loop.index` | `index + 1` | 1-based index |
| `loop.index0` | `index` | 0-based index |
| `loop.first` | `index === 0` | True on first iteration |
| `loop.last` | `index === arr.length - 1` | True on last iteration |
| `loop.length` | `arr.length` | Total items count |

## Common Mistakes

- **Wrong**: Using `{% for item in items|slice(0, 3) if item.active %}` → **Right**: Filter in preprocess if you need exactly N matching items
- **Wrong**: Trying to mutate the loop variable → **Right**: `{% set %}` inside a `{% for %}` creates a new scope; use preprocess for aggregations
- **Wrong**: Forgetting that `loop.length` counts filtered items → **Right**: When using `{% for ... if %}`, `loop.length` reflects the filtered count, not the original array length

## See Also

- [Conditional Rendering](conditional-rendering.md)
- [Component Composition](composition.md)
- Reference: [Twig For Loop](https://twig.symfony.com/doc/3.x/tags/for.html)
