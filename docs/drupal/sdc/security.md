---
description: "Twig auto-escaping, the Attribute object, and why prop schemas are a dev-time lint, not a security control"
tldr: "Prop validation is assert()-gated, non-mutating, and skips undeclared props entirely — pattern/format/enum on a prop never stands between user input and markup. Sanitize at the boundary (UrlHelper::stripDangerousProtocols, Xss::filter) and rely on Twig auto-escaping plus the Attribute object, not on schema validation."
drupal_version: "11.x"
---

# Security

## When to Use

> - You're handling user-generated content in components
> - You're passing data from untrusted sources
> - You're working with attributes and HTML markup

## Decision

Twig auto-escapes all output by default. Use the `Attribute` object for dynamic attributes. **Prop schemas are a development-time lint. They are not a runtime defence and must never be the thing standing between user input and your markup.**

Three reasons it does not hold:
- The validation call is `assert($this->doValidateProps($context, $component_id));` (`ComponentsTwigExtension.php:106`). On a production `zend.assertions=-1` PHP compiles the call away. Nothing runs.
- Even with assertions on, `ComponentValidator::validateProps()` takes the context by value and returns a bool (`:172`). A failing prop is *reported*, never corrected or removed — the bad value still reaches the Twig.
- The context is narrowed to declared prop names before validating (`:189-190`), so a prop nobody declared is never examined at all.

`pattern`, `format`, `enum` and `minLength` are excellent for catching *your own* integration mistakes early and for describing the API to tooling. Use them for that — not for keeping malicious input out.

## Pattern

**Pattern: Auto-Escaping in Twig**

Twig auto-escapes all output by default.

Reference: [Drupal Security Documentation](https://www.drupal.org/docs/administering-a-drupal-site/security-in-drupal/writing-secure-code-for-drupal)

```twig
{# Auto-escaped by default #}
<h1>{{ title }}</h1>  <!-- Safe: HTML entities encoded -->

{# Explicitly mark as safe (only for trusted markup) #}
<div>{{ content|raw }}</div>  <!-- DANGER: No escaping -->
```

**WHY auto-escape is critical:** Prevents XSS attacks. User input automatically sanitized unless explicitly marked safe.

**Pattern: Attribute Object for Safe Attribute Handling**

Always use `Attribute` object for dynamic attributes.

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

**WHY use Attribute:** Handles proper escaping of attribute values, prevents injection attacks.

**Anti-Pattern: Props Validation as a Security Control**

```yaml
# This does NOT keep a javascript: URI out of the href.
props:
  type: object
  properties:
    url:
      type: string
      format: uri
      pattern: '^https?://'
```

**Sanitize at the boundary instead.** Whatever produces the value — preprocess, controller, formatter — is responsible for it:

```php
use Drupal\Component\Utility\UrlHelper;

// Strip javascript:, data:, vbscript: etc. before the value becomes a prop.
// UrlHelper::stripDangerousProtocols() (core/lib/Drupal/Component/Utility/UrlHelper.php:402)
$url = UrlHelper::stripDangerousProtocols($raw);
```

and in the template, prefer Drupal's own escaping over trusting the prop:

```twig
{# Attribute handles URI escaping; it does not whitelist schemes — filter first #}
<a{{ attributes.setAttribute('href', url) }}>{{ text }}</a>
```

**Pattern: Sanitizing User Input**

For user-generated content in props (rare), sanitize before passing.

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

**Pattern: Safe Markup in Slots**

Slots should contain render arrays or safe markup objects.

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

**Common Mistake:** Using `|raw` filter on user-generated content.
**WHY:** Disables auto-escaping. Only use on trusted, pre-sanitized markup from Drupal render system.

**Common Mistake:** Building attributes as strings instead of Attribute object.
**WHY:** String concatenation doesn't escape attribute values. Use Attribute object for safe attribute handling.

**Common Mistake:** Not validating props with schema in development.
**WHY:** Invalid data passes through in production without validation. Development is the only place a schema violation can be seen, so always test with assertions enabled.

**Common Mistake:** Treating a prop schema as a security boundary.
**WHY:** It is `assert()`-gated, non-mutating, and skips undeclared props entirely. Filter and escape at the source; let the schema catch integration mistakes, not attackers.

## See Also

- [Drupal XSS Advisory](https://www.drupal.org/sa-core-2025-001)
- [Writing Secure Code for Drupal](https://www.drupal.org/docs/administering-a-drupal-site/security-in-drupal/writing-secure-code-for-drupal)
- [Component YAML Schema](component-yaml-schema.md)
- [Testing SDCs](testing-sdcs.md)
