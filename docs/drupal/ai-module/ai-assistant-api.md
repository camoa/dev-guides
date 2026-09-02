---
description: AI Assistant API — config entities, runner service, action plugins, and system prompt tokens
tldr: "Use this guide when creating AI assistants, writing custom action plugins, or calling the runner programmatically. Use [AI Chatbot](ai-chatbot-deepchat.md) for the frontend chatbot configuration."
drupal_version: "11.x"
---

# AI Assistant API

## When to Use

> Use this guide when creating AI assistants, writing custom action plugins, or calling the runner programmatically. Use [AI Chatbot](ai-chatbot-deepchat.md) for the frontend chatbot configuration.

The `ai_assistant_api` module provides config entities for AI assistants and a runner service that orchestrates actions. It has no frontend — `ai_chatbot` consumes it.

## Decision

| Situation | Choose | Why |
|-----------|--------|-----|
| Add capability to assistant | Action plugin | Actions are composable and config-driven |
| Use tool calling vs prompts | `use_function_calling: true` | Requires action to implement `getFunctionCallSchema()` |
| Allow conversation history | `allow_history: session` | Persists thread in PrivateTempStore |
| Delegate to an agent | Set `ai_agent` on entity | AgentRunner handles the autonomous loop |

## Config Entity: `ai_assistant`

Admin UI: `/admin/config/ai/ai-assistant`

| Field | Type | Description |
|-------|------|-------------|
| `llm_provider` | string | Provider plugin ID or `__default__` |
| `llm_model` | string | Model ID |
| `system_prompt` | text | Final system prompt (supports tokens) |
| `pre_action_prompt` | text | Pre-action selection prompt |
| `instructions` | text | Injected into system prompt via `[instructions]` |
| `allow_history` | string | `none`, `session`, `session_one_thread` |
| `history_context_length` | integer | Messages to include in context |
| `actions_enabled` | array | Keyed by action plugin ID |
| `roles` | array | Roles that can use this assistant |
| `use_function_calling` | boolean | Use tool calling instead of prompt-based action selection |
| `ai_agent` | string | Optional agent plugin ID (delegates to `AgentRunner`) |
| `error_message` | string | Custom error message |
| `specific_error_messages` | array | Per-exception error overrides |

## Runner Service

```php
$runner = \Drupal::service('ai_assistant_api.runner');
$assistant = \Drupal::entityTypeManager()->getStorage('ai_assistant')->load('my_assistant');

$runner->setAssistant($assistant);
$runner->setUserMessage(new UserMessage('Hello'));
$runner->setContext(['route' => '/node/1']); // arbitrary context
$runner->streamedOutput(FALSE);

$output = $runner->process(); // ChatOutput
$text = $output->getNormalized()->getText();
```

## Additional Runner Methods

| Method | Purpose |
|--------|---------|
| `setVerboseMode(TRUE)` | Enable verbose output (shows intermediate agent steps) |
| `setThrowException(TRUE)` | Throw exceptions on error instead of returning error messages |
| `getMessageHistory()` | Returns the current thread's conversation history |
| `isSetup()` | Returns `TRUE` if the runner has an assistant and user message configured |
| `resetThread()` | Clears the current thread from PrivateTempStore |

## Agent Integration

When `ai_agent` is set on an assistant config entity, the `AgentRunner` service takes over processing. It loads the `ConfigAiAgentInterface` plugin identified by the `ai_agent` field and delegates execution to it. Context is passed to the agent via `AiAssistantPassContextToAgentEvent`. This allows AI Agents (from the `drupal/ai_agents` contrib module) to be exposed as standard assistants.

## Function Calling Mode

When `use_function_calling` is enabled, action plugins must implement `getFunctionCallSchema()` to return a JSON Schema describing their parameters. The runner passes these schemas as native tool definitions instead of embedding action lists in the pre-action prompt. The LLM responds with structured tool calls rather than JSON extracted from natural language.

## System Prompt Tokens

The `AssistantMessageBuilder` substitutes these tokens in the system prompt:

`[instructions]`, `[pre_action_prompt]`, `[is_logged_in]`, `[user_roles]`, `[user_id]`, `[user_name]`, `[user_language]`, `[user_timezone]`, `[page_title]`, `[page_path]`, `[page_language]`, `[site_name]`

## Action Plugins

Actions extend the assistant's capabilities. The runner does a two-pass process:

1. **Pre-prompt pass** — asks LLM which actions to invoke based on available actions
2. **Action execution** — runs selected actions, collects output
3. **Final pass** — LLM synthesizes action output into a response

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

## Events

| Event | Constant | Purpose |
|-------|----------|---------|
| `AiAssistantSystemRoleEvent` | `ai_assistant.change_assistant_message` | Alter final system prompt |
| `PrepromptSystemRoleEvent` | `ai_assistant.change_preprompt_message` | Alter pre-action prompt |
| `AiAssistantPassContextToAgentEvent` | `ai_assistant.pass_context_to_agent` | Inject context into agent |

## Settings.php Options

```php
$settings['ai_assistant_custom_prompts'] = TRUE; // Use DB-stored prompts
$settings['ai_assistant_advanced_mode_enabled'] = TRUE; // Show prompt fields in UI
```

## Common Mistakes

| Mistake | Why it's wrong |
|---------|---------------|
| Not implementing `listActions()` correctly | Each action needs `id`, `label`, `description`, `plugin` keys |
| Setting `allow_history` to `session` without checking context length | Large histories consume tokens; set `history_context_length` conservatively |
| Using `use_function_calling` with providers that don't support tools | Falls back to prompt-based selection, which may be unreliable |

## See Also

- [AI Chatbot](ai-chatbot-deepchat.md)
- [AI Agents](ai-agents.md)
- Reference: `web/modules/contrib/ai/modules/ai_assistant_api/`
