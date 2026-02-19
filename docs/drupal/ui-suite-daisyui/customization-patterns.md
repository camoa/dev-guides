---
description: Add custom components, override DaisyUI tokens, and extend base components
---

# Customization Patterns

## Adding a Custom Component

Create a new SDC in your sub-theme's `components/` directory:

```yaml
# components/pricing_card/pricing_card.component.yml
name: Pricing Card
description: "A pricing tier card with DaisyUI styling."
group: "Custom"
slots:
  title:
    title: Title
  price:
    title: Price
  features:
    title: Features
  action:
    title: Action Button
props:
  type: object
  properties:
    highlighted:
      title: "Highlighted?"
      description: "Apply primary border to highlight this tier."
      type: boolean
```

```twig
{# components/pricing_card/pricing_card.twig #}
{% set classes = [
  'card',
  'card-border',
  highlighted ? 'border-primary border-2',
] %}
<div {{ attributes.addClass(classes) }}>
  <div class="card-body text-center">
    <h3 class="card-title justify-center text-2xl">{{ title }}</h3>
    <div class="text-4xl font-bold my-4">{{ price }}</div>
    <div class="text-left">{{ features }}</div>
    <div class="card-actions justify-center mt-4">{{ action }}</div>
  </div>
</div>
```

## Overriding DaisyUI Tokens via CSS

To customize DaisyUI design tokens beyond what UI Skins provides, add a custom CSS file:

```css
/* dist/css/custom/overrides.css */
:root {
  --radius-box: 0.5rem;
  --radius-field: 0.25rem;
  --border: 2px;
}

/* Override for a specific theme */
[data-theme="corporate"] {
  --color-primary: oklch(0.55 0.2 250);
  --color-secondary: oklch(0.65 0.15 200);
}
```

Register in your sub-theme's libraries:

```yaml
# my_theme.libraries.yml
overrides:
  css:
    theme:
      dist/css/custom/overrides.css: {}
```

## Extending a Base Component

To modify an existing component without fully replacing it, override only the Twig template while keeping the original YAML:

```twig
{# my_theme/components/card/card.twig #}
{# Extends the card with an optional "featured" badge #}
{% set classes = [
  'card',
  variant and variant == 'side' ? 'card-' ~ variant,
  border ? 'card-' ~ border,
  size ? 'card-' ~ size,
  image_full ? 'image-full',
] %}

<div {{ attributes.addClass(classes) }}>
  {% if featured %}
    <div class="badge badge-primary absolute top-2 right-2">Featured</div>
  {% endif %}
  {# ... rest of card template ... #}
</div>
```

## Common Mistakes

- **Adding Tailwind utility classes not scanned by `@source` directives** -- The build pipeline only includes Tailwind classes found in files matched by `@source` patterns in `app.pcss.css`. Classes used only in custom templates outside those patterns will be purged. WHY: Tailwind 4 tree-shakes unused classes at build time. Add appropriate `@source` directives or include classes in `safelist.txt`.
- **Overriding `.component.yml` without copying all props** -- If you override a component's YAML in a sub-theme, you must include ALL props and slots, not just the ones you changed. WHY: UI Patterns reads the entire YAML; partial overrides result in missing props.

## See Also

- `drupal-ui-patterns.md` -- Component creation patterns
- `design-system-daisyui.md` -- DaisyUI token customization
