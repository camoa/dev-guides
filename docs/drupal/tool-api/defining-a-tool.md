---
description: "Write a Tool API plugin: file location, every #[Tool] attribute parameter, the plugin ID rule, and service injection through create()"
tldr: "A tool lives in src/Plugin/tool/Tool, carries #[Tool] and extends ToolBase; inject services by overriding create(). Gotcha: one tool with no permission and no checkAccess() override breaks discovery for every tool."
drupal_version: "^10.5 || ^11"
---

# Defining a Tool

## When to Use

> Use this when writing a Tool API plugin. It covers the file location, every `#[Tool]` parameter, the ID rule, and how to inject services into a class whose constructor is `final`.
>
> **Version:** applies to `drupal/tool` 1.0.0-beta11 (beta; no security advisory coverage). Paths are under `modules/contrib/tool/`.

## The Attribute

A tool lives in `src/Plugin/tool/Tool/` of your module, in namespace `Drupal\<module>\Plugin\tool\Tool`, carries `#[Tool]` from `Drupal\tool\Attribute\Tool`, and extends `Drupal\tool\Tool\ToolBase`. The manager discovers `Plugin/tool/Tool` with interface `ToolInterface` (tool 1.0.0-beta11 `src/Tool/ToolManager.php`). Parameters, from the attribute constructor in `src/Attribute/Tool.php`:

| Parameter | Required | Default | What it does |
|---|---|---|---|
| `id` | yes | | Plugin ID. See the ID rule below |
| `label` | yes | | Human name. Also the AI function's `name` |
| `description` | yes | | What the tool does. Always the AI function description. The MCP description too, unless the `mcp_tool_config` entity sets its own (mcp_server_tool_bridge 1.0.0-beta3 `src/Plugin/Derivative/McpToolConfigDeriver.php`) |
| `operation` | yes | | A `ToolOperation` case. See [Operation and Destructive](operation-and-destructive.md) |
| `destructive` | no | `FALSE` | Metadata that callers may use to ask for confirmation. Nothing in Tool API enforces it |
| `input_definitions` | no | `[]` | Inputs keyed by name. See [Input Definitions](input-definitions.md) |
| `input_definition_refiners` | no | `[]` | Map of `target_input => [dependency inputs]`. The class must implement `InputDefinitionRefinerInterface`, or `Tool::get()` throws `\InvalidArgumentException` |
| `output_definitions` | no | `[]` | Outputs keyed by name. See [Output Definitions](output-definitions.md) |
| `deriver` | no | `NULL` | A deriver class, to produce many tools from one class |
| `forms` | no | `[]` | Form classes keyed by operation. The manager adds `configure` (`ConfigureToolPluginForm`) and `execute` (`ExecuteToolPluginForm`) when absent |
| `icon` | no | `NULL` | A core Icon API ID `pack_id:icon_id`, stored as-is. An unresolvable reference means no icon |
| `permission` | no | `NULL` | Route-style permission string. See [Access Control](access-control.md) |

## The ID Rule

The attribute docblock states the rule and calls its cause "implementation bugs":

```php
// tool 1.0.0-beta11 src/Attribute/Tool.php
// It must be either identical to group or prefixed with the group.
// E.g. if the group is "foo" the ID must be either "foo" or "foo:bar".
```

In practice, use a single token (`send_email`) or `prefix:name`. Tool Belt prefixes all 58 of its tools with `tool_belt:` (for example `tool_belt:entity_save`) without a deriver, and they are discovered. Core treats `:` as the derivative separator (`core/lib/Drupal/Component/Plugin/Discovery/DerivativeDiscoveryDecorator.php`). **Unverified:** which other ID shapes fail, and how. The shipped agent skill says a wrong shape is "silently not discovered" (tool 1.0.0-beta11 `.agents/skills/create-tool-plugins/references/anatomy.md`); no code path in Tool API showed this.

## Pattern

