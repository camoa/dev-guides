---
description: Drupal TranslatableMarkup and t() — translation functions, placeholders, string context, plural forms, render arrays
---

# TranslatableMarkup & t()

### When to Use
When translating UI strings in PHP code — form labels, system messages, error messages, navigation text.

### Decision: Which Translation Function

| If you need... | Use... | Why |
|---|---|---|
| Translate static string in class | `$this->t('Text')` via StringTranslationTrait | Best practice, testable, DI-friendly |
| Translate in function (no class) | `new TranslatableMarkup('Text')` | Explicit object creation |
| Translate in legacy code | `t('Text')` global function | Acceptable but avoid in new code |
| Format without translation | `new FormattableMarkup()` | Placeholder replacement only, no translation |
| Plural forms | `\Drupal::translation()->formatPlural($count, '1 item', '@count items')` | Handles singular/plural correctly per language |

### Pattern: Using t() Correctly

**Basic usage**:

```php
use Drupal\Core\StringTranslation\StringTranslationTrait;

class MyClass {
  use StringTranslationTrait;

  public function myMethod() {
    $message = $this->t('Hello, world!');
    return $message;
  }
}
```

**With placeholders**:

```php
// @variable — sanitized with Html::escape()
$message = $this->t('Welcome, @name!', ['@name' => $account->getDisplayName()]);

// %variable — sanitized and wrapped in <em>
$message = $this->t('File %filename uploaded.', ['%filename' => $file->getFilename()]);

// :variable — sanitized for use in href attributes (URL-safe)
$message = $this->t('Visit <a href=":url">the site</a>.', [':url' => $url]);
```

**Placeholder types** (Drupal 8+):
- `@variable` — use for user input, entity labels, filenames (auto-escaped)
- `%variable` — use for emphasized values (auto-escaped + `<em>`)
- `:variable` — use for URLs in href attributes (auto-escaped, safe for URLs)

**Note**: The `!variable` placeholder from Drupal 7 is NOT supported in `t()` or `TranslatableMarkup`. For pre-sanitized markup, use `FormattableMarkup` instead of `t()`.

### Pattern: String Context for Disambiguation

**Problem**: English word "May" translates differently as month vs permission verb.

**Solution**: Add context parameter.

```php
// Month name
$month = $this->t('May', [], ['context' => 'Long month name']);

// Permission
$verb = $this->t('May', [], ['context' => 'Verb: permission']);
```

**In .po file**:

```po
msgctxt "Long month name"
msgid "May"
msgstr "Mayo"

msgctxt "Verb: permission"
msgid "May"
msgstr "Puede"
```

**When to use context**:
- Short strings with multiple meanings (days, months, verbs)
- Ambiguous single words
- Technical terms that vary by domain

### Pattern: Plural Forms

```php
$count = 5;
$message = \Drupal::translation()->formatPlural(
  $count,
  '1 item',              // Singular
  '@count items',        // Plural
  ['@count' => $count],  // Replacements
  ['context' => 'Shopping cart']  // Optional context
);
// Returns: "5 items"
```

**Language-specific plural rules**:
- English: 1 vs other
- French: 0-1 vs other
- Russian: complex rules with 3+ forms
- Drupal handles this automatically based on language

### Pattern: TranslatableMarkup in Render Arrays

```php
$build['#markup'] = $this->t('Translatable text');

// Or
$build['message'] = [
  '#markup' => $this->t('Welcome, @name!', ['@name' => $user->getDisplayName()]),
];
```

**Delay translation**: Don't cast to string early. Let rendering system translate.

```php
// GOOD — delays translation
$build['#title'] = $this->t('Page title');

// BAD — forces early translation, breaks caching
$build['#title'] = (string) $this->t('Page title');
```

### Common Mistakes

- **Translating user input** → `$this->t($user_input)` is XSS vulnerability. NEVER translate variables. Only translate literal strings
- **Using variables as source string** → `$this->t($string)` where `$string` is a variable. Static analysis can't extract for translation. Always use literal strings
- **Wrong placeholder type** → Using `!variable` for user input allows XSS. Use `@variable` for user data
- **Concatenating translated strings** → Don't do `$this->t('Hello') . ' ' . $this->t('world')`. Languages reorder words. Use placeholders: `$this->t('Hello @name', ['@name' => 'world'])`
- **Casting to string too early** → `(string) $this->t('Text')` breaks language-based caching. Let rendering system handle
- **Missing context for ambiguous strings** → "Order", "May", "Second" need context to translate correctly

### See Also
- → [Interface Translation](interface-translation.md) — .po file management
- → [Twig Translation](twig-translation.md) — translating in templates
- → [Anti-Patterns & Common Mistakes](anti-patterns.md) — security issues
- Reference: `core/lib/Drupal/Core/StringTranslation/TranslatableMarkup.php`
- Reference: https://www.drupal.org/docs/8/api/translation-api/overview
- Reference: https://drupalize.me/tutorial/drupal-code-standards-t-function
