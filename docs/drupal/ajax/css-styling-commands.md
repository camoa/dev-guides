---
description: AJAX commands for CSS properties, jQuery method invocation, data attributes, and dynamic CSS loading
tldr: "Use CssCommand for inline styles, InvokeCommand for jQuery methods, DataCommand for `.data()`. AddCssCommand expects `[['href' => '...']]` (link attribute arrays, not library-registry format) — prefer `#attached` for static assets."
drupal_version: "11.x"
---

# CSS Styling Commands

## When to Use

You need to add CSS classes, modify styles, invoke jQuery methods, or attach data to elements via AJAX.

## Decision

| Command | Use When | Avoid When |
|---------|----------|-----------|
| CssCommand | Need inline style changes | Permanent styles — use classes instead |
| InvokeCommand | No specific command exists | A semantic command (CssCommand, etc.) covers the need |
| DataCommand | Need to attach data to elements | Data needs to persist in DOM attributes |
| AddCssCommand | Truly dynamic CSS assets | Static CSS — use `#attached` for aggregation |

## Command: CssCommand

**Description:** Sets CSS properties on elements.

**Pattern:**

```php
use Drupal\Core\Ajax\CssCommand;

$response->addCommand(new CssCommand('#element', [
  'background-color' => '#f0f0f0',
  'border' => '1px solid #ccc',
  'padding' => '10px',
]));
```

**Gotchas:**

- Sets inline styles (high specificity)
- Better to add classes and use CSS when possible
- Property names use JavaScript format (backgroundColor) or CSS format (background-color)

## Command: InvokeCommand

**Description:** Invokes jQuery methods on elements.

**Pattern:**

```php
use Drupal\Core\Ajax\InvokeCommand;

// Add class
$response->addCommand(new InvokeCommand('.message', 'addClass', ['success']));

// Animate
$response->addCommand(new InvokeCommand('.message', 'fadeIn', ['slow']));

// Set value
$response->addCommand(new InvokeCommand('#field', 'val', ['New value']));
```

**Gotchas:**

- Method must exist in jQuery API
- Arguments passed as array to method
- Powerful but tightly couples to jQuery (consider DataCommand or CssCommand alternatives)

## Command: DataCommand

**Description:** Attaches data to elements using jQuery's `.data()` API.

**Pattern:**

```php
use Drupal\Core\Ajax\DataCommand;

$response->addCommand(new DataCommand('#element', 'userId', 123));
$response->addCommand(new DataCommand('#element', 'config', ['key' => 'value']));
```

**Gotchas:**

- Data stored in jQuery's internal cache, not DOM
- Survives DOM updates if element ID persists
- JavaScript retrieves via `$('#element').data('userId')`

## Command: AddCssCommand

**Description:** Dynamically loads CSS files by injecting `<link>` elements.

**Pattern:**

```php
use Drupal\Core\Ajax\AddCssCommand;

// $styles is an array of attribute arrays; each becomes a <link> element.
// 'href' is the only required attribute.
$response->addCommand(new AddCssCommand([
  ['href' => '/modules/custom/my_module/css/dynamic.css'],
]));
```

**Gotchas:**

- Each item in the array maps directly to `<link>` attributes (`href`, `media`, etc.)
- Do NOT pass a library-registry nested array — the constructor expects `[['href' => '...']]`, not `['library_name' => ['css' => ...]]`
- Better to attach via `#attached` when possible so assets participate in aggregation
- Source: `core/lib/Drupal/Core/Ajax/AddCssCommand.php`

## Common Mistakes

- Using CssCommand for permanent styles → Inline styles are hard to maintain; add classes and use stylesheets
- Invoking non-existent jQuery methods → Silent failures in production; test thoroughly
- Overusing InvokeCommand → Prefer semantic commands (ReplaceCommand, CssCommand); InvokeCommand is a fallback
- Not handling jQuery dependency → Code breaks if jQuery isn't loaded; ensure `core/jquery` in library dependencies
- Adding CSS/JS instead of using `#attached` → Bypasses aggregation and caching; use AddCssCommand only for truly dynamic assets

## See Also

- ← Previous: [Content Manipulation Commands](content-manipulation-commands.md) | Next: [Dialog Commands](dialog-commands.md)
- Reference: `core/lib/Drupal/Core/Ajax/CssCommand.php`, `core/lib/Drupal/Core/Ajax/InvokeCommand.php`
