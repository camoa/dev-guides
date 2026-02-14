---
description: Debug when icons aren't appearing, pack definitions aren't loading, or icon IDs aren't resolving
drupal_version: "11.x"
---

# Troubleshooting Icon Discovery

## When to Use

Icons aren't appearing, pack definitions aren't loading, or icon IDs aren't resolving correctly.

## Decision

| Symptom | Likely cause | Debug method |
|---|---|---|
| Pack not listed | YAML syntax error | Check YAML validity, clear cache |
| Icons not found | File path mismatch | Verify source patterns match files |
| Wrong icon renders | Icon ID collision | Check multiple packs for same ID |
| No icons render | Template error | Check Twig syntax, template variables |
| Intermittent failures | Cache issues | Clear all caches, check cache tags |

## Pattern

Debug icon pack definitions:

```bash
# List all icon packs
drush php:eval "print_r(array_keys(\\Drupal::service('plugin.manager.icon_pack')->getDefinitions()));"

# Get specific pack definition
drush php:eval "print_r(\\Drupal::service('plugin.manager.icon_pack')->getDefinition('my_theme'));"

# Check if pack has icons
drush php:eval "print_r(\\Drupal::service('plugin.manager.icon_pack')->getIcons(['my_theme']));"
```

Validate YAML files:

```bash
# Check YAML syntax
drush php:eval "yaml_parse_file('themes/my_theme/my_theme.icons.yml');"

# Or use yamllint
yamllint themes/my_theme/my_theme.icons.yml
```

Debug icon file paths:

```bash
# Verify icon files exist
ls -la themes/my_theme/icons/

# Check if pattern matches files
# Pattern: icons/{icon_id}.svg
# File: icons/home.svg
# Should match: icon('my_theme:home')
```

Enable Twig debugging:

```yaml
# sites/default/services.yml
parameters:
  twig.config:
    debug: true
    auto_reload: true
    cache: false
```

Add debug output to template:

```twig
{# Temporary debug output #}
{{ dump({
  icon_id: icon_id,
  source: source,
  content: content|length ~ ' chars',
  settings: _context
}) }}

<svg>{{ content }}</svg>
```

Check extractor discovery:

```php
// In custom module or theme preprocess
function my_module_preprocess_page(&$variables) {
  $icon_manager = \Drupal::service('plugin.manager.icon_pack');
  $pack = $icon_manager->getDefinition('my_theme');

  \Drupal::logger('debug')->debug('<pre>@pack</pre>', [
    '@pack' => print_r($pack, TRUE),
  ]);
}
```

Reference: `/core/lib/Drupal/Core/Theme/Icon/Plugin/IconPackManager.php`

## Common Mistakes

- **Wrong**: Not clearing cache after YAML changes → **Right**: Run `drush cr` after every `*.icons.yml` modification
- **Wrong**: Case-sensitive icon IDs → **Right**: `home` ≠ `Home`, normalize IDs to lowercase
- **Wrong**: Extra spaces in YAML → **Right**: YAML is whitespace-sensitive, use consistent indentation
- **Wrong**: Missing file extensions in patterns → **Right**: Pattern `icons/{icon_id}` won't match `home.svg`, use `icons/{icon_id}.svg`
- **Wrong**: Debugging in production → **Right**: Enable Twig debug only in development, impacts performance

## See Also

- [Remote Resource Security](remote-resource-security.md)
- [Debugging Templates](debugging-templates.md)
- Reference: [Drupal logging](https://www.drupal.org/docs/develop/development-tools/logging-and-debugging)
