---
description: Required and optional files in SDC directory structure with automatic asset loading
drupal_version: "11.x"
---

# Component File Structure

## When to Use

> Use this when creating a new component, debugging "component not found" errors, or understanding automatic asset loading.

## Decision: Required vs Optional Files

| File Type | Status | Purpose |
|-----------|--------|---------|
| `component-name.component.yml` | Required | Metadata and schema |
| `component-name.twig` | Required | Template |
| `component-name.css` | Optional | Styles (auto-attached as library) |
| `component-name.js` | Optional | Scripts (auto-attached as library) |
| `README.md` | Optional | Documentation |
| `thumbnail.png` | Optional | Preview for admin UI |
| `assets/` | Optional | Additional assets (must reference manually) |

**CRITICAL**: Directory name MUST match all file basenames exactly. Drupal's discovery system matches files by directory name. Mismatched names result in "component not found" errors.

## Pattern

Correct file naming:

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

Automatic library generation:
- Format: `core/components.{provider}--{component-name}`
- Example: `core/components.my_theme--hero-banner`
- Includes CSS/JS files named identically to component
- Loaded automatically when component renders

## Common Mistakes

- **Wrong**: Using underscores in component names → **Right**: Component names should use hyphens (kebab-case) per Drupal conventions. Underscores in provider names are converted to hyphens in library names.

## See Also

- Reference: `/core/themes/olivero/components/teaser/` - Reference implementation
- Reference: `/themes/contrib/radix/components/button/` - Radix button example
- [SCSS/CSS in SDCs](scss-css-in-sdcs.md)
- [JavaScript in SDCs](javascript-in-sdcs.md)
