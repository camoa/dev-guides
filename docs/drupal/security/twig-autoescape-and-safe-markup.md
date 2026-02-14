---
description: Understanding Twig automatic XSS protection, Markup objects, translation placeholders, and avoiding double-escaping issues.
---

# Twig Autoescape and Safe Markup

## When to Use
Understanding Twig's automatic XSS protection when building themes or rendering output.

## Steps
1. **Default behavior: everything autoescapes**
   ```twig
   {# Automatically escaped #}
   {{ node.title.value }}
   {{ user_input }}
   {{ form.field_name }}
   ```

2. **Marking trusted content as safe**
   ```php
   // In preprocess/controller
   use Drupal\Core\Render\Markup;

   // Create safe markup object
   $variables['safe_html'] = Markup::create('<strong>Trusted</strong>');

   // Or use render array (system handles it)
   $variables['content'] = [
     '#type' => 'processed_text',
     '#text' => $text,
     '#format' => 'full_html',  // Runs text through filters
   ];
   ```

3. **In Twig: avoid |raw filter**
   ```twig
   {# WRONG: Disables XSS protection #}
   {{ user_bio|raw }}

   {# CORRECT: Use Markup object from preprocess #}
   {{ safe_markup_variable }}

   {# CORRECT: Let render system handle it #}
   {{ content.body }}
   ```

4. **Handling double-escaping issues**
   ```php
   // Problem: t() returns TranslatableMarkup (MarkupInterface)
   // Twig won't escape it, but if you escape before t()...

   // WRONG: Double-escaped
   $text = Html::escape($user_input);
   $variables['message'] = $this->t('Hello @name', ['@name' => $text]);

   // CORRECT: t() handles escaping
   $variables['message'] = $this->t('Hello @name', ['@name' => $user_input]);
   // @name is automatically escaped by t()
   ```

5. **Working with text formats**
   ```php
   // Filtered text (user-formatted content)
   $build = [
     '#type' => 'processed_text',
     '#text' => $node->body->value,
     '#format' => $node->body->format,  // 'basic_html', 'full_html', etc.
   ];
   // Text format filters apply (XSS protection included)
   ```

## Decision Points
| At this step... | If... | Then... |
|---|---|---|
| Template output | Variable is user input | Use `{{ var }}` (autoescaped) |
| Template output | Variable is trusted HTML | Pass as `Markup` object from preprocess |
| Preprocess | Building HTML string | Use render arrays instead |
| Preprocess | Must create HTML string | Use `Markup::create()` and ensure content is safe |
| Translation | Placeholder is user input | Use `@placeholder` (escaped) not `!placeholder` (unescaped) |

## Translation Placeholder Types
```php
// @placeholder - Escaped (safe for user input)
$this->t('Hello @name', ['@name' => $user_input]);

// %placeholder - Escaped + <em> wrapper
$this->t('Welcome %user', ['%user' => $username]);

// :placeholder - URL-escaped for href attributes
$this->t('<a href=":url">Link</a>', [':url' => $url]);

// !placeholder - NOT escaped (dangerous, only for trusted markup)
$this->t('Message: !html', ['!html' => Markup::create($safe_html)]);
```

## Common Mistakes
- Using `|raw` filter -- Only if absolutely necessary and content is verified safe
- Not understanding MarkupInterface -- Objects implementing it skip autoescape
- Creating Markup from user input -- `Markup::create($user_input)` is an XSS hole
- Escaping before translation -- `t()` handles it; double-escaping breaks output
- Using `!placeholder` with user input -- Never use unescaped placeholders with untrusted data

## See Also
- [XSS Prevention](xss-prevention.md) for broader context
- Reference: https://www.drupal.org/node/2297711 (Twig autoescape issues)
- Reference: `/core/lib/Drupal/Component/Render/MarkupInterface.php`
