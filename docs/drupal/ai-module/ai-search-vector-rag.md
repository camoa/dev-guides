---
description: AI Search — vector database integration, RAG with AI assistants, semantic search via Search API
tldr: "Use this guide when setting up semantic search or Retrieval-Augmented Generation (RAG) with vector databases. Use [AI Assistant API](ai-assistant-api.md) to wire the `rag_action` into an assistant."
drupal_version: "11.x"
---

# AI Search (Vector / RAG)

## When to Use

> Use this guide when setting up semantic search or Retrieval-Augmented Generation (RAG) with vector databases. Use [AI Assistant API](ai-assistant-api.md) to wire the `rag_action` into an assistant.

## Decision

| Situation | Choose | Why |
|-----------|--------|-----|
| Accurate semantic search | `contextual_chunks` strategy | Multiple vectors; chunk enriched with title + context |
| Faster, less accurate | `average_pool` strategy | Single composite vector; simpler |
| RAG in a chatbot | `rag_action` plugin on assistant | Retrieves semantically relevant content into LLM context |
| Hybrid with keyword search | Boost processors | Combines vector and DB/Solr results |

## Pattern

```php
$index = \Drupal\search_api\Entity\Index::load('my_ai_index');
$query = $index->query(['limit' => 10]);
$query->keys('semantic search phrase');
$results = $query->execute();

foreach ($results->getResultItems() as $item) {
  $score = $item->getScore();          // vector distance
  $content = $item->getExtraData('content');
  $entity_id = $item->getExtraData('drupal_entity_id');
}

// Get chunk-level results instead of item-level:
$query->setOption('search_api_ai_get_chunks_result', TRUE);
```

## Setup Steps

1. Install a VDB provider (`ai_vdb_provider_pinecone`, `ai_vdb_provider_milvus`, etc.)
2. Create a Search API Server: choose "AI Search" backend
3. Configure VDB connection, embeddings engine, embedding strategy
4. Create a Search API Index on that server
5. Go to Fields tab — assign indexing options to each field
6. Index content

## Indexing Options

| Option | Description |
|--------|-------------|
| `main_content` | Chunked and embedded — at least one required |
| `contextual_content` | Prepended to every chunk for context |
| `attributes` | Stored as VDB metadata for filtering |
| `ignore` | Not processed |

## Embedding Strategies

| Strategy | Description |
|----------|-------------|
| `contextual_chunks` | Multiple vectors per item; each chunk enriched with title + context. Most accurate. Default. |
| `average_pool` | Single composite vector via average pooling. Faster, less accurate. |

## Hybrid Search Processors

| Processor | Backend | Description |
|-----------|---------|-------------|
| `database_boost_by_ai_search` | `search_api_db` | Injects AI-matched IDs into DB query |
| `solr_boost_by_ai_search` | `search_api_solr` | Elevates AI-matched IDs in Solr results |
| `ai_search_score_threshold` | `search_api_ai_search` | Filters below minimum relevance score |

## Custom Embedding Strategy

```php
use Drupal\ai_search\Attribute\EmbeddingStrategy;

#[EmbeddingStrategy(
  id: 'my_strategy',
  label: new TranslatableMarkup('My Strategy'),
  description: new TranslatableMarkup('Custom chunking approach'),
)]
class MyStrategy extends EmbeddingBase {
  // Override getEmbedding() or getChunks()
}
```

## Common Mistakes

- **Wrong**: No `main_content` field assigned → **Right**: At least one field must be `main_content` for embeddings to work
- **Wrong**: Mismatched tokenizer model → **Right**: Chunk sizes are calculated from the tokenizer model; mismatch causes wrong chunk sizes
- **Wrong**: Not re-indexing after strategy change → **Right**: Existing vectors don't match new strategy; must reindex

## See Also

- [AI Assistant API](ai-assistant-api.md)
- [Operation Types](operation-types.md)
- Reference: `web/modules/contrib/ai/modules/ai_search/`
- Reference: https://project.pages.drupalcode.org/ai/
