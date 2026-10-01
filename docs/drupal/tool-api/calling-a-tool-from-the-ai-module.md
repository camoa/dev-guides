---
description: "Expose Tool API tools to the AI module as function calls through the experimental tool_ai_connector submodule"
tldr: "Enable tool_ai_connector to turn every tool into an AI function named tool__ plus the ID with colons replaced by __. Gotcha: it exposes every tool and ignores operation, destructive and requirements; scope agent tool lists."
drupal_version: "^10.5 || ^11"
---

# Calling a Tool from the AI Module

## When to Use

> Use this when an AI agent or chatbot must call Tool API plugins. The experimental `tool_ai_connector` submodule turns every tool into one AI module function call.
>
> **Version:** applies to `drupal/tool` 1.0.0-beta11, submodule `tool_ai_connector` (experimental; no security advisory coverage). Paths are under `modules/contrib/tool/`.

## How It Works

One `#[FunctionCall(id: 'tool', ...)]` class, `ToolPluginBase`, uses `ToolPluginDeriver` to emit one derivative per tool:

```php
// tool 1.0.0-beta11 modules/tool_ai_connector/src/Plugin/AiFunctionCall/Derivative/ToolPluginDeriver.php
$definition['id'] = 'tool:' . $id;
$definition['name'] = $tool_definition->getLabel();
$definition['group'] = 'tool';
$definition['function_name'] = str_replace(':', '__', $definition['id']);
$definition['description'] = $tool_definition->getDescription();
$definition['context_definitions'] = $tool_definition->getInputDefinitions();
```

| Tool ID | AI plugin ID | Function name the model sees |
|---|---|---|
| `send_email` | `tool:send_email` | `tool__send_email` |
| `tool_belt:entity_save` | `tool:tool_belt:entity_save` | `tool__tool_belt__entity_save` |

Every tool lands in one function group, "Tools API", ID `tool`, whatever its `operation` (tool 1.0.0-beta11 `modules/tool_ai_connector/src/Plugin/AiFunctionGroup/ToolsApi.php`). The invoker (the caller identity; see [Calling a Tool from PHP](calling-a-tool-from-php.md)) is `tool_ai_connector` with `EntitiesAsHandles`, so entities travel as handles. Nested property names escape `:` as `__colon__`.

The parameter schema comes from `ToolPluginBase::normalize()`: Tool API's serializer builds the JSON Schema and `SchemaToolsPropertyConverter` turns it into AI module property objects, map inputs included. The module's docs say map inputs are "handled through the AI module's tools property alter hook" (tool 1.0.0-beta11 `docs/usage/ai-function-calling.md`); `tool_ai_connector` in beta11 implements no alter hook. Trust the code.

## Execution Sequence

From `ToolPluginBase::execute()`:

1. `ToolManager::checkPermission()` before any model value is used.
2. `setInputValue()` for each **declared** input the model sent; other names are dropped.
3. `validateInputs()`; violations return as a correctable failure.
4. `access()`; a denial returns category `Access`.
5. `execute()`, then `getFormattedResult()` at once, so handles exist for the next call.

The model receives `{success, message, outputs}`. `outputs` holds the formatted values, on failure too. Hints, such as handle notes, are appended to `message`. On a correctable (`Input`) failure, `input_schema` is attached so the model can retry.

## Decision

| If you need... | Then... |
|---|---|
| Only some tools available to an agent | Select functions in the agent's configuration; see [AI Agents](../ai-module/ai-agents.md). The connector itself does not filter |
| A tool's output entity in a later call | Pass the `handle:` string the hint shows |
| Stable function names across releases | Do not rename tool IDs; the function name derives from the ID |

## Common Mistakes

- Expecting the connector to skip tools with unmet requirements, `destructive: TRUE` or `Write` operations → the deriver reads none of them
- Expecting `Write` tools in the AI module's `modification_tools` group → every connector tool sits in the `tool` group, so group-based safety signals do not apply; scope the agent's tool list instead
- Searching for `tool_belt:entity_save` in the AI function list → it is `tool__tool_belt__entity_save`
- Treating "Experimental" as stable → the info file says "(Experimental)"; pin versions

## See Also

- [Function Calling](../ai-module/function-calling.md) → the AI module side
- [Entity Inputs and Handles](entity-inputs-and-handles.md) → how handles travel
- [doExecute and ExecutableResult](doexecute-and-executableresult.md) → failure categories
- Reference: `modules/contrib/tool/modules/tool_ai_connector/src/Plugin/AiFunctionCall/ToolPluginBase.php`, `modules/contrib/tool/modules/tool_ai_connector/src/ToolAiConnectorInvoker.php`, `modules/contrib/tool/docs/usage/ai-function-calling.md`
