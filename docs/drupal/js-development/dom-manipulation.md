---
description: Safe DOM manipulation patterns with vanilla JavaScript preferred over jQuery
drupal_version: "10.x/11.x"
---

# DOM Manipulation

## When to Use

> Use when modifying page structure, content, or attributes in response to user interaction or dynamic updates.

## Decision

| Situation | Choose | Why |
|-----------|--------|-----|
| Simple DOM queries and updates | Vanilla JavaScript | Better performance, no jQuery dependency |
| Complex DOM traversal | jQuery (with core/jquery dependency) | Still acceptable for complex cases |
| User input insertion | textContent or Drupal.checkPlain() | XSS-safe, prevents script injection |
| Existing jQuery-heavy code | jQuery (with dependency declared) | Maintain consistency in legacy code |

**Modern Drupal**: Prefer vanilla JavaScript over jQuery. Drupal is phasing out jQuery dependency - use native DOM APIs (querySelector, addEventListener, classList) for better performance and future compatibility.

## Pattern

**Vanilla JavaScript** (preferred):

```javascript
Drupal.behaviors.vanillaDOM = {
  attach(context) {
    once('vanilla', '.element', context).forEach(function (element) {
      // Query elements
      const child = element.querySelector('.child');
      const all = element.querySelectorAll('.items');

      // Modify classes
      element.classList.add('active');
      element.classList.remove('hidden');
      element.classList.toggle('expanded');

      // Modify attributes
      element.setAttribute('aria-expanded', 'true');
      element.removeAttribute('hidden');

      // Safe text insertion (XSS-safe)
      element.textContent = 'Safe text content';

      // Events
      element.addEventListener('click', handler);
    });
  }
};
```

**jQuery pattern** (when necessary):

```javascript
(function ($, Drupal, once) {
  Drupal.behaviors.jqueryDOM = {
    attach(context) {
      once('jquery', '.element', context).forEach(function (element) {
        const $element = $(element);
        $element.addClass('active');
        $element.on('click', handler);
      });
    }
  };
})(jQuery, Drupal, once);
```

**Safe HTML insertion** (avoid XSS):

```javascript
// NEVER use innerHTML with user input
// element.innerHTML = userInput; // XSS vulnerability!

// Safe alternatives:
element.textContent = userInput;  // Text only, escapes HTML
element.innerText = userInput;    // Similar to textContent

// If HTML needed, sanitize first:
const sanitized = Drupal.checkPlain(userInput);
element.innerHTML = sanitized;
```

## Common Mistakes

- **Wrong**: Using innerHTML with unsanitized data → **Right**: Use textContent or Drupal.checkPlain()
  - **Why**: XSS vulnerability, allows script injection
- **Wrong**: jQuery for simple operations → **Right**: Use vanilla JS
  - **Why**: Unnecessary 30KB dependency for operations vanilla JS handles
- **Wrong**: Not using context in selectors → **Right**: Query within context
  - **Why**: Queries entire document, performance penalty
- **Wrong**: Modifying DOM outside behaviors → **Right**: Always use behaviors
  - **Why**: Breaks AJAX compatibility, timing issues

## See Also

- [Security](security.md) - XSS prevention in DOM manipulation
- [Event Handling](event-handling.md) - addEventListener patterns
- Reference: [Drupal JavaScript Coding Standards](https://project.pages.drupalcode.org/coding_standards/javascript/best-practice/)
- Reference: [DOM XSS Prevention](https://cheatsheetseries.owasp.org/cheatsheets/DOM_based_XSS_Prevention_Cheat_Sheet.html)
