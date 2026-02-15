---
description: Leverage Twig template inheritance (extends, block, parent, include, embed) to reuse markup structure and avoid template duplication.
---

# Twig Template Inheritance

## When to Use

When you need to override theme templates but want to reuse most of the structure, changing only specific sections.

## Twig Inheritance Mechanisms

| Technique | Syntax | Use When |
|-----------|--------|----------|
| **Extends** | `{% extends "parent.html.twig" %}` | Inherit entire template, override specific blocks |
| **Block** | `{% block blockname %}...{% endblock %}` | Define replaceable sections in base template |
| **Parent** | `{{ parent() }}` | Include parent block content in child override |
| **Include** | `{% include "snippet.html.twig" %}` | Embed reusable template snippet |
| **Embed** | `{% embed "base.html.twig" %}...{% endembed %}` | Include template with block overrides inline |

## Decision

| If you need... | Use... | Why |
|---|---|---|
| Override one section of template | `{% extends %}` + `{% block %}` | Reuse structure, change specific parts |
| Add to parent block content | `{{ parent() }}` inside block | Preserve parent content, add yours |
| Same snippet in multiple templates | `{% include %}` | DRY for shared markup (headers, footers) |
| Theme suggestions | Template naming convention | Drupal auto-discovers more specific templates |
| Cross-theme inheritance | `{% extends "@themename/template.html.twig" %}` | Reuse templates from base theme or module |

## Pattern

```twig
{# mytheme/templates/layout/page.html.twig #}
{# Extends base theme template #}
{% extends "@classy/layout/page.html.twig" %}

{# Override only the content block #}
{% block content %}
  <div class="custom-wrapper">
    {{ parent() }}  {# Include parent block content #}
  </div>
{% endblock %}

{# Override sidebar #}
{% block sidebar %}
  <aside class="custom-sidebar">
    {% include "@mytheme/partials/custom-sidebar.html.twig" %}
  </aside>
{% endblock %}
```

Reference: `core/themes/stable9/templates/`, `core/modules/system/templates/`

## Theme Suggestions for DRY

Drupal's theme suggestion system allows specific template overrides without duplication:

```
node.html.twig                          (base, generic)
node--article.html.twig                 (bundle-specific)
node--article--teaser.html.twig         (bundle + view mode)
node--123.html.twig                     (specific node ID)
```

Each more specific template can extend the more generic one:

```twig
{# node--article.html.twig #}
{% extends "node.html.twig" %}

{% block content %}
  <div class="article-specific">
    {{ parent() }}
  </div>
{% endblock %}
```

## Common Mistakes

- **Extending contrib template without considering updates** — If contrib template changes, your extension may break; prefer copying and customizing over extending
- **Not using {{ parent() }} when needed** — If you want to add to parent content, not replace it, use `{{ parent() }}`
- **Duplicating entire templates for small changes** — Use `{% extends %}` and override only the changed blocks
- **Forgetting block names** — Parent and child blocks must have matching names
- **Complex logic in templates** — Move logic to preprocess functions; templates should be presentational

## See Also

- [Plugin Reuse Patterns](plugin-reuse.md)
- [SDC Component Reuse](sdc-component-reuse.md)
- Reference: [Extending templates | Drupal.org](https://www.drupal.org/docs/develop/theming-drupal/twig-in-drupal/extending-templates)
- Reference: [Twig Template Inheritance | Drupalize.Me](https://drupalize.me/tutorial/twig-template-inheritance)
