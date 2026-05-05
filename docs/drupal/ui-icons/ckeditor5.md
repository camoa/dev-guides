---
description: Embed UI Icons inline in CKEditor 5 body text using the drupal-icon tag and icon_embed filter.
tldr: Enable ui_icons_ckeditor5 and ui_icons_text, then add the Icon toolbar button and Embed icon filter to each text format. Authors get a modal picker; output is a drupal-icon tag transformed at render time. Enabling the toolbar button without the filter leaves the raw tag in output.
drupal_version: "11.x"
---

# CKEditor 5 Integration

## When to Use

> Letting authors embed icons inline in body text without writing markup.

## Decision

| Need | Approach |
|---|---|
| Inline icons in body text | `<drupal-icon>` filter (this guide) |
| Icons as a separate field | `ui_icon` field type ([Field API](field-api.md)) |
| Both | Both — they're independent integrations |

## Pattern

Enable `ui_icons_ckeditor5` and `ui_icons_text`.

For each text format that should support icons:

1. **Configuration → Text formats and editors → {format} → Configure**
2. **Toolbar**: drag the **Icon** button to the active toolbar
3. **Filters**: enable **"Embed icon"**
4. Save

The Icon button opens a modal picker. On save, an `<drupal-icon>` tag is inserted:

```html
<drupal-icon
  data-icon-id="my_theme_icons:check"
  data-icon-settings='{"size":18,"color":"#0a0"}'
></drupal-icon>
```

The `icon_embed` text filter transforms the tag at render time using the pack's template.

## Common Mistakes

- **Wrong**: enabling the toolbar button without enabling the filter → **Right**: `<drupal-icon>` shows up as raw text in output
- **Wrong**: incorrect filter order — HTML restriction filter runs before Embed icon → **Right**: ensure `Embed icon` runs before any filter that strips `data-icon-*` attributes
- **Wrong**: not restricting allowed packs in the filter settings → **Right**: configure allowed_icon_pack in the filter to limit picker scope

## See Also

- [Overview](overview.md)
- [Field API Integration](field-api.md)
- Reference: `modules/ui_icons_ckeditor5/`, `modules/ui_icons_text/src/Plugin/Filter/IconEmbed.php`
