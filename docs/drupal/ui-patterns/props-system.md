---
description: Props System — built-in prop types, normalize/preprocess pipeline, meta:enum
drupal_version: "11.x"
---

# Props System

## When to Use

> Reference this guide when a prop is hidden from forms (unknown type), when choosing between `$ref` shortcuts and manual JSON Schema, or when understanding type conversion paths.

## Decision

| Prop Type ID | JSON Schema | Default Source | YAML Shortcut |
|--------------|-------------|----------------|---------------|
| `string` | `type: string` | `textfield` | `ui-patterns://string` |
| `number` | `type: [number, integer]` | `number` | `ui-patterns://number` |
| `boolean` | `type: boolean` | `checkbox` | `ui-patterns://boolean` |
| `url` | `type: string, format: iri-reference` | `url` | `ui-patterns://url` |
| `identifier` | Machine-name pattern | `textfield` | `ui-patterns://identifier` |
| `enum` | `type: [string,number,integer], enum: []` | `select` | `ui-patterns://enum` |
| `enum_list` | Array of enums | `selects` | `ui-patterns://enum_list` |
| `enum_set` | Array with `uniqueItems: true` | `checkboxes` | `ui-patterns://enum_set` |
| `links` | Array of link objects | `menu` | `ui-patterns://links` |
| `list` | Array of strings/numbers | `list_textarea` | `ui-patterns://list` |
| `attributes` | Object with pattern properties | `attributes` | `ui-patterns://attributes` |
| `variant` | String enum (auto-generated) | `select` | `ui-patterns://variant` |
| `unknown` | (fallback — hidden from forms) | — | — |

## Pattern

### Type conversion paths

```
string  <-- number, url, identifier
slot    <-- string
```

The `PropTypePluginManager` walks the shortest conversion path when a source produces a value for a non-native prop type.

### Normalize and preprocess pipeline

1. **`normalize()`** — Before SDC validation. Converts incoming values to JSON Schema-valid form (e.g., `"1"` → `true` for boolean).
2. **`preprocess()`** — After validation, before template rendering. Prepares template-friendly values (e.g., wraps HTML strings in `Markup::create()`).

### `meta:enum` for human-readable labels

```yaml
position:
  type: "string"
  "$ref": "ui-patterns://enum"
  enum: ["top", "bottom", "left", "right"]
  "meta:enum":
    top: "Top"
    bottom: "Bottom"
    left: "Left"
    right: "Right"
```

## Common Mistakes

- **Wrong**: Complex nested JSON Schema instead of `$ref` shortcuts → **Right**: Use `ui-patterns://` references; complex schemas may be marked `unknown` and hidden from forms
- **Wrong**: Expecting `unknown`-typed props to appear in forms → **Right**: Fix the JSON Schema to match a known prop type
- **Wrong**: `format: uri` for URLs → **Right**: Use `format: iri-reference`; the URL prop type matches `iri-reference`

## See Also

- [Source Plugins](source-plugins.md)
- [Defining Components](defining-components.md)
- Reference: [Prop Type Plugins](https://project.pages.drupalcode.org/ui_patterns/3-devs/2-prop-type-plugins/)
