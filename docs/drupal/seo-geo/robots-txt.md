---
description: robots.txt configuration for Drupal 11 — core file, custom rules, sitemap reference, and AI crawler policies
drupal_version: "11.x"
---

# Robots.txt

## When to Use

> Configure robots.txt on every Drupal site before launch. It controls which paths search engines crawl. The default Drupal core `robots.txt` covers common admin paths — extend it for site-specific private areas, staging environments, and AI crawler policies.

## Decision

| Situation | Choice | Why |
|-----------|--------|-----|
| Standard Drupal site | Edit core robots.txt directly | Simplest — it ships with sensible defaults |
| Drupal CMS with seo_tools recipe applied | Use robots.append.txt | Recipe manages the base; append.txt for custom rules |
| Staging / dev environment | Disallow all crawlers | Prevent indexing of non-production content |
| Need AI crawler-specific rules | robots.txt + per-agent Disallow | Training bots vs search bots need separate rules |
| Composer-managed project overwriting robots.txt | robots.txt via scaffolding config | Prevent composer from resetting your edits |

## Pattern

### Core robots.txt Location

Drupal ships `robots.txt` in the webroot. Its default rules:

```
User-agent: *
Crawl-delay: 10

# Drupal admin and system paths
Disallow: /admin/
Disallow: /comment/reply/
Disallow: /filter/tips
Disallow: /node/add/
Disallow: /search/
Disallow: /user/register
Disallow: /user/password
Disallow: /user/login
Disallow: /user/logout

# Files directories
Disallow: /sites/*/files/private/

# Sitemap reference (add this)
Sitemap: https://example.com/sitemap.xml
```

### drupal_cms_seo_tools — robots.append.txt

When using the `drupal_cms_seo_tools` recipe, custom rules go in `robots.append.txt` (project webroot). The recipe merges this file with core robots.txt during deployment:

```
# robots.append.txt — project-specific additions

# Block access to private staging areas
Disallow: /stage/
Disallow: /preview/

# AI crawler policies — see ai-crawler-policy.md for full list
User-agent: GPTBot
Disallow: /

User-agent: Google-Extended
Disallow: /

User-agent: ClaudeBot
Disallow: /
```

### Essential Rules to Always Include

```
# Admin UI — always block
Disallow: /admin/
Disallow: /node/*/edit
Disallow: /node/*/delete

# System paths
Disallow: /batch
Disallow: /cron/
Disallow: /update.php
Disallow: /install.php

# Private files
Disallow: /sites/*/files/private/

# Views exposed filters (prevent crawl traps)
Disallow: *?*

# Sitemap — always include
Sitemap: https://example.com/sitemap.xml
```

### Staging Environment — Block Everything

```
# robots.txt for staging.example.com
User-agent: *
Disallow: /
```

Set this via environment-specific file or server configuration — do not rely solely on robots.txt as it is not enforced.

### Protecting robots.txt from Composer Scaffold Overwriting

Add to `composer.json` to prevent Drupal scaffold from resetting your robots.txt:

```json
"drupal-scaffold": {
  "file-mapping": {
    "[webroot-dir]/robots.txt": false
  }
}
```

## Common Mistakes

- **Wrong**: Disallowing `/sites/default/files/` entirely → **Right**: Only disallow `/sites/*/files/private/` — public media should be crawlable
- **Wrong**: Using robots.txt as a security mechanism → **Right**: Robots.txt is advisory only; use access control for real security
- **Wrong**: Forgetting the `Sitemap:` directive → **Right**: Add it so crawlers auto-discover without Search Console submission
- **Wrong**: Wildcard `Disallow: *?*` on sites using query parameters for canonical content → **Right**: Only block faceted navigation query parameters, not all query strings
- **Wrong**: Same robots.txt on production and staging → **Right**: Staging must disallow all crawlers to prevent duplicate content indexing

## See Also

- [AI Crawler Policy](ai-crawler-policy.md) — full table of AI crawler user agents and recommended rules
- [XML Sitemap](xml-sitemap.md) — generating the sitemap to reference here
- [Canonical URLs](canonical-urls.md) — duplicate content prevention at the URL level
- Reference: [Google robots.txt specification](https://developers.google.com/search/docs/crawling-indexing/robots/intro)
- Reference: [Drupal core robots.txt](https://git.drupalcode.org/project/drupal/-/blob/11.x/robots.txt)
