---
description: You're setting up a new Radix sub-theme
drupal_version: "11.x"
---

## 3.6 Radix Sub-Theme Best Practices

### When to Use This Section
- You're setting up a new Radix sub-theme
- You need to understand override strategy (when to override vs extend vs create)
- You're managing SCSS variables and compilation
- You want guidance on starterkit usage and library management

### Why Extend Radix Instead of Starting from Scratch

**CRITICAL PRINCIPLE:** Never use Radix directly as your theme. Always create a sub-theme.

**WHY USE RADIX AS BASE:**

1. **Bootstrap 5 Integration Built-In**
   - Radix handles Bootstrap compilation with proper import order
   - SCSS structure follows Bootstrap best practices
   - Updates to Bootstrap are managed by Radix maintainers

2. **57 Pre-Built SDC Components**
   - Atoms: buttons, inputs, badges, headings, images
   - Molecules: forms, dropdowns, lists, navigation items
   - Organisms: navbars, cards, accordions, modals, carousels
   - Drupal integration: blocks, nodes, fields, views, regions

3. **Mobile-First, Responsive by Default**
   - Uses Bootstrap's responsive grid and breakpoints
   - Components include responsive behavior

4. **Active Maintenance and Community**
   - Compatible with Drupal 10.3+ and 11+
   - Regular updates for Bootstrap and Drupal core changes

5. **Build Tools Included**
   - Laravel Mix configuration for SCSS/JS compilation
   - Development (watch) and production (minified) build modes
   - Source maps for debugging

**WHAT YOU GET BY EXTENDING:**
- Update Radix via Composer without losing customizations
- Inherit improvements and security patches
- Stand on shoulders of Bootstrap + Drupal community patterns

**COMPARISON:**

| Starting from Scratch | Extending Radix |
|-----------------------|-----------------|
| Build Bootstrap integration yourself | Bootstrap integration ready |
| Create all components from zero | 57 components ready to use/override |
| Figure out Drupal template integration | Templates integrated with core/contrib |
| Set up build tools | Laravel Mix configured |
| Implement responsive patterns | Responsive patterns built-in |
| **Time: Weeks/months** | **Time: Days** |

### Override Strategy: When to Override vs Extend vs Create

#### Decision Framework

**1. REUSE AS-IS** (Best option)

```twig
{# Just use Radix component directly #}
{% include 'radix:button' with {
  color: 'primary',
  content: 'Click me',
} %}
```

**WHEN:** Component meets needs exactly or you only need to pass different props.

**WHY:** Zero maintenance burden, automatic updates from Radix.

---

**2. EXTEND** (Second best option)

```twig
{# Wrap Radix component with custom markup #}
<div class="custom-button-wrapper">
  {% include 'radix:button' with {
    color: 'primary',
    content: 'Click me',
  } %}
  <span class="tooltip">Click to submit</span>
</div>
```

**Or add custom SCSS:**

```scss
// src/scss/components/_custom-buttons.scss
@import '../init';

// Extend Radix button styles
.btn-brand {
  @include button-variant(
    $background: $brand-color,
    $border: $brand-color,
    $color: color-contrast($brand-color)
  );
}
```

**WHEN:**
- Need additional wrapper markup
- Need custom color variant not in Bootstrap
- Need to add functionality without changing structure

**WHY:** Still leverages Radix base, updates won't break you, minimal maintenance.

---

**3. OVERRIDE** (Third option — use sparingly)

**Process:**
1. Copy component directory from Radix to sub-theme:
   ```bash
   cp -r ~/workspace/contrib/web/themes/contrib/radix/components/button \
         themes/custom/THEME_NAME/components/button
   ```

2. Modify files in your sub-theme copy

3. Drupal automatically uses your version (component discovery order: sub-theme → base theme)

**WHEN:**
- Need major structural changes to Twig template
- Need to change component's props/slots schema
- Need completely different markup from Radix version

**WHY OVERRIDE SPARINGLY:**
- **You own maintenance** — Radix updates won't reach your override
- **Security patches** — You won't get fixes automatically
- **Upgrade burden** — Each Drupal/Bootstrap major version requires manual review
- **Divergence risk** — Your version may become incompatible with future Radix patterns

**BEST PRACTICE AFTER OVERRIDE:**
- Document WHY you overrode (comment in `.component.yml`)
- Note the original Radix version you copied from
- Periodically check if Radix made improvements you should merge

---

**4. CREATE NEW** (When necessary)

```bash
# Use drupal-radix-cli to generate new component
drupal-radix add my-custom-component
```

