---
description: Migrate from manual icons, icon fonts, or other systems to Icon API
drupal_version: "11.x"
---

# Migration Patterns

## When to Use

> Use when you're migrating from manual icon management, icon fonts, or other icon systems to Icon API.

## Decision

| Current system | Migration strategy | Effort |
|---|---|---|
| Manual SVG in templates | Create SVG extractor pack | Low |
| Icon font (Font Awesome, etc.) | Font extractor or switch to SVG | Medium |
| Image files (PNG, WebP) | Path extractor | Low |
| Multiple unorganized sources | Consolidate into packs | Medium-High |
| Custom icon rendering logic | Custom extractor plugin | High |

## Pattern

Migrate from manual SVG embedding:

```twig
{# Before - Manual SVG in template #}
<svg width="24" height="24" viewBox="0 0 24 24">
  <path d="M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8z"/>
</svg>

{# After - Icon API #}
{# 1. Create icon pack in my_theme.icons.yml #}
{# 2. Move SVG to themes/my_theme/icons/home.svg #}
{# 3. Use icon() function #}
{{ icon('my_theme:home', { size: 24 }) }}
```

Migrate from Font Awesome:

```twig
{# Before - Font Awesome CSS classes #}
<i class="fas fa-home"></i>

{# After - Icon API with font extractor #}
{# Option 1: Keep using font #}
{{ icon('fontawesome:home') }}

{# Option 2: Switch to SVG (recommended) #}
{# Download Font Awesome SVGs, create SVG pack #}
{{ icon('fontawesome_svg:home', { size: 24 }) }}
```

Icon pack for Font Awesome migration:

```yaml
# Option 1: Font extractor
fontawesome:
  extractor: font
  config:
    sources:
      - fonts/fontawesome.woff2
  library: "my_theme/fontawesome"
  template: >-
    <i class="fas fa-{{ icon_id }}" style="font-size: {{ size|default(24) }}px;"></i>

# Option 2: SVG extractor (recommended)
fontawesome_svg:
  extractor: svg
  config:
    sources:
      - icons/fontawesome/{icon_id}.svg
  template: >-
    <svg width="{{ size|default(24) }}" height="{{ size|default(24) }}">
      {{ content }}
    </svg>
```

Migrate image-based icons:

```twig
{# Before - Image files #}
<img src="{{ base_path ~ directory }}/images/icons/home.png" alt="Home" width="24">

{# After - Path extractor #}
{{ icon('my_theme:home', {
  size: 24,
  alt: 'Home'  # For semantic icons
}) }}
```

```yaml
# Image icon pack
image_icons:
  extractor: path
  config:
    sources:
      - images/icons/{icon_id}.png
      - images/icons/{icon_id}.webp
  template: >-
    <img src="{{ source }}"
         width="{{ size|default(24) }}"
         height="{{ size|default(24) }}"
         alt="{{ alt|default('') }}"
         loading="lazy">
```

Batch migrate template files:

```bash
# Find all manual SVG embeddings
grep -r "<svg" themes/my_theme/templates/

# Find all Font Awesome icons
grep -r "fas fa-" themes/my_theme/templates/

# Find all image-based icons
grep -r 'icons/' themes/my_theme/templates/
```

Reference: Migration is theme-specific, no core migration path.

## Common Mistakes

- **Wrong**: Migrating everything at once → **Right**: Migrate incrementally by component/template
- **Wrong**: Not updating documentation → **Right**: Update theme docs with new icon() usage
- **Wrong**: Breaking existing functionality → **Right**: Test thoroughly, icons are high-visibility
- **Wrong**: Forgetting to remove old assets → **Right**: Clean up unused font files, image directories
- **Wrong**: Not updating CSS → **Right**: Remove icon-specific CSS that's now in Icon API templates

## See Also

- [Debugging Templates](debugging-templates.md)
- [Custom Extractor Development](custom-extractor-development.md)
- Reference: Project-specific migration planning
