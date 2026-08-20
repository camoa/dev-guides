---
description: "Installing Facets and Search API, and the prerequisite steps before creating your first facet"
tldr: "Use this guide when setting up Facets on a Drupal site with Search API. Facets requires a saved View on an indexed Search API source before facets can be created against it."
drupal_version: "11.x"
---

# Installation & Setup

## When to Use

> When setting up Facets on a Drupal site with Search API.

These guides document **Facets 3.0.4**, the current stable tag on the 3.x branch. Where they say "3.x" they mean a behaviour that holds across the branch, not a looser version claim.

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

**Prerequisites checklist:**

| Step | Action | Where |
|---|---|---|
| 1 | Create a Search API server | `/admin/config/search/search-api` |
| 2 | Create a Search API index | `/admin/config/search/search-api/add-index` |
| 3 | Add fields to the index | Index → Fields tab |
| 4 | Index the content | Index → View tab → "Index now" |
| 5 | Create a View using the index | Views → Add (select the search index as source) |
| 6 | Save the View | Must save before adding facets |
| 7 | Create facets | `/admin/config/search/facets/add-facet` |

**Admin routes:**

| Route | Purpose |
|---|---|
| `/admin/config/search/facets` | Facet listing and management |
| `/admin/config/search/facets/add-facet` | Create new facet |
| `/admin/config/search/facets/{facet}/edit` | Edit facet configuration |
| `/admin/config/search/facets/facet-sources/{source}/edit` | Configure facet source |

## Common Mistakes

- **Wrong**: Adding fields to the index without saving the View first → **Right**: You must save the View before facets can see it as a source.
- **Wrong**: Forgetting to reindex after adding fields → **Right**: Facets only show results for indexed content — reindex after any field change.
- **Wrong**: Using the Database server in production → **Right**: For development, use the "Database" server. For production, use Solr or Elasticsearch — hierarchy and range facets work better with Solr.

## See Also

- [Facet Sources](facet-sources.md) — connecting facets to your View
- [Facets Exposed Filters](facets-exposed-filters.md) — exposed filter approach