**WHEN:**
- Component doesn't exist in Radix 57-component catalog
- Design system has unique patterns not in Bootstrap
- Project-specific functionality

**WHY:** Some patterns are project-specific and wouldn't make sense in Radix base theme.

---

### Variable Override Location Best Practices

#### CRITICAL RULE: Override in base/_variables.scss

**File:** `src/scss/base/_variables.scss`

```scss
/**
 * Variables
 * Variables should follow the $component-state-property-size formula for
 * consistent naming. Examples:
 * $nav-link-disabled-color
 * $modal-content-box-shadow-xs
 *
 * Customization:
 * To customize Bootstrap variables:
 * Copy the desired variable from node_modules/bootstrap/scss/_variables.scss
 * @see https://github.com/twbs/bootstrap/blob/main/scss/_variables.scss
 * Change the value and remove the !default flag.
 */

// Color system
$primary: #194582;
$secondary: #6c757d;

// Typography
$font-family-base: system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
$font-size-base: 1rem;
$line-height-base: 1.5;

// Spacing
$spacer: 1rem;

// Borders
$border-radius: 0.375rem;
```

**WHY THIS LOCATION:**
1. **Imported before Bootstrap** — `_init.scss` imports `_variables.scss` before Bootstrap's `_variables.scss`
2. **Override mechanism** — Bootstrap uses `!default` flag (only sets if not already set)
3. **Survives Radix updates** — Radix won't overwrite your `src/scss/base/_variables.scss`
4. **Centralized customization** — All variable overrides in one place

**COMMON MISTAKE: Editing _init.scss**

```scss
// BAD: Don't modify _init.scss directly
// File: src/scss/_init.scss
$primary: #194582;  // NO! This file may be updated by Radix
```

**WHY BAD:** Radix updates may replace `_init.scss`, losing your changes.

**INSTEAD:** Put overrides in `_variables.scss` which is imported by `_init.scss`.

---

### Starterkit Usage: What to Keep, Customize, Delete

#### When Generating Sub-Theme from Starterkit

