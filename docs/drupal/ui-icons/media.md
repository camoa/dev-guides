---
description: Store UI icon references as Drupal media entities using the Icon media source plugin.
tldr: Enable ui_icons_media and create a media type with source plugin Icon to treat icons as reusable media library assets. Use this only when true cross-page reuse is needed; for per-entity icons or inline CKEditor icons the Field API and CKEditor integrations are simpler.
drupal_version: "11.x"
---

# Media Integration

## When to Use

> Storing icon references as media entities so they can be browsed in the media library and reused across the site.

## Decision

| Want | Use |
|---|---|
| Icons as a "library" reused across pages | Media + Icon source (this guide) |
| Inline icons in content body | [CKEditor 5 integration](ckeditor5.md) |
| Per-entity icon field | [Field API integration](field-api.md) |

## Pattern

Enable `ui_icons_media`. Create a new media type with source plugin **Icon**. Each media entity stores one `pack_id:icon_id` plus optional settings and can be browsed in the standard media library.

## Common Mistakes

- **Wrong**: creating Icon media entities for every individual icon use → **Right**: the Field API and CKEditor integrations are simpler when cross-page reuse isn't needed; reserve the media approach for a shared icon library

## See Also

- [Field API Integration](field-api.md)
- [CKEditor 5 Integration](ckeditor5.md)
- Reference: `modules/ui_icons_media/`
