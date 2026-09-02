---
description: "Common JavaScript mistakes in Drupal and how to avoid them"
tldr: "Review these eight anti-patterns when checking JavaScript code — each includes the WRONG and CORRECT form plus why it matters. Gotcha: an anti-pattern often works initially but fails with AJAX, caching, or scale."
drupal_version: "11.x"
---

# Common Anti-Patterns

## When to Use

> Reviewing code for mistakes and understanding what NOT to do.

## Decision

Avoid these patterns that create bugs, performance issues, or maintainability problems. Each anti-pattern has a WHY explanation - understanding the consequences helps prevent them.

## Pattern

**Anti-Pattern 1: No context parameter**
```javascript
// WRONG
Drupal.behaviors.bad = {
  attach() {  // Missing context!
    $('.element').each(function() {
      // Scans entire document every time
    });
  }
};

// CORRECT
Drupal.behaviors.good = {
  attach(context) {
    once('good', '.element', context).forEach(function(element) {
      // Scans only new/updated content
    });
  }
};
```
**WHY**: Without context, code scans entire DOM on every AJAX request. Severe performance penalty, especially on large pages.

**Anti-Pattern 2: Missing once()**
```javascript
// WRONG
$('.button', context).on('click', handler);
// Binds handler multiple times on AJAX updates
// Memory leak + handler fires multiple times per click

// CORRECT
once('click-handler', '.button', context).forEach(function(button) {
  button.addEventListener('click', handler);
  // Binds exactly once per element
});
```
**WHY**: Without once(), event handlers bind multiple times on AJAX updates, causing memory leaks and duplicate execution.

**Anti-Pattern 3: jQuery for simple operations**
```javascript
// WRONG - Adds 30KB jQuery dependency
$(element).addClass('active');
$(element).on('click', handler);

// CORRECT - Native JavaScript
element.classList.add('active');
element.addEventListener('click', handler);
```
**WHY**: jQuery adds significant weight for operations vanilla JS handles. Drupal is phasing out jQuery.

**Anti-Pattern 4: Missing detach()**
```javascript
// WRONG - No cleanup
Drupal.behaviors.leaky = {
  attach(context) {
    setInterval(updateStatus, 1000); // Interval never cleared
    window.addEventListener('resize', handler); // Never removed
  }
  // No detach() method
};

// CORRECT - Cleanup in detach
Drupal.behaviors.clean = {
  attach(context) {
    once('clean', 'html').forEach(function() {
      this.intervalId = setInterval(updateStatus, 1000);
    });
  },
  detach(context, settings, trigger) {
    if (trigger === 'unload') {
      clearInterval(this.intervalId);
    }
  }
};
```
**WHY**: Intervals and global event listeners persist after content removal, causing memory leaks.

**Anti-Pattern 5: Inline JavaScript**
```twig
{# WRONG #}
<button onclick="doSomething()">Click</button>
<script>
  function doSomething() { }
</script>

{# CORRECT #}
<button class="action-button">Click</button>
{# JavaScript in behavior with library attachment #}
```
**WHY**: Inline JS bypasses asset system, breaks CSP, prevents aggregation, violates separation of concerns.

**Anti-Pattern 6: Global scope pollution**
```javascript
// WRONG - Pollutes global scope
function myFunction() { }
var myVariable = 'value';

// CORRECT - Wrapped in IIFE
(function (Drupal) {
  'use strict';

  function myFunction() { }
  const myVariable = 'value';

  // Only expose what's necessary
  Drupal.behaviors.myBehavior = { };
})(Drupal);
```
**WHY**: Global variables conflict with other scripts, create unpredictable bugs.

**Anti-Pattern 7: $(document).ready()**
```javascript
// WRONG - Only runs once, breaks with AJAX
$(document).ready(function() {
  $('.element').initializeWidget();
});

// CORRECT - Runs on page load AND AJAX updates
Drupal.behaviors.widget = {
  attach(context) {
    once('widget', '.element', context).forEach(function(element) {
      initializeWidget(element);
    });
  }
};
```
**WHY**: $(document).ready() only executes on initial page load. AJAX-loaded content never initializes.

**Anti-Pattern 8: innerHTML with user data**
```javascript
// WRONG - XSS vulnerability
element.innerHTML = '<div>' + userInput + '</div>';

// CORRECT - Safe alternatives
element.textContent = userInput;  // Text only
element.innerHTML = Drupal.checkPlain(userInput); // Escaped HTML
```
**WHY**: Direct innerHTML with user input allows script injection and XSS attacks.

## Common Mistakes

- **Not understanding WHY anti-patterns are bad** - WHY: Repeat mistakes in different forms
- **Copy-pasting old Drupal 7 patterns** - WHY: Many D7 patterns are anti-patterns in modern Drupal
- **Thinking "it works" means "it's correct"** - WHY: Anti-patterns often work initially but fail with AJAX, caching, or scale

## See Also

- [Drupal.behaviors Pattern](drupal-behaviors-pattern.md) - Correct patterns
- [Once API](once-api.md) - Preventing duplicates
- [Security](security.md) - XSS prevention
