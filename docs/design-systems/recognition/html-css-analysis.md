---
description: Extract design tokens and components from HTML/CSS source code
---

# HTML/CSS Analysis

## When to Use

> Use when analyzing HTML design systems or component libraries. Use when extracting design tokens from CSS custom properties or reverse-engineering a website's design system.

## Decision

| CSS Pattern | Token Type | Recognition |
|------------|-----------|-------------|
| `:root { --color-blue-500: #0052CC; }` | Reference token | Raw color value at root |
| `--color-primary: var(--color-blue-500);` | Semantic token | Token referencing token |
| `--button-bg: var(--color-primary);` | Component token | Application-specific |
| `.btn`, `.button` classes | Atom | Single element component |
| `.form-field` wrapper | Molecule | Composite component |
| `<header>`, `<footer>`, `<nav>` | Organism | Semantic HTML boundaries |
| `.theme-dark { --color-bg: black; }` | Theme variant | Dark mode tokens |

## Pattern

**CSS Custom Properties as Tokens:**

```css
:root {
  /* Layer 1: Reference tokens (primitives) */
  --color-blue-500: #0052CC;
  --font-size-base: 16px;
  --space-2: 8px;

  /* Layer 2: Semantic tokens (context) */
  --color-primary: var(--color-blue-500);
  --font-size-body: var(--font-size-base);

  /* Layer 3: Component tokens (application) */
  --button-background: var(--color-primary);
  --button-padding: var(--space-2);
}
```

**BEM Naming as Component Boundaries:**

```html
<!-- Block = Component boundary (molecule/organism) -->
<div class="card">
  <!-- Element = Child atom -->
  <h2 class="card__title">Title</h2>
  <p class="card__text">Content</p>
  <!-- Modifier = Variant state -->
  <button class="card__button card__button--primary">CTA</button>
</div>
```

Recognition rules:
- **Block** (`.card`) = Component boundary
- **Element** (`.card__title`) = Child atom
- **Modifier** (`.card__button--primary`) = Variant

**Semantic HTML as Hierarchy:**

| HTML Element | Component Type |
|--------------|---------------|
| `<button>`, `<input>`, `<label>` | Atoms |
| `<form>` with multiple inputs | Molecule/Organism |
| `<header>`, `<footer>`, `<nav>` | Organisms |
| `<section>`, `<article>` | Organisms/Templates |
| `<main>` with layout | Template |

**Dark Mode Recognition:**

```css
/* Media query approach */
@media (prefers-color-scheme: dark) {
  :root {
    --color-background: #1a1a1a;
    --color-text: #ffffff;
  }
}

/* Class-based approach */
.theme-dark {
  --color-background: #1a1a1a;
  --color-text: #ffffff;
}
```

Cues: `prefers-color-scheme`, `.theme-dark` classes, same token names with different values

## Common Mistakes

- **Wrong**: Missing token reference chains → **Right**: Track `var()` references through all layers (component → semantic → reference)
- **Wrong**: Using computed values from DevTools → **Right**: Extract source definitions from `:root`, not computed values
- **Wrong**: Utility classes as atoms → **Right**: `.mt-4`, `.text-center` are utilities, not components
- **Wrong**: Ignoring cascade specificity → **Right**: Component tokens may override global tokens; note specificity layers

## See Also

- [Design Tokens](./design-tokens.md)
- [Component Classification](./component-classification.md)
- [Figma Analysis](./figma-analysis.md)
- Reference: [CSS Variables and Design Tokens](https://penpot.app/blog/the-developers-guide-to-design-tokens-and-css-variables/)
- Reference: [W3C Design Tokens Format](https://www.designtokens.org/tr/drafts/format/)
