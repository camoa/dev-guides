---
description: "Facets SEO and bot protection — layered defense against crawl budget exhaustion and AI scraper abuse, including robots.txt, facet_bot_blocker, Cloudflare WAF, and form-based facets"
tldr: "Use this guide when deploying any site with Facets. Facets have ZERO built-in SEO or bot protection — combinatorial URL explosion invites crawl budget waste. Form-based (exposed filter) facets are the primary architectural fix."
drupal_version: "11.x"
---

# SEO & Bot Protection

## When to Use

> When you need to prevent search engine AND AI bot crawl abuse on faceted URLs. This is critical for any site with facets — without protection, bots generate millions of URL combinations that exhaust server resources, waste crawl budgets, and create duplicate content penalties.

## Decision: The Crawl Problem

Facets create **combinatorial URL explosion**:

- 5 facets × 10 options each = 100,000+ possible URL combinations
- Each URL is a "new page" to crawlers — and every facet combination generates a **unique, cache-breaking request** that hits the origin database
- Leads to: crawl budget waste, duplicate content penalties, index bloat, server load, hosting cost overruns

**Example:** A product search with Category (20), Color (10), Size (5), Brand (50), Price Range (10) = 20 × 10 × 5 × 50 × 10 = **5,000,000 URLs**

**Real-world impact:** Facet traversal multiplies crawlable URLs combinatorially — each additional facet with N values multiplies the URL space, so a handful of facets can generate more distinct URLs than the site has content. Distributed crawlers walking that space evict useful entries from the page cache. Measure your own cache hit ratio before and after enabling blocking rather than working from a headline figure.

## Decision: Two Threat Categories

| Threat | Behavior | Goal | robots.txt Respected? |
|---|---|---|---|
| **Search engine bots** (Googlebot, Bingbot) | Follow every link, index every page | Index content | Usually yes |
| **AI scrapers** (GPTBot, ClaudeBot, CCBot, Bytespider, etc.) | Aggressively crawl all reachable URLs | Harvest training data | Often no |

AI bots are now the **bigger threat** — they don't respect robots.txt reliably, they crawl deeper and faster than search engines, and they generate massive server load without any benefit to your site.

## Decision: Protection Strategies (Layered Defense)

| Layer | Strategy | Stops | Effectiveness | Complexity |
|---|---|---|---|---|
| 1 | **robots.txt** | Compliant bots | High for Googlebot | Low |
| 2 | **Facet Bot Blocker module** | Deep facet crawlers | High — blocks at kernel level | Low |
| 3 | **Form-based facets** (exposed filters) | Link-following bots | High — bots don't submit forms | Medium |
| 4 | **Cloudflare WAF / CDN rules** | All bots at edge | Very high — blocks before reaching server | Medium |
| 5 | **Meta robots noindex** | Indexing of crawled pages | Medium — prevents indexing | Medium |
| 6 | **Canonical URLs** | Duplicate content penalties | High — consolidates signals | Medium |
| 7 | **AI bot user-agent blocking** | Known AI scrapers | Medium — user agents can be spoofed | Low |

## Pattern: Layer 1 — robots.txt

Block the facet query parameter pattern. The critical detail: `f[0]` in URLs is encoded as `f%5B0%5D` — you must block **both** patterns:

```
# Block all faceted search URLs (both encoded and unencoded)
Disallow: /*f%5B0%5D*
Disallow: /*?*f[

# Block known AI scrapers entirely
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

# If using pretty paths:
Disallow: /search/facets/
```

**Implementation:** Use the `robotstxt` module to manage robots.txt from the Drupal admin:

```bash
composer require drupal/robotstxt
drush en robotstxt
```

Then edit at `/admin/config/search/robotstxt`.

## Pattern: Layer 2 — Facet Bot Blocker Module

The `facet_bot_blocker` module blocks requests that exceed a configurable facet parameter depth. It operates as a **kernel event subscriber** at priority 101 — blocking requests before Drupal fully bootstraps.

