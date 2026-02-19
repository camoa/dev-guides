---
description: Theme hook implementations in ui_suite_daisyui.theme for pagers, forms, and inputs
---

# Preprocess & Hooks

## Hook Implementations

The `ui_suite_daisyui.theme` file implements four hooks:

### `ui_suite_daisyui_preprocess_pager()`

Normalizes the Drupal pager variables into the `LinksPropType` format expected by the `pagination` component. Merges first/previous, numbered pages, and next/last into a flat links array. Removes the URL from the current page link to make it appear as the active page.

### `ui_suite_daisyui_preprocess_views_mini_pager()`

Normalizes the Views mini-pager variables (previous, current count, next) into the `LinksPropType` format for the `pagination` component.

### `ui_suite_daisyui_form_alter()`

Adds DaisyUI button classes to all form submit buttons:

- All submit buttons get `btn` and `btn-primary`
- Non-primary buttons additionally get `btn-secondary`
- Search block form buttons are excluded from the secondary class

### `ui_suite_daisyui_preprocess_input()`

Adds DaisyUI input classes to form elements:

- `file` type: `file-input file-input-bordered`
- All other visible inputs: `input input-bordered`
- Excluded types: `hidden`, `submit`, `token`, `button`

### `ui_suite_daisyui_preprocess_field()`

Adds Tailwind Typography (`prose`) class to formatted text fields:

- Applies to `text`, `text_long`, `text_with_summary` field types
- Adds `prose !container` to preserve WYSIWYG formatting within Tailwind

## Common Mistakes

- **Overriding form_alter without calling parent** -- If your sub-theme implements `form_alter`, the base theme's button styling still applies (Drupal merges hooks). But if you explicitly set `#attributes['class']` on buttons, you may override the DaisyUI classes. WHY: Drupal's class attribute is an array that gets merged, but direct assignment replaces.
- **Not understanding the `prose` class** -- The `prose` class from Tailwind Typography is added to formatted text fields. If you remove or override this in a sub-theme, WYSIWYG content will lose its formatting. WHY: Tailwind CSS resets all element styles; `prose` restores heading, paragraph, list, and other element styling.

## See Also

- `drupal-twig-theming.md` -- Preprocess hook patterns
