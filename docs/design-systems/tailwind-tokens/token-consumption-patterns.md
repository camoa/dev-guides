---
description: Access design tokens from CSS, Twig, JavaScript, and Drupal preprocess
---

# Token Consumption Patterns

## When to Use

> Use this when you need to access design tokens from CSS, Twig templates, JavaScript, or Drupal preprocess functions.

## Decision

| Context | Approach | Why |
|---|---|---|
| Component CSS | var(--token-name) | Direct access to design tokens |
| Twig template | Utility classes | Preferred for static styling |
| Twig template (dynamic) | Inline style with var() | Only for CMS-driven values |
| JavaScript (read) | getComputedStyle() | Get current token value at runtime |
| JavaScript (write) | setProperty() | Dynamic theme switching |

## Pattern

**CSS**

```css
.hero-banner {
  background-color: var(--color-brand);
  font-family: var(--font-display);
  border-radius: var(--radius-lg);
  padding: var(--spacing-section);
}
```

**Twig**

Prefer utility classes. Use inline styles only for truly dynamic CMS-driven values.

```twig
{# Utility classes (preferred) #}
<div class="bg-brand text-brand-light p-18 rounded-pill">{{ content }}</div>

{# Inline style (dynamic values only) #}
<div style="background-color: var(--color-brand);">{{ content }}</div>
```

**JavaScript**

```javascript
// Read a design token at runtime
const brand = getComputedStyle(document.documentElement)
  .getPropertyValue('--color-brand').trim();

// Set a token dynamically (e.g., theme switching)
document.documentElement.style
  .setProperty('--color-brand', 'oklch(60% 0.25 200)');
```

## Common Mistakes

- **Wrong**: Hardcoding background-color: #3b82f6. **Right**: background-color: var(--color-brand). Hardcoded values bypass the token system and break theme switching.
- **Wrong**: Caching JS-read token values permanently. Token values change when themes switch -- always read at the point of use.

## See Also

- [DaisyUI CSS Variable Reference](daisyui-css-variable-reference.md)
- [Custom DaisyUI Theme Definition](custom-daisyui-theme-definition.md)
- Reference: https://tailwindcss.com/docs/theme
