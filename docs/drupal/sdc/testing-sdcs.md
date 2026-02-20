---
description: Testing strategies for SDC components including schema validation and visual regression
drupal_version: "11.x"
---

# Testing SDCs

## When to Use

> Use this when setting up component development workflow, testing components in isolation, or implementing visual regression testing.

## Decision

| Testing Method | Use Case | Tools |
|----------------|----------|-------|
| Schema validation | Catch prop/slot errors in development | Development environment settings |
| Storybook integration | Isolated component development | CL Server module |
| Manual testing | Variant and accessibility testing | Checklist-based approach |
| Visual regression | Automated screenshot comparison | BackstopJS, Percy, Playwright |

## Pattern

**Development Environment Validation:**
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

**Storybook Integration:**
```bash
# Install and enable
composer require drupal/cl_server drupal/cl_devel --dev
drush en cl_server cl_devel

# Access component library at /cl
```

**Manual Testing Checklist:**
- All defined variants (props enums)
- With/without optional slots
- With invalid props (should error in development)
- Mobile/tablet/desktop breakpoints
- Keyboard navigation (accessibility)
- Screen reader compatibility

## Common Mistakes

- **Wrong**: Not testing with schema validation enabled → **Right**: Enable in development to catch issues early (production doesn't validate)
- **Wrong**: Only testing default prop values → **Right**: Test all enum values and required/optional prop combinations

## See Also

- Reference: Schema validation documentation
- [Component YAML Schema](component-yaml-schema.md)
- [CL Server Module](https://www.drupal.org/project/cl_server)
- [SDC Styleguide Module](https://www.drupal.org/project/sdc_styleguide)
