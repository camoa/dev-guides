---
description: Drupal multilingual code reference — core modules, services, entity translation API, config schema paths, hooks, debugging helpers
---

# Code Reference Map

### When to Use
When exploring core translation code, understanding architecture, or debugging translation issues.

### Core Modules

**Language** — `core/modules/language/`
- Language entity, negotiation, language types
- Key files:
  - `language.api.php` — hooks documentation
  - `language.services.yml` — DI services
  - `src/LanguageNegotiator.php` — negotiation logic
  - `src/Plugin/LanguageNegotiation/` — negotiation method plugins

**Locale** — `core/modules/locale/`
- Interface translation, .po files, string storage
- Key files:
  - `locale.api.php` — hooks documentation
  - `src/LocaleTranslation.php` — translation service
  - `src/StringStorageInterface.php` — translation string storage

**Content Translation** — `core/modules/content_translation/`
- Entity translation, field translatability
- Key files:
  - `src/ContentTranslationHandler.php` — translation handler
  - `src/ContentTranslationManager.php` — manager service
  - `src/ContentTranslationMetadataWrapper.php` — translation metadata
  - `content_translation.admin.inc` — field sync UI (deprecated 11.4.0)

**Config Translation** — `core/modules/config_translation/`
- Configuration translation, schema-based discovery
- Key files:
  - `src/ConfigMapperManager.php` — discovers translatable config
  - `src/ConfigEntityMapper.php` — config entity translation
  - `src/ConfigNamesMapper.php` — simple config translation

### Core Services

```php
// Language manager
$language_manager = \Drupal::languageManager();
$current_language = $language_manager->getCurrentLanguage();
$default_language = $language_manager->getDefaultLanguage();
$languages = $language_manager->getLanguages();

// Language negotiator
$negotiator = \Drupal::service('language_negotiator');

// String translation
$translation = \Drupal::service('string_translation');
$translated = $translation->translate('Hello');

// Content translation manager
$ct_manager = \Drupal::service('content_translation.manager');
$handler = $ct_manager->getTranslationHandler('node');

// Config translation mapper manager
$mapper_manager = \Drupal::service('plugin.manager.config_translation.mapper');
```

### Entity Translation API

**File**: `core/lib/Drupal/Core/Entity/ContentEntityBase.php`

```php
// Key methods (line numbers approximate)
addTranslation($langcode, $values)      // Line ~997
getTranslation($langcode)               // Line ~893
hasTranslation($langcode)               // Line ~980
removeTranslation($langcode)            // Line ~1018
getTranslationLanguages()               // Line ~1057
isTranslatable()                        // Line ~878
```

### TranslatableMarkup API

**File**: `core/lib/Drupal/Core/StringTranslation/TranslatableMarkup.php`

```php
// Constructor
__construct($string, array $arguments = [], array $options = [], TranslationInterface $string_translation = NULL)

// Options array keys:
// - 'langcode': Target language
// - 'context': Translation context for disambiguation
```

### Language Negotiation Plugins

**Directory**: `core/modules/language/src/Plugin/LanguageNegotiation/`

- `LanguageNegotiationUrl.php` — URL (prefix or domain)
- `LanguageNegotiationSession.php` — Session/query parameter
- `LanguageNegotiationUI.php` — User preference
- `LanguageNegotiationBrowser.php` — Accept-Language header
- `LanguageNegotiationSelected.php` — Default language

### Config Schema Paths

```
core/modules/language/config/schema/language.schema.yml
core/modules/content_translation/config/schema/content_translation.schema.yml
core/modules/config_translation/config/schema/config_translation.schema.yml
```

### Hooks

**Language module hooks** — `language.api.php`:
- `hook_language_types_info()` — define custom language types
- `hook_language_types_info_alter()` — alter language types
- `hook_language_negotiation_info_alter()` — alter negotiation methods
- `hook_language_fallback_candidates_alter()` — alter fallback languages

**Locale module hooks** — `locale.api.php`:
- `hook_locale_translation_projects_alter()` — alter translation projects

### TMGMT (Contrib)

**Module**: `modules/contrib/tmgmt/`

- `src/Entity/Job.php` — translation job entity
- `src/Entity/JobItem.php` — job item (content to translate)
- `src/TranslatorPluginInterface.php` — translator plugin interface
- `src/SourcePluginInterface.php` — translation source plugin

**Key services**:

```php
// Job queue
$job_queue = \Drupal::service('tmgmt.job_queue');

// Source manager
$source_manager = \Drupal::service('plugin.manager.tmgmt.source');

// Translator manager
$translator_manager = \Drupal::service('plugin.manager.tmgmt.translator');
```

### Debugging Helpers

```php
// Check current language context
$interface_lang = \Drupal::languageManager()->getCurrentLanguage(LanguageInterface::TYPE_INTERFACE)->getId();
$content_lang = \Drupal::languageManager()->getCurrentLanguage(LanguageInterface::TYPE_CONTENT)->getId();
$url_lang = \Drupal::languageManager()->getCurrentLanguage(LanguageInterface::TYPE_URL)->getId();

// Dump negotiation methods and weights
$negotiation_info = \Drupal::service('language_negotiator')->getNegotiationMethods();
var_dump($negotiation_info);

// Check if entity is translatable
$entity_type = \Drupal::entityTypeManager()->getDefinition('node');
var_dump($entity_type->isTranslatable()); // TRUE

// Check field translatability
$field = FieldConfig::load('node.article.body');
var_dump($field->isTranslatable()); // TRUE or FALSE
```

### See Also
- → [Multilingual Overview](multilingual-overview.md) — architecture overview
- → All other sections — usage examples
- Reference: https://api.drupal.org/api/drupal/core!modules!language!language.api.php/group/language_negotiation/11.x
- Reference: https://api.drupal.org/api/drupal/core!lib!Drupal!Core!Language!language.api.php/group/i18n/11.x
