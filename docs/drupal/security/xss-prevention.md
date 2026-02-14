---
description: Preventing Cross-Site Scripting attacks using Twig autoescape, Xss::filter(), Html::escape(), and safe markup patterns.
---

# XSS Prevention

## When to Use
Whenever displaying user-generated content or building HTML output -- XSS (Cross-Site Scripting) is one of the most common web vulnerabilities.

## Decision
| If you need... | Use... | Why |
|---|---|---|
| Display user text in Twig | `{{ variable }}` | Autoescapes by default |
| Display HTML from trusted source | `{{ trusted_markup }}` with `Markup` object | Twig won't double-escape |
| Filter untrusted HTML | `Xss::filter($string, $allowed_tags)` | Strips dangerous tags/attributes |
| Admin-only HTML | `Xss::filterAdmin($string)` | Permits more tags, still removes scripts |
| Plain text output | `Html::escape($string)` | Converts `<` to `&lt;`, etc. |
| URL sanitization | `UrlHelper::filterBadProtocol($url)` | Removes `javascript:`, `data:` schemes |

**XSS Attack Vectors:**
- `<script>alert('XSS')</script>` -- Direct script injection
- `<img src=x onerror=alert(1)>` -- Event handler injection
- `<a href="javascript:alert(1)">` -- Protocol injection
- `"><script>alert(1)</script>` -- Attribute breakout

## Pattern
Safe output patterns:
```php
// In Twig templates (autoescaped)
{{ user.getDisplayName() }}  {# Safe: autoescaped #}
{{ node.body.value }}        {# Safe: autoescaped #}

// Render array (safe by default)
$build['#markup'] = $user_input;  // WRONG: not sanitized
$build['#markup'] = Xss::filter($user_input);  // Safe
$build['#plain_text'] = $user_input;  // Safe: auto-escaped

// Creating Markup objects (trusted content)
use Drupal\Component\Render\MarkupInterface;
use Drupal\Core\Render\Markup;

$safe_markup = Markup::create('<strong>Trusted HTML</strong>');
// Twig won't escape this because it implements MarkupInterface
```
Reference: `/core/lib/Drupal/Component/Utility/Xss.php`

## Common Mistakes
- Using `{{ var|raw }}` in Twig -- Disables autoescape, opens XSS hole
- Concatenating HTML strings instead of render arrays -- Bypasses rendering system
- Using `#markup` with unsanitized input -- Must use `Xss::filter()` first
- Trusting data from database -- User-generated content can contain XSS, even stored
- Filtering output instead of input -- Filter on output, validate on input (different stages)
- Using `strip_tags()` instead of `Xss::filter()` -- `strip_tags()` misses attribute-based XSS

## See Also
- [Twig Autoescape and Safe Markup](twig-autoescape-and-safe-markup.md) for Twig-specific details
- Reference: https://www.drupal.org/docs/administering-a-drupal-site/security-in-drupal/writing-secure-code-for-drupal
- Reference: https://www.drupal.org/node/2296163 (Twig autoescape change record)
