---
description: Expose drupal/tool Tool API plugins as Orchestration services via the orchestration_tool submodule
tldr: "Use orchestration_tool to let external platforms call `drupal/tool` plugins directly. Service UUID is `tool::{plugin_id}`; entity-typed inputs expect the entity's numeric ID (resolved internally before execute()). The Tool API is explicitly marked early-stage — treat orchestration_tool as similarly unstable."
drupal_version: "11.x"
---

# Tool API Provider

## When to Use

> Use this when you want external platforms to call `drupal/tool` Tool API plugins directly via Orchestration.

## How It Works

The `orchestration_tool` submodule registers a `ServicesProvider` that iterates all `plugin.manager.tool` definitions and exposes each as an Orchestration service.

**Service UUID format**: `tool::{tool_plugin_id}`

**ServiceConfig entries** are built from each tool's `InputDefinition` objects, preserving: key, label, description, required flag, data type, editability (`!$input->isLocked()`), default value, and constraints.

**Execute workflow**:
1. Instantiate the tool plugin via `ToolManager`
2. For each `InputDefinition`: if data type starts with `entity:`, load the entity via `EntityTypeManagerInterface` using the config value as the ID; otherwise use the value directly
3. Call `$executableTool->execute()`
4. Return `$executableTool->getResultMessage()`

**Entity resolution**: Entity-typed inputs expect the entity's numeric/string ID in the config — the provider resolves them internally before calling `execute()`.

## Stability Warning

The `drupal/tool` module documentation explicitly states: "the Tool API is still in development and that their structure and functionality are still subject to change." Treat `orchestration_tool` as similarly early-stage. Input parameter structures and entity resolution behavior may change in minor releases of `drupal/tool`.

## Pattern

```json
// Calling a Tool API plugin via Orchestration:
POST /orchestration/service/execute
{
  "id": "tool::my_tool_plugin_id",
  "config": {
    "text_param": "some value",
    "node_param": "42"
  }
}
```

Reference: `modules/tool/src/ServicesProvider.php`

## Common Mistakes

- **Passing entity UUIDs when entity IDs are expected** — the provider uses `EntityTypeManagerInterface::getStorage()->load($value)`, which expects the entity ID
- **Enabling `orchestration_tool` alongside `orchestration_ai_function` and being surprised when Tool-provider FunctionCall plugins only appear once** — `orchestration_ai_function` skips them; the combination is safe
- **Relying on Tool API plugin structure in production without hedging against the upstream instability warning**

## See Also

- [AI Agents and AI Function Providers](ai-agents-and-ai-function-providers.md) → for the de-duplication relationship
- Reference: `modules/tool/src/ServicesProvider.php`, `modules/tool/orchestration_tool.services.yml`
