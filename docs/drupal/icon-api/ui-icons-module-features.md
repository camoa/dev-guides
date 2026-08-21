---
description: "UI Icons contrib submodules for fields, menus, and CKEditor — there is no separate Link submodule, and Iconify is not part of UI Icons"
tldr: "You need icon fields, menu icons, or CKEditor embedding beyond core rendering; link-field icons ship from ui_icons_field (no separate Link submodule), and ui_icons_ckeditor5 needs ui_icons_text to actually render the embed."
drupal_version: "11.x"
---

# UI Icons Module Features

## When to Use

You need icon integration beyond rendering in templates: icon field types, menu icons, CKEditor embedding, or icon browsing UI for content editors. UI Icons is a contrib module that extends core Icon API functionality.

## Decision

| Feature | Submodule (machine name) | Use when... |
|---|---|---|
| Icon field type | `ui_icons_field` | Storing icons in entities (nodes, paragraphs, taxonomy) |
| Link field icons | `ui_icons_field` | Same submodule — it ships `IconLinkWidget` and `IconLinkFormatter`; there is no separate "UI Icons Link" |
| Menu icons | `ui_icons_menu` | Displaying icons in navigation menus |
| CKEditor 5 embedding | `ui_icons_ckeditor5` (plugin + dialog) plus `ui_icons_text` (the `icon_embed` text filter that renders it) | Inserting icons in WYSIWYG content |
| Media type | `ui_icons_media` | Managing icons as media entities |
| Icon browser UI | `ui_icons_library` | Content editors need to browse available icons |
| Icon picker widget | `ui_icons_picker` | Advanced autocomplete/visual icon selection |
| UI Patterns integration | `ui_icons_patterns` | Icon prop type and data sources for UI Patterns 2 |
| Font extractor | `ui_icons_font` | See [Font Extractor](font-extractor.md) |

Iconify is **not** a UI Icons submodule. `ui_icons_iconify_api` is a deprecated empty placeholder pointing at the standalone `drupal/iconify_icons`, which is what provides the `iconify` extractor plugin.

## Pattern

**Installation:**

```bash
composer require 'drupal/ui_icons:^2.0'   # ^1.1 on core 11.1/11.2
drush en ui_icons ui_icons_field ui_icons_menu
```

**Icon field** on content type:

```yaml
# Via UI: Structure > Content types > [Type] > Manage fields
# Add field of type "Icon"
field.field.node.article.field_icon:
  field_name: field_icon
  entity_type: node
  bundle: article
  field_type: icon
  settings:
    allowed_icon_pack:  # Limit available packs; empty means "all"
      my_theme: my_theme
      bootstrap_icons: bootstrap_icons
```

**Field formatter** rendering. The field stores a single property, `target_id`, holding the full `pack_id:icon_id` string (`IconType::propertyDefinitions()`, `varchar_ascii(128)`, indexed). There is no `pack_id` or `icon_id` property on the field item, so splitting it yourself means splitting `target_id`:

```twig
{# Preferred: let the formatter render it #}
{{ content.field_icon }}

{# Manual access, if you need to override the settings #}
{% if node.field_icon.target_id %}
  {% set parts = node.field_icon.target_id|split(':', 2) %}
  {{ icon(parts[0], parts[1], {size: 32}) }}
{% endif %}
```

**Menu icons** (via UI Icons Menu submodule):

```
# Configuration available at:
# Structure > Menus > [Menu] > Edit link
# Icon picker appears in link edit form
```

**Icon library browser** (via UI Icons Library submodule):

```
# Access at: /admin/appearance/ui/icons  (per-pack: /admin/appearance/ui/icons/{pack_id})
# Provides documentation page showing all available icons
# Useful for editors and stakeholders to browse icon packs
```

Reference: [UI Icons module page](https://www.drupal.org/project/ui_icons)

## Common Mistakes

- **Wrong**: Installing UI Icons without enabling needed submodules → **Right**: Core module alone doesn't add field/menu features
- **Wrong**: Enabling `ui_icons_ckeditor5` without `ui_icons_text` → **Right**: The editor inserts the markup but no text filter renders it
- **Wrong**: Expecting core Icon API to include field types → **Right**: Fields, widgets, formatters are UI Icons contrib
- **Wrong**: Reading `field_icon.pack_id` in Twig → **Right**: The property is `target_id` and it holds `pack:id` as one string
- **Wrong**: `ui_icons_ckeditor5` + `ckeditor5_icons` conflict → **Right**: Both provide CKEditor icon integration, choose one
- **Wrong**: Not limiting icon packs in field config → **Right**: Users see all packs, can cause overwhelming UI
- **Wrong**: Forgetting to clear cache after enabling submodules → **Right**: Icon picker widgets won't appear

## See Also

- [Font Extractor](font-extractor.md)
- [Template Variables](template-variables.md)
- Reference: [UI Icons documentation site](https://project.pages.drupalcode.org/ui_icons/)
- Reference: [UI Icons module on Drupal.org](https://www.drupal.org/project/ui_icons)
