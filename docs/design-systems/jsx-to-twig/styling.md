---
description: Convert React styling patterns to Twig and SDC scoped CSS
drupal_version: "11.x"
---

# Styling Translation

## When to Use

> Use this when converting React styling patterns -- `className`, CSS Modules, Tailwind utilities, `cn()`/`clsx()`, `cva()` (class-variance-authority), inline styles -- to Twig and SDC equivalents.

## Decision

| React/CSS Pattern | Twig/SDC Equivalent | Notes |
|---|---|---|
| `className="btn btn-primary"` | `class="btn btn-primary"` (static) | Direct translation for static classes |
| `className="btn btn-primary"` (with attributes) | `{{ attributes.addClass('btn', 'btn-primary') }}` | When component needs Drupal attribute merging |
| `className={cn('btn', variant && \`btn-${variant}\`)}` | `{% set classes = ['btn', variant ? 'btn-' ~ variant] %}` | Conditional class array pattern |
| `className={cn('card', { 'card-bordered': bordered })}` | `bordered ? 'card-bordered'` in classes array | Object syntax maps to ternary in Twig |
| `style={{ color: 'red', fontSize: '14px' }}` | Avoid; use CSS classes | Inline styles are an anti-pattern in SDCs |
| `style={{ '--custom-prop': value }}` | `attributes.setAttribute('style', '--custom-prop: ' ~ value)` | CSS custom properties are the exception |
| CSS Modules: `styles.card` | SDC scoped CSS: `component-name.css` | File in same directory as component; auto-scoped |
| Tailwind: `className="flex gap-4 p-6"` | `class="flex gap-4 p-6"` | Tailwind classes are framework-agnostic; identical in Twig |
| `cn()` / `clsx()` (class merging) | `{% set classes = [...] %}` + `attributes.addClass(classes)` | No runtime JS equivalent; resolve in Twig template |
| `cva()` (class-variance-authority) | component.yml `variants` + Twig conditionals | Map each CVA variant to an enum prop |

## Pattern: CVA Variants to component.yml

**React (with CVA)**
```jsx
const buttonVariants = cva('btn', {
  variants: {
    variant: {
      default: '',
      primary: 'btn-primary',
      secondary: 'btn-secondary',
      ghost: 'btn-ghost',
    },
    size: {
      sm: 'btn-sm',
      md: '',
      lg: 'btn-lg',
    },
  },
  defaultVariants: { variant: 'default', size: 'md' },
});

function Button({ variant, size, children, ...props }) {
  return <button className={buttonVariants({ variant, size })} {...props}>{children}</button>;
}
```

**component.yml**
```yaml
name: Button
variants:
  default: { title: Default }
  primary: { title: Primary }
  secondary: { title: Secondary }
  ghost: { title: Ghost }
props:
  type: object
  properties:
    size:
      title: Size
      type: string
      enum: [sm, md, lg]
      meta:enum:
        sm: Small
        md: Medium
        lg: Large
slots:
  label:
    title: Label
```

**Twig**
```twig
{% set classes = [
  'btn',
  variant and variant != 'default' ? 'btn-' ~ variant,
  size and size != 'md' ? 'btn-' ~ size,
] %}
<button {{ attributes.addClass(classes) }}>{{ label }}</button>
```

## Pattern: SDC Scoped CSS

**SDC structure**
```
components/
  card/
    card.component.yml
    card.twig
    card.css           <-- Scoped to this component automatically
```

**card.css**
```css
/* Styles are automatically scoped to this component's markup */
.card {
  border-radius: var(--rounded-box, 1rem);
  overflow: hidden;
}
.card-body {
  padding: var(--card-padding, 2rem);
}
```

SDC CSS files are automatically attached when the component is rendered. No import statement is needed.

## Common Mistakes

- **Wrong**: Using `twMerge()` logic in JavaScript alongside Twig → **Right**: No Twig equivalent; ensure your Twig template produces the correct final set of classes
- **Wrong**: Putting component styles in global CSS files → **Right**: SDC scoped CSS keeps styles co-located with the component
- **Wrong**: Using `{{ attributes.setAttribute('class', 'my-classes') }}` → **Right**: `setAttribute` overwrites all existing classes; use `addClass()` to merge

## See Also

- [Conditional Rendering](conditional-rendering.md)
- [TypeScript to Component.yml](typescript-to-component-yml.md)
- Reference: [Class Variance Authority](https://cva.style/docs)
