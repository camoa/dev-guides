---
description: "BEF auto-submit — data attributes, debounce configuration, breakpoint-based submit, and JS behavior details"
tldr: "Use auto-submit when you want the View to refresh automatically when users change filter values, without requiring a manual Apply button click."
drupal_version: "11.x"
---

# Auto-Submit

## When to Use

> When you want the View to refresh automatically when users change filter values, without requiring a manual "Apply" button click.

## Decision: Auto-Submit Options

| Option | Config Key | Default | Behavior |
|---|---|---|---|
| Enable | `autosubmit` | FALSE | Auto-submit on any filter change |
| Sort only | `auto_submit_sort_only` | FALSE | Only auto-submit on sort changes |
| Breakpoint | `autosubmit_breakpoint` | '' | Media query — auto-submit only when matches |
| Exclude text | `autosubmit_exclude_textfield` | FALSE | Skip auto-submit for text fields |
| Text delay | `autosubmit_textfield_delay` | 500 | Debounce delay in ms |
| Min length | `autosubmit_textfield_minimum_length` | 3 | Minimum characters before submit |
| Hide button | `autosubmit_hide` | FALSE | Visually hide submit button |

## Pattern: Data Attributes

BEF communicates auto-submit settings via HTML data attributes:

| Attribute | Purpose |
|---|---|
| `data-bef-auto-submit-full-form` | On form — enables auto-submit for all elements |
| `data-bef-auto-submit` | On individual element — enables auto-submit for that element |
| `data-bef-auto-submit-exclude` | On element — excludes from auto-submit |
| `data-bef-auto-submit-click` | On button — identifies which button to "click" on submit |
| `data-bef-auto-submit-delay` | On form — debounce delay in ms |
| `data-bef-auto-submit-media-query` | On form — CSS media query string |
| `data-bef-auto-submit-minimum-length` | On form — minimum text length |
| `data-bef-auto-submit-sort-only` | On form — only auto-submit on sort changes |

## Pattern: How Auto-Submit Works

1. `Drupal.behaviors.betterExposedFiltersAutoSubmit` attaches to elements matching the data attributes
2. On `change` events (select, radio, checkbox): submits immediately (except date inputs which are debounced)
3. On `keyup` events (text, textarea): debounced by `autosubmit_textfield_delay` ms
4. Ignored keys: Shift, Ctrl, Alt, Caps Lock, Page Up/Down, Home/End, Arrow keys, Tab, Enter, Esc, Space
5. Excluded elements: `[data-bef-auto-submit-exclude]`, `:submit`, `.select2-search__field`, `.chosen-search-input`
6. Finds the button with `data-bef-auto-submit-click` and triggers its click handler

## Pattern: Breakpoint-Based Auto-Submit

Use a CSS media query to only auto-submit above a certain screen width:
```
# In BEF settings, set Breakpoint to:
(min-width: 768px)
```

This prevents auto-submit on mobile where the UX may be poor. The JS checks `matchMedia(mediaQuery).matches` before each submit.

## Common Mistakes

- **Auto-submit fires too aggressively on text** — Set `autosubmit_textfield_delay` to 500-1000ms and `autosubmit_textfield_minimum_length` to 3+ to avoid submitting on every keystroke.
- **Hidden submit button breaks accessibility** — `autosubmit_hide` adds `visually-hidden` class. The button is still in the DOM for accessibility. If JS fails, keyboard users can still tab to it.
- **Auto-submit with exposed form as block** — Works, but the form and View may be far apart on the page. Consider UX implications.
- **Date input rapid-fire** — Date inputs emit `change` events as soon as the value is valid (e.g., after typing day). BEF debounces date change events to prevent premature submission.

## See Also

- [General Settings](general-settings.md) — where auto-submit is configured
- [JavaScript Behaviors](javascript-behaviors.md) — auto_submit.js details
- Reference: `web/modules/contrib/better_exposed_filters/js/auto_submit.js`
