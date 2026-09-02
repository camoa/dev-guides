---
description: Deprecated AI sub-modules — migration paths for ai_eca, ai_external_moderation, ai_logging, ai_translate, ai_validations, and ai_content_suggestions
tldr: "Use this guide when planning migrations away from deprecated sub-modules. As of AI Core 1.4.7 all deprecations remain in place — removal is planned for AI 2.0.0, which is not yet released."
drupal_version: "11.x"
---

# Deprecated Modules

## When to Use

> Use this guide when planning migrations away from deprecated sub-modules.

These modules carry a `lifecycle: deprecated` designation in AI Core. As of AI Core **1.4.7** (current stable, verified 2026-08-20) every deprecation is still in place — none have been removed yet. Removal is planned for **AI 2.0.0, which is not yet released** (currently dev-only on the `2.0.x-dev` branch). The replacements have moved to standalone projects at very different maturity levels, so verify each before migrating.

## Deprecation Status

| Module | Status | Replacement (verified Jun 2026) |
|--------|--------|-------------|
| `ai_eca` | Migration shim (removal planned in 2.0.0) | standalone `drupal/ai_integration_eca` — **1.0.0-rc3** (RC; not yet security-covered) |
| `ai_external_moderation` | Migration shim | Guardrails **in AI Core** since 1.3.0 (`ai.external_moderation` config). Experimental extension `drupal/ai_guardrails` exists (dev-only, needs core patches) — not the core replacement |
| `ai_logging` | Deprecated | in-core `ai_observability` (recommended). A legacy standalone `drupal/ai_logging` (2.0.0-alpha1) exists but is **maintenance-only** — not for new sites |
| `ai_translate` | Split to standalone | standalone `drupal/ai_translate` — **1.3.1 stable** (security-covered). See [AI Translate](ai-translate.md) |
| `ai_validations` | Deprecated | standalone `drupal/ai_validations` — **1.0.0-alpha1** only (pre-stable; wait for a stable tag); issue #3552888 |
| `ai_content_suggestions` | Deprecated | standalone `drupal/ai_content_suggestions` — **1.4.0 stable** (security-covered), but the project targets the **AI Core 2.0.x** branch; verify the `drupal/ai` constraint for your AI Core version. Issue #3552885 |

## Migration: ai_eca

```bash
composer require drupal/ai_integration_eca   # 1.0.0-rc3 — RC, not security-covered yet
drush updb  # runs ai_eca_update_11001 — migrates config, installs replacement, uninstalls self
```

## Migration: ai_external_moderation

```bash
drush updb  # runs ai_external_moderation_update_10001 — copies config to ai.external_moderation, uninstalls self
```

Guardrails are part of AI Core (since 1.3.0); no separate install is needed. `drupal/ai_guardrails` is an experimental extension, not the replacement.

## Migration: ai_logging → ai_observability

1. Enable the in-core `ai_observability` submodule
2. Configure at `/admin/config/ai/observability`
3. Disable `ai_logging`

Do not install the standalone `drupal/ai_logging` for new sites — it is maintenance-only for sites that used the original in-core module.

## Migration: ai_translate

Already a published standalone. See the [AI Translate](ai-translate.md) section for the full path:

```bash
composer require 'drupal/ai_translate:^1.3'
drush updb  # post_update converts prompts to config entities and migrates language settings
```

## Migration: ai_validations

The standalone is **alpha** (1.0.0-alpha1). Keep using the in-core submodule until a stable tag lands, then:

```bash
composer require drupal/ai_validations   # wait for a stable release
drush updb
# remove ai_validations from the AI Core monorepo install
```

## Migration: ai_content_suggestions

A stable standalone (`drupal/ai_content_suggestions` 1.4.0) exists, but its project page states it is designed for the **AI Core 2.0.x** branch — which is still dev-only. Before adopting it on AI Core 1.4.x, confirm the release's `drupal/ai` constraint (`composer show drupal/ai_content_suggestions 1.4.0`) actually permits your AI Core version.

```bash
composer show drupal/ai_content_suggestions 1.4.0  # check drupal/ai version constraint
```

## Common Mistakes

- **Wrong**: Installing `ai_eca` from AI 1.3.0+ and expecting it to work → **Right**: It is a migration shim only; install `drupal/ai_integration_eca` instead
- **Wrong**: Using `ai_logging` for production monitoring → **Right**: Deprecated; use the in-core `ai_observability` submodule
- **Wrong**: Waiting to plan `ai_translate` migration → **Right**: The standalone is released; `composer require 'drupal/ai_translate:^1.3'`
- **Wrong**: Installing `drupal/ai_content_suggestions` 1.4.0 on AI Core 1.4.x without checking → **Right**: The project targets AI Core 2.0.x; run `composer show drupal/ai_content_suggestions 1.4.0` to verify the `drupal/ai` constraint first

## See Also

- [AI Observability](ai-observability.md)
- [Guardrails System](guardrails-system.md)
- Reference: https://www.drupal.org/project/ai
- Reference: https://www.drupal.org/node/3570275
