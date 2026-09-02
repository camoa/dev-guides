---
description: Open, close, and configure modal dialogs, off-canvas panels, and non-modal dialogs via AJAX commands
tldr: "Use OpenModalDialogCommand when you need to block page interaction. Use OpenDialogCommand for non-blocking side panels."
drupal_version: "11.x"
---

# Dialog Commands

## When to Use

You need to display content in modal dialogs, off-canvas panels, or regular dialogs.

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

## Command: OpenModalDialogCommand

**Description:** Opens content in a modal dialog (blocks page interaction).

**Pattern:**

```php
use Drupal\Core\Ajax\OpenModalDialogCommand;

$content = [
  '#markup' => '<p>Modal content here</p>',
];

$response->addCommand(new OpenModalDialogCommand(
  'Dialog Title',
  $content,
  ['width' => 700, 'height' => 500]  // Optional dialog options
));
```

**Parameters:**

| Param | Type | Description |
|-------|------|-------------|
| title | string | Dialog title (plain text, auto-escaped) |
| content | array/string | Render array or HTML string |
| dialog_options | array | jQuery UI dialog options |
| settings | array | Drupal settings to attach |

**Gotchas:**

- Uses #drupal-modal selector (created automatically)
- Backdrop prevents interaction with main page
- ESC key closes modal by default
- Multiple modals not supported (second call closes first)

## Command: OpenDialogCommand

**Description:** Opens content in a non-modal dialog (page remains interactive).

**Pattern:**

```php
use Drupal\Core\Ajax\OpenDialogCommand;

$response->addCommand(new OpenDialogCommand(
  '#my-dialog',     // Selector for dialog container
  'Dialog Title',
  $content,
  ['width' => 500]
));
```

**Gotchas:**

- Requires existing container element with matching selector
- Page remains interactive (no backdrop)
- Can have multiple dialogs open simultaneously
- Must manually create dialog container if not exists

## Command: OpenOffCanvasDialogCommand

**Description:** Opens content in a side panel.

**Pattern:**

```php
use Drupal\Core\Ajax\OpenOffCanvasDialogCommand;

$response->addCommand(new OpenOffCanvasDialogCommand(
  'Panel Title',
  $content,
  ['width' => 400]
));
```

**Gotchas:**

- Slides in from page edge (typically right side)
- Theme controls positioning and styling
- Common for admin UI, settings panels
- Uses #drupal-off-canvas selector

## Command: CloseModalDialogCommand

**Description:** Closes the currently open modal dialog.

**Pattern:**

```php
use Drupal\Core\Ajax\CloseModalDialogCommand;

$response->addCommand(new CloseModalDialogCommand());
```

**Gotchas:**

- No parameters needed
- Only closes #drupal-modal
- No effect if modal not open

## Command: CloseDialogCommand

**Description:** Closes a specific dialog by selector.

**Pattern:**

```php
use Drupal\Core\Ajax\CloseDialogCommand;

$response->addCommand(new CloseDialogCommand('#my-dialog'));
```

**Gotchas:**

- Requires selector parameter
- Can close any dialog, not just modals
- Silent if dialog doesn't exist

## Command: SetDialogOptionCommand

**Description:** Changes dialog options after it's open.

**Pattern:**

```php
use Drupal\Core\Ajax\SetDialogOptionCommand;

$response->addCommand(new SetDialogOptionCommand('#drupal-modal', 'width', 800));
```

**Gotchas:**

- Uses jQuery UI dialog option() method
- Options depend on jQuery UI dialog widget
- Not all options can be changed after opening

## Command: SetDialogTitleCommand

**Description:** Updates the title of an open dialog.

**Pattern:**

```php
use Drupal\Core\Ajax\SetDialogTitleCommand;

$response->addCommand(new SetDialogTitleCommand('#drupal-modal', 'New Title'));
```

**Gotchas:**

- Shortcut for SetDialogOptionCommand with 'title' option
- Title is plain text, auto-escaped

## Common Mistakes

- Not escaping user content in titles → XSS vulnerability; always use plain text or `Html::escape()`
- Missing dialog library → Dialogs won't open; ensure `core/drupal.dialog.ajax` in page libraries
- Using OpenDialogCommand without container → Dialog fails silently; create container first or use OpenModalDialogCommand
- Forgetting to close dialogs → Memory leaks and UI confusion; always provide close mechanism
- Not handling dialog close events → Use Drupal.behaviors to clean up when dialog closes

## See Also

- ← Previous: [CSS Styling Commands](css-styling-commands.md) | Next: [Feedback Commands](feedback-commands.md)
- Reference: `core/lib/Drupal/Core/Ajax/OpenModalDialogCommand.php`
