---
description: Variants — pre-defined visual variations for components, including per-instance variants in Layout Builder
tldr: Variants are declared in component YAML and auto-converted to a string enum prop named variant. For per-instance variants in Layout Builder, use either an entity field (Option 1 — same variant everywhere the block is placed) or a block template reading configuration.{prop} (Option 2 — different variant per placement, requires Plus Suite BlockPropertiesEvent).
drupal_version: "10.3+ / 11"
---

# Variants

## When to Use

> Use variants for pre-defined, mutually exclusive visual styles of a component. Use props for data-driven values, typed inputs, or field-sourced values. For per-placement variant control in Layout Builder, choose between the entity-field pattern (same variant per block content) and the LB block configuration pattern (different variant per placement).

## Decision

| Use Case | Use Variants | Use Props |
|----------|-------------|-----------|
| Visual theme/style switching | Yes | No |
| Multiple mutually exclusive appearances | Yes | No |
| Data that affects rendering logic | No | Yes |
| Values that need specific typing (boolean, number) | No | Yes |
| Values that come from entity fields | No | Yes |

### Per-Instance Variants in Layout Builder

| Need | Pattern |
|------|---------|
| Variant tied to the block content (same everywhere it's placed) | Option 1 — entity field |
| Variant tied to the placement (different per page) | Option 2 — LB block configuration + template |
| Plus Suite project with `BlockPropertiesEvent` already wired | Option 2 |
| No template overrides allowed (pure UI Patterns shop) | Option 1 |

## Pattern

### Defining Variants in YAML

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

### Always Set a Default in Twig

```twig
{# GOOD: handles missing variant #}
<div class="alert alert--{{ variant|default('info') }}">

{# BAD: breaks if variant is empty #}
<div class="alert alert--{{ variant }}">
```

### Option 1 — Entity Field (variant same per block content)

Add `field_variant` (`list_string`) to the block content type with allowed values matching the SDC's variant keys. Map it in Manage Display:

```yaml
variant_id:
  source_id: 'field_property:block_content:field_variant:value'
  source:
    type: value
```

Pro: pure UI Patterns wiring, no template required.
Con: variant is per-block-content — duplicating content to vary the variant.

### Option 2 — LB Block Configuration + Twig Template (variant per placement)

Plus Suite (or a custom `BlockPropertiesEvent` subscriber) adds a variant select to the LB block placement form. A block template reads `configuration.{prop}` and passes it to the SDC:

```twig
{# templates/block--inline-block--hero.html.twig #}
{% set variant = configuration.hero_variant|default('default') %}
{% include 'mytheme:hero' with {
  variant: variant,
  heading: content.field_heading[0]['#context'].value,
  body: content.field_body|render,
  image: content.field_image,
} only %}
```

Pro: each placement carries its own variant value.
Con: incompatible with pure UI Patterns wiring — the formatter has no access to LB block `configuration` arrays.

## Common Mistakes

- **Wrong**: Faking variants with a string prop + enum → **Right**: Variants get a dedicated variant selector UI and per-variant story rendering that a plain enum prop loses.
- **Wrong**: Not using `|default('...')` in Twig → **Right**: If no variant is configured, the template receives an empty string, producing malformed class names like `card--`.
- **Wrong**: Expecting `variant_id` in entity view display to differ per LB placement → **Right**: View display config is per-bundle and applies to every instance. Use Option 1 or 2 for per-instance variation.
- **Wrong**: Trying to wire `configuration.variant` into a `field_property` source → **Right**: UI Patterns formatters can't read LB block configuration. Use the template pattern for per-placement variants.

## See Also

- [Defining Components](defining-components.md)
- [Pattern Library](pattern-library.md)
- [Plus Suite Custom Block Types](../plus-suite/custom-block-types.md) — `BlockPropertiesEvent` subscriber for adding LB block configuration fields
