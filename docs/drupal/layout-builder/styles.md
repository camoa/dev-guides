---
description: Adding CSS classes to sections and blocks
drupal_version: "11.x"
---

# Layout Builder Styles

### When to Use

When you need to apply CSS classes or styling options to sections, components (blocks), or regions in Layout Builder without custom code for each option.

### Steps

1. **Install Layout Builder Styles**
   ```bash
   composer require drupal/layout_builder_styles
   drush en layout_builder_styles
   ```

2. **Create Style Configuration**
   - Navigate to Configuration → Content authoring → Layout Builder Styles
   - Click "Add style"
   - Configure:
     - Label (shown to editors)
     - CSS classes (applied to markup)
     - Type: Section, Component, or Region
     - Optionally restrict to specific layouts

3. **Via Configuration Export**
   ```yaml
   # layout_builder_styles.style.background_blue.yml
   uuid: abc-123
   langcode: en
   status: true
   dependencies: {  }
   id: background_blue
   label: 'Blue Background'
   classes: 'bg-blue text-white'
   type: section  # or component, region
   ```

4. **Apply in Layout Builder UI**
   - Edit layout
   - Configure section or block
   - Select style from "Style" dropdown
   - Save

5. **Result in Config**
   ```yaml
   # Section with LB Styles applied
   - layout_id: layout_onecol
     layout_settings: {  }
     components: []
     third_party_settings:
       layout_builder_styles:
         style:
           section_wrapper: background_blue
   ```

### Decision Points

| At this point... | If... | Then... |
|---|---|---|
| Choosing type | Need section backgrounds, margins | Use "section" type style |
| Choosing type | Need block-level spacing, borders | Use "component" type style |
| Choosing type | Need column-specific styling | Use "region" type style (experimental) |
| Creating classes | Using Bootstrap or design system | Match classes to existing framework classes |
| Creating classes | Custom theme | Define corresponding CSS in theme stylesheet |
| Restricting styles | Style only makes sense for certain layouts | Restrict style to specific layout plugin IDs |

### Common Mistakes

- **Not defining CSS** → Layout Builder Styles applies classes, doesn't provide CSS. Must define styles in theme
- **Too many options** → Creating 50 styles overwhelms editors. Create curated set matching design system
- **Mixing concerns** → Don't use styles for structural layout (columns, grids). Use layout plugins for structure, styles for aesthetics
- **Forgetting responsive** → Classes like `bg-blue` need responsive considerations. Define mobile-first CSS
- **Not namespacing classes** → Generic class names like `blue` conflict with other modules. Use prefixed classes like `lb-bg-blue`
- **Skipping labels** → Editor-facing labels should be descriptive: "Blue Background" not "bg-blue"
- **Using !important in style CSS** → Leads to specificity wars. Use proper selector specificity instead

### See Also

- Section 15: Theming Layout Builder (implementing style CSS)
- Section 16: Best Practices (curating style options)
- Reference: [Layout Builder Styles module](https://www.drupal.org/project/layout_builder_styles)
- Reference: [Layout Builder Styles documentation](https://www.drupal.org/docs/contributed-modules/layout-builder-styles)
