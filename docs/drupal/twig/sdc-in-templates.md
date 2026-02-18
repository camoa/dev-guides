---
topic: drupal/twig
guide: sdc-in-templates
---

## SDC in Templates

### When to Use
When including or rendering Single Directory Components from Twig templates, or when a component needs to embed another SDC component.

### Decision
| Scenario | Approach |
|---|---|
| Include SDC from any template | `{% include 'themename:component-name' %}` |
| Embed SDC with slot content | `{% embed 'themename:component-name' %}{% block slot %}...{% endembed %}` |
| Render SDC via render array | `['#type' => 'component', '#component' => 'theme:name', '#props' => [...]]` |
| Nest SDC inside another SDC | `{% include 'theme:child-component' with props %}` |

### Pattern

**Basic SDC include:**
```twig
{# theme_name:component-name maps to themes/custom/theme_name/components/component-name/ #}
{% include 'mytheme:hero-banner' with {
  title: node.label,
  subtitle: node.field_subtitle.value,
  image: content.field_hero_image,
} only %}
```

**SDC with slots (embed pattern):**
```twig
{% embed 'mytheme:card' with {
  title: node.label,
  url: url,
} %}
  {% block card_body %}
    {{ content.field_summary }}
  {% endblock %}
{% endembed %}
```

**SDC rendering from preprocess (render array approach):**
```php
// In preprocess — preferred for full cache metadata support
$variables['hero'] = [
  '#type' => 'component',
  '#component' => 'mytheme:hero-banner',
  '#props' => [
    'title' => $node->label(),
    'variant' => 'full-width',
  ],
  '#slots' => [
    'body' => $node->body->view('full'),
  ],
];
```

**SDC component namespace format:** `{theme_or_module}:{component-name}`
- Theme components: `mytheme:card`, `radix:button`
- Module components: `mymodule:notification`
- Component names use hyphens matching the directory name

### Common Mistakes
- Using `@` prefix for SDC namespaces (`@mytheme/card`) — SDC uses colon syntax (`mytheme:card`); `@` is the Components module style
- Forgetting `only` keyword → parent template context bleeds into component, causing unexpected variable availability
- Passing a render array as a prop when a string is expected → validate props schema
- Including an SDC that doesn't exist → Twig throws a template not found error; check component directory name matches

### See Also
- SDC Development Guide for full SDC authoring details
- Radix SDC Mapping Guide for Radix-specific components
