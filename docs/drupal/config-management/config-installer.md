---
description: Provide default configuration that installs when a module is enabled — content types, views, fields, settings.
---

# Config Installer (Module Install)

## When to Use

When your module needs to provide default configuration that's installed when the module is enabled — content types, views, fields, module settings.

## Workflow

**On Module Install:**
1. **Install default config** — Files from `config/install/` imported
2. **Check dependencies** — Config dependencies must be satisfied
3. **Validate schema** — Config validated against schema
4. **Save to active storage** — Config written to database
5. **Install optional config** — Files from `config/optional/` imported if dependencies met

## Directory Structure

```
mymodule/
├── config/
│   ├── install/           # Required config, always installed
│   │   ├── mymodule.settings.yml
│   │   ├── node.type.custom_type.yml
│   │   └── views.view.custom_view.yml
│   ├── optional/          # Optional config, installed if dependencies met
│   │   ├── field.storage.node.custom_field.yml  # Requires field module
│   │   └── block.block.custom_block.yml         # Requires block module
│   └── schema/
│       └── mymodule.schema.yml  # Config schema
```

**Reference:** `/core/lib/Drupal/Core/Config/ConfigInstaller.php`

## Example: Module Settings

```yaml
# mymodule/config/install/mymodule.settings.yml
api_key: ''
enabled: false
max_items: 10
notification_email: ''
```

## Example: Config Entity

```yaml
# mymodule/config/install/mymodule.example.default.yml
id: default
label: 'Default Example'
description: 'Default example configuration'
weight: 0
status: true
langcode: en
dependencies:
  enforced:
    module:
      - mymodule
```

## Install vs Optional Config

**Install Config (`config/install/`):**
- Always imported on module enable
- Must have dependencies satisfied
- Module won't install if dependencies missing
- Use for: Core module functionality, required settings

**Optional Config (`config/optional/`):**
- Imported only if dependencies satisfied
- Module installs even if dependencies missing
- Use for: Integration with optional modules, example content

## Example: Optional Field Config

```yaml
# mymodule/config/optional/field.storage.node.custom_field.yml
# Only installed if Node module enabled
id: node.custom_field
field_name: custom_field
entity_type: node
type: string
settings:
  max_length: 255
dependencies:
  module:
    - node
```

## Updating Config After Install

**Config updates NOT automatic** — Changing files in `config/install/` doesn't update already-installed config. Options:

1. **Update hook** — Modify config programmatically in `hook_update_N()`
   ```php
   function mymodule_update_10001() {
     $config = \Drupal::configFactory()->getEditable('mymodule.settings');
     $config->set('new_setting', 'default_value')->save();
   }
   ```

2. **Config import** — Export updated config, users import via `drush cim`

3. **Config revert** — Use Config Revert module to reset to default

## Config on Module Uninstall

**Default behavior:**
- Config with enforced module dependency deleted
- Config without enforced dependency remains

**Enforcing deletion:**
```yaml
# Ensures config deleted on module uninstall
dependencies:
  enforced:
    module:
      - mymodule
```

**Manual cleanup:**
```php
function mymodule_uninstall() {
  // Delete config manually
  \Drupal::configFactory()->getEditable('mymodule.settings')->delete();

  // Delete all config with prefix
  $config_factory = \Drupal::configFactory();
  foreach ($config_factory->listAll('mymodule.') as $config_name) {
    $config_factory->getEditable($config_name)->delete();
  }
}
```

## Common Mistakes

- No enforced dependencies — Config not deleted on uninstall, orphaned in database
- Missing schema — Config imported but not validated, type coercion fails
- Config in wrong directory — `config/install` typos, config not found
- Changing install config after release — Existing installs not updated, need update hook
- Optional config without dependencies — Imported even when dependencies missing
- Hardcoded UUIDs — UUID conflicts on multi-site or re-install

## See Also

- [Config Entities](config-entities.md) — creating config entities
- [Config Dependencies](config-dependencies.md) — dependency management
- [Config & Recipes Integration](config-and-recipes-integration.md) — Recipes for config distribution
- Reference: [Providing Default Configuration](https://www.drupal.org/docs/drupal-apis/configuration-api/providing-default-configuration)
