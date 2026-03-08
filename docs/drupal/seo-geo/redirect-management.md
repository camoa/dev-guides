---
description: Drupal redirect management — manual redirects, redirect_404 submodule for 404 logging, auto-redirect on alias change, 301 vs 302 decision, and domain migrations
drupal_version: "11.x"
---

# Redirect Management

## When to Use

> Use the Redirect module whenever URL aliases change, content moves, or domains migrate. A site without redirect management bleeds SEO equity every time a URL changes — search engines and users hit 404s that could be 301s.

## Decision

| Situation | Choice | Why |
|-----------|--------|-----|
| Alias changes on an existing node | Auto-redirect (Pathauto integration) | Redirect module creates a 301 automatically on save — zero manual work |
| Moving content from one URL to another permanently | 301 Permanent redirect | Transfers ~95% of link equity to destination; tells crawlers to update their index |
| Temporary campaign URL or A/B test | 302 Temporary redirect | No equity transfer; crawlers keep crawling the source |
| Bulk 404 errors from a migration | redirect_404 submodule | Logs 404s with referrer data; batch-fix by assigning destinations in admin UI |
| Domain migration (old.com → new.com) | Redirect Domain submodule | Server-level domain redirect with proper 301 handling |
| Internal search result pages, session URLs | No redirect — noindex instead | Redirecting dynamic URLs is fragile; noindex is the right tool |

## Pattern

**Manual redirect** at `admin/config/search/redirect/add`:

```
From: /old-path
To: /new-path (or external URL)
Status: 301 Moved Permanently
Language: <language-agnostic> unless multilingual
```

**Auto-redirect on alias change** — enable in Pathauto settings at `admin/config/search/path/settings`:

- Check "Automatically create redirects when URL aliases are changed"
- Requires Redirect module to be enabled

**redirect_404 workflow** at `admin/config/search/redirect/404`:

1. Let crawlers and real traffic generate 404s for a few days
2. Review the log — entries show the 404 path, referrer, and hit count
3. Prioritize by hit count; high-traffic 404s get fixed first
4. For each 404 path, click "Add redirect" to assign a destination inline
5. Bulk-delete low-count 404 entries with no referrer (likely bots scanning)

**Redirect Domain submodule** — handles domain-level redirects:

```
Enable: Redirect Domain (included with Redirect module package)
Config at: admin/config/search/redirect/domain
Add: old.com → https://new.com (301)
```

Note: Redirect Domain works at the Drupal routing layer. For high-traffic migrations, pair with a web server (nginx/Apache) level redirect to avoid Drupal bootstrap overhead.

## Common Mistakes

- **Wrong**: Using 302 for permanent content moves → **Right**: 302 does not transfer link equity; Google will keep crawling the source URL indefinitely
- **Wrong**: Creating a redirect chain (A → B → C) → **Right**: Point A directly to C; chains add latency and each hop loses a small percentage of equity. The redirect_404 log reveals chains — trace and collapse them
- **Wrong**: Redirect module installed but auto-redirect not enabled in Pathauto → **Right**: Auto-redirect is a Pathauto setting, not a Redirect module setting; enable it at `admin/config/search/path/settings`
- **Wrong**: Ignoring redirect_404 after a migration → **Right**: Monitor for 2–4 weeks post-launch; the first wave of crawlers will reveal all the URLs you missed
- **Wrong**: Creating redirects for every variation of trailing slashes and www/non-www at the Drupal level → **Right**: Handle www and trailing slash normalization at the web server or CDN layer; Drupal-level redirects for these add unnecessary database queries

## See Also

- [Pathauto Patterns](pathauto-patterns.md) — auto-redirect integrates with Pathauto alias changes
- [SEO Recipe Baseline](seo-recipe-baseline.md) — Redirect is installed by `drupal_cms_seo_basic`
- [Canonical URLs](canonical-urls.md) — domain canonicalization strategy
- Reference: [Redirect module on drupal.org](https://www.drupal.org/project/redirect)
- Reference: [Google: Redirects and Google Search](https://developers.google.com/search/docs/crawling-indexing/301-redirects)
