---
description: "Tell a Tool API plugin apart from an MCP Server native tool, an AI module FunctionCall, an AI agent tool and an ECA Tool event"
tldr: "The word tool names five Drupal mechanisms. A Tool API tool uses the #[Tool] attribute from the tool module and extends ToolBase. Gotcha: mcp_server ships its own #[Tool] attribute, and ECA 3.1 removed eca_base.tool."
drupal_version: "^10.5 || ^11"
---

# Tool API vs FunctionCall, MCP and ECA Tools

## When to Use

> Read this when a task says "tool" and you need to know which Drupal mechanism it means. On a site with AI, MCP and ECA installed, the word names five different things, and two of them share the attribute name `#[Tool]`.
>
> **Version:** applies to `drupal/tool` 1.0.0-beta11, `mcp_server` 2.0.0-beta5, `eca_tool` 1.0.0-beta1 and ECA 3.1.

## Decision

| The word "tool" can mean... | What it is | Where it is covered |
|---|---|---|
| **A Tool API plugin** | `#[Tool]` from `Drupal\tool\Attribute\Tool`, extending `Drupal\tool\Tool\ToolBase`, in `src/Plugin/tool/Tool/`, discovered by `plugin.manager.tool` | [Tool API topic](index.md) |
| An MCP Server native tool | `#[Tool]` from `Drupal\mcp_server\Attribute\Tool`, extending `Drupal\mcp_server\Plugin\ToolPluginBase`, in `src/Plugin/mcp_server/Tool/`. Callable over MCP only (mcp_server 2.0.0-beta5 `src/Attribute/Tool.php`, `src/Plugin/ToolPluginManager.php`) | [Native Tool Plugins](../mcp-server/native-tool-plugins.md) |
| An AI module function call | The AI module's `#[FunctionCall]` attribute, run by an LLM through function calling | [Function Calling](../ai-module/function-calling.md) |
| An AI agent "tool" | Whatever function calls an AI agent may use. Tool API plugins reach agents only through `tool_ai_connector`, which wraps each tool as a `#[FunctionCall]` | [AI Agents](../ai-module/ai-agents.md); [Calling a Tool from the AI Module](calling-a-tool-from-the-ai-module.md) |
| An ECA Tool event | ECA 2.1.x and 3.0.x shipped `eca_base.tool`; ECA 3.1 removed it (`modules/base/src/BaseEvents.php` defines only `eca_base.cron` and `eca_base.custom`). On ECA 3.1 the Tool event comes from `eca_tool` (`eca_tool.tool`) | [ECA Services Provider](../orchestration/eca-services-provider.md); [Calling a Tool from ECA](calling-a-tool-from-eca.md) |

The Orchestration module consumes Tool API plugins too; see [Tool API Provider](../orchestration/tool-api-provider.md).

## Common Mistakes

- Importing the wrong `Tool` attribute → `use Drupal\mcp_server\Attribute\Tool` makes an MCP-only plugin that Drush, the AI module and ECA never see; for a Tool API tool, import `Drupal\tool\Attribute\Tool` and extend `Drupal\tool\Tool\ToolBase`. See [Native Tool Plugins](../mcp-server/native-tool-plugins.md)
- Writing a `#[FunctionCall]` plugin when the task asked for a Tool API tool → check the attribute namespace
- Assuming ECA's `eca_base.tool` exists on ECA 3.1 → it was removed; `eca_tool` provides its own `eca_tool.tool` event
- Searching the AI function list for a tool by its plugin ID → the AI connector names it `tool__` plus the ID with every `:` replaced by `__`

## See Also

- [What Tool API Is](what-tool-api-is.md) → purpose of the module
- Reference: `modules/contrib/tool/src/Attribute/Tool.php`, `modules/contrib/mcp_server/src/Attribute/Tool.php`, `modules/contrib/tool/modules/tool_ai_connector/src/Plugin/AiFunctionCall/ToolPluginBase.php`
