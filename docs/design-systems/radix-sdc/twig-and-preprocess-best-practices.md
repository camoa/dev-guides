---
description: You're deciding whether logic belongs in Twig or preprocess function
drupal_version: "11.x"
---

## 7.5 Twig and Preprocess Best Practices

### When to Use This Section
- You're deciding whether logic belongs in Twig or preprocess function
- You need guidance on Twig template inheritance (extend vs include vs embed)
- You're working with the Drupal attributes object
- You want performance best practices for Twig templates

### Preprocess vs Twig: What Belongs Where

#### CRITICAL PRINCIPLE: Separation of Concerns

**PREPROCESS FUNCTIONS (.theme file):** Logic and data manipulation
**TWIG TEMPLATES (.twig file):** Presentation and markup

#### Decision Framework: Preprocess or Twig?

| Task | Preprocess Function | Twig Template | WHY |
|------|---------------------|---------------|-----|
| **Data transformation** | ✅ | ❌ | Complex logic doesn't belong in templates |
| **Array manipulation** | ✅ | ❌ | PHP is better at array operations |
| **Database queries** | ✅ | ❌ | Never query in templates |
| **Conditional logic** | ❌ | ✅ | Simple conditionals are fine in Twig |
| **Loops** | ❌ | ✅ | Twig is designed for iteration |
| **Filters (t, url, date)** | ❌ | ✅ | Twig filters optimize better than PHP |
| **Adding CSS classes** | ✅ | ✅ | Both work; preprocess for complex logic |
| **Render arrays** | ✅ | ❌ | Return render arrays, don't call drupal_render() |

#### Pattern: What Goes in Preprocess

**File: `THEME_NAME.theme`**

```php
<?php

/**
 * Implements hook_preprocess_node().
 */
function THEME_NAME_preprocess_node(&$variables) {
  $node = $variables['node'];

  // GOOD: Data transformation
  $variables['formatted_date'] = \Drupal::service('date.formatter')
    ->format($node->getCreatedTime(), 'custom', 'F j, Y');

  // GOOD: Complex conditional class logic
  $variables['attributes']['class'][] = 'node';
  $variables['attributes']['class'][] = 'node--type-' . $node->bundle();
  if (!$node->isPublished()) {
    $variables['attributes']['class'][] = 'node--unpublished';
  }

  // GOOD: Adding contextual information
  $variables['author_name'] = $node->getOwner()->getDisplayName();

  // GOOD: Preparing render arrays for template
  $variables['share_buttons'] = [
    '#theme' => 'share_buttons',
    '#node' => $node,
  ];

  // BAD: Don't render in preprocess
  // $variables['content'] = \Drupal::service('renderer')->render($content);
}
```

**WHY IN PREPROCESS:**
- **Complexity** — Data transformation logic doesn't clutter template
- **Testability** — Can unit test PHP functions
- **Performance** — PHP is faster than Twig for complex operations
- **Reusability** — Logic can be shared across templates

#### Pattern: What Goes in Twig

**File: `templates/content/node--article.html.twig`**

```twig
{#
/**
 * @file
 * Theme override for article nodes.
 *
 * Available variables:
 * - formatted_date: Pre-formatted date string from preprocess
 * - author_name: Author display name from preprocess
 */
#}

{# GOOD: Simple conditional rendering #}
{% if author_name %}
  <div class="node__author">{{ 'By @name'|t({'@name': author_name}) }}</div>
{% endif %}

{# GOOD: Using Twig filters #}
<time datetime="{{ node.created.value|date('c') }}">
  {{ formatted_date }}
</time>

{# GOOD: Looping through content #}
{% for item in content.field_tags %}
  <span class="tag">{{ item }}</span>
{% endfor %}

{# GOOD: Using url() filter in template #}
<a href="{{ url('entity.node.canonical', {'node': node.id}) }}">
  {{ 'Read more'|t }}
</a>

{# BAD: Don't do complex logic in Twig #}
{% set complex_calculation = some_value * 100 / total_value %}
{# This should be in preprocess #}
```

