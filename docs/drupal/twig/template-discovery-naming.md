---
topic: drupal/twig
guide: template-discovery-naming
---

## Template Discovery & Naming

### When to Use
When you need to create a template file and need to name it correctly, or when your template is not being picked up by Drupal.

### Decision
| Template type | Convention | Example |
|---|---|---|
| Base hook | `hook-name.html.twig` | `node.html.twig` |
| Suggestion (one level) | `hook-name--suggestion.html.twig` | `node--article.html.twig` |
| Suggestion (two levels) | `hook-name--s1--s2.html.twig` | `node--article--teaser.html.twig` |
| Field-specific | `field--field-name--bundle.html.twig` | `field--field-hero--article.html.twig` |
| Block plugin | `block--plugin-id.html.twig` | `block--system-menu-block.html.twig` |

**Naming rules:**
- Use **hyphens** (`-`) in filenames — underscores in hook names become hyphens in filenames
- Suggestions use **double hyphens** (`--`) as separators
- Theme engine converts hyphens to underscores when matching to hook names

**Discovery order** (highest to lowest priority):
1. Active theme's `templates/` directory
2. Active theme's base theme `templates/` directories (in reverse inheritance order)
3. Module's `templates/` directory (for the module that registered the hook)

### Pattern
```twig
{# Filename: node--article--teaser.html.twig #}
{# This overrides node.html.twig for article nodes in teaser view mode #}
{# Place in: themes/custom/mytheme/templates/content/ #}

{# Subdirectories under templates/ are scanned recursively — organize freely #}
```

**Template file → hook name mapping:**
- `node--article.html.twig` → theme hook `node__article`
- `field--field-tags.html.twig` → theme hook `field__field_tags`
- `block--system-branding-block.html.twig` → theme hook `block__system_branding_block`

### Common Mistakes
- Using single hyphens between suggestion parts → `node-article.html.twig` won't be found as a suggestion
- Placing templates outside the `templates/` directory → Drupal won't scan arbitrary directories
- Not clearing the theme registry cache after adding a template → run `drush cr` after new template files
- Mixing underscores and hyphens incorrectly — filenames use hyphens, hook names use underscores

### See Also
- Template suggestions → [Template Suggestions](template-suggestions.md)
- Core source: `core/lib/Drupal/Core/Theme/Registry.php`
