---
description: "JavaScript security best practices for XSS prevention and CSP compliance"
tldr: "Sanitize all user input before inserting into the DOM, use Drupal.checkPlain() for escaping, and never pass sensitive data through drupalSettings. Gotcha: never use innerHTML with unsanitized data, and avoid eval() or new Function() — both break CSP."
drupal_version: "11.x"
---

# Security

## When to Use

> Any JavaScript that handles user input, manipulates DOM, or processes data from external sources.

## Decision

Prevent XSS by sanitizing all user input before inserting into DOM. Use Drupal.checkPlain() for escaping. Never use innerHTML with unsanitized data. Follow CSP compatibility patterns. Never pass sensitive data through drupalSettings.

## Pattern

**Safe text insertion**:
```javascript
// SAFE: textContent escapes HTML automatically
element.textContent = userInput;

// SAFE: Drupal.checkPlain() escapes HTML entities
element.innerHTML = Drupal.checkPlain(userInput);

// DANGEROUS: Raw user input in innerHTML
// element.innerHTML = userInput; // XSS VULNERABILITY!
```

**Safe attribute setting**:
```javascript
// SAFE: setAttribute escapes automatically
element.setAttribute('title', userInput);
element.setAttribute('data-value', userInput);

// DANGEROUS: Direct attribute manipulation
// element.outerHTML = '<div title="' + userInput + '">'; // XSS!
```

**drupalSettings security**:
```php
// NEVER pass sensitive data
$build['#attached']['drupalSettings'] = [
  'module' => [
    'apiUrl' => '/api/public',        // OK: Public endpoint
    // 'apiKey' => $secret_key,       // NEVER: Visible in page source!
    // 'userEmail' => $email,         // NEVER: Private user data!
  ],
];
```

**CSP-compatible patterns**:
```javascript
// AVOID inline event handlers
// <button onclick="handler()">  // Breaks CSP

// USE addEventListener
button.addEventListener('click', handler);

// AVOID eval() and Function()
// eval(userInput); // Security violation + CSP violation

// USE JSON.parse for data
const data = JSON.parse(jsonString);
```

**Reference**:
- https://www.drupal.org/docs/administering-a-drupal-site/security-in-drupal/writing-secure-code-for-drupal
- https://www.drupal.org/node/2513818 - CSP-compatible drupalSettings

## Common Mistakes

- **innerHTML with user input** - WHY: Direct XSS vulnerability, allows script injection
- **Passing API keys in drupalSettings** - WHY: Visible in page source to all users
- **Using eval() or new Function()** - WHY: Security risk, breaks CSP, code injection vector
- **Not sanitizing URL parameters** - WHY: Reflected XSS vulnerability
- **Inline event handlers in templates** - WHY: Breaks CSP, mixes concerns

## See Also

- [DOM Manipulation](dom-manipulation.md) - Safe DOM patterns
- [drupalSettings](drupal-settings.md) - What not to pass
- Reference: [DOM XSS Prevention](https://cheatsheetseries.owasp.org/cheatsheets/DOM_based_XSS_Prevention_Cheat_Sheet.html)
