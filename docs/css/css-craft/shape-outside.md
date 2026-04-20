---
description: shape-outside text flow — wrap text around circular images, custom polygons, and alpha-channel image shapes
tldr: "Use `shape-outside` when a client wants the \"magazine layout\" effect — text flowing around a non-rectangular element. Requires `float`; does not work with flexbox or grid."
---

# Shape Outside & Text Flow

## When to Use

> Use `shape-outside` when a client wants the "magazine layout" effect — text flowing around a non-rectangular element. Requires `float`; does not work with flexbox or grid.

## Decision

| Client asks for... | Use... | Why |
|---|---|---|
| Text wrapping around a circular image | `shape-outside: circle()` + `float` | Text flows around the circle |
| Text wrapping around an irregular shape | `shape-outside: url(image.png)` | Uses image alpha channel |
| Text avoiding a polygon area | `shape-outside: polygon()` | Custom shape exclusion |
| Pull quote with text wrap | `shape-outside: ellipse()` + `float` | Elegant wrap around pull quote |
| Text indent from shape edge | `shape-margin` | Adds breathing room |

## Pattern

```css
/* Circular image with text wrap */
.article-image--circular {
  float: left;
  width: 200px; height: 200px;
  border-radius: 50%;
  shape-outside: circle(50%);
  shape-margin: 1rem;
  margin-right: 1.5rem;
  object-fit: cover;
}

/* Custom polygon text wrap */
.pull-quote {
  float: right;
  width: 300px;
  shape-outside: polygon(0 0, 100% 0, 100% 100%, 30% 100%);
  shape-margin: 1.5rem;
  margin-left: 2rem;
}

/* Alpha channel wrap */
.shaped-image {
  float: left;
  shape-outside: url('person-cutout.png');
  shape-image-threshold: 0.5;
  shape-margin: 12px;
}
```

## Common Mistakes

- **Forgetting `float`** — `shape-outside` has no effect without it
- **Using with flexbox/grid children** — only works on floated elements
- **Missing `shape-margin`** — text touching the shape edge looks cramped; always add spacing
- **High-res images for shape-outside URL** — use a small, low-res alpha mask; shape calculation is expensive

## See Also

- [CSS Shapes & Decorative Geometry](css-shapes.md) → clip-path for visual shapes
- Reference: [MDN: shape-outside](https://developer.mozilla.org/en-US/docs/Web/CSS/shape-outside)
