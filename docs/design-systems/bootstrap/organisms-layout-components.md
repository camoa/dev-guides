---
description: Organisms to Layout + Components — mapping navbars, complete cards, and forms to Bootstrap's complex components
---

# Organisms to Layout + Components

## When to Use

> Use when mapping organisms (navbars, complete cards, forms) — complex UI sections combining multiple molecules and atoms — to Bootstrap's layout components.

## Decision

| Organism Type | Bootstrap Variable | Bootstrap Classes | Custom Required |
|---------------|-------------------|------------------|-----------------|
| Navbar | `$navbar-padding-y`, `$navbar-brand-*` | `.navbar`, `.navbar-brand`, `.navbar-nav` | No |
| Card | `$card-border-width`, `$card-spacer-y` | `.card`, `.card-body`, `.card-header` | No |
| Form | `$form-label-*`, `$input-*` | `.row`, `.col-*`, `.form-label`, `.form-control` | No |

## Pattern

**Navbar Organism**:
```scss
$navbar-padding-y: 0.5rem;
$navbar-padding-x: 1rem;
$navbar-brand-font-size: 1.25rem;
$navbar-nav-link-padding-x: 0.5rem;
$navbar-dark-color: rgba(255, 255, 255, 0.85);
$navbar-toggler-border-radius: 0.375rem;

@import "bootstrap";
```

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
      </ul>
    </div>
  </div>
</nav>
```

**Card Organism**:
```scss
$card-spacer-y: 1rem;
$card-spacer-x: 1rem;
$card-border-width: 1px;
$card-border-radius: 0.5rem;
$card-border-color: rgba(0, 0, 0, 0.125);

@import "bootstrap";
```

**Form Organism**:
```scss
$form-label-margin-bottom: 0.5rem;
$form-label-font-size: 0.875rem;
$form-label-font-weight: 500;
$form-feedback-valid-color: $success;
$form-feedback-invalid-color: $danger;

@import "bootstrap";
```

## Common Mistakes

- **Wrong**: Not using `.navbar-expand-*` classes → **Right**: Required for responsive behavior
- **Wrong**: Mixing navbar color variants → **Right**: Use either `.navbar-light` OR `.navbar-dark`
- **Wrong**: Not including collapse/toggler → **Right**: Mobile navigation requires these
- **Wrong**: Using deprecated `.card-deck` → **Right**: Use grid system (`.row` + `.row-cols-*`)
- **Wrong**: Not using `.form-label` class → **Right**: Labels need this for proper styling
- **Wrong**: Not using grid for form layout → **Right**: Use Bootstrap grid (`.row` + `.col-*`)

## See Also

- [Molecules to Component Combinations](molecules-component-combinations.md)
- [Templates to Bootstrap Grid](templates-bootstrap-grid.md)
- Reference: [Bootstrap 5.3 Navbar](https://getbootstrap.com/docs/5.3/components/navbar/)
- Reference: [Bootstrap 5.3 Cards](https://getbootstrap.com/docs/5.3/components/card/)
- Reference: [Bootstrap 5.3 Forms](https://getbootstrap.com/docs/5.3/forms/overview/)
