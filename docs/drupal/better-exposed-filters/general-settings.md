---
description: "BEF general settings — auto-submit, secondary options panel, reset button, and input-required configuration keys"
tldr: "Use this guide when configuring BEF's global options that apply to all exposed filters on a View — auto-submit, secondary options panel, reset button, and input-required behavior."
drupal_version: "11.x"
---

# General Settings

## When to Use

> When configuring BEF's global options that apply to all exposed filters on a View — auto-submit, secondary options panel, reset button, and input-required behavior.

## Decision: General Configuration Options

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

## Pattern: Accessing General Settings in Code

```php
// In a form alter or preprocess:
$view = $variables['view'];
$exposed_form = $view->display_handler->getPlugin('exposed_form');
$bef_options = $exposed_form->options['bef']['general'];
// $bef_options['autosubmit'], $bef_options['allow_secondary'], etc.
```

## Common Mistakes

- **Enabling auto-submit without debounce** — For text fields, always set `autosubmit_textfield_delay` to avoid excessive AJAX requests on every keystroke.
- **Hiding submit button without auto-submit** — If you hide the button but auto-submit fails (JS error), users can't submit the form at all.
- **Forgetting to check "Allow secondary"** — Per-filter "is_secondary" options are invisible unless "Allow secondary" is enabled in general settings.

## See Also

- [Auto-Submit](auto-submit.md) — detailed auto-submit configuration
- [Secondary & Collapsible Options](secondary-collapsible.md) — secondary panel details
