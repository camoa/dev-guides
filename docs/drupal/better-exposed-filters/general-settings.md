---
description: BEF general settings — auto-submit, secondary options panel, reset button, and input-required configuration keys
drupal_version: "11.x"
---

# General Settings

## When to Use

> Use this guide when configuring BEF's global options that apply to all exposed filters on a View — auto-submit, secondary options panel, reset button, and input-required behavior.

## Decision

| Option | Config Key | Default | Purpose |
|---|---|---|---|
| Auto-submit | `autosubmit` | FALSE | Submit form automatically when any filter changes |
| Sort-only auto-submit | `auto_submit_sort_only` | FALSE | Auto-submit only when sort changes |
| Breakpoint | `autosubmit_breakpoint` | '' | Media query — only auto-submit above this breakpoint |
| Exclude text fields | `autosubmit_exclude_textfield` | FALSE | Don't auto-submit on text input changes |
| Text field delay | `autosubmit_textfield_delay` | 500 | Debounce delay in ms for text field auto-submit |
| Minimum text length | `autosubmit_textfield_minimum_length` | 3 | Minimum characters before text field triggers submit |
| Hide submit button | `autosubmit_hide` | FALSE | Visually hide the submit button when auto-submit is on |
| Input required | `input_required` | FALSE | Show text instead of results until user filters |
| Allow secondary | `allow_secondary` | FALSE | Enable the secondary options panel |
| Secondary label | `secondary_label` | 'Advanced options' | Label for the secondary options details element |
| Secondary open | `secondary_open` | FALSE | Secondary panel open by default |
| Reset always show | `reset_button_always_show` | FALSE | Show reset button even when no filters are active |

## Pattern

```php
// Access general settings in a form alter or preprocess:
$view = $variables['view'];
$exposed_form = $view->display_handler->getPlugin('exposed_form');
$bef_options = $exposed_form->options['bef']['general'];
// $bef_options['autosubmit'], $bef_options['allow_secondary'], etc.
```

## Common Mistakes

- **Wrong**: Enabling auto-submit without debounce for text fields → **Right**: Set `autosubmit_textfield_delay` to avoid excessive AJAX requests on every keystroke.
- **Wrong**: Hiding the submit button without auto-submit enabled → **Right**: If `autosubmit_hide` is TRUE but auto-submit fails (JS error), users cannot submit the form.
- **Wrong**: Expecting per-filter "is_secondary" options to appear without enabling secondary → **Right**: Enable "Allow secondary" in general settings first. Per-filter options are hidden until then.

## See Also

- [Auto-Submit](auto-submit.md)
- [Secondary & Collapsible Options](secondary-collapsible.md)
- Reference: `web/modules/contrib/better_exposed_filters/src/Plugin/views/exposed_form/BetterExposedFilters.php`
