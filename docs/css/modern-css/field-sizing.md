---
description: Auto-resize textarea, input, and select to fit content with field-sizing — replacing JavaScript scrollHeight scripts
drupal_version: "11.x"
---

# field-sizing: content — Auto-Sizing Form Controls

## When to Use

> Use `field-sizing: content` when you need a `<textarea>`, `<input>`, or `<select>` to automatically resize to fit its content. Use JavaScript `scrollHeight` or `ResizeObserver` when cross-browser support is required (Safari does not support `field-sizing` yet).

## Decision

| If you need... | Use... | Why |
|---|---|---|
| Textarea that grows with content | `field-sizing: content` | One CSS property replaces scrollHeight JS |
| Input width matching typed text | `field-sizing: content` on `<input>` | No JS measurement needed |
| Select width matching selected option | `field-sizing: content` on `<select>` | Adapts to longest visible option |
| Cross-browser auto-resize now | JavaScript `scrollHeight` or ResizeObserver | Safari doesn't support `field-sizing` yet |

## Pattern

```css
/* Auto-expanding textarea */
textarea {
  field-sizing: content;
  min-height: 3lh;    /* At least 3 lines */
  max-height: 10lh;   /* Cap at 10 lines */
}

/* Input that fits its content */
input[type="text"] {
  field-sizing: content;
  min-width: 10ch;    /* Minimum 10 characters wide */
  max-width: 40ch;    /* Cap at 40 characters */
}

/* Select that matches selected option width */
select {
  field-sizing: content;
}
```

The `lh` unit represents one line-height of the element. `3lh` = 3 lines of text. Useful for min/max constraints on auto-sizing textareas.

**Browser support:** Chrome 123+, Edge 123+, Firefox 136+. Not supported in Safari. Use as progressive enhancement — without support, the element uses its default fixed size.

## Common Mistakes

- **Wrong**: No `min-height` / `min-width` → **Right**: Without constraints, the element collapses to zero when empty
- **Wrong**: No `max-height` on textareas → **Right**: Content-sized textareas can push the page layout significantly without a cap
- **Wrong**: Using on password fields → **Right**: `field-sizing: content` on `type="password"` reveals password length
- **Wrong**: Expecting it to work on `<input type="number">` with spinners → **Right**: Spinner buttons add width that doesn't shrink

## See Also

- [:user-valid / :user-invalid](user-valid-invalid.md) — for validation styling on auto-sized fields
- Reference: [MDN: field-sizing](https://developer.mozilla.org/en-US/docs/Web/CSS/field-sizing)
