---
description: Molecules to Component Combinations — mapping input groups and card content to Bootstrap's component combinations
---

# Molecules to Component Combinations

## When to Use

> Use when mapping molecules (input groups, card content) — combinations of 2-3 atoms working together — to Bootstrap's component combinations.

## Decision

| Molecule Pattern | Bootstrap Component | Bootstrap Classes | Custom Required |
|------------------|-------------------|------------------|-----------------|
| Label + Input | Form group | `.mb-3` + `.form-label` + `.form-control` | No |
| Input + Button | Input group | `.input-group` + `.form-control` + `.btn` | No |
| Input + Icon/Text | Input group with text | `.input-group` + `.input-group-text` | No |
| Image + Title + Text | Card content | `.card-img-top` + `.card-body` + `.card-title` + `.card-text` | No |

## Pattern

**Input Group Molecules**:
```html
<!-- Input + Button -->
<div class="input-group mb-3">
  <input type="text" class="form-control" placeholder="Search">
  <button class="btn btn-primary" type="button">Search</button>
</div>

<!-- Input + Icon/Text -->
<div class="input-group">
  <span class="input-group-text">@</span>
  <input type="text" class="form-control" placeholder="Username">
</div>
```

**SCSS Customization**:
```scss
$input-group-addon-bg: #e9ecef;
$input-group-addon-border-color: $input-border-color;

@import "bootstrap";
```

**Card Content Molecules**:
```html
<div class="card">
  <img src="..." class="card-img-top" alt="...">
  <div class="card-body">
    <h5 class="card-title">Card Title</h5>
    <p class="card-text">Card description text.</p>
  </div>
</div>
```

**SCSS Customization**:
```scss
$card-border-radius: 0.5rem;
$card-cap-bg: rgba(0, 0, 0, 0.03);
$card-title-spacer-y: 0.5rem;

@import "bootstrap";
```

## Common Mistakes

- **Wrong**: Not wrapping in `.input-group` → **Right**: Input group styles require parent container
- **Wrong**: Using spacing utilities inside input groups → **Right**: Input groups handle spacing automatically
- **Wrong**: Not using `.card-body` wrapper → **Right**: Card padding requires this class
- **Wrong**: Creating custom card content classes → **Right**: Use Bootstrap's `.card-title`, `.card-text`
- **Wrong**: Creating custom input group styles → **Right**: Use Bootstrap's variables

## See Also

- [Atoms to Bootstrap Components](atoms-bootstrap-components.md)
- [Organisms to Layout + Components](organisms-layout-components.md)
- Reference: [Bootstrap 5.3 Input Groups](https://getbootstrap.com/docs/5.3/forms/input-group/)
- Reference: [Bootstrap 5.3 Cards](https://getbootstrap.com/docs/5.3/components/card/)
