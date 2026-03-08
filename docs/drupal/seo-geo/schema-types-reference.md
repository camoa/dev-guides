---
description: All 25 Schema Metatag supported Schema.org types with key properties, GEO priority types, and field-to-property mapping patterns
drupal_version: "11.x"
---

# Schema Types Reference

## When to Use

> Reference this guide when mapping Drupal content types and fields to Schema.org types. Schema Metatag 3.x supports 25 top-level Schema.org types via submodules. Each type has required and recommended properties that affect rich result eligibility in Google Search.

## Decision

### Choosing a Schema Type for Your Content

| Content type | Schema type | Rich result? | GEO value |
|--------------|-------------|--------------|-----------|
| News/blog post | Article / NewsArticle / BlogPosting | Yes | High |
| FAQ section | FAQPage | Yes | Very high |
| Product page | Product | Yes | High |
| Step-by-step guide | HowTo | Yes | High |
| Event listing | Event | Yes | Medium |
| Person/author | Person | No (enhances) | Medium |
| Company/org page | Organization | No (enhances) | High |
| Course/training | Course | Yes | Medium |
| Recipe | Recipe | Yes | Medium |
| Video | VideoObject | Yes | High |
| General page | WebPage | No | Low |
| Book | Book | Yes | Low |
| Software app | SoftwareApplication | Yes | Medium |

### Article Subtype Selection

| Content | Use | Why |
|---------|-----|-----|
| News content, timely reporting | NewsArticle | Eligible for Top Stories carousel |
| Editorial blog posts | BlogPosting | Appropriate for opinion/commentary |
| Generic articles | Article | Broadest coverage; safe default |
| Scholarly/research content | ScholarlyArticle | Academic indexing |

## Pattern

### All 25 Supported Types

**Editorial & Content**

| Type | Submodule | Key Required Properties | Rich Results |
|------|-----------|------------------------|--------------|
| Article | schema_article | headline, image, datePublished, author | Yes |
| NewsArticle | schema_article | headline, image, datePublished, author | Yes (Top Stories) |
| BlogPosting | schema_article | headline, image, datePublished, author | Yes |
| ScholarlyArticle | schema_article | headline, author, datePublished | No |

**Commerce & Products**

| Type | Submodule | Key Required Properties | Rich Results |
|------|-----------|------------------------|--------------|
| Product | schema_product | name, image, offers | Yes |
| Offer | schema_product | price, priceCurrency, availability | Nested in Product |
| AggregateRating | schema_product | ratingValue, reviewCount | Nested in Product |
| Review | schema_review | reviewRating, author | Nested in Product |

**Events & Activities**

| Type | Submodule | Key Required Properties | Rich Results |
|------|-----------|------------------------|--------------|
| Event | schema_event | name, startDate, location | Yes |
| Course | schema_course | name, description, provider | Yes |
| Recipe | schema_recipe | name, image, recipeIngredient, recipeInstructions | Yes |

**Information Architecture**

| Type | Submodule | Key Required Properties | Rich Results |
|------|-----------|------------------------|--------------|
| FAQPage | schema_faq_page | mainEntity (Question + acceptedAnswer) | Yes |
| HowTo | schema_how_to | name, step (HowToStep) | Yes |
| BreadcrumbList | schema_breadcrumb | itemListElement (ListItem) | Yes |
| WebPage | schema_web_page | name, url | No |
| AboutPage | schema_web_page | name, url | No |
| ContactPage | schema_web_page | name, url | No |

**Entities & Organizations**

| Type | Submodule | Key Required Properties | Rich Results |
|------|-----------|------------------------|--------------|
| Organization | schema_organization | name, url, logo | No (enhances) |
| LocalBusiness | schema_organization | name, address, telephone | Yes |
| Person | schema_person | name | No (enhances) |
| JobPosting | schema_job_posting | title, hiringOrganization, jobLocation | Yes |

**Media**

