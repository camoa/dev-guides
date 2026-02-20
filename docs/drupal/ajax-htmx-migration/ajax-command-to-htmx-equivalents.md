---
description: Quick reference mapping every Drupal AJAX command to its HTMX equivalent swap strategy or method
drupal_version: "11.x"
---

# AJAX Command to HTMX Equivalents

## When to Use

> Use this reference when converting existing AJAX commands to HTMX patterns. Find the HTMX equivalent of a specific AJAX command before rewriting.

## Decision

| AJAX Command | HTMX Equivalent | Notes |
|---|---|---|
| `ReplaceCommand` | `swap('outerHTML')` | Replace entire element including wrapper |
| `HtmlCommand` | `swap('innerHTML')` | Replace inner content only |
| `AppendCommand` | `swap('beforeend')` | Append inside element at end |
| `PrependCommand` | `swap('afterbegin')` | Prepend inside element at start |
| `BeforeCommand` | `swap('beforebegin')` | Insert before element |
| `AfterCommand` | `swap('afterend')` | Insert after element |
| `RemoveCommand` | Return empty + `swap('outerHTML')` | Remove element from DOM |
| `RedirectCommand` | `redirectHeader(Url)` | Full page redirect via header |
| `MessageCommand` | Auto-included | Via `HtmxRenderer` |
| `SettingsCommand` | Auto-merged | Via `htmx-assets.js` |
| `InvokeCommand` | `on('::afterSwap', 'fn()')` | Custom JavaScript event |
| `CssCommand` | Custom trigger header + JS | Not built-in, use events |
| Multiple commands | `swapOob()` | Out-of-band swaps for multiple elements |

## Pattern

**Multiple DOM updates — AJAX with multiple commands:**
```php
$response = new AjaxResponse();
$response->addCommand(new ReplaceCommand('#content', $content));
$response->addCommand(new ReplaceCommand('#sidebar', $sidebar));
$response->addCommand(new MessageCommand('Updated!'));
```

**Multiple DOM updates — HTMX with out-of-band swaps:**
```php
// Primary target
$build['content'] = [...];

// Additional target via OOB
$build['sidebar'] = [...];
(new Htmx())
  ->swapOob('outerHTML:#sidebar')
  ->applyTo($build['sidebar'], '#wrapper_attributes');

// Messages included automatically
return $build;
```

## Common Mistakes

- **Trying to use `AjaxResponse` with HTMX** → HTMX uses render arrays, not response objects. Return build arrays from controllers
- **Not using `onlyMainContent()` for minimal responses** → Without this, HTMX receives the full page. Use `onlyMainContent()` or `_htmx_route: TRUE` in routing
- **Confusing `select()` and `target()`** → `select()` filters what to extract from response, `target()` specifies where to put it. They can be different selectors
- **Using multiple commands thinking** → HTMX doesn't have "commands". Use `swapOob()` for multiple updates or trigger custom events for JavaScript actions
- **Expecting `MessageCommand` equivalent** → Status messages are automatically included in HTMX responses. No explicit command needed

## See Also

- Previous: [AJAX vs HTMX Fundamentals](ajax-vs-htmx-fundamentals.md)
- Next: [Dependent Dropdown Migration](dependent-dropdown-migration.md)
- Reference: [HTMX swap strategies](https://htmx.org/attributes/hx-swap/)
- Source: `/core/lib/Drupal/Core/Render/MainContent/HtmxRenderer.php`
