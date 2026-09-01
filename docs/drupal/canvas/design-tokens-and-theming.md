---
description: "How Canvas handles design tokens, CSS custom properties, and Tailwind theming for both SDC and Code Components."
tldr: "Use this when you need to understand how Canvas handles design tokens, CSS custom properties, and theming — both for the Canvas editor UI (where editors can adjust token values) and for component styling (how tokens flow into SDC and Code…"
drupal_version: "11.x"
---

# Design Tokens and Theming

## When to Use

> Use this when you need to understand how Canvas handles design tokens, CSS custom properties, and theming — both for the Canvas editor UI (where editors can adjust token values) and for component styling (how tokens flow into SDC and Code Components).

## Decision

| If you need... | Approach... | Why |
|---|---|---|
| Brand colors available as Tailwind classes | Tailwind `@theme` in global CSS | Tokens become both CSS vars and utility classes |
| Tokens editable in Canvas UI by editors | Expose tokens in Canvas theme configuration | Editors can adjust without code changes |
| SDC component using theme colors | Reference CSS custom properties (`var(--color-brand-primary)`) | SDC CSS doesn't use Tailwind by default |
| Design tokens from Figma | Figma token export → CSS custom properties → `@theme` | Standard token pipeline; no Canvas-specific tool |
| Component-specific overrides | Prop-driven CSS classes or inline styles | Per-component flexibility without global token changes |

## Design Token Exposure in Canvas Editor

Canvas allows token values to be surfaced in the editor for non-developer adjustment. This is a Canvas configuration concern, not a component concern. Currently tracked as an evolving feature — consult the Canvas project roadmap for the current state of the design token editor UI.

## Pattern

Canvas approaches theming in layers:

1. **Global CSS / Tailwind configuration** — A theme provides base CSS and Tailwind configuration that applies globally to all Code Components. In a Nebula-based codebase, this lives in a global CSS entry file that Tailwind 4 processes.

2. **Design tokens as CSS custom properties** — Canvas supports exposing design tokens (colors, typography, spacing) that editors can adjust in the Canvas UI. When a token changes, all components using that token update across all Canvas pages.

3. **Tailwind CSS 4 `@theme`** — Tailwind 4's `@theme` directive maps design tokens to Tailwind utility classes and CSS custom properties simultaneously:

```css
/* global.css */
@import "tailwindcss";

@theme {
  --color-brand-primary: #2563eb;
  --color-brand-secondary: #1e40af;
  --font-size-heading: 2.25rem;
  --spacing-section: 4rem;
}
```

After this, `text-brand-primary`, `bg-brand-primary` etc. are valid Tailwind classes in your components.

4. **SDC component styling** — SDC components use their own `*.css` file. Standard Drupal/Bootstrap CSS classes work. To use Canvas design tokens, reference the CSS custom properties Canvas exposes.

**Drupal Theme for Canvas setup:**

1. Generate the theme with Drush or create manually
2. Add `package.json` with Tailwind 4 + Vite build tooling
3. Define CSS custom properties and `@theme` declarations in the global CSS entry
4. Use `canvas_page` in the theme's page template as a render target
5. Disable CSS/JS aggregation during development (`/admin/config/development/performance`)

Standard `*.info.yml` registrations apply for CSS and JS assets. Canvas pages use a different template than standard content types — your theme may need both `page.html.twig` (standard pages) and `canvas-page.html.twig` (Canvas pages).

## Common Mistakes

- **Wrong**: Using Tailwind classes in SDC Twig templates without Tailwind configured in the Drupal theme build → **Right**: Twig files don't process through Tailwind unless the build watches them
- **Wrong**: Defining design tokens only in the Code Component codebase but not in the Drupal theme → **Right**: Tokens need to be consistent across both SDC and Code Component contexts
- **Wrong**: Expecting Tailwind to be available server-side for SDC components → **Right**: Tailwind is only available to Code Components via the Canvas runtime; SDC components need their own CSS build
- **Wrong**: Not testing Canvas page appearance across both the Canvas editor and the live page → **Right**: Some styles apply only in the editor context

## See Also

- Tailwind CSS 4 theme configuration: https://tailwindcss.com/docs/theme
- WebWash Tailwind Canvas setup: https://www.webwash.net/tailwind-css-theme-setup-for-drupal-canvas/
- Canvas SDC Starterkit: https://www.drupal.org/project/canvas_sdc_starterkit
