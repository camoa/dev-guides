---
description: JavaScript development standards checklist for Drupal projects
drupal_version: "10.x/11.x"
---

# Best Practices Summary

## When to Use

> Use as a code review checklist and development standards reference.

## Decision

Senior developers ask these questions when reviewing Drupal JavaScript:

**Architecture**:

- "Why is this not in a behavior?" - Most JS should use Drupal.behaviors
- "Where's your context parameter?" - Missing context = performance penalty
- "Where's your once() wrapper?" - Missing once() = memory leaks
- "Where's your detach()?" - Missing cleanup = memory leaks

**Performance**:

- "Why is this library loaded globally?" - Conditional loading saves bandwidth
- "Why not use defer?" - Non-blocking load improves page speed
- "Is this debounced?" - High-frequency events need debounce/throttle
- "Are you forcing reflows?" - Batch DOM reads/writes

**Security**:

- "Where's the sanitization?" - User input in DOM needs escaping
- "Why is this in drupalSettings?" - Sensitive data doesn't belong in settings
- "Is this CSP-compatible?" - No inline handlers, no eval()

**Modern Patterns**:

- "Why jQuery for this?" - Vanilla JS preferred for simple operations
- "Why not vanilla addEventListener?" - Modern event handling pattern
- "Is this tested with AJAX?" - Most Drupal JS bugs are AJAX-related

## Pattern

**Every JavaScript file must**:

- [ ] Use IIFE wrapper: `(function (Drupal, once) { })(Drupal, once);`
- [ ] Declare 'use strict';
- [ ] Use Drupal.behaviors pattern
- [ ] Accept context parameter in attach()
- [ ] Use once() for element processing
- [ ] Implement detach() if creating intervals/global listeners
- [ ] Namespace behavior: `Drupal.behaviors.moduleName`

**Every library definition must**:

- [ ] Include version number for cache busting
- [ ] Declare core/drupal dependency
- [ ] Declare core/once dependency if using once()
- [ ] Use defer attribute unless header placement required
- [ ] Set preprocess: true for aggregation
- [ ] Namespace under module/theme name

**Security requirements**:

- [ ] Sanitize all user input before DOM insertion
- [ ] Use textContent or Drupal.checkPlain() for user data
- [ ] Never pass sensitive data in drupalSettings
- [ ] No eval() or new Function()
- [ ] No inline event handlers
- [ ] CSP-compatible patterns only

**Performance requirements**:

- [ ] Conditional loading where possible
- [ ] Debounce high-frequency events
- [ ] Batch DOM reads/writes
- [ ] Test with aggregation enabled
- [ ] Minimize jQuery dependency

## Common Mistakes

- **Wrong**: Skipping checklist items → **Right**: Verify all requirements
  - **Why**: Missing patterns create bugs, performance issues, security vulnerabilities
- **Wrong**: Not reviewing with AJAX enabled → **Right**: Test all functionality with AJAX
  - **Why**: Most Drupal JS bugs surface with AJAX/BigPipe
- **Wrong**: Not testing with aggregation → **Right**: Test production configuration
  - **Why**: Works in dev, breaks in production

## See Also

- [Common Anti-Patterns](common-anti-patterns.md) - What to avoid
- [Security](security.md) - Security checklist
- [Performance Optimization](performance-optimization.md) - Performance checklist
