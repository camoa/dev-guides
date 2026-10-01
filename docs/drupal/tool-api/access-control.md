---
description: "Control who may run a Tool API tool with the permission attribute, checkAccess() and the order of access checks"
tldr: "Declare permission for account-level rules and override checkAccess() for rules on input values; access() runs permission, then validation, then checkAccess(). Gotcha: the override must keep the return_as_object parameter."
drupal_version: "^10.5 || ^11"
---

# Access Control

## When to Use

> Use this when deciding who may run a tool. A tool must declare a `permission`, or override `checkAccess()` (or `access()` itself), or both; `access()` runs the permission, then input validation, then `checkAccess()`.
>
> **Version:** applies to `drupal/tool` 1.0.0-beta11 (beta; no security advisory coverage). Paths are under `modules/contrib/tool/`.

## The Permission String

`permission` uses route `_permission` syntax. `ToolManager::checkPermission()` parses it:

```php
// tool 1.0.0-beta11 src/Tool/ToolManager.php
$split = explode(',', $permission);
$access = count($split) > 1
  ? AccessResult::allowedIfHasPermissions($account, array_map('trim', $split), 'AND')
  : AccessResult::allowedIfHasPermissions($account, array_map('trim', explode('+', $permission)), 'OR');
```

| String | Meaning |
|---|---|
| `'administer users'` | One permission |
| `'a, b'` | All of them (comma = AND) |
| `'a+b'` | Any one of them (plus = OR) |
| `'a,b+c'` | Rejected at discovery with `InvalidPluginDefinitionException` |
| `NULL` or `''` | No declared permission. `checkPermission()` then returns **allowed** for every account |

A name that matches no defined permission denies every account except user 1 and administrator roles. `drush tool:info` prints a warning for unknown names (tool 1.0.0-beta11 `src/Drush/Commands/ToolInfoCommand.php`).

## Order of Checks

```php
// tool 1.0.0-beta11 src/Tool/ToolBase.php, access()
$permission_access = ToolManager::checkPermission($definition, $account);
if (!$permission_access->isAllowed()) {
  return $return_as_object ? $permission_access : FALSE;
}
try {
  $values = $this->getExecutableValues();
}
catch (\InvalidArgumentException) {
  $access = AccessResult::forbidden('Tool input validation failed.')->setCacheMaxAge(0);
  return $return_as_object ? $access : FALSE;
}
$check = $this->checkAccess($values, $account, TRUE);
$result = $permission_access->andIf(is_bool($check) ? AccessResult::allowedIf($check)->setCacheMaxAge(0) : $check);
```

1. Declared permission. 2. Input resolution and validation. 3. `checkAccess()` with resolved values. The results combine with `andIf()`, so `checkAccess()` never needs to re-check the permission.

## checkAccess()

`checkAccess()` is **not abstract** in beta11. Its real signature and default:

```php
// tool 1.0.0-beta11 src/Tool/ToolBase.php
protected function checkAccess(array $values, AccountInterface $account, bool $return_as_object = FALSE): bool|AccessResultInterface {
  $definition = $this->getPluginDefinition();
  $access = AccessResult::allowedIf($definition->getPermission() !== NULL);
  return $return_as_object ? $access : $access->isAllowed();
}
```

A tool with no permission and neither `checkAccess()` nor `access()` overridden is rejected when definitions rebuild (tool 1.0.0-beta11 `src/Tool/ToolManager.php`, `processDefinition()`).

## Decision

| If the rule... | Use... | Why |
|---|---|---|
| Depends only on the account | `permission:` | Callers that pre-check it deny before touching input, so handle resolution and refiners never run for a denied account. `tool:run`, the AI connector and Tool Explorer pre-check; the MCP bridge 1.0.0-beta3 does not, and denies only inside `access()` after inputs are set |
| Depends on the input values (this node, this field) | `checkAccess()` delegating to entity or field access | Values are resolved and validated when it runs |
| Needs both | `permission:` plus `checkAccess()` | Both must allow |
| Must list tools for an account without instantiating them | `ToolManager::checkPermission($definition, $account)` | Static, cacheable, works from `getDefinitions()` |

Real value-dependent example, delegating to entity access:

```php
// tool_belt 1.0.0-alpha6 modules/tool_belt_content/src/Plugin/tool/Tool/EntitySave.php
if ($entity->isNew()) {
  $access_handler = $this->entityTypeManager->getHandler($entity->getEntityTypeId(), 'access');
  $access_result = $access_handler->createAccess($entity->bundle(), $account, [], TRUE);
}
else {
  $access_result = $entity->access('update', $account, TRUE);
}
return $return_as_object ? $access_result : $access_result->isAllowed();
```

## Common Mistakes

- Copying a two-argument `checkAccess(array $values, AccountInterface $account): bool` from older examples → PHP fatal; the override must keep `bool $return_as_object = FALSE` and return `bool|AccessResultInterface`
- Checking `hasPermission()` inside `doExecute()` → that advice in the AI module pages is for `#[FunctionCall]` plugins; a Tool API tool declares `permission:` and uses `checkAccess()` for value-level rules
- Calling `access()` first and reporting its denial → invalid input also returns Forbidden ("Tool input validation failed."). Call `validateInputs()` first, as `tool:run`, the AI connector and the MCP bridge do
- Overriding `access()` itself → you bypass the declared permission unless you call `parent::access()` or `ToolManager::checkPermission()` (tool 1.0.0-beta11 `src/Tool/ToolInterface.php`)
- Using a permission for a rule that depends on the entity (for example `administer node fields`) → keep it in `checkAccess()`
- Checking field access without the passed account → Tool Belt's `entity_field_values` calls `->access('view')` with no account, so it checks the current user, not the `$account` given to `checkAccess()` (its own `@todo`); always pass `$account`
- Assuming a tool without `permission` is hidden from catalogs → `checkPermission()` allows it for everyone; only `checkAccess()` denies later
- Shipping the generated `checkAccess()` that throws `\LogicException` → `access()` does not catch it, so every invoker gets an exception, not a clean denial; replace it before use

## See Also

- [Defining a Tool](defining-a-tool.md) → the `permission` attribute
- [Calling a Tool from PHP](calling-a-tool-from-php.md) → the full invoker sequence
- [Security Checklist](security-best-practices.md)
- Reference: `modules/contrib/tool/src/Tool/ToolBase.php`, `modules/contrib/tool/src/Tool/ToolManager.php`, `modules/contrib/tool/src/Tool/ToolInterface.php`, `modules/contrib/tool/docs/configuration.md`
