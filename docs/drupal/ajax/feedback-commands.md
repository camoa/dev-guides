---
description: Show messages, alerts, and screen reader announcements after AJAX operations using MessageCommand, AlertCommand, and AnnounceCommand
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

// User-facing message (auto-escaped, screen reader aware)
$response->addCommand(new MessageCommand(
  'Operation successful',
  NULL,                      // Selector (NULL = default message region)
  ['type' => 'status'],      // status, warning, error
  TRUE                       // Announce to screen readers
));

// Screen reader only announcement
$response->addCommand(new AnnounceCommand(
  'Content updated',
  'polite'  // 'polite' (wait) or 'assertive' (interrupt)
));
```

Reference: `core/lib/Drupal/Core/Ajax/MessageCommand.php`, `core/lib/Drupal/Core/Ajax/AnnounceCommand.php`

## Common Mistakes

- **Wrong**: Using AlertCommand in production → **Right**: Blocks all page interaction; use MessageCommand for all user-facing messages
- **Wrong**: Not announcing AJAX updates to screen readers → **Right**: WCAG violation; always use AnnounceCommand or MessageCommand with announce option
- **Wrong**: Using 'assertive' priority unnecessarily → **Right**: Interrupts current screen reader speech; reserve for critical errors only
- **Wrong**: Not escaping user input in messages → **Right**: MessageCommand auto-escapes, but verify any custom implementations
- **Wrong**: Not clearing old messages → **Right**: Messages accumulate; use RemoveCommand to clear message container when needed

## See Also

- [Dialog Commands](dialog-commands.md)
- [Custom AJAX Commands](custom-ajax-commands.md)
- [Screen Reader Support](screen-reader-support.md)
- Reference: `core/lib/Drupal/Core/Ajax/AnnounceCommand.php`
