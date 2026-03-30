---
description: BEF configuration schema — YAML structure in Views export, dynamic schema resolution, and config updater migrations
drupal_version: "11.x"
---

# Configuration Schema

## When to Use

> Use this guide when exporting/importing BEF configuration, creating custom widgets that need config schema, or debugging config validation errors.

## Decision

| Schema File | Defines |
|---|---|
| `better_exposed_filters.exposed_form.schema.yml` | Top-level BEF config on Views exposed form |
| `better_exposed_filters.filter.schema.yml` | Per-filter widget config schema |
| `better_exposed_filters.sort.schema.yml` | Sort widget config schema |
| `better_exposed_filters.pager.schema.yml` | Pager widget config schema |

**Dynamic schema resolution:**
- `better_exposed_filters.filter.[plugin_id]` — resolves to the specific filter widget's schema
- `better_exposed_filters.sort.[plugin_id]` — resolves to the specific sort widget's schema
- `better_exposed_filters.pager.[plugin_id]` — resolves to the specific pager widget's schema

## Pattern

```yaml
# BEF config location in Views YAML export:
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
            sort:
              plugin_id: bef
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
```

**Config updater migrations (`BetterExposedFiltersConfigUpdater`):**

| Method | Migration |
|---|---|
| `updateCombineParam()` | Adds `combine_param` key |
| `updateSoftLimitParams()` | Adds `soft_limit`, `soft_limit_label_less`, `soft_limit_label_more` |
| `updateSingleCheckboxFilters()` | Adds `treat_as_false` |
| `updateAddOpenByDefaultKey()` | Adds `open_by_default` |

Run `drush updb` to execute post_update hooks that apply these migrations.

## Common Mistakes

- **Wrong**: Adding a custom widget without a config schema entry → **Right**: Config import will fail with validation errors. Add a schema entry in `config/schema/` for your custom widget.
- **Wrong**: Copying config between sites with different BEF versions without checking for missing keys → **Right**: Check for missing keys. The config updater only runs during `drush updb`, not on import.

## See Also

- [Custom Widget Plugins](custom-widget-plugins.md)
- [Installation & Setup](installation-setup.md)
- Reference: `web/modules/contrib/better_exposed_filters/config/schema/`
- Reference: `web/modules/contrib/better_exposed_filters/src/BetterExposedFiltersConfigUpdater.php`
