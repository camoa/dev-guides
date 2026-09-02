---
description: AI Automators — auto-populate entity fields on save using AI, with 52 plugin types and three worker modes
tldr: "Use this guide when auto-generating field content on entity save. 1.4 adds guardrail_set_id per automator, RunAutomatorAction for VBO backfilling without re-saving, and a drush generator for custom automator types."
drupal_version: "11.x"
---

# AI Automators

## When to Use

> Use this guide when auto-generating field content on entity save. Use [AI Agents](ai-agents.md) when you need autonomous decision-making rather than fixed field generation.

The `ai_automators` module auto-populates entity fields on save using AI. It provides a config entity (`ai_automator`) attached to entity type/bundle/field combinations.

## Decision

| Situation | Choose | Why |
|-----------|--------|-----|
| Interactive editor save | `batch` worker | JS-driven progress bar for editors |
| Programmatic/API save | `direct` worker | Batch requires JS — won't run in API context |
| High-volume background | `queue` worker | Cron queue; no timeout risk |
| Only generate when empty | `edit_mode: false` | Prevents overwriting manual edits |
| Backfill existing content | `RunAutomatorAction` + VBO | Runs outside entity presave; no re-save needed |

## How It Works

1. Entity presave hook fires
2. `AiAutomatorEntityModifier` checks for matching rules
3. `AiAutomatorRuleRunner` runs each rule: generate -> verify -> store
4. Generated values are set on the entity before save completes

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

## Built-in Plugin Types (52 total)

**Text/String:**

- Simple (no format): `LlmSimpleString`, `LlmSimpleStringLong`, `LlmSimpleText`, `LlmSimpleTextLong`, `LlmSimpleTextWithSummary`
- Formatted: `LlmString`, `LlmStringLong`, `LlmText`, `LlmTextLong`, `LlmTextWithSummary`
- Summary: `LlmTextCreateSummary`, `LlmSummarizeToStringLong`, `LlmSummarizeToTextLong`

**Numeric:** `LlmBoolean`, `LlmDecimal`, `LlmFloat`, `LlmInteger`, `LlmListFloat`, `LlmListInteger`, `LlmListString`

**Reference:** `LlmEntityReference`, `LlmTaxonomy`, `VectorSearchEntityReference`, `VectorSearchText`

**Media/File:** `LlmImageGeneration`, `LlmMediaImageGeneration`, `LlmMediaAudioGeneration`, `LlmSpeechGeneration`, `LlmImageAltText`, `LlmRewriteImageFilename`, `LlmChartFromText`

**Audio/Video:** `LlmAudioToStringLong`, `LlmAudioToTextLong`, `LlmAudioToTextWithSummary`, `LlmVideoToHtml`, `LlmVideoToImage`, `LlmVideoToStringLong`, `LlmVideoToTextLong`, `LlmVideoToVideo`

**Contact/Link:** `LlmAddress`, `LlmEmail`, `LlmLink`, `LlmTelephone`

**JSON:** `LlmJsonField`, `LlmJsonNative`, `LlmJsonNativeBinary`

**Contrib fields:** `LlmCustomField`, `LlmFaqField`, `LlmMetatag`, `LlmModerationState`, `LlmOfficeHours`

**External:** `ViewsExtractor`

## Writing a Custom Automator Type

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

## Rule Runner Flow

`AiAutomatorRuleRunner` orchestrates each individual rule:

1. Loads the `AiAutomatorType` plugin for the rule
2. Calls `ruleIsAllowed()` — checks entity state, field emptiness, edit mode
3. Calls `generate()` — sends prompt to AI provider, gets raw values
4. Calls `verifyValue()` — validates generated values (e.g., taxonomy terms exist)
5. Calls `storeValues()` — sets values on the entity fields
6. Fires `ValuesChangeEvent` before final storage

## Automators Tool (Config Entity)

The `automators_tool` config entity exposes an automator workflow as a tool for the AI function calling system. Each tool wraps an automator chain type and registers it as an `AiFunctionCall` plugin via `AutomatorPluginDeriver`. This allows assistants to invoke automator workflows during conversations (e.g., "generate a summary" triggers an automator chain).

## Automator Chains (Pipeline)

Chain multiple automators into a disposable workflow. The `Automate` service (`ai_automator.automate`) provides the full programmatic API:

```php
$service = \Drupal::service('ai_automator.automate');

// List available workflows (automator chain types).
$workflows = $service->getWorkflows();

// Get required input fields for a chain type.
$required = $service->getRequiredFields('my_chain_type');

// Get automated (output) fields for a chain type.
$automated = $service->getAutomatedFields('my_chain_type');

// Run: creates a temporary automator_chain entity, runs automators, returns results, deletes entity.
$output = $service->run('my_chain_machine_name', [
  'field_input_text' => 'source text here',
]);
// $output['field_output_text'] contains the generated value
```

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

## Guardrails on Automators (New in 1.4)

An automator can carry its own guardrail set via the `guardrail_set_id` config property (set under the automator's advanced settings; schema key in `ai_automators.schema.yml`). Its guardrails run in addition to any [global guardrails](guardrails-system.md) on every generation the automator triggers.

## Running Automators as Actions / VBO (New in 1.4)

The `RunAutomatorAction` action plugin (derived per automator by `RunAutomatorActionDeriver`) exposes any automator as a core Action. Because it is an Action, it runs **outside** entity presave — wrap it in Views Bulk Operations to backfill fields across many existing entities (e.g. generate alt text for 1,000 images) without re-saving each one through the normal automator save hook.

## Scaffolding an Automator Type (New in 1.4)

```bash
drush generate plugin:ai:automator-type   # alias: ai-automator-type
```

## Setup Steps

1. Enable `ai_automators` (+ Field UI for configuration UI)
2. Edit field settings on a content type
3. Enable "AI Automator" section
4. Select automator type, configure prompt, set worker type
5. Save — field will auto-populate on next entity save

## Common Mistakes

| Mistake | Why it's wrong |
|---------|---------------|
| Using `batch` worker for programmatic saves | Batch requires JS — only works in browser |
| Not setting `edit_mode: false` for existing content | Regenerates on every save, overwriting manual edits |
| Forgetting `base_field` | Automator needs a source field to read from |

## See Also

- [AI Agents](ai-agents.md)
- [AI CKEditor](ai-ckeditor.md)
- [Function Calling](function-calling.md)
- [Guardrails System](guardrails-system.md)
- Reference: `web/modules/contrib/ai/modules/ai_automators/`
