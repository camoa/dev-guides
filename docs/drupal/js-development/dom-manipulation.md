---
description: "Safe DOM manipulation patterns with vanilla JavaScript preferred over jQuery"
tldr: "Prefer vanilla JavaScript (querySelector, addEventListener, classList) over jQuery for DOM manipulation; jQuery stays acceptable for existing jQuery-heavy code or complex traversal. Gotcha: never use innerHTML with unsanitized user input."
drupal_version: "11.x"
---

# DOM Manipulation

## When to Use

> Modifying page structure, content, or attributes in response to user interaction or dynamic updates.

## Decision

**Modern Drupal**: Prefer vanilla JavaScript over jQuery. Drupal is phasing out jQuery dependency - use native DOM APIs (querySelector, addEventListener, classList) for better performance and future compatibility.

**When jQuery is acceptable**: Working with existing jQuery-heavy code, complex DOM traversal, or jQuery-specific plugins. Always declare `core/jquery` dependency.

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

**Reference**: Drupal coding standards prefer vanilla JS - https://project.pages.drupalcode.org/coding_standards/javascript/best-practice/

## Common Mistakes

- **Using innerHTML with unsanitized data** - WHY: XSS vulnerability, allows script injection
- **jQuery for simple operations** - WHY: Unnecessary 30KB dependency for operations vanilla JS handles
- **Not using context in selectors** - WHY: Queries entire document, performance penalty
- **document.createElement() without need** - WHY: More verbose than native methods, no benefit
- **Modifying DOM outside behaviors** - WHY: Breaks AJAX compatibility, timing issues

## See Also

- [Security](security.md) - XSS prevention in DOM manipulation
- [Event Handling](event-handling.md) - addEventListener patterns
- Reference: [DOM XSS Prevention](https://cheatsheetseries.owasp.org/cheatsheets/DOM_based_XSS_Prevention_Cheat_Sheet.html)
