---
description: CSS field-sizing:content for auto-growing inputs, textareas, and selects that fit their content without JavaScript scrollHeight scripts.
tldr: Use field-sizing:content as progressive enhancement — Chrome/Edge 123+, Safari 26.2+, not Firefox. Set min-inline-size on inputs (prevents zero-width collapse when empty) and fixed width on textareas (prevents jarring horizontal shift). Override width:100% global CSS with width:auto. Feature-detect with @supports.
drupal_version: ""
---

# Field Sizing

## When to Use

> Use `field-sizing: content` when inputs, textareas, or selects should automatically grow or shrink to fit their content, replacing JavaScript `scrollHeight` resize scripts. Treat as progressive enhancement — browsers without support degrade to standard fixed-size controls.

## Decision

| Need | Pattern | Notes |
|------|---------|-------|
| Textarea grows with typing | `field-sizing: content` + `min-block-size` | Fix horizontal width to prevent jarring shifts |
| Input width matches typed text | `field-sizing: content` + `min-inline-size` | Prevents collapsing to zero when empty |
| Select width matches selected option | `field-sizing: content` + `max-inline-size` | Prevents long options breaking layout |
| Cross-browser auto-grow today | JS `scrollHeight` pattern | CSS Grid textarea fallback for Firefox |

**Baseline status: Limited availability.** Chrome 123+, Edge 123+, Safari 26.2+. Not supported in Firefox.

## Pattern

```css
@supports (field-sizing: content) {
  input {
    field-sizing: content;
    width: auto;           /* Reset if global CSS sets width: 100% */
    min-inline-size: 15ch; /* Prevents collapse when empty */
    max-inline-size: 50ch;
  }

  textarea {
    field-sizing: content;
    height: auto;          /* Reset if global CSS sets fixed height */
    width: 100%;           /* Fixed width prevents jarring horizontal shift */
    min-block-size: 3lh;   /* At least 3 lines when empty */
    max-block-size: 10lh;  /* Cap; scrolls after this height */
  }

  select {
    field-sizing: content;
    max-inline-size: 50ch;
  }
}
```

**Layout override rules:**
- **`width: 100%` in global CSS overrides `field-sizing: content`** — explicitly reset to `width: auto`.
- **Grid and Flexbox stretch children** — if a field-sized input refuses to shrink, apply `align-self: start` or `justify-self: start`.
- Wrap in `@supports (field-sizing: content) { … }` to isolate from unsupported browsers.

## Common Mistakes

- **Missing `min-inline-size` on inputs** → input collapses to zero width when empty; becomes unclickable
- **Allowing horizontal `field-sizing` on textarea** → jarring width jump when a long placeholder is replaced by typed content
- **No `max-block-size` on textarea** → textarea grows infinitely; breaks page layout
- **`field-sizing` inside flex/grid without `align-self: start`** → container stretching overrides the content sizing

## See Also

- [field-sizing: content](../../css/modern-css/field-sizing.md) — full CSS coverage, CSS Grid fallback for Firefox
- Reference: MWG `form-fields-automatically-fit-contents.md`
