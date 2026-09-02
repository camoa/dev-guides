---
description: "Auto-resize textarea, input, and select to fit content with field-sizing — replacing JavaScript scrollHeight scripts"
tldr: "Use `field-sizing: content` when you need a `<textarea>`, `<input>`, or `<select>` to automatically resize to fit its content. Use JavaScript `scrollHeight` or `ResizeObserver` when cross-browser support is required (Safari does not…"
---

# field-sizing: content — Auto-Sizing Form Controls

## When to Use

> When you need a `<textarea>`, `<input>`, or `<select>` to automatically resize to fit its content, replacing JavaScript auto-resize scripts.

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

**The `lh` unit:** Represents one line-height of the element. `3lh` = 3 lines of text. Useful for min/max constraints on auto-sizing textareas.

**Browser support:** Chrome 123+, Edge 123+, Firefox 136+. **Not supported** in Safari. Use as progressive enhancement — without support, the element uses its default fixed size.

## Common Mistakes

- Forgetting `min-height` / `min-width` — without constraints, the element collapses to zero when empty
- Not setting `max-height` on textareas — content-sized textareas can push the page layout significantly
- Using on password fields — `field-sizing: content` on `type="password"` reveals password length
- Expecting it to work on `<input type="number">` with spinners — spinner buttons add width that doesn't shrink

## See Also

- [:user-valid / :user-invalid](user-valid-invalid.md) → for validation styling on auto-sized fields
- Reference: [MDN: field-sizing](https://developer.mozilla.org/en-US/docs/Web/CSS/field-sizing)
