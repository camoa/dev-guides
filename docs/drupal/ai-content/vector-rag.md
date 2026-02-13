---
description: Vector databases and RAG - semantic search, content similarity, AI chatbots with site context
drupal_version: "11.x"
---

# Vector Databases & RAG

## When to Use

> Use vector databases for semantic search, content similarity analysis, and RAG (Retrieval-Augmented Generation) workflows. Use when you need to find conceptually similar content, power AI chatbots with site context, or analyze content relationships.

## Decision

| Provider | Stability | Best For | Scale |
|----------|-----------|----------|-------|
| SQLite | Stable | Development, small sites | < 10K documents |
| PostgreSQL | Beta | Self-hosted, familiar tech stack | < 100K documents |
| Milvus | Beta | Large scale, production (most popular) | 100K+ documents |
| Pinecone | Experimental | Cloud-managed, serverless | Any scale |
| Azure AI Search | Beta | Microsoft ecosystem | Enterprise |

## Setup Pattern

**Step 1: Install VDB Provider Module**
```bash
drush en ai_vdb_provider_milvus ai_search
```

**Step 2: Configure VDB Connection**
Navigate to `/admin/config/ai/vdb-providers`:

```yaml
# Milvus configuration example
provider: milvus
connection:
  host: localhost
  port: 19530
  database: drupal
  collection: content_embeddings
embedding:
  provider: openai
  model: text-embedding-3-large
  dimensions: 3072
```

**Step 3: Configure AI Search**
The `ai_search` module integrates VDB with Search API:

```yaml
# /admin/config/search/search-api
index_id: ai_content_index
datasources:
  - entity:node
fields:
  title: text
  body: text
  field_summary: text
  field_tags: entity_reference
processor:
  ai_embedding:
    provider: openai
    model: text-embedding-3-large
    chunk_size: 512
    chunk_overlap: 50
server:
  backend: ai_vdb
  vdb_provider: milvus
```

## Embedding & Indexing

**Text Chunking**:
Long content must be chunked for embedding models (token limits):

```php
$chunker = \Drupal::service('ai.text_chunker');

// Chunk text with overlap for context preservation
$chunks = $chunker->chunkText($long_text, [
  'max_tokens' => 512,
  'overlap_tokens' => 50,
  'preserve_sentences' => TRUE,
]);

// Generate embeddings for each chunk
$embeddings = [];
foreach ($chunks as $chunk) {
  $embeddings[] = $ai_provider->embed($chunk, 'text-embedding-3-large');
}
```

## RAG Implementation

**RAG (Retrieval-Augmented Generation)** combines vector search with LLM generation to provide accurate, context-aware responses.

**Pattern: AI Chatbot with RAG**

```php
class RagChatbot {

  public function generateResponse(string $user_query): string {
    // Step 1: Generate query embedding
    $query_embedding = $this->aiProvider->embed(
      $user_query,
      'text-embedding-3-large'
    );

    // Step 2: Retrieve relevant content via vector search
    $vdb = \Drupal::service('ai.vdb_provider');
    $relevant_chunks = $vdb->proximitySearch($query_embedding, 5);

    // Step 3: Build context from retrieved chunks
    $context = '';
    foreach ($relevant_chunks as $chunk) {
      $context .= $chunk['text'] . "\n\n";
    }

    // Step 4: Generate response with context
    $prompt = sprintf(
      "Answer this question using ONLY the context provided. If the answer is not in the context, say 'I don't have information about that.'\n\nContext:\n%s\n\nQuestion: %s",
      $context,
      $user_query
    );

    $response = $this->aiProvider->chat([
      ['role' => 'system', 'content' => 'You are a helpful assistant that answers questions using provided context.'],
      ['role' => 'user', 'content' => $prompt]
    ], 'gpt-4');

    return $response;
  }

}
```

**Benefits of RAG**:
- Reduces hallucination (AI making up facts)
- Provides source attribution (can link to original content)
- Keeps responses current (always uses latest indexed content)
- Maintains control over knowledge base

## Content Intelligence Use Cases

**Similar Content Discovery**:
```php
// Find articles similar to current article
$current_embedding = $node->get('field_embedding')->value;
$similar = $vdb->proximitySearch($current_embedding, 5, [
  'filters' => [
    'content_type' => 'article',
    'exclude_id' => $node->id(),
  ],
]);
```

**Semantic Tag Suggestions**:
```php
// Suggest tags based on content similarity
$content_embedding = $ai_provider->embed($node->body->value);
$similar_content = $vdb->proximitySearch($content_embedding, 20);

$tag_frequency = [];
foreach ($similar_content as $item) {
  foreach ($item['tags'] as $tag) {
    $tag_frequency[$tag] = ($tag_frequency[$tag] ?? 0) + 1;
  }
}

// Sort by frequency and return top 5
arsort($tag_frequency);
$suggested_tags = array_slice(array_keys($tag_frequency), 0, 5);
```

## Common Mistakes

- **Wrong**: Not chunking long content → **Right**: Embedding models have token limits (512-8192); long content must be chunked or truncated
- **Wrong**: Using wrong similarity metric → **Right**: OpenAI embeddings use cosine similarity; using euclidean distance produces poor results
- **Wrong**: Not handling embedding model changes → **Right**: Switching embedding models requires complete re-indexing; plan migrations carefully
- **Wrong**: Ignoring embedding costs → **Right**: Embedding generation costs per token; batch processing and caching are essential at scale
- **Wrong**: Trusting RAG responses without source attribution → **Right**: Always include source references so users can verify AI responses
- **Wrong**: Not implementing RAG filtering → **Right**: Without filters, chatbot may pull irrelevant or outdated content; filter by date, content type, publication status

## See Also

- [Content Quality & Review](quality-review.md)
- [Security & Privacy](security-privacy.md)
- Reference: `/modules/contrib/ai/modules/ai_search/`
- Reference: https://www.thedroptimes.com/64433/unlocking-ai-search-in-drupal-practical-guide-vector-database-modules
- Reference: https://www.droptica.com/blog/recommended-vector-databases-vdb-drupal-overview-ai-providers/
- Reference: https://www.brainsum.com/blog/ai-chatbot-demo-drupal-and-rag
- Reference: https://www.vardot.com/en-us/ideas/blog/step-step-guide-creating-rag-based-drupal-ai-chatbot
