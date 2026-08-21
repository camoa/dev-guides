---
description: "Declare icon-typed props on UI Patterns / SDC components via the icon PropType and $ref: ui-patterns://icon."
tldr: "Enable ui_icons_patterns to register the icon PropType (pack_id, icon_id, settings) and four data sources. An icon prop is plain data, not a renderable — call icon(prop.pack_id, prop.icon_id, prop.settings) in the template, or use a slot fed by icon_renderable."
drupal_version: "11.x"
---

# UI Patterns Integration

## When to Use

> Declaring icon props on UI Patterns components or SDC components used through UI Patterns.

## Pattern

Enable `ui_icons_patterns`. The submodule registers:

**PropType**: `icon` — declares an icon-typed component prop, schema `{pack_id: $ref ui-patterns://identifier, icon_id: string, settings: object}` with `pack_id` and `icon_id` required.

**Data Sources**:

| Source plugin | Serves prop types | Returns |
|---|---|---|
| `icon` | `icon` | Plain `{pack_id, icon_id, settings}` array — **not** a render array |
| `link_icon` | `icon` | Same plain array, read from a Link field's `icon` option |
| `icon_renderable` | `slot` | A ready-to-print render array (`IconDefinition::getRenderable()`) |
| `field_icon` | `icon` **and** `slot` | Plain array for an `icon` prop, render array for a slot. Derived per field: the real plugin ID is `field_icon:{entity_type}:{field_name}:ui_icon` |

**Explicit typing** — reference the PropType by `$ref` in a component definition (`*.component.yml` or pattern):

```yaml
props:
  type: object
  properties:
    leading_icon:
      title: "Leading icon"
      $ref: ui-patterns://icon
```

**Implicit typing** also works: an object prop shaped like the schema is matched to the same PropType by UI Patterns' shape matching (the plugin declares `priority: 10`):

```yaml
props:
  type: object
  properties:
    leading_icon:
      title: "Leading icon"
      type: object
      properties:
        pack_id: {type: string}
        icon_id: {type: string}
```

Either way the component editor sees an icon picker for that prop. Add an `enum` under `pack_id` to restrict which packs the prop accepts.

## Rendering an icon prop in the template

**An `icon` prop is not a render array — printing it bare renders nothing usable.** `IconSource::getPropValue()` returns the plain array `['pack_id' => …, 'icon_id' => …, 'settings' => […]]` with no `#type` key, and `IconPropType` does not override `preprocess()`, so nothing converts it on the way to Twig. `{{ leading_icon }}` hands that plain array to the renderer, which then walks `pack_id` / `icon_id` as if they were child render elements.

Render an icon prop by passing its three keys to core's `icon()` function:

```twig
{% if leading_icon %}
  {{ icon(leading_icon.pack_id, leading_icon.icon_id, leading_icon.settings) }}
{% endif %}
```

This is exactly what the submodule's own reference component does — see `modules/ui_icons_patterns/tests/modules/ui_icons_patterns_test/components/icon_test/icon_test.twig`, which declares both the explicit and the implicit prop shapes above and renders every one of them through `icon(...)`.

The source always sets a `settings` key even when the prop schema doesn't declare one, so `leading_icon.settings` is safe on both shapes.

**If you want a value you can print bare**, declare a **slot** instead of an `icon` prop and let the site builder choose the `icon_renderable` source — it is registered for `prop_types: ['slot']` and is the only source that returns `IconDefinition::getRenderable()`. Slots do print with `{{ leading_icon }}`.

## Common Mistakes

- **Wrong**: writing `type: ui:icon` → **Right**: JSON Schema has no such type keyword; use `$ref: ui-patterns://icon`
- **Wrong**: declaring a flat `type: string` prop for an icon → **Right**: an object prop with `pack_id` and `icon_id` keeps the picker; a flat string loses it
- **Wrong**: printing an icon prop bare as `{{ leading_icon }}` → **Right**: it is plain data, not a renderable. Call `icon(prop.pack_id, prop.icon_id, prop.settings)`, or make the prop a slot fed by `icon_renderable`
- **Wrong**: hardcoding rendered SVG in the component template → **Right**: use the picker; hardcoding bypasses settings, cache metadata, and a11y templating

## See Also

- [Field API Integration](field-api.md)
- [Twig Rendering](twig.md)
- Reference: `modules/ui_icons_patterns/src/Plugin/UiPatterns/PropType/IconPropType.php`
- Reference: `modules/ui_icons_patterns/src/Plugin/UiPatterns/Source/IconSource.php`
- Reference: `modules/ui_icons_patterns/tests/modules/ui_icons_patterns_test/components/icon_test/icon_test.twig`
- [UI Patterns guide](../ui-patterns/index.md)
