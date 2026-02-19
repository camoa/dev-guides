---
description: 22 Drupal template overrides that delegate to DaisyUI SDC components
---

# Template Overrides

## Templates Provided by the Theme

The theme overrides 22 Drupal templates (including system, form, menu, node, and view templates):

| Template | Path | Purpose |
|---|---|---|
| `page.html.twig` | `templates/system/` | Main page layout using navbar + grid components |
| `block.html.twig` | `templates/system/` | Simplified block wrapper |
| `block--system-branding-block.html.twig` | `templates/system/` | Site name as `btn btn-ghost text-xl` |
| `breadcrumb.html.twig` | `templates/system/` | Delegates to `breadcrumbs` component |
| `page-title.html.twig` | `templates/system/` | `text-4xl font-extrabold mb-8 mt-12` |
| `status-messages.html.twig` | `templates/system/` | Maps Drupal message types to alert variants |
| `menu-local-tasks.html.twig` | `templates/system/` | Primary tabs as `lifted`, secondary as `bordered` |
| `menu-local-task.html.twig` | `templates/system/` | Delegates to `tab` component |
| `pager.html.twig` | `templates/system/` | Delegates to `pagination` component |
| `select.html.twig` | `templates/system/` | Adds `select select-bordered` classes |
| `form-element.html.twig` | `templates/system/` | Adds `form-control my-3` and DaisyUI form classes |
| `node.html.twig` | `templates/node/` | Minimal article wrapper |
| `menu--main.html.twig` | `templates/menu/` | Horizontal menu with collapsible sub-items |
| `menu--account.html.twig` | `templates/menu/` | Renders each item as a button |
| `menu--footer.html.twig` | `templates/menu/` | Delegates to `footer` component (centered) |
| `views-mini-pager.html.twig` | `templates/views/` | Delegates to `pagination` component |

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
