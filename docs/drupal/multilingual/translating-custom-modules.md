---
description: Drupal custom module translation — translatable strings, config schema, .po files, JavaScript translation, custom entities
---

# Translating Custom Modules

### When to Use
When developing custom modules that need to support multilingual sites — providing translatable strings, config, and .po files.

### Decision: What to Make Translatable

| Element type | How to make translatable | Example |
|---|---|---|
| UI strings in code | Wrap in `$this->t()` or `TranslatableMarkup` | Form labels, messages |
| Config values | Define in schema as `type: label` | Module settings, default text |
| Entity labels | Use translation handlers | Custom entity type names |
| Plugin annotations | Use `@Translation` annotation | Plugin names, descriptions |
| JavaScript strings | Use `Drupal.t()` | JS UI messages |

### Pattern: Translatable Strings in Code

**Form example**:

```php
namespace Drupal\mymodule\Form;

use Drupal\Core\Form\ConfigFormBase;
use Drupal\Core\StringTranslation\StringTranslationTrait;

class SettingsForm extends ConfigFormBase {
  use StringTranslationTrait;

  public function buildForm(array $form, FormStateInterface $form_state) {
    $form['title'] = [
      '#type' => 'textfield',
      '#title' => $this->t('Page title'),
      '#description' => $this->t('Enter the title to display.'),
      '#default_value' => $this->config('mymodule.settings')->get('title'),
    ];

    $form['actions']['submit'] = [
      '#type' => 'submit',
      '#value' => $this->t('Save configuration'),
    ];

    return $form;
  }
}
```

**Plugin annotation**:

```php
use Drupal\Core\Annotation\Translation;

/**
 * Provides a custom block.
 *
 * @Block(
 *   id = "mymodule_custom_block",
 *   admin_label = @Translation("Custom Block"),
 *   category = @Translation("Custom"),
 * )
 */
class CustomBlock extends BlockBase {
  // ...
}
```

### Pattern: Translatable Config Schema

**Config file** (`config/install/mymodule.settings.yml`):

```yaml
page_title: 'Welcome to our site'
welcome_message: 'Thank you for visiting.'
```

**Schema file** (`config/schema/mymodule.schema.yml`):

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

**Result**: Config Translation UI automatically discovers and allows translating these values.

### Pattern: Providing .po Files

**Directory structure**:
```
mymodule/
  mymodule.info.yml
  translations/
    mymodule.es.po
    mymodule.fr.po
```

**mymodule.info.yml**:

```yaml
name: My Module
type: module
core_version_requirement: ^10 || ^11
'interface translation project': mymodule
'interface translation server pattern': modules/custom/mymodule/translations/%project.%language.po
```

**Generate .pot template** (using Potx module):

```bash
# Install Potx
composer require drupal/potx
drush en potx

# Generate .pot file
drush potx module mymodule
# Creates mymodule.pot in module root
```

**Create .po files from .pot**:
- Copy `mymodule.pot` to `translations/mymodule.es.po`
- Translate strings in .po file
- Repeat for each language

**Example .po** (`translations/mymodule.es.po`):

```po
msgid ""
msgstr ""
"Project-Id-Version: My Module\n"
"Language: es\n"

msgid "Page title"
msgstr "Título de página"

msgid "Enter the title to display."
msgstr "Ingrese el título a mostrar."

msgid "Save configuration"
msgstr "Guardar configuración"
```

### Pattern: JavaScript Translation

**JavaScript file**:

```javascript
(function (Drupal) {
  'use strict';

  Drupal.behaviors.myModule = {
    attach: function (context, settings) {
      // Translate strings in JavaScript
      var message = Drupal.t('Hello, @name!', {'@name': settings.userName});

      // Plural form
      var count = 5;
      var itemsText = Drupal.formatPlural(count, '1 item', '@count items');

      // With context
      var month = Drupal.t('May', {}, {context: 'Long month name'});
    }
  };
})(Drupal);
```

**Strings extracted to .pot automatically** if using Potx with `--api-version` flag.

### Pattern: Custom Entity Translation

**Enable translation for custom entity**:

```php
/**
 * @ContentEntityType(
 *   id = "myentity",
 *   label = @Translation("My Entity"),
 *   handlers = {
 *     "translation" = "Drupal\content_translation\ContentTranslationHandler",
 *   },
 *   translatable = TRUE,
 *   // ...
 * )
 */
class MyEntity extends ContentEntityBase {
  // ...
}
```

**Field definitions**:

```php
public static function baseFieldDefinitions(EntityTypeInterface $entity_type) {
  $fields['title'] = BaseFieldDefinition::create('string')
    ->setLabel(t('Title'))
    ->setTranslatable(TRUE); // Make field translatable

  $fields['created'] = BaseFieldDefinition::create('created')
    ->setLabel(t('Created'))
    ->setTranslatable(FALSE); // Non-translatable

  return $fields;
}
```

### Common Mistakes

- **Forgetting 'interface translation project' in .info.yml** → Locale module won't discover your .po files
- **Not using StringTranslationTrait** → Using global `t()` instead of `$this->t()` makes testing harder
- **Hardcoding strings instead of using t()** → Any user-visible text must be wrapped in `t()` or `TranslatableMarkup`
- **Missing @Translation annotation** → Plugin labels won't be translatable without `@Translation()` wrapper
- **Not defining translatable in schema** → Config values won't appear in Config Translation UI without schema
- **Forgetting to regenerate .pot after string changes** → New strings won't be in .po files for translators

### See Also
- → [Interface Translation](interface-translation.md) — .po file management
- → [TranslatableMarkup & t()](translatable-markup.md) — translation API
- → [Config Translation](config-translation.md) — config schema
- Reference: `core/modules/locale/locale.api.php`
- Reference: https://www.drupal.org/docs/8/api/translation-api/overview
