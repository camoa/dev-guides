---
description: "File structure, component.yml schema, JSX patterns, and allowed package imports for Canvas Code Components (React/Preact)."
tldr: "Use Code Components when you need browser-rendered React/Preact with interactive state, dynamic behavior, or Tailwind CSS styling without a separate Drupal theme build. Use SDC components when you need server-side Drupal field integration."
drupal_version: "11.x"
---

# Code Component Format

## When to Use

> You need a browser-rendered React/Preact component with interactive state, dynamic behavior, or you want to use Tailwind CSS for styling without a separate Drupal theme build process. Code Components are authored in JSX and CSS, stored as Drupal config entities, and rendered entirely in the browser (no server-side Twig rendering).

## Decision

| Situation | Choose | Why |
|---|---|---|
| Interactive React state / hooks | Code Component | Full React/Preact state management |
| Tailwind-styled, no Drupal preprocess | Code Component | Tailwind 4 globally available; no build config needed |
| Server-side rendering + Drupal fields | SDC Component | Works with Drupal's render + caching system |
| Static text/image layout | SDC Component | Less overhead than React |

## File Structure

When working locally (with the CLI), a Code Component lives in its own directory:

```
my-components/
  components/
    hero-banner/
      component.yml   ← metadata, props, slots schema
      index.jsx       ← React/Preact component (default export required)
      index.css       ← optional: component styles (Tailwind utility classes)
```

**The CLI discovers components by looking for `component.yml` files** and then expects `index.{js,jsx,ts,tsx}` and optionally `index.css` in the same folder.

## component.yml for Code Components

Code Component YAML shares structure with SDC YAML but the rendering is React instead of Twig:

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

**Note on naming**: prop and slot keys in `component.yml` are used **exactly as authored** — the CLI does no renaming. camelCase is a convention here, not a rule, and it exists because the *in-browser* code editor derives the machine name from the human-readable name you type by running it through lodash `camelCase` (so typing "CTA label" or "cta_label" both yield `ctaLabel`). If you author `component.yml` by hand, name props in camelCase yourself for consistency with components round-tripped through the editor.

## index.jsx — The React Component

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

**Critical rules for Code Components:**

1. **Default export only** — named exports are not allowed and will cause errors
2. **Preact under the hood** — Canvas uses Preact with the React compatibility layer; the import map aliases `react`, `react-dom`, and `react-dom/client` onto Preact's compat build. Import `react`, not `preact/compat` — the latter is not in the map
3. **Tailwind CSS 4 is available globally** — Tailwind utility classes work in all Code Components without any build configuration
4. **Props arrive as component parameters** — same names as defined in `component.yml`
5. **Slots arrive as React children** — a slot named `badge` in YAML becomes a `badge` prop containing renderable content

## Allowed Package Imports

Code Components run in a browser import-map environment. Canvas ships a base import map, and that map is the complete list of bare specifiers that resolve without any build step:

| Import | Notes |
|---|---|
| `preact` | Preact core |
| `preact/hooks` | `useState`, `useEffect`, … |
| `react` | Aliased to Preact's compat build |
| `react-dom` | Aliased to Preact's compat build |
| `react-dom/client` | Aliased to Preact's compat build |
| `react/jsx-runtime` | Automatic JSX runtime |
| `clsx` | Class-name joining |
| `class-variance-authority` | Variant-based class composition |
| `tailwind-merge` | Tailwind class conflict resolution |
| `swr` | Data fetching / caching hooks |
| `drupal-jsonapi-params` | JSON:API query building |
| `@drupal-api-client/json-api-client` | JSON:API client (prefer `JsonApiClient` from `drupal-canvas`) |
| `@tailwindcss/typography` | Prose styles |
| `drupal-canvas` | Canvas runtime: `Image`, `FormattedText`, `JsonApiClient`, utils |

**`preact/compat` is not in the map.** `react` and `react-dom` are *aliased to* Preact's compat build, but `import … from 'preact/compat'` does not resolve — import `react` instead.

Four legacy specifiers — `@/lib/FormattedText`, `@/lib/utils`, `@/lib/jsonapi-utils`, `@/lib/drupal-utils` — are still in the map for backward compatibility but are **deprecated and reserved**: their contents moved into `drupal-canvas`, and Canvas's ESLint config errors (with an autofix) if you import them. You cannot use those four paths for your own files. `next-image-standalone` is likewise deprecated in favour of `Image` from `drupal-canvas`.

**Third-party npm packages: it depends which path you are on.**

- **In-browser code editor** — you get the base import map and nothing else. An arbitrary `import _ from 'lodash'` will not resolve.
- **CLI (`@drupal-canvas/cli`)** — third-party packages *are* supported. `canvas build` walks your imports, bundles anything it classifies as third-party into a vendor bundle, and `canvas push` writes those bundles into the site's global asset library. Canvas then appends the asset library's entries to the runtime import map, where they override same-named base entries. So a package installed in your codebase and imported from a component works in production after a push.

**Your own shared code** uses the `@/` alias, rooted at the `aliasBaseDir` from `canvas.config.json`. `@/…` imports are resolved and bundled at build time. Relative `./` and `../` JS/TS *module* imports are **not** supported — use `@/`. (Relative *asset* imports — images, SVG, fonts by file — are fine.) Font packages (`@fontsource/*`) and CSS side-effect imports are rejected outright.

## Common Mistakes

- Named exports (`export function MyComponent`) — Canvas requires `export default`
- Importing `preact/compat` — not in the import map; import `react` instead
- Importing an arbitrary npm package while working in the **in-browser** editor — only the base import map resolves there. Through the CLI, install it and let `build`/`push` bundle it
- Using `./` or `../` to import a sibling helper — Canvas rejects relative module imports; use the `@/` alias
- Writing your own file at `@/lib/utils` (or the other three reserved `@/lib/*` paths) — Canvas owns those specifiers
- Using `className` the React way then wondering why Tailwind isn't working — Tailwind IS available; double-check class names
- Server-side expectations — Code Components render only in the browser; there is no PHP/Drupal preprocess
- Using React-specific APIs not available in Preact — most React APIs work, but some edge cases differ; test in the Canvas environment
- Forgetting that slots are renderable content, not strings — render `{badge}` directly, not `{badge.toString()}`

## See Also

- [Canvas CLI](canvas-cli.md) for the local development workflow
- [Allowed Packages](canvas-npm-tools.md) for full npm tooling context
- Canvas Code Component docs: https://project.pages.drupalcode.org/canvas/code-components/
- Packages: https://project.pages.drupalcode.org/canvas/code-components/packages/
- canvas-starter (Balint Kleri's preconfigured dev environment): https://github.com/balintbrews/canvas-starter
