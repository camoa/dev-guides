---
description: "Declare Tool API outputs, how execute() collects and validates them, and what reaches the caller"
tldr: "Declare every returned key with an output definition class. Gotchas: required defaults to TRUE, so a missing output turns success into a Runtime failure, and undeclared result keys still reach Drush, AI and MCP callers raw."
drupal_version: "^10.5 || ^11"
---

# Output Definitions

## When to Use

> Use this when declaring what a tool returns. Only declared keys become typed outputs, undeclared keys still reach callers raw, and a successful run that misses a required output becomes a failure.
>
> **Version:** applies to `drupal/tool` 1.0.0-beta11 (beta; no security advisory coverage). Paths are under `modules/contrib/tool/`.

## Classes

`OutputDefinition`, `EntityOutputDefinition`, `ListOutputDefinition` and `MapOutputDefinition`, all in `Drupal\tool\TypedData` and implementing `OutputDefinitionInterface`. Constructors mirror the input classes without `locked`:

```php
// tool 1.0.0-beta11 src/TypedData/OutputDefinition.php
public function __construct($data_type, string|TranslatableMarkup $label, string|TranslatableMarkup $description, $required = TRUE, $multiple = FALSE, $default_value = NULL, ?array $constraints = [], array $examples = [])
```

**`required` defaults to `TRUE` for outputs too.**

## How Outputs Are Collected

After `doExecute()` returns a success, `execute()` copies only the result values whose key matches a declared output, then validates the outputs:

```php
// tool 1.0.0-beta11 src/Tool/ToolBase.php, execute()
if ($this->result->isSuccess()) {
  if ($provided_definitions = $this->getOutputDefinitions()) {
    $this->outputs = [];
    foreach ($this->result->getContextValues() as $context_name => $value) {
      if (isset($provided_definitions[$context_name])) {
        $this->setOutputValue($context_name, $value);
      }
    }
  }
  $this->failOnOutputViolations();
}
```

`failOnOutputViolations()` replaces the success with a `Runtime` failure when a required output was not provided ("The @name output is required but was not provided.") or a value fails its definition. It logs the detail to the `tool` logger channel. Output checks are by shape: an entity output must be an entity of the declared type; its fields are not validated (tool 1.0.0-beta11 `src/TypedOutputsTrait.php`).

## What Reaches the Caller

Callers read `getFormattedResult()`, not the typed outputs. `getFormattedResult()` walks **every** result value, declared or not (tool 1.0.0-beta11 `src/Tool/ToolBase.php`):

| Result key | Typed output (`getOutputValue()`, validation) | Output transforms (handles, wire coercion) | Sent by Drush, AI connector, MCP bridge |
|---|---|---|---|
| Declared | Yes | Yes | Yes |
| Undeclared | No | No, passed through raw | Yes, raw |

## Decision

| If the output... | Declare... |
|---|---|
| Is always set on success | `required` left at `TRUE` |
| Is set only on some paths | `required: FALSE` |
| Is a list | `ListOutputDefinition` with an `item_definition` |
| Is a structured object | `MapOutputDefinition` with `OutputDefinitionInterface` properties |
| Is a content entity | `EntityOutputDefinition`. Handle-capable callers receive a handle (a `handle:<uuid>` string standing in for the entity; see [Entity Inputs and Handles](entity-inputs-and-handles.md)). A config entity passes through as an object |

## Common Mistakes

- Returning a key with no output definition and assuming it stays private → it reaches Drush, AI and MCP callers raw, with no handle conversion; an entity under an undeclared key leaves as an object
- Omitting a conditional output without `required: FALSE` → a correct run reports "Tool execution failed" with category `Runtime`
- Returning a value the definition cannot store (wrong structure) → `setOutputValue()` throws outside the `try` in `execute()`; Drush reports `execution_failed` (tool 1.0.0-beta11 `src/Drush/RunErrorType.php`)
- Declaring outputs with core `ContextDefinition` or an input class → deprecated in beta9, removed in rc1

## See Also

- [doExecute and ExecutableResult](doexecute-and-executableresult.md) → how results are built
- [Calling a Tool from PHP](calling-a-tool-from-php.md) → `getResult()` vs `getFormattedResult()`
- [Input Definitions](input-definitions.md) → the input side
- Reference: `modules/contrib/tool/src/TypedOutputsTrait.php`, `modules/contrib/tool/src/Tool/ToolBase.php`
