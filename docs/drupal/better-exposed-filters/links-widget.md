---
description: BEF links widget — clickable filter links with AJAX support, toggle behavior, and template variables
tldr: "Use this widget when you want filters rendered as clickable links instead of form elements — useful for faceted navigation style where each option is a URL. Use checkboxes when form-based interaction (submit button) is preferred."
drupal_version: "11.x"
---

# Links Widget

## When to Use

> Use this widget when you want filters rendered as clickable links instead of form elements — useful for faceted navigation style where each option is a URL. Use checkboxes when form-based interaction (submit button) is preferred.

## Decision

| Property | Value |
|---|---|
| Plugin ID | `bef_links` |
| Class | `Drupal\better_exposed_filters\Plugin\better_exposed_filters\filter\Links` |
| Template | `bef-links.html.twig` |

**Applicable filter types:** Any filter with `#options` — `InOperator`, `StringFilter` (in/or/and/not), `BooleanOperator`, `TaxonomyIndexTid` (select), grouped filters, `SearchApiFulltext`, `FacetsFilter`

| Option | Config Key | Default | Purpose |
|---|---|---|---|
| Select all/none | `select_all_none` | FALSE | Add select all/none links (requires "Allow multiple selections") |
| Soft limit | `soft_limit` | 0 | Truncate to N items |

## Pattern

```php
// AJAX detection — BEF adds class and library automatically
if ($filter->view->ajaxEnabled()) {
    $form[$field_id]['#attributes']['class'][] = 'bef-links-use-ajax';
    $form['#attached']['library'][] = 'better_exposed_filters/links_use_ajax';
}

// Each link has:
// #attributes.class = ['bef-link'] + ['bef-link--selected'] when active
// #url = Url object with query parameters for that filter state
```

**Template variables (`bef-links`):**

| Variable | Type | Description |
|---|---|---|
| `links` | array | Array of link render elements with `#url`, `#title`, `#attributes` |
| `selected` | array | Currently selected values |
| `hiddens` | array | Hidden input elements for form submission |
| `is_nested` | bool | Hierarchical rendering |

**Exposed form as block:** BEF uses `#bef_path` to ensure links point to the correct View page when the exposed form is a block.

## Common Mistakes

- **Wrong**: Expecting links to work via AJAX without Views AJAX enabled → **Right**: Without AJAX, links cause a full page reload. Enable AJAX on the View for smooth filtering.
- **Wrong**: Not accounting for the View path when form is a block → **Right**: BEF handles the URL via `#bef_path`. Verify the View's page path is correct.
- **Wrong**: Expecting one click to set multiple values at once → **Right**: Each click toggles one option. The URL accumulates query parameters for multi-value selections.

## See Also

- [JavaScript Behaviors](javascript-behaviors.md)
- [Auto-Submit](auto-submit.md)
- Reference: `web/modules/contrib/better_exposed_filters/src/Plugin/better_exposed_filters/filter/Links.php`
