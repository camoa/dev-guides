---
description: Radix component reuse strategy — component catalog, reuse decision framework, overriding Radix components
drupal_version: "11.x"
---

# Radix Component Reuse Strategy

## When to Use

> Use this when evaluating whether to reuse, override, or create components, needing a catalog of existing Radix SDC components, or wanting to extend Radix components in your sub-theme.

## Decision

| Scenario | Decision | Action |
|----------|----------|--------|
| Radix component exists, meets needs | **REUSE** | Use `{% include 'radix:COMPONENT' %}` |
| Radix component exists, needs minor changes | **EXTEND** | Include + add custom wrapper/styles |
| Radix component exists, needs major changes | **OVERRIDE** | Copy to sub-theme, modify |
| Radix component doesn't exist | **CREATE** | New SDC in sub-theme |
| Design system atom = Bootstrap class | **USE BOOTSTRAP** | No SDC needed |

**Decision Process:**

```
1. Does this match a Radix component?
   YES → Can you use it as-is?
      YES → REUSE via include
      NO → Continue to step 2
   NO → Continue to step 4

2. Are changes minor (styling, props)?
   YES → EXTEND (include + custom SCSS)
   NO → Continue to step 3

3. Are changes major (structure, behavior)?
   YES → OVERRIDE (copy to sub-theme)
   NO → Back to step 2

4. Can Bootstrap utility classes achieve this?
   YES → USE BOOTSTRAP (no SDC)
   NO → CREATE new SDC
```

## Pattern

**Radix 6.x Component Catalog (57 components):**

**Atoms:**

- `badge/` — Count/labeling component
- `button/` — Button with variants (color, outline, size, disabled)
- `close-button/` — Dismissal button
- `heading/` — Configurable headings h1-h6
- `image/` — Responsive images
- `input/` — Form text inputs
- `select/` — Dropdown select input
- `spinner/` — Loading indicator
- `textarea/` — Multiline text input

**Molecules:**

- `button-group/` — Groups buttons/inputs
- `dropdown/` — Dropdown menu component
- `dropdown-menu/` — Dropdown menu items
- `fieldset/` — Form fieldset element
- `figure/` — Image with caption
- `form-element/` — Form field wrapper
- `form-element--label/` — Form label
- `form-element--radiocheckbox/` — Radio/checkbox wrapper
- `list-group/` — Bootstrap list group
- `nav-item/` — Single navigation item
- `radios/` — Radio button group

**Organisms:**

- `accordion/` — Bootstrap accordion
- `alert/` — Contextual feedback (stable status)
- `breadcrumb/` — Breadcrumb navigation
- `card/` — Flexible content container (with image/body/footer slots)
- `carousel/` — Image/content carousel
- `collapse/` — Collapsible content
- `details/` — Disclosure widget
- `modal/` — Layered content overlay
- `nav/` — Flexible navigation
- `navbar/` — Responsive header
- `navbar-brand/` — Navbar branding
- `offcanvas/` — Hidden sidebar
- `pagination/` — Page navigation
- `progress/` — Progress indicator
- `table/` — Data table
- `toasts/` — Toast notifications

**Page-Level:**

- `html/` — HTML document structure
- `page/` — Main page structure
- `page-content/` — Main content area
- `page-footer/` — Page footer
- `page-navigation/` — Navigation container
- `page-title/` — Page heading

**Drupal Integration:**

- `block/` — Block wrapper
- `comment/` — Comment display
- `field/` — Field display
- `field-comment/` — Comment field section
- `form/` — Form wrapper
- `local-tasks/` — Tabs and pills navigation
- `media/` — Media entity display
- `node/` — Node entity display
- `region/` — Drupal region wrapper
- `taxonomy/` — Taxonomy term display
- `user/` — User profile display
- `views-view/` — Views display base
- `views-view--grid/` — Views grid layout
- `views-view--table/` — Views table display
- `views-view--unformatted/` — Views unformatted rows

**Reuse Example:**

```twig
{# REUSE: Use Radix button as-is #}
{% include 'radix:button' with {
  color: 'primary',
  content: 'Submit',
} %}
```

**Extend Example:**

```twig
{# EXTEND: Wrap Radix component #}
<div class="custom-wrapper">
  {% include 'radix:button' with {
    color: 'primary',
    content: 'Submit',
  } %}
  <span class="tooltip">Submit the form</span>
</div>
```

```scss
// EXTEND: Add custom styles
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

**Override Example:**

```bash
# Copy Radix component to sub-theme
cp -r ~/workspace/contrib/web/themes/contrib/radix/components/button \
      themes/custom/THEME_NAME/components/button

# Modify in sub-theme
# Document WHY in button.component.yml:
# description: "Override: Custom brand-specific button structure"
# original_radix_version: "6.0.5"
```

**Override Considerations:**

| Maintenance Aspect | Impact |
|-------------------|--------|
| Security patches | Won't get fixes automatically |
| Radix updates | Won't receive improvements |
| Upgrade burden | Manual review on major versions |
| Divergence risk | May become incompatible |

## Common Mistakes

- **Wrong**: Not checking Radix first → **Right**: Always review existing components before creating
- **Wrong**: Duplicating Radix components → **Right**: Reuse or extend instead
- **Wrong**: Overriding when extending would work → **Right**: Try extending first
- **Wrong**: Not documenting why you overrode → **Right**: Comment in `.component.yml` with reason
- **Wrong**: Not noting original Radix version → **Right**: Document version you copied from
- **Wrong**: Assuming Radix has everything → **Right**: Some specialized components need creation
- **Wrong**: Not reading component YAML → **Right**: Props/slots defined in `.component.yml` files
- **Wrong**: Confusing component names → **Right**: Directory name must match file prefix

## See Also

- [Atoms SDC Components](atoms-sdc-components.md)
- [Radix Sub-Theme Best Practices](radix-sub-theme-best-practices.md)
- [SDC Component Best Practices](sdc-component-best-practices.md)
- Reference: `~/workspace/contrib/web/themes/contrib/radix/components/`
- Radix Documentation: https://docs.trydrupal.com/radix/working-with-the-components/
