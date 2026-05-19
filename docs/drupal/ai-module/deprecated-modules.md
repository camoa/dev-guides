---
description: Deprecated AI sub-modules — migration paths for ai_eca, ai_external_moderation, ai_logging, ai_translate, and ai_validations
tldr: "Use this guide when planning migrations away from deprecated sub-modules. All deprecations from 1.3.0-rc2 remain in 1.3.5 and 1.4.0-rc1 — none have been removed yet. Removal is planned for AI 2.0.0."
drupal_version: "11.x"
---

# Deprecated Modules

## When to Use

> Use this guide when planning migrations away from deprecated sub-modules. All deprecations that existed in 1.3.0-rc2 remain in 1.3.5 and 1.4.0-rc1 — none have been un-deprecated or removed yet. Removal planned for AI 2.0.0.

## Deprecation Status

| Module | Status | Replacement |
|--------|--------|-------------|
| `ai_eca` | Migration shim (removal planned in 2.0.0) | `drupal/ai_integration_eca` (separate project) |
| `ai_external_moderation` | Migration shim | Guardrails in AI Core (`ai.external_moderation` config) |
| `ai_logging` | Deprecated | `ai_observability` |
| `ai_translate` | Deprecated | TBD (no replacement announced; issue #3570275) |
| `ai_validations` | Deprecated | `drupal/ai_validations` (separate project; issue #3552888) |
| `ai_content_suggestions` | Deprecated | TBD (issue #3552885) |

## Migration: ai_eca

```bash
composer require drupal/ai_integration_eca
drush updb
# Runs ai_eca_update_11001 — migrates config, installs replacement, uninstalls self.
```

## Migration: ai_external_moderation

```bash
drush updb
# Runs ai_external_moderation_update_10001 — copies config to ai.external_moderation, uninstalls self.
```

## Migration: ai_logging → ai_observability

1. Enable `ai_observability`
2. Configure at `/admin/config/ai/observability`
3. Disable `ai_logging`

## Migration: ai_validations

1. `composer require drupal/ai_validations` (when released as stable)
2. Run database updates
3. Remove `ai_validations` from the monorepo

## Common Mistakes

- **Wrong**: Installing `ai_eca` from AI 1.3.0+ and expecting it to work → **Right**: It is a migration shim only; install `drupal/ai_integration_eca` instead
- **Wrong**: Using `ai_logging` for production monitoring → **Right**: Deprecated; use `ai_observability`
- **Wrong**: Waiting for `ai_translate` replacement before planning → **Right**: No replacement announced; plan a custom solution

## See Also

- [AI Observability](ai-observability.md)
- [Guardrails System](guardrails-system.md)
- Reference: https://www.drupal.org/project/ai
- Reference: https://www.drupal.org/node/3570275
