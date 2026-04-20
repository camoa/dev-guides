---
description: AI Automators — auto-populate entity fields on save using AI, with 52 plugin types and three worker modes
tldr: "Use this guide when auto-generating field content on entity save. Use [AI Agents](ai-agents.md) when you need autonomous decision-making rather than fixed field generation."
drupal_version: "11.x"
---

# AI Automators

## When to Use

> Use this guide when auto-generating field content on entity save. Use [AI Agents](ai-agents.md) when you need autonomous decision-making rather than fixed field generation.

## Decision

| Situation | Choose | Why |
|-----------|--------|-----|
| Interactive editor save | `batch` worker | JS-driven progress bar for editors |
| Programmatic/API save | `direct` worker | Batch requires JS — won't run in API context |
| High-volume background | `queue` worker | Cron queue; no timeout risk |
| Only generate when empty | `edit_mode: false` | Prevents overwriting manual edits |

## Pattern

```php
use Drupal\ai_automators\Attribute\AiAutomatorType;
use Drupal\ai_automators\PluginBaseClasses\RuleBase;

#[AiAutomatorType(
  id: 'my_string_generator',
  label: new TranslatableMarkup('My Generator'),
  field_rule: 'string',
  target: NULL,
)]
class MyStringGenerator extends RuleBase {

  public function generate(ContentEntityInterface $entity, FieldDefinitionInterface $fieldDef, array $config): array {
    $instance = $this->prepareLlmInstance('chat', $config);
    $prompt = $this->buildPrompt($entity, $config);
    $values = [$this->runChatMessage($prompt, $config, $instance, $entity)[0] ?? ''];
    return $values;
  }
}
```

## Config Entity: `ai_automator`

| Field | Description |
|-------|-------------|
| `rule` | AiAutomatorType plugin ID |
| `worker_type` | `direct` (sync), `batch` (JS), `queue` (cron) |
| `edit_mode` | If false, only generate when field is empty |
| `base_field` | Source field to read from |
| `prompt` | Prompt template (supports tokens) |

## Workers

| Worker | Execution | Best For |
|--------|-----------|----------|
| `direct` | Synchronous on save | Fast operations, programmatic saves |
| `batch` | JS-driven batch UI | Interactive saves with progress bar |
| `queue` | Cron queue | Background processing, high volume |

## Built-in Plugin Types (52 total)

- **Text/String**: `LlmSimpleString`, `LlmString`, `LlmTextWithSummary`, `LlmTextCreateSummary`
- **Reference**: `LlmEntityReference`, `LlmTaxonomy`, `VectorSearchEntityReference`
- **Media**: `LlmImageGeneration`, `LlmImageAltText`, `LlmMediaAudioGeneration`
- **Audio/Video**: `LlmAudioToStringLong`, `LlmVideoToHtml`, `LlmVideoToVideo`
- **Numeric**: `LlmBoolean`, `LlmInteger`, `LlmDecimal`
- **JSON**: `LlmJsonField`, `LlmJsonNative`
- **Contrib**: `LlmCustomField`, `LlmMetatag`, `LlmModerationState`

## Automator Chains (Programmatic API)

```php
$service = \Drupal::service('ai_automator.automate');

// Run a chain — creates temp entity, runs automators, returns results.
$output = $service->run('my_chain_machine_name', [
  'field_input_text' => 'source text here',
]);
// $output['field_output_text'] contains the generated value.
```

## Events

| Event | Purpose |
|-------|---------|
| `AutomatorConfigEvent` | Alter config before rule runs |
| `ValuesChangeEvent` | Alter generated values before verify/store |
| `RuleIsAllowedEvent` | Override whether a rule should run |
| `ProcessFieldEvent` | Force-process or force-skip a field |

## Common Mistakes

- **Wrong**: Using `batch` worker for programmatic saves → **Right**: Batch requires JS — only works in browser context
- **Wrong**: Not setting `edit_mode: false` for existing content → **Right**: Regenerates on every save, overwriting manual edits
- **Wrong**: Forgetting `base_field` → **Right**: Automator needs a source field to read from

## See Also

- [AI Agents](ai-agents.md)
- [AI CKEditor](ai-ckeditor.md)
- Reference: `web/modules/contrib/ai/modules/ai_automators/`
