---
description: Implement dark mode in Tailwind — choose between automatic system preference, class-based toggle, or design token approach.
tldr: "Use the default `dark:` variant for automatic system preference. Use class or data-attribute strategy when a manual toggle is required."
---

# Dark Mode

## When to Use

> Implementing dark mode — whether automatic (system preference) or manually toggled.

## Decision

| If you need... | Use... | Why |
|----------------|--------|-----|
| Automatic system-preference only | Default `dark:` variant (media query) | Zero JavaScript; respects OS setting |
| Manual toggle (button switches mode) | Class strategy (`@custom-variant dark`) | Requires JS to add `.dark` class to `<html>` |
| Data-attribute theme system | `@custom-variant dark ([data-theme=dark] *)` | Supports multiple themes, not just light/dark |
| Three-way toggle (light/dark/system) | Class strategy + `localStorage` JS snippet | Most complete UX |

## Pattern — Automatic (Media Query, No Config)

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

## Pattern — Design Token Approach for Dark Mode

```css
@import "tailwindcss";
@custom-variant dark (&:where([data-theme=dark], [data-theme=dark] *));

@layer base {
  :root {
    --color-surface: var(--color-white);
    --color-surface-alt: var(--color-gray-50);
    --color-text-primary: var(--color-gray-900);
    --color-text-muted: var(--color-gray-600);
  }
  [data-theme="dark"] {
    --color-surface: var(--color-gray-900);
    --color-surface-alt: var(--color-gray-800);
    --color-text-primary: var(--color-gray-100);
    --color-text-muted: var(--color-gray-400);
  }
}
```
```html
<!-- Semantic token utilities don't need dark: prefix — they change with theme -->
<div class="bg-[var(--color-surface)] text-[var(--color-text-primary)]">
```

The design token approach is preferable for large design systems: semantic color tokens flip automatically via CSS custom property reassignment, eliminating `dark:` prefixes from every component.

## Common Mistakes

- **Forgetting the inline script for class strategy** — causes Flash of Unstyled Content (FOUC) when page loads in dark mode
- **Over-using `dark:` utilities when a token-based approach would be cleaner** — every `dark:bg-gray-900` is coupling component markup to the color value
- **Using `dark:` with media strategy AND class strategy simultaneously** — pick one; mixing creates specificity conflicts

## See Also

- [Component Patterns](component-patterns.md)
- [Design Token Mapping](design-token-mapping.md)
- Reference: https://tailwindcss.com/docs/dark-mode
