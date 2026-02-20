---
description: Required and optional SDC component file structure and naming conventions
drupal_version: "11.x"
---

# Component File Structure

## When to Use

> Use this when creating a new component, debugging "component not found" errors, or understanding automatic asset loading.

## Decision

| File | Required | Auto-loaded | Purpose |
|------|----------|-------------|---------|
| `component-name.component.yml` | Yes | Always | Component metadata and schema |
| `component-name.twig` | Yes | Always | Template markup |
| `component-name.css` | No | If present | Styles (attached as library) |
| `component-name.js` | No | If present | Scripts (attached as library) |
| `README.md` | No | Never | Documentation |
| `thumbnail.png` | No | Never | Admin UI preview |
| `assets/` | No | Never | Additional assets (manual reference) |

## Pattern

**CRITICAL:** Directory name MUST match all file basenames exactly.

```
✓ CORRECT:
my-button/
├── my-button.component.yml
├── my-button.twig
├── my-button.css
└── my-button.js

✗ WRONG:
my-button/
├── button.component.yml      ← Won't be discovered
├── my_button.twig             ← Won't be discovered
```

**Automatic Library Generation:**
- Format: `core/components.{provider}--{component-name}`
- Example: `core/components.my_theme--hero-banner`
- Includes CSS/JS files named identically to component
- Loaded automatically when component renders

## Common Mistakes

- **Wrong**: Using underscores in component names → **Right**: Use hyphens (kebab-case) per Drupal conventions
- **Wrong**: Mismatched file basenames → **Right**: All files must match directory name exactly
- **Wrong**: Expecting `assets/` directory to auto-load → **Right**: Only root-level `.css` and `.js` files auto-attach

## See Also

- Reference: `/core/themes/olivero/components/teaser/` - Reference implementation
- Reference: `/themes/contrib/radix/components/button/` - Radix button example
- [SCSS/CSS in SDCs](scss-css-in-sdcs.md)
- [JavaScript in SDCs](javascript-in-sdcs.md)
