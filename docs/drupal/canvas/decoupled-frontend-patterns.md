---
description: Patterns for using Canvas with a decoupled JavaScript frontend (Next.js, Astro, Nuxt) — component tree API, CLI sync, canvas_extjs, and Lupus Decoupled.
drupal_version: "11.x"
---

# Decoupled Frontend Patterns

## When to Use

> Use this when your project needs a fully decoupled JavaScript frontend (Next.js, Astro, Nuxt) that renders content managed by Drupal Canvas. This is an advanced pattern — most Canvas projects do NOT need this.

## Decision

| Pattern | Approach | Use when |
|---|---|---|
| Canvas → External Renderer (headless SSR) | CLI pull + JSON:API component tree | Drupal manages pages; external framework renders |
| External Components → Canvas (canvas_extjs) | Register external JS components in Canvas | Existing Vue/Nuxt components need Canvas placement |
| Server-Side Rendering via Node.js | Experimental (2026 roadmap) | Check Canvas release notes for current status |

## Pattern

Canvas stores its page layout as a **component tree** — a structured JSON field on the `canvas_page` entity.

**Architecture:**

```
Drupal Canvas             External Frontend
──────────────            ────────────────
canvas_page entity   →    fetch component tree via API
  component_tree field     identify components + props
  references Config        import same Code Components
  entities               → render with Astro/Nuxt/Next.js
                          → SSR output to browser
```

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

**Key tools:**

| Tool | Role |
|---|---|
| `@drupal-canvas/cli push/pull` | Keeps Code Components in sync between Drupal and the external codebase |
| `canvas_extjs` module | Registers external JS components (Vue, Nuxt, etc.) as Canvas components |
| Lupus Decoupled (`lupus_decoupled`) | Nuxt + Custom Elements decoupled approach with Canvas integration in v1.4+ |

**Limitations:**
- No official headless SDK as of early 2026 — patterns are community-documented
- SSR via Node.js is experimental — evaluate stability before production use
- `canvas_extjs` is a contrib module — evaluate stability before production use
- Component sync drift between Drupal and frontend is a real operational risk

## Common Mistakes

- **Wrong**: Using decoupled Canvas for a standard marketing site → **Right**: Not worth the complexity for most projects; use standard Canvas
- **Wrong**: Not setting up a sync workflow (CLI pull in CI/CD) → **Right**: Code Components drift between Drupal and frontend without automated sync
- **Wrong**: Expecting canvas_extjs to provide two-way editing → **Right**: Editors can place external components but the Canvas UI cannot edit their props the same way as Code Components
- **Wrong**: Skipping the Balint Kleri blog post → **Right**: It is the most comprehensive technical treatment of decoupled Canvas patterns

## See Also

- Balint Kleri's decoupled Canvas blog post: https://balintbrews.com/blog/drupal-canvas-decoupled/
- DrupalCon Vienna 2025 demo repo: https://github.com/balintbrews/drupalcon-vienna-2025-canvas-js-frontend
- canvas_extjs module: https://www.drupal.org/project/canvas_extjs
- Lupus Decoupled: https://www.drupal.org/project/lupus_decoupled
- Drupal.org Decoupled Canvas docs: https://www.drupal.org/docs/develop/decoupled-drupal/decoupled-drupal-canvas
