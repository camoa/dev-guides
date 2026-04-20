---
description: Which Search API processors to enable — 23 built-in processors by category, and per-backend recommendations for Database vs Solr
tldr: "Use this when deciding which processors to enable for your Search API index."
drupal_version: "11.x"
---

# Processor Recommendations

## When to Use

> Use this when deciding which processors to enable for your Search API index.

## Decision

**By backend:**

| Processor | Database | Solr | Why |
|---|---|---|---|
| Entity status | Enable | Enable | Always — skip unpublished |
| Content access | Enable if restricted | Enable if restricted | Access control — NOT default |
| HTML filter | Enable | Enable | Strip tags, element boosts |
| Ignore case | Enable | **Disable** | Solr handles natively |
| Tokenizer | Enable | **Disable** | Solr handles natively, better |
| Stemmer | Enable | **Disable** | Solr has language-specific stemmers |
| Stopwords | Enable | **Disable** | Solr has language-specific lists |
| Transliteration | Enable | Optional | Accent normalization |
| Highlight | Enable | Enable | Show search excerpts |
| Rendered item | Optional | Optional | Render entity for indexing |
| Aggregated fields | Optional | Optional | Combine multiple fields |
| Type boost | Optional | Optional | Boost by entity/bundle type |

## Pattern

**23 built-in processors grouped by category:**

| Category | Processors |
|---|---|
| Content transformation | html_filter, ignorecase, tokenizer, stemmer, stopwords, transliteration, ignore_character |
| Field generation | rendered_item, aggregated_field, custom_value, add_url, add_hierarchy, reverse_entity_references |
| Access & filtering | content_access, role_access, entity_status, role_filter |
| Relevance | type_boost, number_field_boost, highlight |
| Utility | entity_type, language_with_fallback |

## Common Mistakes

- **Wrong**: Enabling Tokenizer, Stemmer, Stopwords, Ignore case on Solr → **Right**: Causes redundant processing and can conflict with Solr's analyzer chain. Disable them.
- **Wrong**: Not enabling Content access → **Right**: Search API does NOT restrict access by default. Without this processor, restricted content appears in results for all users.
- **Wrong**: Enabling Highlight on high-traffic pages → **Right**: Can add 10x latency. Use query tag `search_api_skip_processor_highlight` to skip selectively.

## See Also

- [Processor Architecture](processor-architecture.md)
- [Relevance & Boosting](relevance-boosting.md)
- [Content Access & Security](content-access-security.md)
- Reference: https://www.drupal.org/docs/8/modules/search-api/getting-started/processors
