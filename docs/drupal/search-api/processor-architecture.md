---
description: Search API processor pipeline — 6 stages, execution flow, weight system, and ProcessorInterface
drupal_version: "11.x"
---

# Processor Architecture

## When to Use

> Use this when you need to understand how Search API processors work — the stages, weights, and execution order.

## Decision

| Stage | Constant | When | Purpose | Example Processors |
|---|---|---|---|---|
| **ADD_PROPERTIES** | `STAGE_ADD_PROPERTIES` | Index config time | Add virtual fields | RenderedItem, AggregatedFields, AddURL |
| **PRE_INDEX_SAVE** | `STAGE_PRE_INDEX_SAVE` | Before index entity saves | Validate/modify index config | ContentAccess, Highlight |
| **ALTER_ITEMS** | `STAGE_ALTER_ITEMS` | Before indexing items | Filter/modify items | EntityStatus (skip unpublished) |
| **PREPROCESS_INDEX** | `STAGE_PREPROCESS_INDEX` | During indexing | Transform field values | HtmlFilter, IgnoreCase, Tokenizer, Stemmer |
| **PREPROCESS_QUERY** | `STAGE_PREPROCESS_QUERY` | Before search executes | Modify search query | ContentAccess (add access conditions) |
| **POSTPROCESS_QUERY** | `STAGE_POSTPROCESS_QUERY` | After search returns | Modify results | Highlight (add excerpts) |

## Pattern

**Execution flow:**
```
INDEXING:
  Entity saved → Tracker marks for indexing
  → ALTER_ITEMS (filter out unpublished, etc.)
  → PREPROCESS_INDEX (transform values: lowercase, strip HTML, tokenize, stem)
  → Backend.indexItems() (store in search engine)

SEARCHING:
  Query built → PREPROCESS_QUERY (add access checks, modify keywords)
  → QueryPreExecuteEvent dispatched
  → Backend.search() (execute search)
  → ProcessingResultsEvent dispatched
  → POSTPROCESS_QUERY (add highlights, modify results)
  → Results returned
```

**ProcessorInterface** — key methods:
```php
public function supportsIndex(IndexInterface $index): bool;
public function supportsStage(string $stage): bool;
public function getWeight(string $stage): int;
public function preprocessIndexItems(array $items): void;   // PREPROCESS_INDEX
public function preprocessSearchQuery(QueryInterface $query): void; // PREPROCESS_QUERY
public function postprocessSearchResults(ResultSetInterface $results): void; // POSTPROCESS_QUERY
```

Processors execute in weight order per stage. Lower weights run first. ContentAccess runs at weight -30 in preprocess_query to add access conditions before other processors.

## Common Mistakes

- **Wrong**: Expecting processor changes to affect existing indexed data → **Right**: Must reindex after changing processors.
- **Wrong**: Wrong stage for the task → **Right**: `alter_items` to filter items, `preprocess_index` to transform values, `preprocess_query` to modify queries.

## See Also

- [Processor Recommendations](processor-recommendations.md)
- [Custom Plugin Development](custom-plugin-development.md)
- Reference: `web/modules/contrib/search_api/src/Processor/ProcessorInterface.php`