```bash
composer require drupal/facet_bot_blocker
drush en facet_bot_blocker
```

**How it works:** Checks if `$_GET['f'][$limit]` exists. If a request has more facet parameters than the limit, it returns 403 Forbidden or 410 Gone immediately.

**Configuration** at `/admin/config/system/facet-bot-blocker`:

| Setting | Default | Purpose |
|---|---|---|
| Facet parameter limit | 1 | Block if `f[N]` where N >= limit exists |
| Return 410 Gone | FALSE | 410 tells bots the URL is permanently gone (stronger signal than 403) |
| Custom blocked message | `<h1>Excessive crawling detected</h1><p>We have blocked your request.</p>` | HTML returned to blocked requests |

**Example:** With limit set to `2`, these requests are allowed:

- `?f[0]=color:blue` — 1 facet parameter (allowed)
- `?f[0]=color:blue&f[1]=size:large` — 2 parameters (allowed)

But this is blocked:

- `?f[0]=color:blue&f[1]=size:large&f[2]=brand:acme` — 3 parameters (blocked, `f[2]` exceeds limit)

**Dashboard:** `/admin/reports/facet-bot-blocker` shows blocked/allowed request counts, last blocked IP and user agent. Requires Memcache or Redis for metrics storage.

**Permission:** `bypass facet bot blocker` — logged-in users with this permission are never blocked.

**Recommendation:** Use 410 Gone — it tells bots the URL is permanently removed, so they stop trying. 403 may be retried.

## Pattern: Layer 3 — Form-Based Facets (Exposed Filters)

The most architecturally effective defense: **bots don't submit forms**.

Link-based facets render as `<a href="?f[0]=color:blue">Blue</a>` — bots follow these links eagerly. Form-based facets (via `facets_exposed_filters` + BEF) render as `<input type="checkbox">` elements inside a `<form>`. Bots must execute JavaScript and submit the form to trigger filtering.

**Setup:**

```bash
drush en facets_exposed_filters better_exposed_filters
```

Then configure facets as Views exposed filters with BEF widgets (checkboxes, radio buttons, dropdowns).

**Why this works:**

- HTML forms require POST/GET submission — bots that just follow `<a>` tags never trigger them
- BEF's auto-submit requires JavaScript execution
- Checkbox/radio button state is not in the HTML source as a crawlable URL
- Even AI bots that execute JavaScript rarely interact with form elements

**Caveat:** This protection may weaken over time as bots become more sophisticated at form interaction. Use as one layer in a defense-in-depth strategy, not the only layer.

## Pattern: Layer 4 — Cloudflare WAF Rules

Block facet URL patterns at the CDN edge — before requests reach your server:

**Cloudflare Dashboard → Security → WAF → Custom Rules:**

```
Rule name: Block Facet Bot Crawling
Field: URI Query String
Operator: wildcard
Value: *f%5B0%5D*
Action: Managed Challenge
```

"Managed Challenge" shows a CAPTCHA-like challenge to bots while allowing real users through. Use "Block" for more aggressive protection.

**Additional Cloudflare rule for AI bots:**

```
Rule name: Block AI Scrapers
Field: User-Agent
Operator: contains
Value: GPTBot OR ClaudeBot OR CCBot OR Bytespider OR anthropic-ai
Action: Block
```

**Pantheon-specific:** Request AGCDN+WAF configuration via support ticket. Pantheon can apply JA3 fingerprinting to identify bot signatures and deploy VCL (Varnish Control Language) rules.

## Pattern: Layer 5 — Meta Robots noindex

Add noindex to pages with facet parameters — prevents indexing even if bots crawl:

```php
/**
 * Implements hook_page_attachments_alter().
 */
function my_module_page_attachments_alter(array &$attachments) {
  $request = \Drupal::request();
  $facet_params = $request->query->all('f');

  if (!empty($facet_params)) {
    $noindex = [
      '#tag' => 'meta',
      '#attributes' => [
        'name' => 'robots',
        'content' => 'noindex, follow',
      ],
    ];
    $attachments['#attached']['html_head'][] = [$noindex, 'robots_noindex'];
  }
}
```

