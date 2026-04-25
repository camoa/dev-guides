---
description: Use Better Exposed Filters with AJAX for filtered-view switchers — not client-side JS that hides pre-rendered content.
drupal_version: "11.x"
tldr: When users need to switch between filtered views (tabs, segmented controls, "show me X vs Y"), use Better Exposed Filters with AJAX — not client-side JS toggles that hide/show pre-rendered content.
---

# BEF + AJAX Over JS Toggles

**What:** When users need to switch between filtered views (tabs, segmented controls, "show me X vs Y"), use Better Exposed Filters with AJAX — not client-side JS toggles that hide/show pre-rendered content.

**Rationale:** Three wins, all measurable:
- **LCP**: smaller initial payload (only the active filter's content renders) → faster Largest Contentful Paint
- **SEO**: no duplicate hidden DOM content → search engines don't crawl/score variants of the same content as separate views
- **Accessibility**: BEF widgets are standard form elements with built-in ARIA → screen reader users get proper semantics; JS toggle UIs require manual ARIA wiring that's often wrong

**When it applies:** Any UI pattern where the user picks one variant from a small set: tab interfaces over Views, "All / Featured / Recent" filters, category switchers, view-mode toggles.

**Example:**

```
Wrong — render all variants, hide with JS
  <div class="tabs">
    <button data-tab="all">All</button>
    <button data-tab="featured">Featured</button>
  </div>
  <div class="content" data-tab="all">
    <!-- 50 cards rendered -->
  </div>
  <div class="content" data-tab="featured" hidden>
    <!-- 50 more cards rendered -->
  </div>

Right — Views + BEF exposed filter, AJAX-enabled
  drush en better_exposed_filters
  - Configure View with exposed filter on the variant field
  - Enable AJAX on the View display
  - BEF widget: links / radios styled as tabs
  → Only active variant's content is in the DOM
```