**WHY IN TWIG:**
- **Presentation focus** — Templates focus on markup
- **Performance** — Twig filters like `t()` and `url()` optimize better than calling them in preprocess (lazy evaluation — only executed if actually printed)
- **Readability** — Frontend developers can work on templates without PHP knowledge
- **Caching** — Twig templates cache well

### Twig Template Inheritance: Extend vs Include vs Embed

#### Pattern: {% extends %} for Template Hierarchy

**WHEN TO USE:** Base template with blocks that child templates override

**File: `templates/layout/page--base.html.twig`** (Base template)

```twig
<div class="page-wrapper">
  <header class="page-header">
    {% block header %}
      {# Default header content #}
    {% endblock %}
  </header>

  <main class="page-content">
    {% block content %}
      {# Default content #}
    {% endblock %}
  </main>

  <footer class="page-footer">
    {% block footer %}
      {# Default footer content #}
    {% endblock %}
  </footer>
</div>
```

**File: `templates/layout/page--front.html.twig`** (Child template)

```twig
{% extends "page--base.html.twig" %}

{% block header %}
  {# Custom front page header #}
  <div class="hero-section">
    {{ page.header }}
  </div>
{% endblock %}

{% block content %}
  {# Keep parent content and add more #}
  {{ parent() }}
  <div class="featured-content">
    {# Additional front page content #}
  </div>
{% endblock %}

{# footer block inherits default from base #}
```

**WHY USE EXTENDS:**
- **DRY principle** — Share common structure across templates
- **Consistency** — All pages use same base wrapper
- **Maintainability** — Update base template, all children inherit changes

**CRITICAL:** Template can only extend ONE parent, and `{% extends %}` must be first tag in template.

---

#### Pattern: {% include %} for Reusable Snippets

**WHEN TO USE:** Drop in a component or snippet without inheritance

**File: `templates/content/node--article.html.twig`**

```twig
<article{{ attributes }}>

  {# Include share buttons component #}
  {% include 'THEME_NAME:share-buttons' with {
    'url': url('entity.node.canonical', {'node': node.id}),
    'title': label,
  } only %}

  {# Include breadcrumb #}
  {% include '@radix/breadcrumb/breadcrumb.twig' with {
    'breadcrumb': breadcrumb,
  } %}

  <div class="node__content">
    {{ content }}
  </div>
</article>
```

**WHY USE INCLUDE:**
- **Composition** — Build pages from components
- **Reusability** — Same snippet used in multiple templates
- **Isolation** — `only` keyword prevents variable bleed

**TIP:** Use `only` keyword to explicitly pass only specified variables:

```twig
{# GOOD: Explicit variable passing #}
{% include 'component.twig' with {'title': title} only %}

{# RISKY: All template variables passed #}
{% include 'component.twig' %}
```

---

#### Pattern: {% embed %} for Extending Included Templates

**WHEN TO USE:** Include a template BUT override some of its blocks

**File: `components/card/card.twig`**

```twig
<div class="card">
  <div class="card-header">
    {% block card_header %}
      <h3>{{ title }}</h3>
    {% endblock %}
  </div>

  <div class="card-body">
    {% block card_body %}
      {{ content }}
    {% endblock %}
  </div>

  <div class="card-footer">
    {% block card_footer %}
      {# Default footer #}
    {% endblock %}
  </div>
</div>
```

**File: `templates/node--teaser.html.twig`**

```twig
{% embed 'THEME_NAME:card' with {'title': label} %}

  {% block card_body %}
    {# Override card body #}
    {{ content.field_image }}
    {{ content.body }}
  {% endblock %}

  {% block card_footer %}
    {# Custom footer for node teaser #}
    <a href="{{ url }}" class="btn btn-primary">
      {{ 'Read more'|t }}
    </a>
  {% endblock %}

{% endembed %}
```

**WHY USE EMBED:**
- **Flexible composition** — Include base structure, customize parts
- **DRY principle** — Reuse card structure, override specific sections
- **Powerful pattern** — Combines benefits of extend and include

**COMPARISON:**

