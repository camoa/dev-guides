---
description: Implement dark mode in Tailwind — choose between automatic system preference, class-based toggle, or design token approach.
---

# Dark Mode

## When to Use

> Use the default `dark:` variant for automatic system preference. Use class or data-attribute strategy when a manual toggle is required.

## Decision

| If you need... | Use... | Why |
|----------------|--------|-----|
| Automatic system-preference only | Default `dark:` variant (media query) | Zero JavaScript; respects OS setting |
| Manual toggle (button switches mode) | Class strategy (`@custom-variant dark`) | Requires JS to add `.dark` class to `<html>` |
| Data-attribute theme system | `@custom-variant dark ([data-theme=dark] *)` | Supports multiple themes, not just light/dark |
| Three-way toggle (light/dark/system) | Class strategy + `localStorage` JS snippet | Most complete UX |

## Pattern — Automatic (No Config)

```html
<!-- Default behavior — no configuration needed -->
<div class="bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-100">
  <p class="text-gray-600 dark:text-gray-400">Content</p>
</div>
```

## Pattern — Class Strategy (v4)

```css
/* In your CSS */
@import "tailwindcss";
@custom-variant dark (&:where(.dark, .dark *));
```

```js
// Inline script in <head> — prevents FOUC
const isDark = localStorage.theme === 'dark' ||
  (!localStorage.theme && matchMedia('(prefers-color-scheme: dark)').matches);
document.documentElement.classList.toggle('dark', isDark);
```

## Pattern — Design Token Approach

```css
@import "tailwindcss";
@custom-variant dark (&:where([data-theme=dark], [data-theme=dark] *));

@layer base {
  :root {
    --color-surface: var(--color-white);
    --color-text-primary: var(--color-gray-900);
    --color-text-muted: var(--color-gray-600);
  }
  [data-theme="dark"] {
    --color-surface: var(--color-gray-900);
    --color-text-primary: var(--color-gray-100);
    --color-text-muted: var(--color-gray-400);
  }
}
```

```html
<!-- Semantic token utilities flip automatically — no dark: prefix needed -->
<div class="bg-[var(--color-surface)] text-[var(--color-text-primary)]">
```

The token approach is preferable for large design systems: semantic color tokens flip automatically via CSS custom property reassignment, eliminating `dark:` prefixes from every component.

## Common Mistakes

- **Wrong**: Forgetting the inline script for class strategy — causes Flash of Unstyled Content (FOUC) when page loads in dark mode. **Right**: Put the script inline in `<head>` before any CSS loads.
- **Wrong**: Over-using `dark:` utilities when a token-based approach would be cleaner. **Right**: Every `dark:bg-gray-900` couples component markup to the color value; semantic tokens decouple this.
- **Wrong**: Using `dark:` with media strategy AND class strategy simultaneously. **Right**: Pick one; mixing creates specificity conflicts.

## See Also

- [Component Patterns](component-patterns.md)
- [Design Token Mapping](design-token-mapping.md)
- Reference: https://tailwindcss.com/docs/dark-mode
