---
description: "Source references and maintenance manifest for the caching guides — web sources, code sources, and version history"
---

# Sources & Maintenance

## Drupal Research Install

Path: `/home/camoa/workspace/contrib/web/`

## Web Sources

| Source | URL | Guide Sections | Last Verified |
|--------|-----|----------------|---------------|
| Drupal Cache API documentation | https://www.drupal.org/docs/8/api/cache-api/cache-api | 1, 2, 17 | 2026-02-14 |
| Cacheability of render arrays | https://www.drupal.org/docs/drupal-apis/render-api/cacheability-of-render-arrays | 2, 8, 9 | 2026-02-14 |
| Cache tags documentation | https://www.drupal.org/docs/drupal-apis/cache-api/cache-tags | 3, 14, 15 | 2026-02-14 |
| Cache contexts documentation | https://www.drupal.org/docs/develop/drupal-apis/cache-api/cache-contexts | 4, 17 | 2026-02-14 |
| Cache max-age documentation | https://www.drupal.org/docs/develop/drupal-apis/cache-api/cache-max-age | 5 | 2026-02-14 |
| Dynamic Page Cache overview | https://www.drupal.org/docs/8/core/modules/dynamic-page-cache/overview | 12 | 2026-02-14 |
| Internal Page Cache documentation | https://www.drupal.org/docs/administering-a-drupal-site/internal-page-cache | 11 | 2026-02-14 |
| Drupal BigPipe documentation | https://www.drupal.org/docs/8/core/modules/big-pipe | 13 | 2026-02-14 |
| Auto-placeholdering documentation | https://www.drupal.org/docs/drupal-apis/render-api/auto-placeholdering | 10 | 2026-02-14 |
| Add cache metadata tutorial (Drupalize.me) | https://drupalize.me/tutorial/add-cache-metadata-render-arrays | 2, 17 | 2026-02-14 |
| Drupal caching best practices (Pantheon) | https://pantheon.io/learning-center/drupal/caching | 1, 17 | 2026-02-14 |
| Cache system for Drupal 10 | https://www.digitalprojex.com/blog/cache-system-drupal-10-optimizing-your-websites-performance | 6, 16 | 2026-02-14 |
| Redis module project page | https://www.drupal.org/project/redis | 6, 16 | 2026-02-14 |
| Memcache module project page | https://www.drupal.org/project/memcache | 6, 16 | 2026-02-14 |
| Setting Up Redis Caching with Drupal | https://www.markdorison.com/articles/setting-up-redis-caching-with-drupal/ | 16 | 2026-02-14 |
| Drupal BigPipe lazy builders (Droptica) | https://www.droptica.com/blog/drupal-bigpipe-using-lazy-builders-2023/ | 10, 13 | 2026-02-14 |
| Enhancing Website Performance with BigPipe | https://www.thedroptimes.com/34003/enhancing-website-performance-with-drupals-bigpipe-and-lazy-builders | 13 | 2026-02-14 |
| Drupal 11.3.0 performance improvements | https://www.drupal.org/about/core/blog/drupal-1130-biggest-performance-boost-in-a-decade | 13 | 2026-02-14 |
| Choosing the right Cache Backend | https://www.qed42.com/insights/choosing-the-right-cache-backend-for-your-drupal-site | 6 | 2026-02-14 |
| Drupal speed optimization guide (David Loor) | https://davidloor.com/en/blog/drupal-caching-opcache-apcu-redis-memcached-guide | 6, 16 | 2026-02-14 |
| Cache tags + Varnish | https://www.drupal.org/docs/develop/drupal-apis/cache-api/cache-tags-varnish | 3 | 2026-02-14 |
| OWASP Session Management | https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html | 19 | 2026-02-14 |
| Drupal security best practices | https://www.drupal.org/security/secure-configuration | 19 | 2026-02-14 |

## Code Sources

| Module | Relative Path | Guide Sections | Drupal Version |
|--------|---------------|----------------|----------------|
| Core Cache API | `core/lib/Drupal/Core/Cache/` | 1, 2, 3, 4, 5, 6, 7, 8, 9, 14, 15, 20 | 11.x |
| Core Render | `core/lib/Drupal/Core/Render/` | 8, 9, 10, 20 | 11.x |
| Page Cache module | `core/modules/page_cache/` | 11, 20 | 11.x |
| Dynamic Page Cache module | `core/modules/dynamic_page_cache/` | 12, 20 | 11.x |
| BigPipe module | `core/modules/big_pipe/` | 10, 13, 20 | 11.x |
| Core services | `core/core.services.yml` | 6, 7, 20 | 11.x |
| Default settings | `sites/default/default.settings.php` | 16 | 11.x |

<!-- END PARTITION: sources-maintenance -->
