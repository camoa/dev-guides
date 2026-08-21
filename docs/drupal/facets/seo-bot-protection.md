---
description: "Facets SEO and bot protection — layered defense against crawl budget exhaustion and AI scraper abuse, including robots.txt, facet_bot_blocker, Cloudflare WAF, and form-based facets"
tldr: "Use this guide when deploying any site with Facets. Facets have ZERO built-in SEO or bot protection — combinatorial URL explosion invites crawl budget waste. Form-based (exposed filter) facets are the primary architectural fix."
drupal_version: "11.x"
---

# SEO & Bot Protection

## When to Use

> Use this guide when deploying any site with Facets. Without protection, bots generate combinatorial URL explosions that exhaust server resources, waste crawl budgets, and create duplicate content penalties.

## Decision

**The crawl problem:**
- 5 facets × 10 options each = 100,000+ possible URL combinations
- Example: Category (20) × Color (10) × Size (5) × Brand (50) × Price (10) = **5,000,000 URLs**
- Each URL breaks the cache and hits the origin database
- AI scrapers frequently ignore robots.txt and generate more abuse than Googlebot
- **Real-world impact:** facet traversal multiplies crawlable URLs combinatorially — each additional facet with N values multiplies the URL space, so a handful of facets can generate more distinct URLs than the site has content. Distributed crawlers walking that space evict useful entries from the page cache. Measure your own cache hit ratio before and after enabling blocking rather than working from a headline figure.

**Two threat categories:**

| Threat | Behavior | robots.txt Respected? |
|---|---|---|
| Search engine bots (Googlebot, Bingbot) | Follow every link, index every page | Usually yes |
| AI scrapers (GPTBot, ClaudeBot, CCBot, Bytespider) | Aggressively crawl all reachable URLs | Often no |

**Recommended defense stack (priority order) — layer 1 is architectural, not a mitigation:**

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

**Layer 1 — form-based facets (primary solution):** block-based facets render as `<a href="?f[0]=color:blue">` — bots follow these links eagerly. Exposed filter facets render as `<input type="checkbox">` inside a `<form>`; no crawlable URLs exist in the HTML at all.

```bash
drush en facets_exposed_filters better_exposed_filters
```

Why this works: HTML forms require POST/GET submission — bots that just follow `<a>` tags never trigger them; BEF's auto-submit requires JavaScript execution; checkbox/radio state is not in the HTML source as a crawlable URL; even AI bots that execute JavaScript rarely interact with form elements. Every option in a block-based facet is a crawlable link — 5 facets × 10 options puts 50+ links in the HTML, each leading to 50+ more. Bots that only follow links never discover facet URLs at all if there are none to follow — this is the correct architecture, not a band-aid; the remaining layers are insurance.

**Caveat:** this protection may weaken over time as bots grow more sophisticated at form interaction — use it as one layer in a defense-in-depth strategy, not the only layer.

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

User-agent: anthropic-ai
Disallow: /

User-agent: Google-Extended
Disallow: /

User-agent: FacebookBot
Disallow: /
```

If you use pretty paths, add `Disallow: /search/facets/` for the path form too.

Manage it from the admin UI: `composer require drupal/robotstxt && drush en robotstxt`.

**Layer 3 — Cloudflare WAF rule at the edge:**

```
Rule: URI Query String wildcard *f%5B0%5D*
Action: Managed Challenge
```

"Managed Challenge" shows a CAPTCHA-like challenge to bots while letting real users through; use "Block" for more aggressive protection. A second rule catches the AI scrapers by user agent:

```
Rule: User-Agent contains GPTBot OR ClaudeBot OR CCBot OR Bytespider OR anthropic-ai
Action: Block
```

On Pantheon, request AGCDN+WAF via a support ticket — Pantheon can apply JA3 fingerprinting and VCL rules to identify bot signatures at the edge.

**Layer 4 — Facet Bot Blocker module:**

```bash
composer require drupal/facet_bot_blocker
drush en facet_bot_blocker
```

Config at `/admin/config/system/facet-bot-blocker`:

| Setting | Default | Purpose |
|---|---|---|
| Facet parameter limit | 1 | Block if `f[N]` where N >= limit exists |
| Return 410 Gone | FALSE | 410 tells bots the URL is permanently gone (stronger than 403) |
| Custom blocked message | `<h1>Excessive crawling detected</h1><p>We have blocked your request.</p>` | HTML returned to blocked requests |

**Example** with limit set to `2`: `?f[0]=color:blue` (1 param) and `?f[0]=color:blue&f[1]=size:large` (2 params) are allowed; `?f[0]=color:blue&f[1]=size:large&f[2]=brand:acme` is blocked because `f[2]` exceeds the limit.

It operates as a kernel event subscriber at priority 101, checking `$_GET['f'][$limit]` before Drupal fully bootstraps. The permission `bypass facet bot blocker` exempts logged-in users. Dashboard: `/admin/reports/facet-bot-blocker` (requires Memcache or Redis for metrics).

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

Or use the `metatag` module configured for search page paths.

**Layer 6 — canonical URLs:** point all faceted variations at the base search page with `rel="canonical"` so link signals consolidate on one URL. The `hook_page_attachments_alter()` implementation is in [Canonical URLs & Duplicate Content](canonical-urls.md).

## Common Mistakes

- **Wrong**: Deploying Facets with no protection → **Right**: The module has zero built-in SEO/bot protection. You must implement it yourself.
- **Wrong**: Relying only on robots.txt → **Right**: AI bots frequently ignore robots.txt. Use server-side and edge-level blocking too.
- **Wrong**: Using 403 Forbidden instead of 410 Gone → **Right**: 410 tells bots the URL is permanently removed — stronger deindexing signal, less likely to be retried.
- **Wrong**: Blocking only `f[0]` without the URL-encoded form → **Right**: `f[0]` becomes `f%5B0%5D` in URLs. Both patterns must be blocked in robots.txt and WAF rules.
- **Wrong**: Ignoring AI scrapers and only thinking about Googlebot → **Right**: AI scrapers now generate more facet abuse traffic than search engines.
- **Wrong**: Blocking the base search page or all query parameters → **Right**: Scope blocking to the facet `f[]` pattern only.
- **Wrong**: Deploying the layers and never looking again → **Right**: The threat evolves. Watch the Facet Bot Blocker dashboard, Cloudflare analytics, or server logs for shifting bot traffic patterns.

## See Also

- [Canonical URLs & Duplicate Content](canonical-urls.md) — deeper canonical strategy
- [Facets Exposed Filters](facets-exposed-filters.md) — form-based facets as architectural defense
- [Pretty Paths](pretty-paths.md) — cleaner URLs that are easier to block
- [URL Processors](url-processors.md) — how facet URLs are structured
