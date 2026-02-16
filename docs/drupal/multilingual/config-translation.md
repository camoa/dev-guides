---
description: Drupal config translation — translating views, menus, field labels, site name via config schema and translation UI
---

# Config Translation

### When to Use
When translating configuration entities and simple config: views, menus, field labels, site name, content type labels, block labels.

### Decision: What Config is Translatable

| Config type | Translatable? | Example |
|---|---|---|
| Views labels and descriptions | Yes | View title, exposed filter labels, header/footer text |
| Menu item titles | Yes | Menu link title and description |
| Field labels and descriptions | Yes | "Body", "Tags", help text |
| Content type names | Yes | "Article", "Basic page" |
| Block labels | Yes | Custom block label |
| Site name, slogan | Yes | System site settings |
| Module settings text | Depends | If schema marks it `type: label` or `translatable: true` |

### Pattern: How Config Translation Works

**Discovery process**:
1. Config Translation module scans config schema
2. Finds config with `type: label` or `type: text` marked `translatable: true`
3. Generates translation UI automatically

**Config schema example** — `views.schema.yml`:

```yaml
views.view.*:
  type: config_entity
  mapping:
    label:
      type: label  # <-- Marks as translatable
      label: 'Label'
    description:
      type: text
      label: 'Description'
      translatable: true  # <-- Explicit translatable
```

**Translation UI**:
- Navigate to config entity (e.g., view, menu, field)
- Click "Translate" tab
- Select language → add translation
- Enter translated values for translatable keys

**Translation storage**:
- Original config: `config/sync/views.view.frontpage.yml`
- Spanish translation: `config/sync/language/es/views.view.frontpage.yml`

**Spanish override example** — `language/es/views.view.frontpage.yml`:

```yaml
label: 'Página de inicio'
description: 'Vista de contenido de la página de inicio'
```

### Pattern: Making Custom Config Translatable

**Step 1**: Define config schema with translatable labels

**File**: `mymodule.schema.yml`

```yaml
mymodule.settings:
  type: config_object
  label: 'My Module Settings'
  mapping:
    page_title:
      type: label
      label: 'Page title'
    welcome_message:
      type: text
      label: 'Welcome message'
      translatable: true
```

**Step 2**: Implement config mapper (optional, for complex config)

Most simple config is automatically discovered. For custom UI integration, implement `ConfigMapperInterface`.

**Step 3**: Access translated config

```php
// Loads config with language override applied
$config = \Drupal::config('mymodule.settings');
$title = $config->get('page_title'); // Returns translated value

// Get language-specific config override
$language_manager = \Drupal::service('language_manager');
$config_override = $language_manager->getLanguageConfigOverride('es', 'mymodule.settings');
$title = $config_override->get('page_title'); // Returns Spanish value
```

### Common Mistakes

- **Forgetting to define config schema** → Config Translation requires schema to discover translatable keys. No schema = no translation UI
- **Using wrong schema type** → Use `type: label` for short text, `type: text` for longer text. Both auto-detected as translatable. Plain `type: string` is NOT translatable unless `translatable: true` added
- **Translating the wrong thing** → Don't translate machine names, IDs, or CSS classes. Only translate human-readable labels and descriptions
- **Exporting config without language overrides** → Config export includes base config but not translations. Export language-specific overrides separately from `config/sync/language/LANGCODE/`
- **Hardcoding text in forms instead of using config** → If text appears in custom forms, put it in config and mark translatable in schema. Hardcoded strings can use `t()` but aren't stored translatably

### See Also
- → [Interface Translation](interface-translation.md) — translating UI strings with t()
- → [Translating Custom Modules](translating-custom-modules.md) — making your module translatable
- Reference: `core/modules/config_translation/`
- Reference: https://www.drupal.org/docs/administering-a-drupal-site/multilingual-guide/translating-configuration
- Reference: https://www.drupal.org/project/drupal/issues/1648930 (config schema for translation)
