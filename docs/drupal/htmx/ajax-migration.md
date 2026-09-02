---
description: "Migrate Drupal AJAX implementations to HTMX — patterns for buttons, forms, multiple updates, and migration checklist"
tldr: "Use this when converting existing AJAX implementations to HTMX, or running both systems in parallel during gradual migration. Simple content replacement and dependent fields migrate well; complex command sequences and heavy JS processing should stay AJAX."
drupal_version: "11.x"
---

# Migrating from Traditional AJAX

## When to Use

> You're converting existing AJAX implementations to HTMX or running both systems in parallel.

## Migration Strategy

**When to Migrate:**

| AJAX Pattern | Migrate to HTMX? | Reason |
|---|---|---|
| Simple content replacement | Yes | HTMX simpler, less code |
| Form field dependencies | Yes | Better DX, automatic form_build_id handling |
| Load more / infinite scroll | Yes | Native HTMX patterns |
| Modal content loading | Yes | Simpler target swapping |
| Complex command sequences (css, invoke, settings) | No | AJAX commands needed |
| Heavy JavaScript processing | No | HTMX is server-driven |
| Contrib module integration | No | Maintain compatibility |

**Gradual Migration:**
Both systems coexist. Migrate new features to HTMX while maintaining existing AJAX functionality.

Reference: `/core/modules/system/tests/modules/test_htmx/src/Form/HtmxTestAjaxForm.php` demonstrates AJAX inserting HTMX content

## Pattern: AJAX Button → HTMX Button

**Before (AJAX):**
```php
$form['load_button'] = [
  '#type' => 'button',
  '#value' => 'Load Content',
  '#ajax' => [
    'callback' => '::ajaxCallback',
    'wrapper' => 'content-wrapper',
    'method' => 'replace',
  ],
];

$form['content'] = [
  '#type' => 'container',
  '#attributes' => ['id' => 'content-wrapper'],
];

public function ajaxCallback(array &$form, FormStateInterface $form_state) {
  $response = new AjaxResponse();
  $content = ['#markup' => '<div>New content</div>'];
  $response->addCommand(new ReplaceCommand('#content-wrapper', $content));
  return $response;
}
```

**After (HTMX):**
```php
$form['load_button'] = [
  '#type' => 'button',
  '#value' => 'Load Content',
];

(new Htmx())
  ->get(Url::fromRoute('my.route'))
  ->target('#content-wrapper')
  ->swap('innerHTML')
  ->onlyMainContent()
  ->applyTo($form['load_button']);

$form['content'] = [
  '#type' => 'container',
  '#attributes' => ['id' => 'content-wrapper'],
];

// Route controller returns render array directly
public function htmxContent() {
  return ['#markup' => '<div>New content</div>'];
}
```

## Pattern: AJAX Form → HTMX Form

**Before (AJAX):**
```php
$form['type'] = [
  '#type' => 'select',
  '#options' => $types,
  '#ajax' => [
    'callback' => '::updateName',
    'wrapper' => 'name-wrapper',
  ],
];

$form['name_wrapper'] = [
  '#type' => 'container',
  '#attributes' => ['id' => 'name-wrapper'],
];

$form['name_wrapper']['name'] = [
  '#type' => 'select',
  '#options' => $this->getNames($type),
];

public function updateName(array &$form, FormStateInterface $form_state) {
  return $form['name_wrapper'];
}
```

**After (HTMX):**
```php
$form['type'] = [
  '#type' => 'select',
  '#options' => $types,
  '#default_value' => $type,
];

(new Htmx())
  ->post(Url::fromRoute('<current>'))
  ->onlyMainContent()
  ->select('*:has(>select[name="name"])')
  ->target('*:has(>select[name="name"])')
  ->swap('outerHTML')
  ->applyTo($form['type']);

$default_type = $form_state->getValue('type', $type);
$form['name'] = [
  '#type' => 'select',
  '#options' => $this->getNames($default_type),
  '#default_value' => $name,
];

// No callback needed - buildForm() handles everything
// Detect trigger via $this->getHtmxTriggerName()
```

## Pattern: Multiple AJAX Commands → OOB Swaps

**Before (AJAX):**
```php
public function ajaxCallback(array &$form, FormStateInterface $form_state) {
  $response = new AjaxResponse();
  $response->addCommand(new ReplaceCommand('#region-1', $content1));
  $response->addCommand(new ReplaceCommand('#region-2', $content2));
  $response->addCommand(new InvokeCommand('.alert', 'show'));
  return $response;
}
```

**After (HTMX):**
```php
// Primary target
$form['region1']['#markup'] = '<div>Content 1</div>';

// Out-of-band updates
(new Htmx())
  ->swapOob('outerHTML:#region-2')
  ->applyTo($form['region2'], '#wrapper_attributes');

// For JavaScript invoke commands, use trigger header
(new Htmx())
  ->triggerHeader(['showAlert' => []])
  ->applyTo($form);

// JavaScript behavior handles custom event
htmx.on('showAlert', () => {
  document.querySelector('.alert').show();
});
```

## Comparison: AJAX vs HTMX

| Aspect | AJAX | HTMX |
|---|---|---|
| Response type | JSON with commands | HTML render arrays |
| Configuration | `#ajax` array | `Htmx` class methods |
| Callbacks | Required | Optional (use routes) |
| Multiple updates | Command array | Out-of-band swaps |
| JavaScript | Heavy use | Minimal, declarative |
| Progressive enhancement | Harder | Built-in |
| form_build_id | Manual handling | Automatic OOB swap |

## Migration Checklist

- [ ] Identify AJAX callbacks — Simple content returns migrate well
- [ ] Check for command complexity — Multiple commands may stay AJAX
- [ ] Convert callbacks to routes — Or use buildForm() for forms
- [ ] Replace `#ajax` with `Htmx` attributes
- [ ] Update JavaScript behaviors — Listen for `htmx:drupal:load`
- [ ] Test progressive enhancement — Form should work without JavaScript
- [ ] Update tests — Change AJAX test expectations to HTMX
- [ ] Document migration decisions — Why some stayed AJAX, why some moved to HTMX

## Common Mistakes

- Trying to use AJAX commands with HTMX — Return HTML, not JSON
- Not updating behaviors for HTMX events — Use `htmx:drupal:load` instead of AJAX events
- Migrating everything blindly — Some use cases genuinely need AJAX
- Forgetting to test both systems — During gradual migration, both must work
- Not removing old AJAX callbacks — Dead code accumulates

## See Also

- Previous: [Troubleshooting](troubleshooting.md)
- Next: [Core File Reference](core-file-reference.md)
- Reference: [HTMX vs AJAX Decision](htmx-vs-ajax.md)
- Reference: `/core/modules/system/tests/modules/test_htmx/`
