---
description: Choose between HTMX and traditional AJAX — decision table for Drupal dynamic content patterns
drupal_version: "11.x"
---

# HTMX vs Traditional AJAX

## When to Use

> Use HTMX when replacing content with simple swaps, dependent form fields, load more, or modals. Use traditional AJAX when you need complex command sequences, heavy client-side processing, or contrib module integration.

## Decision

| If you need... | Use | Why |
|----------------|-----|-----|
| Content replacement with simple swap | HTMX | Declarative attributes, less code, better progressive enhancement |
| Forms with dependent fields | HTMX | Built-in form handling, automatic form_build_id, cleaner implementation |
| Load more / infinite scroll | HTMX | Native `swap('beforeend')` and `trigger('revealed')` support |
| Modal/dialog content loading | HTMX | Simple target swapping, minimal JavaScript |
| Complex command sequences (css, invoke, settings) | Traditional AJAX | AJAX commands provide fine-grained DOM control |
| Heavy client-side processing | Traditional AJAX | HTMX is server-driven; complex JS logic needs AJAX callbacks |
| Contrib module integration expecting AJAX | Traditional AJAX | Maintain compatibility with existing ecosystems |
| Gradual migration from AJAX | Both | Systems coexist; use HTMX for new features while maintaining AJAX |

## Pattern

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

## Common Mistakes

- **Wrong**: Trying to use AJAX commands with HTMX → **Right**: HTMX returns HTML, not JSON commands
- **Wrong**: Migrating everything from AJAX to HTMX → **Right**: Some use cases genuinely need AJAX's command flexibility
- **Wrong**: Not testing progressive enhancement → **Right**: HTMX should work without JavaScript
- **Wrong**: Assuming HTMX is always better → **Right**: Choose the right tool for the use case

## See Also

- [HTMX Overview](htmx-overview.md)
- [Request/Response Lifecycle](request-response-lifecycle.md)
- [AJAX Migration Patterns](ajax-migration.md)
- Reference: `/core/modules/system/tests/modules/test_htmx/src/Form/HtmxTestAjaxForm.php`
