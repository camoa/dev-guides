---
description: Migrate Drupal AJAX implementations to HTMX — patterns for buttons, forms, multiple updates, and migration checklist
drupal_version: "11.x"
---

# AJAX to HTMX Migration

## When to Use

> Use this when converting existing AJAX implementations to HTMX, or running both systems in parallel during gradual migration.

## Decision

| AJAX Pattern | Migrate to HTMX? | Reason |
|---|---|---|
| Simple content replacement | Yes | HTMX simpler, less code |
| Form field dependencies | Yes | Better DX, automatic form_build_id handling |
| Load more / infinite scroll | Yes | Native HTMX patterns |
| Modal content loading | Yes | Simpler target swapping |
| Complex command sequences (css, invoke, settings) | No | AJAX commands needed |
| Heavy JavaScript processing | No | HTMX is server-driven |
| Contrib module integration | No | Maintain compatibility |

## Pattern

**AJAX button → HTMX button:**

Before (AJAX):

```php
$form['load_button'] = [
  '#type' => 'button',
  '#value' => 'Load Content',
  '#ajax' => ['callback' => '::ajaxCallback', 'wrapper' => 'content-wrapper'],
];
public function ajaxCallback(array &$form, FormStateInterface $form_state) {
  $response = new AjaxResponse();
  $response->addCommand(new ReplaceCommand('#content-wrapper', $content));
  return $response;
}
```

After (HTMX):

```php
$form['load_button'] = ['#type' => 'button', '#value' => 'Load Content'];
(new Htmx())
  ->get(Url::fromRoute('my.route'))
  ->target('#content-wrapper')
  ->swap('innerHTML')
  ->onlyMainContent()
  ->applyTo($form['load_button']);
// Controller returns render array directly — no callback needed
```

**Multiple AJAX commands → OOB swaps:**

Before (AJAX):

```php
$response->addCommand(new ReplaceCommand('#region-1', $content1));
$response->addCommand(new ReplaceCommand('#region-2', $content2));
$response->addCommand(new InvokeCommand('.alert', 'show'));
```

After (HTMX):

```php
// Primary target handles region-1 automatically
(new Htmx())->swapOob('outerHTML:#region-2')->applyTo($form['region2'], '#wrapper_attributes');
(new Htmx())->triggerHeader(['showAlert' => []])->applyTo($form);
// JS: htmx.on('showAlert', () => document.querySelector('.alert').show());
```

**Migration checklist:**

- [ ] Identify AJAX callbacks — simple content returns migrate well
- [ ] Check for command complexity — multiple commands may stay AJAX
- [ ] Replace `#ajax` arrays with `Htmx` class attributes
- [ ] Update JavaScript behaviors — listen for `htmx:drupal:load` instead of AJAX events
- [ ] Test progressive enhancement — form should work without JavaScript
- [ ] Update tests — change AJAX test expectations to HTMX
- [ ] Document decisions — why some stayed AJAX, why some moved

## Common Mistakes

- **Wrong**: Trying to use AJAX commands with HTMX → **Right**: Return HTML render arrays, not JSON
- **Wrong**: Not updating behaviors for HTMX events → **Right**: Use `htmx:drupal:load` instead of AJAX events
- **Wrong**: Migrating everything blindly → **Right**: Some use cases genuinely need AJAX
- **Wrong**: Not removing old AJAX callbacks → **Right**: Dead code accumulates

## See Also

- [Troubleshooting](troubleshooting.md)
- [Core File Reference](core-file-reference.md)
- [HTMX vs AJAX Decision](htmx-vs-ajax.md)
- Reference: `/core/modules/system/tests/modules/test_htmx/src/Form/HtmxTestAjaxForm.php`