Or use the `metatag` module configured for search page paths.

## Pattern: Layer 6 — Canonical URLs

Point all faceted variations at the base search page with `rel="canonical"`, so link signals consolidate on one URL instead of scattering across parameter combinations. The implementation — a `hook_page_attachments_alter()` that strips any existing canonical and emits one for the unfiltered path — lives in [Canonical URLs & Duplicate Content](canonical-urls.md).

## Pattern: Recommended Defense Stack (Production)

**The #1 solution is architectural: use facets_exposed_filters + BEF instead of block-based facets.** This eliminates the problem at its root — form-based facets produce NO crawlable facet URLs in the HTML. Link-based block facets produce millions. Everything else in this stack is a mitigation for sites that still use link-based facets, or belt-and-suspenders hardening for sites that have already switched.

| Priority | Layer | What It Stops | Notes |
|---|---|---|---|
| **1** | **Form-based facets (exposed filters + BEF)** | **Eliminates crawlable facet URLs entirely** | **The primary solution — do this first** |
| 2 | Cloudflare WAF rule on `f%5B0%5D` | Bots at edge — zero server load | Defense in depth even with exposed filters |
| 3 | Cloudflare AI bot user-agent blocking | Known AI scrapers | Blocks GPTBot, ClaudeBot, etc. |
| 4 | robots.txt with `Disallow: /*f%5B0%5D*` | Compliant bots | Free, easy, minimal effort |
| 5 | Facet Bot Blocker module (limit: 2, 410 Gone) | Deep crawlers that reach Drupal | Kernel-level, catches anything that slips through |
| 6 | Meta noindex on faceted pages | Prevents indexing of crawled pages | Safety net |
| 7 | Canonical URL to base search page | Consolidates link signals | SEO hygiene |

**Why exposed filters is the primary solution, not just one layer:**

- Block-based facets render as `<a href="?f[0]=color:blue">` — every option is a crawlable link. With 5 facets × 10 options, the HTML contains 50+ links to unique URLs, each of which contains 50+ more.
- Exposed filter facets render as `<input type="checkbox">` inside a `<form>`. No crawlable URLs exist in the HTML at all.
- Bots that follow links will never discover facet URLs because there are no links to follow.
- This is not a band-aid — it's the correct architecture. Layers 2-7 are insurance.

## Common Mistakes

- **No protection at all** — Facets module has ZERO built-in SEO or bot protection. You MUST implement it yourself. This is the single most critical issue with Facets deployments.
- **Only using robots.txt** — AI bots frequently ignore robots.txt. You need server-side and edge-level blocking too.
- **Using 403 instead of 410** — 403 (Forbidden) may be retried. 410 (Gone) tells bots the URL is permanently removed — stronger deindexing signal.
- **Forgetting URL-encoded brackets** — `f[0]` becomes `f%5B0%5D` in URLs. Both patterns must be blocked in robots.txt and WAF rules.
- **Not monitoring** — Use Facet Bot Blocker dashboard, Cloudflare analytics, or server logs to monitor bot traffic patterns. The threat evolves.
- **Blocking too aggressively** — Don't block the base search page. Don't block all query parameters — only the facet `f[]` pattern.
- **Ignoring AI bots entirely** — Traditional SEO advice focuses on Googlebot. In 2025-2026, AI scrapers generate more facet abuse traffic than search engines.

## See Also

- [Canonical URLs & Duplicate Content](canonical-urls.md) — deeper canonical strategy
- [Facets Exposed Filters](facets-exposed-filters.md) — form-based facets as architectural defense
- [Pretty Paths](pretty-paths.md) — cleaner URLs that are easier to block
- [URL Processors](url-processors.md) — how facet URLs are structured
