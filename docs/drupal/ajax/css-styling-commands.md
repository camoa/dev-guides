---
description: AJAX commands for CSS properties, jQuery method invocation, data attributes, and dynamic CSS loading
drupal_version: "11.x"
---

# CSS Styling Commands

## When to Use

> Use CSS styling commands for dynamic visual changes triggered by AJAX responses. Prefer adding classes over inline styles. Use InvokeCommand only when no semantic command exists.

## Decision

| Command | Use When | Avoid When |
|---------|----------|-----------|
| CssCommand | Need inline style changes | Permanent styles — use classes instead |
| InvokeCommand | No specific command exists | A semantic command (CssCommand, etc.) covers the need |
| DataCommand | Need to attach data to elements | Data needs to persist in DOM attributes |
| AddCssCommand | Truly dynamic CSS assets | Static CSS — use `#attached` for aggregation |

## Pattern

```php
use Drupal\Core\Ajax\CssCommand;
use Drupal\Core\Ajax\InvokeCommand;
use Drupal\Core\Ajax\DataCommand;

$response = new AjaxResponse();

// Set inline CSS properties
$response->addCommand(new CssCommand('#element', [
  'background-color' => '#f0f0f0',
  'border' => '1px solid #ccc',
]));

// Invoke jQuery method
$response->addCommand(new InvokeCommand('.message', 'addClass', ['success']));
$response->addCommand(new InvokeCommand('.message', 'fadeIn', ['slow']));
$response->addCommand(new InvokeCommand('#field', 'val', ['New value']));

// Attach data to element
$response->addCommand(new DataCommand('#element', 'userId', 123));
// Retrieved in JS: $('#element').data('userId')
```

Reference: `core/lib/Drupal/Core/Ajax/CssCommand.php`, `core/lib/Drupal/Core/Ajax/InvokeCommand.php`

## Common Mistakes

- **Wrong**: Using CssCommand for permanent styles → **Right**: Add classes and use stylesheets; inline styles are hard to maintain
- **Wrong**: Invoking non-existent jQuery methods → **Right**: Silent failures in production; test thoroughly before deploying
- **Wrong**: Overusing InvokeCommand → **Right**: Prefer semantic commands (ReplaceCommand, CssCommand); InvokeCommand is a fallback
- **Wrong**: Not ensuring jQuery is loaded → **Right**: Add `core/jquery` to library dependencies
- **Wrong**: Using AddCssCommand for static assets → **Right**: Use `#attached` for aggregation and caching benefits

## See Also

- [Content Manipulation Commands](content-manipulation-commands.md)
- [Dialog Commands](dialog-commands.md)
- Reference: `core/lib/Drupal/Core/Ajax/InvokeCommand.php`
