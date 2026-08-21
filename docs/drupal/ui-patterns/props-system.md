---
description: Prop types — built-in types, JSON Schema compatibility, and normalize/preprocess pipeline
tldr: "Prop types — built-in types, JSON Schema compatibility, and normalize/preprocess pipeline"
drupal_version: "11.x"
---

# Props System

## How Prop Types Work

Prop type plugins are intermediaries between component JSON Schema definitions and source plugins. Each prop in a component definition is annotated with a `PropTypeInterface` instance during discovery. The `PropTypePluginManager` determines the prop type by checking JSON Schema compatibility:

1. If the prop uses a `$ref` with `ui-patterns://` prefix, the prop type is resolved directly (e.g., `ui-patterns://boolean` maps to the `boolean` prop type).
2. Otherwise, all prop type definitions are checked via `CompatibilityChecker::isCompatible()`, sorted by priority.
3. If no match is found, the `unknown` fallback type is used (which hides the prop from forms).

## Built-in Prop Types

| Prop Type ID | JSON Schema | Default Source | Converts From | YAML Shortcut |
|---|---|---|---|---|
| `string` | `type: string` | `textfield` | number, url, identifier | `ui-patterns://string` |
| `number` | `type: [number, integer]` | `number` | -- | `ui-patterns://number` |
| `boolean` | `type: boolean` | `checkbox` | -- | `ui-patterns://boolean` |
| `url` | `type: string, format: iri-reference` | `url` | -- | `ui-patterns://url` |
| `identifier` | Machine-name pattern | `textfield` | string | `ui-patterns://identifier` |
| `enum` | `type: [string,number,integer], enum: []` | `select` | -- | `ui-patterns://enum` |
| `enum_list` | Array of enums | `selects` | -- | `ui-patterns://enum_list` |
| `enum_set` | Array with `uniqueItems: true` | `checkboxes` | -- | `ui-patterns://enum_set` |
| `links` | Array of link objects | `menu` | -- | `ui-patterns://links` |
| `list` | Array of strings/numbers | `list_textarea` | -- | `ui-patterns://list` |
| `attributes` | Object with pattern properties | `attributes` | -- | `ui-patterns://attributes` |
| `variant` | String enum (auto-generated) | `select` | string | `ui-patterns://variant` |
| `slot` | (internal) | `component` | string | -- |
| `unknown` | (fallback) | -- | -- | -- |

## Type Conversion

Prop types declare `convert_from` in their attribute, enabling automatic value conversion between compatible types:

```
string     <- number, url, identifier
slot       <- string
identifier <- string
variant    <- string
```

Those four are the complete set — only `StringPropType`, `SlotPropType`, `IdentifierPropType` and `VariantPropType` declare `convert_from`. Every other prop type accepts only its native sources.

The `PropTypePluginManager` builds a directed graph of conversion paths. When a source produces a value for a prop type it does not natively support, the system walks the shortest conversion path. For example, a URL source can provide a value for a string prop because `string` declares `convert_from: ['url']`, and a `textfield` or `token` source can fill an `identifier` or `variant` prop for the same reason.

One exception to watch: conversion deliberately skips sources tagged `widget:dismissible` (`path`, `url`, `number`, `attributes`, `list_textarea`). `SourcePluginManager::getConvertibleDefinitionsPerPropertyId()` forces `["widget:dismissible" => FALSE]` into the tag filter, so `path` never appears as a converted source for a `string` prop even though `string` converts from `url`.

## Normalize and Preprocess Pipeline

Each prop type implements two processing stages:

1. **`normalize()`** -- Runs before SDC validation. Converts incoming values to JSON Schema-valid form (e.g., `StringPropType::normalize()` renders render arrays to strings; `BooleanPropType::normalize()` converts `"1"` to `true`).
2. **`preprocess()`** -- Runs after validation, before template rendering. Prepares template-friendly values. Only `AttributesPropType` and `LinksPropType` override it; `PropTypePluginBase::preprocess()` returns the value unchanged, so most prop types do nothing at this stage.

`StringPropType::normalize()` is where the escaping decision is made, and it changed after 2.0.15 (issue #3611167, "Escape at render, not in sources"). Trust now follows the PHP type of the value, not the prop's `contentMediaType`:

- `contentMediaType: text/plain` -> `strip_tags()`, always, even on a `Markup` value.
- A `MarkupInterface` value (`Markup::create()`, `TranslatableMarkup`) is passed through untouched and stays trusted.
- A renderable or render array is rendered through Drupal's render pipeline and the result is wrapped in `Markup::create()`.
- A **plain PHP string is left as a plain string** and Twig autoescapes it at render time.

That last rule is the one to internalise: as of 2.0.19 a plain string prop no longer emits raw HTML. To pass raw HTML through a string prop, the source must hand over a `Markup` object. In 2.0.15, `StringPropType::preprocess()` wrapped every non-`text/plain` string in `Markup::create()`; that override is gone.

## The `meta:enum` Extension

Non-standard but supported by UI Patterns, `meta:enum` provides human-readable labels for enum values in forms:

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

| Mistake | Why It Is Wrong |
|---|---|
| Creating complex nested JSON Schema instead of using `$ref` shortcuts | UI Patterns may not recognize complex schemas and mark them as `unknown` type, hiding the prop from forms entirely. Use `ui-patterns://` references. |
| Expecting unknown-typed props to appear in forms | Props with `unknown` type get zero source plugins and are hidden. Fix the JSON Schema to match a known prop type. |
| Assuming all prop types are interchangeable | Conversion paths are directional. A string source works for slots (string -> slot), but a slot source never works for string props. |
| Putting `format: uri` instead of `format: iri-reference` | The URL prop type matches `iri-reference` (supports internationalized URLs). Using `uri` may fall back to a plain string type. |

## See Also

- [Source Plugins](source-plugins.md)
- [Defining Components](defining-components.md)