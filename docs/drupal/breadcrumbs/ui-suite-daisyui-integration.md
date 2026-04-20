---
description: Use the UI Suite DaisyUI breadcrumbs SDC component — template bridge, item mapping, direct SDC usage, and accessibility notes
tldr: "When your theme extends `ui_suite_daisyui`, the theme's `breadcrumb.html.twig` delegates to the `ui_suite_daisyui:breadcrumbs` SDC automatically. You get DaisyUI breadcrumb styling with no extra code."
drupal_version: "11.x"
---

# UI Suite DaisyUI Integration

## When to Use

> When your theme extends `ui_suite_daisyui`, the theme's `breadcrumb.html.twig` delegates to the `ui_suite_daisyui:breadcrumbs` SDC automatically. You get DaisyUI breadcrumb styling with no extra code. Customize by overriding the template in your sub-theme.

## Decision

| Need | Approach |
|---|---|
| Default DaisyUI breadcrumb styling | Extend `ui_suite_daisyui` — the template bridge works automatically |
| Add `max_width` constraint | Override `breadcrumb.html.twig` and pass `max_width: true` prop to the SDC |
| Use SDC directly in a block/component | Use `include('ui_suite_daisyui:breadcrumbs', { items: [...] })` with `title` + `url` keys |
| WCAG-compliant breadcrumb | Override sub-theme template; wrap SDC output in `<nav aria-label="{{ 'Breadcrumb'|t }}">` |

## Pattern

**Theme's `breadcrumb.html.twig`** (the bridge):
```twig
{% if breadcrumb %}
  {{ include('ui_suite_daisyui:breadcrumbs', {
    items: breadcrumb,
  }, with_context: false) }}
{% endif %}
```

**SDC component props:**
```yaml
# components/breadcrumbs/breadcrumbs.component.yml
props:
  items:
    $ref: "ui-patterns://links"   # each item: title + url
  max_width:
    type: boolean                  # adds max-w-xs class (scrollable for long trails)
```

**Important:** The core breadcrumb preprocessor outputs `item.text`, but the SDC template reads `item.title`. The theme's bridge template passes the raw `breadcrumb` array directly — this works because UI Suite DaisyUI's template maps between the two. When using the SDC directly outside the bridge template, use `title` not `text`:

```twig
{{ include('ui_suite_daisyui:breadcrumbs', {
  items: [
    { title: 'Home', url: '/' },
    { title: 'Products', url: '/products' },
    { title: 'Widget A' },
  ],
  max_width: false,
}) }}
```

**Sub-theme override** to add props:
```twig
{% if breadcrumb %}
  {{ include('ui_suite_daisyui:breadcrumbs', {
    items: breadcrumb,
    max_width: false,
  }, with_context: false) }}
{% endif %}
```

## Common Mistakes

- **Wrong**: Passing `text` instead of `title` when using the SDC directly → **Right**: The SDC template reads `item.title`; `item.text` produces no output
- **Wrong**: Setting `max_width: true` without realizing it adds `max-w-xs` (20rem) → **Right**: This makes the breadcrumb scroll horizontally; useful for very long trails, confusing otherwise
- **Wrong**: Assuming DaisyUI's breadcrumb component provides `<nav>` for accessibility → **Right**: The SDC uses `<div>` + `<ul>`; wrap in `<nav aria-label="{{ 'Breadcrumb'|t }}">` if WCAG compliance is required

## See Also

- [Twig Theming](twig-theming.md)
- [Block Placement](block-placement.md)
- Reference: `themes/contrib/ui_suite_daisyui/components/breadcrumbs/breadcrumbs.component.yml`
- Reference: `themes/contrib/ui_suite_daisyui/components/breadcrumbs/breadcrumbs.twig`
- Reference: `themes/contrib/ui_suite_daisyui/templates/system/breadcrumb.html.twig`
