---
description: Choose between Schema Metatag and Schema.org Blueprints for JSON-LD structured data — retrofit vs greenfield, stability vs depth
tldr: "Drupal has two distinct approaches to outputting Schema.org JSON-LD. Schema Metatag layers structured data on top of existing content using token-mapped metatags — ideal for retrofitting established sites."
drupal_version: "11.x"
---

# Structured Data Decision

## When to Use

> Drupal has two distinct approaches to outputting Schema.org JSON-LD. Schema Metatag layers structured data on top of existing content using token-mapped metatags — ideal for retrofitting established sites. Schema.org Blueprints inverts the relationship entirely, generating Drupal content types and fields from Schema.org definitions — designed for greenfield builds that want schema-aligned content models from day one. The format question (JSON-LD vs Microdata vs RDFa) is simpler: use JSON-LD.

## Decision

### Format: JSON-LD vs Microdata vs RDFa

| Format | Use | Why |
|--------|-----|-----|
| JSON-LD | Always | Google's recommended format; lives in `<script>` tag separate from HTML; easiest to debug and maintain |
| Microdata | Avoid | Embedded in HTML attributes; brittle when markup changes; no advantage over JSON-LD |
| RDFa | Avoid for Schema.org | Useful for semantic web/Linked Data contexts; no Rich Results advantage; complex to maintain |

Both Schema Metatag and Schema.org Blueprints output JSON-LD. Do not mix formats on the same page.

### Module: Schema Metatag vs Schema.org Blueprints

| Situation | Choice | Why |
|-----------|--------|-----|
| Existing site with established content types | Schema Metatag | Token-based mapping — no content restructuring required |
| Greenfield build, schema-first architecture | Schema.org Blueprints | Content types and fields are generated from Schema.org; tighter coupling |
| Need production-stable module (now) | Schema Metatag 3.0.4 | Stable release; widely adopted; well-tested |
| Alpha risk acceptable, deep schema alignment wanted | Schema.org Blueprints 1.0.0-alpha38 | Limited adoption; alpha stability; significant ongoing API changes |
| Decoupled/headless Drupal | Schema.org Blueprints | schemadotorg_jsonld outputs structured JSON API; schema-aligned field names |
| Quick wins on article/product pages | Schema Metatag | 25 pre-built types; configure in admin UI; no custom code needed |
| Custom content model already built | Schema Metatag | Map existing fields to schema properties via tokens |
| Need FAQPage or HowTo rich results | Schema Metatag | Both types supported out of the box |

### Using Both Together

Schema Metatag and Schema.org Blueprints are not mutually exclusive. A valid pattern:

- Use Schema.org Blueprints to model new content types (Event, Product)
- Use Schema Metatag for types not yet supported in Blueprints (FAQPage, HowTo)
- Avoid outputting duplicate JSON-LD blocks for the same entity — pick one per content type

## Pattern

Schema Metatag — token-mapped JSON-LD on existing content:

```
# Admin: /admin/config/search/metatag
# Content type "Article" → Schema.org tab
@type: Article
name: [node:title]
datePublished: [node:created:html_datetime]
dateModified: [node:changed:html_datetime]
author > @type: Person
author > name: [node:author:display-name]
```

Schema.org Blueprints — schema-first content type creation:

```bash
# Generate content type from Schema.org definition
drush schemadotorg:create-type node:Article
drush schemadotorg:create-type node:Event

# JSON-LD output is automatic via schemadotorg_jsonld submodule
# No token mapping required — fields match schema properties
```

## Common Mistakes

- **Wrong**: Using Microdata or RDFa for Schema.org markup on a new build → **Right**: JSON-LD only; simpler to implement and maintain
- **Wrong**: Installing Schema.org Blueprints on an existing site expecting a drop-in replacement for Schema Metatag → **Right**: Blueprints rebuilds content architecture; it is not a configuration replacement
- **Wrong**: Running both modules outputting JSON-LD for the same content type → **Right**: Disable schemadotorg_jsonld for types managed by Schema Metatag, or vice versa
- **Wrong**: Treating alpha38 stability as production-ready for high-stakes projects → **Right**: Monitor the project issue queue; test upgrades in staging; Schema Metatag 3.0.4 is the safer choice for production
- **Wrong**: Skipping validation after configuration → **Right**: Always verify with Google Rich Results Test after setup

## See Also

- [Schema Metatag Setup](schema-metatag-setup.md)
- [Schema Types Reference](schema-types-reference.md)
- [Schema.org Blueprints](schemadotorg-blueprints.md)
- [Testing & Validation](testing-validation.md)
- Reference: [Schema Metatag on drupal.org](https://www.drupal.org/project/schema_metatag)
- Reference: [Schema.org Blueprints on drupal.org](https://www.drupal.org/project/schemadotorg)
- Reference: [Google JSON-LD recommendation](https://developers.google.com/search/docs/appearance/structured-data/intro-structured-data)
