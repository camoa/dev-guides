---
description: You're deciding component granularity (too small vs too large)
drupal_version: "11.x"
---

## 3.5 SDC Component Best Practices

### When to Use This Section
- You're deciding component granularity (too small vs too large)
- You need guidance on props vs slots architecture
- You're questioning whether a Bootstrap class is sufficient vs creating an SDC
- You want senior themer guidance on component design decisions

### Component Granularity Decision Framework

#### Pattern: When Component is Too Small

**DON'T CREATE SDC FOR:**

```yaml
# BAD: Wrapper component
name: Flex Container
props:
  gap:
    type: string
    enum: ['1', '2', '3']
```

**WHY:** Bootstrap already provides `.d-flex .gap-2`. Creating an SDC adds indirection without value.

**INSTEAD USE:** Bootstrap utility classes directly in templates:
```twig
<div class="d-flex gap-2 align-items-center">
  {# Content #}
</div>
```

**DON'T CREATE SDC FOR:**

```yaml
# BAD: Spacing component
name: Spacer
props:
  size:
    type: string
```

**WHY:** This is literally what Bootstrap spacing utilities (`.mb-3`, `.py-4`) are for.

**RULE OF THUMB:** If the component is just applying 1-3 Bootstrap classes without custom logic or markup structure, use Bootstrap classes directly.

#### Pattern: When Component is Too Large

**SPLIT WHEN:**
- Component has 200+ lines of Twig
- Component needs different props for different "sections"
- Component is reused but you only need parts of it sometimes

**EXAMPLE: Hero section too large**

```yaml
# BAD: Monolithic hero
name: Hero Section
props:
  # 30+ props for different hero variants
  # Background image, video background, carousel, parallax...
```

**WHY:** Different page types need different hero patterns. Monolithic component has unused props/slots and complex conditional logic.

**INSTEAD:** Split into focused components:
- `hero-simple/` — Image background + heading + CTA
- `hero-video/` — Video background variant
- `hero-carousel/` — Carousel-based hero

#### Pattern: Component Granularity Sweet Spot

**CREATE SDC WHEN:**
1. **Reused across multiple templates** — Used in 3+ places
2. **Has configurable variants** — Not just one fixed layout
3. **Contains custom markup structure** — Not achievable with utility classes alone
4. **Represents a design system atom/molecule** — Part of your design language

**EXAMPLE: Button with icon (justified)**

```yaml
# GOOD: Icon button component
name: Icon Button
props:
  icon_position:
    type: string
    enum: ['before', 'after']
    default: 'before'
  icon_class:
    type: string
  color:
    type: string
    enum: ['primary', 'secondary']
slots:
  content:
    title: Button text
```

**WHY:** This pattern appears across the site, has consistent structure but configurable variants, and represents a design system element.

### Props vs Slots Architecture Decisions

#### Decision Table: Props vs Slots

| Scenario | Use Props | Use Slots | WHY |
|----------|-----------|-----------|-----|
| Simple text/string | ✅ | ❌ | Props are validated, typed, documented in schema |
| HTML content | ❌ | ✅ | Props can't contain markup safely |
| Number/boolean config | ✅ | ❌ | Props provide type validation |
| Nested components | ❌ | ✅ | Slots enable composition |
| User-generated content | ❌ | ✅ | Props shouldn't trust user HTML |
| Design system token | ✅ | ❌ | Props enforce valid values via enum |

#### Pattern: Props for Configuration

**GOOD PRACTICE:**

```yaml
props:
  type: object
  properties:
    size:
      type: string
      enum: ['sm', 'md', 'lg']  # Enforce valid values
      default: 'md'
    color:
      type: string
      enum: ['primary', 'secondary', 'success']
      default: 'primary'
```

**WHY:**
- **Schema validation** — Invalid values are caught during rendering
- **Documentation** — Developers see valid options without reading code
- **IDE support** — Schema enables autocomplete in modern IDEs
- **Design system enforcement** — Can't use arbitrary colors outside the system

#### Pattern: Slots for Content

**GOOD PRACTICE:**

```yaml
slots:
  header:
    title: Card Header
    description: Optional header content with custom markup
  body:
    title: Card Body
    description: Main card content
  footer:
    title: Card Footer
    description: Optional footer with buttons or links
```

**WHY:**
- **Flexibility** — Content editors can use rich text, other components, or Drupal fields
- **Composition** — Slots enable nesting `{% include 'theme:button' %}` inside card
- **No escaping issues** — Slots handle markup safely without prop escaping concerns

### SCSS Scoping Best Practices

#### Pattern: BEM Inside Components

**CRITICAL RULE:** Use BEM methodology for component-specific classes.

```scss
// components/card-teaser/card-teaser.scss
@import '../../src/scss/init';

.card-teaser {
  // Block-level styles
  background: $white;
  border-radius: $border-radius;

  // Elements (use &__ syntax)
  &__image {
    width: 100%;
    height: auto;
  }

  &__title {
    font-size: $h3-font-size;
    color: $headings-color;
  }

  &__excerpt {
    color: $text-muted;
  }

  // Modifiers (use &-- syntax)
  &--featured {
    border: 2px solid $primary;
    box-shadow: $box-shadow-lg;
  }
}
```

**WHY BEM IN SDCs:**
- **Prevents global CSS conflicts** — `.card-teaser__title` won't accidentally affect other `.title` classes
- **Self-documenting** — Class names describe the component structure
- **Maintainable** — Easy to understand which styles belong to which component
- **Scoped styling** — Changes to `.card-teaser` don't leak to other components

