---
description: Never use the > child combinator in selectors targeting Layout Builder content — nesting depth changes when editors rearrange blocks.
drupal_version: "11.x"
tldr: Layout Builder wraps blocks in variable-depth divs. Never use `>` in selectors that target Layout Builder content — the nesting depth changes when editors rearrange blocks.
---

# No Direct Child Selectors with Layout Builder

**What:** Layout Builder wraps blocks in variable-depth divs. Never use `>` in selectors that target Layout Builder content — the nesting depth changes when editors rearrange blocks.

**Rationale:** Editors rearrange sections, change layouts (1 column → 2 column), nest blocks inside layout blocks (LB+ feature). Each rearrangement adds or removes wrapper divs. A `>` selector that worked in a 1-column layout silently fails when the editor moves the block to a 2-column layout.

**When it applies:** Any selector whose right-hand side targets content rendered through Layout Builder — block labels, field content, inline-block bodies, layout block children.

**Example:**

```scss
// Wrong — breaks when LB adds wrapper divs
.section-heading > .field {
  padding-left: 1rem;
}

// Right — works at any nesting depth
.section-heading .field {
  padding-left: 1rem;
}

// If specificity matters, use other strategies:
//   - BEM modifier classes on the leaf element
//   - :is() / :where() with a depth-agnostic ancestor
//   - SDC scope + minimal classes inside the component
```
