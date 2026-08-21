---
description: "Wire an icon picker onto fields, and make icon props editable in Drupal Canvas — target_id verified on 1.1.2, Canvas claims unread."
tldr: "Enable ui_icons_field and add a ui_icon field; the widget stores pack_id:icon_id in target_id (verified on 1.1.2). mainPropertyName/ICON_ID_PCRE and the whole ui_icons_canvas subsection are unverified 2.0.0-only claims."
drupal_version: "11.x"
---

# Field API Integration

## When to Use

> Exposing an icon picker on a content type, taxonomy term, paragraph, or any fieldable entity.

## Pattern

Enable `ui_icons_field`. Add a field of type **Icon** to the bundle.

| Field type | Widget | Formatter | Storage |
|---|---|---|---|
| `ui_icon` | `icon_widget` | `icon_formatter` | one `target_id` column, `varchar_ascii(128)`, `not null`, indexed |

Field settings include `allowed_icon_pack` (array) — restrict the picker to specific packs.

## Storage Format

The column is named **`target_id`**, not `value`, and it is the field's main property (`IconType::mainPropertyName()`). It holds the full `pack_id:icon_id` string and carries a `Regex` constraint, `IconType::ICON_ID_PCRE` = `/^[a-z0-9_]+:.+$/`.

> **The `target_id` column is verified on 1.1.2; the main-property and constraint claims are not.**
> `IconType::schema()` really does declare a single `target_id` column (`varchar_ascii(128)`,
> `not null`, indexed) on 1.1.2. But that version's `IconType` declares **neither**
> `mainPropertyName()` **nor** `ICON_ID_PCRE`, and no `Regex` constraint anywhere — so on 1.x the
> inherited `FieldItemBase::mainPropertyName()` still answers `value`, naming a property the field
> does not define, and nothing validates the stored string's shape. Both are plausible 2.0.0
> additions and both are unread. If you are writing code that depends on either, check your own
> `IconType.php` first.

```yaml
# Example field value (single column)
field_icon:
  - target_id: "my_theme_icons:arrow-left"
```

**There is no per-value settings storage.** Size, color, and the rest are not saved alongside each icon — they are configured once on the display, in `icon_formatter`'s `icon_settings` setting, and applied to every value the formatter renders. If editors need per-value control, expose those choices as separate fields; the icon field cannot carry them.

## Pattern: Drupal Canvas (`ui_icons_canvas`)

Enable `ui_icons_canvas` to make icons editable inside the Drupal Canvas builder. It wires two things:

- **The field widget.** A client-side transform `uiIcon` is registered on `icon_widget`. Canvas throws a `LogicException` for any widget without transform metadata, and the stock `mainProperty` transform is not enough here because both selectors (`icon_autocomplete`, and `icon_picker` which extends it) nest their output under `value[icon_id]`.
- **SDC props.** Any SDC **string** prop tagged `x-canvas-prop: ui-icon` is routed to the `ui_icon` field's `target_id` property and edited with `icon_widget`:

```yaml
# my_component.component.yml
props:
  type: object
  properties:
    icon:
      type: string
      title: "Icon"
      pattern: '^[a-z0-9_]+:.+$'
      x-canvas-prop: ui-icon
```

The `pattern` matters: Canvas's shape matcher compares the field's `Regex` constraint against the pattern derived from the prop's JSON Schema **by value**, so it must be exactly `^[a-z0-9_]+:.+$` or the prop will not match the icon field.

> **This whole subsection is unverified, and the installed Canvas does not recognise
> `x-canvas-prop`.** `ui_icons_canvas` does not exist in UI Icons 1.1.2, so nothing here could be
> read first-hand. Checking the other half — Canvas **1.10.1** on the reference site — the string
> `x-canvas-prop` appears nowhere in the module. The schema-extension keywords Canvas 1.10.1 does
> honour are `x-formatting-context`, `x-translation-context`, `x-allowed-schemes` and
> `x-required-variables`. Two supporting mechanisms *are* real: `hook_canvas_storable_prop_shape_alter`
> is declared in `canvas.api.php`, and `JsonSchemaType` really does turn a JSON-Schema `pattern`
> into a `Regex` shape requirement — so a `pattern`-driven match is the plausible route. The
> `x-canvas-prop: ui-icon` key itself needs confirmation against UI Icons 2.0.0 plus the Canvas
> release it targets before anyone writes a `.component.yml` around it.

## Decision: Link Field Enhancement

UI Icons also enhances the core Link field:

| Widget | Use |
|---|---|
| `icon_link_widget` | Adds icon picker before/after URL + title |
| `icon_link_attributes_widget` | Same plus integration with `link_attributes` module |

| Formatter | Use |
|---|---|
| `icon_link_formatter` | Renders `[icon] link text` or `link text [icon]` |

Integration sub-submodules: `ui_icons_field_link_attributes` (Link + Link Attributes), `ui_icons_field_linkit` (Link + Linkit), `ui_icons_field_linkit_attributes` (all three).

## Common Mistakes

- **Wrong**: restricting `allowed_icon_pack` to a pack that's later disabled → **Right**: audit before disabling packs in production; field values reference the pack ID and become orphaned otherwise
- **Wrong**: using a regular Link field where editors need icons → **Right**: switch to `icon_link_widget` instead of building a custom field
- **Wrong**: writing `value` when setting the field programmatically or in a migration → **Right**: the column is `target_id`; a `value` key is ignored and the save produces an empty icon
- **Wrong**: expecting per-icon settings to persist → **Right**: they live on the formatter, so every value in the field renders at the same size and color
- **Wrong**: relying on `IconType::mainPropertyName()` or `ICON_ID_PCRE` on a 1.x site → **Right**: neither exists on 1.1.2; `mainPropertyName()` falls back to `value` there and nothing validates the stored string
- **Wrong**: writing a `.component.yml` around `x-canvas-prop: ui-icon` against an installed Canvas without checking its version → **Right**: Canvas 1.10.1 does not recognize that keyword at all; confirm against the actual Canvas release before relying on it

## See Also

- [UI Patterns Integration](patterns.md)
- [Settings & Rendering](settings-rendering.md)
- Reference: `modules/ui_icons_field/src/Plugin/Field/FieldType/IconType.php`
- Reference: `modules/ui_icons_canvas/src/Hook/UiIconsCanvasHooks.php`
