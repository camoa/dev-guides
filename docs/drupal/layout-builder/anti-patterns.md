## 17. Anti-Patterns & Common Mistakes

### When to Use

When you need to know what NOT to do — these are patterns that seem logical but cause problems.

### Decision

| Anti-Pattern | Why It's Wrong | Correct Approach |
|--------------|----------------|------------------|
| **Using LB for site header/footer** | LB is per-entity, not site-wide. Adds overhead to every entity render | Use Block Layout for site structure. LB for entity content areas only |
| **Enabling overrides everywhere "just in case"** | Creates maintenance nightmare. Can't push default updates to overridden entities | Enable overrides only when proven necessary. Most sites don't need per-entity layouts |
| **Creating 50+ Layout Builder Styles** | Overwhelms editors, dilutes design system | Curate 5-10 styles matching design system. More = harder to choose, less consistency |
| **Using inline blocks for repeated content** | Creates duplicate content, orphan blocks, deployment headaches | Use reusable block content entities or field blocks for anything used more than once |
| **Not running cron** | Orphaned inline blocks accumulate, bloating database | Schedule regular cron runs, consider cleanup modules for large sites |
| **Hardcoding blocks in preprocess** | Can't export/import, not portable, breaks config workflow | Use configuration, recipes, or contrib modules. Keep presentation in config |
| **Relying on restrictions for security** | Restrictions are UI convenience, not access control | Use proper permissions and field access. Don't hide sensitive data via LB restrictions |
| **Changing layout plugin regions** | Breaks all existing sections using that layout | Create new layout plugin instead of modifying existing. Deprecate old layout |
| **Mixing layout concerns** | Using LB for structure, Paragraphs for presentation, Block Layout for content | Each tool has purpose: Block Layout (site), LB (entity display), Paragraphs (field collections) |
| **Not validating config before import** | Malformed YAML causes white screens, broken layouts | Use `drush config:inspect` to validate, test imports on dev first |
| **Assuming editors understand overrides** | Editors expect changes to defaults to apply everywhere, get confused when overridden entities don't update | Document override behavior clearly, consider warnings in UI, train editors |
| **Creating deeply nested sections** | Performance hit, confusing for editors, hard to maintain | Keep layouts flat. 2-3 sections typical, rarely need more than 5 |

### Pattern

**Anti-Pattern: Hardcoded Block Placement**

```php
// DON'T DO THIS
function mymodule_preprocess_node(&$variables) {
  if ($variables['view_mode'] === 'full') {
    $block = Block::load('my_block');
    $render = \Drupal::entityTypeManager()
      ->getViewBuilder('block')
      ->view($block);
    $variables['content']['hardcoded_block'] = $render;
  }
}
```

**Why wrong:**
- Not exportable via config
- Can't be rearranged by editors
- Bypasses LB access control
- No cache tags from LB
- Breaks if block doesn't exist

**Correct approach:**
```yaml
# In entity_view_display config or via UI
components:
  - uuid: abc-123
    region: content
    configuration:
      id: 'block_content:my-block-uuid'
      label_display: '0'
    weight: 5
```

**Anti-Pattern: No Block Restrictions**

```php
// Letting editors see ALL blocks
// - 200+ field blocks from all entity types
// - System blocks editors shouldn't touch
// - Debug/devel blocks in production
```

**Why wrong:**
- Editor overwhelm, can't find right blocks
- Accidental exposure of sensitive data
- Inconsistent designs when editors pick random blocks
- Support burden when editors choose wrong blocks

**Correct approach:**
```php
// Curated block library
function mymodule_layout_builder_block_alter(array &$definitions) {
  $allowed_base_ids = [
    'field_block:node:article',  // Article fields only
    'inline_block:basic',        // Basic inline blocks
    'system_branding_block',     // Specific approved blocks
  ];

  foreach ($definitions as $id => $definition) {
    $matches = FALSE;
    foreach ($allowed_base_ids as $base) {
      if (strpos($id, $base) === 0) {
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

**Anti-Pattern: Overrides Without Plan**

```yaml
# Enabling overrides immediately
third_party_settings:
  layout_builder:
    enabled: true
    allow_custom: true  # DON'T do this by default
```

**Why wrong:**
- Editors override immediately "just to see"
- Default updates don't apply to overridden entities
- Content-based deployment complexity
- No central control over layouts
- Can't A/B test layout changes easily

**Correct approach:**
```yaml
# Start with defaults only
third_party_settings:
  layout_builder:
    enabled: true
    allow_custom: false
    sections:
      # Well-designed default layout
      - layout_id: layout_twocol_section
        components: [...]

# Only enable overrides after:
# 1. Default layout proven insufficient
# 2. Editorial team trained
# 3. Override policy documented
# 4. Deployment workflow accounts for content sync
```

### Common Mistakes

- **Using @extend in layout CSS** → Creates selector explosion, hard to debug, poor performance. Use Bootstrap mixins or classes directly
- **Not testing as editor** → Admin sees everything. Test with editor role to verify restrictions work
- **Forgetting about translations** → Overrides don't inherit from defaults in translations. Layout per language requires separate overrides
- **Assuming LB is cacheable by default** → It is, but custom blocks/preprocessing can break cache. Add cache metadata correctly
- **Not considering mobile** → Desktop-focused layouts break on mobile. Test responsive behavior or use mobile-first layouts
- **Treating inline blocks as portable** → Inline blocks tied to specific entity/section. Can't easily move between entities
- **Using !important in style CSS** → Causes specificity wars, hard to override. Use proper selector specificity
- **Not monitoring orphaned blocks** → Check `inline_block_usage` table periodically for cleanup needs

### See Also

- Section 16: Best Practices (what TO do)
- Section 18: Security & Performance (avoiding performance anti-patterns)
- Reference: [Layout Builder issue queue](https://www.drupal.org/project/issues/layout_builder) for documented problems
