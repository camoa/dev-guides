---
description: Expose Drupal AI Agents and AI FunctionCall plugins via orchestration_ai_agents and orchestration_ai_function submodules
tldr: "Use orchestration_ai_agents to invoke AI Agent config entities from external platforms (service UUID: `ai_agent::{machine_name}`). Use orchestration_ai_function only for custom `ai.function_calls` plugins not covered by other providers — it auto-deduplicates against eca, ai_agents, and tool providers."
drupal_version: "11.x"
---

# AI Agents and AI Function Providers

## When to Use

> Use this when you want external platforms to invoke Drupal AI Agents or AI FunctionCall plugins via the Orchestration API.

## Decision

| Scenario | Submodule |
|---|---|
| Invoke AI Agents defined in Drupal config | `orchestration_ai_agents` |
| Call custom `ai.function_calls` plugins not covered by other providers | `orchestration_ai_function` |
| Trigger ECA models that happen to call AI internally | `orchestration_eca` (the ECA model handles the AI) |

## Pattern

**AI Agents Provider (`orchestration_ai_agents`):**

- Service UUID: `ai_agent::{agent_machine_name}`
- Required config fields per service:

| Key | Required | Notes |
|---|---|---|
| `instructions` | yes | The task prompt to send to the agent |
| `model` | yes | Select from `provider--model` options with JSON output support |

**Execute workflow:** load provider from `model` → instantiate agent via `AiAgentManager` → `isAvailable()` → `determineSolvability()` → on `JOB_SOLVABLE`: `solve()` → return result.

**Successful response shape:**
```json
{
  "success": true,
  "result": {
    "message": "...",
    "tools": [{"name": "tool_name", "message": "..."}]
  }
}
```

**AI Function Call Provider (`orchestration_ai_function`):**

- Service UUID: `ai_function::{plugin_id}`
- Acts as a catch-all for custom `ai.function_calls` plugins
- **De-duplication**: automatically skips plugins whose provider is `eca_base` (if `orchestration_eca` enabled), `ai_agents` (if `orchestration_ai_agents` enabled), or starts with `tool` (if `orchestration_tool` enabled)

## Common Mistakes

- **Wrong**: Enabling `orchestration_ai_agents` without an AI provider module → **Right**: The service catalog lists agents but `execute()` fails at provider load time
- **Wrong**: Expecting `orchestration_ai_function` to expose AI Agents → **Right**: It explicitly excludes `ai_agents`-provided plugins to avoid duplication
- **Wrong**: Passing a `model` that does not support JSON output mode → **Right**: The agent execution path requires `AiModelCapability::ChatJsonOutput`
- **Wrong**: Enabling both submodules when only AI Agents are needed → **Right**: The combination is safe (de-duplication prevents conflicts) but widens the service surface unnecessarily

## See Also

- [Installation and Setup](installation-and-setup.md)
- [Orchestration API Reference](orchestration-api-reference.md)
- Reference: `modules/ai_agents/src/ServicesProvider.php`, `modules/ai_function/src/ServicesProvider.php`
