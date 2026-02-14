---
description: Icon integration beyond rendering - field types, menu icons, CKEditor embedding, and browsing UI for content editors
drupal_version: "11.x"
---

# UI Icons Module Features

## When to Use

You need icon integration beyond rendering in templates: icon field types, menu icons, CKEditor embedding, or icon browsing UI for content editors. UI Icons is a contrib module that extends core Icon API functionality.

## Decision

| Feature | Submodule | Use when... |
|---|---|---|
| Icon field type | UI Icons Field | Storing icons in entities (nodes, paragraphs, taxonomy) |
| Link field icons | UI Icons Link | Adding icons to link fields with formatter |
| Menu icons | UI Icons Menu | Displaying icons in navigation menus |
| CKEditor5 embedding | UI Icons CKEditor | Inserting icons in WYSIWYG content |
| Media type | UI Icons Media | Managing icons as media entities |
| Icon browser UI | UI Icons Library | Content editors need to browse available icons |
| Icon picker widget | UI Icons Picker | Advanced autocomplete/visual icon selection |

## Pattern

**Installation:**

```bash
composer require 'drupal/ui_icons:^1.1'
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
    icon_packs:  # Limit available packs
      - my_theme
      - bootstrap_icons
```

**Field formatter** rendering:

```twig
{# Automatic rendering via field formatter #}
{{ content.field_icon }}

{# Manual access to field value #}
{% if node.field_icon.pack_id and node.field_icon.icon_id %}
  {{ icon(node.field_icon.pack_id, node.field_icon.icon_id, {size: 32}) }}
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
# Access at: /admin/appearance/ui-libraries
# Provides documentation page showing all available icons
# Useful for editors and stakeholders to browse icon packs
```

Reference: [UI Icons module page](https://www.drupal.org/project/ui_icons)

## Common Mistakes

- **Wrong**: Installing UI Icons without enabling needed submodules → **Right**: Core module alone doesn't add field/menu features
- **Wrong**: Expecting core Icon API to include field types → **Right**: Fields, widgets, formatters are UI Icons contrib
- **Wrong**: UI Icons CKEditor + ckeditor5_icons conflict → **Right**: Both modules try to provide CKEditor icon integration, choose one
- **Wrong**: Not limiting icon packs in field config → **Right**: Users see all packs, can cause overwhelming UI
- **Wrong**: Forgetting to clear cache after enabling submodules → **Right**: Icon picker widgets won't appear

## See Also

- [Font Extractor](font-extractor.md)
- [Template Variables](template-variables.md)
- Reference: [UI Icons documentation site](https://project.pages.drupalcode.org/ui_icons/)
- Reference: [UI Icons module on Drupal.org](https://www.drupal.org/project/ui_icons)
