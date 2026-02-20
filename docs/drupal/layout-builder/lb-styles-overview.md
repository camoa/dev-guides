## 11. Layout Builder Styles Overview

### When to Use

When you need to apply CSS classes to Layout Builder sections (layouts) or components (blocks) without creating custom plugins. Layout Builder Styles provides a config entity system for defining reusable style options that editors select in the Layout Builder UI.

### Decision

| If you need... | Use... | Why |
|---|---|---|
| Section-level styling (backgrounds, spacing, containers) | Section styles | Applied to layout wrapper, affects entire section |
| Block-level styling (borders, shadows, alignment) | Component styles | Applied to individual block wrappers |
| Curated style options for editors | Style groups with restrictions | Organize related styles, control which blocks/layouts can use them |
| Design system integration | Bootstrap class mapping | Map style IDs to framework utility classes |
| Custom styling logic | Event subscriber on `SECTION_COMPONENT_BUILD_RENDER_ARRAY` | Programmatically alter styles before render |

### Pattern

**Installation & Setup:**
```bash
composer require drupal/layout_builder_styles:^2.1
drush en layout_builder_styles
```

**Config Entity Architecture:**
- `LayoutBuilderStyle` — individual style (CSS classes + restrictions)
- `LayoutBuilderStyleGroup` — groups styles (e.g., "Padding", "Color Scheme")

**Applied Styles in Config:**
```yaml
# Section with style applied
sections:
  - layout_id: layout_onecol
    layout_settings:
      layout_builder_styles_style:
        - padding_large
        - bg_primary
    components: []

# Block with style applied
components:
  - uuid: abc-123
    configuration:
      layout_builder_styles_style:
        - shadow_medium
        - rounded_corners
```

**Rendering Flow:**
1. Editor selects styles in Layout Builder UI
2. Styles stored in section/component config
3. `BlockComponentRenderArraySubscriber` event subscriber applies CSS classes
4. `layout_builder_styles_preprocess_layout()` applies section classes
5. Template suggestions added: `block__STYLE_ID`, `block__EXISTING__STYLE_ID`

Reference: `modules/contrib/layout_builder_styles/src/Entity/LayoutBuilderStyle.php`

### Common Mistakes

- **Creating styles before groups** → Must create at least one style group before creating styles. Groups organize styles in the UI
- **Confusing types** → "section" applies to layout wrappers, "component" applies to block wrappers. Cannot apply section style to block
- **Not defining CSS** → LB Styles only applies CSS classes. You must define the actual CSS in your theme
- **Too many ungrouped styles** → Without groups, all styles appear in one dropdown. Use groups to organize (Spacing, Colors, Effects)
- **Forgetting to clear cache** → Style config changes require cache clear to appear in Layout Builder UI
- **Using region type** → Region styles are experimental and not widely supported. Stick to section and component types

### See Also

- Section 11.1: Style Groups Config (creating groups)
- Section 11.2: Style Definitions (creating individual styles)
- Section 11.3: Bootstrap Integration (mapping to framework classes)
- Section 11.4: Extending LB Styles (programmatic alterations)
- Reference: [Layout Builder Styles module](https://www.drupal.org/project/layout_builder_styles)
- Reference: [Layout Builder Styles documentation](https://www.drupal.org/docs/contributed-modules/layout-builder-styles)
