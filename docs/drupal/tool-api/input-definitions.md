---
description: "Declare Tool API inputs with InputDefinition, EntityInputDefinition, ListInputDefinition and MapInputDefinition: types, constraints, defaults, locking, coercion and refiners"
tldr: "Declare inputs with the typed-data definition classes; they drive validation, forms and the JSON Schema callers see. Gotcha: required defaults to TRUE, and an empty list or map still passes required; add NotBlank or Count."
drupal_version: "^10.5 || ^11"
---

# Input Definitions

## When to Use

> Use this when declaring what a tool accepts. Inputs are typed-data definitions; they drive validation, the Explorer form, the config schema suggestion, and the JSON Schema that AI and MCP callers see.
>
> **Version:** applies to `drupal/tool` 1.0.0-beta11 (beta; no security advisory coverage). Paths are under `modules/contrib/tool/`.

## Classes

All live in `Drupal\tool\TypedData` and implement `InputDefinitionInterface`.

| Class | Use for | Constructor (copied from tool 1.0.0-beta11) |
|---|---|---|
| `InputDefinition` | A scalar or any typed-data type | `($data_type, $label, $description, $required = TRUE, $multiple = FALSE, $default_value = NULL, ?array $constraints = [], bool $locked = FALSE, array $examples = [])` |
| `EntityInputDefinition` | An entity | `($data_type, $label, $description, $required = TRUE, $multiple = FALSE, $default_value = NULL, array $constraints = [], bool $locked = FALSE, array $examples = [])`; a bare `'node'` becomes `'entity:node'` |
| `ListInputDefinition` | A repeated value | `($label, $description, $required = TRUE, $default_value = NULL, array $constraints = [], ?InputDefinitionInterface $item_definition = NULL, bool $locked = FALSE)`; no item definition means items of type `any` |
| `MapInputDefinition` | An object with named properties | `($label, $description, $required = TRUE, $multiple = FALSE, $default_value = NULL, array $constraints = [], array $property_definitions = [], bool $locked = FALSE)`; every property must be an `InputDefinitionInterface` |

`label` and `description` have no default. **`required` defaults to `TRUE`.**

## Data Types and Constraints

`data_type` is any core typed-data type ID: `string`, `integer`, `float`, `decimal`, `boolean`, `email`, `uri`, `timestamp`, `datetime_iso8601`, `map`, `list`, `any`, `entity`, `entity:<type>`. The module adds a `text` data type (tool 1.0.0-beta11 `src/Plugin/DataType/TextData.php`).

`constraints` takes any validation constraint by plugin name, for example `['Choice' => ['choices' => ['ASC', 'DESC']]]`. The module adds `DateTime`, `DateOnly`, `FieldExists`, `GreaterThan`, `GreaterThanOrEqual`, `LessThan`, `LessThanOrEqual`, `IdenticalTo` and `PositiveOrZero` (tool 1.0.0-beta11 `src/Plugin/Validation/Constraint/`).

**Enums in the JSON Schema.** `Choice` and `AllowedValues` become a JSON Schema `enum` and are never limited. Enums derived from site state (`PluginExists`, `EntityBundleExists`) are **left out entirely** when they would exceed 50 entries; they are not truncated (`DERIVED_ENUM_LIMIT` in `src/Normalizer/ContextDefinitionNormalizer.php`).

## Pattern

A list input, from the shipped agent skill reference (tool 1.0.0-beta11 `.agents/skills/create-tool-plugins/references/anatomy.md`):

```php
new ListInputDefinition(
  label: new TranslatableMarkup('Tags'),
  description: new TranslatableMarkup('...'),
  required: FALSE,
  constraints: ['Count' => ['max' => 10]],       // binds the list
  item_definition: new InputDefinition(
    data_type: 'string',
    label: '',
    description: '',
    constraints: ['Length' => ['max' => 64]],    // binds each value
  ),
);
```

## Input Semantics

