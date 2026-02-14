---
description: "Reference sources and maintenance manifest for the Next.js for Drupal guide, including web sources, code modules, and version compatibility."
drupal_version: "11.x"
topic: "drupal/next-drupal"
---

## Sources & Maintenance Manifest

### Drupal Research Install

Path: /home/camoa/workspace/contrib/web/

**Note:** The `next` and `decoupled_router` modules were not found in the current research install. To install for code reference:

```bash
cd /home/camoa/workspace/contrib/web
composer require drupal/next drupal/simple_oauth drupal/jsonapi_menu_items drupal/jsonapi_views drupal/jsonapi_search_api
```

### Web Sources

| Source | URL | Guide Sections | Last Verified |
|--------|-----|----------------|---------------|
| Next.js for Drupal Official Site | https://next-drupal.org/ | All sections | 2026-02-13 |
| Next.js for Drupal Drupal.org Module | https://www.drupal.org/project/next | Drupal Setup, Version Compatibility | 2026-02-13 |
| Chapter Three next-drupal GitHub | https://github.com/chapter-three/next-drupal | NextDrupal Client, API Reference | 2026-02-13 |
| Next-Drupal Quick Start Guide | https://next-drupal.org/learn/quick-start | Drupal Setup, Next.js Project Setup | 2026-02-13 |
| BRAINSUM: Decoupled Architecture with Next.js and Drupal | https://www.brainsum.com/blog/harnessing-power-decoupled-architecture-nextjs-and-drupal | Decoupled Architecture Decision | 2026-02-13 |
| Axelerant: Decoupled Drupal with Next.js | https://www.axelerant.com/blog/decoupled-drupal-nextjs-using-next-drupal | Architecture Patterns | 2026-02-13 |
| QED42: Next.js 15 App Router Integration | https://www.qed42.com/insights/seamless-headless-drupal-integration-with-next-js-15-app-router | Building Pages (App Router) | 2026-02-13 |
| Chapter Three: Next-Drupal 2.0 Release | https://www.chapterthree.com/blog/next-drupal-20-making-a-good-thing-even-better | Version 2.0 Features, App Router Support | 2026-02-13 |
| Drupal.org: Decoupled Router Issue #3111456 | https://www.drupal.org/project/decoupled_router/issues/3111456 | Multilingual Support Patch | 2026-02-13 |

### Code Sources

| Module | Relative Path | Guide Sections | Drupal Version |
|--------|---------------|----------------|----------------|
| next | modules/contrib/next | Drupal Setup, Draft Mode, On-Demand Revalidation | ^10 \|\| ^11 |
| simple_oauth | modules/contrib/simple_oauth | Authentication Patterns | ^6.0 |
| decoupled_router | modules/contrib/decoupled_router | Path Resolution, Multilingual Support | Core dependency |
| jsonapi_menu_items | modules/contrib/jsonapi_menu_items | Fetching Content (getMenu) | Recommended |
| jsonapi_views | modules/contrib/jsonapi_views | Fetching Content (getView) | Recommended |
| jsonapi_search_api | modules/contrib/jsonapi_search_api | Search Integration | Optional |
| jsonapi_search_api_facets | modules/contrib/jsonapi_search_api_facets | Search Integration (Facets) | Optional |
| webform_rest | modules/contrib/webform_rest | Webform Integration | Optional |

**Next.js Library:**
- Package: `next-drupal` (npm)
- Repository: https://github.com/chapter-three/next-drupal
- Latest Version: 2.0.1 (supports Next.js 15, App Router, Drupal 11)
- All Sections

**Related Guides:**
- drupal-jsonapi.md (for JSON:API parameter syntax, filtering, relationships)
