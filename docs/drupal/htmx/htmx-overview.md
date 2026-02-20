---
description: HTMX in Drupal 11.3+ — core concepts, benefits, and when to use declarative HTML-driven interactions
drupal_version: "11.x"
---

# HTMX Overview

## When to Use

> Use HTMX when you're building interactive Drupal features that update page regions without full page reloads and want a simpler approach than traditional AJAX. Use traditional AJAX when you need complex command sequences or contrib module compatibility.

## Decision

| Situation | Choose | Why |
|-----------|--------|-----|
| Content replacement, simple swap | HTMX | Declarative attributes, less code |
| Forms with dependent fields | HTMX | Automatic form_build_id, cleaner DX |
| Up to 71% less JavaScript needed | HTMX | Drupal 11.3 core integration |
| Complex AJAX command sequences | Traditional AJAX | Fine-grained DOM control |
| Contrib module integration | Traditional AJAX | Maintain compatibility |

## Pattern

```html
<button data-hx-get="/contacts/1" data-hx-target="#contact-ui">
  Fetch Contact
</button>
```

HTMX extends HTML with attributes that enable dynamic content updates without extensive JavaScript. Elements issue HTTP requests and swap content directly in the DOM.

## Common Mistakes

- **Wrong**: Assuming HTMX replaces all AJAX → **Right**: Traditional AJAX still needed for complex command sequences and contrib module compatibility
- **Wrong**: Not using `_htmx_route: TRUE` or `onlyMainContent()` → **Right**: Without these, routes return full page renders instead of minimal responses
- **Wrong**: Forgetting progressive enhancement → **Right**: Always provide a non-JavaScript fallback for forms and links
- **Wrong**: Using HTMX for heavy client-side processing → **Right**: HTMX is server-driven; complex JS logic belongs in traditional patterns

## See Also

- [HTMX vs AJAX Decision](htmx-vs-ajax.md)
- [Request/Response Lifecycle](request-response-lifecycle.md)
- Reference: [Official HTMX documentation](https://htmx.org/reference/)
- Reference: [Drupal 11.3 HTMX announcement](https://www.drupal.org/about/core/blog/native-htmx-in-drupal-1130-rich-ux-with-up-to-71-less-javascript)
- Reference: `/core/lib/Drupal/Core/Htmx/Htmx.php`
