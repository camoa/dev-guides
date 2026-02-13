---
description: Preventing XSS with auto-escaping, Attribute object, and props validation
drupal_version: "11.x"
---

# Security

## When to Use

> Use this when handling user-generated content in components, passing data from untrusted sources, or working with attributes and HTML markup.

## Decision: Security Best Practices

| Pattern | Purpose | Why |
|---------|---------|-----|
| Twig auto-escaping | Prevent XSS attacks | All output auto-escaped by default |
| Attribute object | Safe attribute handling | Handles proper escaping of attribute values |
| Props validation | Prevent invalid data | JSON Schema validates format, pattern, enum |
| Sanitize before props | Clean user input | Use `Html::escape()` or `Xss::filter()` |
| Render arrays in slots | Safe markup objects | Already sanitized by Drupal render system |

## Pattern

Auto-escaping in Twig (default behavior):

```twig
{# Auto-escaped by default #}
<h1>{{ title }}</h1>  <!-- Safe: HTML entities encoded -->

{# Explicitly mark as safe (only for trusted markup) #}
<div>{{ content|raw }}</div>  <!-- DANGER: No escaping -->
```

**WHY auto-escape is critical**: Prevents XSS attacks. User input automatically sanitized unless explicitly marked safe.

Attribute object for safe attribute handling:

```yaml
# In component schema
props:
  type: object
  properties:
    attributes:
      type: Drupal\Core\Template\Attribute
```

```twig
{# Safe: Attribute object handles escaping #}
<div{{ attributes.addClass('my-class') }}>

{# DANGER: Manual attribute string concatenation #}
<div class="{{ classes }}">  <!-- Vulnerable to XSS -->
```

**WHY use Attribute**: Handles proper escaping of attribute values, prevents injection attacks.

Props validation with JSON Schema:

```yaml
props:
  type: object
  properties:
    url:
      type: string
      format: uri  # Validates URL format
      pattern: '^https?://'  # Restrict to http/https

    email:
      type: string
      format: email  # Validates email format

    heading_level:
      type: integer
      enum: [1, 2, 3, 4, 5, 6]  # Restrict to valid values
```

Sanitizing user input before props:

```php
// In preprocessing or controller
use Drupal\Component\Utility\Html;
use Drupal\Component\Utility\Xss;

$build = [
  '#type' => 'component',
  '#component' => 'my_theme:card',
  '#props' => [
    // Plain text: HTML escape
    'title' => Html::escape($user_input),

    // Allow limited HTML: filter tags
    'description' => Xss::filter($user_input, ['p', 'br', 'strong', 'em']),
  ],
];
```

Safe markup in slots (render arrays):

```php
// Proper slot content handling
'#slots' => [
  'content' => [
    '#markup' => $filtered_html,  // Already sanitized
    '#allowed_tags' => ['p', 'br', 'strong'],
  ],
],
```

## Common Mistakes

- **Wrong**: Using `|raw` filter on user-generated content → **Right**: Disables auto-escaping. Only use on trusted, pre-sanitized markup from Drupal render system.
- **Wrong**: Building attributes as strings instead of Attribute object → **Right**: String concatenation doesn't escape attribute values. Use Attribute object for safe attribute handling.
- **Wrong**: Not validating props with schema in development → **Right**: Invalid data passes through in production without validation. Always test with validation enabled to catch issues early.

## See Also

- [Component YAML Schema](component-yaml-schema.md)
- [Testing SDCs](testing-sdcs.md)
- [Drupal XSS Advisory](https://www.drupal.org/sa-core-2025-001)
- [Writing Secure Code for Drupal](https://www.drupal.org/docs/administering-a-drupal-site/security-in-drupal/writing-secure-code-for-drupal)
