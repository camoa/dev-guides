---
topic: drupal/twig
guide: template-inheritance
---

## Template Inheritance & Composition

### When to Use
When you want to share template structure across multiple templates, or include a sub-template/component as part of a larger template.

### Decision
| Twig tag | Use when | Behavior |
|---|---|---|
| `{% extends %}` | Child wants to share parent's HTML structure with overridable blocks | Parent renders; child fills `{% block %}` regions |
| `{% include %}` | Inserting a reusable partial (no content override needed) | Renders partial with passed variables |
| `{% embed %}` | Inserting partial AND overriding its `{% block %}` regions | Like `include` but allows block overrides |
| `{% block %}` | Defining overridable regions within a template | Works with `extends` and `embed` |

### Pattern

**`{% extends %}` — template inheritance:**
```twig
{# base-card.html.twig #}
<div class="card">
  {% block header %}{% endblock %}
  <div class="card__body">
    {% block body %}{% endblock %}
  </div>
</div>

{# article-card.html.twig — extends the base #}
{% extends 'themes/custom/mytheme/templates/partials/base-card.html.twig' %}
{% block header %}
  <h2 class="card__title">{{ title }}</h2>
{% endblock %}
{% block body %}
  {{ summary }}
{% endblock %}
```

**`{% include %}` — simple partials:**
```twig
{# Include a sub-template; all parent variables available unless 'only' used #}
{% include 'themes/custom/mytheme/templates/partials/social-links.html.twig' %}

{# Pass specific variables only #}
{% include 'themes/custom/mytheme/templates/partials/author.html.twig' with {
  name: author_name,
  picture: author_picture,
} only %}
```

**`{% embed %}` — include with block overrides:**
```twig
{# Embed allows overriding blocks defined in the included template #}
{% embed 'themes/custom/mytheme/templates/partials/card.html.twig' with {title: node.label} %}
  {% block card_image %}
    {{ content.field_thumbnail }}
  {% endblock %}
  {% block card_footer %}
    <a href="{{ url }}">{{ 'Read more'|t }}</a>
  {% endblock %}
{% endembed %}
```

**Drupal block template `{% block content %}`:**
```twig
{# In block.html.twig, content is wrapped in a block #}
{% block content %}
  {{ content }}
{% endblock %}
{# Sub-templates that extend block.html.twig can override this block #}
```

### Common Mistakes
- Using `{% extends %}` when you just need `{% include %}` — extends requires a parent-child relationship; include is a simple embed
- `{% include %}` without `only` → parent context bleeds in; always use `only` when passing explicit variables to prevent surprises
- `{% embed %}` without defining blocks in the included template → nothing to override; embed requires the included template to have `{% block %}` tags
- Forgetting that `{% extends %}` must be the FIRST tag in a template (no content or other tags before it)
- Using extends across too many levels → debugging becomes difficult; prefer shallow hierarchies

### See Also
- SDC includes → [SDC in Templates](sdc-in-templates.md)
