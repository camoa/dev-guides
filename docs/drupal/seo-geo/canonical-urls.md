---
description: Canonical URL configuration for Drupal 11 — Metatag canonical, www vs non-www, trailing slashes, Redirect module, multilingual hreflang, and pagination
drupal_version: "11.x"
---

# Canonical URLs

## When to Use

> Configure canonical URLs whenever a page is accessible at more than one URL — this is the norm in Drupal, not the exception. Drupal generates clean aliases via Pathauto but the same node is also reachable at `/node/123`. Without canonicals, search engines may split ranking signals across duplicate URLs.

## Decision

| Situation | Choice | Why |
|-----------|--------|-----|
| Standard page canonicalization | Metatag module canonical tag | Signals preferred URL without redirecting users |
| www vs non-www domain mismatch | Redirect module + server redirect | 301 redirect consolidates ranking signals |
| Trailing slash inconsistency | Server-level redirect (nginx/Apache) | Drupal alone does not enforce this consistently |
| Alias change (old URL still valid) | Redirect module auto-redirect | Pathauto integration creates 301 automatically |
| Multilingual content | hreflang + canonical per language | Each translation gets its own canonical, linked by hreflang |
| Pagination (/page=2, /page=3) | canonical to page 1 or `rel=next/prev` | Prevents paginated pages from competing |
| Faceted navigation (views filters) | Disallow in robots.txt + canonical to base | Query string URLs should not be indexed |

## Pattern

### Metatag Canonical Configuration

Enable the Metatag module and navigate to:
`/admin/config/search/metatag`

Under **Global** defaults, set the canonical URL token:

```
Canonical URL: [current-page:url]
```

This uses Drupal's current page URL, which resolves to the alias (e.g., `/blog/my-article`) rather than the node path (`/node/123`).

For per-content-type overrides, add a **Content** metatag group and set:

```
Canonical URL: [node:url]
```

`[node:url]` resolves to the node's canonical alias including the base URL.

### Drupal's Default Canonical Handling

Drupal core outputs a `<link rel="canonical">` tag automatically for nodes via `html.html.twig`. The Metatag module **overrides** this with configurable tokens. Install Metatag to take control — do not rely on core's default.

Core canonical behavior:
- Node pages: resolves to alias if Pathauto alias exists
- Views pages: canonical = current URL (may include query strings)
- User pages: canonical = `/user/[uid]`

### www vs Non-www Canonicalization

This must be handled at the server or DNS level — Drupal alone cannot reliably redirect all requests.

**Nginx** — redirect non-www to www:
```nginx
server {
  listen 80;
  server_name example.com;
  return 301 https://www.example.com$request_uri;
}
```

**Redirect module** can supplement this for Drupal-handled requests:
`/admin/config/search/redirect` → add redirect from `http://example.com` to `https://www.example.com`

Also set in `settings.php` to lock the trusted host pattern:
```php
$settings['trusted_host_patterns'] = [
  '^www\.example\.com$',
];
```

### Redirect Module — Alias Change Auto-Redirect

When Pathauto regenerates an alias, the Redirect module automatically creates a 301 from the old alias to the new one. Verify this is enabled at:
`/admin/config/search/redirect/settings` → "Automatically create redirects when URL aliases are changed"

Manual redirects: `/admin/config/search/redirect/add`

Status code decision:
- **301** — permanent redirect; passes ranking signals; use for all production URL changes
- **302** — temporary redirect; search engines do not pass signals; use for A/B testing or maintenance pages only

### Multilingual Canonical + hreflang

Each language version of a page should have:
1. A canonical pointing to its own language URL
2. hreflang annotations pointing to all other language versions

The `metatag_hreflang` submodule handles this automatically when content is translated. See [Metatag for Multilingual](metatag-multilingual.md) for configuration.

### Pagination

For paginated content (Views pager, node body pagination):

```
Page 1: <link rel="canonical" href="https://example.com/blog">
Page 2: <link rel="canonical" href="https://example.com/blog">  (points to page 1)
```

Or use `rel="prev"` / `rel="next"` (still useful for Bing even though Google deprecated it):

```html
<link rel="prev" href="https://example.com/blog">
<link rel="next" href="https://example.com/blog?page=2">
```

In Drupal, add these via `hook_page_attachments()` or a custom Metatag plugin. For most sites, canonical to page 1 is sufficient.

## Common Mistakes

- **Wrong**: Relying on Drupal core canonical without Metatag → **Right**: Install Metatag for configurable, token-driven canonicals
- **Wrong**: Canonical URL token that includes query strings (`[current-page:url:absolute]` on filtered views) → **Right**: Point to the base view URL, not the filtered URL
- **Wrong**: No 301 redirect for www/non-www — letting both versions be indexed → **Right**: Pick one, redirect the other at the server level before launch
- **Wrong**: Internal links using `/node/123` paths → **Right**: Always link using aliases; broken aliases expose node paths to crawlers
- **Wrong**: Not enabling auto-redirect on alias change → **Right**: Enable Redirect module integration with Pathauto immediately after install

## See Also

- [Metatag Architecture](metatag-architecture.md) — cascading inheritance for canonical defaults
- [Redirect Management](redirect-management.md) — 301/302 decision and bulk redirect management
- [Metatag for Multilingual](metatag-multilingual.md) — hreflang configuration
- [Robots.txt](robots-txt.md) — disallowing faceted navigation query strings
- Reference: [Google canonical URL guide](https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls)
- Reference: [Redirect module](https://www.drupal.org/project/redirect)
