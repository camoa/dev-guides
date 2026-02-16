---
description: Drupal Twig translation — t filter, trans block, plural forms, field output, preprocess translation patterns
---

# Twig Translation

### When to Use
When translating text in Twig templates — theme templates, custom template files, template suggestions.

### Decision: Twig Translation Method

| If you need... | Use... | Why |
|---|---|---|
| Translate simple string | `{{ 'Text'\|t }}` | One-line, no variables |
| Translate with placeholders | `{% trans %}` block | Supports `{{ variable }}` placeholders |
| Translate plural forms | `{% trans %}{% plural count %}{% endtrans %}` | Handles singular/plural per language |
| Add translation context | `{% trans with {'context': 'My context'} %}` | Disambiguate ambiguous strings |
| Translate in specific language | `{% trans with {'langcode': 'es'} %}` | Force specific language |

### Pattern: Simple Translation Filter

```twig
{# Simple string #}
<h1>{{ 'Welcome'\|t }}</h1>

{# With context #}
<span>{{ 'May'\|t({}, {'context': 'Long month name'}) }}</span>

{# Common mistake — don't translate variables #}
{# BAD — security risk #}
<p>{{ user_input\|t }}</p>

{# GOOD — just output the variable #}
<p>{{ user_input }}</p>
```

**Explanation**:
- `'Text'\|t` — translates literal string
- First argument: replacements (empty `{}` if none)
- Second argument: options (context, langcode)
- NEVER use `\|t` on variables — only literal strings

### Pattern: Trans Block with Variables

```twig
{% trans %}
  Welcome, {{ name }}!
{% endtrans %}
```

**With placeholders and context**:

```twig
{% trans with {'%filename': file.filename, '@size': file.size} %}
  File %filename uploaded (@size bytes).
{% endtrans %}
```

**With context**:

```twig
{% trans with {'context': 'User greeting'} %}
  Hello, {{ user.name }}!
{% endtrans %}
```

### Pattern: Plural Forms

```twig
{% trans %}
  1 item
{% plural count %}
  {{ count }} items
{% endtrans %}
```

**With context**:

```twig
{% trans with {'context': 'Shopping cart'} %}
  1 item in cart
{% plural item_count %}
  {{ item_count }} items in cart
{% endtrans %}
```

**Explanation**:
- Text before `{% plural %}` — singular form
- Text after `{% plural count %}` — plural form
- `count` variable determines which form to use
- Language-specific plural rules applied automatically

### Pattern: Field Output (Already Translated)

**Entity fields are automatically translated** — don't wrap in `t`:

```twig
{# GOOD — field already translated based on current language #}
<h1>{{ content.title }}</h1>
<div>{{ content.body }}</div>

{# BAD — double translation attempt #}
<h1>{{ content.title\|t }}</h1>
```

**When field renders**:
- Drupal loads entity translation based on language negotiation
- Field formatter outputs translated value
- No `\|t` needed on field output

### Pattern: Translating Render Arrays in Preprocess

```php
// In mytheme.theme or module.module
function mytheme_preprocess_page(&$variables) {
  $variables['custom_message'] = [
    '#markup' => t('Welcome to our site!'),
  ];
}
```

```twig
{# In page.html.twig #}
{{ custom_message }}
```

**Explanation**:
- Use `t()` in PHP preprocess
- Output render array in Twig without `\|t`
- Translation happens in PHP, Twig just renders

### Common Mistakes

- **Translating user content** → `{{ node.title\|t }}` is wrong. Node title is user content, not UI text. Already translated via entity translation
- **Using t filter on render arrays** → `{{ content.field_name\|t }}` is wrong. Field is already translated
- **Concatenating translated strings** → Don't split sentences across multiple `{% trans %}` blocks. Languages reorder words differently. Use single block with placeholders
- **Missing quotes on literal strings** → `{{ Welcome\|t }}` is wrong (undefined constant). Use `{{ 'Welcome'\|t }}` with quotes
- **Translating in wrong language layer** → Don't use `\|t` for content that should be entity-translated. Interface translation is for UI, not content
- **Not using placeholders correctly** → `{% trans %}Welcome {{ name }}{% endtrans %}` works, but `{% trans with {'@name': name} %}Welcome @name{% endtrans %}` is clearer for translators

### See Also
- → [TranslatableMarkup & t()](translatable-markup.md) — PHP translation
- → [Translating Content Entities](translating-content-entities.md) — entity translation vs interface translation
- → [Anti-Patterns & Common Mistakes](anti-patterns.md) — security issues
- Reference: `core/lib/Drupal/Core/Template/TwigNodeTrans.php`
- Reference: https://www.drupal.org/docs/develop/theming-drupal/twig-in-drupal/filters-modifying-variables-in-twig-templates
- Reference: https://www.drupal.org/node/2047135 (trans tag support)
