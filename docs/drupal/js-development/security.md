---
description: JavaScript security best practices for XSS prevention and CSP compliance
drupal_version: "10.x/11.x"
---

# Security

## When to Use

> Use any time JavaScript handles user input, manipulates DOM, or processes data from external sources.

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

## Common Mistakes

- **Wrong**: innerHTML with user input → **Right**: Use textContent or Drupal.checkPlain()
  - **Why**: Direct XSS vulnerability, allows script injection
- **Wrong**: Passing API keys in drupalSettings → **Right**: Never pass secrets
  - **Why**: Visible in page source to all users
- **Wrong**: Using eval() or new Function() → **Right**: Use JSON.parse or safe alternatives
  - **Why**: Security risk, breaks CSP, code injection vector
- **Wrong**: Not sanitizing URL parameters → **Right**: Sanitize before DOM insertion
  - **Why**: Reflected XSS vulnerability
- **Wrong**: Inline event handlers in templates → **Right**: Use addEventListener in behaviors
  - **Why**: Breaks CSP, mixes concerns

## See Also

- [DOM Manipulation](dom-manipulation.md) - Safe DOM patterns
- [drupalSettings](drupal-settings.md) - What not to pass
- Reference: [Writing Secure Code for Drupal](https://www.drupal.org/docs/administering-a-drupal-site/security-in-drupal/writing-secure-code-for-drupal)
- Reference: [DOM XSS Prevention](https://cheatsheetseries.owasp.org/cheatsheets/DOM_based_XSS_Prevention_Cheat_Sheet.html)
