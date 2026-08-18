---
description: "Eight ui_suite_daisyui_* hook implementations across ui_suite_daisyui.theme, includes/form.theme, and includes/settings.theme for pagers, form config, and theme settings"
tldr: "No hook adds a CSS class to a form element -- hooks in ui_suite_daisyui.theme, includes/form.theme, and includes/settings.theme only compute a config array (#daisy_ui_form); templates/forms/input.html.twig and form-element.html.twig read it and decide the classes. There is no form_alter() and no preprocess_field()."
---

# Preprocess & Hooks

## Hook Implementations

The theme ships **eight `ui_suite_daisyui_*` functions across three files** (plus one private submit callback, `_ui_suite_daisyui_theme_settings_form_submit()`). `ui_suite_daisyui.theme` `include`s the other two files, so all of them run, but only two of the eight live in the `.theme` file itself:

| File | Function |
|------|----------|
| `ui_suite_daisyui.theme` | `ui_suite_daisyui_preprocess_pager()`, `ui_suite_daisyui_preprocess_views_mini_pager()` |
| `includes/form.theme` | `ui_suite_daisyui_form_config()`, `ui_suite_daisyui_preprocess_form_element()`, `ui_suite_daisyui_preprocess_input()` |
| `includes/settings.theme` | `ui_suite_daisyui_form_system_theme_settings_alter()`, `ui_suite_daisyui_form_label()`, `ui_suite_daisyui_form_display()` |

### `ui_suite_daisyui_preprocess_pager()`

Normalizes the Drupal pager variables into the `LinksPropType` format expected by the `pagination` component. Merges first/previous, numbered pages, and next/last into a flat links array. Removes the URL from the current page link to make it appear as the active page.

### `ui_suite_daisyui_preprocess_views_mini_pager()`

Normalizes the Views mini-pager variables (previous, current count, next) into the `LinksPropType` format for the `pagination` component.

### The form pipeline -- config in PHP, classes in Twig

This is the part most people get wrong. **No preprocess hook adds a CSS class to a form element.** The hooks compute a *config array* and hang it on the element; the templates read that array and decide the classes.

`ui_suite_daisyui_form_config($type)` returns (or `NULL` for types it does not handle) an array keyed `wrapper_class`, `wrapper_tag`, `label_class`, `label_tag`, `input_class`, chosen from the two theme settings below. `ui_suite_daisyui_preprocess_form_element()` and `ui_suite_daisyui_preprocess_input()` do nothing but assign that array to `$variables['element']['#daisy_ui_form']` (and, in the form-element case, to the label too).

`templates/forms/input.html.twig` then builds the class list itself:

```twig
{% set input_class = element['#daisy_ui_form']['input_class'] %}
{% set classes = [
    input_class,
    type == 'file' ? 'file-input',
    type == 'checkbox' and is_boolean ? 'toggle',
    type == 'checkbox' and not is_boolean ? 'checkbox',
    type == 'radio' ? 'radio',
    type == 'submit' ? 'btn',
    type == 'submit' and button_type == 'primary' ? 'btn-primary',
] %}
```

So: submit buttons get `btn`, and `btn-primary` **only** when `#button_type == 'primary'`. There is no `btn-secondary` anywhere in the theme, and no search-block special case.

`templates/forms/form-element.html.twig` reads `wrapper_tag` and `wrapper_class` from the same array and adds `mb-4 js-form-item form-item js-form-type-* form-item-* js-form-item-*`.

### `ui_suite_daisyui_form_system_theme_settings_alter()`

Adds a **Form settings** fieldset to the theme settings form with two radios that drive `ui_suite_daisyui_form_config()`:

| Setting | Values | Default |
|---------|--------|---------|
| `form_display` | `fieldset` (DaisyUI `fieldset` wrapper) / `inline` (label wrapper carrying the `input` class) | `fieldset` |
| `form_label` | `label` / `floating-label` -- only visible when `form_display` is `inline` | `label` |

`ui_suite_daisyui_form_label()` and `ui_suite_daisyui_form_display()` read those back out of `ui_suite_daisyui.settings`. Under `inline` + `floating-label` the wrapper becomes `<label class="floating-label">` and `input.html.twig` copies `#title` into the `placeholder` attribute -- the only place the theme mutates an attribute from PHP-derived state.

## Common Mistakes

- **Looking for `hook_form_alter()` in this theme** -- There is none, and there never is a `btn-secondary`. If your submit buttons are not styled the way you expect, the answer is in `templates/forms/input.html.twig`, not in a hook. WHY: the theme moved all class decisions into templates and left the hooks to carry configuration only.
- **Setting `#attributes['class']` on a button and expecting the DaisyUI classes to survive** -- They do survive, because `input.html.twig` calls `attributes.addClass(classes)` on whatever you passed in. Direct assignment in a form definition replaces *your* array, not the template's additions.
- **Assuming the base theme adds `prose` to text fields** -- It does not. There is no `ui_suite_daisyui_preprocess_field()`; nothing in the theme applies Tailwind Typography automatically. The theme ships a `prose` SDC component (`components/prose/prose.twig`, a `<div class="prose">` around a `content` slot) and you have to wrap long-form output in it yourself -- or add the class in a sub-theme preprocess or field template. WHY: Tailwind's preflight resets element styles, so WYSIWYG content renders unstyled until something applies `prose`. Note the component's own description: it works only once the typography plugin is imported, which the starterkit does.
- **Overriding `templates/forms/input.html.twig` without carrying `element['#daisy_ui_form']` forward** -- Drop that lookup and every input loses its class, because the hook supplied data, not markup.

## See Also

- `drupal-twig-theming.md` -- Preprocess hook patterns
