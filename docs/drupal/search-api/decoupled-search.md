---
description: Decoupled search with Search API — jsonapi_search_api for Next.js, Typesense direct, and middleware patterns
tldr: "Use this when building headless/decoupled frontends (Next.js, React, etc.) that need search functionality."
drupal_version: "11.x"
---

# Decoupled Search

## When to Use

> Use this when building headless/decoupled frontends (Next.js, React, etc.) that need search functionality.

## Decision

| Module | Purpose | Status |
|---|---|---|
| `jsonapi_search_api` | Query Search API indexes via JSON:API | Stable — **recommended** |
| `jsonapi_search_api_facets` | Expose facets via JSON:API | Pairs with above |
| `search_api_typesense` | Index to Typesense, use InstantSearch.js | Stable (2025) |
| `search_api_decoupled` | Alternative display plugin | Alpha |

## Pattern

**Next.js + JSON:API (recommended):**
1. Install: `search_api` + backend + `facets` + `jsonapi_search_api` + `jsonapi_search_api_facets`
2. JSON:API exposes the index as a queryable resource
3. Next.js queries via API route (enables middleware, rate limiting)
4. Facets available via `jsonapi_search_api_facets`

**Typesense direct — for instant search:**
1. `search_api_typesense` indexes content to Typesense
2. Frontend uses Typesense's InstantSearch.js directly
3. No JSON:API intermediary — frontend talks to Typesense API
4. Drupal proxy recommended for access control

## Common Mistakes

- **Wrong**: Exposing Search API directly to frontend without middleware → **Right**: Always use an API route in Next.js for rate limiting and filtering.
- **Wrong**: Using REST instead of JSON:API → **Right**: JSON:API is in Drupal core, more standardized, more efficient.

## See Also

- [Backend Comparison](backend-comparison.md) — Typesense and Meilisearch for decoupled
- [Facets Integration](facets-integration.md)
- Reference: https://www.drupal.org/project/jsonapi_search_api
- Reference: https://next-drupal.org/guides/search-api
