---
description: Show messages, alerts, and screen reader announcements after AJAX operations using MessageCommand, AlertCommand, and AnnounceCommand
tldr: "MessageCommand: 4th param is `$clear_previous`; control screen-reader announcements via `$options['announce']`. AnnounceCommand provides screen-reader-only output; 'polite' waits, 'assertive' interrupts. Never use AlertCommand in production."
drupal_version: "11.x"
---

# Feedback Commands

## When to Use

> Use MessageCommand for all user-facing messages. Use AnnounceCommand to notify screen readers of content changes. Reserve AlertCommand for debugging only — never in production.

## Decision

| Command | Use When | Priority |
|---------|----------|----------|
| MessageCommand | Status, warning, or error messages | Preferred for all user feedback |
| AnnounceCommand | Screen readers only, no visual needed | WCAG compliance for AJAX updates |
| AlertCommand | Debugging only | Never in production |

## Pattern

```php
use Drupal\Core\Ajax\MessageCommand;
use Drupal\Core\Ajax\AnnounceCommand;

$response = new AjaxResponse();

// Default: clears previous messages, announces via aria-live (polite).
$response->addCommand(new MessageCommand(
  'Operation successful',
  NULL,                      // NULL = default message region
  ['type' => 'status'],      // status, warning, error
  TRUE                       // $clear_previous: clear prior messages first (default TRUE)
));

// Suppress screen reader announcement:
$response->addCommand(new MessageCommand('Saved.', NULL, ['announce' => '']));

// Assertive announcement (errors requiring immediate attention):
$response->addCommand(new MessageCommand('Upload failed.', NULL, [
  'type' => 'error',
  'priority' => 'assertive',
]));

// Screen reader only announcement (no visual output)
$response->addCommand(new AnnounceCommand(
  'Content updated',
  'polite'  // 'polite' (wait) or 'assertive' (interrupt)
));
```

Reference: `core/lib/Drupal/Core/Ajax/MessageCommand.php`, `core/lib/Drupal/Core/Ajax/AnnounceCommand.php`

## Common Mistakes

- **Wrong**: Treating the 4th param as an announce flag → **Right**: The 4th param is `$clear_previous`; control announcements via `$options['announce']`
- **Wrong**: Using AlertCommand in production → **Right**: Blocks all page interaction; use MessageCommand for all user-facing messages
- **Wrong**: Not announcing AJAX updates to screen readers → **Right**: WCAG violation; always use AnnounceCommand or MessageCommand with announce option
- **Wrong**: Using 'assertive' priority unnecessarily → **Right**: Interrupts current screen reader speech; reserve for critical errors only
- **Wrong**: Combining MessageCommand and AnnounceCommand in the same response → **Right**: Can cause double-announcements; test with a screen reader
- **Wrong**: Not clearing old messages → **Right**: Messages accumulate; pass `TRUE` as 4th param to clear, or use RemoveCommand

## See Also

- [Dialog Commands](dialog-commands.md)
- [Custom AJAX Commands](custom-ajax-commands.md)
- [Screen Reader Support](screen-reader-support.md)
- Reference: `core/lib/Drupal/Core/Ajax/AnnounceCommand.php`