| Type | Submodule | Key Required Properties | Rich Results |
|------|-----------|------------------------|--------------|
| ImageObject | Nested type | url, width, height | Enhances others |
| VideoObject | schema_video_object | name, description, thumbnailUrl, uploadDate | Yes |
| AudioObject | schema_audio_object | name, description, contentUrl | No |
| Book | schema_book | name, author, isbn | Yes |
| SoftwareApplication | schema_software_application | name, operatingSystem, applicationCategory | Yes |

### GEO Priority: Field-to-Property Mapping

These five types are highest value for AI citation and rich result eligibility.

**Article**
```
name / headline  → node:title
datePublished    → node:created:html_datetime
dateModified     → node:changed:html_datetime
author > name    → node:author:display-name
image > url      → node:field_hero_image:entity:url:absolute
description      → node:field_summary  (or metatag description token)
publisher > name → site:name
```

**FAQPage** (structured as Question/Answer pairs)
```
mainEntity[] > @type           → Question
mainEntity[] > name            → paragraph:field_question (or node field)
mainEntity[] > acceptedAnswer  → Answer
acceptedAnswer > text          → paragraph:field_answer:value
```

**Product**
```
name             → node:title
description      → node:field_description
image > url      → node:field_product_image:entity:url:absolute
offers > price   → node:field_price
offers > priceCurrency → "USD"  (hardcoded or config token)
offers > availability → "https://schema.org/InStock"
aggregateRating > ratingValue  → node:field_rating
aggregateRating > reviewCount  → node:field_review_count
```

**HowTo**
```
name             → node:title
description      → node:field_summary
totalTime        → node:field_time  (ISO 8601 duration: "PT30M")
step[] > @type   → HowToStep
step[] > name    → paragraph:field_step_title
step[] > text    → paragraph:field_step_body
```

**Organization**
```
name             → site:name
url              → site:url:absolute
logo > url       → site:url:absolute + /path/to/logo.png
address > streetAddress    → config token or hardcoded
address > addressLocality  → config token or hardcoded
address > addressRegion    → config token or hardcoded
address > postalCode       → config token or hardcoded
address > addressCountry   → "US"
telephone        → config token or hardcoded
```

### Nested Types

Schema.org types frequently nest other types. Schema Metatag handles this with grouped property fields:

| Parent | Nested type | Purpose |
|--------|-------------|---------|
| Article | ImageObject | Article.image |
| Article | Person | Article.author |
| Article | Organization | Article.publisher |
| Product | Offer | Pricing and availability |
| Product | AggregateRating | Star ratings |
| Event | PostalAddress | Event location |
| Organization | PostalAddress | Business address |
| Organization | ImageObject | Logo |

## Common Mistakes

- **Wrong**: Using Article for all content types (contact pages, landing pages) → **Right**: Match schema type to content purpose; use WebPage for general pages, AboutPage for about sections
- **Wrong**: Omitting required properties and expecting rich results → **Right**: Google has minimum required properties per type; missing `image` on Article or `offers` on Product disqualifies the rich result
- **Wrong**: Setting datePublished to the node publish date without checking it was actually published then → **Right**: If you backdated content, datePublished should reflect actual original publication, not the Drupal created timestamp
- **Wrong**: Using `http://schema.org` context when Google recommends `https://schema.org` → **Right**: Schema Metatag handles this automatically; verify in output
- **Wrong**: Nesting Organization inside every Article manually → **Right**: Configure publisher Organization once in Global metatag defaults and let Article inherit it

## See Also

- [Schema Metatag Setup](schema-metatag-setup.md)
- [Custom Schema Types](custom-schema-types.md)
- [Testing & Validation](testing-validation.md)
- [Schema.org for AI Discovery](schema-ai-discovery.md)
- Reference: [Google structured data types](https://developers.google.com/search/docs/appearance/structured-data/search-gallery)
- Reference: [Schema.org full type hierarchy](https://schema.org/docs/full.html)
