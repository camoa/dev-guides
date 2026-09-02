---
description: "BEF configuration schema — YAML structure in Views export, dynamic schema resolution, and config updater migrations"
tldr: "Use this guide when exporting/importing BEF configuration, creating custom widgets that need config schema, or debugging config validation errors."
drupal_version: "11.x"
---

# Configuration Schema

## When to Use

> When exporting/importing BEF configuration, creating custom widgets that need config schema, or debugging config validation errors.

## Decision: Schema Files

| File | Defines |
|---|---|
| `config/schema/better_exposed_filters.exposed_form.schema.yml` | Top-level BEF config on Views exposed form |
| `config/schema/better_exposed_filters.filter.schema.yml` | Per-filter widget config schema |
| `config/schema/better_exposed_filters.sort.schema.yml` | Sort widget config schema |
| `config/schema/better_exposed_filters.pager.schema.yml` | Pager widget config schema |

## Pattern: Config Structure in Views Export

BEF configuration lives inside the View's display options under `exposed_form.options.bef`:

```yaml
display:
  page_1:
    display_options:
      exposed_form:
        type: bef
        options:
          bef:
            general:
              autosubmit: true
              autosubmit_hide: true
              allow_secondary: false
              # ...
            sort:
              plugin_id: bef
              # sort widget config...
            pager:
              plugin_id: default
            filter:
              field_category_target_id:
                plugin_id: bef
                select_all_none: true
                display_inline: false
                soft_limit: 10
                advanced:
                  collapsible: false
                  is_secondary: false
                  # ...
```

## Pattern: Dynamic Schema Resolution

BEF uses typed data schema with dynamic type resolution:
- `better_exposed_filters.filter.[plugin_id]` — resolves to the specific filter widget's schema
- `better_exposed_filters.sort.[plugin_id]` — resolves to the specific sort widget's schema
- `better_exposed_filters.pager.[plugin_id]` — resolves to the specific pager widget's schema

## Pattern: Config Updater

`BetterExposedFiltersConfigUpdater` handles config migrations when new keys are added:

| Method | Migration |
|---|---|
| `updateCombineParam()` | Adds `combine_param` key (default: 'sort_bef_combine') |
| `updateSoftLimitParams()` | Adds `soft_limit`, `soft_limit_label_less`, `soft_limit_label_more` |
| `updateSingleCheckboxFilters()` | Adds `treat_as_false` (default: FALSE) |
| `updateAddOpenByDefaultKey()` | Adds `open_by_default` (default: FALSE) |
| `updateAddFieldClassesKey()` | Adds `field_classes` (default: '') |

## Common Mistakes

- **Config import fails** — If you add a custom widget, you must add a matching config schema entry or config validation will fail on import.
- **Missing keys after update** — Run `drush updb` to execute post_update hooks that add new config keys.
- **Schema mismatch** — When copying config between sites with different BEF versions, check for missing keys. The config updater only runs during `drush updb`, not on import.

## See Also

- [Custom Widget Plugins](custom-widget-plugins.md) — schema for custom widgets
- [Installation & Setup](installation-setup.md) — initial configuration
- Reference: `web/modules/contrib/better_exposed_filters/config/schema/`
- Reference: `web/modules/contrib/better_exposed_filters/src/BetterExposedFiltersConfigUpdater.php`
