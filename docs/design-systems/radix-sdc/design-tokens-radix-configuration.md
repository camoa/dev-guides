---
description: You've identified design tokens using the Design System Recognition Guide
drupal_version: "11.x"
---

## 2. Design Tokens → Radix Configuration

### When to Use This Section
- You've identified design tokens using the Design System Recognition Guide
- You've mapped tokens to Bootstrap variables using the Bootstrap Mapping Guide
- You need to know WHERE to put variable overrides in Radix

### 2.1 Variable Override Location

#### Decision Table: Token Category → File Location

| Token Category | Bootstrap Variable | Radix Override Location | Implementation |
|----------------|-------------------|------------------------|----------------|
| Colors | `$primary`, `$theme-colors` | `src/scss/base/_variables.scss` | Set before Bootstrap import |
| Typography | `$font-family-base`, `$h1-font-size` | `src/scss/base/_variables.scss` | Set before Bootstrap import |
| Spacing | `$spacer`, `$spacers` map | `src/scss/base/_variables.scss` | Override or extend map |
| Borders/Radius | `$border-radius`, `$box-shadow` | `src/scss/base/_variables.scss` | Set before Bootstrap import |
| Breakpoints | `$grid-breakpoints` | `src/scss/base/_variables.scss` | Override entire map |
| Custom utilities | N/A | `src/scss/base/_utilities.scss` | Use Bootstrap utilities API |

#### Pattern: Variable Override File

**File: `src/scss/base/_variables.scss`**
```scss
/**
 * Variables
 *
 * Customization:
 * Copy desired variable from node_modules/bootstrap/scss/_variables.scss
 * Change the value and remove the !default flag
 *
 * Examples:
 * $primary: #194582;
 * $body-color: #141414;
 */

// Color tokens
$primary: #194582;
$secondary: #6c757d;

// Typography tokens
$font-family-base: system-ui, -apple-system, "Segoe UI", sans-serif;
$font-size-base: 1rem;
$line-height-base: 1.5;

// Spacing tokens
// Use Bootstrap defaults or override:
// $spacer: 1rem;
// $spacers: (
//   0: 0,
//   1: $spacer * 0.25,
//   2: $spacer * 0.5,
//   // ...
// );

// Border/radius tokens
$border-radius: 0.375rem;
$border-radius-sm: 0.25rem;
$border-radius-lg: 0.5rem;

// Shadow tokens
$box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
$box-shadow-sm: 0 0.0625rem 0.125rem rgba(0, 0, 0, 0.075);
$box-shadow-lg: 0 1rem 3rem rgba(0, 0, 0, 0.175);
```

**CRITICAL:** This file is imported BEFORE Bootstrap in `_init.scss`, so variables override Bootstrap defaults.

#### Common Mistakes
- **Setting variables after Bootstrap import** — Must be BEFORE
- **Using `!default` flag** — Remove it (only Bootstrap uses `!default`)
- **Hardcoding values in components** — Use variables for consistency
- **Not referencing Bootstrap Mapping Guide** — Defer to that guide for WHICH variables to set

#### See Also
- Bootstrap Mapping Guide: Section 2 (Design Tokens → Bootstrap Variables)
- [2.2 SCSS Import Order](#22-scss-import-order)
- [1.2 Bootstrap Loading Chain](#12-bootstrap-loading-chain)

---

### 2.2 SCSS Import Order

#### Pattern: Complete Import Chain

**Refer to Section 1.2 for full import chain details.**

**Key Principle:** Custom variables → Bootstrap functions → Bootstrap variables → Bootstrap core → Radix additions → Bootstrap modules → Utilities API

#### Decision Table: What Goes Where

| Customization Type | Location | Imported By |
|-------------------|----------|-------------|
| Bootstrap variable overrides | `base/_variables.scss` | `_init.scss` (step 1) |
| Custom SCSS mixins | `base/_mixins.scss` | `_init.scss` (step 6) |
| Custom utility extensions | `base/_utilities.scss` | `_init.scss` (step 6) |
| Custom element styles | `base/_elements.scss` | `main.style.scss` (after Bootstrap) |
| Custom typography | `base/_typography.scss` | `main.style.scss` (after Bootstrap) |
| SDC component SCSS | `components/*/COMPONENT.scss` | Auto-loaded by SDC system |

#### Common Mistakes
- **Importing variables after Bootstrap** — Bootstrap won't see your overrides
- **Not importing _init.scss in SDCs** — SDC SCSS needs Bootstrap foundation
- **Modifying _init.scss for every change** — Override in specific files instead
- **Circular imports** — Avoid files importing each other

#### See Also
- Bootstrap Mapping Guide: Section 8 (SCSS Integration Order)
- [3.4 SCSS Integration in SDCs](#34-scss-integration-in-sdcs)

---

### 2.3 Theme Settings Integration

#### Pattern: Drupal Configuration Integration

**Radix does NOT use Drupal's theme settings for design tokens.** Design tokens are implemented via SCSS variables (compile-time) rather than Drupal configuration (runtime).

**Decision Framework:**

| Approach | Use When | Example |
|----------|----------|---------|
| **SCSS Variables** | Design tokens (colors, spacing, typography) | `$primary: #194582;` |
| **Drupal Theme Settings** | User-configurable options | Logo upload, site name toggle |
| **CSS Custom Properties** | Runtime theming (dark mode toggle) | `--bs-primary: #194582;` |

**CSS Custom Properties Pattern (for runtime theming):**

```scss
// In base/_variables.scss
$primary: #194582;

// Bootstrap generates CSS custom properties:
// --bs-primary: #194582;

// Can be overridden at runtime via JavaScript or theme settings
```

#### Common Mistakes
- **Expecting theme settings to control tokens** — Tokens are compile-time (SCSS)
- **Not using CSS custom properties for runtime changes** — Use for dark mode, user themes
- **Overusing runtime customization** — Most tokens should be compile-time for performance

#### See Also
- [1.3 Theme Configuration Files](#13-theme-configuration-files)