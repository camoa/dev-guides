---
description: You're setting up a new Radix sub-theme
drupal_version: "11.x"
---

## 1. Radix Sub-Theme Architecture

### When to Use This Section
- You're setting up a new Radix sub-theme
- You need to understand how Radix organizes files and loads Bootstrap
- You're mapping design system files to Radix file structure

### 1.1 Sub-Theme Directory Structure

#### Decision Table: Where Files Go

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

#### Pattern: Radix Starterkit Structure

```
radix_starterkit/               # Sub-theme root
├── components/                 # SDC components directory
│   ├── button/                # Atom example
│   │   ├── button.component.yml
│   │   ├── button.twig
│   │   └── button.scss
│   ├── search-bar/            # Molecule example
│   │   ├── search-bar.component.yml
│   │   ├── search-bar.twig
│   │   └── search-bar.scss
│   └── navbar/                # Organism example
│       ├── navbar.component.yml
│       ├── navbar.twig
│       └── navbar.scss
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
│   │   └── main.script.js
│   └── assets/
│       ├── fonts/
│       └── images/
├── templates/                  # Twig template overrides
│   ├── layout/
│   ├── navigation/
│   └── content/
├── config/                     # Configuration schemas
├── THEME_NAME.info.yml         # Theme definition
├── THEME_NAME.libraries.yml    # Asset libraries
├── THEME_NAME.theme            # Theme hooks
├── package.json                # Node dependencies
└── webpack.mix.js              # Laravel Mix config
```

**Reference Source:** Radix starterkit at `~/workspace/contrib/web/themes/contrib/radix/src/kits/radix_starterkit/`

#### Common Mistakes and WHY They Matter
- **Putting SDCs in wrong location** — Must be in `components/` directory (not `src/components/`). WHY: Drupal scans for leaf directories with `.component.yml` files only in the `components/` folder; files elsewhere won't be discovered.
- **Naming mismatch** — Directory name must match component file prefix (e.g., `button/button.component.yml`). WHY: Drupal's component discovery expects this naming convention; mismatches cause "component not found" errors.
- **Missing _init.scss** — SDC SCSS files should import `_init.scss` for Bootstrap foundation. WHY: Without it, you lose access to Bootstrap variables, mixins, and functions, forcing hardcoded values.
- **Editing Radix base theme** — Always work in sub-theme, never modify Radix contrib files. WHY: Updates to Radix will overwrite your changes, and debugging becomes impossible when code doesn't match the contrib version.
- **Over-componentizing** — Not every `<div>` needs an SDC. WHY: Bootstrap utility classes (`.d-flex`, `.mb-3`) are sufficient for simple layouts; creating SDCs for trivial markup adds maintenance burden without benefit.

