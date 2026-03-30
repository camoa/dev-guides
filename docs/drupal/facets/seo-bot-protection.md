---
description: Facets SEO and bot protection — layered defense against crawl budget exhaustion and AI scraper abuse, including robots.txt, facet_bot_blocker, Cloudflare WAF, and form-based facets
drupal_version: "11.x"
---

# SEO & Bot Protection

## When to Use

> Use this guide when deploying any site with Facets. Facets have ZERO built-in SEO or bot protection. Without protection, bots generate combinatorial URL explosions that exhaust server resources, waste crawl budgets, and create duplicate content penalties.

## Decision

**The crawl problem:**
- 5 facets × 10 options each = 100,000+ possible URL combinations
- Example: Category (20) × Color (10) × Size (5) × Brand (50) × Price (10) = **5,000,000 URLs**
- Each URL breaks the cache and hits the origin database
- AI scrapers frequently ignore robots.txt and generate more abuse than Googlebot

**Two threat categories:**

| Threat | Behavior | robots.txt Respected? |
|---|---|---|
| Search engine bots (Googlebot, Bingbot) | Follow every link, index every page | Usually yes |
| AI scrapers (GPTBot, ClaudeBot, CCBot, Bytespider) | Aggressively crawl all reachable URLs | Often no |

**Recommended defense stack (priority order):**

| Priority | Layer | What It Stops |
|---|---|---|
| **1** | **Form-based facets (exposed filters + BEF)** | **Eliminates crawlable facet URLs entirely** |
| 2 | Cloudflare WAF rule on `f%5B0%5D` | Bots at edge — zero server load |
| 3 | Cloudflare AI bot user-agent blocking | Known AI scrapers |
| 4 | robots.txt with `Disallow: /*f%5B0%5D*` | Compliant bots |
| 5 | Facet Bot Blocker module (limit: 2, 410 Gone) | Deep crawlers that reach Drupal |
| 6 | Meta noindex on faceted pages | Prevents indexing of crawled pages |
| 7 | Canonical URL to base search page | Consolidates link signals |

## Pattern

**Layer 1 — Form-based facets (primary solution):**

Block-based facets render as `<a href="?f[0]=color:blue">` — bots follow these links eagerly. Exposed filter facets render as `<input type="checkbox">` inside a `<form>`. No crawlable URLs exist in the HTML at all.

```bash
drush en facets_exposed_filters better_exposed_filters
```

**Layer 2 — robots.txt** (block both encoded and unencoded brackets):

```
Disallow: /*f%5B0%5D*
Disallow: /*?*f[

User-agent: GPTBot
Disallow: /

User-agent: ClaudeBot
Disallow: /

User-agent: CCBot
Disallow: /

User-agent: Bytespider
Disallow: /
```

Use the `robotstxt` module: `composer require drupal/robotstxt && drush en robotstxt`

**Layer 3 — Facet Bot Blocker module:**

```bash
composer require drupal/facet_bot_blocker
drush en facet_bot_blocker
```

Config at `/admin/config/system/facet-bot-blocker`:

| Setting | Default | Purpose |
|---|---|---|
| Facet parameter limit | 1 | Block if `f[N]` where N >= limit exists |
| Return 410 Gone | FALSE | 410 tells bots the URL is permanently gone (stronger than 403) |

**Layer 4 — Cloudflare WAF rule:**

```
Rule: URI Query String wildcard *f%5B0%5D*
Action: Managed Challenge
```

**Layer 5 — Meta noindex:**

```php
function my_module_page_attachments_alter(array &$attachments) {
  $facet_params = \Drupal::request()->query->all('f');
  if (!empty($facet_params)) {
    $attachments['#attached']['html_head'][] = [[
      '#tag' => 'meta',
      '#attributes' => ['name' => 'robots', 'content' => 'noindex, follow'],
    ], 'robots_noindex'];
  }
}
```

## Common Mistakes

- **Wrong**: Deploying Facets with no protection → **Right**: The module has zero built-in SEO/bot protection. You must implement it yourself.
- **Wrong**: Relying only on robots.txt → **Right**: AI bots frequently ignore robots.txt. Use server-side and edge-level blocking too.
- **Wrong**: Using 403 Forbidden instead of 410 Gone → **Right**: 410 tells bots the URL is permanently removed — stronger deindexing signal, less likely to be retried.
- **Wrong**: Blocking only `f[0]` without the URL-encoded form → **Right**: `f[0]` becomes `f%5B0%5D` in URLs. Both patterns must be blocked.
- **Wrong**: Ignoring AI scrapers and only thinking about Googlebot → **Right**: In 2025-2026, AI scrapers generate more facet abuse traffic than search engines.

## See Also

- [Canonical URLs & Duplicate Content](canonical-urls.md) — deeper canonical strategy
- [Facets Exposed Filters](facets-exposed-filters.md) — form-based facets as architectural defense
- [Pretty Paths](pretty-paths.md) — cleaner URLs that are easier to block
- [URL Processors](url-processors.md) — how facet URLs are structured
