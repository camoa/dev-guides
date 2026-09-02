---
description: Drupal AJAX architecture — three-layer system, workflow, and minimal form pattern
tldr: "Drupal AJAX: PHP callbacks return AjaxResponse objects; clients execute commands and re-attach behaviors. Required for ordered sequences, the dialog system, and contrib compatibility. HTMX is the alternative for new work in Drupal 11.3+."
drupal_version: "11.x"
---

# AJAX Core Concepts

## When to Use

You need to understand Drupal's AJAX architecture, workflow, and component interaction.

> Use Drupal AJAX when maintaining existing codebases, working with contributed modules, or requiring ordered command sequences and the core dialog system. See [Drupal HTMX Development Guide](../htmx/index.md) for HTMX-based approaches available in Drupal 11.3+.

## Architecture

Drupal's AJAX system has three layers:

| Layer | Purpose | Key Components |
|-------|---------|----------------|
| Server-side | Process requests, build responses | FormStateInterface, AjaxResponse, Commands |
| Client-side | Handle events, execute commands | Drupal.ajax, Behaviors API, jQuery |
| Integration | Connect server to client | `#ajax` property, routes, callbacks |

## Workflow

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

## Pattern

```php
// Minimal AJAX-enabled form element
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

Reference: `core/lib/Drupal/Core/Form/FormBuilderInterface.php`

## Common Mistakes

- Returning HTML string instead of render array → Always return render arrays or AjaxResponse objects
- Missing wrapper element → Wrapper must exist in DOM before AJAX triggers
- Forgetting `#prefix`/`#suffix` → ReplaceCommand needs wrapper ID in returned content
- Not calling `$form_state->setRebuild()` → Form won't rebuild properly for multi-step workflows
- Using static calls instead of dependency injection → Breaks testability and caching

## See Also

- Next: [Form Element AJAX Configuration](form-element-ajax-configuration.md)
- Reference: [Drupal AJAX API documentation](https://www.drupal.org/docs/drupal-apis/ajax-api)
- Reference: [AJAX API to HTMX documentation](https://www.drupal.org/docs/develop/drupal-apis/htmx/ajax-api-to-htmx)
