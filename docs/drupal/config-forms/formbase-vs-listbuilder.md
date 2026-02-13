---
description: Choose between FormBase and ListBuilder for admin interfaces
drupal_version: "11.x"
---

# FormBase vs ListBuilder

## When to Use

> Use FormBase/ConfigFormBase when building settings pages or custom admin forms. Use ListBuilder when displaying entity collections with standard CRUD operations.

## Decision

| Situation | Choose | Why |
|-----------|--------|-----|
| Module settings page | ConfigFormBase | Settings are simple configuration, not entities |
| Template/handler management | FormBase | Complex forms with bulk operations, not individual entities |
| Entity collection list (nodes, users, config entities) | ListBuilder | Automatic CRUD operations, admin theme integration |
| Bulk operations on multiple items | FormBase | Full control over form structure and submission |
| Standard entity CRUD only | ListBuilder | Minimal code, automatic features, future-proof |
| Custom workflow that doesn't fit entity pattern | FormBase | Maximum flexibility |
| Mixed content types in one interface | FormBase | Entity lists expect homogeneous data |

## Pattern

**FormBase/ConfigFormBase**: Manual control, use for configuration/settings.
**ListBuilder**: Automatic entity collection, use for standard CRUD.

## Common Mistakes

- **Wrong**: Using FormBase for simple entity lists → **Right**: Use ListBuilder for automatic features
- **Wrong**: Using ListBuilder for configuration settings → **Right**: Use ConfigFormBase, not entities
- **Wrong**: Creating custom routing when entity links exist → **Right**: Let entity annotations handle routing
- **Wrong**: Overriding entire render() in ListBuilder → **Right**: Override buildRow/buildHeader instead
- **Wrong**: Mixing configuration data with entity management → **Right**: Separate concerns, different base classes

## See Also

- [ConfigFormBase Pattern](configformbase-pattern.md)
- [FormBase Pattern](formbase-pattern.md)
- [ListBuilder Pattern](listbuilder-pattern.md)
- Reference: [Drupal Form API Introduction](https://www.drupal.org/docs/drupal-apis/form-api/introduction-to-form-api)
- Reference: core/lib/Drupal/Core/Form/FormBase.php
- Reference: core/lib/Drupal/Core/Config/Entity/ConfigEntityListBuilder.php
