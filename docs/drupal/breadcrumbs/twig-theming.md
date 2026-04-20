---
description: Override breadcrumb.html.twig for custom markup — accessibility requirements, aria-current, and template discovery
tldr: "Override the default breadcrumb template when you need custom markup: different HTML structure, additional CSS classes, aria attributes, or schema microdata. The template override requires no PHP — just create the file in the right place."
drupal_version: "11.x"
---

# Twig Theming

## When to Use

> Override the default breadcrumb template when you need custom markup: different HTML structure, additional CSS classes, aria attributes, or schema microdata. The template override requires no PHP — just create the file in the right place.

## Decision

| Need | Approach |
|---|---|
| Minor class additions | Override `breadcrumb.html.twig` in your sub-theme's `templates/navigation/` |
| Full markup control | Override `breadcrumb.html.twig` |
| UI Suite DaisyUI theme | Use the theme's `breadcrumb.html.twig` which delegates to `ui_suite_daisyui:breadcrumbs` SDC |
| Dynamic per-page theming | Use `hook_preprocess_breadcrumb()` in your `.theme` file |

## Pattern

Drupal finds `breadcrumb.html.twig` via `#theme => 'breadcrumb'` set in `Breadcrumb::toRenderable()`. Place in `templates/navigation/` or `templates/` in your theme. Sub-theme takes precedence over base theme.

**Available Twig variables:**
- `breadcrumb` — array of items, each with `text` (string) and `url` (string, empty for current page)
- `attributes` — wrapper HTML attributes object

**Accessible override with `aria-current`** (recommended):
```twig
{% if breadcrumb %}
  <nav aria-label="{{ 'Breadcrumb'|t }}" class="breadcrumb">
    <ol class="breadcrumb-list">
    {% for item in breadcrumb %}
      <li class="breadcrumb-item">
        {% if item.url %}
          <a href="{{ item.url }}" class="breadcrumb-link">{{ item.text }}</a>
        {% else %}
          <span aria-current="page">{{ item.text }}</span>
        {% endif %}
      </li>
    {% endfor %}
    </ol>
  </nav>
{% endif %}
```

**Accessibility requirements:**
1. Keep `role="navigation"` or use `<nav>` (equivalent)
2. Add `aria-label="Breadcrumb"` or `aria-labelledby` referencing a visually-hidden heading
3. Use `<ol>` — breadcrumbs are an ordered sequence (`<ul>` is semantically incorrect)
4. Add `aria-current="page"` on the last item — core's default template does not include this
5. Use CSS `::before` pseudo-elements for separators (`/` or `>`) — DOM text separators are read aloud by screen readers

## Common Mistakes

- **Wrong**: Adding separators as DOM text nodes (` / `) → **Right**: Use CSS `li + li::before { content: '/'; }` — screen readers skip pseudo-elements
- **Wrong**: Omitting `aria-current="page"` on the current page item → **Right**: Required by WCAG 2.1 SC 2.4.8 for location awareness
- **Wrong**: Using `<ul>` instead of `<ol>` → **Right**: Breadcrumbs are an ordered sequence; `<ol>` is semantically correct
- **Wrong**: Placing the template in `templates/system/` expecting it to work → **Right**: `templates/system/breadcrumb.html.twig` also works (Drupal checks multiple template paths)

## See Also

- [UI Suite DaisyUI Integration](ui-suite-daisyui-integration.md)
- Reference: `core/modules/system/templates/breadcrumb.html.twig`
- Reference: `core/lib/Drupal/Core/Breadcrumb/BreadcrumbPreprocess.php`
- ARIA pattern: https://www.w3.org/WAI/ARIA/apg/patterns/breadcrumb/
