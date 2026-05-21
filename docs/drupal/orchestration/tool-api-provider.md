---
description: Expose drupal/tool Tool API plugins as Orchestration services via the orchestration_tool submodule
tldr: "Use orchestration_tool to let external platforms call `drupal/tool` plugins directly. Service UUID is `tool::{plugin_id}`; entity-typed inputs expect the entity's numeric ID (resolved internally before execute()). The Tool API is explicitly marked early-stage — treat orchestration_tool as similarly unstable."
drupal_version: "11.x"
---

# Tool API Provider

## When to Use

> Use this when you want external platforms to call `drupal/tool` Tool API plugins directly via Orchestration.

## Decision

| Situation | Notes |
|---|---|
| Tool API plugin with scalar inputs | Pass value directly in config |
| Tool API plugin with entity-typed inputs | Pass the entity's numeric/string ID — provider resolves to entity object internally |
| Production use | Hedge against upstream instability — the Tool API docs explicitly warn structure is subject to change |

## Pattern

```json
POST /orchestration/service/execute
{
  "id": "tool::my_tool_plugin_id",
  "config": {
    "text_param": "some value",
    "node_param": "42"
  }
}
```

**Execute workflow:**
1. Instantiate tool plugin via `ToolManager`
2. For each `InputDefinition`: if data type starts with `entity:`, load the entity via `EntityTypeManagerInterface` using the config value as the ID; otherwise use the value directly
3. Call `$executableTool->execute()`
4. Return `$executableTool->getResultMessage()`

**ServiceConfig entries** are built from each tool's `InputDefinition` objects, preserving: key, label, description, required flag, data type, editability, default value, and constraints.

**Stability warning:** The `drupal/tool` module explicitly states its Tool API is still in development and subject to change. Treat `orchestration_tool` as similarly early-stage.

## Common Mistakes

- **Wrong**: Passing entity UUIDs when entity IDs are expected → **Right**: The provider uses `EntityTypeManagerInterface::getStorage()->load($value)` which expects the entity ID, not UUID
- **Wrong**: Enabling `orchestration_tool` alongside `orchestration_ai_function` and being surprised by deduplication → **Right**: `orchestration_ai_function` skips Tool-provider FunctionCall plugins; the combination is safe
- **Wrong**: Relying on Tool API plugin structure in production → **Right**: The upstream module warns structure may change in minor releases

## See Also

- [AI Agents and AI Function Providers](ai-agents-and-ai-function-providers.md)
- Reference: `modules/tool/src/ServicesProvider.php`, `modules/tool/orchestration_tool.services.yml`
