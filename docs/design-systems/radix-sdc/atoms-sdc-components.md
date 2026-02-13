---
description: You've identified atoms using the Design System Recognition Guide
drupal_version: "11.x"
---

## 3. Atoms → SDC Components

### When to Use This Section
- You've identified atoms using the Design System Recognition Guide
- You need to decide when to create an atom SDC vs use Bootstrap classes
- You're creating foundational UI components

### 3.1 Atom Creation Decision Framework

#### Decision Table: Create SDC vs Use Bootstrap

| Atom Type | Radix Provides SDC? | Bootstrap Provides Classes? | Decision |
|-----------|---------------------|----------------------------|----------|
| Button | Yes (`button/`) | Yes (`.btn`) | **REUSE** Radix SDC or Bootstrap classes |
| Input | Yes (`input/`) | Yes (`.form-control`) | **REUSE** Radix SDC or Bootstrap classes |
| Badge | Yes (`badge/`) | Yes (`.badge`) | **REUSE** Radix SDC or Bootstrap classes |
| Heading | Yes (`heading/`) | Yes (`<h1>`-`<h6>`) | **REUSE** Radix SDC or Bootstrap classes |
| Icon | No | No | **CREATE** SDC if reusable |
| Avatar | No | No | **CREATE** SDC if reusable |
| Tag/Chip | No | Partial (`.badge`) | **CREATE** or extend Radix badge |
| Custom atom | No | No | **CREATE** SDC |

#### Pattern: Atom Creation Decision Process

```
1. Does Radix provide this atom?
   YES → Reuse Radix SDC (see Section 8)
   NO → Continue to step 2

2. Do Bootstrap utility classes suffice?
   YES → Use Bootstrap classes in HTML (no SDC needed)
   NO → Continue to step 3

3. Is this atom reused across multiple templates?
   YES → Create SDC
   NO → Consider inline styles or template-specific CSS

4. Does this atom have configurable variants?
   YES → Create SDC with props
   NO → May not need SDC
```

#### Common Mistakes
- **Creating SDC for every element** — Not everything needs an SDC; use Bootstrap classes when possible
- **Duplicating Radix SDCs** — Check existing Radix components first (see Section 8.1)
- **Over-engineering simple atoms** — Use Bootstrap utilities for simple styling
- **Not considering reusability** — Only create SDC if component is reused

