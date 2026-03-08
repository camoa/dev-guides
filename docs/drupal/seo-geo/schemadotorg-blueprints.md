---
description: Schema.org Blueprints (schemadotorg) — schema-first content modeling for Drupal, drush commands, submodules, and alpha stability guidance
drupal_version: "11.x"
---

# Schema.org Blueprints

## When to Use

> Schema.org Blueprints inverts the normal Drupal workflow: instead of creating content types and then mapping them to Schema.org, you declare a Schema.org type and the module generates the Drupal content type, fields, and JSON-LD output automatically. This is a greenfield architectural choice — use it when starting a new project that needs deep schema alignment, decoupled API output with schema-consistent field names, or automated JSON-LD without token mapping. Do not introduce it mid-project on established content models.

## Decision

| Situation | Use Schema.org Blueprints? | Alternative |
|-----------|---------------------------|-------------|
| Greenfield build, schema alignment from day one | Yes | — |
| Decoupled/headless Drupal needing schema-aligned JSON | Yes | — |
| Existing site with established content types | No | Schema Metatag for token-mapped JSON-LD |
| Need production-stable module now | No | Schema Metatag 3.0.4 (stable) |
| Small site, 1-3 content types | No | Schema Metatag is simpler |
| Complex schema hierarchy, 10+ content types | Yes | — |
| Team comfortable with alpha modules | Yes, with monitoring | — |
| Client project with strict stability requirements | No | Schema Metatag |

### Stability Warning

Schema.org Blueprints is at **1.0.0-alpha37** (March 2026) with approximately 210 installs. Alpha status means:

- API changes between releases without deprecation periods
- Database schema migrations may be required on update
- Not covered by Drupal's security advisory policy until stable release
- Active development; issue queue moves quickly

Monitor the [project page](https://www.drupal.org/project/schemadotorg) and changelog before any update in production.

## Pattern

### Install

```bash
composer require drupal/schemadotorg
drush en schemadotorg schemadotorg_jsonld
drush cr
```

Enable additional submodules based on your use case (see Submodules table below).

### Create Content Types from Schema.org Definitions

```bash
# Create a node type mapped to Schema.org Article
drush schemadotorg:create-type node:Article

# Create an Event content type
drush schemadotorg:create-type node:Event

# Create a Product content type
drush schemadotorg:create-type node:Product

# Create a Person content type (for author profiles)
drush schemadotorg:create-type node:Person

# Preview what fields will be created (dry run)
drush schemadotorg:create-type node:Article --dry-run
```

These commands generate the content type with field machine names derived from Schema.org property names (e.g., `field_schema_date_published`, `field_schema_author`).

### Automatic JSON-LD

With `schemadotorg_jsonld` enabled, JSON-LD is output automatically for any entity mapped to a Schema.org type. No token mapping required:

```html
<!-- Output on /node/42 (Article type) -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "My Article",
  "datePublished": "2026-03-01T10:00:00+00:00",
  "author": { "@type": "Person", "name": "Editor Name" },
  "image": { "@type": "ImageObject", "url": "https://..." }
}
</script>
```

### Key Submodules

50+ submodules are available. Core workflow:

| Submodule | Purpose | Enable? |
|-----------|---------|---------|
| schemadotorg | Core — type mapping and field generation | Always |
| schemadotorg_jsonld | Automatic JSON-LD output | Always |
| schemadotorg_ui | Admin UI for type management | Recommended |
| schemadotorg_report | Reports on mapped types and properties | Recommended |
| schemadotorg_descriptions | Schema.org descriptions on fields | Recommended |
| schemadotorg_mapping_set | Predefined mapping sets (Article, Event, etc.) | Recommended |
| schemadotorg_role | Role-based Schema.org type access | If multi-role |
| schemadotorg_taxonomy | Map taxonomy vocabularies to Schema.org types | If using taxonomy |
| schemadotorg_media | Map media types to ImageObject, VideoObject | If using Media |
| schemadotorg_paragraphs | Map paragraphs to Schema.org nested types | If using Paragraphs |
| schemadotorg_layout_builder | Schema.org awareness in Layout Builder | If using LB |
| schemadotorg_jsonld_preview | Preview JSON-LD output in admin | Development |

### Admin UI

Navigate to `/admin/config/search/schemadotorg` to:
- Browse available Schema.org types
- Create type mappings via UI (alternative to drush commands)
- Configure global settings and property mappings
- View a report of all mapped types on the site

## Common Mistakes

- **Wrong**: Installing on an existing site and running `drush schemadotorg:create-type` over existing content types → **Right**: The drush command creates new content types; it does not retroactively map existing ones without manual field remapping
- **Wrong**: Treating alpha37 as stable for client production sites → **Right**: Pin the version in composer.json and test updates in a staging environment before applying to production; subscribe to the project's release notifications
- **Wrong**: Enabling all 50+ submodules → **Right**: Enable only what your use case needs; unused submodules add UI clutter and can slow admin pages
- **Wrong**: Using Schema.org Blueprints and Schema Metatag on the same content type for JSON-LD → **Right**: Pick one per content type; running both causes duplicate `<script type="application/ld+json">` blocks which confuse validators
- **Wrong**: Expecting field machine names to match your existing naming conventions → **Right**: Blueprints uses Schema.org-derived names (`field_schema_date_published`); plan your content architecture around this before creating types

## See Also

- [Structured Data Decision](structured-data-decision.md) — when to choose Blueprints vs Schema Metatag
- [Schema Types Reference](schema-types-reference.md)
- [Testing & Validation](testing-validation.md)
- Reference: [Schema.org Blueprints on drupal.org](https://www.drupal.org/project/schemadotorg)
- Reference: [schemadotorg project documentation](https://git.drupalcode.org/project/schemadotorg/-/blob/1.x/README.md)
