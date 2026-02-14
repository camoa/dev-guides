---
description: Render array structure fundamentals -- properties vs children, nesting, weight-based ordering.
---

# Render Array Structure

## When to Use

Whenever you're building any render array -- understanding structure is foundational to using the Render API.

## Structure Components

Render arrays have two types of keys:

| Key Type | Syntax | Purpose | Example |
|---|---|---|---|
| **Properties** | Start with `#` | Control rendering behavior | `#type`, `#theme`, `#markup`, `#cache`, `#access` |
| **Children** | No `#` prefix | Nested render arrays that become child content | `'title'`, `'body'`, `0`, `1` |

**Rendering order:**

1. Properties are processed to determine how to render
2. Children are sorted by `#weight` (if not `#sorted = TRUE`)
3. Children are rendered recursively
4. Results are combined according to parent's `#theme` or `#type`

## Pattern: Nested Structure

```php
$build = [
  // Properties (start with #)
  '#type' => 'container',
  '#attributes' => ['class' => ['outer']],
  '#weight' => 10,
  '#cache' => ['contexts' => ['user']],

  // Children (no # prefix)
  'header' => [
    '#type' => 'html_tag',
    '#tag' => 'h2',
    '#value' => $this->t('Title'),
    '#weight' => -10,  // Rendered first
  ],
  'body' => [
    '#markup' => $body_text,
    '#weight' => 0,
  ],
];
```

**Reference:** `core/lib/Drupal/Core/Render/RendererInterface.php` (lines 93-99) -- properties vs children explanation

## Common Mistakes

- **Using `#` prefix on child keys** -- Makes them properties, not children -- they won't render
- **Forgetting `#sorted = TRUE` when children are pre-sorted** -- Wastes CPU on unnecessary sorting
- **Deeply nesting without considering cache contexts** -- Cache contexts bubble up; every level needs appropriate metadata
- **Mixing numeric and string child keys without understanding sort order** -- Numeric keys sort before string keys; use `#weight` for explicit control

## See Also

- [Render Properties](render-properties.md) for property reference
- [Cache Metadata in Render Arrays](cache-metadata-render-arrays.md) for metadata bubbling
- Reference: [Render arrays documentation](https://www.drupal.org/docs/drupal-apis/render-api/render-arrays)
