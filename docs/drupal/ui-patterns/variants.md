---
description: Variants — visual variations, variant prop generation, when to use variants vs props
drupal_version: "11.x"
---

# Variants

## When to Use

> Use variants for pre-defined visual/style switching between mutually exclusive appearances. Use props for data-driven values, typed inputs, or values sourced from entity fields.

## Decision

| Use Case | Use Variants | Use Props |
|----------|-------------|-----------|
| Visual theme/style switching | Yes | No |
| Multiple mutually exclusive appearances | Yes | No |
| Data that affects rendering logic | No | Yes |
| Values that need specific typing (boolean, number) | No | Yes |
| Values that come from entity fields | No | Yes |

## Pattern

### Defining variants in YAML

```yaml
variants:
  default:
    title: "Default"
    description: "Standard appearance"
  highlighted:
    title: "Highlighted"
    description: "Emphasized with accent border"
  compact:
    title: "Compact"
    description: "Reduced padding"
```

UI Patterns automatically generates a `variant` string enum prop from these definitions.

### Using variants in Twig

```twig
{# GOOD: handles missing variant #}
<div class="card card--{{ variant|default('default') }}">
  {{ content }}
</div>

{# BAD: breaks if variant is empty #}
<div class="card card--{{ variant }}">
```

Always use `|default('default')` or equivalent. If no variant is configured, the template receives an empty string, producing malformed class names like `card--`.

## Common Mistakes

- **Wrong**: Faking variants with a string prop and enum → **Right**: Variants get special UI treatment (separate selector, per-variant story rendering) that plain enum props lose
- **Wrong**: Not setting a default variant in Twig → **Right**: Always use `|default()` to handle empty variant values
- **Wrong**: Using variants for non-visual data → **Right**: Data-driven behavior should use typed props

## See Also

- [Defining Components](defining-components.md)
- [Pattern Library](pattern-library.md)
