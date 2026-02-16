---
description: Drupal multilingual anti-patterns — translating user input, concatenating strings, hardcoding language codes, missing cache contexts
---

# Anti-Patterns & Common Mistakes

### When to Use
When reviewing code or debugging multilingual issues — learn what NOT to do and why.

### Anti-Pattern: Translating User Input

**What NOT to do**:

```php
// NEVER DO THIS — XSS vulnerability
$user_input = $_POST['message'];
$message = $this->t($user_input);

// NEVER DO THIS — user content, not UI
$node_title = $node->getTitle();
$translated = $this->t($node_title);
```

**Why it's wrong**:
- `t()` is for interface text, not user content
- User input through `t()` is XSS attack vector
- Translation database gets polluted with user content
- User content should use entity translation, not interface translation

**What to do instead**:

```php
// For user input — sanitize, don't translate
$user_input = $_POST['message'];
$safe_output = Html::escape($user_input);

// For entity content — use entity translation
$node = Node::load(1);
$spanish = $node->getTranslation('es');
$title = $spanish->getTitle(); // Already translated via entity API
```

### Anti-Pattern: Concatenating Translated Strings

**What NOT to do**:

```php
// WRONG — languages have different word orders
$message = $this->t('Hello') . ' ' . $user->getDisplayName() . ', ' . $this->t('welcome to our site!');

// WRONG — can't reorder for different languages
$label = $this->t('Posted by') . ' ' . $author . ' ' . $this->t('on') . ' ' . $date;
```

**Why it's wrong**:
- Word order varies by language
- Some languages put verb at end
- Translators can't reorder concatenated parts
- Results in broken grammar in other languages

**What to do instead**:

```php
// RIGHT — single translatable string with placeholders
$message = $this->t('Hello @name, welcome to our site!', [
  '@name' => $user->getDisplayName(),
]);

$label = $this->t('Posted by @author on @date', [
  '@author' => $author,
  '@date' => $date,
]);
```

### Anti-Pattern: Hardcoding Language Codes

**What NOT to do**:

```php
// WRONG — assumes Spanish always exists and uses 'es'
if ($node->hasTranslation('es')) {
  $spanish = $node->getTranslation('es');
}

// WRONG — hardcodes default language
$config->set('default_langcode', 'en');

// WRONG — business logic depends on language code
if ($current_language == 'en') {
  // Special English-only logic
}
```

**Why it's wrong**:
- Site might use different language codes (es-MX vs es, en-GB vs en)
- Breaks if languages added/removed
- Not portable across sites
- Violates separation of concerns

**What to do instead**:

```php
// RIGHT — use configuration
$default_language = \Drupal::languageManager()->getDefaultLanguage()->getId();
$available_languages = \Drupal::languageManager()->getLanguages();

// RIGHT — iterate all languages instead of hardcoding
foreach ($node->getTranslationLanguages() as $langcode => $language) {
  $translation = $node->getTranslation($langcode);
  // Process
}

// RIGHT — business logic independent of language
// Use content/config to control behavior, not language code
```

### Anti-Pattern: Embedding Unsanitized Content in Translated Strings

**What NOT to do**:

```php
// WRONG — user input directly in markup
$user_input = $_POST['name'];
$message = new FormattableMarkup('Hello @name', ['@name' => $user_input]);
// This is fine for FormattableMarkup, but don't confuse with t()

// WRONG — concatenating markup into t()
$message = $this->t('Hello ' . $user_input);
// XSS vulnerability — user input not sanitized
```

**Why it's wrong**:
- Direct string concatenation in `t()` bypasses sanitization
- User input must always go through placeholders
- In Drupal 8+, only `@`, `%`, `:` placeholders are supported in `t()`

**What to do instead**:

```php
// RIGHT — @placeholder auto-sanitizes in t()
$user_input = $_POST['name'];
$message = $this->t('Hello @name', ['@name' => $user_input]);

// RIGHT — for pre-sanitized markup, use FormattableMarkup (NOT t())
use Drupal\Component\Render\FormattableMarkup;
$markup = new FormattableMarkup('<strong>@label</strong>', ['@label' => $label]);
```

### Anti-Pattern: Translating Non-Translatable Fields

**What NOT to do**:

```php
// Create entity with non-translatable field
$node = Node::create(['type' => 'article']);
$node->set('field_date', '2026-02-16'); // Non-translatable
$node->save();

// Add translation and try to change non-translatable field
$spanish = $node->addTranslation('es');
$spanish->set('field_date', '2026-02-17'); // Changes ALL translations
$node->save();

// English node now has 2026-02-17 too — unexpected!
```

**Why it's wrong**:
- Non-translatable fields share value across translations
- Changing in one translation affects all
- Users expect field to be independent but it's not

**What to do instead**:

```php
// Only set translatable fields per translation
$spanish = $node->addTranslation('es');
$spanish->set('title', 'Título en español'); // Translatable
$spanish->set('body', 'Cuerpo en español');  // Translatable
// Don't set field_date — it's shared
$node->save();

// Or make field translatable if it needs different values
$field = FieldConfig::load('node.article.field_date');
$field->setTranslatable(TRUE)->save();
```

### Anti-Pattern: Missing Cache Contexts

**What NOT to do**:

```php
// WRONG — language-dependent render array without language cache context
function mymodule_block_view() {
  return [
    '#markup' => t('Welcome!'),
    '#cache' => [
      'max-age' => 3600,
      // Missing: 'contexts' => ['languages:language_interface']
    ],
  ];
}
// Cached in English, shown to Spanish users
```

**Why it's wrong**:
- Cache doesn't vary by language
- First visitor's language cached for everyone
- Other language users see wrong language

**What to do instead**:

```php
// RIGHT — include language cache context
function mymodule_block_view() {
  return [
    '#markup' => t('Welcome!'),
    '#cache' => [
      'max-age' => 3600,
      'contexts' => ['languages:language_interface'],
    ],
  ];
}
```

### Anti-Pattern: Ignoring Translation Metadata

**What NOT to do**:

```php
// Create translation without metadata
$node = Node::load(1);
$spanish = $node->addTranslation('es', ['title' => 'Título']);
$node->save();
// Missing: source language, translation author, timestamp
```

**Why it's wrong**:
- Translation overview UI shows incomplete info
- Can't track who translated what
- Can't mark translations outdated
- Breaks TMGMT integration

**What to do instead**:

```php
// Set translation metadata
$node = Node::load(1);
$spanish = $node->addTranslation('es', ['title' => 'Título']);
$spanish->content_translation_source = 'en';
$spanish->content_translation_outdated = FALSE;
$spanish->content_translation_uid = \Drupal::currentUser()->id();
$spanish->content_translation_created = time();
$node->save();
```

### See Also
- → [TranslatableMarkup & t()](translatable-markup.md) — correct usage
- → [Best Practices & Patterns](best-practices.md) — what to do
- → [Security, Performance & Caching](security-performance-caching.md) — security details
- Reference: https://www.drupal.org/docs/8/api/translation-api/overview
