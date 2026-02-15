---
description: Custom Field plugin architecture with three plugin managers, key services, hook classes, and extensibility patterns.
---

# Architecture & Plugin System

## When to Use

You need to understand how Custom Field's plugin system works to extend it with custom field types, widgets, or formatters, or to debug plugin discovery issues.

## Pattern

**Three custom plugin managers** (defined in `custom_field.services.yml`):

```yaml
plugin.manager.custom_field_type:
  class: Drupal\custom_field\Plugin\CustomFieldTypeManager
  # Discovers #[CustomFieldType] plugins in /Plugin/CustomField/FieldType/

plugin.manager.custom_field_widget:
  class: Drupal\custom_field\Plugin\CustomFieldWidgetManager
  # Discovers #[CustomFieldWidget] plugins in /Plugin/CustomField/FieldWidget/

plugin.manager.custom_field_formatter:
  class: Drupal\custom_field\Plugin\CustomFieldFormatterManager
  # Discovers #[CustomFieldFormatter] plugins in /Plugin/CustomField/FieldFormatter/
```

**Main field type**: `CustomItem` (plugin ID `custom`) -- single field type with dynamic columns defined via settings. Uses `CustomItemList` as list class.

**Column separator constant**: `CustomItem::SEPARATOR = '__'` -- used for extended properties like `image__alt`, `link__title`.

**Key services**:

- `plugin.manager.custom_field_type` -- FieldType plugin manager
- `plugin.manager.custom_field_widget` -- Widget plugin manager
- `plugin.manager.custom_field_formatter` -- Formatter plugin manager
- `custom_field.update_manager` -- Handles schema updates for existing fields
- `custom_field.generate_data` -- Generates sample data

**Hook classes** (Drupal 11 style):

- `GeneralHooks` -- General hooks
- `FormHooks` -- Form alterations
- `ThemeHooks` -- Theme preprocessing
- `TokenHooks` -- Token definitions
- `ViewsHooks` -- Views integration

## Common Mistakes

- **Calling plugin managers statically** -- Inject via dependency injection, don't use `\Drupal::service()` in classes
- **Assuming core field plugin discovery** -- Custom Field has its own plugin namespaces under `/Plugin/CustomField/`, not `/Plugin/Field/`
- **Not clearing cache after adding plugins** -- Plugin definitions are cached; run `drush cr` after creating new plugins

## See Also

- Reference: `/modules/contrib/custom_field/src/Plugin/CustomFieldTypeManager.php`
- Reference: `/modules/contrib/custom_field/custom_field.services.yml`
