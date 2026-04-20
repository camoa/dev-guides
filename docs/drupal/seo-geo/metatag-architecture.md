---
description: Metatag 2.2.0 module architecture — 11 submodules, attribute-based plugins, cascading inheritance, and token system overview
tldr: "You are setting up meta tags on a Drupal 11 site. Start here to understand how the Metatag module is structured before configuring individual tags or submodules."
drupal_version: "11.x"
---

# Metatag Architecture

## When to Use

> You are setting up meta tags on a Drupal 11 site. Start here to understand how the Metatag module is structured before configuring individual tags or submodules. The cascading inheritance model determines where you configure defaults vs. per-content-type vs. per-entity overrides.

## Decision

| If you need... | Configure at... | Why |
|----------------|-----------------|-----|
| Site-wide defaults for all pages | Global group | Lowest specificity — catches everything not overridden |
| Tags specific to the front page | Front page group | Front page has distinct SEO needs (brand name in title) |
| Different tags per content type | Content type group | Article vs. Landing Page have different description needs |
| Tags for taxonomy terms | Vocabulary group | Term pages need their own title/description patterns |
| One-off override on a specific node | Entity-level metatag field | Highest specificity — overrides all groups |
| Custom meta tag not in core Metatag | Custom plugin | Attribute-based plugin API in 2.2.0 |

## Pattern

Metatag 2.2.0 uses a PHP attribute on plugin classes. Each submodule adds a group of related tags.

```php
// Plugin class — attribute-based in 2.2.0+
#[MetatagTag(
  id: "og_title",
  label: new TranslatableMarkup("Open Graph Title"),
  description: new TranslatableMarkup("..."),
  name: "og:title",
  group: "open_graph",
  weight: 1,
)]
class OgTitle extends MetaNameBase { }
```

Admin path: `/admin/config/search/metatag`

## Submodule Reference

| Submodule | Machine name | Tags provided |
|-----------|-------------|---------------|
| Core (required) | `metatag` | Title, description, abstract, keywords, robots, canonical, shortlink |
| Open Graph | `metatag_open_graph` | og:title, og:description, og:image, og:url, og:type, og:site_name |
| Twitter Cards | `metatag_twitter_cards` | twitter:card, twitter:title, twitter:description, twitter:image, twitter:site |
| hreflang | `metatag_hreflang` | hreflang for each active language + x-default |
| Dublin Core | `metatag_dc` | dc.title, dc.description, dc.creator, dc.date |
| Dublin Core Advanced | `metatag_dc_advanced` | dc.type, dc.format, dc.publisher, dc.rights |
| Facebook | `metatag_facebook` | fb:admins, fb:app_id |
| Google+ (legacy) | `metatag_google_plus` | itemtype, itemprop — rarely used now |
| Verification | `metatag_verification` | google-site-verification, msvalidate |
| App Links | `metatag_app_links` | App store deep linking |
| Mobile & UI Adjustments | `metatag_mobile` | viewport, theme-color, apple-mobile-web-app-* |

Enable only submodules you use — each adds database weight and query overhead.

## Cascading Inheritance

```
Global defaults
    └── Content type defaults (overrides Global)
            └── Vocabulary defaults (overrides Global)
                    └── Per-entity override (overrides everything)
```

Metatag resolves the most-specific value for each tag. An empty field at the entity level falls back to the content type, which falls back to Global. A value of `[node:field_meta_description]` stays empty (and falls back) when that field has no value on the node.

## Token System

Metatag depends on the Token module. All fields accept token syntax:

| Token | Resolves to |
|-------|-------------|
| `[node:title]` | Node title |
| `[node:field_summary]` | Summary field value |
| `[node:created:html_date]` | ISO 8601 creation date |
| `[site:name]` | Site name from config |
| `[site:url]` | Site base URL |
| `[current-page:url]` | Current page canonical URL |
| `[node:field_image:entity:url]` | Image field file URL |

Browse available tokens at `/admin/help/token` (requires Token UI submodule) or at the bottom of any Metatag configuration form.

## Common Mistakes

- **Wrong**: Enabling all 11 submodules on install → **Right**: Enable only submodules you will actively configure; unused submodules add noise to the admin UI and database
- **Wrong**: Leaving the Global group empty → **Right**: Set Global defaults first — every page gets fallback values before content-type overrides apply
- **Wrong**: Hardcoding values like `My Site - [node:title]` in title fields → **Right**: Use tokens throughout so values update automatically when content changes
- **Wrong**: Skipping the Token module → **Right**: Token is a required dependency; Metatag will not function without it
- **Wrong**: Expecting entity-level fields to appear on content types by default → **Right**: Add the Metatag field to each content type's form display at `/admin/structure/types/manage/{type}/form-display`

## See Also

- [Core Meta Tags](core-meta-tags.md) — configure title, description, canonical using this architecture
- [Open Graph](open-graph.md) — metatag_open_graph submodule in detail
- [Twitter Cards](twitter-cards.md) — metatag_twitter_cards submodule in detail
- [Metatag for Multilingual](metatag-multilingual.md) — metatag_hreflang submodule
- Reference: [Metatag module on drupal.org](https://www.drupal.org/project/metatag)
- Reference: [Token module on drupal.org](https://www.drupal.org/project/token)
