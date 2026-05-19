---
description: AI Automators — auto-populate entity fields on save using AI, with 52 plugin types and three worker modes
tldr: "Use this guide when auto-generating field content on entity save. Use [AI Agents](ai-agents.md) when you need autonomous decision-making rather than fixed field generation. AutomatorsTool config entity exposes automator chains as function-calling tools."
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
| `input_mode` | `basic` or `token` |
| `worker_type` | `direct` (sync), `batch` (JS), `queue` (cron) |
| `edit_mode` | If false, only generate when field is empty |
| `base_field` | Source field to read from |
| `prompt` | Prompt template (supports tokens) |
| `plugin_config` | Provider, model, and plugin-specific settings |

## Workers

| Worker | Execution | Best For |
|--------|-----------|----------|
| `direct` | Synchronous on save | Fast operations, programmatic saves |
| `batch` | JS-driven batch UI | Interactive saves with progress bar |
| `queue` | Cron queue | Background processing, high volume |

## Rule Runner Flow

`AiAutomatorRuleRunner` orchestrates each rule:
1. Calls `ruleIsAllowed()` — checks entity state, field emptiness, edit mode
2. Calls `generate()` — sends prompt to AI provider, gets raw values
3. Calls `verifyValue()` — validates generated values (e.g., taxonomy terms exist)
4. Calls `storeValues()` — sets values on the entity fields
5. Fires `ValuesChangeEvent` before final storage

## AutomatorsTool (Function Calling Integration)

The `automators_tool` config entity exposes an automator workflow as a function-calling tool. Each tool wraps an automator chain type and registers it as an `AiFunctionCall` plugin via `AutomatorPluginDeriver`. Allows assistants to invoke automator workflows during conversations.

## Automator Chains (Programmatic API)

```php
$service = \Drupal::service('ai_automator.automate');

// List available workflows.
$workflows = $service->getWorkflows();

// Run a chain — creates temp entity, runs automators, returns results.
$output = $service->run('my_chain_machine_name', [
  'field_input_text' => 'source text here',
]);
// $output['field_output_text'] contains the generated value.
```

## Built-in Plugin Types (52 total)

- **Text/String**: `LlmSimpleString`, `LlmSimpleStringLong`, `LlmString`, `LlmTextWithSummary`, `LlmTextCreateSummary`, `LlmSummarizeToStringLong`
- **Reference**: `LlmEntityReference`, `LlmTaxonomy`, `VectorSearchEntityReference`, `VectorSearchText`
- **Media**: `LlmImageGeneration`, `LlmMediaImageGeneration`, `LlmImageAltText`, `LlmRewriteImageFilename`, `LlmMediaAudioGeneration`, `LlmChartFromText`
- **Audio/Video**: `LlmAudioToStringLong`, `LlmVideoToHtml`, `LlmVideoToImage`, `LlmVideoToVideo`, `LlmSpeechGeneration`
- **Numeric**: `LlmBoolean`, `LlmInteger`, `LlmDecimal`, `LlmFloat`, `LlmListFloat`, `LlmListInteger`, `LlmListString`
- **JSON**: `LlmJsonField`, `LlmJsonNative`, `LlmJsonNativeBinary`
- **Contact/Link**: `LlmAddress`, `LlmEmail`, `LlmLink`, `LlmTelephone`
- **Contrib**: `LlmCustomField`, `LlmFaqField`, `LlmMetatag`, `LlmModerationState`, `LlmOfficeHours`
- **External**: `ViewsExtractor`

## Events

| Event | Purpose |
|-------|---------|
| `AutomatorConfigEvent` | Alter config before rule runs |
| `ProcessFieldEvent` | Force-process or force-skip a field |
| `ValuesChangeEvent` | Alter generated values before verify/store |
| `RuleIsAllowedEvent` | Override whether a rule should run |

## Settings.php

```php
$settings['ai_automator_advanced_mode_enabled'] = TRUE; // Show token mode + provider selection
```

## Common Mistakes

- **Wrong**: Using `batch` worker for programmatic saves → **Right**: Batch requires JS — only works in browser context
- **Wrong**: Not setting `edit_mode: false` for existing content → **Right**: Regenerates on every save, overwriting manual edits
- **Wrong**: Forgetting `base_field` → **Right**: Automator needs a source field to read from

## See Also

- [AI Agents](ai-agents.md)
- [AI CKEditor](ai-ckeditor.md)
- [Function Calling](function-calling.md)
- Reference: `web/modules/contrib/ai/modules/ai_automators/`
