---
description: AJAX commands for updating, adding, removing, and rearranging DOM content — ReplaceCommand, HtmlCommand, AppendCommand and others
tldr: "ReplaceCommand swaps the full element (new content must include wrapper ID); HtmlCommand updates inner HTML only. InsertCommand's 3rd param is `$settings` (JS behaviors), not an insertion method — use AppendCommand or PrependCommand for explicit insertion."
drupal_version: "11.x"
---

# Content Manipulation Commands

## When to Use

You need to update, add, remove, or rearrange DOM content from AJAX callbacks.

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
| InsertCommand | Uses `#ajax['method']` from triggering element | 3rd param is `$settings`, not insertion method |

## Command: ReplaceCommand

**Description:** Replaces an entire element with new content (most common command).

**Pattern:**

```php
use Drupal\Core\Ajax\AjaxResponse;
use Drupal\Core\Ajax\ReplaceCommand;

$response = new AjaxResponse();
$response->addCommand(new ReplaceCommand('#target', '<div id="target">New content</div>'));
return $response;
```

**Gotchas:**

- New content MUST include the wrapper ID being replaced
- Replaces outer element; use HtmlCommand to replace inner HTML only
- Attached JavaScript behaviors automatically re-attach to new content

## Command: HtmlCommand

**Description:** Replaces the inner HTML of an element without replacing the element itself.

**Pattern:**

```php
use Drupal\Core\Ajax\HtmlCommand;

$response->addCommand(new HtmlCommand('#target', 'New inner HTML'));
```

**Gotchas:**

- Keeps the wrapper element intact, only changes contents
- Faster than ReplaceCommand when wrapper doesn't need updating
- Doesn't require wrapper ID in replacement content

## Command: AppendCommand

**Description:** Adds content inside an element, after existing content.

**Pattern:**

```php
use Drupal\Core\Ajax\AppendCommand;

$response->addCommand(new AppendCommand('#list', '<li>New item</li>'));
```

**Gotchas:**

- Adds content as last child inside the element
- Useful for infinite scroll, dynamic lists, chat messages
- Can cause memory issues if appending infinitely without cleanup

## Command: PrependCommand

**Description:** Adds content inside an element, before existing content.

**Pattern:**

```php
use Drupal\Core\Ajax\PrependCommand;

$response->addCommand(new PrependCommand('#notifications', '<div class="notification">New alert</div>'));
```

**Gotchas:**

- Adds content as first child inside the element
- Good for most-recent-first displays (notifications, comments)

## Command: BeforeCommand

**Description:** Inserts content before an element (as a sibling, not child).

**Pattern:**

```php
use Drupal\Core\Ajax\BeforeCommand;

$response->addCommand(new BeforeCommand('#target', '<p>Before target</p>'));
```

**Gotchas:**

- Inserts at same DOM level as target, not inside it
- Target element remains unchanged

## Command: AfterCommand

**Description:** Inserts content after an element (as a sibling, not child).

**Pattern:**

```php
use Drupal\Core\Ajax\AfterCommand;

$response->addCommand(new AfterCommand('#target', '<p>After target</p>'));
```

**Gotchas:**

- Inserts at same DOM level as target, not inside it
- Target element remains unchanged

## Command: RemoveCommand

**Description:** Removes an element from the DOM.

**Pattern:**

```php
use Drupal\Core\Ajax\RemoveCommand;

$response->addCommand(new RemoveCommand('#remove-me'));
```

**Gotchas:**

- Permanently removes element; can't be updated afterward
- Detaches JavaScript behaviors before removal (prevents memory leaks)
- Multiple selectors supported: removes all matching elements

## Command: InsertCommand

**Description:** Generic insertion command. When triggered by a form element, uses the element's `#ajax['method']` value to determine how content is inserted. Returns `method: null` in the JSON response — the JavaScript side resolves the method from the original request context.

**Pattern:**

```php
use Drupal\Core\Ajax\InsertCommand;

// Selector and content; 3rd param $settings is for JS behavior settings, NOT insertion method.
$response->addCommand(new InsertCommand('#target', $render_array));
```

**Gotchas:**

- The 3rd constructor parameter is `$settings` (JS behavior data) — there is NO method parameter; passing `['method' => 'append']` does nothing for insertion behavior
- To explicitly choose a DOM insertion method in an AjaxResponse, use the specific command classes (AppendCommand, PrependCommand, etc.) — those map to named jQuery operations
- InsertCommand is most useful for form element callbacks where the method is already encoded in the triggering element's `#ajax['method']`
- Source: `core/lib/Drupal/Core/Ajax/InsertCommand.php`

## Common Mistakes

- Using ReplaceCommand without wrapper ID in new content → Element disappears, no errors shown
- Not rendering arrays properly → Pass render arrays through `\Drupal::service('renderer')->render()` before adding to commands
- Forgetting to create AjaxResponse object → Attempting to add commands to render array won't work
- Chaining commands in wrong order → Commands execute in order added; replace before append, etc.
- Not sanitizing user input in commands → XSS vulnerability; always use render arrays or proper escaping

## See Also

- Next: [CSS Styling Commands](css-styling-commands.md)
- [Feedback Commands](feedback-commands.md)
- Reference: `core/lib/Drupal/Core/Ajax/` (all command classes)
