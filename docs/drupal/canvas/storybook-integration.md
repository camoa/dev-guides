---
description: How to use Storybook for Canvas Code Component and SDC component development — story formats, setup approaches, and decision by component type.
tldr: "Use this when developing Canvas Code Components locally and you want to build, preview, and test components in isolation before pushing to Drupal. Storybook is the recommended isolated development environment for Canvas Code Components."
drupal_version: "11.x"
---

# Storybook Integration

## When to Use

> Use this when developing Canvas Code Components locally and you want to build, preview, and test components in isolation before pushing to Drupal. Storybook is the recommended isolated development environment for Canvas Code Components.

## Decision

| Component type | Storybook approach | Story format |
|---|---|---|
| Code Component (React/Preact) | Standard Storybook in Nebula | `.stories.jsx` / `.stories.tsx` |
| SDC Component (Twig) with Canvas SDC Starterkit | Starterkit's built-in Storybook | Component YAML drives stories automatically |
| SDC Component (Twig) with Drupal Storybook module | Drupal Storybook module | `.stories.twig` with `{% story %}` tags |

## Pattern

Nebula includes Storybook preconfigured with:
- Viewports that match Canvas editor breakpoints
- Vite-based Storybook builder (fast HMR)
- SWC for JSX compilation

For Canvas Code Components, stories are standard JavaScript/JSX/TypeScript Storybook stories:

```jsx
// components/hero-banner/hero-banner.stories.jsx
import HeroBanner from './index.jsx';

export default {
  title: 'Marketing/Hero Banner',
  component: HeroBanner,
};

export const Default = {
  args: {
    headline: 'Transform Your Business',
    body: 'Start your journey today with our platform.',
    ctaLabel: 'Get Started',
    ctaUrl: 'https://example.com',
  },
};

export const MinimalContent = {
  args: {
    headline: 'Simple Message',
  },
};
```

Canvas Code Component stories are regular React/Preact stories — no special Canvas-specific story format is required.

**SDC Components and Storybook** (separate tools):
- **Drupal Storybook module** (`drupal.org/project/storybook`) — Allows writing stories in Twig using `{% stories %}` and `{% story %}` tags
- **SDC Storybook addon** (`storybook-addon-sdc`) — Dynamically loads `*.component.yml` definitions as stories
- **Canvas SDC Starterkit** — Includes Storybook integration where SDC components appear automatically without separate story files

## Common Mistakes

- **Wrong**: Expecting Canvas-specific story formats → **Right**: Code Component stories are standard Storybook; no special Canvas story format exists
- **Wrong**: Not mocking slot content in stories → **Right**: Slots arrive as React children; in stories, pass mock components or JSX as the slot arg
- **Wrong**: Stories passing the wrong prop types → **Right**: The `component.yml` is the source of truth for props; keep stories consistent with it
- **Wrong**: Running Storybook Tailwind CSS separately from the Canvas CLI build → **Right**: Ensure the Tailwind configuration in Storybook matches what the CLI builds

## See Also

- [Acquia Nebula](acquia-nebula.md) — Storybook is preconfigured there
- Drupal Storybook module: https://www.drupal.org/project/storybook
- Canvas SDC Starterkit: https://www.drupal.org/project/canvas_sdc_starterkit
- Storybook SDC addon: https://storybook.js.org/addons/storybook-addon-sdc
