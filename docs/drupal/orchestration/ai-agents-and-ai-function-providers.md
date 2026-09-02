---
description: Expose Drupal AI Agents and AI FunctionCall plugins via orchestration_ai_agents and orchestration_ai_function submodules
tldr: "Use orchestration_ai_agents to invoke AI Agent config entities from external platforms (service UUID: `ai_agent::{machine_name}`). Use orchestration_ai_function only for custom `ai.function_calls` plugins not covered by other providers — it auto-deduplicates against eca, ai_agents, and tool providers."
drupal_version: "11.x"
---

# AI Agents and AI Function Providers

## When to Use

> Use this when you want external platforms to invoke Drupal AI Agents or AI FunctionCall plugins via the Orchestration API.

## AI Agents Provider (`orchestration_ai_agents`)

**What it exposes**: Every enabled `ai_agent` config entity becomes an Orchestration service. The service UUID is `ai_agent::{agent_machine_name}`.

**Configuration fields per agent service** (ServiceConfig entries):

| Key | Required | Description |
|---|---|---|
| `instructions` | yes | The task prompt to send to the agent |
| `model` | yes | Select: chat provider model with JSON output support; options populated from `aiProviderManager->getSimpleProviderModelOptions()` |

**Execute workflow**:
1. Load AI provider from the `model` simple-option string (format: `provider--model`)
2. Instantiate the agent plugin via `AiAgentManager`
3. Call `isAvailable()` — returns error if false
4. Set a `Task` with the `instructions` config value, then call `determineSolvability()`
5. On `JOB_SOLVABLE`: call `solve()`, collect tool results, return structured response
6. On `JOB_NEEDS_ANSWERS` or `JOB_NOT_SOLVABLE`: return error

**Successful response shape**:
```json
{
  "success": true,
  "result": {
    "message": "...",
    "tools": [{"name": "tool_name", "message": "..."}]
  }
}
```

**Error response shape**:
```json
{"success": false, "error": "Agent is not available."}
```

Output (`message`) is decoded from YAML first, then JSON; falls back to raw string.

**Dependencies**: Requires `drupal/ai` + `drupal/ai_agents` + at least one AI provider module.

## AI Function Call Provider (`orchestration_ai_function`)

**What it exposes**: All `ai.function_calls` plugin definitions become Orchestration services — minus those already covered by a more specific provider.

**De-duplication logic** (from `modules/ai_function/src/ServicesProvider.php`):
- Skips plugins where `$definition['provider'] === 'eca_base'` — if `orchestration_eca` is enabled
- Skips plugins where `$definition['provider'] === 'ai_agents'` — if `orchestration_ai_agents` is enabled
- Skips plugins whose provider starts with `'tool'` — if `orchestration_tool` is enabled

This makes `orchestration_ai_function` a catch-all for any custom `ai.function_calls` plugins not handled by the other three providers. Enable it only if you have such plugins.

**Service UUID format**: `ai_function::{plugin_id}`

**Execute workflow**: Instantiate the plugin, iterate context definitions (loading entities for `entity:*`-typed contexts), call `execute()`, return `getReadableOutput()`.

**Dependencies**: Requires `drupal/ai`.

## Decision: Which AI Provider to Enable

| Scenario | Submodule |
|---|---|
| Invoke AI Agents defined in Drupal config | `orchestration_ai_agents` |
| Call custom `ai.function_calls` plugins not covered by other providers | `orchestration_ai_function` |
| Trigger ECA models that happen to call AI internally | `orchestration_eca` (the ECA model handles the AI) |

## Common Mistakes

- **Enabling `orchestration_ai_agents` without an AI provider module** — the service catalog lists agents, but `execute()` fails at provider load time
- **Expecting `orchestration_ai_function` to expose AI Agents** — it explicitly excludes `ai_agents`-provided plugins to avoid duplication
- **Passing a `model` that the selected AI provider does not support JSON output mode for** — the agent execution path requires `AiModelCapability::ChatJsonOutput`
- **Enabling both `orchestration_ai_agents` and `orchestration_ai_function` when only AI Agents are needed** — the combination is safe (de-duplication prevents conflicts) but widens the service surface unnecessarily

## See Also

- [Installation and Setup](installation-and-setup.md) → for AI provider composer/drush commands
- [Orchestration API Reference](orchestration-api-reference.md) → for the execute endpoint
- Reference: `modules/ai_agents/src/ServicesProvider.php`, `modules/ai_function/src/ServicesProvider.php`
