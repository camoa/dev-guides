---
description: Layout Builder style plugins must apply to the section or block wrapper only — they must not cascade into component-specific elements.
drupal_version: "11.x"
tldr: Layout Builder style plugins should apply to the section or block wrapper level. They should not cascade into component-specific elements. Use specificity guards when needed.
---

# LB Styles Must Not Override Component Internals

**What:** Layout Builder style plugins should apply to the section or block wrapper level. They should not cascade into component-specific elements. Use specificity guards when needed.

**Rationale:** LB Styles are editor-controlled — content editors apply them via the Layout Builder UI without touching code. If a style cascades into a component's internals (button colors, heading sizes, internal padding), editors can break the component contract by accident. Components should remain self-contained; styles should affect placement, spacing, background, alignment — not internal rendering.

**When it applies:** Every LB Styles definition. The styles you write determine what editors can do; design them so misuse is impossible or harmless.

**Example:**

```scss
// Wrong — LB Style cascades into component internals
.lb-style-callout {
  background: $primary;
  .btn { background: white; }       // breaks button variants
  h2 { font-size: 3rem; }            // breaks RFS scaling
  .card-body { padding: 0; }          // breaks card layout
}

// Right — LB Style affects only the wrapper
.lb-style-callout {
  background: $primary;
  padding: $spacer * 2;
  border-radius: $border-radius-lg;
  // No descendant overrides — component renders as designed
}
```