#### See Also
- [1.2 Bootstrap Loading Chain](#12-bootstrap-loading-chain)
- [7.1 Component YAML Schema](#71-component-yaml-schema)

---

### 1.2 Bootstrap Loading Chain

#### Pattern: How Radix Loads Bootstrap SCSS

**File: `src/scss/main.style.scss`** (Main entry point)
```scss
// Bootstrap
@import 'init';        // Loads Bootstrap foundation
@import 'bootstrap';   // Loads Bootstrap modules

// Custom stylesheets
@import "base/elements";
@import "base/functions";
@import "base/helpers";
@import "base/typography";
```

**File: `src/scss/_init.scss`** (Bootstrap foundation)
```scss
// Custom overrides FIRST
@import "base/variables";

// 1. Bootstrap functions (color/math operations)
@import "~bootstrap/scss/functions";

// 2. Default variable overrides here (already done in base/variables)

// 3. Bootstrap variables (with !default flag)
@import "~bootstrap/scss/variables";
@import "~bootstrap/scss/variables-dark";

// 4. Map overrides here

// 5. Bootstrap core
@import "~bootstrap/scss/maps";
@import "~bootstrap/scss/utilities";
@import "~bootstrap/scss/mixins";
@import "~bootstrap/scss/root";

// 6. Radix-specific additions
@import "base/mixins";
@import "base/utilities";

// 7. Bootstrap vendor utilities
@import "~bootstrap/scss/vendor/rfs";
```

**File: `src/scss/_bootstrap.scss`** (Bootstrap modules)
```scss
// Required modules
@import "init";
@import "~bootstrap/scss/utilities";
@import "~bootstrap/scss/root";
@import "~bootstrap/scss/reboot";

// Optional modules (selective imports for performance)
@import "~bootstrap/scss/type";
@import "~bootstrap/scss/images";
@import "~bootstrap/scss/containers";
@import "~bootstrap/scss/grid";
@import "~bootstrap/scss/forms";
@import "~bootstrap/scss/buttons";
// ... (see full list in Radix starterkit)

// Utilities API (must be last)
@import "~bootstrap/scss/utilities/api";
```

#### Decision Table: Import Order Logic

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

**CRITICAL:** Variables must be set BEFORE Bootstrap imports them. Bootstrap uses `!default` flag — your values take precedence ONLY if defined first.

#### Common Mistakes and WHY They Matter
- **Importing Bootstrap before variables** — Variables must come FIRST. WHY: Bootstrap uses the `!default` flag, meaning "only set this if not already set." If Bootstrap loads first, your variables come too late and are ignored.
- **Not importing functions first** — Functions needed for color operations. WHY: If you use `color-contrast()`, `shade-color()`, or `tint-color()` in variables before functions are loaded, SCSS compilation fails.
- **Importing utilities/api too early** — Must come AFTER all customizations. WHY: The utilities API generates utility classes from your final configuration; running it early means your customizations won't be reflected in generated utilities.
- **Modifying _init.scss directly** — Override in `base/_variables.scss` instead. WHY: Radix updates will overwrite `_init.scss`, but your `_variables.scss` is safe. Separating overrides from framework code prevents loss of customizations during updates.

#### See Also
- [2.1 Variable Override Location](#21-variable-override-location)
- [2.2 SCSS Import Order](#22-scss-import-order)
- Bootstrap Mapping Guide: Section 8 (SCSS Integration Order)

---

### 1.3 Theme Configuration Files

#### Pattern: Core Configuration Files

**File: `THEME_NAME.info.yml`**
```yaml
name: My Theme
description: "Custom theme based on Radix 6.x and Bootstrap 5"
core_version_requirement: ^10.3 || ^11
type: theme
base theme: radix
starterkit: true

regions:
  navbar_branding: Navbar branding
  navbar_left: Navbar left
  navbar_right: Navbar right
  header: Header
  content: Content
  page_bottom: Page bottom
  footer: Footer

libraries:
  - THEME_NAME/style

libraries-extend:
  core/drupal.ajax:
    - THEME_NAME/drupal.ajax
  core/drupal.message:
    - THEME_NAME/drupal.message
```

**File: `THEME_NAME.libraries.yml`**
```yaml
style:
  css:
    theme:
      build/css/main.style.css: {}
  js:
    build/js/main.script.js: {}
  dependencies:
    - core/drupal
```

#### Decision Table: Configuration Purposes

| File | Purpose | Design System Mapping |
|------|---------|----------------------|
| `*.info.yml` | Theme metadata, regions, library loading | Defines where organisms/templates go (regions) |
| `*.libraries.yml` | CSS/JS asset definitions | Compiled design token SCSS and scripts |
| `*.breakpoints.yml` | Responsive breakpoints | Maps to design system breakpoint tokens |
| `*.theme` | PHP theme hooks | Custom data transformation for components |
| `package.json` | Node dependencies | Bootstrap, build tools, linting |
| `webpack.mix.js` | Build configuration | SCSS compilation, optimization |

#### Common Mistakes
- **Not declaring library dependencies** — Components won't load without proper dependencies
- **Missing regions** — Template can't place content without defined regions
- **Wrong base theme** — Must be `base theme: radix`
- **Forgetting to extend core libraries** — Drupal AJAX, dialogs need library-extend

#### See Also
- [2.3 Theme Settings Integration](#23-theme-settings-integration)
- [6.1 Page Template Structure](#61-page-template-structure)