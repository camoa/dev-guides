---
description: Use Bootstrap's media-breakpoint-up() for desktop overrides — define mobile as the base and layer up with a consistent stacking breakpoint.
drupal_version: "11.x"
tldr: Use Bootstrap's `media-breakpoint-up()` for desktop overrides. Define mobile as the base, layer up. Pick the project's stacking breakpoint intentionally and apply it consistently across all components.
---

# Mobile-First Breakpoints

**What:** Use Bootstrap's `media-breakpoint-up()` for desktop overrides. Define mobile as the base, layer up. Pick the project's stacking breakpoint intentionally and apply it consistently across all components.

**Rationale:** Mobile-first writes shorter selectors at the base case (no media query) and progressively enhances. `media-breakpoint-down()` and inverted approaches require duplicating defaults, complicate cascade reasoning, and tend to produce more CSS. Picking a stacking breakpoint up front (typically `md` or `lg`) keeps component behavior predictable site-wide.

**When it applies:** Every responsive rule in the theme. The project should have a documented stacking breakpoint (e.g., "components stack below `lg`"); all components honor it.

**Example:**

```scss
// Wrong — desktop-first with downward overrides
.nav-list {
  display: flex;
  gap: 2rem;
  @include media-breakpoint-down(md) {
    flex-direction: column;
    gap: 1rem;
  }
}

// Right — mobile-first with upward overrides
.nav-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  @include media-breakpoint-up(lg) {
    flex-direction: row;
    gap: 2rem;
  }
}
```
