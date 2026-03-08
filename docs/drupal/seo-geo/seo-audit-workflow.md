---
description: SEO audit workflow for Drupal 11 — SEO Checklist module, Real-time SEO content scoring, manual audit checklist, Google Search Console, and ongoing monitoring
drupal_version: "11.x"
---

# SEO Audit Workflow

## When to Use

> Run an SEO audit at site launch, after major content migrations, and quarterly thereafter. Drupal provides two complementary module-based audit tools — SEO Checklist for configuration audits and Real-time SEO (Yoast) for per-content scoring — plus Google Search Console for live crawl data.

## Decision

| Audit goal | Tool | When to run |
|------------|------|-------------|
| Site configuration completeness | SEO Checklist module | Launch + quarterly |
| Per-content optimization scoring | Real-time SEO (Yoast) module | When editing content |
| Crawl errors, coverage gaps | Google Search Console | Weekly monitoring |
| Core Web Vitals at scale | Google Search Console + PageSpeed Insights | Monthly |
| Broken links, redirect chains | Screaming Frog or Ahrefs | Pre-launch + quarterly |
| Structured data errors | Google Rich Results Test | After schema changes |
| Full technical SEO crawl | Screaming Frog (paid) or Ahrefs | Quarterly |

## Pattern

### SEO Checklist Module (5.2.x)

The SEO Checklist module (`drupal/seo_checklist`) provides a task-based configuration audit at:
`/admin/config/search/seo-checklist`

```bash
composer require drupal/seo_checklist:^5.2
drush en seo_checklist
```

The checklist covers 7 categories with actionable items. Items auto-check when the module is installed:

| Category | Key checks |
|----------|-----------|
| Paths | Pathauto installed, clean URLs enabled |
| Metatag | Metatag module, global defaults configured |
| Sitemap | Simple Sitemap installed, submitted to Search Console |
| Analytics | Google Analytics / Matomo connected |
| Webmaster Tools | Search Console verification |
| Performance | Page caching enabled, CSS/JS aggregation on |
| Content | XML sitemap, breadcrumbs, canonical URLs |

Work through unchecked items in order — earlier items unblock later ones.

### Real-time SEO (Yoast) — Content Scoring

The `drupal/yoast_seo` module (Real-time SEO for Drupal) adds a scoring widget to node edit forms. Installed by the `drupal_cms_seo_tools` recipe.

```bash
composer require drupal/yoast_seo
drush en yoast_seo
```

Configure at: `/admin/config/search/yoast_seo`
- Enable per content type at: `/admin/structure/types/manage/[type]/fields`
- Add the "Real-time SEO" field to the content type form display

**Scoring categories** (0-100):
- **Readability** — sentence length, passive voice, subheadings, paragraph length
- **SEO** — focus keyphrase in title/URL/meta description, internal links, outbound links, image alt text

**Target:** Green indicator (good) for cornerstone content; orange (OK) is acceptable for supporting content.

Editor workflow:
1. Set **Focus Keyphrase** before writing
2. Draft content, watching the live score panel
3. Aim for green on readability and SEO before publishing
4. Use the score as a guide, not a rule — natural writing beats keyword stuffing

### Manual Pre-Launch Audit Checklist

Run this checklist before every site launch:

**Meta Tags**
- [ ] Metatag global defaults set (title template, description token)
- [ ] Per content type defaults configured for articles, pages
- [ ] No empty meta descriptions (check with `drush sql:query "SELECT nid FROM node WHERE ..."` or Screaming Frog)
- [ ] Open Graph tags rendering with correct image (test with Facebook Sharing Debugger)

**Structured Data**
- [ ] Schema Metatag installed and Article/WebPage configured
- [ ] Organization schema set with logo and name
- [ ] Google Rich Results Test returns no errors for sample pages
- [ ] BreadcrumbList JSON-LD present on interior pages

**Technical**
- [ ] Sitemap at `/sitemap.xml` — all content types included, no private content
- [ ] Sitemap submitted in Google Search Console
- [ ] robots.txt: admin paths disallowed, sitemap referenced
- [ ] Canonical URLs correct on node pages (`[node:url]` not `/node/123`)
- [ ] No www/non-www duplicates (test both with curl)
- [ ] 301 redirects in place for any URL changes from previous site
- [ ] Core Web Vitals: LCP < 2.5s, INP < 200ms, CLS < 0.1 (PageSpeed Insights)

**Content**
- [ ] All images have alt text
- [ ] No broken internal links
- [ ] Cornerstone pages have internal links pointing to them

### Google Search Console Integration

1. Verify ownership at `https://search.google.com/search-console/`
   - Recommended: DNS TXT record verification (survives site changes)
   - Alternative: HTML meta tag via Metatag module `[site:google-site-verification]`
2. Submit sitemap: Search Console → Sitemaps → add `/sitemap.xml`
3. Request indexing for key pages after launch

**Weekly monitoring in Search Console:**
- Coverage report — identify pages with crawl errors or "excluded" status
- Core Web Vitals report — URL-level data over real users (28-day window)
- Search performance — impressions, clicks, average position per query
- Manual Actions — check for penalties before they surprise you

### Ongoing Monitoring Pattern

| Cadence | Task | Tool |
|---------|------|------|
| Weekly | Check coverage errors, crawl anomalies | Google Search Console |
| Monthly | Core Web Vitals scores across top pages | Search Console + PageSpeed API |
| Quarterly | Full crawl: broken links, redirect chains, thin content | Screaming Frog |
| On content change | Per-page score before publishing | Real-time SEO (Yoast) |
| On schema change | Validate rich results | Google Rich Results Test |

## Common Mistakes

- **Wrong**: Running the SEO Checklist once at launch and ignoring it → **Right**: Revisit quarterly — new modules and content patterns introduce new gaps
- **Wrong**: Treating the Yoast green score as mandatory for all content → **Right**: Cornerstone and conversion-critical content earns the investment; blog posts and supporting pages at orange is fine
- **Wrong**: Verifying Search Console ownership with an HTML file → **Right**: Use DNS TXT record — it survives theme changes, server migrations, and domain moves
- **Wrong**: Only checking desktop PageSpeed scores → **Right**: Mobile scores determine your ranking; always test mobile first
- **Wrong**: Ignoring the "Valid with warnings" structured data status → **Right**: Warnings in Rich Results Test often indicate missing recommended properties that improve rich result eligibility

## See Also

- [Performance & Core Web Vitals](performance-core-web-vitals.md) — fixing the performance issues the audit surfaces
- [XML Sitemap](xml-sitemap.md) — sitemap configuration for Search Console submission
- [Canonical URLs](canonical-urls.md) — fixing duplicate content issues surfaced in the audit
- [SEO Recipe Baseline](seo-recipe-baseline.md) — the recipe installs SEO Checklist and Real-time SEO
- Reference: [SEO Checklist module](https://www.drupal.org/project/seo_checklist)
- Reference: [Real-time SEO (Yoast) module](https://www.drupal.org/project/yoast_seo)
- Reference: [Google Search Console](https://search.google.com/search-console/)
- Reference: [PageSpeed Insights](https://pagespeed.web.dev/)