| Method | Purpose | Can Override Blocks? | Variable Scope |
|--------|---------|---------------------|----------------|
| `{% extends %}` | Template hierarchy | ✅ | Inherits all |
| `{% include %}` | Drop in snippet | ❌ | Explicit with `with` |
| `{% embed %}` | Include + override blocks | ✅ | Explicit with `with` |

### Attributes Object Best Practices

#### CRITICAL RULE: Always Use attributes.addClass()

**Pattern: Proper Attribute Usage**

```twig
{# GOOD: Use attributes object #}
{%
  set classes = [
    'node',
    'node--type-' ~ node.bundle|clean_class,
    node.isPromoted() ? 'node--promoted',
    node.isSticky() ? 'node--sticky',
    not node.isPublished() ? 'node--unpublished',
    view_mode ? 'node--view-mode-' ~ view_mode|clean_class,
  ]
%}

<article{{ attributes.addClass(classes) }}>
  {{ content }}
</article>
```

**WHY:**
- **Drupal integration** — Drupal can add contextual classes, IDs, data attributes
- **Module compatibility** — Contrib modules can modify attributes
- **Extensibility** — Other code can add attributes without template changes

**BAD PRACTICE: Hardcoded classes**

```twig
{# BAD: Hardcoded classes prevent Drupal from adding attributes #}
<article class="node node--article node--promoted">
  {{ content }}
</article>
```

**WHY BAD:**
- **Loss of functionality** — Drupal can't add contextual editing, quickedit, contextual links
- **Module conflicts** — Modules that depend on attributes won't work
- **Inflexible** — Can't add custom attributes without template changes

#### Pattern: Merging Custom Attributes

```twig
{# Scenario: Component receives attributes prop #}
{%
  set classes = [
    'my-component',
    variant ? 'my-component--' ~ variant : '',
  ]
%}

{# Merge component classes with passed attributes #}
<div {{ attributes.addClass(classes) }}>
  {{ slots.content }}
</div>
```

**WHY:** Allows callers to add their own classes/attributes without overriding component classes.

#### Pattern: Separating Title and Content Attributes

```twig
{# Common in node templates #}
<article{{ attributes }}>

  <h2{{ title_attributes.addClass('node__title') }}>
    <a href="{{ url }}">{{ label }}</a>
  </h2>

  <div{{ content_attributes.addClass('node__content') }}>
    {{ content }}
  </div>

</article>
```

**WHY:** Different elements may have different contextual attributes from Drupal.

### Twig Debug Mode and Performance

#### Development vs Production Settings

**Development: Enable Twig Debugging**

**File: `sites/default/services.yml`**

```yaml
parameters:
  twig.config:
    debug: true
    auto_reload: true
    cache: false
```

**WHAT THIS DOES:**
- **debug: true** — Shows template suggestions in HTML comments
- **auto_reload: true** — Recompiles templates on every page load
- **cache: false** — Doesn't cache compiled templates

**WHEN TO USE:** Local development only

**WHY:** See which template is rendering, find template suggestions, no need to clear cache after changes.

---

**Production: Disable Twig Debugging**

```yaml
parameters:
  twig.config:
    debug: false
    auto_reload: false
    cache: true
```

**WHAT THIS DOES:**
- **debug: false** — No HTML comments (cleaner markup, better performance)
- **auto_reload: false** — Only recompile if template modified
- **cache: true** — Cache compiled PHP from Twig

**WHEN TO USE:** Staging and production

**WHY:** Performance. Twig compilation is expensive; caching drastically improves speed.

**PERFORMANCE IMPACT:**
- **Debug on**: ~20-30% slower page loads
- **Cache off**: ~50-70% slower (recompiles every page load)
- **Production settings**: Optimal performance

### Common Mistakes Senior Themers Catch in Code Review

**1. Not returning render arrays from preprocess**

```php
// BAD: Calling renderer in preprocess
function mytheme_preprocess_node(&$variables) {
  $content = ['#markup' => '<div>Content</div>'];
  $variables['rendered_content'] = \Drupal::service('renderer')->render($content);
}
```

