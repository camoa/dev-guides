---
description: Search API multilingual — single index per language, language field, language_with_fallback processor, and Solr multilingual
tldr: "Use this when building search for multilingual Drupal sites."
drupal_version: "11.x"
---

# Multilingual Search

## When to Use

> Use this when building search for multilingual Drupal sites.

## Decision

| Setting | Where | Purpose |
|---|---|---|
| "Item language" field | Index → Fields | Add for faceting/filtering by language |
| "Language (with fallback)" processor | Index → Processors | Handles translation fallback logic |
| "Content Translation" datasource setting | Index → Datasources | Configure which languages to index |
| `search_current_language` module | Contrib | Auto-filter results to current interface language |

## Pattern

Search API stores one indexed item **per language per entity**. A node with 3 translations creates 3 index items. You do NOT need separate indexes per language.

**Solr multilingual:** Since `search_api_solr` 8.x-2.x, the formerly separate `search_api_solr_multilingual` module is **merged into the main module**. No separate install needed.

Solr applies language-specific analyzers automatically:
- Different stemmers per language
- Language-specific stop words
- Compound word splitting for German
- CJK tokenization for Chinese/Japanese/Korean

The jump-start configsets are multilingual by default.

## Common Mistakes

- **Wrong**: Installing `search_api_solr_multilingual` separately → **Right**: It's been merged into `search_api_solr`. Just use the main module.
- **Wrong**: Forgetting to add language filter to View → **Right**: Without a language filter, results from all languages appear. Add "Item language" filter or use `search_current_language`.
- **Wrong**: Mixing Language (with fallback) processor + Solr fulltext without testing → **Right**: Known issues exist. Test thoroughly.

## See Also

- [Solr Best Practices](solr-best-practices.md)
- [Processor Recommendations](processor-recommendations.md)
