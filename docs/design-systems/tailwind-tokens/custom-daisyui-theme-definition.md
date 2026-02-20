---
description: Create branded DaisyUI themes with Tailwind v4 syntax
---

# Custom DaisyUI Theme Definition

## When to Use

> Use this when you need to create a branded DaisyUI theme for your project.

## Decision

| Need | Approach | Config Field |
|---|---|---|
| Light theme | color-scheme: light | Sets CSS color-scheme for browser UI |
| Dark theme | color-scheme: dark | Sets CSS color-scheme for browser UI |
| Default theme | default: true | Applied when no data-theme specified |
| Auto dark mode | prefersdark: true | Auto-activates for prefers-color-scheme: dark |

## Pattern

**DaisyUI v5 Custom Theme (Tailwind v4 syntax)**

```css
@plugin "daisyui/theme" {
  name: "mybrand";
  default: true;
  color-scheme: light;

  --color-primary: oklch(55% 0.3 240);
  --color-primary-content: oklch(98% 0.01 240);
  --color-secondary: oklch(65% 0.22 180);
  --color-secondary-content: oklch(98% 0.01 180);
  --color-accent: oklch(70% 0.2 330);
  --color-accent-content: oklch(98% 0.01 330);
  --color-neutral: oklch(30% 0.03 240);
  --color-neutral-content: oklch(95% 0.01 240);
  --color-base-100: oklch(98% 0.005 240);
  --color-base-200: oklch(95% 0.01 240);
  --color-base-300: oklch(90% 0.015 240);
  --color-base-content: oklch(25% 0.03 240);
  --color-info: oklch(70% 0.18 230);
  --color-info-content: oklch(98% 0.01 230);
  --color-success: oklch(65% 0.2 145);
  --color-success-content: oklch(98% 0.01 145);
  --color-warning: oklch(82% 0.18 80);
  --color-warning-content: oklch(20% 0.04 80);
  --color-error: oklch(60% 0.25 25);
  --color-error-content: oklch(98% 0.01 25);

  --radius-selector: 0.25rem;
  --radius-field: 0.5rem;
  --radius-box: 1rem;
  --size-selector: 0.25rem;
  --size-field: 0.25rem;
  --border: 1px;
  --depth: 1;
  --noise: 0;
}
```

**Dark Theme Variant**

```css
@plugin "daisyui/theme" {
  name: "mybrand-dark";
  prefersdark: true;         /* Auto-activates for prefers-color-scheme: dark */
  color-scheme: dark;        /* Sets CSS color-scheme for browser UI */

  --color-primary: oklch(65% 0.25 240);
  --color-primary-content: oklch(15% 0.02 240);
  --color-base-100: oklch(18% 0.02 240);
  --color-base-200: oklch(22% 0.025 240);
  --color-base-300: oklch(28% 0.03 240);
  --color-base-content: oklch(90% 0.01 240);
  /* ... remaining colors with dark-adjusted lightness values */
}
```

**Switching Themes at Runtime**

```javascript
document.documentElement.setAttribute('data-theme', 'mybrand-dark');
```

In Drupal, UI Suite DaisyUI handles theme switching via ui_suite_daisyui.ui_skins.themes.yml which maps theme names to data-theme on html.

## Common Mistakes

- **Wrong**: Defining theme without color-scheme field. **Right**: Always set color-scheme: light or dark for proper browser UI rendering.
- **Wrong**: Creating dark theme by inverting lightness values mechanically. **Right**: Re-evaluate contrast and saturation for dark mode separately.

## See Also

- [DaisyUI CSS Variable Reference](daisyui-css-variable-reference.md)
- [Brand Color Mapping Workflow](brand-color-mapping-workflow.md)
- [UI Suite DaisyUI Starterkit Patterns](ui-suite-daisyui-starterkit-patterns.md)
- Reference: https://daisyui.com/docs/themes/
