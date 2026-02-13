---
description: AI Automator system - field-level content generation with 50+ automator types
drupal_version: "11.x"
---

# AI Automator System

## When to Use

> Use AI Automators when you need consistent, automated content generation for specific fields without custom code. Use for field-level automation triggered on entity create or update.

## Automator Types Overview

**Text Generation**
- `llm_simple_string_long`: Basic text fields
- `llm_simple_text_long`: Plain text long fields
- `llm_simple_text_with_summary`: Text with summary
- `llm_text_long`: Formatted text long
- `llm_custom_field`: Custom field types

**Structured Data**
- `llm_metatag`: Meta tags generation
- `llm_address`: Address fields
- `llm_link`: Link fields with titles
- `llm_email`: Email generation
- `llm_boolean`: Yes/no decision
- `llm_float`: Numeric values

**Media & Files**
- `llm_rewrite_image_filename`: SEO-friendly image filenames
- `llm_audio_to_string_long`: Audio transcription
- `llm_speech_generation`: Text-to-speech
- `llm_json_native_binary`: JSON field population

**Advanced**
- `vector_search_text`: Vector database search integration
- `views_extractor`: Extract data from Views results
- Chained automators: Multi-step workflows

## Pattern

**UI Configuration** (recommended for most use cases):

1. Navigate to Structure → Content types → [Type] → Manage fields
2. Edit field settings
3. Enable "AI Automator" under field settings
4. Configure automator:
   - Select automator type
   - Choose AI provider and model
   - Write prompt template using tokens
   - Set trigger conditions (on create, on update, manual)
   - Configure fallback behavior

**Code Configuration** (for complex logic):

```php
// Define automator in custom module config
$automator = [
  'id' => 'article_summary',
  'label' => 'Article Summary Generator',
  'type' => 'llm_simple_text_with_summary',
  'field_name' => 'field_summary',
  'prompt' => 'Summarize this article in 2-3 sentences:\n\n[node:body]',
  'provider' => 'openai',
  'model' => 'gpt-4',
  'trigger' => ['create', 'update'],
  'conditions' => [
    'field_empty' => TRUE, // Only run if summary is empty
  ],
];

// Programmatic execution
$automator_manager = \Drupal::service('plugin.manager.ai_automator_type');
$instance = $automator_manager->createInstance($automator['type'], $automator);
$result = $instance->process($entity, $field_name);
```

## Automator Chains

Chain multiple automators for complex workflows:

```yaml
# Chain example: Blog post automation
chain_id: blog_post_complete

steps:
  1_outline:
    type: llm_text_long
    field: field_outline
    prompt: "Create outline for: [node:title]"

  2_body:
    type: llm_text_long
    field: field_body
    prompt: "Write blog post following this outline: [node:field_outline]"
    depends_on: 1_outline

  3_summary:
    type: llm_simple_text_with_summary
    field: field_summary
    prompt: "Summarize: [node:field_body]"
    depends_on: 2_body

  4_metatags:
    type: llm_metatag
    field: field_metatags
    prompt: "Generate SEO metatags for: [node:title] - [node:field_summary]"
    depends_on: 3_summary
```

## Best Practices

**Prompt Engineering**:
- Use specific, actionable instructions
- Include tone and style requirements
- Set length constraints (word count, character limits)
- Provide examples in prompt when possible
- Use token replacements for dynamic context

**Performance**:
- Enable queue processing for slow models (GPT-4)
- Cache automator results when content doesn't change
- Use fast models (GPT-3.5) for simple text generation
- Batch process multiple fields in single request when possible

**Error Handling**:
- Configure fallback values for API failures
- Set timeouts appropriate to model speed
- Log failures for debugging
- Provide manual override options for editors

## Common Mistakes

- **Wrong**: Running expensive models on every save → **Right**: Use GPT-4 only when necessary; GPT-3.5-turbo is 10x cheaper and sufficient for most text generation
- **Wrong**: Not using queue processing → **Right**: Synchronous automator execution blocks form submission; always queue for models taking >3 seconds
- **Wrong**: Writing vague prompts → **Right**: "Write content" produces generic output; specify tone, length, structure, and purpose for quality results
- **Wrong**: Chaining too many automators → **Right**: Each step adds latency and cost; limit chains to 3-5 steps or use background processing
- **Wrong**: Ignoring token limits → **Right**: Long prompts with full node body can exceed model limits; use text chunking or summaries in prompts
- **Wrong**: Not providing manual override → **Right**: Editors need ability to regenerate or edit AI content; always include manual trigger option

## See Also

- [Framework Patterns](framework-patterns.md)
- [SEO with AI](seo.md)
- [Performance Optimization](performance.md)
- Reference: `/modules/contrib/ai/modules/ai_automators/`
- Reference: https://project.pages.drupalcode.org/ai/1.0.x/modules/ai_automators/
