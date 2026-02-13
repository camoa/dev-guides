---
description: You're implementing page-level layouts (templates)
drupal_version: "11.x"
---

## 6. Templates → Drupal Theme Layer

### When to Use This Section
- You're implementing page-level layouts (templates)
- You need to override Drupal's default page structure
- You're composing organisms into complete pages

### 6.1 Page Template Structure

#### Pattern: Page Template Hierarchy

**Radix Template Hierarchy:**
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

#### Decision Table: Template Override Strategy

| Template | Override When | Location |
|----------|---------------|----------|
| `page.html.twig` | Custom page structure | `templates/layout/` |
| `node.html.twig` | Custom node display | `templates/content/` |
| `node--TYPE.html.twig` | Content type specific | `templates/content/` |
| `block.html.twig` | Custom block wrapper | `templates/layout/` |
| `region.html.twig` | Custom region wrapper | `templates/layout/` |

#### Common Mistakes
- **Not using Drupal regions** — Define regions in `*.info.yml`
- **Hardcoding content** — Use region variables from Drupal
- **Not using Bootstrap grid** — Wrap content in `.container`, `.row`, `.col-*`
- **Missing template suggestions** — Use `hook_theme_suggestions_*` for variants

#### See Also
- [1.3 Theme Configuration Files](#13-theme-configuration-files)
- [6.3 Template Hierarchy](#63-template-hierarchy)

---

### 6.2 Layout Builder Composition

#### Pattern: Composing Organisms via Layout Builder

**Layout Builder replaces traditional page templates for content types:**

```
Traditional Approach:
page.html.twig → regions → blocks/content

Layout Builder Approach:
Layout Builder → sections → blocks (including SDC organisms)
```

**Configuration:**
1. Enable Layout Builder for content type
2. Configure default layout
3. Add organism blocks to sections
4. Content editors can customize per-node

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

#### Decision Table: Template vs Layout Builder

| Use Template When | Use Layout Builder When |
|-------------------|-------------------------|
| Consistent structure across all pages | Per-page customization needed |
| Header/footer organisms | Content-specific organisms |
| Simple layouts | Complex, flexible layouts |
| Developer-controlled | Editor-controlled |

#### Common Mistakes
- **Not enabling Layout Builder** — Required in content type settings
- **Missing block plugins** — Organisms need block plugins for Layout Builder
- **No default layout** — Provide sensible default structure
- **Cache issues** — Ensure proper cache tags on blocks

#### See Also
- [5.3 Layout Builder Integration](#53-layout-builder-integration)
- Drupal Layout Builder: https://www.drupal.org/docs/8/core/modules/layout-builder

---

### 6.3 Template Hierarchy

#### Pattern: Radix Template Hierarchy

**Template Discovery Order:**
```
1. Sub-theme templates/        (Your custom overrides)
2. Radix base theme templates/ (Radix defaults)
3. Drupal core templates/      (Core fallback)
```

**Template Suggestion Hierarchy Example:**
```
node.html.twig                    # Generic node
node--TYPE.html.twig              # Content type specific
node--TYPE--VIEW-MODE.html.twig   # Content type + view mode
node--NID.html.twig               # Specific node
```

**Debugging Template Suggestions:**
1. Enable Twig debugging: `sites/default/services.yml`
2. View source in browser
3. Look for `<!-- FILE NAME SUGGESTIONS: -->` comments

#### Common Mistakes
- **Not using most specific template** — More specific templates override generic ones
- **Copying all Radix templates** — Only override what you need to change
- **Not clearing cache** — Template changes require cache clear
- **Missing template suggestions** — Use `hook_theme_suggestions_alter()`

#### See Also
- [6.1 Page Template Structure](#61-page-template-structure)
- Drupal Theming Guide: https://www.drupal.org/docs/theming-drupal