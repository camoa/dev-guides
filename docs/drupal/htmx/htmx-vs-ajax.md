---
description: "Choose between HTMX and traditional AJAX — decision table for Drupal dynamic content patterns"
tldr: "Use HTMX when replacing content with simple swaps, dependent form fields, load more, or modals; use traditional AJAX for complex command sequences, heavy client-side processing, or contrib module integration. HTMX returns HTML render arrays, not JSON commands."
drupal_version: "11.x"
---

# HTMX vs Traditional AJAX

## When to Use

> You're choosing between HTMX and traditional AJAX for dynamic content, or migrating existing AJAX implementations.

## Decision

| If you need... | Use... | Why |
|---|---|---|
| Content replacement with simple swap | HTMX | Declarative attributes, less code, better progressive enhancement |
| Forms with dependent fields | HTMX | Built-in form handling, automatic form_build_id updates, cleaner implementation |
| Load more / infinite scroll | HTMX | Native `swap('beforeend')` and `trigger('revealed')` support |
| Modal/dialog content loading | HTMX | Simple target swapping, minimal JavaScript |
| Complex command sequences (css, invoke, settings) | Traditional AJAX | AJAX commands provide fine-grained DOM control |
| Heavy client-side processing | Traditional AJAX | HTMX is server-driven; complex JS logic needs AJAX callbacks |
| Contrib module integration expecting AJAX | Traditional AJAX | Maintain compatibility with existing ecosystems |
| Gradual migration from AJAX | Both | Systems coexist; use HTMX for new features while maintaining AJAX |

## Pattern: Basic HTMX vs AJAX Comparison

**Traditional AJAX** returns JSON with command arrays:
```php
$response = new AjaxResponse();
$response->addCommand(new ReplaceCommand('#target', $content));
return $response;
```

**HTMX** returns HTML render arrays:
```php
$build = ['#markup' => '<div>Content</div>'];
(new Htmx())
  ->get(Url::fromRoute('my.route'))
  ->target('#target')
  ->swap('outerHTML');
return $build;
```

Reference: `/core/modules/system/tests/modules/test_htmx/src/Form/HtmxTestAjaxForm.php` demonstrates AJAX inserting HTMX content (both systems coexisting).

## Common Mistakes

- Trying to use AJAX commands with HTMX — HTMX returns HTML, not JSON commands
- Migrating everything from AJAX to HTMX — Some use cases genuinely need AJAX's command flexibility
- Not testing progressive enhancement — HTMX should work without JavaScript
- Assuming HTMX is always better — Choose the right tool for the use case

## See Also

- Previous: [HTMX Overview](htmx-overview.md)
- Next: [Request/Response Lifecycle](request-response-lifecycle.md)
- Reference: [AJAX to HTMX Migration Patterns](ajax-migration.md)
