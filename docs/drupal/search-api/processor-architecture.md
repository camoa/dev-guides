---
description: Search API processor pipeline — 6 stages, execution flow, weight system, and ProcessorInterface
tldr: "Use this when you need to understand how Search API processors work — the stages, weights, and execution order."
drupal_version: "11.x"
---

# Processor Architecture

## When to Use

> When you need to understand how Search API processors work — the stages, weights, and execution order.

## Decision: Processing Stages

| Stage | Constant | When | Purpose | Example Processors |
|---|---|---|---|---|
| **ADD_PROPERTIES** | `STAGE_ADD_PROPERTIES` | Index config time | Add virtual fields | RenderedItem, AggregatedFields, AddURL |
| **PRE_INDEX_SAVE** | `STAGE_PRE_INDEX_SAVE` | Before index entity saves | Validate/modify index config | ContentAccess, Highlight |
| **ALTER_ITEMS** | `STAGE_ALTER_ITEMS` | Before indexing items | Filter/modify items | EntityStatus (skip unpublished) |
| **PREPROCESS_INDEX** | `STAGE_PREPROCESS_INDEX` | During indexing | Transform field values | HtmlFilter, IgnoreCase, Tokenizer, Stemmer |
| **PREPROCESS_QUERY** | `STAGE_PREPROCESS_QUERY` | Before search executes | Modify search query | ContentAccess (add access conditions) |
| **POSTPROCESS_QUERY** | `STAGE_POSTPROCESS_QUERY` | After search returns | Modify results | Highlight (add excerpts) |

## Pattern: Execution Flow

```
INDEXING:
  Entity saved → Tracker marks for indexing
  → STAGE_ALTER_ITEMS (filter out unpublished, etc.)
  → STAGE_PREPROCESS_INDEX (transform values: lowercase, strip HTML, tokenize, stem)
  → Backend.indexItems() (store in search engine)

SEARCHING:
  Query built → STAGE_PREPROCESS_QUERY (add access checks, modify keywords)
  → QueryPreExecuteEvent dispatched
  → Backend.search() (execute search)
  → ProcessingResultsEvent dispatched
  → STAGE_POSTPROCESS_QUERY (add highlights, modify results)
  → Results returned
```

## Pattern: Processor Weight System

Processors execute in weight order per stage. Lower weights run first. Negative weights = earlier. Processor weights are configurable per stage in the Processors admin UI.

**Critical ordering examples:**
- ContentAccess (preprocess_query: -30) runs early to add access conditions before other processors
- Highlight (postprocess_query: 0) runs after results are returned

## Pattern: Processor Interface

```php
interface ProcessorInterface {
  public function supportsIndex(IndexInterface $index): bool;
  public function supportsStage(string $stage): bool;
  public function getWeight(string $stage): int;
  public function setWeight(string $stage, int $weight): void;
  public function isLocked(): bool;  // Can't be disabled
  public function isHidden(): bool;  // Hidden from UI

  // Stage-specific methods:
  public function getPropertyDefinitions(): array;     // ADD_PROPERTIES
  public function preIndexSave(): void;                // PRE_INDEX_SAVE
  public function alterIndexedItems(array &$items): void; // ALTER_ITEMS
  public function preprocessIndexItems(array $items): void; // PREPROCESS_INDEX
  public function preprocessSearchQuery(QueryInterface $query): void; // PREPROCESS_QUERY
  public function postprocessSearchResults(ResultSetInterface $results): void; // POSTPROCESS_QUERY
}
```

## See Also

- [Processor Recommendations](processor-recommendations.md) — which processors to enable
- [Custom Plugin Development](custom-plugin-development.md) — creating custom processors
