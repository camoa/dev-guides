---
description: Core Web Vitals optimization for Drupal 11 — LCP, INP, CLS, caching layers, BigPipe, image optimization, CDN, and CSS/JS aggregation
drupal_version: "11.x"
---

# Performance & Core Web Vitals

## When to Use

> Address Core Web Vitals before other SEO work — Google uses them as ranking signals and poor scores actively suppress rankings regardless of content quality. Drupal's caching stack, when configured correctly, solves most performance issues without custom code.

## Decision

| Metric affected | Root cause | Solution |
|-----------------|-----------|----------|
| LCP (slow largest paint) | Uncached TTFB, unoptimized hero image | Enable page cache + CDN, use responsive images with preload |
| LCP (render blocking) | CSS/JS blocking initial render | Enable CSS/JS aggregation, defer non-critical JS |
| INP (slow interactions) | Heavy JS on interaction, no BigPipe | Defer JS, use BigPipe for personalized blocks |
| CLS (layout shift) | Images without dimensions, web fonts FOUT | Always set width/height on img elements, use font-display: swap |
| TTFB > 600ms | Dynamic page cache miss, no reverse proxy | Enable Dynamic Page Cache, add Varnish/CDN layer |
| Slow for authenticated users | Render cache miss on user-specific blocks | BigPipe + per-user render cache tags |

## Core Web Vitals — Drupal Context

### LCP (Largest Contentful Paint)
Target: under 2.5s. In Drupal, LCP is usually the hero image or H1. Failures come from:
- Page cache disabled (every request hits PHP)
- Hero image not preloaded
- Unoptimized image format (JPEG instead of WebP/AVIF)

### INP (Interaction to Next Paint)
Target: under 200ms. Replaces FID as of March 2024. Drupal-specific risks:
- jQuery-heavy themes running on every click
- AJAX callbacks with no loading indicators
- Drupal behaviors re-attaching on full page content

### CLS (Cumulative Layout Shift)
Target: under 0.1. Drupal-specific risks:
- Images without width/height attributes (common in CKEditor content)
- Lazy-loaded above-the-fold images shifting content
- Cookie consent banners injecting above-the-fold content

## Pattern

### Drupal Caching Stack

Enable all three caching layers at `/admin/config/development/performance`:

```php
# settings.php — production caching
$settings['cache']['default'] = 'cache.backend.database';

// For Memcache/Redis (recommended for high traffic):
$settings['cache']['default'] = 'cache.backend.memcache';
```

| Cache Layer | Scope | What It Caches |
|-------------|-------|----------------|
| Page Cache | Anonymous users | Full HTML responses — fastest possible |
| Dynamic Page Cache | All users | Partial responses, personalized blocks excluded |
| Render Cache | All users | Individual render elements, survives page rebuilds |

Enable at: `/admin/config/development/performance` → check both "Cache pages for anonymous users" and "Cache blocks"

Verify page cache is working:
```bash
curl -I https://example.com/ | grep X-Drupal-Cache
# Should return: X-Drupal-Cache: HIT
```

### BigPipe

BigPipe renders placeholders for personalized content and streams them after the initial page. Enable it for any site with authenticated users or personalized blocks.

```bash
drush en big_pipe
```

No additional configuration needed. BigPipe automatically identifies uncacheable placeholders (lazy builder callbacks) and defers them via streaming. Verify in browser: personalized content (e.g., "Hello, [username]") should appear after the main page paints.

### Image Optimization

**Responsive Images module** (Drupal core):

```bash
drush en responsive_image
```

Configure image styles and responsive image styles at:
`/admin/config/media/responsive-image-style`

Map to content at:
`/admin/structure/types/manage/[type]/display` → set field formatter to "Responsive image"

**WebP/AVIF via ImageAPI Optimize or similar:**

```bash
composer require drupal/imageapi_optimize_webp
drush en imageapi_optimize_webp
```

Configure at: `/admin/config/media/imageapi-optimize`

**Lazy loading** — Drupal 9.1+ adds `loading="lazy"` automatically to img elements below the fold. For hero images (above the fold), explicitly set `loading="eager"` and add a preload hint:

```html
<!-- In your theme's html.html.twig or via hook_page_attachments -->
<link rel="preload" as="image" href="/sites/default/files/hero.webp" fetchpriority="high">
```

**Always set image dimensions** — prevents CLS:
```html
<!-- Wrong — causes layout shift -->
<img src="hero.jpg" alt="Hero">

<!-- Right — reserves space before image loads -->
<img src="hero.jpg" alt="Hero" width="1200" height="630">
```

### CSS/JS Aggregation

Enable at: `/admin/config/development/performance`

- "Aggregate CSS files" — merges all CSS into fewer requests
- "Aggregate JavaScript files" — merges and defers JS

```php
# settings.php — ensure aggregation is on in production
$config['system.performance']['css']['preprocess'] = TRUE;
$config['system.performance']['js']['preprocess'] = TRUE;
```

For render-blocking JS, use the `defer` or `async` attribute in your library definition:

```yaml
# mytheme.libraries.yml
non-critical:
  js:
    js/non-critical.js:
      attributes:
        defer: true
```

See [Defer and Async Attributes](../../drupal/js-development/defer-and-async-attributes.md) for the full decision.

### CDN Integration

A CDN in front of Drupal (Cloudflare, Fastly, AWS CloudFront) is the single highest-impact performance change for LCP:

1. All static assets (CSS, JS, images) served from edge nodes near users
2. Full-page caching possible for anonymous users
3. TTFB drops from 200-800ms to 10-50ms

Drupal modules for CDN integration:
- `drupal/cdn` — rewrites asset URLs to CDN domain
- `drupal/fastly` — Fastly API integration with purge support
- `drupal/cloudflare` — cache purge on node save

Recommended pattern: configure the CDN to cache anonymous responses (matching `X-Drupal-Cache: HIT`), purge on node save via webhook or Drupal module.

## Common Mistakes

- **Wrong**: Running with `$settings['cache']['default'] = 'cache.backend.null'` in production → **Right**: Only disable caches locally in `settings.local.php`
- **Wrong**: Lazy loading hero/LCP images → **Right**: Hero images need `loading="eager"` and a `<link rel="preload">` — lazy loading the LCP element is a common mistake that kills scores
- **Wrong**: No image dimensions in CKEditor body content → **Right**: Train editors to set alt and dimensions, or use the CKEditor 5 image resize plugin
- **Wrong**: Enabling BigPipe but not testing with authenticated users → **Right**: Test the authenticated page experience — BigPipe must not stream broken placeholders
- **Wrong**: Aggregating CSS/JS in development → **Right**: Disable aggregation locally (`settings.local.php`), enable in production `settings.php`
- **Wrong**: Relying on Drupal page cache alone without a reverse proxy → **Right**: Drupal page cache still runs PHP for every request; a reverse proxy (Varnish, CDN) serves without PHP

## See Also

- [SEO Audit Workflow](seo-audit-workflow.md) — measuring and tracking Web Vitals scores
- [XML Sitemap](xml-sitemap.md) — sitemap correctness as a crawl efficiency signal
- Reference: [Google Core Web Vitals overview](https://web.dev/articles/vitals)
- Reference: [Drupal Performance documentation](https://www.drupal.org/docs/administering-a-drupal-site/managing-site-performance-and-scalability)
- Reference: [BigPipe module](https://www.drupal.org/docs/8/core/modules/big-pipe/overview)
- Reference: [Responsive Image module](https://www.drupal.org/docs/8/core/modules/responsive-image)
