---
description: "Source code locations for all Custom Field 5.x components -- field types, widgets, formatters, services, hooks, Views plugins, templates, and sub-modules."
tldr: "Reference map of every Custom Field 5.x source path -- field types, widgets, formatters, plugin managers, hook classes, Views plugins, templates, and the nine sub-module directories -- for locating implementation details fast."
drupal_version: "11.x"
---

# Code Reference Map

## When to Use

You need to find specific source code for custom field functionality.

## Core Field Type

- `/modules/contrib/custom_field/src/Plugin/Field/FieldType/CustomItem.php` -- Main field type plugin
- `/modules/contrib/custom_field/src/Plugin/Field/FieldType/CustomItemList.php` -- Field list class

## Plugin Managers

- `/modules/contrib/custom_field/src/Plugin/CustomFieldTypeManager.php` -- FieldType plugin manager
- `/modules/contrib/custom_field/src/Plugin/CustomFieldWidgetManager.php` -- Widget plugin manager
- `/modules/contrib/custom_field/src/Plugin/CustomFieldFormatterManager.php` -- Formatter plugin manager (uses core's `FieldFormatter` attribute class)
- Plus the Feeds, link-attributes and (5.x) prop-widget managers -- see `custom_field.services.yml`

## Attributes

- `/modules/contrib/custom_field/src/Attribute/` -- `CustomFieldType`, `CustomFieldWidget`, `CustomFieldFeedsType`, `PropWidget`. There is no `CustomFieldFormatter` attribute

> **The three `*Base` classes named after the module are not in the plugin directories.** `CustomFieldTypeBase.php`, `CustomFieldWidgetBase.php` and `CustomFieldFormatterBase.php` all sit one level up, in `src/Plugin/` -- alongside their `*Interface` and `*Manager` counterparts. Only the type-specific bases live beside the plugins.

## Field Types (27 files, 22 plugin classes)

- Directory: `/modules/contrib/custom_field/src/Plugin/CustomField/FieldType/`
- Non-plugin files in that directory: `NumericTypeBase.php`, `OptionsTrait.php`, `DurationOptionsTrait.php`, `DateTimeTypeInterface.php`, `LinkTypeInterface.php`
- `CustomFieldTypeBase.php` / `CustomFieldTypeInterface.php` -- `src/Plugin/`

## Widgets (39 files, 32 plugin classes as of 5.0.2 -- 38/31 in 5.0.1, before `SelectOrOtherWidget`)

- Directory: `/modules/contrib/custom_field/src/Plugin/CustomField/FieldWidget/`
- Base classes in that directory (7): `NumberWidgetBase.php`, `EntityReferenceWidgetBase.php`, `EntityReferenceOptionsWidgetBase.php`, `ListWidgetBase.php`, `DateTimeWidgetBase.php`, `DateRangeWidgetBase.php`, `UrlWidgetBase.php` (`MapWidgetBase.php` existed in 4.x and is removed in 5.x)
- `CustomFieldWidgetBase.php` / `CustomFieldWidgetInterface.php` -- `src/Plugin/`

## Formatters (36 files, 33 plugin classes)

- Directory: `/modules/contrib/custom_field/src/Plugin/CustomField/FieldFormatter/`
- Base classes in that directory (3): `NumericFormatterBase.php`, `DateTimeFormatterBase.php`, `EntityReferenceFormatterBase.php`
- `CustomFieldFormatterBase.php` / `CustomFieldFormatterInterface.php` -- `src/Plugin/`
- New in 5.x: `LinkTextFormatter`, `MapInlineFormatter`, `MapListFormatter`

## SDC Prop Widgets (5.x) -- three different directories, which is easy to get wrong

- `/modules/contrib/custom_field/src/Plugin/Components/PropWidget/` -- the 14 `#[PropWidget]` plugin classes (`PropWidgetString`, `PropWidgetImage`, `PropWidgetArrayObject`, ...) plus `PropWidgetArrayBase.php`
- `/modules/contrib/custom_field/src/Plugin/PropWidgetBase.php` and `PropWidgetInterface.php` -- the base class and interface, one level up
- `/modules/contrib/custom_field/src/PluginManager/PropWidgetManager.php` (+ `PropWidgetManagerInterface.php`) -- the only classes in `src/PluginManager/`. The manager's discovery subdirectory string is `'Plugin/Components/PropWidget'`.

## Field-Level Widgets

- `/modules/contrib/custom_field/src/Plugin/Field/FieldWidget/CustomStackedWidget.php`
- `/modules/contrib/custom_field/src/Plugin/Field/FieldWidget/CustomFlexWidget.php`

## Field-Level Formatters

- `/modules/contrib/custom_field/src/Plugin/Field/FieldFormatter/CustomFormatter.php`
- `/modules/contrib/custom_field/src/Plugin/Field/FieldFormatter/CustomInlineFormatter.php`
- `/modules/contrib/custom_field/src/Plugin/Field/FieldFormatter/CustomListFormatter.php`
- `/modules/contrib/custom_field/src/Plugin/Field/FieldFormatter/CustomTableFormatter.php`
- `/modules/contrib/custom_field/src/Plugin/Field/FieldFormatter/FlippedTableFormatter.php`
- `/modules/contrib/custom_field/src/Plugin/Field/FieldFormatter/CustomTemplateFormatter.php`
- `/modules/contrib/custom_field/src/Plugin/Field/FieldFormatter/SingleDirectoryComponentFormatter.php` -- plugin ID `custom_field_sdc`, but it is in the **main module**, not the sub-module of the same name
- `/modules/contrib/custom_field/src/Plugin/Field/FieldFormatter/BaseFormatter.php` + `BaseFormatterInterface.php` -- shared base for all seven

## Services

- `/modules/contrib/custom_field/custom_field.services.yml` -- Service definitions
- `/modules/contrib/custom_field/src/Service/UpdateManager.php` -- Schema update service (id `custom_field.update_manager`, interface `UpdateManagerInterface`)
- `/modules/contrib/custom_field/src/Service/GenerateData.php` -- Sample data generation (interface `GenerateDataInterface`)

## Hook Classes (5.x has no `.module` files at all)

- `/modules/contrib/custom_field/src/Hook/GeneralHooks.php`
- `/modules/contrib/custom_field/src/Hook/FormHooks.php`
- `/modules/contrib/custom_field/src/Hook/ThemeHooks.php`
- `/modules/contrib/custom_field/src/Hook/TokenHooks.php`
- `/modules/contrib/custom_field/src/Hook/ViewsHooks.php`
- `/modules/contrib/custom_field/src/Hook/EntityHooks.php` -- taxonomy index maintenance, `entity_view_display_presave`

## Post-Update

- `/modules/contrib/custom_field/custom_field.post_update.php` -- `custom_field_post_update_bulk_populate_taxonomy_index()`, the one 5.x upgrade step

## Form Element

- `/modules/contrib/custom_field/src/Element/MultiValue.php` -- `#[FormElement('custom_field_multivalue')]` (5.x)
- `/modules/contrib/custom_field/src/Element/SelectOrOtherBase.php`, `SelectOrOtherSelect.php`, `SelectOrOtherRadios.php` -- backing elements for the `select_or_other` widget (5.0.2)

## Entity Usage Tracking

- `/modules/contrib/custom_field/src/Plugin/EntityUsage/Track/CustomField.php`
- `/modules/contrib/custom_field/src/Plugin/EntityUsage/Track/CustomFieldLink.php` (5.x)
- `/modules/contrib/custom_field/src/Plugin/EntityUsage/Track/CustomFieldText.php` (5.x)

## Views Plugins

- `/modules/contrib/custom_field/src/Plugin/views/field/CustomField.php` -- Field plugin
- `/modules/contrib/custom_field/src/Plugin/views/filter/CustomFieldDate.php` -- Date filter
- `/modules/contrib/custom_field/src/Plugin/views/filter/CustomFieldEntityReference.php` -- Entity ref filter
- `/modules/contrib/custom_field/src/Plugin/views/sort/CustomFieldDate.php` -- Date sort
- `/modules/contrib/custom_field/src/Plugin/views/argument/` -- 6 date argument plugins plus their `CustomFieldDate` base class

## Validation Constraints

- `/modules/contrib/custom_field/src/Plugin/Validation/Constraint/LinkAccessConstraint.php`
- `/modules/contrib/custom_field/src/Plugin/Validation/Constraint/LinkExternalProtocolsConstraint.php`
- `/modules/contrib/custom_field/src/Plugin/Validation/Constraint/LinkNotExistingInternalConstraint.php`
- `/modules/contrib/custom_field/src/Plugin/Validation/Constraint/LinkTypeConstraint.php`
- `/modules/contrib/custom_field/src/Plugin/Validation/Constraint/TimeConstraint.php`

## Templates

- `/modules/contrib/custom_field/templates/custom-field.html.twig`
- `/modules/contrib/custom_field/templates/custom-field-item.html.twig`
- `/modules/contrib/custom_field/templates/custom-field-daterange.html.twig`
- `/modules/contrib/custom_field/templates/custom-field-time-range.html.twig`
- `/modules/contrib/custom_field/templates/custom-field-flex-wrapper.html.twig`
- `/modules/contrib/custom_field/templates/custom-field-hierarchical-formatter.html.twig`

## Feeds Integration

- `/modules/contrib/custom_field/src/Plugin/CustomField/FeedsType/` -- 23 target plugins (24 files, one being the abstract `BaseTarget`)
- `/modules/contrib/custom_field/src/Feeds/Target/CustomField.php` -- the single Feeds target that dispatches to them

## Config Schema

- `/modules/contrib/custom_field/config/schema/custom_field.schema.yml` -- 1088 lines in 5.0.2 (1071 in 5.0.1)

## Upstream Documentation

- `/modules/contrib/custom_field/docs/` + `mkdocs.yml` -- 143-file mkdocs (Material) site shipped in the release tarball, one page per plugin. Canonical upstream reference since 5.0.0

## Sub-Module Directories

- `/modules/contrib/custom_field/modules/custom_field_ai/`
- `/modules/contrib/custom_field/modules/custom_field_entity_browser/`
- `/modules/contrib/custom_field/modules/custom_field_graphql/`
- `/modules/contrib/custom_field/modules/custom_field_jsonapi/`
- `/modules/contrib/custom_field/modules/custom_field_linkit/`
- `/modules/contrib/custom_field/modules/custom_field_media/`
- `/modules/contrib/custom_field/modules/custom_field_sdc/`
- `/modules/contrib/custom_field/modules/custom_field_search_api/`
- `/modules/contrib/custom_field/modules/custom_field_viewfield/`

## See Also

- Drupal install: `/home/camoa/workspace/contrib/web/`
- Module path: `/home/camoa/workspace/contrib/web/modules/contrib/custom_field/`
