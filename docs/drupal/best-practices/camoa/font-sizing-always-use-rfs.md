---
description: Never set font-size directly on headings or body text — always use Bootstrap's @include font-size() mixin for RFS scaling.
drupal_version: "11.x"
tldr: Never set `font-size:` directly on headings or body text. Use Bootstrap's `@include font-size()` mixin which handles responsive scaling via RFS (Responsive Font Sizes).
---

# Font Sizing — Always Use RFS

**What:** Never set `font-size:` directly on headings or body text. Use Bootstrap's `@include font-size()` mixin which handles responsive scaling via RFS (Responsive Font Sizes).

**Rationale:** RFS automatically scales font sizes based on viewport width using a calculation that maintains readability at all screen sizes. Direct `font-size` (even with `clamp()` or scoped breakpoint overrides) bypasses the system, breaks consistency with Bootstrap's own headings, and forces every component to reinvent responsive scaling.

**When it applies:** Every text-bearing rule in the theme. Headings, body copy, buttons, form labels, captions, badges — anything visible to users.

**Example:**

```scss
// Wrong — bypasses RFS
font-size: 2.125rem;
font-size: $h2-font-size;
font-size: clamp(1.75rem, 1.5rem + 0.83vw, 2.125rem);

// Right — uses RFS
@include font-size($h2-font-size);
@include font-size($font-size-base);
@include font-size(1.5rem);  // raw value also OK as input to the mixin
```
