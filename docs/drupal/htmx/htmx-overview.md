---
description: "HTMX in Drupal 11.3+ — core concepts, benefits, and when to use declarative HTML-driven interactions"
tldr: "Use HTMX to build interactive Drupal features that update page regions without full page reloads. Drupal 11.3 adopted it as a simpler, declarative alternative to AJAX with up to 71% less JavaScript; skipping `_htmx_route: TRUE` or `onlyMainContent()` produces full page renders instead of minimal responses."
drupal_version: "11.x"
---

# HTMX Overview

## When to Use

> You're building interactive Drupal features that update page regions without full page reloads, and you want a simpler approach than traditional AJAX with JSON commands.

## What HTMX Is

HTMX extends HTML with attributes that enable dynamic content updates without extensive JavaScript. Elements issue HTTP requests and swap content directly in the DOM using declarative markup:

```html
<button data-hx-get="/contacts/1" data-hx-target="#contact-ui">
  Fetch Contact
</button>
```

Reference: Core implementation at `/core/lib/Drupal/Core/Htmx/Htmx.php` — comprehensive API for all HTMX attributes and headers.

## Why Drupal Adopted HTMX

Drupal 11.3 introduced native HTMX support as a simpler alternative to traditional AJAX.

**Key Benefits:**
- **Declarative approach**: HTML attributes replace imperative JavaScript
- **Smaller footprint**: Reduced JavaScript compared to traditional AJAX framework
- **Progressive enhancement**: Forms/links work without JavaScript
- **Hypermedia-driven**: Aligns with web platform patterns
- **Seamless integration**: Works with Drupal's render system and behaviors

Reference: Change record "Ajax subsystem now includes HTMX" published September 10, 2025 (Drupal 11.3.0).

## Common Mistakes

- Assuming HTMX replaces all AJAX — Traditional AJAX still needed for complex command sequences and contrib module compatibility
- Not using `_htmx_route: TRUE` or `onlyMainContent()` — Results in full page renders instead of minimal responses
- Forgetting progressive enhancement — Always provide non-JavaScript fallback for forms and links
- Using HTMX for heavy client-side processing — HTMX is server-driven; complex JavaScript logic belongs in traditional patterns

## See Also

- Next: [HTMX vs AJAX Decision](htmx-vs-ajax.md)
- Reference: [Official HTMX documentation](https://htmx.org/reference/)
- Reference: [Drupal 11.3 HTMX announcement](https://www.drupal.org/about/core/blog/native-htmx-in-drupal-1130-rich-ux-with-up-to-71-less-javascript)
