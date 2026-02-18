---
topic: drupal/twig
guide: anti-patterns
---

## Anti-Patterns & Common Mistakes

### When to Use
Code review checklist. Review your templates against these patterns before committing.

### Anti-Patterns

**1. Logic in templates**
Twig templates are presentation layer. Business logic belongs in PHP.
```twig
{# WRONG — calculating in template #}
{% set words = node.field_body.value|split(' ')|length %}
{% set minutes = (words / 200)|round %}
Reading time: {{ minutes }} minutes

{# RIGHT — calculate in preprocess #}
Reading time: {{ reading_time }} minutes
```

**2. Accessing `content` array like it's field objects**
```twig
{# WRONG — content is a render array, not field objects #}
{% if content.field_tags.value %}
{% for tag in content.field_tags %}

{# RIGHT — use node object for raw access, content for rendering #}
{% if node.field_tags is not empty %}
{{ content.field_tags }}
```

**3. Not using `|without()` — double-rendering fields**
```twig
{# WRONG — field_image renders twice #}
<div class="hero">{{ content.field_image }}</div>
{{ content }}  {# field_image renders again here #}

{# RIGHT — exclude from catch-all #}
<div class="hero">{{ content.field_image }}</div>
{{ content|without('field_image') }}
```

**4. Hard-coded paths to theme assets**
```twig
{# WRONG — breaks when theme moves, no cache busting #}
<img src="/themes/custom/mytheme/images/logo.svg">

{# RIGHT — use library system or active_theme_path() sparingly #}
{{ attach_library('mytheme/header') }}
{# Or in preprocess: #}
{# $variables['logo_url'] = $theme_path . '/images/logo.svg'; #}
```

**5. Bypassing field formatters for display**
```twig
{# WRONG — bypasses formatters, breaks field display config, no cache metadata #}
<p>{{ node.field_body.value|raw }}</p>

{# RIGHT — respects display config, formatters, text filters #}
{{ content.field_body }}
```

**6. PHP-in-Twig patterns (twig_tweak `|php` filter)**
```twig
{# WRONG — arbitrary PHP in templates is a security nightmare #}
{{ 'SomeClass::method()'|php }}

{# RIGHT — use preprocess functions or proper Twig extensions #}
{{ my_preprocess_variable }}
```

**7. Not checking for empty entity references before traversal**
```twig
{# WRONG — crashes if field is empty #}
<img src="{{ file_url(node.field_image.entity.fileUri) }}">

{# RIGHT — guard against empty fields #}
{% if node.field_image.entity %}
  <img src="{{ file_url(node.field_image.entity.fileUri) }}">
{% endif %}
```

**8. Using template preprocess for data that belongs in field formatters**
If you're rewriting how a field renders in preprocess + template, consider: should this be a custom field formatter instead? Formatters are reusable, configurable in the UI, and cacheable properly.

**9. Modifying render arrays destructively in templates**
```twig
{# WRONG — `without` takes the name as a string argument, not like this #}
{% set custom_content = content %}
{% unset custom_content.field_image %}  {# This doesn't work in Twig #}

{# RIGHT #}
{{ content|without('field_image') }}
```

### See Also
- Security → [Security & Performance](security-performance.md)
- Correct field access → [Accessing Field Values](accessing-field-values.md)
