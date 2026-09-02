---
description: Function calling tools — building custom FunctionCall plugins for AI agents and assistants
tldr: "Use this guide when building custom tools that agents or assistants can invoke. Implement OverridableFunctionCallInterface (added 1.3.3) to allow per-instance parameter overrides. Use [AI Agents](ai-agents.md) for configuring which tools an agent uses."
drupal_version: "11.x"
---

# Function Calling

## When to Use

> Use this guide when building custom tools that agents or assistants can invoke. Use [AI Agents](ai-agents.md) for configuring which tools an agent uses.

Function calls are tools that agents and assistants can invoke. They're plugins discovered in `src/Plugin/AiFunctionCall/`.

## Decision

| Situation | Choose | Why |
|-----------|--------|-----|
| Read-only operation | `information_tools` group | Search, lookup — signals safe to auto-run |
| Write operation | `modification_tools` group | Create, update, delete — signals caution |
| Organizing tools | `FunctionGroup` plugin | Organizational only — no logic |
| Allow per-agent parameter overrides | `OverridableFunctionCallInterface` | Opt-in; tools that must not be customized don't implement this |

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

Implement this interface on your `FunctionCallBase` plugin to support per-instance context definition overrides. When an agent or assistant configures this tool, it can override the default context definitions (parameter definitions) declared in the `#[FunctionCall]` attribute — for example, to restrict allowed values or pre-fill a parameter. Tools that should never be customized per-instance do not need this interface.

```php
use Drupal\ai\Interface\OverridableFunctionCallInterface;

class MyTool extends FunctionCallBase implements OverridableFunctionCallInterface {
  // The plugin manager and agent runner handle the override mechanics.
  // Implementing this interface is the signal that overrides are accepted.
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
- **Wrong**: No permission check in `execute()` → **Right**: Always check `$this->currentUser->hasPermission()` before performing operations
- **Wrong**: Using the same ID format as core plugins → **Right**: Prefix with your module name (e.g., `mymodule:tool_name`)

## See Also

- [AI Agents](ai-agents.md)
- [AI Assistant API](ai-assistant-api.md)
- Reference: `web/modules/contrib/ai/src/Plugin/AiFunctionCall/`
