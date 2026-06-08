---
description: Cases where AJAX is better than HTMX — complex command sequences, jQuery UI dialogs, CSS manipulation, and contrib dependencies; and when native dialog can migrate
tldr: "Keep AJAX for ordered command sequences, CSS manipulation, jQuery UI dialogs with complex options, jQuery data API, and contrib dependencies. Native <dialog> elements can migrate to HTMX via ->on('::afterSwap', 'showModal()')."
drupal_version: "11.x"
---

# When NOT to Migrate

## When to Use

> Keep AJAX for ordered command sequences, CSS manipulation, jQuery UI dialogs with complex options, jQuery data API, and contrib dependencies. Native `<dialog>` elements can migrate to HTMX via `->on('::afterSwap', 'showModal()')`.

## Decision

| Use Case | Keep AJAX | Migrate to HTMX | Why |
|---|---|---|---|
| Complex command sequences | Yes | — | AJAX commands run in order; HTMX swaps are atomic |
| CSS manipulation | Yes | — | `CssCommand`, `InvokeCommand` have no HTMX equivalent |
| jQuery UI dialogs | Yes | — | `dialogClass`, `buttons`, and jQuery UI options have no HTMX equivalent |
| Native `<dialog>` dialogs | — | Yes | Use `->on('::afterSwap', 'showModal()')` pattern with native HTML element |
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

**Keep AJAX for jQuery UI dialogs with options** — when `dialogClass`, `buttons`, resize handles, or other jQuery UI options are required:
```php
$response->addCommand(new OpenModalDialogCommand('Title', $content, [
  'width' => 700,
  'dialogClass' => 'my-dialog',
]));
```

**Migrate with HTMX using native `<dialog>`** — when jQuery UI options are not needed:
```php
// Ensure a <dialog> element exists in your form or controller build array:
$build['my_modal'] = [
  '#type' => 'html_tag',
  '#tag' => 'dialog',
  '#attributes' => ['id' => 'my-modal'],
  'content' => ['#markup' => '', '#attributes' => ['id' => 'my-modal-content']],
];

// On the trigger element, load content then call showModal():
(new Htmx())
  ->get($dialogUrl)
  ->target('#my-modal-content')
  ->swap('innerHTML')
  ->on('::afterSwap', 'document.getElementById("my-modal")?.showModal()')
  ->applyTo($build['open_button']);
```

## Common Mistakes

- **Forcing HTMX on everything** → AJAX is not deprecated. Use the right tool for each situation
- **Rewriting working AJAX** → If AJAX works and is not causing problems, migration is optional. Focus on new code
- **Ignoring contrib dependencies** → Check whether contrib modules you use expect AJAX. Breaking their assumptions causes bugs
- **Not considering team knowledge** → If your team knows AJAX well and rarely adds new interactive features, migration ROI may be low
- **Treating all dialogs as unmigrateable** → jQuery UI dialogs with complex options stay in AJAX, but simple modal use-cases can migrate to native `<dialog>` + `->on('::afterSwap', 'showModal()')`. The native element requires explicit `::backdrop` CSS and keyboard close handling (`Escape` key works natively)
- **Migrating dialogs without an accessibility plan** → Native `<dialog>` handles focus trapping and `Escape` natively, but you must still provide visible close buttons and test with screen readers

## See Also

- Previous: [Accessibility Migration](accessibility-migration.md)
- Next: [Hybrid AJAX-HTMX Approach](hybrid-ajax-htmx-approach.md)
- Reference: `/core/lib/Drupal/Core/Ajax/` — full AJAX command catalog
