---
description: "Run a Tool API tool from your own PHP code with the plugin.manager.tool service and the five-step invoker sequence"
tldr: "Call checkPermission(), setInputValue(), validateInputs(), access() and execute() in that order, then read getResult() or getFormattedResult(). Gotcha: execute() does not check access; your code is the gate."
drupal_version: "^10.5 || ^11"
---

# Calling a Tool from PHP

## When to Use

> Use this when your own code runs a Tool API tool: a service, a queue worker, a form or a controller. Tool API ships no programmatic HTTP endpoint for running tools, so you call the manager and follow the invoker sequence.
>
> **Version:** applies to `drupal/tool` 1.0.0-beta11 (beta; no security advisory coverage). Paths are under `modules/contrib/tool/`.

## The Invoker

The **invoker** is the caller identity: a string or a `Drupal\tool\Tool\Invoker` passed as the third argument of `createInstance($plugin_id, array $configuration = [], string|Invoker|null $invoker = NULL)` (tool 1.0.0-beta11 `src/Tool/ToolManager.php`). Event subscribers read it to adapt values for that caller. An `Invoker` can also carry capabilities such as `InvokerCapability::EntitiesAsHandles`; see [Entity Inputs and Handles](entity-inputs-and-handles.md).

## The Invoker Sequence

The module documents one sequence for invokers (tool 1.0.0-beta11 `docs/developers/index.md`):

1. `ToolManager::checkPermission($definition, $account)` before touching caller input.
2. `setInputValue()` for each input.
3. `validateInputs()`; report violations as input errors.
4. `access($account, TRUE)`.
5. `execute()`; read `getResult()` or `getFormattedResult()`.

`tool:run` and the AI connector follow all five steps. Not every caller does: the Tool Explorer form skips `validateInputs()`, and the MCP bridge 1.0.0-beta3 skips the step 1 pre-check (mcp_server_tool_bridge `src/Plugin/mcp_server/Tool/ToolApi.php`).

## Pattern

Derived from `ToolRunCommand::executeTool()`; not a shipped controller. Inject `plugin.manager.tool`.

```php
use Drupal\tool\Tool\ToolManager;

// $account: the AccountInterface to check, for example $this->currentUser().
$definition = $this->toolManager->getDefinition('tool_belt:entity_list');
if (!ToolManager::checkPermission($definition, $account)->isAllowed()) {
  throw new AccessDeniedHttpException();
}
$tool = $this->toolManager->createInstance('tool_belt:entity_list');
$tool->setInputValue('entity_type_id', 'node');
if (($violations = $tool->validateInputs())->count() > 0) {
  // Correctable: report $violations to the caller.
}
elseif ($tool->access($account, TRUE)->isAllowed()) {
  $result = $tool->execute()->getResult();
}
```

## Raw vs Formatted Results

| Method | Gives | Use for |
|---|---|---|
| `getResult()->getContextValues()`, `getOutputValue($name)` | PHP values as the tool returned them | Further PHP processing |
| `getFormattedResult()` | Every result value after output transforms. Wire-format coercion applies even with no invoker: timestamps on core 11.1 and later, decimals, `datetime_iso8601` values with the `DateTime` constraint, and zero-keyed maps; handle conversion applies only with `EntitiesAsHandles` (tool 1.0.0-beta11 `src/EventSubscriber/OutputTypeCoercionSubscriber.php`). Memoized per execution | A wire format |

## From a Controller

A controller is your own route around the same sequence. The only route Tool API ships that runs a tool is the Tool Explorer admin form. Each point below is a recommendation:

- Gate the route with a `_permission` equal to the tool's declared permission, and still call `access()` with values (recommendation).
- Run `Write` and `Trigger` tools only from POST requests protected against CSRF, for example a form or a route with `_csrf_token: 'TRUE'` (recommendation).
- Return outputs through your own serializer or render array. Do not dump entities; Drush prints only `{entity_type, id, uuid, label}` because fields can hold secrets (recommendation).

## Decision

| If you need... | Use... |
|---|---|
| Defaults from stored config | `createInstance($id, $configuration)`; configuration values fill inputs you did not set |
| Values changed for one kind of caller | A subscriber to `ToolInputTransformEvent` or `ToolOutputTransformEvent` that checks `$event->getInvoker()?->id` (tool 1.0.0-beta11 `docs/developers/events.md`) |

## Common Mistakes

- Skipping `validateInputs()` and reporting an `access()` denial as "permission denied" → it may be bad input
- Calling `execute()` without `access()` → `execute()` does not check access; your code is the gate
- Creating a tool with a handle-capable `Invoker` in PHP and then passing objects → outputs become handle strings; use no invoker for PHP-to-PHP calls
- Reusing one tool instance for two calls → the instance holds inputs and the result; create a new instance per call (recommendation)

## See Also

- [Access Control](access-control.md) → the order of checks
- [Entity Inputs and Handles](entity-inputs-and-handles.md) → invoker capabilities
- Reference: `modules/contrib/tool/docs/developers/index.md`, `modules/contrib/tool/docs/developers/events.md`, `modules/contrib/tool/src/Drush/Commands/ToolRunCommand.php`
