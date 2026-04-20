---
tldr: "When you need to generate URLs, attach libraries, create links, or use other Drupal-specific functions from within a Twig template."
topic: drupal/twig
guide: twig-functions
---

## Drupal Twig Functions

### When to Use
When you need to generate URLs, attach libraries, create links, or use other Drupal-specific functions from within a Twig template.

### Items

#### `url(route_name, parameters, options)`
**Description:** Generates an absolute URL. Returns a render array with bubbled cache metadata.
**Usage:**
```twig
{{ url('entity.node.canonical', {node: node.id()}) }}
{{ url('<front>') }}
```
**Gotchas:** Returns a `GeneratedUrl` object, not a plain string. For string-safe use, prefer `path()`.

#### `path(route_name, parameters, options)`
**Description:** Generates a relative path (no scheme/host).
**Usage:**
```twig
<a href="{{ path('entity.user.canonical', {user: user.id()}) }}">Profile</a>
```
**Gotchas:** Safe for HTML context when parameters are simple (one constant param). Multiple parameters may need escaping.

#### `link(text, url, attributes)`
**Description:** Returns a render array for an `<a>` element. Preferred over manual `<a href>` for internal links.
**Usage:**
```twig
{{ link('Read more'|t, url) }}
{{ link(node.label, 'internal:/node/' ~ node.id(), {'class': ['read-more']}) }}
```
**Gotchas:** `url` can be a string URI or a `Url` object. Text can be a translated string or markup.

#### `file_url(uri)`
**Description:** Converts a `public://...` file URI to a web-accessible URL.
**Usage:**
```twig
<img src="{{ file_url(node.field_image.entity.fileUri) }}" alt="{{ node.field_image.alt }}">
```
**Gotchas:** Input must be a URI (`public://`, `private://`, `base:`). Passing a path instead of URI returns wrong URL.

#### `attach_library(library)`
**Description:** Attaches a CSS/JS library to the response from within a template.
**Usage:**
```twig
{{ attach_library('mytheme/my-component') }}
{{ attach_library('core/drupal.dialog') }}
```
**Gotchas:** Returns empty string (nothing to print). Use `{{ attach_library(...) }}` not `{% set x = attach_library(...) %}`. Prefer attaching in preprocess or `#attached` for performance.

#### `active_theme()`
**Description:** Returns the machine name of the active theme.
**Usage:**
```twig
{% if active_theme() == 'mytheme' %}...{% endif %}
```

#### `active_theme_path()`
**Description:** Returns the path to the active theme.
**Usage:**
```twig
<img src="{{ active_theme_path() }}/images/logo.svg">
```
**Gotchas:** Avoid hard-coded asset paths this way — use `#attached` libraries instead.

#### `create_attribute(attributes)`
**Description:** Creates a new `Attribute` object for use in templates.
**Usage:**
```twig
{% set wrapper_attrs = create_attribute({'class': ['my-wrapper'], 'data-type': node.bundle}) %}
<div{{ wrapper_attrs }}>
```

#### `render_var(variable)`
**Description:** Renders a render array to a string. Rarely needed directly — Twig's print already calls it.
**Usage:**
```twig
{% set rendered = render_var(content.field_body) %}
{% if rendered|trim is not empty %}
  {{ rendered }}
{% endif %}
```

#### `icon(pack_id, icon_id, settings)`
**Description:** Returns a render array for the Icon API (Drupal 11+). Renders an icon from a registered icon pack.
**Usage:**
```twig
{{ icon('material_symbols', 'arrow_forward') }}
{{ icon('my_icons', 'search', {size: 24}) }}
```
**Gotchas:** Both `pack_id` and `icon_id` are required — returns empty array if either is missing. Requires an icon pack module to be installed. New in Drupal 11.

#### `dump(variable)`
**Description:** Debug-dumps a variable using Symfony VarDumper. With no arguments, dumps the entire Twig context.
**Usage:**
```twig
{{ dump() }}         {# Dumps ALL available variables #}
{{ dump(content) }}  {# Dumps specific variable #}
```
**Gotchas:** Only works when Twig debug mode is enabled (`debug: true` in `services.yml`). Remove before production. Different from twig_tweak's `drupal_dump` which uses Devel.

### Common Mistakes
- Using `{{ path() }}` without checking if parameters are safe → multiple variable params need extra care
- Using `{{ active_theme_path() }}` for referencing images/assets → wrong approach; use `#attached` libraries or `file_url()` with the file URI
- Calling `{{ file_url(node.field_image.entity.fileUri) }}` without checking if entity exists → fatal if field is empty

### See Also
- Drupal Twig filters → [Drupal Twig Filters](twig-filters.md)
- Core source: `core/lib/Drupal/Core/Template/TwigExtension.php`
