---
description: "When NOT to Migrate — cases where AJAX is still the right tool, and where native <dialog> replaces jQuery UI"
tldr: "Keep AJAX for ordered command sequences, CSS manipulation, jQuery UI dialogs with complex options, and contrib callbacks. Simple modals can still migrate to HTMX via a native <dialog> plus ->on('::afterSwap', 'showModal()')."
drupal_version: "11.x"
---

# When NOT to Migrate

## When to Use

> Understand when to keep using AJAX instead of migrating to HTMX. Not all AJAX patterns map cleanly to HTMX's hypermedia approach.

## Decision

| Use Case | Keep AJAX | Migrate to HTMX | Why |
|---|---|---|---|
| Complex command sequences | ✓ | — | AJAX commands run in order, HTMX swaps are atomic |
| CSS manipulation | ✓ | — | `CssCommand`, `InvokeCommand` have no HTMX equivalent |
| jQuery UI dialogs | ✓ | — | `dialogClass`, `buttons`, and jQuery UI options have no HTMX equivalent |
| Native `<dialog>` dialogs | — | ✓ | Use `->on('::afterSwap', 'showModal()')` pattern with native HTML element |
| jQuery data API | ✓ | — | `DataCommand` works with jQuery, HTMX uses render arrays |
| Contrib integration | ✓ | — | Many contrib modules expect AJAX callbacks |
| Form element interaction | — | ✓ | HTMX is simpler, no callback methods |
| Content replacement | — | ✓ | HTMX handles this better with CSS selectors |
| Browser history | — | ✓ | HTMX has built-in `pushUrl()` support |

## Pattern

**Keep AJAX for:**

1. **Complex command sequences** — Multiple DOM manipulations in specific order:
```php
$response->addCommand(new RemoveCommand('#old-content'));
$response->addCommand(new PrependCommand('body', $modal));
$response->addCommand(new InvokeCommand('#modal', 'fadeIn'));
$response->addCommand(new CssCommand('#overlay', ['display' => 'block']));
```

2. **jQuery UI dialog with options** — when `dialogClass`, `buttons`, resize handles, or other jQuery UI options are required:
```php
$response->addCommand(new OpenModalDialogCommand('Title', $content, [
  'width' => 700,
  'dialogClass' => 'my-dialog',
]));
```

**Migrate with HTMX using native `<dialog>`** — when jQuery UI options are not needed:
```php
// In your form or controller build array, ensure a <dialog> element exists:
$build['my_modal'] = [
  '#type' => 'html_tag',
  '#tag' => 'dialog',
  '#attributes' => ['id' => 'my-modal'],
  'content' => ['#markup' => '', '#attributes' => ['id' => 'my-modal-content']],
];

// On the trigger element (link or button), load content then call showModal():
(new Htmx())
  ->get($dialogUrl)
  ->target('#my-modal-content')
  ->swap('innerHTML')
  ->on('::afterSwap', 'document.getElementById("my-modal")?.showModal()')
  ->applyTo($build['open_button']);
```

3. **Contrib module callbacks** — Modules that extend AJAX API:
```php
// Many contrib modules provide their own AJAX commands
// or expect AJAX callback signatures
```

## Common Mistakes

- **Forcing HTMX on everything** → AJAX is not deprecated. Use the right tool for each situation
- **Rewriting working AJAX** → If AJAX works and isn't causing problems, migration is optional. Focus on new code
- **Ignoring contrib dependencies** → Check if contrib modules you use expect AJAX. Breaking their assumptions causes bugs
- **Not considering team knowledge** → If your team knows AJAX well and you rarely add new interactive features, migration ROI may be low
- **Treating all dialogs as unmigrateable** → jQuery UI dialogs with complex options stay in AJAX, but simple modal use-cases can migrate to native `<dialog>` + `->on('::afterSwap', 'showModal()')`. The native element requires explicit `::backdrop` CSS and keyboard close handling (`Escape` key works natively)
- **Migrating dialogs without accessibility plan** → Native `<dialog>` handles focus trapping and `Escape` natively, but you must still provide visible close buttons and test with screen readers

## See Also

- Previous: [Accessibility Migration](accessibility-migration.md)
- Next: [Hybrid AJAX-HTMX Approach](hybrid-ajax-htmx-approach.md)
- Reference: `/core/lib/Drupal/Core/Ajax/` for full AJAX command catalog
