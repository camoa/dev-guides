---
description: Map organism-level components (navbars, complete cards, forms) to Bootstrap
---

# Organisms → Layout + Components

## When to Use

> Use this for mapping organisms (complex UI sections combining multiple molecules and atoms) like navbars and complete cards to Bootstrap's component system.

## Navbar Organisms

| Design System Need | Bootstrap Variable | Bootstrap Classes |
|-------------------|-------------------|------------------|
| Navbar base | `$navbar-padding-y`, `$navbar-padding-x` | `.navbar` |
| Navbar brand/logo | `$navbar-brand-*` variables | `.navbar-brand` |
| Navbar links | `$navbar-nav-link-padding-x` | `.navbar-nav` + `.nav-link` |
| Navbar light/dark | N/A | `.navbar-light`, `.navbar-dark` |
| Navbar background | Uses `$theme-colors` | `.bg-primary`, `.bg-dark` |
| Navbar toggler (mobile) | `$navbar-toggler-*` variables | `.navbar-toggler` |

### Pattern

**SCSS:**

```scss
$navbar-padding-y: 0.5rem;
$navbar-padding-x: 1rem;
$navbar-brand-font-size: 1.25rem;
$navbar-nav-link-padding-x: 0.5rem;
$navbar-dark-color: rgba(255, 255, 255, 0.85);
$navbar-dark-hover-color: rgba(255, 255, 255, 1);

@import "bootstrap";
```

**HTML:**

```html
<nav class="navbar navbar-expand-lg navbar-dark bg-primary">
  <div class="container-fluid">
    <a class="navbar-brand" href="#">Brand</a>
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarNav">
      <ul class="navbar-nav">
        <li class="nav-item"><a class="nav-link active" href="#">Home</a></li>
        <li class="nav-item"><a class="nav-link" href="#">About</a></li>
      </ul>
    </div>
  </div>
</nav>
```

## Card Organisms

| Design System Need | Bootstrap Variable | Bootstrap Classes |
|-------------------|-------------------|------------------|
| Card container | `$card-border-width`, `$card-border-radius` | `.card` |
| Card sections | `$card-spacer-y`, `$card-spacer-x` | `.card-header`, `.card-body`, `.card-footer` |
| Card colors | Uses `$theme-colors` | `.bg-*`, `.text-*`, `.border-*` |
| Card groups | `$card-group-margin` | `.card-group`, `.card-deck` |

### Pattern

```scss
$card-spacer-y: 1rem;
$card-spacer-x: 1rem;
$card-border-width: 1px;
$card-border-radius: 0.5rem;
$card-cap-bg: rgba(0, 0, 0, 0.03);

@import "bootstrap";
```

## Form Organisms

| Design System Need | Bootstrap Variable | Bootstrap Classes |
|-------------------|-------------------|------------------|
| Form layout | N/A | `.row` + `.col-*` or `.mb-3` wrappers |
| Form labels | `$form-label-*` variables | `.form-label` |
| Form controls | Input/select variables | `.form-control`, `.form-select` |
| Form validation | Validation variables | `.was-validated`, `.is-valid`, `.is-invalid` |
| Form buttons | Button variables | `.btn` |

### Pattern

```html
<form class="row g-3 needs-validation" novalidate>
  <div class="col-md-6">
    <label for="firstName" class="form-label">First name</label>
    <input type="text" class="form-control" id="firstName" required>
    <div class="valid-feedback">Looks good!</div>
  </div>
  <div class="col-md-6">
    <label for="lastName" class="form-label">Last name</label>
    <input type="text" class="form-control" id="lastName" required>
  </div>
  <div class="col-12">
    <button class="btn btn-primary" type="submit">Submit</button>
  </div>
</form>
```

## Common Mistakes

- **Wrong**: Not using .navbar-expand-* classes → **Right**: Required for responsive behavior
- **Wrong**: Mixing navbar color variants → **Right**: Use either .navbar-light or .navbar-dark
- **Wrong**: Not including collapse/toggler → **Right**: Mobile navigation requires .navbar-toggler and .collapse
- **Wrong**: Hardcoding navbar heights → **Right**: Bootstrap calculates from brand/padding variables
- **Wrong**: Not using container → **Right**: Wrap navbar content in .container or .container-fluid

## See Also

- [Molecules → Component Combinations](molecules-component-combinations.md)
- [Templates → Bootstrap Grid](templates-bootstrap-grid.md)
- Reference: [Bootstrap Navbar](https://getbootstrap.com/docs/5.3/components/navbar/)
- Reference: [Bootstrap Cards](https://getbootstrap.com/docs/5.3/components/card/)
- Reference: [Bootstrap Forms](https://getbootstrap.com/docs/5.3/forms/overview/)
