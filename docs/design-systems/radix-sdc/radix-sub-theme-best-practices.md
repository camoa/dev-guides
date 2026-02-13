---
description: Radix sub-theme best practices — override strategy, variable location, starterkit usage, library management, development workflow
drupal_version: "11.x"
---

# Radix Sub-Theme Best Practices

## When to Use

> Use this when setting up a new Radix sub-theme, understanding override strategy (when to override vs extend vs create), managing SCSS variables and compilation, or implementing starterkit usage and library management.

## Decision

**Override Strategy:**

| Approach | When to Use | Maintenance Burden |
|----------|-------------|-------------------|
| **Reuse as-is** | Component meets needs exactly | Zero (automatic updates) |
| **Extend** | Need additional wrapper or custom variant | Minimal |
| **Override** | Need major structural changes | High (you own maintenance) |
| **Create new** | Component doesn't exist in Radix | Medium |

**Why Extend Radix:**

| Starting from Scratch | Extending Radix |
|-----------------------|-----------------|
| Build Bootstrap integration yourself | Bootstrap integration ready |
| Create all components from zero | 57 components ready to use/override |
| Figure out Drupal template integration | Templates integrated with core/contrib |
| Set up build tools | Laravel Mix configured |
| Implement responsive patterns | Responsive patterns built-in |
| **Time: Weeks/months** | **Time: Days** |

**Library Loading:**

| Library Type | Load Where | When to Use | Performance Impact |
|-------------|-----------|-------------|-------------------|
| Global | `THEME_NAME.info.yml` | Site-wide styles/scripts | Loaded on every page |
| Component-specific | SDC auto-loaded | Component-only styles | Only when component renders |
| Template-specific | `{{ attach_library() }}` | Specific content type | Only on relevant pages |

## Pattern

**1. Reuse As-Is (Best Option):**

```twig
{# Just use Radix component directly #}
{% include 'radix:button' with {
  color: 'primary',
  content: 'Click me',
} %}
```

**2. Extend (Second Best):**

```scss
// src/scss/components/_custom-buttons.scss
@import '../init';

.btn-brand {
  @include button-variant(
    $background: $brand-color,
    $border: $brand-color,
    $color: color-contrast($brand-color)
  );
}
```

**3. Override (Use Sparingly):**

```bash
# Copy component from Radix to sub-theme
cp -r ~/workspace/contrib/web/themes/contrib/radix/components/button \
      themes/custom/THEME_NAME/components/button

# Modify in sub-theme
# Document WHY you overrode (comment in .component.yml)
# Note original Radix version
```

**4. Create New:**

```bash
# Use drupal-radix-cli
drupal-radix add my-custom-component
```

**Variable Override Location (`src/scss/base/_variables.scss`):**

```scss
/**
 * Variables
 * Copy from node_modules/bootstrap/scss/_variables.scss
 * Change value and remove !default flag
 */

// Color system
$primary: #194582;
$secondary: #6c757d;

// Typography
$font-family-base: system-ui, -apple-system, "Segoe UI", sans-serif;
```

**Starterkit File Strategy:**

| Files | Action | Reason |
|-------|--------|---------|
| `_init.scss`, `_bootstrap.scss` | Keep as-is | Radix manages these |
| `base/_variables.scss` | Customize | Primary customization file |
| `THEME_NAME.info.yml` | Customize | Theme metadata, regions |
| `components/` | Delete examples | Add your own components |
| `templates/` | Add only overrides | Don't keep unnecessary files |

**Library Dependencies:**

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

# BAD: Using weight (deprecated)
custom-component:
  css:
    theme:
      css/custom-component.css:
        weight: 100  # Avoid this
```

**Development Workflow:**

```bash
# Development mode (watch)
npm run watch

# Production mode (before commit)
npm run production
git add src/scss/base/_variables.scss
git add build/css/main.style.css
git commit
```

## Common Mistakes

- **Wrong**: Installing npm in `themes/contrib/radix` → **Right**: Install in your sub-theme
- **Wrong**: Committing SCSS changes without compiling → **Right**: Run `npm run production` before commit
- **Wrong**: Copying entire navbar just to change color → **Right**: Extend with custom SCSS
- **Wrong**: Manually creating component files → **Right**: Use `drupal-radix add` CLI
- **Wrong**: Editing `_init.scss` directly → **Right**: Add to `base/_variables.scss`
- **Wrong**: Using weight-based library ordering → **Right**: Use dependencies
- **Wrong**: Loading everything globally → **Right**: Use component-specific or template-specific libraries
- **Wrong**: Overriding when extending would work → **Right**: Extend first, override only when necessary
- **Wrong**: Not documenting why you overrode → **Right**: Document in `.component.yml` comments
- **Wrong**: Keeping unnecessary starterkit files → **Right**: Delete examples, add only what you need

## See Also

- [Sub-Theme Architecture](sub-theme-architecture.md)
- [Design Tokens Configuration](design-tokens-configuration.md)
- [Radix Component Reuse Strategy](radix-component-reuse-strategy.md)
- Reference: `~/workspace/contrib/web/themes/contrib/radix/components/`
