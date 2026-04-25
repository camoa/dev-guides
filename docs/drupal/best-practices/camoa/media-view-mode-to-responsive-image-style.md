---
description: Never use the default media view mode for content display — create purpose-specific view modes that use responsive image formatters.
drupal_version: "11.x"
tldr: Never use the `default` media view mode for content display. Create purpose-specific view modes that use responsive image formatters. The chain is: Media View Mode → Responsive Image Formatter → Responsive Image Style → Breakpoint-specific Image Styles → `<picture>` or `srcset`.
---

# Media View Mode → Responsive Image Style

**What:** Never use the `default` media view mode for content display. Create purpose-specific view modes that use responsive image formatters. The chain is: Media View Mode → Responsive Image Formatter → Responsive Image Style → Breakpoint-specific Image Styles → `<picture>` or `srcset`.

**Rationale:** The `default` view mode is a Drupal admin/fallback display, not a content-rendering target. Using it forces every place that renders the media to share one formatter, blocking per-context responsive image control. Purpose-specific view modes let each context (card, hero, gallery thumbnail) pick its own responsive image style.

**When it applies:** Every place media is rendered for end users — node templates, view rows, paragraph displays, entity reference field formatters.

**Example:**

```yaml
# Wrong — uses default view mode for content
core.entity_view_display.node.article.default.yml
  field_image:
    type: media_thumbnail
    settings:
      view_mode: default

# Right — purpose-specific view mode chain
core.entity_view_mode.media.card_thumbnail.yml         # the view mode
core.entity_view_display.media.image.card_thumbnail.yml  # uses responsive formatter
  field_media_image:
    type: responsive_image
    settings:
      responsive_image_style: card_thumbnail
core.entity_view_display.node.article.default.yml
  field_image:
    type: entity_reference_entity_view
    settings:
      view_mode: card_thumbnail
```