#### Pattern: Import _init.scss for Bootstrap Access

**ALWAYS DO THIS:**

```scss
// At the top of every SDC SCSS file
@import '../../src/scss/init';
```

**WHY:**
- **Access to variables** — `$primary`, `$spacer`, `$border-radius` available
- **Access to mixins** — `media-breakpoint-up()`, `button-variant()` available
- **Access to functions** — `color-contrast()`, `shade-color()`, `tint-color()` available
- **Consistency** — Component uses same design tokens as rest of theme

**COMMON MISTAKE — Hardcoding values:**

```scss
// BAD: Hardcoded
.my-component {
  color: #194582;  // What token is this?
  padding: 16px;   // Is this consistent with spacing scale?
}

// GOOD: Using Bootstrap variables
.my-component {
  color: $primary;
  padding: $spacer;  // Uses spacing scale
}
```

#### Pattern: Component-Specific Styles Only

**KEEP SCOPED:**

```scss
// GOOD: Styles scoped to .card-teaser
.card-teaser {
  &__title {
    // Only affects titles inside card-teaser
  }
}
```

**DON'T DO THIS:**

```scss
// BAD: Global styles in component SCSS
h3 {
  // This affects ALL h3 elements, not just in this component
  font-size: 1.5rem;
}

.container {
  // Accidentally overriding Bootstrap's .container
}
```

**WHY:** Component SCSS should style ONLY that component. Global styles belong in `src/scss/base/_elements.scss` or `_typography.scss`.

### Schema Definition Best Practices

#### Pattern: Require Only What's Necessary

```yaml
props:
  type: object
  required:
    - title  # Actually required
  properties:
    title:
      type: string
      title: Title
    description:
      type: string
      title: Description
      default: ''  # Optional, has default
```

**WHY:**
- **Flexibility** — Components work with minimal data
- **Reusability** — Can use component in more contexts
- **Better error messages** — Clear what's actually required

**COMMON MISTAKE — Over-requiring:**

```yaml
required:
  - title
  - description
  - icon
  - color
  - size
```

**WHY BAD:** Forces developers to pass props they don't need, reducing reusability.

#### Pattern: Use Enums for Fixed Options

```yaml
props:
  properties:
    size:
      type: string
      enum: ['sm', 'md', 'lg']
      default: 'md'
```

**WHY:**
- **Validation** — Drupal rejects invalid values at render time
- **Documentation** — Developers see valid options immediately
- **Prevents typos** — Can't accidentally pass 'medium' instead of 'md'

#### Pattern: Default Values for Everything Optional

```yaml
props:
  properties:
    show_icon:
      type: boolean
      default: false  # Explicit default
    button_style:
      type: string
      enum: ['primary', 'secondary']
      default: 'primary'  # Explicit default
```

**WHY:**
- **Graceful fallback** — Component works even if prop omitted
- **Consistent behavior** — All devs get same default behavior
- **Documentation** — Defaults show intended usage

### Common Mistakes Senior Themers Catch in Code Review

**1. Not checking slot existence**

```twig
{# BAD: Will error if slot not provided #}
<div class="header">
  {{ slots.header }}
</div>

{# GOOD: Conditional rendering #}
{% if slots.header %}
  <div class="header">
    {{ slots.header }}
  </div>
{% endif %}
```

**WHY:** Empty slots render empty `<div>`s or cause errors.

**2. Using props for HTML content**

```yaml
# BAD: Props can't safely contain markup
props:
  properties:
    description:
      type: string  # What if this contains <script> tags?
```

```twig
{# BAD: Unescaped HTML in prop #}
<div>{{ description|raw }}</div>
```

**WHY:** Security risk (XSS) and props aren't designed for markup. Use slots instead.

**3. Not using Drupal attributes object**

```twig
{# BAD: Hardcoded classes #}
<div class="my-component my-component--primary">

{# GOOD: Merge with attributes #}
{%
  set classes = [
    'my-component',
    variant ? 'my-component--' ~ variant : '',
  ]
%}
<div {{ attributes.addClass(classes) }}>
```

**WHY:** `attributes` object allows Drupal to add contextual classes, data attributes, and IDs. Hardcoding prevents this.

**4. Duplicating Radix components**

```bash
# BAD: Creating custom button when Radix has one
components/button/button.component.yml
```

**WHY:** Radix already has 57 components. Check `radix/components/` before creating.

**PROCESS:**
1. Check Radix component catalog (Section 8.1)
2. Can you use Radix component as-is? → Use `{% include 'radix:button' %}`
3. Need minor changes? → Extend via wrapper or custom SCSS
4. Need major structural changes? → Override (copy to sub-theme)
5. Doesn't exist? → Create new component

**5. Not namespacing component CSS**

```scss
// BAD: Generic class names
.title {
  // This will conflict with other .title classes
}

// GOOD: Namespaced with BEM
.hero-section__title {
  // Clear scope and ownership
}
```

**WHY:** CSS specificity battles and accidental overrides across components.

#### See Also
- [4.2 Slots and Composition](#42-slots-and-composition)
- [7.1 Component YAML Schema](#71-component-yaml-schema)
- [7.3 SCSS Scoping](#73-scss-scoping)
- [8.1 Radix Component Catalog](#81-radix-component-catalog)