---
description: BEF auto-submit — data attributes, debounce configuration, breakpoint-based submit, and JS behavior details
tldr: "Use auto-submit when you want the View to refresh automatically when users change filter values, without requiring a manual \"Apply\" button click. Avoid auto-submit on mobile without a breakpoint guard."
drupal_version: "11.x"
---

# Auto-Submit

## When to Use

> Use auto-submit when you want the View to refresh automatically when users change filter values, without requiring a manual "Apply" button click. Avoid auto-submit on mobile without a breakpoint guard.

## Decision

| Option | Config Key | Default | Behavior |
|---|---|---|---|
| Enable | `autosubmit` | FALSE | Auto-submit on any filter change |
| Sort only | `auto_submit_sort_only` | FALSE | Only auto-submit on sort changes |
| Breakpoint | `autosubmit_breakpoint` | '' | CSS media query — auto-submit only when matches |
| Exclude text | `autosubmit_exclude_textfield` | FALSE | Skip auto-submit for text fields |
| Text delay | `autosubmit_textfield_delay` | 500 | Debounce delay in ms |
| Min length | `autosubmit_textfield_minimum_length` | 3 | Minimum characters before submit |
| Hide button | `autosubmit_hide` | FALSE | Visually hide submit button (`visually-hidden` class) |

## Pattern

**Data attributes BEF sets on the form:**

| Attribute | Purpose |
|---|---|
| `data-bef-auto-submit-full-form` | On form — enables auto-submit for all elements |
| `data-bef-auto-submit` | On individual element — enables for that element |
| `data-bef-auto-submit-exclude` | On element — excludes from auto-submit |
| `data-bef-auto-submit-delay` | On form — debounce delay in ms |
| `data-bef-auto-submit-media-query` | On form — CSS media query string |
| `data-bef-auto-submit-minimum-length` | On form — minimum text length |

**JS behavior (`Drupal.behaviors.betterExposedFiltersAutoSubmit`):**
- `change` on non-date elements: submits immediately
- `change` on date inputs: debounced (prevents premature submit while typing)
- `keyup` on text/textarea: debounced by configured delay
- Ignored keys: Shift, Ctrl, Alt, Caps Lock, Page Up/Down, Home/End, Arrow keys, Tab, Enter, Esc
- Excluded: `.select2-search__field`, `.chosen-search-input`

**Breakpoint guard (prevent auto-submit on mobile):**
```
# In BEF settings, set Breakpoint to:
(min-width: 768px)
```

## Common Mistakes

- **Wrong**: Auto-submit without debounce on text fields → **Right**: Set `autosubmit_textfield_delay` to 500-1000ms and `autosubmit_textfield_minimum_length` to 3+ to avoid submitting on every keystroke.
- **Wrong**: Hiding submit button when auto-submit may fail → **Right**: `autosubmit_hide` adds `visually-hidden` — the button stays in the DOM. If JS fails, keyboard users can still reach it.
- **Wrong**: Using auto-submit on mobile without a breakpoint → **Right**: Add a media query breakpoint to disable auto-submit on small screens where the UX may be poor.

## See Also

- [General Settings](general-settings.md)
- [JavaScript Behaviors](javascript-behaviors.md)
- Reference: `web/modules/contrib/better_exposed_filters/js/auto_submit.js`
