---
description: Override breadcrumb.html.twig for custom markup — accessibility requirements, aria-current, and template discovery
tldr: "Override the default breadcrumb template when you need custom markup: different HTML structure, additional CSS classes, aria attributes, or schema microdata. The template override requires no PHP — just create the file in the right place."
drupal_version: "11.x"
---

# Twig Theming

## When to Use

> Override the default breadcrumb template when you need custom markup: different HTML structure, additional CSS classes, aria attributes, schema microdata attributes, or DaisyUI-specific classes.

## Decision

| Need | Approach |
|---|---|
| Minor class additions | Override `breadcrumb.html.twig` in your sub-theme's `templates/navigation/` |
| Full markup control | Override `breadcrumb.html.twig` |
| UI Suite DaisyUI theme | Use the theme's `breadcrumb.html.twig` which delegates to `ui_suite_daisyui:breadcrumbs` SDC |
| Dynamic per-page theming | Use `preprocess_breadcrumb` in your `.theme` file |

## Pattern

The `BreadcrumbPreprocess::preprocessBreadcrumb()` method converts `Link` objects into a Twig-friendly array:

```php
// Result in Twig: $breadcrumb[] = ['text' => 'Link Label', 'url' => '/path']
// The last item intentionally has no url when it's the current page (plain text)
```

**Core `breadcrumb.html.twig`:**
```twig
{% if breadcrumb %}
  <nav role="navigation" aria-labelledby="system-breadcrumb">
    <h2 id="system-breadcrumb" class="visually-hidden">{{ 'Breadcrumb'|t }}</h2>
    <ol>
    {% for item in breadcrumb %}
      <li>
        {% if item.url %}
          <a href="{{ item.url }}">{{ item.text }}</a>
        {% else %}
          {{ item.text }}
        {% endif %}
      </li>
    {% endfor %}
    </ol>
  </nav>
{% endif %}
```

**Available Twig variables:**
- `breadcrumb` — array of items, each with `text` (string) and `url` (string, empty for current page)
- `attributes` — wrapper HTML attributes object

**Accessible overriding — key requirements:**
1. Keep `role="navigation"` on the wrapping element
2. Keep `aria-labelledby` referencing a visually-hidden heading (or use `aria-label="Breadcrumb"` directly on `<nav>`)
3. Use `<ol>` (ordered list) — breadcrumbs are an ordered sequence
4. Add `aria-current="page"` on the last item (the current page) — core's template does not do this; you must add it in your override
5. Use a separator via CSS (`::before` on `li+li`) rather than DOM content — screen readers skip visual separators

**Recommended override with `aria-current`:**
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

**Template discovery path:** Drupal looks for `breadcrumb.html.twig` in `templates/navigation/` or `templates/` within the active theme (sub-theme first, then base theme). No suggestion hook is needed — Drupal finds `breadcrumb.html.twig` by the `#theme => 'breadcrumb'` render element key set in `Breadcrumb::toRenderable()`.

## Common Mistakes

- Putting separators (` / ` or `>`) as DOM text nodes — screen readers read them aloud; use CSS `::before` pseudo-elements instead
- Skipping `aria-current="page"` on the current page item — this is required by WCAG 2.1 success criterion 2.4.8 for location awareness
- Using `<ul>` instead of `<ol>` — breadcrumbs are ordered; `<ol>` is semantically correct
- Placing the template in the wrong directory — `templates/system/breadcrumb.html.twig` also works (Drupal checks multiple template paths)

## See Also

- UI Suite DaisyUI template → [UI Suite DaisyUI Integration](ui-suite-daisyui-integration.md)
- Reference: `core/modules/system/templates/breadcrumb.html.twig`
- Reference: `core/lib/Drupal/Core/Breadcrumb/BreadcrumbPreprocess.php`
- ARIA pattern: https://www.w3.org/WAI/ARIA/apg/patterns/breadcrumb/
