---
description: Build reusable UI components with Drupal Single Directory Components (SDC) using props, slots, and component composition.
---

# SDC Component Reuse

## When to Use

When you need reusable UI components (buttons, cards, modals, forms) used across multiple pages, content types, or blocks. SDCs (Single Directory Components) are Drupal's native component system (core since 10.3).

## Props and Slots

| Mechanism | Type | Use When |
|-----------|------|----------|
| **Props** | Strictly-typed data (strings, booleans, numbers, arrays) | Pass configuration values, labels, settings |
| **Slots** | Renderable content (HTML, nested components) | Pass flexible content, nested markup |

## Decision

| If you need... | Use... | Why |
|---|---|---|
| Reusable button with variants | SDC with props for variant/size | Single component, customized via props |
| Card with variable content | SDC with slots for header/body/footer | Flexible content injection |
| Component with nested components | Slots | Compose components from other components |
| Component used once | Standard Twig template | Don't create SDC until reused 2+ times |
| Design system consistency | SDCs for all UI patterns | Centralized, reusable, maintainable |

## Pattern

```yaml
# mytheme/components/card/card.component.yml
$schema: https://git.drupalcode.org/project/drupal/-/raw/HEAD/core/modules/sdc/src/component.schema.json
name: Card
status: stable
props:
  type: object
  properties:
    variant:
      type: string
      enum: [default, highlighted, compact]
      default: default
    title:
      type: string
      title: Card Title
slots:
  header:
    title: Card Header
  body:
    title: Card Body
  footer:
    title: Card Footer
```

```twig
{# mytheme/components/card/card.twig #}
<div class="card card--{{ variant }}">
  {% if slots.header %}
    <div class="card__header">
      {{ slots.header }}
    </div>
  {% endif %}

  {% if title %}
    <h3 class="card__title">{{ title }}</h3>
  {% endif %}

  <div class="card__body">
    {{ slots.body }}
  </div>

  {% if slots.footer %}
    <div class="card__footer">
      {{ slots.footer }}
    </div>
  {% endif %}
</div>
```

```twig
{# Using the component #}
{% include 'mytheme:card' with {
  variant: 'highlighted',
  title: 'Welcome',
  slots: {
    body: content.field_body,
    footer: content.field_links,
  }
} %}
```

Reference: `core/modules/sdc/`, Radix theme components at `themes/contrib/radix/components/`

## Component Composition

```twig
{# Nesting components via slots #}
{% include 'mytheme:modal' with {
  slots: {
    content: include('mytheme:card' with {
      title: 'Modal Card',
      slots: {
        body: 'Card inside modal',
      }
    })
  }
} %}
```

## Common Mistakes

- **Creating component for single use** — Wait until component is reused 2+ times (Rule of Three)
- **Duplicating components instead of using props** — Use props/slots to make one flexible component instead of creating multiple similar components
- **Props for renderable content** — Use slots for HTML/components, props for simple data
- **Missing component schema** — Always define `component.yml` for validation and IDE autocomplete
- **Not using design tokens** — Define colors, spacing, typography in CSS custom properties, reference in component styles

## See Also

- [Twig Template Inheritance](twig-template-inheritance.md)
- [Render Array Patterns](render-array-patterns.md)
- Reference: [Using Single-Directory Components | Drupal.org](https://www.drupal.org/docs/develop/theming-drupal/using-single-directory-components)
- Reference: [Understanding Props and Slots | Drupalize.Me](https://drupalize.me/tutorial/understanding-props-and-slots-drupal-single-directory-components)
