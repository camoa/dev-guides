---
description: Cases where AJAX is better than HTMX — complex command sequences, dialogs, CSS manipulation, and contrib dependencies
drupal_version: "11.x"
---

# When NOT to Migrate

## When to Use

> Use AJAX when you need ordered command sequences, the core dialog system, CSS manipulation, jQuery data API, or when contrib modules expect AJAX callbacks.

## Decision

| Use Case | Keep AJAX | Migrate to HTMX | Why |
|---|---|---|---|
| Complex command sequences | Yes | — | AJAX commands run in order; HTMX swaps are atomic |
| CSS manipulation | Yes | — | `CssCommand`, `InvokeCommand` have no HTMX equivalent |
| Modal dialogs (core) | Yes | — | `OpenModalDialogCommand` integrates with core dialog system |
| jQuery data API | Yes | — | `DataCommand` works with jQuery; HTMX uses render arrays |
| Contrib integration | Yes | — | Many contrib modules expect AJAX callbacks |
| Form element interaction | — | Yes | HTMX is simpler, no callback methods |
| Content replacement | — | Yes | HTMX handles this better with CSS selectors |
| Browser history | — | Yes | HTMX has built-in `pushUrl()` support |

## Pattern

**Keep AJAX for complex command sequences:**
```php
$response->addCommand(new RemoveCommand('#old-content'));
$response->addCommand(new PrependCommand('body', $modal));
$response->addCommand(new InvokeCommand('#modal', 'fadeIn'));
$response->addCommand(new CssCommand('#overlay', ['display' => 'block']));
```

**Keep AJAX for core dialog system:**
```php
$response->addCommand(new OpenModalDialogCommand('Title', $content, [
  'width' => 700,
  'dialogClass' => 'my-dialog',
]));
```

## Common Mistakes

- **Forcing HTMX on everything** → AJAX is not deprecated. Use the right tool for each situation
- **Rewriting working AJAX** → If AJAX works and is not causing problems, migration is optional. Focus on new code
- **Ignoring contrib dependencies** → Check whether contrib modules you use expect AJAX. Breaking their assumptions causes bugs
- **Not considering team knowledge** → If your team knows AJAX well and rarely adds new interactive features, migration ROI may be low
- **Migrating dialogs without a plan** → Core dialog commands are well-tested. Custom HTMX dialog patterns need careful accessibility work

## See Also

- Previous: [Accessibility Migration](accessibility-migration.md)
- Next: [Hybrid AJAX-HTMX Approach](hybrid-ajax-htmx-approach.md)
- Reference: `/core/lib/Drupal/Core/Ajax/` — full AJAX command catalog