The module's own minimal example (tool 1.0.0-beta11 `docs/developers/creating-a-tool.md`), trimmed. Two changes: the optional `greeting` input is dropped, and the docs' allow-everyone `checkAccess()` override is replaced by a `permission` line.

```php
namespace Drupal\my_module\Plugin\tool\Tool;

use Drupal\Core\StringTranslation\TranslatableMarkup;
use Drupal\tool\Attribute\Tool;
use Drupal\tool\ExecutableResult;
use Drupal\tool\Tool\ToolBase;
use Drupal\tool\Tool\ToolOperation;
use Drupal\tool\TypedData\InputDefinition;
use Drupal\tool\TypedData\OutputDefinition;

#[Tool(
  id: 'greeting_tool',
  label: new TranslatableMarkup('Greeting Tool'),
  description: new TranslatableMarkup('Generates a greeting message.'),
  operation: ToolOperation::Transform,
  permission: 'access content',
  input_definitions: [
    'name' => new InputDefinition(data_type: 'string', label: new TranslatableMarkup('Name'), description: new TranslatableMarkup('The name to greet.')),
  ],
  output_definitions: [
    'message' => new OutputDefinition(data_type: 'string', label: new TranslatableMarkup('Message'), description: new TranslatableMarkup('The generated greeting message.')),
  ],
)]
final class GreetingTool extends ToolBase {
  protected function doExecute(array $values): ExecutableResult {
    return ExecutableResult::success(new TranslatableMarkup('Greeting generated.'), ['message' => "Hello, {$values['name']}!"]);
  }
}
```

Remove the `permission` line without adding a `checkAccess()` override, and discovery rejects the class. See [Access Control](access-control.md).

## Injecting Services

The `ToolBase` constructor is `final`. Override `create()` and call the parent:

```php
// tool_belt 1.0.0-alpha6 modules/tool_belt_content/src/Plugin/tool/Tool/EntitySave.php
public static function create(ContainerInterface $container, array $configuration, $plugin_id, $plugin_definition) {
  $instance = parent::create($container, $configuration, $plugin_id, $plugin_definition);
  $instance->entityTypeManager = $container->get('entity_type.manager');
  return $instance;
}
```

`ToolBase` already injects `$currentUser`, `$eventDispatcher` and `$logger` (channel `logger.channel.tool`). A subclass that redeclares `$logger` must type it exactly `LoggerChannelInterface` (tool 1.0.0-beta11 `src/Tool/ToolBase.php`).

## Common Mistakes

- Overriding `__construct()` → fatal, it is `final`; override `create()`
- No `permission` and no `checkAccess()`/`access()` override → `InvalidPluginDefinitionException` at cache rebuild. Core's `DefaultPluginManager::findDefinitions()` does not catch it, so **one such tool breaks `getDefinitions()` for every tool** (core 11.4.5 `core/lib/Drupal/Core/Plugin/DefaultPluginManager.php`)
- Declaring `input_definition_refiners` on a class that does not implement `InputDefinitionRefinerInterface` → `\InvalidArgumentException` at discovery, with the same site-wide effect
- A refiner naming an input that does not exist → `ContextException` from `ToolDefinition::setInputDefinitionRefiners()`
- Writing `description` as developer notes → it is the text an LLM or MCP client reads to choose the tool; state what the tool does and its side effects
- Trusting the shipped `create-tool-plugins` agent skill reference for the base class → its `anatomy.md` still says `checkAccess()` is abstract and shows a four-argument constructor; beta11 code differs

## See Also

- [Operation and Destructive](operation-and-destructive.md) → next decision in the attribute
- [Access Control](access-control.md) → `permission` and `checkAccess()`
- [Scaffolding with drush generate](scaffolding-with-drush-generate.md) → generate this file
- Reference: `modules/contrib/tool/src/Attribute/Tool.php`, `modules/contrib/tool/src/Tool/ToolManager.php`, `modules/contrib/tool/src/Tool/ToolBase.php`, `modules/contrib/tool/docs/developers/creating-a-tool.md`
