---
description: Function calling tools — building custom FunctionCall plugins for AI agents and assistants
tldr: "Use this guide when building custom tools that agents or assistants can invoke. Extending FunctionCallBase gives per-instance parameter overrides through OverridableFunctionCallInterface (added 1.3.3). Use [AI Agents](ai-agents.md) for configuring which tools an agent uses."
drupal_version: "11.x"
---

# Function Calling

## When to Use

> Use this guide when building custom tools that agents or assistants can invoke. Use [AI Agents](ai-agents.md) for configuring which tools an agent uses.

Function calls are tools that agents and assistants can invoke. They're plugins discovered in `src/Plugin/AiFunctionCall/`.

**Version:** checked against `drupal/ai` 1.4.7 and `drupal/tool` 1.0.0-beta11.

## Decision

| Situation | Choose | Why |
|-----------|--------|-----|
| Read-only operation | `information_tools` group | Search, lookup — signals safe to auto-run |
| Write operation | `modification_tools` group | Create, update, delete — signals caution |
| Organizing tools | `FunctionGroup` plugin | Organizational only — no logic |
| Allow per-agent parameter overrides | Extend `FunctionCallBase` | Already implements `OverridableFunctionCallInterface`; only a plugin that skips the base class and the interface cannot be limited |
| The capability must be callable from more than the AI module | A [Tool API](../tool-api/index.md) tool, not a `#[FunctionCall]` plugin | One plugin serves MCP (`mcp_server_tool_bridge`), ECA (`eca_tool`), Drush (`tool:run`) and the AI module (`tool_ai_connector`); a `#[FunctionCall]` plugin reaches only the AI module |

## Tool API Tools as Function Calls

The experimental `tool_ai_connector` submodule of `drupal/tool` derives one function call per Tool API tool. The plugin ID is `tool:<tool_id>`, the function name the model sees is `tool__<tool_id>` with every `:` replaced by `__`, and all of them sit in the `tool` group ("Tools API"), never in `information_tools` or `modification_tools`. See [Calling a Tool from the AI Module](../tool-api/calling-a-tool-from-the-ai-module.md).

Reference: `modules/contrib/tool/modules/tool_ai_connector/src/Plugin/AiFunctionCall/Derivative/ToolPluginDeriver.php`, `modules/contrib/tool/modules/tool_ai_connector/src/Plugin/AiFunctionGroup/ToolsApi.php`

## Creating a Custom Tool

```php
use Drupal\ai\Attribute\FunctionCall;
use Drupal\Core\Plugin\Context\ContextDefinition;

#[FunctionCall(
  id: 'mymodule:weather_lookup',
  function_name: 'get_weather',
  name: 'Weather Lookup',
  description: 'LLM reads this to decide when to call the tool.',
  group: 'information_tools',
  context_definitions: [
    'city' => new ContextDefinition(
      data_type: 'string',
      label: new TranslatableMarkup('City'),
      required: TRUE,
    ),
  ],
)]
class WeatherLookup extends FunctionCallBase {

  public function execute(): void {
    $city = $this->getContextValue('city');
    $result = $this->weatherService->lookup($city);
    $this->setOutput(json_encode($result));
  }
}
```

## Tool Groups

```php
use Drupal\ai\Attribute\FunctionGroup;

#[FunctionGroup(
  id: 'mymodule:content_tools',
  label: new TranslatableMarkup('Content Tools'),
  description: new TranslatableMarkup('Tools for content management'),
)]
class ContentTools extends FunctionGroupBase {
  // Groups are organizational — they don't have logic.
}
```

## OverridableFunctionCallInterface (added 1.3.3)

`FunctionCallBase` already implements this interface, so every plugin that extends it supports per-instance context definition overrides; there is nothing to opt into. When an agent configures this tool, the agent runner can override the default context definitions (parameter definitions) declared in the `#[FunctionCall]` attribute — for example, to restrict allowed values or pre-fill a parameter. The runner applies tool usage limits only when the plugin is an `OverridableFunctionCallInterface` instance; for any other plugin it logs an error and ignores the limits. A plugin that extends `FunctionCallBase` cannot opt out.

```php
use Drupal\ai\Base\FunctionCallBase;

// No explicit `implements`: FunctionCallBase already implements
// \Drupal\ai\Service\FunctionCalling\OverridableFunctionCallInterface, and the
// agent runner (ai_agents) calls setContextDefinitionOverride() on it.
class MyTool extends FunctionCallBase {
}
```

## Key Methods (FunctionCallBase)

| Method | Purpose |
|--------|---------|
| `execute()` | Main logic — call `setOutput()` when done |
| `getContextValue('param')` | Get LLM-provided parameter |
| `setOutput($data)` | Set the tool's return value |
| `getOutput()` | Retrieve output |

## Tool Groups Reference

| Group | Purpose |
|-------|---------|
| `information_tools` | Read-only operations (search, lookup) |
| `modification_tools` | Write operations (create, update, delete) |

## Common Mistakes

- **Wrong**: Writing vague tool descriptions → **Right**: The LLM reads the description to decide when to call the tool — be specific about what it does and what it doesn't do
- **Wrong**: No permission check in a `#[FunctionCall]` plugin's `execute()` → **Right**: Check `$this->currentUser->hasPermission()` before performing operations. This applies to `#[FunctionCall]` plugins only; a Tool API tool declares the `permission` attribute parameter and puts value-level rules in `checkAccess()` (see [Access Control](../tool-api/access-control.md))
- **Wrong**: Using the same ID format as core plugins → **Right**: Prefix with your module name (e.g., `mymodule:tool_name`)

## See Also

- [AI Agents](ai-agents.md)
- [AI Assistant API](ai-assistant-api.md)
- Reference: `modules/contrib/ai/src/Plugin/AiFunctionCall/`
