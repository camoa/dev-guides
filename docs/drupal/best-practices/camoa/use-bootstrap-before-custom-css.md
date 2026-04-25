---
description: Always check Bootstrap for an existing class, mixin, variable, or utility before writing custom SCSS.
drupal_version: "11.x"
tldr: Always check if Bootstrap provides a class, mixin, variable, or utility before writing custom SCSS.
---

# Use Bootstrap Before Custom CSS

**What:** Always check if Bootstrap provides a class, mixin, variable, or utility before writing custom SCSS.

**Rationale:** Bootstrap's grid, spacing utilities, and responsive mixins are tested across browsers and breakpoints, integrate with the theme's variable system, and stay consistent across the codebase. Hand-written equivalents drift from the design system, duplicate logic, and accumulate maintenance debt.

**When it applies:** Every SCSS file in a Radix/Bootstrap sub-theme. The check is mental: before writing a media query or a `padding: 1rem`, look for the Bootstrap utility, mixin, or variable that already does it.

**Example:**

```scss
// Wrong — handwritten what Bootstrap already provides
.card {
  padding: 1rem;
  margin-bottom: 1.5rem;
  @media (min-width: 768px) {
    padding: 1.5rem;
  }
}

// Right — Bootstrap utilities and mixin
.card {
  @include media-breakpoint-up(md) {
    padding: $spacer * 1.5;
  }
  padding: $spacer;
  margin-bottom: $spacer * 1.5;
}

// Or even better — utility classes on the markup itself
// <div class="card p-3 p-md-4 mb-4">
```
