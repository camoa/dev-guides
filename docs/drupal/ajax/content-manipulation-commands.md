---
description: AJAX commands for updating, adding, removing, and rearranging DOM content — ReplaceCommand, HtmlCommand, AppendCommand and others
drupal_version: "11.x"
---

# Content Manipulation Commands

## When to Use

> Use these commands when you need to update DOM content from AJAX callbacks. Choose the command that matches the specific DOM operation needed.

## Decision

| Command | Operation | Key Difference |
|---------|-----------|----------------|
| ReplaceCommand | Replaces the entire element | New content MUST include the wrapper ID |
| HtmlCommand | Replaces inner HTML only | Wrapper element stays intact |
| AppendCommand | Adds inside element, after existing content | For lists, infinite scroll, chat |
| PrependCommand | Adds inside element, before existing content | For most-recent-first displays |
| BeforeCommand | Inserts before element (sibling) | Target element unchanged |
| AfterCommand | Inserts after element (sibling) | Target element unchanged |
| RemoveCommand | Removes element from DOM | Permanently removes; detaches behaviors |

## Pattern

```php
use Drupal\Core\Ajax\AjaxResponse;
use Drupal\Core\Ajax\ReplaceCommand;
use Drupal\Core\Ajax\HtmlCommand;
use Drupal\Core\Ajax\AppendCommand;
use Drupal\Core\Ajax\RemoveCommand;

$response = new AjaxResponse();

// Replace entire element (wrapper ID must be in new content)
$response->addCommand(new ReplaceCommand('#target', '<div id="target">New content</div>'));

// Replace inner HTML only
$response->addCommand(new HtmlCommand('#target', 'New inner HTML'));

// Append to list
$response->addCommand(new AppendCommand('#list', '<li>New item</li>'));

// Remove element
$response->addCommand(new RemoveCommand('#remove-me'));

return $response;
```

Reference: `core/lib/Drupal/Core/Ajax/` (all command classes)

## Common Mistakes

- **Wrong**: Using ReplaceCommand without wrapper ID in new content → **Right**: Element disappears with no error; new content must include the ID
- **Wrong**: Passing render arrays directly to commands → **Right**: Render arrays need `\Drupal::service('renderer')->render()` before adding to commands
- **Wrong**: Forgetting to create AjaxResponse → **Right**: Commands must be added to an AjaxResponse, not a render array
- **Wrong**: Chaining commands in wrong order → **Right**: Commands execute in order added; replace before append
- **Wrong**: Not sanitizing user input in commands → **Right**: Use render arrays or proper escaping to prevent XSS

## See Also

- [CSS Styling Commands](css-styling-commands.md)
- [Feedback Commands](feedback-commands.md)
- Reference: `core/lib/Drupal/Core/Ajax/`
