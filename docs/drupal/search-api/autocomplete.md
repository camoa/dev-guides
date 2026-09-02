---
description: Search API autocomplete — search_api_autocomplete module setup, Solr Terms suggester, and min characters configuration
tldr: "Use this when adding search-as-you-type suggestions to search forms."
drupal_version: "11.x"
---

# Autocomplete

## When to Use

> When adding search-as-you-type suggestions to search forms.

## Decision: Module Setup

```bash
composer require drupal/search_api_autocomplete
drush en search_api_autocomplete
```

## Pattern: Configuration

1. Navigate to your Search API index → "Autocomplete" tab
2. Enable autocomplete for specific search views/pages
3. Configure: max suggestions, minimum characters, suggester plugins

## Decision: Configuration Options

| Setting | Recommendation | Why |
|---|---|---|
| Min characters | 3 | Prevents excessive queries on 1-2 chars |
| Max suggestions | 5-10 | UX best practice |
| Suggester | Backend-specific | Solr Terms for Solr, default for DB |

## Pattern: Solr Autocomplete

Use the Solr Terms component for blazing-fast autocompletion — queries the Solr terms component directly instead of running full searches.

## Pattern: Enhanced Module

`search_api_autocomplete_improved` provides:
- Optimized caching
- Accurate result counting
- Auto-discovers views config from autocomplete entities

## Common Mistakes

- **Autocomplete on String fields** — Use Fulltext fields for autocomplete. String fields require exact match.
- **Min characters = 1** — Causes excessive backend load on large indexes. Set to 3+.

## See Also

- [Views Integration](views-integration.md) — search page setup
- [Solr Best Practices](solr-best-practices.md) — Solr Terms suggester
