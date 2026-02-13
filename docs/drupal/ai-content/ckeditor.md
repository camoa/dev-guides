---
description: CKEditor AI integration - in-editor content generation, rewriting, and enhancement
drupal_version: "11.x"
---

# CKEditor AI Integration

## When to Use

> Use CKEditor AI integration for in-editor AI assistance. Use when content creators need real-time content generation, rewriting, and enhancement without leaving the editing interface.

## Core Capabilities

**ai_ckeditor Module Features**:
- Inline content generation within CKEditor
- Text rewriting and tone adjustment
- Content expansion and summarization
- Grammar and style improvements
- Integration with custom AI plugins

## Pattern

**Enable Module**:
```bash
drush en ai_ckeditor
```

**Configure CKEditor Profile**:
Navigate to `/admin/config/content/formats`, edit text format, configure CKEditor toolbar:

1. Add AI buttons to toolbar (Generate, Rewrite, Summarize, Expand)
2. Configure AI plugin settings
3. Select default provider and model
4. Set permissions for AI features

**Custom AI Plugin Example**:

```php
<?php

namespace Drupal\custom_ai\Plugin\AiCKEditor;

use Drupal\ai_ckeditor\PluginBase\AiCKEditorPluginBase;

/**
 * Tone adjustment plugin.
 *
 * @AiCKEditorPlugin(
 *   id = "tone_adjuster",
 *   label = @Translation("Adjust Tone"),
 *   description = @Translation("Rewrite selected text with specified tone"),
 * )
 */
class ToneAdjuster extends AiCKEditorPluginBase {

  public function process(string $content, array $config): string {
    $tone = $config['tone'] ?? 'professional';

    $prompt = sprintf(
      "Rewrite this text with a %s tone:\n\n%s",
      $tone,
      $content
    );

    return $this->aiProvider->chat([
      ['role' => 'user', 'content' => $prompt]
    ], $config['model']);
  }

}
```

Register in `custom_ai.ai_ckeditor.yml`:
```yaml
tone_adjuster:
  label: 'Adjust Tone'
  button: TRUE
  context_menu: TRUE
  tones:
    - professional
    - friendly
    - formal
    - casual
    - technical
```

## Usage Patterns

**Pattern 1: Content Generation**
1. Position cursor in editor
2. Click "Generate" button
3. Provide prompt or use pre-configured prompt template
4. AI generates content at cursor position
5. Editor reviews and edits

**Pattern 2: Text Rewriting**
1. Select text in editor
2. Right-click → AI menu → Rewrite
3. Choose tone or style
4. AI rewrites selected text
5. Accept or reject changes

**Pattern 3: Content Enhancement**
- **Summarize**: Select long text, click Summarize, AI produces brief version
- **Expand**: Select outline or short text, click Expand, AI adds detail
- **Improve**: Select text, click Improve, AI fixes grammar and style

## Best Practices

**Editor Experience**:
- Provide clear button labels describing action
- Show loading indicators during AI processing
- Allow undo/redo of AI changes
- Provide diff view for AI modifications
- Enable manual retry if generation fails

**Prompt Design**:
- Include context from other fields when relevant
- Set clear length expectations
- Specify tone and style requirements
- Use examples for complex operations
- Fall back gracefully on errors

**Performance**:
- Use fast models (GPT-3.5-turbo) for real-time operations
- Implement client-side rate limiting
- Cache common prompts and responses
- Provide cancel button for long operations

## Common Mistakes

- **Wrong**: Blocking editor during AI generation → **Right**: Use asynchronous processing with loading indicators; editors should be able to continue editing other fields
- **Wrong**: Not providing undo for AI changes → **Right**: Always integrate with CKEditor's undo system so editors can revert AI modifications
- **Wrong**: Using slow models for inline operations → **Right**: GPT-4 can take 10-30 seconds; use GPT-3.5-turbo or Claude Haiku for sub-3-second responses
- **Wrong**: Overwriting editor's work without confirmation → **Right**: Show preview or diff before applying AI changes, especially for rewrites
- **Wrong**: Not contextualizing prompts with field data → **Right**: Prompts using only selected text miss important context from title, category, etc.
- **Wrong**: Exposing AI features to all users → **Right**: Restrict AI features via permissions based on role and trust level

## See Also

- [SEO with AI](seo.md)
- [Content Quality & Review](quality-review.md)
- [AI Automator System](automators.md)
- Reference: `/modules/contrib/ai/modules/ai_ckeditor/`
- Reference: https://www.webwash.net/ai-automators-drupal-ai-in-drupal-cms/
