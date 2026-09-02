---
description: Show messages, alerts, and screen reader announcements after AJAX operations using MessageCommand, AlertCommand, and AnnounceCommand
tldr: "MessageCommand: 4th param is `$clear_previous`; control screen-reader announcements via `$options['announce']`. AnnounceCommand provides screen-reader-only output; 'polite' waits, 'assertive' interrupts. Never use AlertCommand in production."
drupal_version: "11.x"
---

# Feedback Commands

## When to Use

You need to show messages, alerts, or screen reader announcements after AJAX operations.

## Decision

| Command | Use When | Priority |
|---------|----------|----------|
| MessageCommand | Status, warning, or error messages | Preferred for all user feedback |
| AnnounceCommand | Screen readers only, no visual needed | WCAG compliance for AJAX updates |
| AlertCommand | Debugging only | Never in production |

## Command: MessageCommand

**Description:** Displays Drupal status messages with proper theming and screen reader support.

**Pattern:**

```php
use Drupal\Core\Ajax\MessageCommand;

// Default: clears previous messages, announces via aria-live (polite).
$response->addCommand(new MessageCommand(
  'Operation successful',
  NULL,                   // NULL = default message region
  ['type' => 'status'],   // type: status | warning | error
  TRUE                    // $clear_previous: clear prior messages first
));

// Suppress screen reader announcement:
$response->addCommand(new MessageCommand('Saved.', NULL, ['announce' => '']));

// Assertive announcement (errors requiring immediate attention):
$response->addCommand(new MessageCommand('Upload failed.', NULL, [
  'type' => 'error',
  'priority' => 'assertive',
]));
```

**Parameters:**

| Param | Type | Description |
|-------|------|-------------|
| message | string\|Markup | Message text; plain strings are Xss::filterAdmin-sanitized |
| wrapper_query_selector | string\|NULL | CSS selector for container; NULL uses default region |
| options | array | `type` (status/warning/error), `announce` ('' to suppress), `priority` (assertive) |
| clear_previous | bool | If TRUE (default), existing messages in the region are cleared first |

**Gotchas:**

- The 4th parameter is `$clear_previous`, NOT an "announce" flag — announcement is controlled via `$options['announce']`
- By default MessageCommand also announces via `Drupal.announce()` — pass `['announce' => '']` in options to suppress
- Combining MessageCommand and AnnounceCommand in the same response can cause double-announcements; test with a screen reader
- Source: `core/lib/Drupal/Core/Ajax/MessageCommand.php`

## Command: AlertCommand

**Description:** Shows a JavaScript alert dialog (blocking).

**Pattern:**

```php
use Drupal\Core\Ajax\AlertCommand;

$response->addCommand(new AlertCommand('Alert message'));
```

**Gotchas:**

- Blocks all page interaction until dismissed
- Cannot be styled (native browser dialog)
- Avoid in production (poor UX); use MessageCommand instead
- Useful only for critical errors or debugging

## Command: AnnounceCommand

**Description:** Announces content to screen readers without visual display.

**Pattern:**

```php
use Drupal\Core\Ajax\AnnounceCommand;

$response->addCommand(new AnnounceCommand(
  'Content updated',
  'polite'  // assertive or polite
));
```

**Parameters:**

| Param | Type | Description |
|-------|------|-------------|
| text | string | Message for screen readers |
| priority | string | 'polite' (wait) or 'assertive' (interrupt) |

**Gotchas:**

- No visual indication (screen readers only)
- 'assertive' interrupts current screen reader speech
- 'polite' waits for current speech to finish
- Critical for AJAX accessibility

## Common Mistakes

- Using AlertCommand in production → Terrible UX; use MessageCommand for all user-facing messages
- Not announcing AJAX updates to screen readers → WCAG violation; always use AnnounceCommand or MessageCommand with announce option
- Using 'assertive' priority unnecessarily → Interrupts screen reader users; reserve for critical errors
- Forgetting to escape user input in messages → XSS vulnerability; MessageCommand auto-escapes but verify custom implementations
- Not clearing old messages → Messages accumulate; use RemoveCommand to clear message container when needed

## See Also

- ← Previous: [Dialog Commands](dialog-commands.md) | Next: [Custom AJAX Commands](custom-ajax-commands.md)
- [Screen Reader Support](screen-reader-support.md)
- Reference: `core/lib/Drupal/Core/Ajax/MessageCommand.php`, `core/lib/Drupal/Core/Ajax/AnnounceCommand.php`
