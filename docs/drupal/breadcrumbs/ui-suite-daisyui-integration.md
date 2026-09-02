---
description: Use the UI Suite DaisyUI breadcrumbs SDC component — template bridge, item mapping, direct SDC usage, and accessibility notes
tldr: "When your theme extends `ui_suite_daisyui`, the theme's `breadcrumb.html.twig` delegates to the `ui_suite_daisyui:breadcrumbs` SDC automatically. You get DaisyUI breadcrumb styling with no extra code."
drupal_version: "11.x"
---

# UI Suite DaisyUI Integration

## When to Use

> When your theme extends `ui_suite_daisyui`, the `breadcrumbs` SDC component and the theme's `breadcrumb.html.twig` override replace the core template automatically. You get DaisyUI's breadcrumb styling with no extra code. Customize by overriding the template in your sub-theme or passing different props to the SDC.

This section documents UI Suite DaisyUI 5.0.0-alpha6 against Drupal core 11.4.5 and UI Patterns 2.0.19, which the theme declares as a hard dependency in both its `.info.yml` and its `composer.json`.

## Pattern

**Theme's `breadcrumb.html.twig`** (the bridge):
```twig
{% if breadcrumb %}
  {{ include('ui_suite_daisyui:breadcrumbs', {
    items: breadcrumb,
  }, with_context: false) }}
{% endif %}
```

The bridge does no key mapping. It passes the core `breadcrumb` array through unchanged as `items`, and the theme ships no `preprocess_breadcrumb` anywhere. The keys nonetheless line up, and the reason is UI Patterns rather than the theme.

Core's `BreadcrumbPreprocess::preprocessBreadcrumb()` emits `['text' => ..., 'url' => ...]`, while the SDC template renders `item.title`. The `items` prop declares `$ref: "ui-patterns://links"`, so UI Patterns' `LinksPropType::normalizeLink()` runs first and renames `text` to `title`; core's `breadcrumb.html.twig` is named in that method's own docblock as one of the cases it exists for. An item carrying neither key is given its array index as the title.

That normalization is not confined to render arrays. `ModuleNodeVisitorBeforeSdc` injects a `_ui_patterns_normalize_props` call into every compiled component template, ahead of core's own component node visitor, so the rename also happens on a plain Twig `include()` or `embed` of the component. Passing `text` to the SDC directly therefore works. Still declare `title`: it is the prop's documented shape, and it is the only key the normalizer leaves alone.

**`breadcrumbs` SDC component definition:**
```yaml
# components/breadcrumbs/breadcrumbs.component.yml
name: Breadcrumbs
group: Navigation
props:
  type: object
  properties:
    items:
      title: Items
      description: "Each item can contain: title, url."
      $ref: "ui-patterns://links"
    max_width:
      title: Max-width
      description: "Set max-width so the list scrolls horizontally"
      type: boolean
```

**SDC template output:**
```twig
{# breadcrumbs.twig #}
{% if items %}
<div{{ attributes.addClass(['text-sm', 'breadcrumbs', max_width ? 'max-w-xs']) }}>
<ul>
{% for item in items %}
  {% if item.url %}
    <li><a href="{{ item.url }}">{{ item.title }}</a></li>
  {% else %}
    <li>{{ item.title }}</li>
  {% endif %}
{% endfor %}
</ul>
</div>
{% endif %}
```

**Using the SDC directly** (e.g., in a custom component or block template):
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

**Sub-theme override:** Copy `themes/contrib/ui_suite_daisyui/templates/system/breadcrumb.html.twig` to `themes/custom/my_theme/templates/system/breadcrumb.html.twig` and modify the `include()` call to add props:

```twig
{% if breadcrumb %}
  {{ include('ui_suite_daisyui:breadcrumbs', {
    items: breadcrumb,
    max_width: false,
  }, with_context: false) }}
{% endif %}
```

**Accessibility note:** The DaisyUI `breadcrumbs` component uses `<div>` + `<ul>` rather than `<nav>` + `<ol>`. If WCAG compliance is required, override the sub-theme template to wrap the SDC output in a `<nav aria-label="{{ 'Breadcrumb'|t }}">` or replace the SDC include with custom accessible markup.

## Common Mistakes

- Assuming the theme's bridge template is what reconciles `text` with `title` — it passes the array through untouched; `LinksPropType` does the rename, and it only does it for props declared `$ref: "ui-patterns://links"`. `normalizeProps()` skips any prop with no UI Patterns type, so your own component typing `items` as a plain array receives `text` untouched and renders nothing if its template reads `title`
- Setting `max_width: true` without knowing it adds `max-w-xs` (20rem) — this makes the breadcrumb scrollable horizontally, which is a feature for very long trails but confusing if unexpected
- Not adding a `<nav>` wrapper — DaisyUI's breadcrumb component does not include one; screen readers need the landmark region

## See Also

- Core template details → [Twig Theming](twig-theming.md)
- Block placement → [Block Placement](block-placement.md)
- Reference: `themes/contrib/ui_suite_daisyui/components/breadcrumbs/breadcrumbs.component.yml`
- Reference: `themes/contrib/ui_suite_daisyui/components/breadcrumbs/breadcrumbs.twig`
- Reference: `themes/contrib/ui_suite_daisyui/templates/system/breadcrumb.html.twig`
- Reference: `modules/contrib/ui_patterns/src/Plugin/UiPatterns/PropType/LinksPropType.php` — the `text` → `title` rename
- Reference: `modules/contrib/ui_patterns/src/Template/ModuleNodeVisitorBeforeSdc.php` — where normalization is injected
