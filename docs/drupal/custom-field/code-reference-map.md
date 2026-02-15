---
description: Source code locations for all Custom Field components -- field types, widgets, formatters, services, hooks, Views plugins, templates, and sub-modules.
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
- `/modules/contrib/custom_field/src/Plugin/CustomFieldFormatterManager.php` -- Formatter plugin manager

## Field Types (26 files)

- Directory: `/modules/contrib/custom_field/src/Plugin/CustomField/FieldType/`
- Base classes: `CustomFieldTypeBase.php`, `NumericTypeBase.php`, `DateTimeWidgetBase.php`

## Widgets (39 files)

- Directory: `/modules/contrib/custom_field/src/Plugin/CustomField/FieldWidget/`
- Base classes: `CustomFieldWidgetBase.php`, `NumberWidgetBase.php`, `EntityReferenceWidgetBase.php`, `ListWidgetBase.php`

## Formatters (33 files)

- Directory: `/modules/contrib/custom_field/src/Plugin/CustomField/FieldFormatter/`
- Base classes: `CustomFieldFormatterBase.php`, `NumericFormatterBase.php`, `DateTimeFormatterBase.php`

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

## Services

- `/modules/contrib/custom_field/custom_field.services.yml` -- Service definitions
- `/modules/contrib/custom_field/src/CustomFieldUpdateManager.php` -- Schema update service
- `/modules/contrib/custom_field/src/CustomFieldGenerateData.php` -- Sample data generation

## Hook Classes

- `/modules/contrib/custom_field/src/Hook/GeneralHooks.php`
- `/modules/contrib/custom_field/src/Hook/FormHooks.php`
- `/modules/contrib/custom_field/src/Hook/ThemeHooks.php`
- `/modules/contrib/custom_field/src/Hook/TokenHooks.php`
- `/modules/contrib/custom_field/src/Hook/ViewsHooks.php`

## Views Plugins

- `/modules/contrib/custom_field/src/Plugin/views/field/CustomField.php` -- Field plugin
- `/modules/contrib/custom_field/src/Plugin/views/filter/CustomFieldDate.php` -- Date filter
- `/modules/contrib/custom_field/src/Plugin/views/filter/CustomFieldEntityReference.php` -- Entity ref filter
- `/modules/contrib/custom_field/src/Plugin/views/sort/CustomFieldDate.php` -- Date sort
- `/modules/contrib/custom_field/src/Plugin/views/argument/` -- 7 date argument plugins

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

- `/modules/contrib/custom_field/src/Feeds/Target/` -- 28 target handler files

## Config Schema

- `/modules/contrib/custom_field/config/schema/custom_field.schema.yml` -- 877 lines

## Sub-Module Directories

- `/modules/contrib/custom_field/modules/custom_field_ai/`
- `/modules/contrib/custom_field/modules/custom_field_entity_browser/`
- `/modules/contrib/custom_field/modules/custom_field_graphql/`
- `/modules/contrib/custom_field/modules/custom_field_jsonapi/`
- `/modules/contrib/custom_field/modules/custom_field_linkit/`
- `/modules/contrib/custom_field/modules/custom_field_media/`
- `/modules/contrib/custom_field/modules/custom_field_search_api/`
- `/modules/contrib/custom_field/modules/custom_field_viewfield/`
