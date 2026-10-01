---
description: "Performance checklist for sites with many Tool API tools or tools run in loops"
tldr: "Keep create() and checkRequirements() cheap, filter catalogs with static checkPermission(), cache expensive Read tools inside doExecute() and page list tools. Gotcha: Tool API never caches tool results."
drupal_version: "^10.5 || ^11"
---

# Performance Checklist

## When to Use

> Run through this when a site has many Tool API tools or tools run in loops. The costs sit in instantiation, listing and schema building. Each item links to the page that owns the rule.
>
> **Version:** applies to `drupal/tool` 1.0.0-beta11 (beta; no security advisory coverage). Paths are under `modules/contrib/tool/`.

## Checklist

- [ ] `create()` and `checkRequirements()` are cheap: no HTTP calls, no entity queries. Drush listings instantiate and check every listed tool → [checkRequirements](checkrequirements.md)
- [ ] Catalogs filter with static `ToolManager::checkPermission()`, not by instantiating tools → [Access Control](access-control.md)
- [ ] `drush cr` runs after tool changes, then `drush tool:list` confirms discovery; one bad definition breaks every tool → [Defining a Tool](defining-a-tool.md)
- [ ] Expensive `Read` tools cache inside `doExecute()`; Tool API does not cache results → [doExecute and ExecutableResult](doexecute-and-executableresult.md)
- [ ] List tools take paging inputs with `Range` constraints → [doExecute and ExecutableResult](doexecute-and-executableresult.md)
- [ ] Agents get a scoped tool list, since every connector tool adds a schema → [Calling a Tool from the AI Module](calling-a-tool-from-the-ai-module.md)
- [ ] Site-derived enums over 50 entries are expected to disappear from the schema → [Input Definitions](input-definitions.md)
- [ ] `getFormattedResult()` is called freely after `execute()`; it is memoized → [Calling a Tool from PHP](calling-a-tool-from-php.md)

## Common Mistakes

- Returning full entity field dumps to an agent → token cost and data exposure; return the fields the task needs

## See Also

- [checkRequirements](checkrequirements.md)
- Reference: `modules/contrib/tool/src/Drush/RequirementStatus.php`, `modules/contrib/tool/src/Tool/ToolManager.php`
