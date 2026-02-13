---
description: YAML escaping rules for Drupal routing - single backslashes in single quotes prevent fatal site crashes
drupal_version: "11.x"
---

# YAML Escaping Rules

## When to Use

> Use single backslashes in single quotes for controller/form class references. This is CRITICAL - incorrect escaping causes fatal site crashes during cache rebuild.

## Decision

| Situation | Choose | Why |
|-----------|--------|-----|
| Controller/form class reference | Single backslashes in single quotes | YAML treats single quotes as literal strings - no escape processing |
| String with special characters | Double quotes with proper escaping | Required for interpolation, but adds complexity |
| Simple path or permission string | Single quotes or unquoted | Consistency and readability |

## Pattern

```yaml
# CORRECT: Single backslashes in single quotes
defaults:
  _controller: '\Drupal\my_module\Controller\MyController::method'
  _form: '\Drupal\my_module\Form\MyForm'
  _title: 'Page Title'

# WRONG: Double backslashes cause site crashes
defaults:
  _controller: '\\Drupal\\my_module\\Controller\\MyController::method'
```

## Common Mistakes

- **Wrong**: Using double backslashes (`\\\\`) in controller definitions → **Right**: Single backslashes in single quotes
- **Wrong**: Mixing quote types inconsistently → **Right**: Use single quotes for all class references
- **Wrong**: Using double quotes without proper escaping → **Right**: Stick to single quotes for simplicity
- **Wrong**: Omitting quotes entirely for class references → **Right**: Always quote class references

## See Also

- [Basic Route Structure](basic-route-structure.md)
- Reference: Core routing examples in `core/modules/*/routing.yml`
- Reference: [YAML 1.2 Specification](https://yaml.org/spec/1.2.2/)