**WHY BAD:** Twig renders automatically. Pre-rendering prevents caching optimization and breaks lazy rendering.

**CORRECT:**

```php
// GOOD: Return render array
function mytheme_preprocess_node(&$variables) {
  $variables['rendered_content'] = [
    '#markup' => '<div>Content</div>',
  ];
}
```

---

**2. Calling theme() or drupal_render() in preprocess**

```php
// BAD: Legacy Drupal 7 patterns
function mytheme_preprocess_node(&$variables) {
  $variables['custom'] = theme('item_list', ['items' => $items]);
}
```

**WHY BAD:** These are Drupal 7 functions. Drupal 8+ uses render arrays.

**CORRECT:**

```php
// GOOD: Use render arrays
function mytheme_preprocess_node(&$variables) {
  $variables['custom'] = [
    '#theme' => 'item_list',
    '#items' => $items,
  ];
}
```

---

**3. Complex logic in Twig templates**

```twig
{# BAD: Complex calculation in Twig #}
{% set percentage = (completed_count / total_count * 100)|round %}
{% set status_class = percentage > 80 ? 'success' : (percentage > 50 ? 'warning' : 'danger') %}
```

**WHY BAD:** Difficult to test, debug, and maintain. Twig is not designed for complex logic.

**CORRECT:**

```php
// GOOD: Logic in preprocess
function mytheme_preprocess_progress_bar(&$variables) {
  $completed = $variables['completed_count'];
  $total = $variables['total_count'];
  $percentage = round(($completed / $total) * 100);

  if ($percentage > 80) {
    $status_class = 'success';
  } elseif ($percentage > 50) {
    $status_class = 'warning';
  } else {
    $status_class = 'danger';
  }

  $variables['percentage'] = $percentage;
  $variables['status_class'] = $status_class;
}
```

```twig
{# GOOD: Simple rendering in Twig #}
<div class="progress-bar progress-bar--{{ status_class }}">
  {{ percentage }}%
</div>
```

---

**4. Using PHP functions directly in Twig**

```twig
{# BAD: Twig doesn't have direct PHP function access (security) #}
<a href="/node/{{ node.id }}">
  {{ label }}
</a>
```

**CORRECT:**

```twig
{# GOOD: Use Twig filters #}
<a href="{{ path('entity.node.canonical', {'node': node.id}) }}">
  {{ label }}
</a>

{# Or use url() function #}
<a href="{{ url('entity.node.canonical', {'node': node.id}) }}">
  {{ label }}
</a>
```

**WHY:** Twig filters are security-hardened and cache-aware. Direct PHP is blocked.

---

**5. Not using trans filter for strings**

```twig
{# BAD: Hardcoded English string #}
<button>Read more</button>
```

**CORRECT:**

```twig
{# GOOD: Translatable string #}
<button>{{ 'Read more'|t }}</button>
```

**WHY:** Makes site translatable. Even single-language sites benefit from centralized string management.

---

**6. Forgetting to check variable existence**

```twig
{# BAD: Will error if author_name doesn't exist #}
<div class="author">{{ author_name }}</div>
```

**CORRECT:**

```twig
{# GOOD: Check existence first #}
{% if author_name is defined and author_name %}
  <div class="author">{{ author_name }}</div>
{% endif %}

{# Or use default filter #}
<div class="author">{{ author_name|default('Anonymous') }}</div>
```

---

**7. Not using 'only' with includes**

```twig
{# RISKY: Passes all variables (potential variable bleed) #}
{% include 'component.twig' with {'title': title} %}
```

**CORRECT:**

```twig
{# GOOD: Explicit variable isolation #}
{% include 'component.twig' with {'title': title} only %}
```

**WHY:** Prevents accidental variable collisions and makes variable dependencies explicit.

#### See Also
- [7.1 Component YAML Schema](#71-component-yaml-schema)
- [7.2 Props and Slots](#72-props-and-slots)
- Drupal Twig Documentation: https://www.drupal.org/docs/theming-drupal/twig-in-drupal