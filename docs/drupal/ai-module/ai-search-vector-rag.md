---
description: AI Search — vector database integration, RAG with AI assistants, semantic search via Search API
tldr: "Use this guide when setting up semantic search or Retrieval-Augmented Generation (RAG) with vector databases. Use [AI Assistant API](ai-assistant-api.md) to wire the `rag_action` into an assistant."
drupal_version: "11.x"
---

# AI Search (Vector / RAG)

## When to Use

> Use this guide when setting up semantic search or Retrieval-Augmented Generation (RAG) with vector databases. Use [AI Assistant API](ai-assistant-api.md) to wire the `rag_action` into an assistant.

The `ai_search` module integrates Search API with Vector Databases for semantic search and RAG.

**Status:** Experimental
**Dependencies:** `ai`, `search_api`

## Architecture

```
Content -> Chunk -> Embed -> Store in VDB -> Query -> Embed query -> Vector match -> Return
```

## Decision

| Situation | Choose | Why |
|-----------|--------|-----|
| Accurate semantic search | `contextual_chunks` strategy | Multiple vectors; chunk enriched with title + context |
| Faster, less accurate | `average_pool` strategy | Single composite vector; simpler |
| RAG in a chatbot | `rag_action` plugin on assistant | Retrieves semantically relevant content into LLM context |
| Hybrid with keyword search | Boost processors | Combines vector and DB/Solr results |

## Programmatic Search

```php
$index = \Drupal\search_api\Entity\Index::load('my_ai_index');
$query = $index->query(['limit' => 10]);
$query->keys('semantic search phrase');
$results = $query->execute();

foreach ($results->getResultItems() as $item) {
  $score = $item->getScore(); // vector distance
  $content = $item->getExtraData('content');
  $entity_id = $item->getExtraData('drupal_entity_id');
  $offset = $item->getExtraData('real_offset');           // chunk offset within item
  $reason = $item->getExtraData('reason_for_finish');     // why search stopped
  $vscore = $item->getExtraData('current_vector_score');  // raw similarity score
}
```

## Chunk-Level Results

```php
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

## Backend Config

| Setting | Description |
|---------|-------------|
| `database` | VDB provider plugin ID |
| `database_settings` | `database_name`, `collection`, `metric` |
| `embeddings_engine` | `provider_id__model_id` format |
| `embedding_strategy` | Strategy plugin ID |
| `chat_model` | Model for tokenizer (chunk size calculation) |
| `include_raw_embedding_vector` | Expose raw vectors in results (for debugging/analysis) |

## VDB Provider Interface

VDB providers must implement `AiVdbProviderSearchApiInterface`, which extends the base VDB interface with Search API-specific methods for indexing, querying, and deleting vectors. This is the contract between `ai_search` and any vector database backend.

## RAG with AI Assistant

Enable the `rag_action` plugin on an assistant. Configure it with a Search API index. The action retrieves semantically relevant content and injects it into the LLM context.

## Hybrid Search (Boost Processors)

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

| Mistake | Why it's wrong |
|---------|---------------|
| No `main_content` field assigned | At least one field must be `main_content` for embeddings |
| Wrong tokenizer model | Chunk sizes calculated from tokenizer; mismatched model = wrong sizes |
| Not re-indexing after strategy change | Existing vectors don't match new strategy; must reindex |

## See Also

- [AI Assistant API](ai-assistant-api.md)
- [Operation Types](operation-types.md)
- Reference: `web/modules/contrib/ai/modules/ai_search/`
- Reference: https://project.pages.drupalcode.org/ai/
