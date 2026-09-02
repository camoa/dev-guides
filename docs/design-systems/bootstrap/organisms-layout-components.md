---
description: "Map organism-level components (navbars, complete cards, forms) to Bootstrap"
tldr: "Use this for mapping organisms (complex UI sections combining multiple molecules and atoms) like navbars and complete cards to Bootstrap's component system."
drupal_version: "11.x"
---

# Organisms → Layout + Components

## When to Use

> Use this for mapping organisms (complex UI sections combining multiple molecules and atoms) like navbars and complete cards to Bootstrap's component system.

- You've identified organisms (navbars, complete cards, forms) from your design system
- These are complex UI sections combining multiple molecules and atoms
- You need to implement large, self-contained components

## Navbar Organisms

### Decision Table: Navbar Implementation

| Design System Need | Bootstrap Variable | Bootstrap Classes | Custom Required |
|-------------------|-------------------|------------------|-----------------|
| Navbar base | `$navbar-padding-y`, `$navbar-padding-x` | `.navbar` | No |
| Navbar brand/logo | `$navbar-brand-*` variables | `.navbar-brand` | No |
| Navbar links | `$navbar-nav-link-padding-x` | `.navbar-nav` + `.nav-link` | No |
| Navbar light/dark | N/A | `.navbar-light`, `.navbar-dark` | No |
| Navbar background | Uses `$theme-colors` | `.bg-primary`, `.bg-dark` | No |
| Navbar toggler (mobile) | `$navbar-toggler-*` variables | `.navbar-toggler` | No |
| Navbar height | `$navbar-brand-height` | Calculated automatically | No |

### Pattern: Navbar Organism

**SCSS Customization:**
```scss
$navbar-padding-y: 0.5rem;
$navbar-padding-x: 1rem;
$navbar-brand-font-size: 1.25rem;
$navbar-brand-padding-y: 0.3125rem;
$navbar-nav-link-padding-x: 0.5rem;
$navbar-dark-color: rgba(255, 255, 255, 0.85);
$navbar-dark-hover-color: rgba(255, 255, 255, 1);
$navbar-toggler-border-radius: 0.375rem;

@import "bootstrap";
```

**HTML Structure:**
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

### Common Mistakes

- **Not using .navbar-expand-* classes** - Required for responsive behavior
- **Mixing navbar color variants** - Use either `.navbar-light` or `.navbar-dark` (not both)
- **Not including collapse/toggler** - Mobile navigation requires `.navbar-toggler` and `.collapse`
- **Hardcoding navbar heights** - Bootstrap calculates heights from brand/padding variables
- **Not using container** - Wrap navbar content in `.container` or `.container-fluid`

### See Also

