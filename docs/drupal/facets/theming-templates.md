---
description: Facets theming and templates — available templates, template variables, template suggestions by widget/facet, and HTML structure
tldr: "Use this guide when customizing the HTML output of facets in your theme."
drupal_version: "11.x"
---

# Theming & Templates

## When to Use

> Use this guide when customizing the HTML output of facets in your theme.

## Decision

**Available templates:**

| Template | Theme Hook | Purpose |
|---|---|---|
| `facets-item-list.html.twig` | `facets_item_list` | Container for facet items |
| `facets-result-item.html.twig` | `facets_result_item` | Individual result item |
| `facets-views-plugin.html.twig` | `facets_views_plugin` | Views integration wrapper |

**Template variables — `facets-item-list`:**

| Variable | Type | Description |
|---|---|---|
| `facet` | FacetInterface | The facet entity |
| `items` | array | Rendered result items |
| `title` | string | Facet label |
| `list_type` | string | 'ul' or 'ol' |
| `attributes` | Attribute | HTML attributes |
| `wrapper_attributes` | Attribute | Wrapper HTML attributes |
| `context` | array | `['list_style' => 'links|checkbox|dropdown']` |

**Template variables — `facets-result-item`:**

| Variable | Type | Description |
|---|---|---|
| `value` | string | Display text |
| `raw_value` | string | Backend value |
| `show_count` | bool | Whether to show count |
| `count` | int | Result count |
| `is_active` | bool | Currently selected |
| `facet` | FacetInterface | Parent facet entity |

## Pattern

**Template suggestions** (most specific to least specific):

```
facets-result-item--links--category.html.twig
facets-result-item--links.html.twig
facets-result-item.html.twig

facets-item-list--links--category.html.twig
facets-item-list--links.html.twig
facets-item-list--checkbox.html.twig
facets-item-list.html.twig
```

**HTML structure of result items:**

```html
<!-- Active item -->
<li class="facet-item is-active">
  <a href="?f[0]=color:blue">
    <span class="facet-item__status js-facet-deactivate">(-)</span>
    <span class="facet-item__value">Blue</span>
    <span class="facet-item__count">(42)</span>
  </a>
</li>

<!-- Inactive item -->
<li class="facet-item">
  <a href="?f[0]=color:red">
    <span class="facet-item__value">Red</span>
    <span class="facet-item__count">(18)</span>
  </a>
</li>
```

`facets_preprocess_block()` adds the widget type as a CSS class: `block-facet--links`, `block-facet--checkbox`, etc.

## Common Mistakes

- **Wrong**: Using a generic `facets_result_item` override when you only need to change one widget → **Right**: Use widget-specific suggestions (`facets-result-item--links.html.twig`) to avoid affecting all widgets.
- **Wrong**: Removing JavaScript-targeting CSS classes in template overrides → **Right**: Widget JS relies on `js-facet-deactivate` and similar classes. Preserve these when overriding templates.

## See Also

- [Widgets](widgets.md) — widget types and their CSS classes
- [Caching](caching.md) — cache debug output in templates
- Reference: `web/modules/contrib/facets/templates/`
