---
description: When a Drupal block needs to render as an SDC, create a block template that includes the SDC — don't hardcode SDCs in page templates.
drupal_version: "11.x"
tldr: When a Drupal block needs to render as an SDC, create a block template that includes the SDC. Don't hardcode SDCs in page templates.
---

# Block → SDC via Block Template

**What:** When a Drupal block needs to render as an SDC, create a block template that includes the SDC. Don't hardcode SDCs in page templates.

**Rationale:** Drupal's block placement system handles where blocks appear, contextual links, region assignment, visibility conditions, and admin permissions. Hardcoding SDCs in page templates bypasses all of that — the SDC always renders regardless of placement config, and editors lose contextual controls. A block template that wraps the SDC keeps placement/visibility in the block system while delegating rendering to the component.

**When it applies:** Any time a block (custom block type, plugin block, view block) should render as an SDC. The pattern: one block template per block plugin/type, one `{% include %}` or `{% embed %}` of the SDC inside.

**Example:**

```twig
{# templates/block/block--mytheme-searchapiform.html.twig #}
{% set component_props = {
  placeholder: 'Search articles, news, and events',
  action_url: path('search.view'),
  field_name: 'keys',
} %}

{% include 'mytheme:search-bar' with component_props %}
```

```twig
{# Wrong — SDC hardcoded in page template #}
{# templates/page.html.twig #}
<header>
  {% include 'mytheme:search-bar' with { placeholder: 'Search...' } %}
</header>
```
