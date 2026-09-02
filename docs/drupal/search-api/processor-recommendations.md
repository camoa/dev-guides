---
description: Which Search API processors to enable — 22 built-in processors by category, and per-backend recommendations for Database vs Solr
tldr: "Use this when deciding which processors to enable for your Search API index."
drupal_version: "11.x"
---

# Processor Recommendations

## When to Use

> When deciding which processors to enable for your Search API index.

## Decision: Built-In Processors (22 Total)

**Content Transformation:**
| ID | Title | Stages | Purpose |
|---|---|---|---|
| `html_filter` | HTML filter | preprocess_index | Strip HTML, boost by element (H1-H3, strong) |
| `ignorecase` | Ignore case | preprocess_index, preprocess_query | Case-insensitive matching |
| `tokenizer` | Tokenizer | preprocess_index, preprocess_query | Split text into words |
| `stemmer` | Stemmer | preprocess_index, preprocess_query | Reduce to root form (running → run) |
| `stopwords` | Stopwords | preprocess_index, preprocess_query | Remove common words (the, a, is) |
| `transliteration` | Transliteration | preprocess_index, preprocess_query | Normalize accents (ü → u) |
| `ignore_character` | Ignore characters | preprocess_index, preprocess_query | Remove/replace specific characters |

**Field Generation:**
| ID | Title | Stage | Purpose |
|---|---|---|---|
| `rendered_item` | Rendered item | add_properties | Render entity for indexing |
| `aggregated_field` | Aggregated fields | add_properties | Combine multiple fields |
| `custom_value` | Custom value | add_properties | Computed field values |
| `add_url` | URL field | add_properties | Add entity URL |
| `add_hierarchy` | Hierarchy | add_properties | Add hierarchical structure |
| `reverse_entity_references` | Reverse references | add_properties | Add reverse entity references |

**Access & Filtering:**
| ID | Title | Stages | Purpose |
|---|---|---|---|
| `content_access` | Content access | pre_index_save, preprocess_query | Node access permissions |
| `role_access` | Role-based access | preprocess_query | Role-based access control |
| `entity_status` | Entity status | alter_items | Skip unpublished entities |
| `role_filter` | Role filter | alter_items | Filter by user role |

**Relevance:**
| ID | Title | Stage | Purpose |
|---|---|---|---|
| `type_boost` | Type boost | preprocess_index | Boost by entity/bundle type |
| `number_field_boost` | Number field boost | preprocess_index | Boost by numeric field value |
| `highlight` | Highlight | postprocess_query | Excerpt with highlighted terms |

**Utility:**
| ID | Title | Stage | Purpose |
|---|---|---|---|
| `entity_type` | Entity type | add_properties | Add entity type field |
| `language_with_fallback` | Language (with fallback) | preprocess_index | Language handling with fallback |

## Decision: Processors by Backend

**Database Backend — Enable These:**
| Processor | Why |
|---|---|
| Entity status | Always — skip unpublished |
| Content access | If any restricted content |
| HTML filter | Strip tags, element boosts |
| Ignore case | Case-insensitive search |
| Tokenizer | Required for DB fulltext |
| Stemmer | Better recall |
| Stopwords | Remove noise words |
| Transliteration | Accent normalization |
| Highlight | Show search excerpts |

**Solr Backend — DISABLE These:**
| Processor | Why Disable |
|---|---|
| Tokenizer | Solr handles natively, better |
| Ignore case | Solr handles natively |
| Stemmer | Solr has language-specific stemmers |
| Stopwords | Solr has language-specific stopword lists |

**Solr Backend — KEEP These:**
| Processor | Why Keep |
|---|---|
| Entity status | Still needed |
| Content access | Still needed |
| HTML filter | Still useful for element boosts |
| Rendered item | Still useful |
| Aggregated fields | Still useful |
| Type boost | Still useful |

## Common Mistakes

- **Enabling Solr-duplicate processors** — Tokenizer, Stemmer, Stopwords, Ignore case on Solr causes redundant processing and can conflict with Solr's analyzer chain.
- **Not enabling Content access** — Search API does NOT restrict access by default. Without this processor, restricted content appears in results.
- **Highlight on high-traffic pages** — Can add 10x latency. Use query tag `search_api_skip_processor_highlight` to skip selectively.

## See Also

- [Processor Architecture](processor-architecture.md) — how processors execute
- [Relevance & Boosting](relevance-boosting.md) — boost strategies