#### See Also
- [8.1 Radix Component Catalog](#81-radix-component-catalog)
- [8.2 Reuse Decision Framework](#82-reuse-decision-framework)
- Design System Recognition Guide: Section 2.2 (Atom Recognition)

---

### 3.2 SDC Component Structure

#### Pattern: Complete SDC File Structure

**Directory: `components/button/`**

```
button/
├── button.component.yml    # Component metadata
├── button.twig             # Component template
├── button.scss             # Component styles (optional)
├── button.js               # Component JavaScript (optional)
└── README.mdx              # Documentation (optional)
```

**File: `button.component.yml`**
```yaml
$schema: https://git.drupalcode.org/project/drupal/-/raw/10.1.x/core/modules/sdc/src/metadata.schema.json
name: Button
status: experimental
description: Custom button component with design system variants
props:
  type: object
  properties:
    color:
      type: string
      title: Color
      default: ''
      enum:
        - ''
        - primary
        - secondary
        - success
    size:
      type: string
      title: Size
      default: ''
      enum:
        - ''
        - sm
        - lg
    disabled:
      type: boolean
      title: Disabled
      default: false
    button_utility_classes:
      type: array
      items:
        type: string
      title: Utility Classes
      default: []
slots:
  content:
    title: Content
    description: Button text or content
```

**File: `button.twig`**
```twig
{%
  set button_classes = [
    'btn',
    color ? 'btn-' ~ color : '',
    size ? 'btn-' ~ size : '',
    disabled ? 'disabled' : '',
  ]|merge(button_utility_classes ?: [])
%}

<button {{ attributes.addClass(button_classes) }}>
  {% block content %}
    {{ content }}
  {% endblock %}
</button>
```

**File: `button.scss`** (optional)
```scss
// Import Bootstrap foundation
@import '../../src/scss/init';

// Component-specific styles
.btn {
  // Customizations beyond Bootstrap defaults
  // Use Bootstrap variables for consistency

  &-custom-variant {
    @include button-variant(
      $background: $custom-color,
      $border: $custom-color,
      $color: color-contrast($custom-color)
    );
  }
}
```

#### Decision Table: File Requirements

| File | Required? | Purpose |
|------|-----------|---------|
| `*.component.yml` | **YES** | Component metadata, props, slots |
| `*.twig` | **YES** | Component markup |
| `*.scss` | No | Component-specific styles (auto-loaded if exists) |
| `*.js` | No | Component-specific JavaScript (auto-loaded if exists) |
| `README.mdx` | No | Documentation |

**CRITICAL:** File prefix must match directory name. Directory `button/` requires `button.component.yml` and `button.twig`.

#### Common Mistakes
- **Naming mismatch** — Directory and file prefix must match exactly
- **Missing schema reference** — Include `$schema` for validation
- **Not using slots** — Slots enable content composition
- **Hardcoding values** — Use props for variant configuration

#### See Also
- [7.1 Component YAML Schema](#71-component-yaml-schema)
- [7.2 Props and Slots](#72-props-and-slots)
- Official Drupal SDC Documentation: https://www.drupal.org/docs/develop/theming-drupal/using-single-directory-components

---

### 3.3 Button Atom Pattern

#### Pattern: Extending Radix Button

**Radix provides:** `radix/components/button/` with Bootstrap integration

**When to extend:**
- Need custom color variant not in Bootstrap
- Need custom size not in Bootstrap
- Need brand-specific styling

**File: `components/brand-button/brand-button.component.yml`**
```yaml
$schema: https://git.drupalcode.org/project/drupal/-/raw/10.1.x/core/modules/sdc/src/metadata.schema.json
name: Brand Button
status: stable
description: Brand-specific button with custom colors
props:
  type: object
  properties:
    variant:
      type: string
      title: Variant
      default: 'primary'
      enum:
        - primary
        - secondary
        - brand-accent
    size:
      type: string
      title: Size
      default: ''
    button_utility_classes:
      type: array
      items:
        type: string
      default: []
slots:
  content:
    title: Content
```

**File: `components/brand-button/brand-button.twig`**
```twig
{%
  set button_classes = [
    'btn',
    'btn-' ~ variant,
    size ? 'btn-' ~ size : '',
  ]|merge(button_utility_classes ?: [])
%}

<button {{ attributes.addClass(button_classes) }}>
  {% block content %}
    {{ content }}
  {% endblock %}
</button>
```

**File: `components/brand-button/brand-button.scss`**
```scss
@import '../../src/scss/init';

// Define brand accent color in base/_variables.scss first:
// $brand-accent: #ff6600;

.btn-brand-accent {
  @include button-variant(
    $background: $brand-accent,
    $border: $brand-accent,
    $color: color-contrast($brand-accent),
    $hover-background: shade-color($brand-accent, 10%),
    $hover-border: shade-color($brand-accent, 12.5%),
    $active-background: shade-color($brand-accent, 12.5%)
  );
}
```

#### Common Mistakes
- **Not importing _init.scss** — Needed for Bootstrap functions/variables
- **Hardcoding colors** — Define in `base/_variables.scss` first
- **Not using Bootstrap mixins** — Use `button-variant()` for consistency
- **Duplicating Radix button** — Extend, don't replace

#### See Also
- [8.3 Overriding Radix Components](#83-overriding-radix-components)
- Bootstrap Mapping Guide: Section 4.1 (Button Atoms)

---

### 3.4 SCSS Integration in SDCs

#### Pattern: Importing Bootstrap Foundation in SDC SCSS

**Every SDC SCSS file should import `_init.scss`:**

```scss
// At top of component SCSS file
@import '../../src/scss/init';

// Now you have access to:
// - All Bootstrap variables ($primary, $spacer, etc.)
// - All Bootstrap mixins (button-variant, media-breakpoint-up, etc.)
// - All Bootstrap functions (color-contrast, shade-color, etc.)
// - Radix custom mixins and utilities

// Component-specific styles
.my-component {
  color: $primary;
  padding: $spacer;

  @include media-breakpoint-up(md) {
    padding: $spacer * 2;
  }
}
```

#### Decision Table: SCSS Scoping Strategy

| Scope | Pattern | When to Use |
|-------|---------|-------------|
| **Component-specific** | Styles in SDC SCSS file | Component-only styles |
| **Global** | Styles in `base/_elements.scss` | Affects all instances |
| **Bootstrap override** | Variables in `base/_variables.scss` | Changes Bootstrap defaults |
| **Custom utility** | Utility in `base/_utilities.scss` | Reusable utility class |

#### Common Mistakes
- **Not importing _init.scss** — Won't have Bootstrap foundation
- **Hardcoding Bootstrap values** — Use variables instead
- **Global styles in SDC SCSS** — Keep SDC styles scoped to component
- **Not using Bootstrap mixins** — Leverage existing Bootstrap patterns

#### See Also
- [1.2 Bootstrap Loading Chain](#12-bootstrap-loading-chain)
- [2.2 SCSS Import Order](#22-scss-import-order)