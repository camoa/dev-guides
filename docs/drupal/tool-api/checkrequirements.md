---
description: "Report missing configuration with checkRequirements() and RequirementsException, and know that it never blocks execution"
tldr: "Throw RequirementsException from checkRequirements() for missing deployment config such as a module or API key. Gotcha: it is a configuration-time signal; execute() and access() never call it, so re-check blockers in doExecute()."
drupal_version: "^10.5 || ^11"
---

# checkRequirements

## When to Use

> Use this when a tool needs static configuration, such as an API key or an enabled module. `checkRequirements()` reports what is missing to listing and configuration UIs; it never blocks execution.
>
> **Version:** applies to `drupal/tool` 1.0.0-beta11 (beta; no security advisory coverage). Paths are under `modules/contrib/tool/`.

## Pattern

Override it and throw `Drupal\tool\Exception\RequirementsException` with a message that says what is missing:

```php
// tool_belt 1.0.0-alpha6 modules/tool_belt_content/src/Plugin/tool/Tool/TextFormatExplain.php
public function checkRequirements(): void {
  if (!$this->moduleHandler->moduleExists('filter')) {
    throw new RequirementsException('The filter module is not installed, so there are no text formats to explain.');
  }
}
```

The default in `ToolBase` does nothing. `RequirementsException` extends `\RuntimeException` (tool 1.0.0-beta11 `src/Exception/RequirementsException.php`).

## Who Calls It

Within Tool API, only the Drush commands call it, through `RequirementStatus::forTool()` (tool 1.0.0-beta11 `src/Drush/RequirementStatus.php`). `tool:list`, `tool:search` and `tool:info` show `Met` or the exception message; `--unmet=hide|only` filters on it. Outside Tool API, `eca_tool` calls it only in its action configuration form and shows a warning (eca_tool 1.0.0-beta1 `src/Plugin/Action/Tool.php`, `buildRequirementsElement()`).

`execute()` and `access()` do not call it. The interface says so on purpose:

```php
// tool 1.0.0-beta11 src/Tool/ToolInterface.php
// This is a configuration-time signal, not a runtime gate (#3582975):
// configuration and curation UIs call it to show an unmet-requirements
// indicator and to prevent a tool from being added to something, but
// execute() and access() deliberately never consult it.
```

Issue [#3582975](https://git.drupalcode.org/project/tool/-/work_items/3582975), "Define checkRequirements() as a configuration-time signal (indicator + add-prevention), not a runtime gate", closed 2026-08-10, marks runtime enforcement as **rejected**. The rc1 meta [#3582978](https://git.drupalcode.org/project/tool/-/work_items/3582978) (last updated 2026-09-20) still carries an older line, "wire it: enforce at execute", next to a link to that closed issue. The code and the closed issue agree; the meta line is out of date.

## Decision

| If the prerequisite... | Then... |
|---|---|
| Is deployment config (module, API key, setting) | Throw `RequirementsException` in `checkRequirements()` |
| Can change per call (network, rate limit, stale token) | Return `ExecutableResult::failure(..., FailureCategory::Runtime)` from `doExecute()` |
| Must block execution | Check it again in `doExecute()`; `checkRequirements()` will not block it |

## Common Mistakes

- Relying on `checkRequirements()` to stop execution → it never does; Tool Belt's `TextFormatExplain` repeats the check in `doExecute()` for this reason
- Putting an HTTP health check or an entity query in it → `tool:list` instantiates and checks every listed tool, so every listing pays for it
- Expecting the AI connector to hide tools with unmet requirements → its deriver exposes every tool

## See Also

- [Calling a Tool from Drush](calling-a-tool-from-drush.md) → the `--unmet` option
- [Performance Checklist](performance-best-practices.md)
- Reference: `modules/contrib/tool/src/Tool/ToolInterface.php`, `modules/contrib/tool/src/Drush/RequirementStatus.php`, https://git.drupalcode.org/project/tool/-/work_items/3582975
