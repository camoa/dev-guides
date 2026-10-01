---
description: "Expose drupal/tool Tool API plugins as Orchestration services via orchestration_tool 1.0.0 (Tool API 1.0.0-beta11, no stable release)"
tldr: "Use orchestration_tool 1.0.0 to let external platforms call drupal/tool plugins; UUID is tool::{plugin_id}, entity inputs take the entity ID. Tool API is 1.0.0-beta11, no stable release: re-test flows after each update."
drupal_version: "11.x"
---

# Tool API Provider

## When to Use

> Use this when you want external platforms to call `drupal/tool` Tool API plugins directly via Orchestration. Applies to `orchestration_tool` 1.0.0 with Tool API 1.0.0-beta11, which has no stable release.

## How It Works

The `orchestration_tool` submodule registers a `ServicesProvider` that iterates all `plugin.manager.tool` definitions and exposes each as an Orchestration service.

**Service UUID format**: `tool::{tool_plugin_id}`

**ServiceConfig entries** are built from each tool's `InputDefinition` objects, preserving: key, label, description, required flag, data type, editability (`!$input->isLocked()`), default value, and constraints. `ToolDefinition::getInputDefinitions()` omits locked inputs by default, so locked inputs never reach the catalog and `editable` is always `true`.

**Execute workflow**:
1. Instantiate the tool plugin via `ToolManager`
2. For each `InputDefinition`: if data type starts with `entity:`, load the entity via `EntityTypeManagerInterface` using the config value as the ID; otherwise use the value directly
3. Call `$executableTool->execute()`
4. Return `$executableTool->getResultMessage()`

**Entity resolution**: Entity-typed inputs expect the entity's numeric/string ID in the config — the provider resolves them internally before calling `execute()`.

## Stability: Tool API Is a Beta

Tool API 1.0.0-beta11 is a beta. It has no stable release and no security advisory coverage. 1.0.0-rc1 removes the deprecated shims; see [What changes at rc1](../tool-api/what-changes-at-rc1.md). For `orchestration_tool` 1.0.0 this means:

- It calls `ToolManager::getDefinitions()`, `createInstance()`, `getInputDefinitions()`, `setInputValue()`, `execute()` and `getResultMessage()`. All exist in beta11; a later beta can change any of them.
- The service catalog mirrors each tool's input definitions. A Tool API update can change the `config` fields an external platform sees without any Orchestration update.
- Re-check `/orchestration/services` and each external flow after every `drupal/tool` update.

For the Tool API itself, see the [Tool API guide](../tool-api/index.md).

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

Reference: `modules/contrib/orchestration/modules/tool/src/ServicesProvider.php`

## Common Mistakes

- **Passing entity UUIDs when entity IDs are expected** — the provider uses `EntityTypeManagerInterface::getStorage()->load($value)`, which expects the entity ID
- **Enabling `orchestration_tool` alongside `orchestration_ai_function` and being surprised when Tool-provider FunctionCall plugins only appear once** — `orchestration_ai_function` skips them; the combination is safe
- **Exposing a tool whose entity input is bundle-qualified (`entity:node:article`)** — the provider passes `substr($dataType, 7)`, here `node:article`, to `getStorage()`, which is not an entity type ID
- **Updating `drupal/tool` in production without re-testing the external flows** — Tool API is a beta, and the catalog follows its input definitions

## See Also

- [AI Agents and AI Function Providers](ai-agents-and-ai-function-providers.md) → for the de-duplication relationship
- [Tool API guide](../tool-api/index.md) → defining tools, input definitions, entity inputs
- Reference: `modules/contrib/orchestration/modules/tool/src/ServicesProvider.php`, `modules/contrib/orchestration/modules/tool/orchestration_tool.services.yml`, `modules/contrib/tool/src/Tool/ToolDefinition.php`, `modules/contrib/tool/src/TypedData/EntityDefinitionBase.php`
