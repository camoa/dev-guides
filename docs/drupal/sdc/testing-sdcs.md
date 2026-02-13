---
description: Testing components with schema validation, Storybook, and visual regression
drupal_version: "11.x"
---

# Testing SDCs

## When to Use

> Use this when setting up component development workflow, testing components in isolation, or implementing visual regression testing.

## Decision: Testing Strategy

| Strategy | Tool/Pattern | Purpose |
|----------|--------------|---------|
| Schema validation | `enforce_sdc_schemas: true` in theme.info.yml | Catch prop validation errors in development |
| Component library | CL Server module | Storybook-style component browsing |
| Manual testing | Variants, slots, breakpoints checklist | Ensure all combinations work |
| Visual regression | BackstopJS, Percy, Playwright | Automated screenshot comparison |

## Pattern

Development environment validation:

```php
// In settings.local.php
assert_options(ASSERT_ACTIVE, TRUE);
\Drupal\Component\Assertion\Handle::register();
ini_set('zend.assertions', 1);
```

```yaml
# In theme.info.yml
enforce_sdc_schemas: true
```

**WHY**: Schema validation only runs in development (performance). Enables strict prop validation and descriptive errors.

Storybook integration with CL Server:

```bash
# Install and enable
composer require drupal/cl_server drupal/cl_devel --dev
drush en cl_server cl_devel

# Access component library at /cl
```

Manual testing checklist:

- All defined variants (props enums)
- With/without optional slots
- With invalid props (should error in development)
- Mobile/tablet/desktop breakpoints
- Keyboard navigation (accessibility)
- Screen reader compatibility

Visual regression testing tools:

- **BackstopJS** - Screenshot comparison
- **Percy** - Visual testing platform
- **Playwright** - End-to-end testing with screenshots

## Common Mistakes

- **Wrong**: Not testing with schema validation enabled → **Right**: Production doesn't validate schemas. Bugs only surface in production if not tested with validation in development.
- **Wrong**: Only testing default prop values → **Right**: Variations and edge cases often have bugs. Test all enum values and required/optional prop combinations.

## See Also

- [Component YAML Schema](component-yaml-schema.md)
- [CL Server Module](https://www.drupal.org/project/cl_server)
- [SDC Styleguide Module](https://www.drupal.org/project/sdc_styleguide)
