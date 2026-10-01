---
description: "Prepare Tool API code for 1.0.0-rc1: deprecated multiple inputs, output declarations, a renamed alter hook and ExecutableResultInterface"
tldr: "Before updating drupal/tool, replace multiple: TRUE with List definitions, declare outputs with output classes, rename the adapter alter hook and drop ExecutableResultInterface. Gotcha: rc1 removes the conversion shims."
drupal_version: "^10.5 || ^11"
---

# Preparing for Tool API 1.0.0-rc1

## When to Use

> Use this before updating `drupal/tool`, or when a Tool API deprecation notice appears. Only items with a `@deprecated` marker or a "removed from tool:1.0.0-rc1" notice in beta11 code are listed as removals. This page goes stale when rc1 ships.
>
> **Version:** applies to `drupal/tool` 1.0.0-beta11 (beta; no security advisory coverage). Paths are under `modules/contrib/tool/`.

## Removals Announced in Code

| Deprecated | Since | Replacement | Runtime notice | Issue |
|---|---|---|---|---|
| `multiple: TRUE` on an input, an output, a map property, or a refined definition | beta10 | `ListInputDefinition` / `ListOutputDefinition` | `E_USER_DEPRECATED` | [#3583049](https://git.drupalcode.org/project/tool/-/work_items/3583049) |
| Declaring an output with a core `ContextDefinition` or an input definition class | beta9 | An `OutputDefinitionInterface` class | `E_USER_DEPRECATED` | [#3583050](https://git.drupalcode.org/project/tool/-/work_items/3583050) |
| `hook_data_type_adapter_info_alter()` | beta4 | `hook_tool_typed_data_adapter_info_alter()` | `E_USER_DEPRECATED` | [#3582963](https://www.drupal.org/project/tool/issues/3582963) |
| `Drupal\tool\ExecutableResultInterface` (now an empty shell) | beta4 | `Drupal\tool\Tool\ToolInterface`; `Drupal\tool\ToolResultInterface` for results | None: `@deprecated` docblock only, so only static analysis reports it | [#3582964](https://git.drupalcode.org/project/tool/-/work_items/3582964) |

Example notice:

```php
// tool 1.0.0-beta11 src/Tool/ToolDefinition.php
@trigger_error(sprintf("Declaring the '%s' input with multiple: TRUE is deprecated in tool:1.0.0-beta10 and is removed from tool:1.0.0-rc1. Declare a ListInputDefinition instead. See https://git.drupalcode.org/project/tool/-/work_items/3583049", $name), E_USER_DEPRECATED);
```

`@internal` helpers that go with them: `ListInputDefinition::fromMultiple()`, `OutputDefinition::fromContextDefinition()`.

## What the rc1 Meta States

Issue [#3582978](https://git.drupalcode.org/project/tool/-/work_items/3582978) "[META] Path to 1.0.0-rc1" (open, last updated 2026-09-20) states an **API freeze must land before the RC1 tag**, and "Frozen at RC1: everything in `src/`". Its `checkRequirements()` line is out of date; see [checkRequirements](checkrequirements.md).

## Steps

1. Run your tests with deprecations shown, run static analysis for `ExecutableResultInterface`, and grep for `multiple: TRUE` and `ContextDefinition(` in tool attributes.
2. Convert to `List*Definition` and `*OutputDefinition` classes.
3. Rename any `hook_data_type_adapter_info_alter()` implementation.
4. Replace `instanceof ExecutableResultInterface` with `ToolInterface` or `ToolResultInterface`.

## Common Mistakes

- Waiting for rc1 to convert → rc1 removes the conversion; declarations using `multiple: TRUE` will no longer be converted
- Splitting constraints wrongly when converting a `multiple` declaration by hand → `ListInputDefinition::fromMultiple()` keeps `Count` on the list and moves every other constraint to `item_definition`; do the same
- Assuming nothing else changes → the API is not frozen until rc1; read each beta's release notes

## See Also

- [Input Definitions](input-definitions.md), [Output Definitions](output-definitions.md) → the replacement classes
- Reference: `modules/contrib/tool/src/Tool/ToolDefinition.php`, `modules/contrib/tool/src/ExecutableResultInterface.php`, `modules/contrib/tool/src/TypedData/Adapter/TypedDataAdapterManager.php`, `modules/contrib/tool/src/TypedData/ListInputDefinition.php`
