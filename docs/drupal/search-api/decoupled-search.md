---
description: Decoupled search with Search API — jsonapi_search_api for Next.js (no stable release), Typesense direct, and middleware patterns
tldr: "Use this when building headless/decoupled frontends (Next.js, React, etc.) that need search functionality. jsonapi_search_api is the most-used option but has never had a stable release."
drupal_version: "11.x"
---

# Decoupled Search

## When to Use

> When building headless/decoupled frontends (Next.js, React, etc.) that need search functionality.

## Decision: Module Options

| Module | Purpose | Status |
|---|---|---|
| `jsonapi_search_api` | Query Search API indexes via JSON:API | **No stable release** — 8.x-1.0-rc5 is the latest tag |
| `jsonapi_search_api_facets` | Expose facets via JSON:API | Sub-module of `jsonapi_search_api`, not a separate project |
| `search_api_decoupled` | Alternative display plugin | Alpha (1.0.0-alpha44) |

`jsonapi_search_api` is the most widely used option and the one next-drupal documents, but it has never had a stable release. On a build policy that forbids pre-releases, it needs an explicit exception before it goes into `composer.json`.

## Pattern: Next.js + JSON:API

The recommended pattern (documented at next-drupal.org):

1. Install: `search_api` + backend + `facets` + `jsonapi_search_api` (enable its `jsonapi_search_api_facets` sub-module for facets)
2. JSON:API exposes the index as a queryable resource
3. Next.js queries via API route (enables middleware, rate limiting)
4. Facets available via `jsonapi_search_api_facets`

## Pattern: Typesense Direct

Alternative for instant search:

1. `search_api_typesense` indexes content to Typesense
2. Frontend uses Typesense's InstantSearch.js directly
3. No JSON:API intermediary — frontend talks to Typesense API
4. Drupal proxy recommended for access control

## Common Mistakes

- **Exposing Search API directly without middleware** — Always use an API route in Next.js for rate limiting and filtering.
- **Using REST instead of JSON:API** — JSON:API is in Drupal core, more standardized, more efficient.

## See Also

- [Backend Comparison](backend-comparison.md) — Typesense and Meilisearch for decoupled
- [Facets Integration](facets-integration.md) — facets in decoupled context
