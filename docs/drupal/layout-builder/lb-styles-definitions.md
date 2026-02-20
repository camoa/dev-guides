## 11.2. Layout Builder Style Definitions

### When to Use

Individual styles define CSS classes to apply, which blocks/sections can use them, and which group they belong to. Styles are config entities exported as YAML for deployment via config sync.

### Decision

| If you need... | Use... | Why |
|---|---|---|
| Section backgrounds, spacing, containers | `type: section` | Applied to layout wrapper via `layout_builder_styles_preprocess_layout()` |
| Block borders, shadows, alignment | `type: component` | Applied to block wrapper via event subscriber |
| Limit to specific block types | `block_restrictions` array | Style only appears for listed block plugin IDs |
| Limit to specific layouts | `layout_restrictions` array | Style only appears for listed layout plugin IDs |
| Inline + reusable block types | `inline_block:BUNDLE` in restrictions | Applies to both inline and reusable blocks of that bundle |

### Pattern

**Basic Style Config:**
```yaml
# config/sync/layout_builder_styles.style.padding_large.yml
langcode: en
status: true
dependencies: {  }
id: padding_large
label: 'Large Padding'
classes: 'p-5'              # One class per line, or space-separated
type: component             # 'section' or 'component'
group: spacing              # Must match existing group ID
weight: 10
block_restrictions: []      # Empty = applies to all blocks
layout_restrictions: []     # Empty = applies to all layouts
uuid: abc-123
```

**Multi-Line Classes:**
```yaml
# config/sync/layout_builder_styles.style.card_primary.yml
id: card_primary
label: 'Primary Card Style'
classes: |
  card
  border-primary
  shadow-sm
  rounded
type: component
group: effects
weight: 0
```

**Block Restrictions Example:**
```yaml
# Only applies to inline/reusable Article and Page blocks
id: article_highlight
label: 'Article Highlight'
classes: 'border-start border-5 border-primary ps-4'
type: component
group: effects
block_restrictions:
  - 'inline_block:article'       # Inline Article blocks
  - 'inline_block:basic'         # Inline Basic blocks
  - 'system_main_block'          # Main content block
```

**Layout Restrictions Example:**
```yaml
# Only applies to two-column layouts
id: column_gap_large
label: 'Large Column Gap'
classes: 'gap-5'
type: section
group: spacing
layout_restrictions:
  - layout_twocol_section       # Core two-column layout
  - layout_threecol_section     # Core three-column layout
  - radix_twocol                # Radix two-column
```

**Bootstrap Integration Example:**
```yaml
# Map to Bootstrap utilities
id: bg_primary
label: 'Primary Background'
classes: 'bg-primary text-white p-4'
type: section
group: background
weight: 0

id: text_center
label: 'Center Aligned'
classes: 'text-center'
type: component
group: alignment
weight: 0

id: shadow_medium
label: 'Medium Shadow'
classes: 'shadow'
type: component
group: effects
weight: 10
```

**Result in Entity View Display Config:**
```yaml
# core.entity_view_display.node.article.default.yml
third_party_settings:
  layout_builder:
    sections:
      - layout_id: layout_twocol_section
        layout_settings:
          layout_builder_styles_style:
            - column_gap_large      # Section style applied
        components:
          - uuid: abc-123
            configuration:
              id: 'inline_block:article'
              layout_builder_styles_style:
                - card_primary      # Component style applied
                - shadow_medium
```

Reference: `modules/contrib/layout_builder_styles/src/Entity/LayoutBuilderStyle.php`

### Common Mistakes

- **Not defining CSS** → LB Styles only adds classes. Define corresponding CSS in theme or use Bootstrap classes
- **Wrong restriction syntax** → Block restrictions use plugin IDs like `system_main_block` or `inline_block:article`, not entity types
- **Mixing section and component types** → Section styles only appear on layout config forms, component styles only on block config forms
- **Forgetting inline_block prefix** → Custom block types need `inline_block:` prefix. `article` won't work, use `inline_block:article`
- **Too many classes on one style** → `classes: 'p-1 p-md-2 p-lg-3 p-xl-4 bg-primary text-white shadow rounded border'` overwhelming. Split into multiple styles in different groups
- **Not namespacing custom classes** → `classes: 'highlight'` conflicts with other modules. Use `classes: 'lb-highlight'` or `mytheme-highlight`
- **Using !important in CSS** → Specificity wars make debugging painful. Use proper selector specificity instead
- **Forgetting weight** → Styles appear in random order within groups. Set weight to control order

### See Also

- Section 11.1: Style Groups (creating groups first)
- Section 11.3: Bootstrap Integration (using framework classes)
- Section 6: Block Placement (understanding block plugin IDs)
- Section 5: Core Layout Plugins (layout plugin IDs for restrictions)
- Reference: `modules/contrib/layout_builder_styles/src/Form/LayoutBuilderStyleForm.php`
