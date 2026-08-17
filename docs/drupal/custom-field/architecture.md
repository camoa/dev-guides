---
description: "Custom Field 5.0.2 plugin architecture with six plugin managers, key services, hook classes, and extensibility patterns."
tldr: "Custom Field discovers types/widgets/formatters/feeds/link-attributes/prop-widget plugins through six services under custom_field.services.yml; formatter plugins use core's #[FieldFormatter] attribute, not a custom_field one."
drupal_version: "11.x"
---

# Architecture & Plugin System

## When to Use

You need to understand how Custom Field's plugin system works to extend it with custom field types, widgets, or formatters, or to debug plugin discovery issues.

## Pattern

**Six plugin-discovery managers** (defined in `custom_field.services.yml`):

```yaml
plugin.manager.custom_field_type:
  class: Drupal\custom_field\Plugin\CustomFieldTypeManager
  # Discovers #[CustomFieldType] plugins in /Plugin/CustomField/FieldType/

plugin.manager.custom_field_widget:
  class: Drupal\custom_field\Plugin\CustomFieldWidgetManager
  # Discovers #[CustomFieldWidget] plugins in /Plugin/CustomField/FieldWidget/

plugin.manager.custom_field_formatter:
  class: Drupal\custom_field\Plugin\CustomFieldFormatterManager
  # Discovers plugins in /Plugin/CustomField/FieldFormatter/ -- note the attribute is
  # CORE's Drupal\Core\Field\Attribute\FieldFormatter, not a custom_field one

plugin.manager.custom_field_feeds:
  # Discovers #[CustomFieldFeedsType] plugins in /Plugin/CustomField/FeedsType/

plugin.manager.custom_field_link_attributes:
  # Discovers link-attribute plugins used by link columns

plugin.manager.custom_field_component_prop_widget:
  # NEW in 5.x -- discovers #[PropWidget] plugins in /Plugin/Components/,
  # which map sub-fields onto SDC component props
```

Plus `custom_field.tag_manager`. Only the prop-widget manager is new in 5.x; the feeds, link-attributes and tag managers already existed in 4.x and were simply undocumented.

**Main field type**: `CustomItem` (plugin ID `custom`) -- single field type with dynamic columns defined via settings. Uses `CustomItemList` as list class.

**Column separator constant**: `CustomItem::SEPARATOR = '__'` -- used for extended properties like `image__alt`, `link__title`.

**Key services**:

- `plugin.manager.custom_field_type` -- FieldType plugin manager
- `plugin.manager.custom_field_widget` -- Widget plugin manager
- `plugin.manager.custom_field_formatter` -- Formatter plugin manager
- `plugin.manager.custom_field_feeds` -- Feeds target plugin manager
- `plugin.manager.custom_field_link_attributes` -- Link attribute plugin manager
- `plugin.manager.custom_field_component_prop_widget` -- SDC prop widget plugin manager (5.x)
- `custom_field.update_manager` -- Handles schema updates for existing fields
- `custom_field.generate_data` -- Generates sample data
- `custom_field.tag_manager` -- Tag handling

In 5.x both services also autowire by interface: type-hint `\Drupal\custom_field\Service\UpdateManagerInterface` or `\Drupal\custom_field\Service\GenerateDataInterface` in a constructor and the container resolves it.

**Hook classes** (OO `#[Hook]` only -- 5.x deleted every `.module` file and the procedural `#[LegacyHook]` shims with them):

- `GeneralHooks` -- General hooks
- `FormHooks` -- Form alterations
- `ThemeHooks` -- Theme preprocessing
- `TokenHooks` -- Token definitions
- `ViewsHooks` -- Views integration
- `EntityHooks` -- Node insert/update maintenance of the taxonomy index, plus `entity_view_display_presave`. In 5.x the node hooks declare `#[Hook('node_update', order: Order::Last)]`, replacing the `hook_module_implements_alter()` reordering 4.x used

**Other integrations shipped in the main module** (not sub-modules):

- Entity Usage tracking -- `src/Plugin/EntityUsage/Track/`: `CustomField` (pre-existing), plus `CustomFieldLink` and `CustomFieldText` new in 5.x
- `custom_field_multivalue` form element -- `src/Element/MultiValue.php`, `#[FormElement('custom_field_multivalue')]`, new in 5.x

## Common Mistakes

- **Calling plugin managers statically** -- Inject via dependency injection, don't use `\Drupal::service()` in classes
- **Assuming core field plugin discovery** -- Custom Field has its own plugin namespaces under `/Plugin/CustomField/`, not `/Plugin/Field/`
- **Not clearing cache after adding plugins** -- Plugin definitions are cached; run `drush cr` after creating new plugins

## See Also

- Reference: `/modules/contrib/custom_field/src/Plugin/CustomFieldTypeManager.php`
- Reference: `/modules/contrib/custom_field/custom_field.services.yml`
- [Custom Field Overview](overview.md)
