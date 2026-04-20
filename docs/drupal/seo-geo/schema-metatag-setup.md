---
description: Install and configure Schema Metatag 3.x for JSON-LD structured data — token mappings for Article, Organization, and WebPage types
tldr: "Schema Metatag extends the Metatag module to output Schema.org JSON-LD via the same token-based admin UI. Configure once at the content type level and every node inherits correct structured data automatically."
drupal_version: "11.x"
---

# Schema Metatag Setup

## When to Use

> Schema Metatag extends the Metatag module to output Schema.org JSON-LD via the same token-based admin UI. Configure once at the content type level and every node inherits correct structured data automatically. Start here for retrofitting any existing Drupal site with rich results eligibility.

## Decision

| Situation | Choice | Why |
|-----------|--------|-----|
| Need Article rich results | Enable schema_article | Supports headline, author, datePublished, image — required properties |
| Need Organization in publisher field | Enable schema_organization | Required as Article.publisher; also used for site-wide identity |
| Need breadcrumb structured data | Enable schema_web_page + Easy Breadcrumb | WebPage type wraps page context; breadcrumbs handled by Easy Breadcrumb module |
| All content shares a publisher | Configure Organization globally | Set once in Global metatag defaults; Article inherits via token |
| Per-node overrides needed | Leave node-level fields empty | Cascading inheritance: Global → Content type → Node; empty = inherit |
| Need FAQPage or HowTo | Enable schema_faq_page or schema_how_to | Separate submodules; configure per content type |

## Pattern

### Install

```bash
composer require drupal/schema_metatag:^3.0
drush en schema_metatag schema_article schema_web_page schema_organization
drush cr
```

### Enable Submodules

Enable only the Schema.org types you actively use. Each submodule adds a new tab to the Metatag configuration form.

| Submodule | Schema Type | When to Enable |
|-----------|-------------|----------------|
| schema_article | Article, NewsArticle, BlogPosting | Any editorial content |
| schema_web_page | WebPage, AboutPage, ContactPage | General pages |
| schema_organization | Organization | Publisher identity, local business |
| schema_person | Person | Author profiles, staff directories |
| schema_product | Product | E-commerce or product catalog |
| schema_event | Event | Event listings |
| schema_faq_page | FAQPage | FAQ sections (high GEO value) |
| schema_how_to | HowTo | Step-by-step instructional content |
| schema_breadcrumb | BreadcrumbList | Manual breadcrumb JSON-LD |

### Configure Article Token Mapping

Navigate to `/admin/config/search/metatag`. Add or edit the configuration for your Article content type. In the Schema.org tab, map tokens:

```
# Required properties for Article rich results
@type:          Article
name:           [node:title]
headline:       [node:title]
datePublished:  [node:created:html_datetime]
dateModified:   [node:changed:html_datetime]
url:            [node:url:absolute]

# Author (nested Person type)
author > @type: Person
author > name:  [node:author:display-name]
author > url:   [node:author:url:absolute]

# Image (required for rich results eligibility)
image > @type:  ImageObject
image > url:    [node:field_image:entity:url:absolute]
image > width:  [node:field_image:width]
image > height: [node:field_image:height]

# Publisher (nested Organization — configure separately)
publisher > @type: Organization
publisher > name:  [site:name]
publisher > logo > @type: ImageObject
publisher > logo > url:   [site:url:absolute]/logo.png
```

### Organization Setup (Global Default)

Configure once at Global level so all content types inherit it:

```
# /admin/config/search/metatag → Global → Schema.org tab
@type:           Organization
name:            [site:name]
url:             [site:url:absolute]
logo > @type:    ImageObject
logo > url:      [site:url:absolute]/path/to/logo.png
logo > width:    600
logo > height:   60
```

### Required Image Dimensions

Google requires Article images to be at minimum 1200px wide with 16:9 aspect ratio for rich result eligibility. Configure a responsive image style or image field formatter to match:

```
Minimum: 1200 × 675px (16:9)
Recommended: 1200 × 630px or 1200 × 900px
Format: JPEG or WebP preferred
```

### Verify JSON-LD Output

View page source and search for `application/ld+json` to confirm the script block is present:

```html
<script type="application/ld+json">
{
  "@context": "http://schema.org",
  "@type": "Article",
  "name": "My Article Title",
  "datePublished": "2026-03-01T10:00:00+00:00",
  ...
}
</script>
```

## Common Mistakes

- **Wrong**: Using `[node:created]` for datePublished → **Right**: Use `[node:created:html_datetime]` to output ISO 8601 format (`2026-03-01T10:00:00+00:00`); Google rejects non-ISO dates
- **Wrong**: Leaving image empty on Article → **Right**: `image` is required for Article rich results eligibility; use a dedicated hero/feature image field
- **Wrong**: Configuring publisher Organization in Article config only → **Right**: Set Organization in Global defaults so all types inherit it; avoid repeating the same config per content type
- **Wrong**: Enabling all 25 schema submodules → **Right**: Enable only active types; unused types still appear in admin UI and create confusion
- **Wrong**: Using relative URLs in schema properties → **Right**: Always use `[node:url:absolute]` and `[site:url:absolute]` — schema URLs must be absolute
- **Wrong**: Setting `@type: Article` on non-editorial pages (contact, about) → **Right**: Map WebPage types to general pages; Article is for editorial content only

## See Also

- [Structured Data Decision](structured-data-decision.md)
- [Schema Types Reference](schema-types-reference.md)
- [Custom Schema Types](custom-schema-types.md)
- [Testing & Validation](testing-validation.md)
- Reference: [Schema Metatag on drupal.org](https://www.drupal.org/project/schema_metatag)
- Reference: [Google Article structured data](https://developers.google.com/search/docs/appearance/structured-data/article)
- Reference: [Metatag token system](metatag-architecture.md)
