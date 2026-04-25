---
description: Configure metatag defaults per content type bundle — not globally — so each bundle uses the right field tokens for title, description, and OG image.
drupal_version: "11.x"
tldr: Configure metatag defaults per content type, not globally. Each bundle has different fields for title, description, and OG image. The base node config provides a `[node:title]` fallback.
---

# Metatag Per Bundle

**What:** Configure metatag defaults per content type, not globally. Each bundle has different fields for title, description, and OG image. The base node config provides a `[node:title]` fallback.

**Rationale:** Different content types have different "best metatag source." Articles have a body summary field; events have a date + location field; products have SKU + price. A global metatag default has to use generic tokens that produce mediocre meta descriptions across the board. Per-bundle defaults can use the right field for each type, producing accurate, useful meta tags that improve SEO and social-share rendering.

**When it applies:** Any site with more than one content type that's publicly visible. The exception is sites where every content type is structurally identical (rare).

**Example:**

```yaml
# config/sync/metatag.metatag_defaults.global.yml
id: global
label: Global
tags:
  title: '[current-page:title] | [site:name]'
  description: '[site:slogan]'

# config/sync/metatag.metatag_defaults.node__article.yml
id: node__article
label: 'Content: Article'
tags:
  title: '[node:title] | [site:name]'
  description: '[node:summary]'              # uses summary field
  og_image: '[node:field_hero_image:entity:field_media_image]'

# config/sync/metatag.metatag_defaults.node__event.yml
id: node__event
label: 'Content: Event'
tags:
  title: '[node:title] — [node:field_event_date:value:short] | [site:name]'
  description: '[node:field_short_description]'
  og_image: '[node:field_event_poster:entity:field_media_image]'
```
