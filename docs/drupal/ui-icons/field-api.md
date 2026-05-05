---
description: Expose a UI Icons picker on a Drupal field for content types, paragraphs, or any fieldable entity.
tldr: Enable ui_icons_field and add an Icon field (type ui_icon) to the bundle; the widget stores pack:icon_id plus settings. Also enhances the core Link field with icon_link_widget and icon_link_formatter for icon+link combos.
drupal_version: "11.x"
---

# Field API Integration

## When to Use

> Exposing an icon picker on a content type, taxonomy term, paragraph, or any fieldable entity.

## Pattern

Enable `ui_icons_field`. Add a field of type **Icon** to the bundle.

| Field type | Widget | Formatter | Storage |
|---|---|---|---|
| `ui_icon` | `icon_widget` | `icon_formatter` | varchar(128) holding `pack:icon_id` |

Field settings include `allowed_icon_pack` (array) — restrict the picker to specific packs.

Storage format (example field value):

```yaml
field_icon:
  - value: "my_theme_icons:arrow-left"
    settings:
      size: 32
      color: "#0066cc"
      decorative: false
```

## Pattern: Link field enhancement

UI Icons also enhances the core Link field:

| Widget | Use |
|---|---|
| `icon_link_widget` | Adds icon picker before/after URL + title |
| `icon_link_attributes_widget` | Same plus integration with `link_attributes` module |

| Formatter | Use |
|---|---|
| `icon_link_formatter` | Renders `[icon] link text` or `link text [icon]` |

Sub-submodules for Link combinations:
- `ui_icons_field_link_attributes` — Link + Link Attributes module
- `ui_icons_field_linkit` — Link + Linkit
- `ui_icons_field_linkit_attributes` — all three

## Common Mistakes

- **Wrong**: restricting `allowed_icon_pack` to a pack that's later disabled → **Right**: orphaned field values result; audit before disabling packs in production
- **Wrong**: using a regular Link field where editors need icons → **Right**: switch to `icon_link_widget` instead of building a custom field

## See Also

- [Overview](overview.md)
- [CKEditor 5 Integration](ckeditor5.md)
- [UI Patterns Integration](patterns.md)
- Reference: `modules/ui_icons_field/`
