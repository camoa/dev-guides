---
description: Drupal interface translation — importing .po files, custom module translations, generating .pot templates, locale management
---

# Interface Translation

### When to Use
When translating UI strings, system messages, form labels, module-provided text — anything wrapped in `t()` or `TranslatableMarkup`.

### Decision: Translation Source

| If you need... | Use... | Why |
|---|---|---|
| Import official Drupal translations | Update Manager + locale.drupal.org | Maintained by community, covers core and contrib |
| Custom module translations | .po files in module/translations/ | Package translations with module |
| Manual string translation | UI at `/admin/config/regional/translate` | Override or add missing translations |
| Export custom translations | Locale export at `/admin/config/regional/translate/export` | Share or backup translations |

### Pattern: Importing Translations

**Automatic import (recommended)**:
1. Enable Locale and Interface Translation modules
2. Add languages at `/admin/config/regional/language`
3. Drupal automatically downloads translations from localize.drupal.org
4. Updates check for new translations periodically

**Manual .po file import**:
1. Go to `/admin/config/regional/translate/import`
2. Select language
3. Upload .po file
4. Choose import options:
   - Treat imported strings as custom (overrides future updates)
   - Treat imported strings as non-custom (can be updated)

**Programmatic import** (via batch API):

```php
use Drupal\locale\Gettext;

$file = new \stdClass();
$file->uri = 'public://translations/es.po';
$file->filename = 'es.po';
$file->langcode = 'es';

$options = [
  'langcode' => 'es',
  'overwrite_options' => [
    'customized' => FALSE,
    'not_customized' => TRUE,
  ],
  'customized' => LOCALE_NOT_CUSTOMIZED,
];

// Use Gettext parser for direct import
Gettext::fileToDatabase($file, $options);
```

### Pattern: Custom Module .po Files

**Directory structure**:
```
mymodule/
  mymodule.info.yml
  translations/
    mymodule.es.po
    mymodule.fr.po
```

**mymodule.info.yml** — tell Locale where to find .po files:

```yaml
name: My Module
type: module
core_version_requirement: ^10 || ^11
'interface translation project': mymodule
'interface translation server pattern': modules/custom/mymodule/translations/%project.%language.po
```

**mymodule.es.po** — Gettext format:

```po
msgid ""
msgstr ""
"Project-Id-Version: My Module\n"
"POT-Creation-Date: 2026-02-16\n"
"Language: es\n"

msgid "Submit"
msgstr "Enviar"

msgid "Welcome, @name!"
msgstr "¡Bienvenido, @name!"

msgctxt "Long month name"
msgid "May"
msgstr "Mayo"
```

**Automatic discovery**:
- Drupal scans for `t()` and `TranslatableMarkup` calls
- Extracts source strings to .pot file
- Translators create .po files with translations
- Locale module imports .po files on module enable or via UI

### Pattern: Generating .pot Files

**Using Drush**:

```bash
# Generate .pot from module
drush locale:export --langcode=en --template --types=customized > mymodule.pot

# Or use potx module (contrib)
drush potx module mymodule
```

**Using Translation Template Extractor (Potx) module**:
- Install Potx module: `composer require drupal/potx`
- UI: `/admin/config/regional/translate/extract`
- Select module, generate .pot file

### Common Mistakes

- **Forgetting 'interface translation project' in .info.yml** → Locale module won't discover your .po files. Must define project name and server pattern
- **Using wrong .po file naming** → Must be `PROJECT.LANGCODE.po` (e.g., `mymodule.es.po`). Wrong naming prevents import
- **Not exporting custom translations** → Custom manual translations entered via UI are lost on re-import unless exported first
- **Translating user-entered content with t()** → NEVER wrap user input in `t()`. Security risk (XSS). [TranslatableMarkup & t()](translatable-markup.md) for details
- **Hardcoding non-English strings** → All source strings in code should be English. Translators translate from English source

### See Also
- → [TranslatableMarkup & t()](translatable-markup.md) — using translation API correctly
- → [Translating Custom Modules](translating-custom-modules.md) — complete module translation workflow
- Reference: `core/modules/locale/locale.api.php`
- Reference: https://www.drupal.org/docs/administering-a-drupal-site/multilingual-guide/translating-site-interfaces
- Reference: https://localize.drupal.org (official translation server)
