---
description: File structure, component.yml schema, JSX patterns, and allowed package imports for Canvas Code Components (React/Preact).
tldr: "Use Code Components when you need browser-rendered React/Preact with interactive state, dynamic behavior, or Tailwind CSS styling without a separate Drupal theme build. Use SDC components when you need server-side Drupal field integration."
drupal_version: "11.x"
---

# Code Component Format

## When to Use

> Use Code Components when you need browser-rendered React/Preact with interactive state, dynamic behavior, or Tailwind CSS styling without a separate Drupal theme build. Use SDC components when you need server-side Drupal field integration.

## Decision

| Situation | Choose | Why |
|---|---|---|
| Interactive React state / hooks | Code Component | Full React/Preact state management |
| Tailwind-styled, no Drupal preprocess | Code Component | Tailwind 4 globally available; no build config needed |
| Server-side rendering + Drupal fields | SDC Component | Works with Drupal's render + caching system |
| Static text/image layout | SDC Component | Less overhead than React |

## Pattern

**File structure** (local development with CLI):

```
my-components/
  components/
    hero-banner/
      component.yml   ← metadata, props, slots schema
      index.jsx       ← React/Preact component (default export required)
      index.css       ← optional: component styles (Tailwind utility classes)
```

**`component.yml` for Code Components:**

```yaml
# component.yml (Code Component)
name: Hero Banner
description: 'Full-width hero section with headline, body, and CTA button.'
group: Marketing
status: stable

props:
  type: object
  properties:
    headline:
      type: string
      title: Headline
    body:
      type: string
      title: Body
    ctaLabel:
      type: string
      title: 'CTA Button Label'
    ctaUrl:
      type: string
      title: 'CTA URL'

slots:
  badge:
    title: Badge
```

Note: Code Component props use camelCase names (e.g., `ctaLabel`), unlike SDC props which use snake_case.

**`index.jsx` — The React Component:**

```jsx
// index.jsx — MUST use default export, not named export
import { useState } from 'preact/hooks';

export default function HeroBanner({ headline, body, ctaLabel, ctaUrl, badge }) {
  return (
    <section className="relative min-h-64 bg-gradient-to-r from-blue-600 to-blue-800">
      {badge && (
        <div className="absolute top-4 left-4">{badge}</div>
      )}
      <div className="container mx-auto px-4 py-16 text-white">
        {headline && <h1 className="text-4xl font-bold mb-4">{headline}</h1>}
        {body && <p className="text-xl mb-8">{body}</p>}
        {ctaLabel && ctaUrl && (
          <a href={ctaUrl} className="btn bg-white text-blue-600 px-6 py-3 rounded-lg">
            {ctaLabel}
          </a>
        )}
      </div>
    </section>
  );
}
```

**Critical rules:**
1. **Default export only** — named exports are not allowed and will cause errors
2. **Preact under the hood** — Canvas uses Preact with the React compatibility layer; `react`, `react-dom`, `react-dom/client` are all mapped to `preact/compat`
3. **Tailwind CSS 4 is available globally** — Tailwind utility classes work without any build configuration
4. **Props arrive as component parameters** — same names as defined in `component.yml`
5. **Slots arrive as React children** — a slot named `badge` in YAML becomes a `badge` prop containing renderable content

**Allowed package imports:**

| Import | Notes |
|---|---|
| `preact` | Preact core — use instead of React |
| `preact/hooks` | React-equivalent hooks (useState, useEffect, etc.) |
| `preact/compat` | React compatibility layer (mapped from `react`) |
| `react` | Mapped to `preact/compat` |
| `react-dom` | Mapped to `preact/compat` |
| `drupal-canvas` | Canvas utilities and base components |

Third-party npm packages are NOT importable by default. Canvas issue #3500761 tracks expanding this.

## Common Mistakes

- **Wrong**: Named exports (`export function MyComponent`) → **Right**: Canvas requires `export default`
- **Wrong**: Importing arbitrary npm packages (`import _ from 'lodash'`) → **Right**: Only allowed packages work; others silently fail or error
- **Wrong**: Server-side expectations — Code Components render only in the browser → **Right**: No PHP/Drupal preprocess available
- **Wrong**: Forgetting that slots are renderable content, not strings → **Right**: Render `{badge}` directly, not `{badge.toString()}`

## See Also

- [Canvas CLI](canvas-cli.md) for the local development workflow
- [Canvas NPM Tools](canvas-npm-tools.md) for full npm tooling context
- Canvas Code Component docs: https://project.pages.drupalcode.org/canvas/code-components/
- Packages: https://project.pages.drupalcode.org/canvas/code-components/packages/
- canvas-starter (Balint Kleri's preconfigured dev environment): https://github.com/balintbrews/canvas-starter
