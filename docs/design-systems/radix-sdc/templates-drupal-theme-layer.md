---
description: Templates and Drupal theme layer — page template structure, Layout Builder composition, template hierarchy
drupal_version: "11.x"
---

# Templates Drupal Theme Layer

## When to Use

> Use this when implementing page-level layouts (templates), overriding Drupal's default page structure, or composing organisms into complete pages.

## Decision

| Template | Override When | Location |
|----------|---------------|----------|
| `page.html.twig` | Custom page structure | `templates/layout/` |
| `node.html.twig` | Custom node display | `templates/content/` |
| `node--TYPE.html.twig` | Content type specific | `templates/content/` |
| `block.html.twig` | Custom block wrapper | `templates/layout/` |
| `region.html.twig` | Custom region wrapper | `templates/layout/` |

**Template vs Layout Builder:**

| Use Template When | Use Layout Builder When |
|-------------------|-------------------------|
| Consistent structure across all pages | Per-page customization needed |
| Header/footer organisms | Content-specific organisms |
| Simple layouts | Complex, flexible layouts |
| Developer-controlled | Editor-controlled |

## Pattern

**Template Hierarchy:**

```
Radix Base Theme
├── templates/
│   ├── layout/
│   │   ├── page.html.twig
│   │   ├── region.html.twig
│   │   └── block.html.twig
│   ├── navigation/
│   │   ├── menu.html.twig
│   │   └── breadcrumb.html.twig
│   └── content/
│       ├── node.html.twig
│       └── field.html.twig

Sub-Theme (Your Theme)
├── templates/
│   ├── layout/
│   │   └── page.html.twig       # Override Radix page
│   └── content/
│       └── node--article.html.twig  # Content type specific
```

**Template Discovery Order:**

```
1. Sub-theme templates/        (Your custom overrides)
2. Radix base theme templates/ (Radix defaults)
3. Drupal core templates/      (Core fallback)
```

**Template Suggestion Hierarchy:**

```
node.html.twig                    # Generic node
node--TYPE.html.twig              # Content type specific
node--TYPE--VIEW-MODE.html.twig   # Content type + view mode
node--NID.html.twig               # Specific node
```

**File: `templates/layout/page.html.twig`**

```twig
{#
/**
 * @file
 * Theme override for page template.
 *
 * Available regions:
 * - navbar_branding
 * - navbar_left
 * - navbar_right
 * - header
 * - content
 * - footer
 */
#}

{# Include navbar organism #}
{% include 'THEME_NAME:site-navbar' with {
  slots: {
    branding: page.navbar_branding,
    navigation: page.navbar_left,
    actions: page.navbar_right,
  }
} %}

{# Header region #}
{% if page.header %}
  <header class="page-header">
    <div class="container">
      {{ page.header }}
    </div>
  </header>
{% endif %}

{# Main content #}
<main class="page-content">
  <div class="container">
    {{ page.content }}
  </div>
</main>

{# Footer region #}
{% if page.footer %}
  <footer class="page-footer">
    <div class="container">
      {{ page.footer }}
    </div>
  </footer>
{% endif %}
```

**Layout Builder Composition:**

```
Traditional Approach:
page.html.twig → regions → blocks/content

Layout Builder Approach:
Layout Builder → sections → blocks (including SDC organisms)
```

**Example Layout:**

```
Section 1 (Full Width)
└── Hero Section Block (SDC organism)

Section 2 (Two Column)
├── Column 1: Main Content
└── Column 2: Sidebar Widgets

Section 3 (Full Width)
└── Card Grid Block (SDC organism)
```

**Debugging Template Suggestions:**

1. Enable Twig debugging: `sites/default/services.yml`
2. View source in browser
3. Look for `<!-- FILE NAME SUGGESTIONS: -->` comments

## Common Mistakes

- **Wrong**: Not defining regions in `*.info.yml` → **Right**: Define regions before using in templates
- **Wrong**: Hardcoding content in templates → **Right**: Use region variables from Drupal
- **Wrong**: Not using Bootstrap grid → **Right**: Wrap content in `.container`, `.row`, `.col-*`
- **Wrong**: Copying all Radix templates → **Right**: Only override what you need to change
- **Wrong**: Not clearing cache after template changes → **Right**: Template changes require cache clear
- **Wrong**: Using generic template when specific exists → **Right**: Use most specific template
- **Wrong**: Not enabling Layout Builder when needed → **Right**: Enable in content type settings
- **Wrong**: Missing block plugins for organisms → **Right**: Organisms need block plugins for Layout Builder
- **Wrong**: No default layout → **Right**: Provide sensible default structure

## See Also

- [Organisms SDC Layout Builder](organisms-sdc-layout-builder.md)
- [Layout Builder Best Practices](layout-builder-best-practices.md)
- [Sub-Theme Architecture](sub-theme-architecture.md)
- Drupal Theming Guide: https://www.drupal.org/docs/theming-drupal
- Drupal Layout Builder: https://www.drupal.org/docs/8/core/modules/layout-builder
