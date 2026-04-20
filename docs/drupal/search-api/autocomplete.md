---
description: Search API autocomplete — search_api_autocomplete module setup, Solr Terms suggester, and min characters configuration
tldr: "Use this when adding search-as-you-type suggestions to search forms."
drupal_version: "11.x"
---

# Autocomplete

## When to Use

> Use this when adding search-as-you-type suggestions to search forms.

## Decision

| Setting | Recommendation | Why |
|---|---|---|
| Min characters | 3 | Prevents excessive queries on 1-2 chars |
| Max suggestions | 5-10 | UX best practice |
| Suggester | Backend-specific | Solr Terms for Solr, default for DB |

## Pattern

```bash
composer require drupal/search_api_autocomplete
drush en search_api_autocomplete
```

**Configuration:**
1. Navigate to your Search API index → "Autocomplete" tab
2. Enable autocomplete for specific search views/pages
3. Configure: max suggestions, minimum characters, suggester plugins

**Solr autocomplete** — use the Solr Terms component for blazing-fast autocompletion. Queries the Solr terms component directly instead of running full searches.

**Enhanced module** — `search_api_autocomplete_improved` provides:
- Optimized caching
- Accurate result counting
- Auto-discovers views config from autocomplete entities

## Common Mistakes

- **Wrong**: Autocomplete on String fields → **Right**: Use Fulltext fields for autocomplete. String fields require exact match.
- **Wrong**: `min_characters = 1` → **Right**: Causes excessive backend load on large indexes. Set to 3+.

## See Also

- [Views Integration](views-integration.md)
- [Solr Best Practices](solr-best-practices.md)
- Reference: https://www.drupal.org/project/search_api_autocomplete
