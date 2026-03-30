---
description: Install Facets with Search API, configure prerequisites, and choose block-based vs exposed filter vs REST approach
drupal_version: "11.x"
---

# Installation & Setup

## When to Use

> Use this guide when setting up Facets on a Drupal site with Search API.

## Decision

| Approach | When to Use | AJAX | Setup Complexity |
|---|---|---|---|
| **Exposed Filters** (3.x recommended) | Standard search pages with AJAX | Yes (native Views AJAX) | Low — add as Views filter criteria |
| **Block-based** (2.x style) | Custom layouts, Layout Builder, sidebars | No | Medium — place blocks in regions |
| **REST** | Headless/decoupled frontends | N/A | Medium — configure REST display |

## Pattern

```bash
# Install Facets (requires Search API)
composer require drupal/facets drupal/search_api

# For exposed filters integration (recommended):
composer require drupal/better_exposed_filters

# Enable modules
drush en search_api facets

# For exposed filters:
drush en facets_exposed_filters better_exposed_filters

# For summary (active filter breadcrumbs):
drush en facets_summary

# For range sliders:
drush en facets_range_widget
```

**Prerequisites Checklist:**

| Step | Action | Where |
|---|---|---|
| 1 | Create a Search API server | `/admin/config/search/search-api` |
| 2 | Create a Search API index | `/admin/config/search/search-api/add-index` |
| 3 | Add fields to the index | Index → Fields tab |
| 4 | Index the content | Index → View tab → "Index now" |
| 5 | Create a View using the index | Views → Add (select the search index as source) |
| 6 | Save the View | Must save before adding facets |
| 7 | Create facets | `/admin/config/search/facets/add-facet` |

**Admin Routes:**

| Route | Purpose |
|---|---|
| `/admin/config/search/facets` | Facet listing and management |
| `/admin/config/search/facets/add-facet` | Create new facet |
| `/admin/config/search/facets/{facet}/edit` | Edit facet configuration |
| `/admin/config/search/facets/facet-sources/{source}/edit` | Configure facet source |

## Common Mistakes

- **Wrong**: Creating facets before saving the View → **Right**: You must save the View before facets can see it as a source. Sources are only generated for saved Views displays.
- **Wrong**: Adding facets without reindexing after adding fields → **Right**: After adding fields to the index, reindex. Facets only show results for indexed content.
- **Wrong**: Using Database server for production range/hierarchy facets → **Right**: For production, use Solr or Elasticsearch. Some facet features (hierarchy, range) work better with Solr.

## See Also

- [Facet Sources](facet-sources.md) — connecting facets to your View
- [Facets Exposed Filters](facets-exposed-filters.md) — exposed filter approach
