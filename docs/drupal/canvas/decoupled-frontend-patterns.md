---
description: "Patterns for using Canvas with a decoupled JavaScript frontend (Next.js, Astro, Nuxt) — component tree API, CLI sync, canvas_extjs, and Lupus Decoupled."
tldr: "Use this when your project needs a fully decoupled JavaScript frontend (Next.js, Astro, Nuxt) that renders content managed by Drupal Canvas. This is an advanced pattern — most Canvas projects do NOT need this."
drupal_version: "11.x"
---

# Decoupled Frontend Patterns

## When to Use

> Your project needs a fully decoupled JavaScript frontend (Next.js, Astro, Nuxt) that renders content managed by Drupal Canvas, OR you want to use Canvas-managed components in a headless architecture. This is an advanced pattern — most Canvas projects do NOT need this.

## Decision

| Pattern | Approach | Use when |
|---|---|---|
| Canvas → External Renderer (headless SSR) | CLI pull + JSON:API component tree | Drupal manages pages; external framework renders |
| External Components → Canvas (canvas_extjs) | Register external JS components in Canvas | Existing Vue/Nuxt components need Canvas placement |
| Server-Side Rendering via Node.js | Experimental (2026 roadmap) | Check Canvas release notes for current status |

## Architecture

Canvas stores its page layout as a **component tree** — a structured JSON field on the `canvas_page` entity. In a decoupled setup:

1. **Drupal exposes the component tree** via JSON:API or a custom endpoint
2. **The frontend fetches the component tree** as structured data
3. **The frontend traverses the tree**, identifies which Code Components are used and with what props
4. **The same Code Components** (synced via CLI from Drupal to the frontend codebase) are used to render the output
5. **Server-side rendering** is handled by the frontend framework (Astro, Nuxt, Next.js)

```
Drupal Canvas             External Frontend
──────────────            ────────────────
canvas_page entity   →    fetch component tree via API
  component_tree field     identify components + props
  references Config        import same Code Components
  entities               → render with Astro/Nuxt/Next.js
                          → SSR output to browser
```

## Tools for Decoupled Canvas

**@drupal-canvas/cli push/pull** — Keeps Code Components in sync between Drupal and the external codebase. After pull, the Code Component files exist in both places and can be imported by the frontend.

**canvas_extjs module** (`drupal.org/project/canvas_extjs`) — Allows external JavaScript components (Vue, Nuxt, etc.) to be registered as available components in Canvas. This is the reverse direction: your external framework components become available in Canvas without being authored as Code Components inside Drupal.

**Lupus Decoupled** (`drupal.org/project/lupus_decoupled`) — A broader decoupled Drupal approach (Nuxt + Custom Elements) that has Canvas integration in version 1.4+. Provides Nuxt Component Preview capability with automatically extracted Vue.js component metadata for Canvas.

## Patterns

**Pattern A: Canvas → External Renderer (headless SSR)**
```
Drupal Canvas manages pages
  ↓ JSON:API exposes canvas_page component tree
Astro/Nuxt fetches tree
  ↓ Imports Code Components from local codebase (synced via CLI pull)
Renders to HTML at build time or SSR
```

**Pattern B: External Components → Canvas (canvas_extjs)**
```
Build Vue/Nuxt/React components independently
  ↓ Register with canvas_extjs
Canvas editor sees them as available components
  ↓ Editors place them on Canvas pages
External app renders them (client-side or SSR)
```

**Pattern C: Server-Side Rendering (experimental)**
Node.js API for SSR of Canvas component trees is on the roadmap for 2026 — experimental support exists but is not stable as of early 2026. Check Canvas release notes for current status.

## Limitations

- **Decoupled Canvas is complex** — It requires maintaining component sync between Drupal and the frontend; drift between the two is a real operational risk
- **No official headless SDK** as of early 2026 — patterns are community-documented, not officially supported tooling
- **SSR via Node.js** is experimental — production use requires careful evaluation
- **canvas_extjs** is a contrib module, not core Canvas — evaluate stability before production use

## Common Mistakes

- Using decoupled Canvas for a standard marketing site — not worth the complexity for most projects
- Not setting up a sync workflow (CLI pull in CI/CD) — Code Components drift between Drupal and frontend
- Expecting canvas_extjs to provide two-way editing — editors can place external components but the Canvas UI cannot edit their props the same way as Code Components
- Skipping the Balint Kleri blog post — it is the most comprehensive technical treatment of decoupled Canvas patterns: https://balintbrews.com/blog/drupal-canvas-decoupled/

## See Also

- Balint Kleri's decoupled Canvas blog post: https://balintbrews.com/blog/drupal-canvas-decoupled/
- DrupalCon Vienna 2025 demo repo: https://github.com/balintbrews/drupalcon-vienna-2025-canvas-js-frontend
- canvas_extjs module: https://www.drupal.org/project/canvas_extjs
- Lupus Decoupled: https://www.drupal.org/project/lupus_decoupled
- Drupal.org Decoupled Canvas docs: https://www.drupal.org/docs/develop/decoupled-drupal/decoupled-drupal-canvas
