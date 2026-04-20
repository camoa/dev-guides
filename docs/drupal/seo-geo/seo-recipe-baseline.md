---
description: Drupal CMS SEO recipes — what drupal_cms_seo_basic and drupal_cms_seo_tools install, decision to apply both vs selective, and what config you get out of the box
tldr: "Start here when setting up SEO for any Drupal 11.3+ site. The two Drupal CMS SEO recipes give you a battle-tested module stack with sane defaults in minutes."
drupal_version: "11.x"
---

# SEO Recipe Baseline

## When to Use

> Start here when setting up SEO for any Drupal 11.3+ site. The two Drupal CMS SEO recipes give you a battle-tested module stack with sane defaults in minutes. Apply both for a complete SEO foundation, or selectively require individual modules if the full stack is too heavy.

## Decision

| Situation | Choice | Why |
|-----------|--------|-----|
| New Drupal 11.3+ site, want full SEO stack | Apply both recipes | Opinionated defaults for every SEO layer — paths, redirects, breadcrumbs, meta tags, sitemaps, content scoring |
| Existing site, avoid conflicts | Apply `seo_basic` only | Pathauto + Redirect + Easy Breadcrumb are safe to add to any site |
| Already have Metatag configured | Skip `seo_tools` or apply selectively | Recipes import config; may overwrite your existing Metatag defaults |
| Headless / decoupled Drupal | Apply `seo_basic` only | Metatag and Yoast output HTML — irrelevant for headless; Pathauto + Redirect still matter |
| Drupal < 11.3 | Manual module install | Recipes require Drupal 11.3+ core recipe support |

## Pattern

**Require and apply both recipes:**

```bash
composer require drupal/drupal_cms_seo_basic drupal/drupal_cms_seo_tools
drush recipe recipes/contrib/drupal_cms_seo_basic
drush recipe recipes/contrib/drupal_cms_seo_tools
drush cr
```

**Apply only the basic recipe (paths + redirects + breadcrumbs):**

```bash
composer require drupal/drupal_cms_seo_basic
drush recipe recipes/contrib/drupal_cms_seo_basic
drush cr
```

**What each recipe installs:**

| Recipe | Modules | Config provided |
|--------|---------|-----------------|
| `drupal_cms_seo_basic` | Pathauto, Redirect, Easy Breadcrumb, Token | Pathauto patterns for nodes/taxonomy/users; redirect on alias change enabled; breadcrumb settings |
| `drupal_cms_seo_tools` | Metatag, Yoast SEO (Real-time SEO), Simple Sitemap, SEO Checklist, ECA, Field Group, Focal Point | Global/content-type Metatag defaults with tokens; sitemap config including all entity types; Focal Point image crop settings |

**Out-of-the-box config from `drupal_cms_seo_basic`:**

- Pathauto node pattern: `/[node:content-type]/[node:title]`
- Pathauto taxonomy pattern: `/[term:vocabulary]/[term:name]`
- Redirect module with auto-redirect on alias change enabled
- Easy Breadcrumb with home segment, title segment, and path-based segments

**Out-of-the-box config from `drupal_cms_seo_tools`:**

- Metatag global defaults: title `[node:title] | [site:name]`, description `[node:summary]`
- Metatag front page defaults with site name and description
- Simple Sitemap configured to include all node types, taxonomy terms, and the front page
- Yoast SEO widget added to node edit forms for content scoring
- SEO Checklist task list available at `/admin/config/search/seo-checklist`

## Common Mistakes

- **Wrong**: Running `drush recipe` without `composer require` first → **Right**: The recipe package must be downloaded before Drush can apply it
- **Wrong**: Applying `drupal_cms_seo_tools` on a site with existing Metatag config → **Right**: Back up your Metatag config first; recipes import config that can overwrite defaults
- **Wrong**: Expecting recipes to work on Drupal < 11.3 → **Right**: Upgrade to 11.3+ or install modules manually with custom config
- **Wrong**: Re-running a recipe expecting it to update an already-applied config → **Right**: Recipes are applied once; subsequent config changes go through the normal config management workflow

## See Also

- [Pathauto Patterns](pathauto-patterns.md) — configure URL alias patterns after applying the recipe
- [Redirect Management](redirect-management.md) — manage manual redirects and 404 logs
- [Metatag Architecture](metatag-architecture.md) — customize the Metatag defaults the recipe installs
- Reference: [drupal_cms_seo_basic on drupal.org](https://www.drupal.org/project/drupal_cms_seo_basic)
- Reference: [drupal_cms_seo_tools on drupal.org](https://www.drupal.org/project/drupal_cms_seo_tools)
- Reference: [Drupal CMS Recipe documentation](https://www.drupal.org/docs/distributions-recipes/drupal-cms/get-started)
