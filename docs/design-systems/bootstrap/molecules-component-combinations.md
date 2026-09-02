---
description: "Map molecule-level component combinations (input groups, card content) to Bootstrap"
tldr: "Use this for mapping molecules (2-3 atoms working together) like input groups and card content to Bootstrap's component combinations."
drupal_version: "11.x"
---

# Molecules → Component Combinations

## When to Use

> Use this for mapping molecules (2-3 atoms working together) like input groups and card content to Bootstrap's component combinations.

- You've identified molecules (input groups, card content) from your design system
- These are combinations of 2-3 atoms working together
- You need to map composite patterns to Bootstrap's component combinations

## Input Group Molecules

### Decision Table: Input Group Implementation

| Design System Pattern | Bootstrap Component | Bootstrap Classes | Custom Required |
|----------------------|-------------------|------------------|-----------------|
| Label + Input | Form group | `.mb-3` wrapper + `.form-label` + `.form-control` | No |
| Input + Button | Input group | `.input-group` + `.form-control` + `.btn` | No |
| Input + Icon/Text | Input group with text | `.input-group` + `.input-group-text` | No |
| Input + Dropdown | Input group with dropdown | `.input-group` + `.dropdown` | No |
| Input + Validation | Form validation | `.was-validated` + `.is-valid`/`.is-invalid` | No |

### Pattern: Input Group Molecule

```html
<!-- Input + Button Molecule -->
<div class="input-group mb-3">
  <input type="text" class="form-control" placeholder="Search">
  <button class="btn btn-primary" type="button">Search</button>
</div>

<!-- Input + Icon/Text Molecule -->
<div class="input-group">
  <span class="input-group-text">@</span>
  <input type="text" class="form-control" placeholder="Username">
</div>
```

**SCSS Customization (if needed):**
```scss
$input-group-addon-bg: #e9ecef;
$input-group-addon-border-color: $input-border-color;

@import "bootstrap";
```

### Common Mistakes

- **Not wrapping in .input-group** - Input group styles require parent container
- **Using spacing utilities inside input groups** - Input groups handle spacing automatically
- **Creating custom input group styles** - Use Bootstrap's variables instead
- **Not considering mobile responsiveness** - Input groups are responsive by default

### See Also

- Bootstrap 5.3 Input Groups: [https://getbootstrap.com/docs/5.3/forms/input-group/](https://getbootstrap.com/docs/5.3/forms/input-group/)
- Reference: Design System Recognition Guide - Molecule Recognition

## Card Content Molecules

### Decision Table: Card Content Implementation

| Design System Pattern | Bootstrap Component | Bootstrap Classes | Custom Required |
|----------------------|-------------------|------------------|-----------------|
| Image + Title + Text | Card content | `.card-img-top` + `.card-body` + `.card-title` + `.card-text` | No |
| Title + Subtitle + Text | Card body content | `.card-title` + `.card-subtitle` + `.card-text` | No |
| List items | Card list group | `.list-group` + `.list-group-item` | No |
| Header + Body + Footer | Card sections | `.card-header` + `.card-body` + `.card-footer` | No |

### Pattern: Card Content Molecule

```html
<!-- Image + Title + Text Molecule -->
<div class="card">
  <img src="..." class="card-img-top" alt="...">
  <div class="card-body">
    <h5 class="card-title">Card Title</h5>
    <p class="card-text">Card description text.</p>
  </div>
</div>
```

**SCSS Customization:**
```scss
$card-border-radius: 0.5rem;
$card-cap-bg: rgba(0, 0, 0, 0.03);
$card-title-spacer-y: 0.5rem;

@import "bootstrap";
```

### Common Mistakes

- **Not using .card-body wrapper** - Card padding requires `.card-body` class
- **Creating custom card content classes** - Use Bootstrap's `.card-title`, `.card-text`, etc.
- **Ignoring card utilities** - Cards work with spacing, border, and color utilities
- **Not considering card groups/grids** - Use `.card-group` or grid classes for layouts

### See Also

- Bootstrap 5.3 Cards: [https://getbootstrap.com/docs/5.3/components/card/](https://getbootstrap.com/docs/5.3/components/card/)
- Reference: Design System Recognition Guide - Molecule Recognition

## See Also

- [Atoms → Bootstrap Components](atoms-bootstrap-components.md)
- [Organisms → Layout + Components](organisms-layout-components.md)
