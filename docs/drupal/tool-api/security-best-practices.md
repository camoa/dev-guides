---
description: "Security checklist for exposing Tool API tools to non-human callers"
tldr: "Before exposing tools to AI, MCP or scripts, check access rules, failure messages, undeclared outputs, entity validation, honest operation labels and who holds administer tool. Gotcha: operation Read is not enforced."
drupal_version: "^10.5 || ^11"
---

# Security Checklist

## When to Use

> Run through this before exposing Tool API tools to any non-human caller. Each item links to the page that owns the rule.
>
> **Version:** applies to `drupal/tool` 1.0.0-beta11 (beta; no security advisory coverage), `tool_belt` 1.0.0-alpha6, `mcp_server_tool_bridge` 1.0.0-beta3.

## Checklist

- [ ] Every tool declares a `permission` for account-level rules and uses `checkAccess()` for object-level rules (OWASP API1, broken object level authorization) → [Access Control](access-control.md)
- [ ] `checkAccess()` passes the given `$account` to every entity and field access call → [Access Control](access-control.md)
- [ ] Invokers you write call `checkPermission()` before setting inputs, and `validateInputs()` before `access()` → [Calling a Tool from PHP](calling-a-tool-from-php.md)
- [ ] MCP-exposed tools keep refiners and input transforms free of side effects, because the bridge sets inputs before any denial → [Calling a Tool over MCP](calling-a-tool-over-mcp.md)
- [ ] Failure messages and failure `context_values` carry no internals → [doExecute and ExecutableResult](doexecute-and-executableresult.md)
- [ ] No undeclared result keys carry entities or secrets → [Output Definitions](output-definitions.md)
- [ ] Write tools validate the entity before saving; `tool_belt:entity_save` does not → [Tool Belt Catalog](tool-belt-catalog.md)
- [ ] `operation` and `destructive` are honest, and agent tool lists exclude destructive tools → [Operation and Destructive](operation-and-destructive.md), [Calling a Tool from the AI Module](calling-a-tool-from-the-ai-module.md)
- [ ] Prerequisites that must block are re-checked in `doExecute()` → [checkRequirements](checkrequirements.md)
- [ ] Access rules are tested with a role-scoped `--uid`, not uid 1 → [Calling a Tool from Drush](calling-a-tool-from-drush.md)
- [ ] `administer tool` stays on trusted roles → [Installation and Submodules](installation-and-submodules.md)

## Common Mistakes

- Trusting `operation: Read` to mean safe → nothing enforces it; review the code

## See Also

- [Access Control](access-control.md)
- OWASP API Security Top 10: https://owasp.org/API-Security/
