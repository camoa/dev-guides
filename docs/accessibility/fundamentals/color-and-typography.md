---
description: Meet WCAG contrast ratios, use relative font units for zoom support, and never convey meaning or state through color alone.
tldr: Normal text needs 4.5:1 contrast (WCAG AA), UI component boundaries need 3:1; use `rem`/`em` for font sizing (never `px`); always pair color-coded states with an icon or text label — color alone fails users with color vision deficiency.
---

# Color and Typography

## When to Use

> Apply these patterns to all UI elements. Color and typography choices must ensure all users can perceive content — meet contrast ratios, use relative units for zoom, and never rely on color alone to convey meaning or state.

## Decision: Contrast Ratios

| Content type | Minimum contrast ratio | Notes |
|---|---|---|
| Normal text (<18pt / <14pt bold) | 4.5:1 | WCAG AA |
| Large text (≥18pt / ≥14pt bold) | 3:1 | WCAG AA large text |
| UI component boundaries | 3:1 | Input borders, button outlines |
| Component state indicators | 3:1 | Checkbox checkmarks, switch thumbs, focus rings |
| Decorative / disabled | No requirement | Disabled elements are exempt |

## Decision: State and Emphasis

| Need | Correct pattern | Wrong pattern |
|---|---|---|
| Error / success state | Icon + color + text | Color alone |
| Emphasis | `<strong>` / `<em>` or font-weight | `text-transform: uppercase` |

**All-caps caveat:** `text-transform: uppercase` in CSS is acceptable for short labels but screen readers announce each letter individually in some AT.

## Decision: Typography

| Need | Pattern | Anti-pattern |
|---|---|---|
| Font sizing | `rem` / `em` | `px` (ignores user zoom) |
| Line length | `max-width: 80ch` | Unrestricted wide paragraphs |
| Text alignment | `text-align: start` (LTR and RTL) | `text-align: justify` |
| Text resize | Allow up to 200% without loss of content | Fixed-height containers that clip text |

## Pattern

```css
/* Relative sizing, capped line length, LTR/RTL alignment */
body { line-height: 1.5; text-align: start; }
article { max-width: 80ch; }
p, li, td { font-size: 1rem; }

/* Dark mode support */
:root { --bg: #ffffff; --text: #212529; }
@media (prefers-color-scheme: dark) {
  :root { --bg: #121212; --text: #f8f9fa; }
}
```

```html
<!-- State conveyed with icon + color, not color alone -->
<div class="error-msg">
  <span aria-hidden="true">&#10060;</span>
  <span>The password entered was invalid.</span>
</div>
```

## Common Mistakes

- **Wrong**: Color alone for error/success → **Right**: Fails users with color vision deficiency; also fails WCAG 1.4.1
- **Wrong**: `px` for font sizes → **Right**: Ignores OS-level text size preference; use `rem`
- **Wrong**: `text-align: justify` → **Right**: Creates uneven word spacing harder to read, especially for dyslexic users
- **Wrong**: Paragraph line length unlimited → **Right**: Lines exceeding ~80 characters increase tracking difficulty
- **Wrong**: High-contrast mode untested → **Right**: Check Windows High Contrast / Forced Colors mode; use `@media (forced-colors: active)`

## See Also

- Reference: https://www.w3.org/TR/WCAG22/#contrast-minimum (WCAG 2.2 SC 1.4.3)
- Reference: https://www.w3.org/TR/WCAG22/#non-text-contrast (WCAG 2.2 SC 1.4.11)
