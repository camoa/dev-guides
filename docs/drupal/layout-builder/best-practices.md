---
description: Layout Builder best practices and patterns
drupal_version: "11.x"
---

# Best Practices & Patterns

### When to Use

When establishing Layout Builder workflows, governance, or making architectural decisions.

### Decision

| Scenario | Best Practice | Why |
|----------|--------------|-----|
| **Starting new project** | Defaults only initially, add overrides later if needed | Easier to maintain, config-based, can always enable overrides later |
| **Content governance** | Restrict available blocks and layouts | Prevents editor overwhelm, enforces design system, maintains consistency |
| **Deployment workflow** | Use defaults + config export for infrastructure | Portable across environments, version controlled, no content dependencies |
| **Editorial flexibility** | Provide curated block library, not everything | Better UX than 100+ blocks, guides editors to approved patterns |
| **Performance** | Cache layouts aggressively, lazy-load images in blocks | LB renders many blocks per page, each block = query potential |
| **Naming** | Descriptive labels for blocks/layouts/styles | "Article Body Content" better than "field_block:node:article:body" for editors |
| **Inline blocks** | Use sparingly, prefer reusable or field blocks | Inline blocks create orphans, complicate deployment, harder to manage |
| **Configuration schema** | Validate config before import | Prevents white screens from malformed YAML, catches errors early |
| **Testing** | Test as editor role, not admin | Admins bypass restrictions and see different UI than editors |
| **Documentation** | Document override behavior for editors | "Once overridden, changes to default layout won't apply to this entity" |

### Pattern

**Configuration-First Workflow:**

1. Design layout in default view display
2. Export configuration
3. Version control YAML files
4. Import to staging/production
5. Only enable overrides when per-entity flexibility proven necessary

**Block Library Curation:**

```php
// Whitelist approved blocks
function mymodule_layout_builder_block_alter(array &$definitions) {
  $allowed_patterns = [
    'field_block:node:*',           // All field blocks
    'inline_block:basic',           // Basic inline blocks only
    'system_branding_block',        // Specific system blocks
    'views_block:news-*',           // News views
  ];

  foreach ($definitions as $id => $definition) {
    $matches = FALSE;
    foreach ($allowed_patterns as $pattern) {
      if (fnmatch($pattern, $id)) {
        $matches = TRUE;
        break;
      }
    }

    if (!$matches) {
      unset($definitions[$id]);
    }
  }
}
```

**Recipe Pattern for Layouts:**

```yaml
# recipes/standard_layouts/recipe.yml
name: 'Standard Content Layouts'
install:
  - layout_builder
  - layout_builder_styles
config:
  import:
    # Import pre-configured view displays
    core.entity_view_display.node.article.default: '*'
    core.entity_view_display.node.page.default: '*'
  actions:
    # Enable LB on landing page type
    core.entity_view_display.node.landing_page.default:
      enableLayoutBuilder: true
      setOverridable: false
```

### Common Mistakes

- **Enabling overrides by default** → Start with defaults. Overrides create maintenance burden and deployment complexity
- **Not restricting blocks** → Editors overwhelmed by 100+ blocks. Curate library to approved set
- **Treating LB as page builder** → LB is for entity display, not site architecture. Use Block Layout for site structure
- **Forgetting about cache** → LB pages can be slow without proper caching. Enable render cache, use block-level cache tags
- **Not planning for multisite** → Overrides are content, not config. Multisite deployments with overrides need content sync
- **Mixing presentation and structure** → Use layout plugins for structure (columns, regions), Layout Builder Styles for presentation (colors, spacing)
- **Not documenting for editors** → Editors need to know: which blocks do what, when to use inline vs reusable, what happens when overriding
- **Hardcoding in preprocess** → Configuration should live in config, not code. Use third-party settings instead of hardcoded values
- **Not testing import** → Always test config import on fresh site to verify dependencies and recipes work

### See Also

- Section 9: Defaults vs Overrides (choosing approach)
- Section 10: Layout Builder Restrictions (curating blocks)
- Section 14: Config Export & Recipes (deployment patterns)
- Section 18: Security & Performance (optimization)
