---
description: "Take or return entities in a Tool API tool: entity objects from PHP, handle strings from AI and MCP callers, and none from Drush"
tldr: "An entity input receives the loaded entity; AI and MCP invokers with EntitiesAsHandles pass handle:<uuid> strings instead. Gotcha: Drush cannot pass entities, so a tool for scripts should take an entity type and ID."
drupal_version: "^10.5 || ^11"
---

# Entity Inputs and Handles

## When to Use

> Use this when a tool takes or returns an entity. Who can supply an entity depends on the caller: PHP passes objects, AI and MCP pass handle strings, and Drush cannot pass entities at all.
>
> **Version:** applies to `drupal/tool` 1.0.0-beta11 (beta; no security advisory coverage). Paths are under `modules/contrib/tool/`.

## How It Works

An entity input receives the **loaded entity object** in `$values`. Validation checks only that the value is an entity of the declared type and bundle; it does not validate the entity's fields (tool 1.0.0-beta11 `src/TypedInputsTrait.php`).

The **invoker** is the caller identity passed to `ToolManager::createInstance()`. Callers that cannot carry objects declare a capability on it:

```php
// tool 1.0.0-beta11 tool.api.php
$tool = $this->toolManager->createInstance(
  $plugin_id,
  [],
  new Invoker('my_connector', InvokerCapability::EntitiesAsHandles),
);
```

With `EntitiesAsHandles`, Tool API:

- resolves `handle:<uuid>` strings to entities on input;
- stores **content entity** outputs in the private tempstore collection `tool_handles` and replaces them with handle strings plus a hint the model can read; any other value, a config entity included, passes through unchanged;
- describes content entity inputs and outputs as strings in the JSON Schema.

(tool 1.0.0-beta11 `src/Handle/ToolHandleStore.php`, `src/Handle/EntityHandleTransformer.php`, `src/EventSubscriber/EntityHandleTransformSubscriber.php`)

## Decision

| Caller | Invoker | Can it pass an entity? |
|---|---|---|
| Your PHP code | none, or a plain string | Yes, pass the entity object |
| `tool_ai_connector` | `tool_ai_connector` + `EntitiesAsHandles` | Yes, as a handle from an earlier tool call |
| `mcp_server_tool_bridge` | `mcp_server` + `EntitiesAsHandles` | Yes, as a handle |
| Drush `tool:run` | `drush`, no capabilities | **No** |
| Tool Explorer execute form | none | Through the entity form widget |
| Orchestration `orchestration_tool` | none, per that page | An entity ID in the request config, loaded by the provider. Reported by [Tool API Provider](../orchestration/tool-api-provider.md); not read in code for this page |

For a Drush caller, validation says so:

```php
// tool 1.0.0-beta11 src/TypedInputsTrait.php
'The @label input must be an entity. The @invoker invoker cannot pass entities; use a tool that takes an entity type and ID instead.'
```

## Pattern

If a tool must run from Drush or a script, take an entity type and ID as strings and load the entity inside. If it serves AI or MCP chains, an entity input lets one tool's output handle feed the next tool.

## Common Mistakes

- Expecting `drush tool:run tool_belt:entity_save --input='{"entity":1}'` to work → the Drush invoker cannot supply entities; this fails validation
- Passing a config entity through a handle → handles cover content entities only; `resolveInput()` throws `UnexpectedHandleValueException` for anything else
- Re-loading the entity from an ID inside `doExecute()` when the input is already an entity → use the object you received; the access check ran against it
- Sharing handles across users → the store is the per-user private tempstore; another account cannot resolve the handle
- Treating a handle exception as a system failure in your own invoker → `HandleNotFoundException` (for example an expired handle), `InvalidHandleException` and `UnexpectedHandleValueException` all implement `HandleExceptionInterface`; catch the interface and report it as a correctable input error, as `tool_ai_connector` does (tool 1.0.0-beta11 `docs/developers/entity-handles.md`)

## See Also

- [Input Definitions](input-definitions.md) → definitions in general
- [Calling a Tool from PHP](calling-a-tool-from-php.md) → invokers
- [Calling a Tool from the AI Module](calling-a-tool-from-the-ai-module.md), [Calling a Tool over MCP](calling-a-tool-over-mcp.md) → handle-capable callers
- Reference: `modules/contrib/tool/tool.api.php` (`tool_entity_handles` group), `modules/contrib/tool/src/Handle/`, `modules/contrib/tool/docs/developers/entity-handles.md`