- **Required means present and not NULL.** An empty list `[]` or map `{}` passes `required`. Add `NotBlank` or `Count` to demand content (tool 1.0.0-beta11 `docs/developers/input-output-definitions.md`).
- **An unset input takes the definition default.** A required input explicitly set to NULL, with a NULL default, is reported by `validateInputs()`. If `access()` or `execute()` runs without `validateInputs()` first, `resolveDefaultValue()` throws `ContextException`, which is not an `\InvalidArgumentException`. `access()` catches only `\InvalidArgumentException`, so it throws the exception uncaught. `execute()` reports a `Runtime` failure with only the class name (tool 1.0.0-beta11 `src/TypedInputsTrait.php`, `src/Tool/ToolBase.php`). The JSON Schema lists every required input under `required`, defaults or not.
- **Value order:** locked default, then explicit input, then configuration value, then definition default (tool 1.0.0-beta11 `src/TypedInputsTrait.php`, `getExecutableValue()`).
- **`locked: TRUE`** fixes the value to the default. `setInputValue()` on it throws `InputException` "The @name input is locked and cannot be changed." Locked inputs are hidden from `getInputDefinitions()` unless you pass `TRUE`.
- **Absent map properties are left unchanged.** A required property that is absent is a violation.
- **List items cannot be NULL.** `setInputValue()` throws "The @name input must not contain NULL items."
- **Coercion.** `InputTypeCoercionSubscriber` runs at priority 50 on every value passed to `setInputValue()`. It runs after invoker-specific subscribers (the invoker is the caller identity passed to `createInstance()`; see [Calling a Tool from PHP](calling-a-tool-from-php.md)), such as handle resolution (100), and before the recursive subscriber (-100). Configuration values and defaults are not coerced. It changes only unambiguous values: JSON strings to maps or lists, a scalar to a one-item list, `"true"` to `TRUE`, `"5"` to `5`, near-miss enum casing (tool 1.0.0-beta11 `src/EventSubscriber/InputTypeCoercionSubscriber.php`).
- **Validation is by shape.** Lists are validated per item and maps per property against their definitions; declared list and map constraints run separately (tool 1.0.0-beta11 `src/TypedInputsTrait.php`, `validateInputValue()`).
- **The root schema rejects unknown names.** `normalizeInputSchema()` emits `additionalProperties: FALSE` at the root only; maps stay open (tool 1.0.0-beta11 `src/Normalizer/ToolDefinitionSerializer.php`).
- **`examples`** are emitted as JSON Schema `examples` and never validated.

## Refiners

A refiner narrows one input from the values of others, for example a `bundle` list that depends on `entity_type_id`. Declare `input_definition_refiners: ['field_name' => ['entity']]` and implement `Drupal\tool\TypedData\InputDefinitionRefinerInterface::refineInputDefinition($name, $definition, $values)`. The refiner runs only when every dependency has a non-NULL, valid value. A refinement that changes the data type or multiplicity throws `\LogicException` (tool 1.0.0-beta11 `src/TypedInputsTrait.php`, `assertRefinementNarrows()`). Real example: `tool_belt:field_set_value` (tool_belt 1.0.0-alpha6 `modules/tool_belt_content/src/Plugin/tool/Tool/FieldSetValue.php`).

## Common Mistakes

- Forgetting `required: FALSE` on optional inputs → every input is required by default; callers get validation failures
- Using `multiple: TRUE` → deprecated in beta10, removed in rc1; declare a `ListInputDefinition`
- A write tool that accepts a required map and saves it → `{}` passes `required` and can wipe config; add `NotBlank`
- Putting item constraints on a `ListInputDefinition` → they bind the list; put them on `item_definition`
- Expecting a refiner to widen a type → it can only narrow; widen in the declaration

## See Also

- [Output Definitions](output-definitions.md) → the output side
- [Entity Inputs and Handles](entity-inputs-and-handles.md) → entity inputs
- Reference: `modules/contrib/tool/src/TypedData/`, `modules/contrib/tool/src/TypedInputsTrait.php`, `modules/contrib/tool/docs/developers/input-output-definitions.md`