**KEEP THESE FILES AS-IS (DON'T MODIFY):**
- `src/scss/_init.scss` — Bootstrap import chain (Radix manages this)
- `src/scss/_bootstrap.scss` — Bootstrap module imports (update only if you want to exclude modules)
- `package.json` — Node dependencies (update versions as needed)
- `webpack.mix.js` — Build configuration (modify only if changing build process)

**CUSTOMIZE THESE FILES:**
- `src/scss/base/_variables.scss` — Your design token overrides (PRIMARY CUSTOMIZATION FILE)
- `src/scss/base/_mixins.scss` — Your custom mixins
- `src/scss/base/_utilities.scss` — Your custom utility classes
- `src/scss/base/_elements.scss` — Global element styles (h1, p, a, etc.)
- `src/scss/base/_typography.scss` — Typography-specific styles
- `THEME_NAME.info.yml` — Regions, libraries, theme metadata
- `THEME_NAME.libraries.yml` — Your asset libraries
- `THEME_NAME.theme` — Preprocess functions, theme hooks

**DELETE OR KEEP MINIMAL:**
- `components/` directory — Delete starterkit examples, add your own components
- `templates/` directory — Only add templates you're actually overriding
- `README.md` — Replace with project-specific documentation

**WHY:** Keeping unnecessary files adds maintenance burden and confusion.

---

### Library Management Best Practices

#### When to Add Libraries vs Using Global

**GLOBAL LIBRARIES** (in `THEME_NAME.info.yml`):

```yaml
libraries:
  - THEME_NAME/style
  - THEME_NAME/script
```

**WHEN TO USE GLOBAL:**
- Site-wide styles (main.style.css)
- Site-wide JavaScript (main.script.js)
- Universal dependencies (Drupal core libraries)

**WHY:** Loaded on every page, always available.

**RISK:** Performance — loading unnecessary CSS/JS on every page.

---

**COMPONENT-SPECIFIC LIBRARIES** (auto-loaded with SDC):

```
components/hero-section/
├── hero-section.component.yml
├── hero-section.twig
├── hero-section.scss  # Auto-loaded when component renders
├── hero-section.js    # Auto-loaded when component renders
```

**WHEN TO USE:**
- Styles specific to one component
- JavaScript for one component
- Loaded only when component is actually rendered

**WHY:** Performance — CSS/JS only loads when component is used.

---

**TEMPLATE-SPECIFIC LIBRARIES** (in Twig):

```twig
{# templates/node--article.html.twig #}
{{ attach_library('THEME_NAME/article-specific') }}

<article{{ attributes }}>
  {# Article markup #}
</article>
```

**WHEN TO USE:**
- Styles for specific content type
- JavaScript for specific page type
- Not used site-wide

**WHY:** Performance — only loads on relevant pages.

---

#### Library Dependencies and Weight

**MODERN DRUPAL (2025): Use Dependencies, Not Weight**

```yaml
# THEME_NAME.libraries.yml

# GOOD: Use dependencies
custom-component:
  css:
    theme:
      css/custom-component.css: {}
  dependencies:
    - core/drupal
    - core/jquery
```

**WHY:**
- **Dependency resolution** — Drupal loads dependencies in correct order automatically
- **Maintainable** — Clear which libraries are required
- **Future-proof** — Drupal core moved away from weight-based ordering in 2024-2025

**OLD APPROACH (Deprecated):**

```yaml
# BAD: Using weight (deprecated in recent Drupal)
custom-component:
  css:
    theme:
      css/custom-component.css:
        weight: 100  # Avoid this
```

**WHY BAD:** Weight-based ordering is being phased out; dependency-based ordering is now standard.

---

### Development Workflow Best Practices

#### SCSS Compilation Modes

**DEVELOPMENT MODE:**

```bash
npm run watch
```

**WHAT IT DOES:**
- Compiles SCSS to CSS with source maps
- Watches for file changes and recompiles automatically
- Non-minified output for debugging

**WHEN TO USE:**
- Active theme development
- Debugging CSS issues
- Need to see which SCSS file generated which CSS line

---

**PRODUCTION MODE:**

```bash
npm run production
```

**WHAT IT DOES:**
- Compiles and minifies CSS
- Removes source maps
- Optimizes for performance

**WHEN TO USE:**
- Before committing to git
- Deploying to staging/production
- Final build before site launch

**BEST PRACTICE:**
- Develop in watch mode: `npm run watch`
- Build production before commit: `npm run production`
- Add `node_modules/` and uncompiled files to `.gitignore`
- Commit only production-built CSS/JS

---

### Common Mistakes Senior Themers Catch in Code Review

**1. Installing npm dependencies in Radix base theme**

```bash
# BAD: Don't do this
cd themes/contrib/radix
npm install
```

**WHY BAD:** Base theme isn't meant to be modified. Updates overwrite changes.

**CORRECT:**

```bash
# GOOD: Install in your sub-theme
cd themes/custom/THEME_NAME
npm install
```

---

**2. Not compiling before committing**

```bash
# BAD: Committing with only SCSS changes
git add src/scss/base/_variables.scss
git commit
```

**WHY BAD:** Uncompiled SCSS doesn't affect site. Production needs compiled CSS.

**CORRECT:**

```bash
# GOOD: Compile production, then commit
npm run production
git add src/scss/base/_variables.scss
git add build/css/main.style.css
git commit
```

---

**3. Overriding Radix component unnecessarily**

```bash
# BAD: Copying entire navbar component just to change one color
cp -r radix/components/navbar themes/custom/THEME_NAME/components/navbar
```

**WHY BAD:** Now you own maintenance, lose updates, increase upgrade burden.

**CORRECT:**

```scss
// GOOD: Extend with custom SCSS
// src/scss/components/_navbar.scss
.navbar {
  &.navbar-custom {
    background-color: $brand-color;
  }
}
```

---

**4. Not using drupal-radix-cli**

```bash
# TEDIOUS: Manually creating all component files
mkdir components/my-component
touch components/my-component/my-component.component.yml
touch components/my-component/my-component.twig
# ... etc
```

**CORRECT:**

```bash
# EFFICIENT: Use CLI
drupal-radix add my-component
```

**WHY:** CLI creates proper structure, follows conventions, saves time.

---

**5. Modifying Radix's _init.scss**

```scss
// BAD: Editing src/scss/_init.scss
@import "base/variables";
$custom-color: #ff6600;  // Adding custom variables here
```

**WHY BAD:** Radix may update `_init.scss`, overwriting your changes.

**CORRECT:**

```scss
// GOOD: Add to base/_variables.scss
$custom-color: #ff6600;
```

#### See Also
- [1.1 Sub-Theme Directory Structure](#11-sub-theme-directory-structure)
- [2.1 Variable Override Location](#21-variable-override-location)
- [8.2 Reuse Decision Framework](#82-reuse-decision-framework)
- [8.3 Overriding Radix Components](#83-overriding-radix-components)