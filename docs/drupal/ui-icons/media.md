---
description: "Store icon references as media entities for cross-page reuse via the ui_icons_media source plugin."
tldr: "Enable ui_icons_media and create a media type with source plugin Icon; each entity stores pack_id:icon_id plus optional settings. Use Field API or CKEditor integrations instead when reuse across pages isn't needed."
drupal_version: "11.x"
---

# Media Integration

## When to Use

> Storing icon references as media entities so they can be browsed in the media library, reused, and have their own metadata.

## Pattern

Enable `ui_icons_media`. Create a new media type with source plugin **Icon**. Each media entity stores one `pack_id:icon_id` plus optional settings.

## Decision

| Want | Use |
|---|---|
| Icons as a "library" reused across pages | Media + Icon source |
| Icons inline in content body | [CKEditor 5 Integration](ckeditor5.md) |
| Icons as a per-entity field | [Field API Integration](field-api.md) |

## Common Mistakes

- **Wrong**: creating Icon media entities for every icon use → **Right**: use the Field API or CKEditor integrations when reuse isn't needed; they're simpler

## See Also

- [Field API Integration](field-api.md)
- [CKEditor 5 Integration](ckeditor5.md)
