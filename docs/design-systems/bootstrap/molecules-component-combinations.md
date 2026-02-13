---
description: Map molecule-level component combinations (input groups, card content) to Bootstrap
---

# Molecules → Component Combinations

## When to Use

> Use this for mapping molecules (2-3 atoms working together) like input groups and card content to Bootstrap's component combinations.

## Input Group Molecules

| Design System Pattern | Bootstrap Component | Bootstrap Classes |
|----------------------|-------------------|------------------|
| Label + Input | Form group | `.mb-3` wrapper + `.form-label` + `.form-control` |
| Input + Button | Input group | `.input-group` + `.form-control` + `.btn` |
| Input + Icon/Text | Input group with text | `.input-group` + `.input-group-text` |
| Input + Dropdown | Input group with dropdown | `.input-group` + `.dropdown` |
| Input + Validation | Form validation | `.was-validated` + `.is-valid`/`.is-invalid` |

### Pattern

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

**SCSS Customization:**

```scss
$input-group-addon-bg: #e9ecef;
$input-group-addon-border-color: $input-border-color;

@import "bootstrap";
```

## Card Content Molecules

| Design System Pattern | Bootstrap Component | Bootstrap Classes |
|----------------------|-------------------|------------------|
| Image + Title + Text | Card content | `.card-img-top` + `.card-body` + `.card-title` + `.card-text` |
| Title + Subtitle + Text | Card body content | `.card-title` + `.card-subtitle` + `.card-text` |
| List items | Card list group | `.list-group` + `.list-group-item` |
| Header + Body + Footer | Card sections | `.card-header` + `.card-body` + `.card-footer` |

### Pattern

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

## Common Mistakes

- **Wrong**: Not wrapping in .input-group → **Right**: Input group styles require parent container
- **Wrong**: Using spacing utilities inside input groups → **Right**: Input groups handle spacing automatically
- **Wrong**: Not using .card-body wrapper → **Right**: Card padding requires .card-body class
- **Wrong**: Creating custom card content classes → **Right**: Use Bootstrap's .card-title, .card-text
- **Wrong**: Ignoring card utilities → **Right**: Cards work with spacing, border, and color utilities

## See Also

- [Atoms → Bootstrap Components](atoms-bootstrap-components.md)
- [Organisms → Layout + Components](organisms-layout-components.md)
- Reference: [Bootstrap Input Groups](https://getbootstrap.com/docs/5.3/forms/input-group/)
- Reference: [Bootstrap Cards](https://getbootstrap.com/docs/5.3/components/card/)
