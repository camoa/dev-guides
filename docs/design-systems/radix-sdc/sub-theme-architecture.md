---
description: Radix sub-theme architecture — directory structure, Bootstrap loading chain, configuration files
drupal_version: "11.x"
---

# Radix Sub-Theme Architecture

## When to Use

> Use this when setting up a new Radix sub-theme, understanding how Radix organizes files and loads Bootstrap, or mapping design system files to Radix file structure.

## Decision

| Design System Element | Radix Location | Purpose |
|----------------------|----------------|---------|
| Design token variables | `src/scss/base/_variables.scss` | Bootstrap variable overrides |
| Custom SCSS mixins | `src/scss/base/_mixins.scss` | Radix-specific mixins |
| Custom utility classes | `src/scss/base/_utilities.scss` | Extend Bootstrap utilities |
| Atom SDCs | `components/` | Single directory components |
| Molecule SDCs | `components/` | Composite components |
| Organism SDCs | `components/` | Complex section components |
| Page templates | `templates/` | Twig template overrides |
| Theme configuration | `THEME_NAME.info.yml` | Libraries, regions, settings |
| Asset libraries | `THEME_NAME.libraries.yml` | CSS/JS definitions |

## Pattern

**Radix Starterkit Structure:**

```
radix_starterkit/
├── components/                 # SDC components directory
│   ├── button/                # Atom example
│   ├── search-bar/            # Molecule example
│   └── navbar/                # Organism example
├── src/
│   ├── scss/
│   │   ├── base/
│   │   │   ├── _variables.scss    # Bootstrap overrides
│   │   │   ├── _mixins.scss       # Custom mixins
│   │   │   ├── _utilities.scss    # Custom utilities
│   │   │   ├── _typography.scss   # Typography styles
│   │   │   └── _elements.scss     # Base element styles
│   │   ├── _init.scss             # Bootstrap import chain
│   │   ├── _bootstrap.scss        # Bootstrap modules
│   │   └── main.style.scss        # Main entry point
│   ├── js/
│   └── assets/
├── templates/
├── THEME_NAME.info.yml
├── THEME_NAME.libraries.yml
├── THEME_NAME.theme
├── package.json
└── webpack.mix.js
```

**Bootstrap Loading Chain (`src/scss/_init.scss`):**

```scss
// 1. Custom overrides FIRST
@import "base/variables";

// 2. Bootstrap functions (color/math operations)
@import "~bootstrap/scss/functions";

// 3. Bootstrap variables (with !default flag)
@import "~bootstrap/scss/variables";

// 4. Bootstrap core
@import "~bootstrap/scss/maps";
@import "~bootstrap/scss/mixins";

// 5. Radix-specific additions
@import "base/mixins";
@import "base/utilities";
```

**Import Order Logic:**

| Step | Import | Why This Order |
|------|--------|----------------|
| 1 | Custom variables | Override Bootstrap defaults BEFORE Bootstrap loads them |
| 2 | Bootstrap functions | Required for color/math operations in variables |
| 3 | Bootstrap variables | Load defaults (skipped if already defined due to `!default`) |
| 4 | Bootstrap maps | Load color/spacing maps |
| 5 | Bootstrap mixins | Provide reusable SCSS functions |
| 6 | Radix mixins/utilities | Extend Bootstrap with Radix-specific patterns |
| 7 | Bootstrap modules | Load specific components (selective for performance) |
| 8 | Utilities API | Generate utility classes LAST |

## Common Mistakes

- **Wrong**: Putting SDCs in `src/components/` → **Right**: Must be in `components/` directory
- **Wrong**: Directory named `button/` with `btn.component.yml` → **Right**: File prefix must match directory name (`button/button.component.yml`)
- **Wrong**: SDC SCSS without `@import '../../src/scss/init'` → **Right**: Import `_init.scss` for Bootstrap foundation
- **Wrong**: Editing files in `themes/contrib/radix/` → **Right**: Always work in sub-theme, never modify Radix contrib files
- **Wrong**: Creating SDC for `<div class="d-flex gap-2">` → **Right**: Use Bootstrap utility classes for simple layouts
- **Wrong**: Importing Bootstrap before variables → **Right**: Variables must come FIRST (Bootstrap uses `!default` flag)
- **Wrong**: Using `!default` flag in `_variables.scss` → **Right**: Remove it (only Bootstrap uses `!default`)

## See Also

- [Design Tokens Configuration](design-tokens-configuration.md)
- [SDC Component Development](sdc-component-development.md)
- Reference: `~/workspace/contrib/web/themes/contrib/radix/src/kits/radix_starterkit/`
