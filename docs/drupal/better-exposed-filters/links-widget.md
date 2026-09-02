---
description: "BEF links widget — clickable filter links with AJAX support, toggle behavior, and template variables"
tldr: "Use this widget when you want filters rendered as clickable links instead of form elements — useful for faceted navigation style where each option is a URL."
drupal_version: "11.x"
---

# Links Widget

## When to Use

> When you want filters rendered as clickable links instead of form elements — useful for faceted navigation style where each option is a URL.

## Decision: Plugin Details

| Property | Value |
|---|---|
| Plugin ID | `bef_links` |
| Class | `Drupal\better_exposed_filters\Plugin\better_exposed_filters\filter\Links` |
| Attribute | `#[FiltersWidget(id: 'bef_links', title: 'Links')]` |
| Template | `bef-links.html.twig` |

## Decision: Applicability

Same as the base `FilterWidgetBase::isApplicable()` — works with any filter that has `#options` (InOperator, StringFilter with in/or/and/not, BooleanOperator, TaxonomyIndexTid select, grouped filters, SearchApiFulltext, FacetsFilter).

## Decision: Widget-Specific Configuration

| Option | Config Key | Default | Purpose |
|---|---|---|---|
| Select all/none | `select_all_none` | FALSE | Add select all/none links (requires "Allow multiple selections") |
| Soft limit | `soft_limit` | 0 | Truncate to N items |
| Show less label | `soft_limit_label_less` | 'Show less' | Custom collapse text |
| Show more label | `soft_limit_label_more` | 'Show more' | Custom expand text |

## Pattern: How Links Work

Each option generates a `#type => 'link'` element with a URL containing the filter value as a query parameter. Clicking a link navigates to that URL (or triggers AJAX if the View uses AJAX).

**Toggle behavior:** Clicking an active link removes that filter value (toggles off). Clicking an inactive link adds the filter value.

**AJAX support:** When the View has AJAX enabled, BEF adds `bef-links-use-ajax` class and attaches the `links_use_ajax` library to intercept clicks and submit via AJAX.

```php
if ($filter->view->ajaxEnabled() || $filter->view->display_handler->ajaxEnabled()) {
    $form[$field_id]['#attributes']['class'][] = 'bef-links-use-ajax';
    $form['#attached']['library'][] = 'better_exposed_filters/links_use_ajax';
}
```

## Pattern: Template Variables (bef-links)

| Variable | Type | Description |
|---|---|---|
| `element` | array | The form element |
| `links` | array | Array of link render elements with #url, #title, #attributes |
| `children` | array | Child element keys |
| `selected` | array | Currently selected values |
| `hiddens` | array | Hidden input elements for form submission |
| `is_nested` | bool | Hierarchical rendering |

Each link has:
- `#attributes.class` — includes `bef-link`, plus `bef-link--selected` when active
- `#url` — Url object with query parameters for that filter state

## Pattern: Exposed Form as Block

When the exposed form is displayed as a block (on a different page), BEF uses `#bef_path` to ensure links point to the correct View page:
```php
$form[$field_id]['#bef_path'] = $this->getExposedFormActionUrl($form_state);
```

## Common Mistakes

- **Links not working without AJAX** — Without AJAX, links cause a full page reload. This is by design but can be unexpected.
- **Links on wrong page** — If the exposed form is a block, ensure the View's path is accessible. BEF handles the URL via `#bef_path`.
- **Links with multiple selections** — For multi-value link filters, each click toggles one option. The URL accumulates query parameters.

## See Also

- [JavaScript Behaviors](javascript-behaviors.md) — bef_links_use_ajax.js
- [Auto-Submit](auto-submit.md) — auto-submit interaction with links
