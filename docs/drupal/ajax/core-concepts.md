---
description: Drupal AJAX architecture — three-layer system, workflow, and minimal form pattern
drupal_version: "11.x"
---

# AJAX Core Concepts

## When to Use

> Use Drupal AJAX when maintaining existing codebases, working with contributed modules, or needing backward compatibility. Use HTMX (available in Drupal 11.3+) for new projects — it reduces JavaScript size by up to 71%.

## Decision

| Layer | Purpose | Key Components |
|-------|---------|----------------|
| Server-side | Process requests, build responses | FormStateInterface, AjaxResponse, Commands |
| Client-side | Handle events, execute commands | Drupal.ajax, Behaviors API, jQuery |
| Integration | Connect server to client | `#ajax` property, routes, callbacks |

## Pattern

```php
public function buildForm(array $form, FormStateInterface $form_state) {
  $form['trigger'] = [
    '#type' => 'select',
    '#title' => t('Category'),
    '#ajax' => [
      'callback' => '::ajaxCallback',
      'wrapper' => 'target-wrapper',
    ],
  ];

  $form['target'] = [
    '#prefix' => '<div id="target-wrapper">',
    '#suffix' => '</div>',
  ];

  return $form;
}

public function ajaxCallback(array &$form, FormStateInterface $form_state) {
  return $form['target'];  // Return render array or AjaxResponse
}
```

**Workflow:**

```
1. User triggers event (click, change, keyup)
   ↓
2. JavaScript sends AJAX request to server
   ↓
3. PHP callback processes FormStateInterface
   ↓
4. Server returns AjaxResponse with commands
   ↓
5. Client executes commands, updates DOM
   ↓
6. Drupal.behaviors.attach() runs on new content
```

Reference: `core/lib/Drupal/Core/Form/FormBuilderInterface.php`

## Common Mistakes

- **Wrong**: Returning HTML string from callback → **Right**: Always return render arrays or AjaxResponse objects
- **Wrong**: Missing wrapper element → **Right**: Wrapper must exist in DOM before AJAX triggers
- **Wrong**: Omitting `#prefix`/`#suffix` → **Right**: ReplaceCommand needs wrapper ID in returned content
- **Wrong**: Skipping `$form_state->setRebuild()` → **Right**: Required for multi-step workflows to rebuild properly
- **Wrong**: Static calls instead of dependency injection → **Right**: Inject services for testability and caching

## See Also

- [Form Element AJAX Configuration](form-element-ajax-configuration.md)
- Reference: [Drupal AJAX API documentation](https://www.drupal.org/docs/drupal-apis/ajax-api)
- Reference: [AJAX API to HTMX migration](https://www.drupal.org/docs/develop/drupal-apis/htmx/ajax-api-to-htmx)
