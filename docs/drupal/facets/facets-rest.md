---
description: Facets REST sub-module — expose facet data in REST API responses for headless/decoupled frontends using FacetsSerializer
drupal_version: "11.x"
---

# Facets REST

## When to Use

> Use this guide when building a headless or decoupled frontend and you need facet data (values, counts, active states, URLs) in API responses.

## Decision

**Module:** `facets_rest`

Provides `FacetsSerializer` — a Views REST display style plugin that includes facet data in the REST response alongside search results.

## Pattern

1. Enable: `drush en facets_rest`
2. Create a Views REST export display using your Search API index
3. Select "Facets Serializer" as the display style
4. Create facets for this display's facet source
5. Use the `array` widget for facets used in REST

**Response format:** The REST response includes a `facets` key with structured facet data — values, counts, active states, and URLs for each facet item.

## Common Mistakes

- **Wrong**: Using `links` or `checkbox` widgets with REST → **Right**: Use the `array` widget for REST responses. It returns a PHP array structure without HTML rendering.

## See Also

- [Widgets](widgets.md) — ArrayWidget for programmatic output
- [Facet Sources](facet-sources.md) — REST display as facet source
- Reference: `web/modules/contrib/facets/modules/facets_rest/`
