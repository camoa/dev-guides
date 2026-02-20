---
description: Open, close, and configure modal dialogs, off-canvas panels, and non-modal dialogs via AJAX commands
drupal_version: "11.x"
---

# Dialog Commands

## When to Use

> Use OpenModalDialogCommand when you need to block page interaction. Use OpenDialogCommand for non-blocking side panels. Use OpenOffCanvasDialogCommand for admin-style slide-in panels.

## Decision

| Scenario | Command | Notes |
|----------|---------|-------|
| Block page, one dialog at a time | OpenModalDialogCommand | Uses `#drupal-modal`; no backdrop for multiple |
| Non-blocking dialog | OpenDialogCommand | Requires existing container element |
| Admin slide-in panel | OpenOffCanvasDialogCommand | Uses `#drupal-off-canvas` |
| Close current modal | CloseModalDialogCommand | No parameters needed |
| Close specific dialog | CloseDialogCommand | Requires selector |
| Change dialog option after open | SetDialogOptionCommand | Uses jQuery UI dialog option() |
| Update open dialog title | SetDialogTitleCommand | Plain text, auto-escaped |

## Pattern

```php
use Drupal\Core\Ajax\OpenModalDialogCommand;
use Drupal\Core\Ajax\CloseModalDialogCommand;

$response = new AjaxResponse();

// Open modal
$content = ['#markup' => '<p>Modal content here</p>'];
$response->addCommand(new OpenModalDialogCommand(
  'Dialog Title',
  $content,
  ['width' => 700, 'height' => 500]
));

// Close modal
$response->addCommand(new CloseModalDialogCommand());
```

Reference: `core/lib/Drupal/Core/Ajax/OpenModalDialogCommand.php`

## Common Mistakes

- **Wrong**: Not escaping user content in titles → **Right**: Always use plain text or `Html::escape()`; XSS vulnerability otherwise
- **Wrong**: Missing dialog library → **Right**: Dialogs won't open; ensure `core/drupal.dialog.ajax` in page libraries
- **Wrong**: Using OpenDialogCommand without container → **Right**: Dialog fails silently; create container first or use OpenModalDialogCommand
- **Wrong**: Forgetting to close dialogs → **Right**: Memory leaks and UI confusion; always provide a close mechanism
- **Wrong**: Not handling dialog close events → **Right**: Use Drupal.behaviors to clean up when dialog closes

## See Also

- [CSS Styling Commands](css-styling-commands.md)
- [Feedback Commands](feedback-commands.md)
- Reference: `core/lib/Drupal/Core/Ajax/OpenModalDialogCommand.php`
