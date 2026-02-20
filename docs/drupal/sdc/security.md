---
description: Security best practices for SDC components including XSS prevention and input sanitization
drupal_version: "11.x"
---

# Security

## When to Use

> Use this when handling user-generated content in components, passing data from untrusted sources, or working with attributes and HTML markup.

## Decision

| Security Mechanism | Use Case | Why |
|--------------------|----------|-----|
| Auto-escaping | All Twig output | Prevents XSS attacks by default |
| Attribute object | Dynamic attributes | Safe attribute value escaping |
| Props validation | User input in props | Prevents invalid data injection |
| Sanitization functions | User-generated content | Filter dangerous HTML tags |

## Pattern

**Auto-Escaping in Twig:**
```twig
{# Auto-escaped by default #}
<h1>{{ title }}</h1>  <!-- Safe: HTML entities encoded -->

{# Explicitly mark as safe (only for trusted markup) #}
<div>{{ content|raw }}</div>  <!-- DANGER: No escaping -->
```

**Attribute Object for Safe Handling:**
```twig
{# Safe: Attribute object handles escaping #}
<div{{ attributes.addClass('my-class') }}>

{# DANGER: Manual attribute string concatenation #}
<div class="{{ classes }}">  <!-- Vulnerable to XSS -->
```

**Props Validation:**
```yaml
props:
  type: object
  properties:
    url:
      type: string
      format: uri
      pattern: '^https?://'
    email:
      type: string
      format: email
    heading_level:
      type: integer
      enum: [1, 2, 3, 4, 5, 6]
```

**Sanitizing User Input:**
```php
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

## Common Mistakes

- **Wrong**: Using `|raw` filter on user-generated content → **Right**: Only use on trusted, pre-sanitized markup
- **Wrong**: Building attributes as strings → **Right**: Use Attribute object for safe attribute handling
- **Wrong**: Not validating props with schema in development → **Right**: Always test with validation enabled

## See Also

- [Drupal XSS Advisory](https://www.drupal.org/sa-core-2025-001)
- [Writing Secure Code for Drupal](https://www.drupal.org/docs/administering-a-drupal-site/security-in-drupal/writing-secure-code-for-drupal)
- [Component YAML Schema](component-yaml-schema.md)
- [Testing SDCs](testing-sdcs.md)
