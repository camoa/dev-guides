---
description: "What a Tool API author needs to know when mcp_server_tool_bridge serves a tool over MCP"
tldr: "MCP exposure is opt-in per tool through an mcp_tool_config entity, and content entities travel as handles. Gotcha: the bridge does not pre-check the declared permission, so keep refiners and input transforms free of side effects."
drupal_version: "^10.5 || ^11"
---

# Calling a Tool over MCP

## When to Use

> Use this as a tool author whose Tool API plugin will be served over MCP. The `drupal/mcp_server_tool_bridge` project does the serving; [Tool API Bridge](../mcp-server/tool-api-bridge.md) owns its setup, hints and wire names.
>
> **Version:** applies to `drupal/tool` 1.0.0-beta11 with `mcp_server_tool_bridge` 1.0.0-beta3 (both beta; no security advisory coverage).

## What a Tool Author Needs to Know

- Exposure is opt-in per tool: an `mcp_tool_config` entity maps one tool to one MCP tool. Writing the tool does not publish it.
- The bridge creates the tool with the invoker `mcp_server` plus `EntitiesAsHandles`, so content entities travel as handles; see [Entity Inputs and Handles](entity-inputs-and-handles.md).
- The bridge sets inputs, then calls `validateInputs()`, `access()`, `execute()` and `getFormattedResult()`. It does not pre-check the declared permission, so handle resolution and refiners run before a denial (mcp_server_tool_bridge 1.0.0-beta3 `src/Plugin/mcp_server/Tool/ToolApi.php`). Keep refiners and input transforms free of side effects.
- On success, outputs become `structuredContent`. On failure, outputs are dropped.

## Decision

| If you want the tool... | Then... |
|---|---|
| Served over MCP | Write a normal Tool API tool and add an `mcp_tool_config`; see [Tool API Bridge](../mcp-server/tool-api-bridge.md) |
| Served over MCP only | Consider an MCP Server native tool instead; see [Native Tool Plugins](../mcp-server/native-tool-plugins.md) |

## Common Mistakes

- Expecting every tool to appear over MCP → only tools with an enabled `mcp_tool_config` appear
- Relying on the declared permission to stop input processing for MCP callers → the bridge denies only inside `access()`
- Trusting the bridge's comment that Tool API does not enforce required outputs ([#3583029](https://git.drupalcode.org/project/tool/-/work_items/3583029)) → beta11 does; see [Output Definitions](output-definitions.md)

## See Also

- [Tool API Bridge](../mcp-server/tool-api-bridge.md), [MCP Server topic](../mcp-server/index.md)
- [Operation and Destructive](operation-and-destructive.md) → the source of the MCP hints
- Reference: `modules/contrib/mcp_server_tool_bridge/src/Plugin/mcp_server/Tool/ToolApi.php`, `modules/contrib/mcp_server_tool_bridge/src/Plugin/Derivative/McpToolConfigDeriver.php`
