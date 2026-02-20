---
description: Variants — pre-defined visual variations for components
drupal_version: "10.3+ / 11"
---

## Variants

### How Variants Work

Variants provide pre-defined visual variations of a component without requiring a separate prop with JSON Schema setup. They are defined in the component YAML and automatically converted to a string enum prop named `variant`.

```yaml
variants:
  default:
    title: "Default"
    description: "Standard card appearance"
  highlighted:
    title: "Highlighted"
    description: "Emphasized card with accent border"
  compact:
    title: "Compact"
    description: "Reduced padding version"
```

During component discovery, `ComponentPluginManager::buildVariantProp()` generates:

```php
[
  'title' => 'Variant',
  '$ref' => 'ui-patterns://variant',
  'enum' => ['default', 'highlighted', 'compact'],
  'meta:enum' => [
    'default' => 'Default',
    'highlighted' => 'Highlighted',
    'compact' => 'Compact',
  ],
]
```

### Using Variants in Twig

The variant value is available as the `variant` variable:

```twig
<div class="card card--{{ variant|default('default') }}">
  {{ content }}
</div>
```

### When to Use Variants vs Props

| Use Case | Use Variants | Use Props |
|---|---|---|
| Visual theme/style switching | Yes | No |
| Multiple mutually exclusive appearances | Yes | No |
| Data that affects rendering logic | No | Yes |
| Values that need specific typing (boolean, number) | No | Yes |
| Values that come from entity fields | No | Yes |

### Always Set a Default Variant

Every component with variants must render correctly when no variant is specified. The template should always use `|default('default')` or equivalent:

```twig
{# GOOD: handles missing variant #}
<div class="alert alert--{{ variant|default('info') }}">

{# BAD: breaks if variant is empty #}
<div class="alert alert--{{ variant }}">
```

### Common Mistakes

| Mistake | Why It Is Wrong |
|---|---|
| Faking variants with a string prop and enum | Variants get special UI treatment (separate selector, per-variant story rendering). A plain enum prop loses these benefits. |
| Not setting a default variant in Twig | If no variant is configured, the template receives an empty string, producing malformed class names like `card--`. |
| Using variants for non-visual data | Variants are for visual switching only. Data-driven behavior should use typed props. |

### See Also

- [Defining Components](#defining-components)
- [Pattern Library](#pattern-library)