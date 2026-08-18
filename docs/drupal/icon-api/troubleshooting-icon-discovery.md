---
description: "Symptom-to-cause table for icon discovery failures — including when json-schema validation is skipped and what exception fires when"
tldr: "Icons aren't appearing or pack IDs aren't resolving; without justinrainbow/json-schema, validateDefinition() returns TRUE unconditionally and a bad pack fails later at render time with IconPackConfigErrorException instead."
drupal_version: "11.x"
---

# Troubleshooting Icon Discovery

## When to Use

Icons aren't appearing, pack definitions aren't loading, or icon IDs aren't resolving correctly.

## Decision

| Symptom | Likely cause | Debug method |
|---|---|---|
| Pack not listed | YAML syntax error, or a top-level `$schema:` key | Check YAML validity, remove `$schema`, rebuild cache |
| Pack listed but `icons` is empty | Remote source on `svg`/`svg_sprite`, or a disallowed local extension (`.webp`, `.woff2`) | Check dblog for "Invalid icon path extension" / "No icon found in source" |
| Icons not found | Source pattern does not match, or discovery is not recursive | Verify the pattern, remember `Finder::depth(0)` |
| Wrong icon renders | Icon ID collision across sources in the same pack | Later source wins; check every `sources:` entry |
| Nothing renders, no error | `icon()` given an unknown pack/icon, or `#pack`/`#icon` instead of `#pack_id`/`#icon_id` | `getIconRenderable()` returns `[]` for empty IDs |
| `ArgumentCountError` / `TypeError` on `icon` | `icon('pack:id')` or `icon('pack:id', {…})` | Use three arguments |
| `IconPackConfigErrorException` at cache rebuild | Bad pack ID, missing `extractor`/`template`, missing `config: sources` | Read the exception message; it names the provider and pack |
| Changes to `*.icons.yml` not taking effect | Nothing watches the file | `drush cr` after every edit |

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

Validate YAML files. `yaml_parse_file()` is a PECL extension function and is usually absent; use Drupal's own serializer:

```bash
# Check YAML syntax with the serializer Drupal actually uses
drush php:eval "print_r(\\Drupal\\Component\\Serialization\\Yaml::decode(file_get_contents('themes/my_theme/my_theme.icons.yml')));"

# Or use yamllint
yamllint themes/my_theme/my_theme.icons.yml
```

Full schema validation only runs when `justinrainbow/json-schema` is installed (`IconPackManager::setValidator()`). Without it, a malformed definition passes discovery and fails later at render time instead:

```bash
composer require --dev justinrainbow/json-schema
drush cr   # definitions are now validated against icon_pack.schema.json
```

Debug icon file paths:

```bash
# Verify icon files exist
ls -la themes/my_theme/icons/

# Check if pattern matches files
# Pattern: icons/{icon_id}.svg
# File: icons/home.svg
# Should match: icon('my_theme', 'home')
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

- **Wrong**: Not clearing cache after YAML changes → **Right**: Run `drush cr` after every `*.icons.yml` modification; nothing invalidates on file change
- **Wrong**: Adding `$schema:` to `*.icons.yml` → **Right**: Breaks discovery for the whole site
- **Wrong**: Case-sensitive icon IDs → **Right**: `home` ≠ `Home`; IDs come straight from filenames with no normalisation
- **Wrong**: Assuming validation ran → **Right**: Without `justinrainbow/json-schema`, `validateDefinition()` returns TRUE unconditionally
- **Wrong**: Missing file extensions in patterns → **Right**: Pattern `icons/{icon_id}` matches `{svg,png,gif}`; a wrong explicit extension matches nothing
- **Wrong**: Debugging in production → **Right**: Enable Twig debug only in development, impacts performance

## See Also

- [Remote Resource Security](remote-resource-security.md)
- [Debugging Templates](debugging-templates.md)
- Reference: [Drupal logging](https://www.drupal.org/docs/develop/development-tools/logging-and-debugging)
