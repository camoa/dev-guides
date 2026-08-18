---
description: "22 Drupal template overrides that delegate to DaisyUI SDC components"
tldr: "22 Drupal template overrides delegate to DaisyUI SDC components; every form template lives in templates/forms/, not templates/system/, and tab variants use DaisyUI 5 names (lift, border) -- the v4 lifted/bordered/form-control spellings render unstyled."
---

# Template Overrides

## Templates Provided by the Theme

The theme ships 29 Twig templates under `templates/`: 22 Drupal template overrides plus 7 that re-skin the `ui_patterns_library` and `ui_styles_library` admin browsers. The overrides live in five directories -- note that **every form template is in `templates/forms/`, not `templates/system/`**:

| Template | Path | Purpose |
|---|---|---|
| `page.html.twig` | `templates/system/` | Main page layout using navbar + grid components |
| `block.html.twig` | `templates/system/` | Simplified block wrapper |
| `block--system-branding-block.html.twig` | `templates/system/` | Site name as `btn btn-ghost text-xl` |
| `breadcrumb.html.twig` | `templates/system/` | Delegates to `breadcrumbs` component |
| `page-title.html.twig` | `templates/system/` | `text-4xl font-extrabold mb-8 mt-12` |
| `status-messages.html.twig` | `templates/system/` | Maps Drupal message types to alert variants |
| `menu-local-tasks.html.twig` | `templates/system/` | Primary tabs with `variant: 'lift'`, secondary with `variant: 'border'` |
| `menu-local-task.html.twig` | `templates/system/` | Delegates to `tab` component |
| `pager.html.twig` | `templates/system/` | Delegates to `pagination` component |
| `select.html.twig` | `templates/forms/` | Adds `select select-bordered` classes |
| `input.html.twig` | `templates/forms/` | Builds every input class list from `element['#daisy_ui_form']` (see section 8) |
| `form-element.html.twig` | `templates/forms/` | Wrapper tag/class from `#daisy_ui_form`, plus `mb-4` and Drupal's `js-form-item form-item form-item-*` classes |
| `form-element-label.html.twig` | `templates/forms/` | Label tag/class from `#daisy_ui_form` |
| `fieldset.html.twig`, `textarea.html.twig`, `datetime-wrapper.html.twig`, `field-multiple-value-form.html.twig` | `templates/forms/` | Remaining form element overrides |
| `node.html.twig` | `templates/node/` | Minimal article wrapper |
| `menu--main.html.twig` | `templates/menu/` | Horizontal menu with collapsible sub-items |
| `menu--account.html.twig` | `templates/menu/` | Renders each item as a button |
| `menu--footer.html.twig` | `templates/menu/` | Delegates to `footer` component (centered) |
| `views-mini-pager.html.twig` | `templates/views/` | Delegates to `pagination` component |

**Variant names are DaisyUI 5 names.** `lift` and `border`, not the DaisyUI 4 `lifted` and `bordered`; `tabs.twig` emits `'tabs-' ~ variant`, so `lifted` would produce `tabs-lifted`, a class DaisyUI 5 does not define -- unstyled tabs, no error. `tabs.component.yml` declares only `default|border|lift|box`, so the UI Patterns form rejects the old names too. The same applies to `form-control`, which DaisyUI 5 removed and this theme never emits.

## Template Delegation Pattern

The theme consistently delegates Drupal template rendering to SDC components using `include()`:

```twig
{# breadcrumb.html.twig #}
{% if breadcrumb %}
  {{ include('ui_suite_daisyui:breadcrumbs', {
    items: breadcrumb,
  }, with_context: false) }}
{% endif %}
```

This pattern:
1. Tests for data availability
2. Calls the SDC component by its full name (`theme_name:component_name`)
3. Passes only the needed variables
4. Uses `with_context: false` to prevent variable leakage

## Status Message Mapping

The `status-messages.html.twig` template maps Drupal message types to DaisyUI alert variants:

| Drupal Type | DaisyUI Variant |
|---|---|
| `status` | `info` |
| `warning` | `warning` |
| `error` | `error` |

## Common Mistakes

- **Overriding templates without the component delegation** -- If you override `breadcrumb.html.twig` with raw HTML instead of using the `breadcrumbs` component, you lose the DaisyUI styling and UI Patterns integration. WHY: The components are the styling mechanism; templates are just the bridge.
- **Not using `with_context: false`** -- Omitting this on `include()` allows all parent template variables to leak into the component scope, which can cause naming collisions. WHY: Components may have props with the same names as Drupal template variables.

## See Also

- `drupal-twig-theming.md` -- Drupal Twig template override patterns
