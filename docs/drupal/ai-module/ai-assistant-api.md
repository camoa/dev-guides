---
description: AI Assistant API — config entities, runner service, action plugins, and system prompt tokens
tldr: "Use this guide when creating AI assistants, writing custom action plugins, or calling the runner programmatically. Use [AI Chatbot](ai-chatbot-deepchat.md) for the frontend chatbot configuration."
drupal_version: "11.x"
---

# AI Assistant API

## When to Use

> Use this guide when creating AI assistants, writing custom action plugins, or calling the runner programmatically. Use [AI Chatbot](ai-chatbot-deepchat.md) for the frontend chatbot configuration.

## Decision

| Situation | Choose | Why |
|-----------|--------|-----|
| Add capability to assistant | Action plugin | Actions are composable and config-driven |
| Use tool calling vs prompts | `use_function_calling: true` | Requires action to implement `getFunctionCallSchema()` |
| Allow conversation history | `allow_history: session` | Persists thread in PrivateTempStore |
| Delegate to an agent | Set `ai_agent` on entity | AgentRunner handles the autonomous loop |

## Pattern

```php
$runner = \Drupal::service('ai_assistant_api.runner');
$assistant = \Drupal::entityTypeManager()->getStorage('ai_assistant')->load('my_assistant');

$runner->setAssistant($assistant);
$runner->setUserMessage(new UserMessage('Hello'));
$runner->setContext(['route' => '/node/1']);
$runner->streamedOutput(FALSE);

$output = $runner->process(); // ChatOutput
$text = $output->getNormalized()->getText();
```

## Config Entity: `ai_assistant`

Admin UI: `/admin/config/ai/ai-assistant`

| Field | Description |
|-------|-------------|
| `llm_provider` | Provider plugin ID or `__default__` |
| `system_prompt` | Final system prompt (supports tokens) |
| `allow_history` | `none`, `session`, `session_one_thread` |
| `history_context_length` | Messages to include in context |
| `use_function_calling` | Use tool calling instead of prompt-based action selection |
| `ai_agent` | Optional agent plugin ID (delegates to `AgentRunner`) |
| `roles` | Roles that can use this assistant |

## Function Calling Mode

When `use_function_calling` is enabled, action plugins must implement `getFunctionCallSchema()` to return a JSON Schema describing their parameters. The runner passes these schemas as native tool definitions instead of embedding action lists in the pre-action prompt. The LLM responds with structured tool calls rather than JSON extracted from natural language.

## System Prompt Tokens

`[instructions]`, `[pre_action_prompt]`, `[is_logged_in]`, `[user_roles]`, `[user_id]`, `[user_name]`, `[page_title]`, `[page_path]`, `[site_name]`

## Writing a Custom Action

```php
use Drupal\ai_assistant_api\Attribute\AiAssistantAction;
use Drupal\ai_assistant_api\Base\AiAssistantActionBase;

#[AiAssistantAction(
  id: 'my_module_search',
  label: new TranslatableMarkup('My Search Action'),
)]
class MySearchAction extends AiAssistantActionBase {

  public function listActions(): array {
    return [[
      'id' => 'search',
      'label' => 'Search',
      'description' => 'Search the knowledge base',
      'plugin' => 'my_module_search',
    ]];
  }

  public function triggerAction(string $action_id, array $params = []): void {
    $results = $this->doSearch($params);
    $this->setOutputContext('my_module_search', json_encode($results));
  }

  public function listContexts(): array { return []; }
  public function listUsageInstructions(): array {
    return ['Use search to find relevant content.'];
  }
  public function provideFewShotLearningExample(): array { return []; }
}
```

## Runner Methods

| Method | Purpose |
|--------|---------|
| `setVerboseMode(TRUE)` | Show intermediate agent steps in output |
| `setThrowException(TRUE)` | Throw exceptions instead of returning error messages |
| `getMessageHistory()` | Returns current thread's conversation history |
| `resetThread()` | Clears the current thread from PrivateTempStore |

## Events

| Event | Purpose |
|-------|---------|
| `AiAssistantSystemRoleEvent` | Alter final system prompt |
| `PrepromptSystemRoleEvent` | Alter pre-action prompt |
| `AiAssistantPassContextToAgentEvent` | Inject context into agent |

## Common Mistakes

- **Wrong**: Missing `id`, `label`, `description`, `plugin` keys in `listActions()` → **Right**: All four keys are required
- **Wrong**: Setting `allow_history: session` with a large `history_context_length` → **Right**: Large histories consume tokens; set conservatively
- **Wrong**: Using `use_function_calling` with providers that don't support tools → **Right**: Falls back to prompt-based selection, which may be unreliable

## See Also

- [AI Chatbot](ai-chatbot-deepchat.md)
- [AI Agents](ai-agents.md)
- Reference: `web/modules/contrib/ai/modules/ai_assistant_api/`
