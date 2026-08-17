---
description: "The facets_rest sub-module for including facet data in Views REST export responses"
tldr: "Use this guide when building a headless or decoupled frontend and you need facet data (values, counts, active states, URLs) in API responses. Use the array widget for REST-facing facets."
drupal_version: "11.x"
---

# Facets REST

## When to Use

> When building a headless/decoupled frontend and need facet data in API responses.

## Decision

**Module:** `facets_rest` — provides `FacetsSerializer`, a Views REST display style plugin that includes facet data in the REST response alongside search results.

## Pattern

1. Enable: `drush en facets_rest`
2. Create a Views REST export display using your Search API index
3. Select "Facets Serializer" as the display style
4. Create facets for this display's facet source
5. Use the `array` widget for facets used in REST

The response includes a `facets` key with structured facet data — values, counts, active states, and URLs for each facet item.

## Common Mistakes

- **Wrong**: Using the `links` or `checkbox` widget for REST facets → **Right**: Use the `array` widget so the response contains raw structured data instead of rendered HTML.

## See Also

- [Widgets](widgets.md) — ArrayWidget for programmatic output
- [Facet Sources](facet-sources.md) — REST display as facet source
- Reference: `modules/facets_rest/`
