---
description: Token replacement for custom field values in Pathauto, Rules, and email templates with correct separator syntax.
---

# Token Support

## When to Use

You need to use custom field values in token replacement contexts (Pathauto, Rules, email templates).

## Pattern

**Token format**: `[entity:field_name:column_name]`

**Available tokens**:

```
[node:field_address:street]
[node:field_address:city]
[node:field_address:state]
[node:field_address:zip]

// Extended properties use double-underscore
[node:field_custom:photo__alt]
[node:field_custom:event_date__timezone]
[node:field_custom:link__title]
```

**In Pathauto patterns**:

```
/products/[node:field_product:sku]/[node:field_product:name]
```

**In Rules actions**:

```yaml
actions:
  - action: drupal_message
    message: 'Event starts: [node:field_event:start_date]'
```

## Common Mistakes

- **Using wrong separator** -- Sub-fields use `:` (colon), extended properties use `__` (double-underscore) in the column name itself
- **Not checking token availability** -- Use token browser (/admin/help/token) to verify available tokens
- **Forgetting to sanitize in templates** -- Tokens in Twig auto-escape, but in PHP code sanitize manually

## See Also

- Reference: `/modules/contrib/custom_field/src/Hook/TokenHooks.php`