- Bootstrap 5.3 Navbar: [https://getbootstrap.com/docs/5.3/components/navbar/](https://getbootstrap.com/docs/5.3/components/navbar/)
- Reference: Bootstrap 5.3 Navbar Variables `/core/scss/_navbar.scss`

## Card Organisms

### Decision Table: Complete Card Implementation

| Design System Need | Bootstrap Variable | Bootstrap Classes | Custom Required |
|-------------------|-------------------|------------------|-----------------|
| Card container | `$card-border-width`, `$card-border-radius` | `.card` | No |
| Card spacing | `$card-spacer-y`, `$card-spacer-x` | Applied to `.card-body` | No |
| Card image overlay | `$card-img-overlay-padding` | `.card-img-overlay` | No |
| Card groups | N/A | `.card-group`, `.row-cols-*` | No |
| Card borders | `$card-border-color` | `.border-*` utilities | No |
| Card backgrounds | Uses `$theme-colors` | `.bg-*`, `.text-bg-*` | No |

### Pattern: Card Organism

**SCSS Customization:**
```scss
$card-spacer-y: 1rem;
$card-spacer-x: 1rem;
$card-border-width: 1px;
$card-border-radius: 0.5rem;
$card-border-color: rgba(0, 0, 0, 0.125);
$card-cap-padding-y: 0.5rem;
$card-cap-bg: rgba(0, 0, 0, 0.03);

@import "bootstrap";
```

### Common Mistakes

- **Using deprecated .card-deck** - Use grid system (`.row` + `.row-cols-*`) instead
- **Not using card utilities** - Cards support all Bootstrap utilities (spacing, borders, shadows)
- **Creating custom card variants unnecessarily** - Use background utilities + text color utilities
- **Ignoring card image positioning** - Use `.card-img-top`, `.card-img-bottom`, or `.card-img-overlay`

### See Also

- Bootstrap 5.3 Cards: [https://getbootstrap.com/docs/5.3/components/card/](https://getbootstrap.com/docs/5.3/components/card/)
- Bootstrap 5.3 Grid: [https://getbootstrap.com/docs/5.3/layout/grid/](https://getbootstrap.com/docs/5.3/layout/grid/)

## Form Organisms

### Decision Table: Complete Form Implementation

| Design System Need | Bootstrap Variable | Bootstrap Classes | Custom Required |
|-------------------|-------------------|------------------|-----------------|
| Form layout | N/A | `.row`, `.col-*`, `.mb-3` | No |
| Form labels | `$form-label-*` variables | `.form-label` | No |
| Form controls | `$input-*` variables | `.form-control`, `.form-select` | No |
| Form validation | `$form-feedback-*` variables | `.was-validated`, `.valid-feedback` | No |
| Form text/help | `$form-text-*` variables | `.form-text` | No |
| Inline forms | N/A | Grid utilities + form classes | No |

### Pattern: Form Organism

**SCSS Customization:**
```scss
$form-label-margin-bottom: 0.5rem;
$form-label-font-size: 0.875rem;
$form-label-font-weight: 500;
$form-text-margin-top: 0.25rem;
$form-feedback-valid-color: $success;
$form-feedback-invalid-color: $danger;

@import "bootstrap";
```

**HTML Structure (custom validation):**
```html
<form class="row g-3 needs-validation" novalidate>
  <div class="col-md-4">
    <label for="validationCustom01" class="form-label">First name</label>
    <input type="text" class="form-control" id="validationCustom01" value="Mark" required>
    <div class="valid-feedback">Looks good!</div>
  </div>
  <div class="col-md-4">
    <label for="validationCustom02" class="form-label">Last name</label>
    <input type="text" class="form-control" id="validationCustom02" value="Otto" required>
    <div class="valid-feedback">Looks good!</div>
  </div>
  <div class="col-12">
    <button class="btn btn-primary" type="submit">Submit form</button>
  </div>
</form>
```

`novalidate` disables the browser's default validation UI. Bootstrap's `.valid-feedback`/`.invalid-feedback` styles only display once JavaScript adds the `.was-validated` class to the form on submit — the classes alone do nothing without that script.

### Common Mistakes

- **Not using form-label class** - Labels need `.form-label` for proper styling
- **Ignoring form validation feedback** - Bootstrap has built-in `.valid-feedback`/`.invalid-feedback`
- **Not using grid for form layout** - Use Bootstrap grid (`.row` + `.col-*`) for alignment
- **Creating custom validation states** - Use Bootstrap's validation system
- **Not considering accessibility** - Use proper `for` attributes on labels and `aria-describedby` for help text

### See Also

- Bootstrap 5.3 Forms: [https://getbootstrap.com/docs/5.3/forms/overview/](https://getbootstrap.com/docs/5.3/forms/overview/)
- Bootstrap 5.3 Form Validation: [https://getbootstrap.com/docs/5.3/forms/validation/](https://getbootstrap.com/docs/5.3/forms/validation/)

## See Also

- [Molecules → Component Combinations](molecules-component-combinations.md)
- [Templates → Bootstrap Grid](templates-bootstrap-grid.md)
