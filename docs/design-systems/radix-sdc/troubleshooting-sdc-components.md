---
description: Your SDC component isn't being discovered by Drupal
drupal_version: "11.x"
---

## 9. Troubleshooting SDC Components

### When to Use This Section
- Your SDC component isn't being discovered by Drupal
- Bootstrap classes aren't being applied correctly in your component
- You need to debug component registration or rendering issues
- You've replaced/overridden a Radix component and it's not working

### Decision Table: Common Issues and Solutions

| Problem | Root Cause | Solution |
|---------|-----------|----------|
| Component not discovered | File structure incorrect or cache stale | Verify directory structure, clear theme cache |
| Bootstrap classes not applied | Utility class merging broken in Twig | Check `attributes.addClass()` usage in template |
| Color inheritance broken | Bootstrap variables not imported | Ensure `@import '_init.scss';` in component SCSS |
| JavaScript conflicts | Drupal.behaviors not used | Wrap JS in `Drupal.behaviors` pattern |
| Component renders blank | YAML schema errors | Validate YAML syntax, check required props |
| Wrong component loads | Namespace collision | Check component discovery order, clear cache |

### Pattern: Debug Commands

#### Verify Component Discovery
```bash
# List all discovered SDC components (shows if your component registered)
drush php:eval "print_r(array_keys(\\Drupal::service('plugin.manager.sdc')->getDefinitions()));"

# Get full definition for specific component
drush php:eval "\$def = \\Drupal::service('plugin.manager.sdc')->getDefinition('THEME_NAME:button'); print_r(\$def);"

# Clear theme cache only (faster than full cache rebuild)
drush cr theme

# Full cache rebuild if theme cache insufficient
drush cr
```

#### Check Component File Structure
```bash
# Verify all required files exist
ls -la /path/to/theme/components/button/

# Should see:
# - button.component.yml (required)
# - button.twig (required)
# - button.scss (optional)
# - button.js (optional)
# - README.md (recommended)

# Find all component definitions in your theme
find /path/to/theme/components -name "*.component.yml"
```

#### Validate YAML Syntax
```bash
# Check for YAML syntax errors
php -r "yaml_parse_file('/path/to/theme/components/button/button.component.yml');"

# Or use Symfony YAML Lint if available
bin/console lint:yaml /path/to/theme/components/button/button.component.yml
```

#### Check Component Namespace Usage
```bash
# Search for component include statements in templates
grep -r "{% include 'THEME_NAME:button'" /path/to/theme/templates/

# Verify namespace matches theme name in .info.yml
grep "^name:" /path/to/theme/THEME_NAME.info.yml
```

### Validation Checklist

Use this checklist when troubleshooting a non-functional SDC component:

- [ ] **Files copied completely** — All files from source (Radix) copied to sub-theme
- [ ] **Directory structure correct** — Component in `themes/custom/THEME_NAME/components/`
- [ ] **YAML schema valid** — No syntax errors in `.component.yml`
- [ ] **Required files present** — Both `.component.yml` and `.twig` exist
- [ ] **Namespace correct** — Using `THEME_NAME:component-id` in includes
- [ ] **Theme cache cleared** — Run `drush cr theme` after creating/modifying component
- [ ] **Bootstrap utility class integration maintained** — Props use `utility_classes` pattern
- [ ] **Color system compatibility preserved** — SCSS imports `_init.scss` for Bootstrap vars
- [ ] **Twig syntax valid** — No template errors when component renders
- [ ] **Props have defaults** — Required props have sensible default values
- [ ] **Slots properly defined** — Slot names match between YAML and Twig
- [ ] **SCSS properly scoped** — Component CSS uses BEM or unique namespace
- [ ] **JavaScript wrapped in behaviors** — JS uses `Drupal.behaviors.COMPONENT_NAME`
- [ ] **Responsive behavior verified** — Tested across Bootstrap breakpoints
- [ ] **Accessibility checked** — ARIA attributes and focus management in place
- [ ] **Performance optimized** — Libraries loaded conditionally, not globally
- [ ] **Documentation updated** — README.md explains customizations and usage

### Common Mistakes

- **Not clearing theme cache after changes** — Drupal caches component definitions. **WHY:** The SDC plugin manager caches discovered components for performance. Until you clear the theme cache, Drupal doesn't know about new/changed components.

- **Missing `@import '_init.scss';` in component SCSS** — Bootstrap variables unavailable. **WHY:** Each SDC SCSS file is compiled independently. Without importing `_init.scss`, the component has no access to Bootstrap variables, mixins, or functions.

- **Using relative paths in component includes** — Use namespace syntax. **WHY:** SDC components must be referenced by namespace (`THEME_NAME:button`), not file paths. The SDC system uses namespaces to handle component discovery and override priority.

- **Editing Radix base theme files directly** — Updates will overwrite changes. **WHY:** Contrib modules/themes in `themes/contrib/` are managed by Composer. Any manual edits will be lost on the next `composer update`. Always copy to your sub-theme instead.

- **Forgetting `.component.yml` or `.twig` file** — Component won't be discovered. **WHY:** Both files are required by the SDC specification. The YAML defines the component schema, and the Twig provides the template. Missing either makes the component invalid.

- **YAML syntax errors** — Silent failure or PHP errors. **WHY:** Invalid YAML causes parse errors. Drupal may fail silently during discovery or throw exceptions when trying to use the component.

- **Not using `attributes.addClass()` in Twig** — Loses Drupal integration. **WHY:** The `attributes` object contains classes, IDs, and data attributes passed from Drupal's render system. Not using it breaks field formatters, views integration, and contextual links.

- **Complex logic in Twig templates** — Hard to maintain and test. **WHY:** Twig is a presentation layer, not a programming language. Complex logic belongs in preprocess functions where it can be unit tested and properly cached.

- **No default values for props** — Component breaks with missing data. **WHY:** If a prop is required but has no default, and the component is used without passing that prop, the component will either error or render incorrectly.

- **Hardcoding design tokens instead of using Bootstrap variables** — Creates inconsistency. **WHY:** Hardcoded values won't update when Bootstrap variables change. Using Bootstrap variables (`var(--bs-primary)` or `$primary`) ensures design consistency.

### See Also
- [3.2 SDC Component Structure](#32-sdc-component-structure)
- [7.1 Component YAML Schema](#71-component-yaml-schema)
- [8.3 Overriding Radix Components](#83-overriding-radix-components)
- [3.6 Radix Sub-Theme Best Practices](#36-radix-sub-theme-best-practices)