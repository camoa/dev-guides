---
description: UI Patterns Best Practices — slot vs prop decisions, prop drilling, prop paradoxes
drupal_version: "11.x"
---

# Best Practices & Anti-Patterns

## When to Use

> Reference this guide when designing component APIs, deciding between slots and props, or reviewing components for architecture problems.

## Decision

### Slot vs prop

| Content Type | Use | Reason |
|-------------|-----|--------|
| Block output, rendered markup | Slot | Renderables need the render pipeline |
| Plain text, numbers, booleans | Prop | Strictly typed, validated by JSON Schema |
| Images with URL + alt + title | Slot | Complex renderables; avoid prop drilling |
| Navigation links | Prop (`links` type) | Structured data with a defined schema |
| CSS classes, HTML attributes | Prop (`attributes` type) | Key-value data, not renderables |

### When NOT to use UI Patterns

| Situation | Better Approach |
|-----------|----------------|
| Component used only by developers in Twig | Use SDC directly |
| Simple text replacement in a theme | Use preprocess hooks or Twig |
| One-off page layout | Use Layout Builder with core layouts |
| Fixed, predictable content type structure | Field formatters may be simpler |

## Pattern

### Avoid prop drilling

```yaml
# BAD: parent has image_url and image_alt just to pass to child
props:
  properties:
    image_url:
      type: "string"
    image_alt:
      type: "string"

# GOOD: image is a slot, filled by a nested image component
slots:
  image:
    title: "Image"
```

### Avoid prop paradoxes

```yaml
# BAD: is_link and url create incompatible states
props:
  properties:
    is_link:
      type: "boolean"
    url:
      type: "string"

# GOOD: single optional URL prop (empty = not a link)
props:
  properties:
    url:
      "$ref": "ui-patterns://url"
```

### Always use `|default()` in Twig

```twig
{# GOOD #}
<h2>{{ title|default('Untitled') }}</h2>
<div class="card card--{{ variant|default('default') }}">

{# BAD #}
<h2>{{ title }}</h2>
<div class="card card--{{ variant }}">
```

### Always use `{{ attributes }}` on wrapper elements

```twig
<div{{ attributes }}>
  {{ content }}
</div>
```

Drupal modules (contextual links, quick edit, translation, SEO tools) inject attributes into the wrapper. Without `{{ attributes }}`, these features break silently.

## Common Mistakes

- **Wrong**: Creating one component per content type → **Right**: Components should be content-agnostic; a "Card" works for articles, events, and products
- **Wrong**: Using business-specific names (EventCard, NewsSlideshow) → **Right**: Use business-agnostic names (Card, Hero, Accordion)
- **Wrong**: Hardcoding component IDs in Twig `include()` → **Right**: Use slots or render arrays; if `include()` is necessary, use `with_context = false`
- **Wrong**: Hardcoding HTML IDs in components → **Right**: Generate IDs with `random()` or accept them as props to avoid duplicate IDs

## See Also

- [Defining Components](defining-components.md)
- [Slots System](slots-system.md)
- [Security & Accessibility](security-and-accessibility.md)
- Reference: [Best Practices](https://project.pages.drupalcode.org/ui_patterns/2-authors/2-best-practices/)
- Reference: [Drupal.org Best Practices](https://www.drupal.org/docs/extending-drupal/contributed-modules/contributed-module-documentation/ui-patterns/best-practices)
