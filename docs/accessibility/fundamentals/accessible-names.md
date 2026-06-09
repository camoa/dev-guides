---
description: Name interactive elements and landmarks so assistive technology can identify them — use native labeling mechanisms first, ARIA only as a fallback.
tldr: Use `<label for="id">` for inputs, `<caption>` for tables, `<figcaption>` for figures; prefer `aria-labelledby` over `aria-label` when visible text exists — it survives translation and never goes stale; disambiguate multiple "Read more" links with visually hidden text.
---

# Accessible Names

## When to Use

> Every interactive element and many landmarks need an accessible name so assistive technology can identify it — use native labeling mechanisms first, ARIA only when no native mechanism fits.

## Decision

| Element | Native naming mechanism | ARIA fallback |
|---|---|---|
| `<input>`, `<select>`, `<textarea>` | `<label for="id">` | `aria-labelledby` → `aria-label` |
| `<fieldset>` | `<legend>` | — |
| `<table>` | `<caption>` | — |
| `<figure>` | `<figcaption>` | — |
| Icon-only button | Visually hidden text inside button | `aria-label` on button |
| Multiple "Edit" buttons in a list | Visually hidden text per button | — |
| Landmark with multiple instances | `aria-label` on `<nav>` / `<section>` | — |

**`aria-labelledby` over `aria-label` when visible text exists:** Points to existing visible text — it never goes stale, survives translation, and reads naturally to sighted screen-reader users. `aria-label` creates a hidden name that can diverge from visible text and is invisible to translators.

## Visually Hidden Utility (authoritative CSS)

```css
/* Hides content visually but keeps it in the accessibility tree.
   :focus-within / :active opt elements out — useful for skip links. */
.visually-hidden:where(:not(:focus-within, :active)) {
  position: absolute !important;
  clip-path: inset(50%) !important;
  overflow: hidden !important;
  width: 1px !important;
  height: 1px !important;
  margin: -1px !important;
  padding: 0 !important;
  border: 0 !important;
  white-space: nowrap !important;
}
```

## Pattern

```html
<!-- Explicit label association -->
<label for="email">Email address</label>
<input type="email" id="email" autocomplete="email">

<!-- Disambiguation with visually hidden text -->
<button>
  Edit <span class="visually-hidden">Carlos Ospina</span>
</button>

<!-- aria-labelledby reusing visible heading -->
<section aria-labelledby="stats-heading">
  <h2 id="stats-heading">Monthly Statistics</h2>
</section>
```

## Common Mistakes

- **Wrong**: Using `placeholder` as a label → **Right**: Placeholder disappears on input, fails contrast requirements, and is not announced reliably by AT
- **Wrong**: Using `title` as an accessible name → **Right**: Tooltip-only; unreliable on touch devices; not announced on focus in most AT
- **Wrong**: `<nav aria-label="Primary navigation">` → **Right**: Reads "Primary navigation navigation" — omit the role name from the label
- **Wrong**: Adding `aria-label` to a plain `<div>` without a role → **Right**: Ignored; must have an implicit or explicit role
- **Wrong**: Repeating ARIA state in the accessible name → **Right**: `aria-expanded`, `aria-checked` are announced separately; "Expanded menu" as the name creates double announcement

## See Also

- [Semantic Structure](semantic-structure.md) — landmark naming
- [ARIA Usage](aria-usage.md) — when ARIA is needed
- Reference: https://www.w3.org/TR/accname-1.2/
