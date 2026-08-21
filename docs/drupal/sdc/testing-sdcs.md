---
description: "Enabling prop-schema validation in development with the correct key, and testing every slot call path separately"
tldr: "The theme key is enforce_prop_schemas, not enforce_sdc_schemas — a misspelling turns nothing on and reports nothing. Production never validates props (the check is assert()-gated), so development with zend.assertions=1 is the only place a schema violation surfaces; test each slot call path (embed, include, render element) individually since the render element hides embed-only bugs."
drupal_version: "11.x"
---

# Testing SDCs

## When to Use

> Use this when you're setting up a component development workflow, you need to test components in isolation, or you're implementing visual regression testing.

## Decision

Enable schema validation in development to catch errors early — it is the only environment where a schema violation is ever visible.

```php
// In settings.local.php
assert_options(ASSERT_ACTIVE, TRUE);
\Drupal\Component\Assertion\Handle::register();
ini_set('zend.assertions', 1);
```

```yaml
# In theme.info.yml — the key is enforce_prop_schemas, NOT enforce_sdc_schemas
enforce_prop_schemas: true
```

**WHY the exact key matters:** `ComponentPluginManager::shouldEnforceSchemas()` reads `->info['enforce_prop_schemas'] ?? FALSE` (`:462`). `.info.yml` accepts arbitrary keys, so a misspelling such as `enforce_sdc_schemas` turns nothing on and reports nothing — you ship components whose schemas were never checked while believing they were.

**What the two switches do, separately:**
- `zend.assertions=1` + `Handle::register()` is what makes prop validation run at all. It is `assert()`-gated at the call site (`ComponentsTwigExtension.php:106`), so on a production `zend.assertions=-1` no prop is ever checked, regardless of any `.info.yml` key.
- `enforce_prop_schemas: true` makes a **theme's** components *require* a `props` schema, and switches on `ComponentNodeVisitor::validateSlots()` (which only fires when `mandatorySchemas` is set). **Components declared in modules always enforce schemas** — `shouldEnforceSchemas()` returns TRUE for any non-theme provider — so this key is a theme-only concern.

Turn both on in development. Neither is a production safety net.

## Pattern

**Storybook Integration** — use CL Server module for a Storybook-style component library.

```bash
# Install and enable
composer require drupal/cl_server drupal/cl_devel --dev
drush en cl_server cl_devel

# Access component library at /cl
```

**Manual Testing Checklist:**
- All defined variants (props enums).
- With/without optional slots.
- With invalid props (should error in development).
- Mobile/tablet/desktop breakpoints.
- Keyboard navigation (accessibility).
- Screen reader compatibility.

**And test every call path you support.** A slot bug is usually path-specific: a `{% block %}` a caller can only fill from `{% embed %}`, a bare `{{ slot }}` a caller can only fill from `include()`, and `#type: component`, which fills both and therefore hides both failures. If the component is intended for `{% embed %}`, exercise it from a real `{% embed %}` — testing it through the render element proves nothing about that path.

**Visual Regression Testing** — consider tools for automated visual testing: BackstopJS (screenshot comparison), Percy (visual testing platform), Playwright (end-to-end testing with screenshots).

## Common Mistakes

- **Wrong**: Not testing with schema validation enabled → **Right**: Production doesn't validate props — the check is compiled out with assertions off. Development is the *only* place a schema error can surface, so a component never rendered under assertions has effectively never been schema-checked.
- **Wrong**: Treating a green run under `enforce_prop_schemas` as proof the slots are right → **Right**: Slot validation reports only slots you passed but never declared. A declared slot nobody filled, or a slot whose block is unreachable behind an `{% if %}`, passes every check core has.
- **Wrong**: Only testing default prop values → **Right**: Variations and edge cases often have bugs. Test all enum values and required/optional prop combinations.

## See Also

- [Component YAML Schema](component-yaml-schema.md)
- [CL Server Module](https://www.drupal.org/project/cl_server)
- [SDC Styleguide Module](https://www.drupal.org/project/sdc_styleguide)
