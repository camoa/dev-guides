---
description: Creating custom layout plugins for Layout Builder — layouts.yml, Twig templates, libraries, and registration.
---

## 12. Custom Layout Plugins

### When to Use

When core layouts don't provide the regions or structure you need, or when you want theme-specific layouts.

### Steps

1. **Create `THEME_NAME.layouts.yml`** in theme root
   ```yaml
   # mytheme.layouts.yml
   custom_hero:
     label: 'Hero Layout'
     category: 'Custom'
     template: layout--custom-hero
     library: mytheme/custom_hero_layout
     default_region: content
     icon_map:
       - [hero]
       - [content]
     regions:
       hero:
         label: 'Hero Region'
       content:
         label: 'Content Region'
   ```

2. **Create Twig template** in `templates/layout/`
   ```twig
   {# templates/layout/layout--custom-hero.html.twig #}
   <div{{ attributes.addClass('custom-hero-layout') }}>
     {% if content.hero %}
       <div class="hero-region">
         {{ content.hero }}
       </div>
     {% endif %}
     {% if content.content %}
       <div class="content-region">
         {{ content.content }}
       </div>
     {% endif %}
   </div>
   ```

3. **Define library** in `THEME_NAME.libraries.yml`
   ```yaml
   custom_hero_layout:
     css:
       theme:
         css/layouts/custom-hero.css: {}
   ```

4. **Create stylesheet**
   ```css
   /* css/layouts/custom-hero.css */
   .custom-hero-layout .hero-region {
     min-height: 400px;
     display: flex;
     align-items: center;
     justify-content: center;
   }
   ```

5. **Clear cache**
   ```bash
   drush cr
   ```

6. **Result**: Layout available in Layout Builder layout selection

### Decision Points

| At this point... | If... | Then... |
|---|---|---|
| Choosing template name | Following Drupal conventions | Use `layout--{layout_id}.html.twig` pattern |
| Defining regions | Complex structure | More regions better than nested markup in template |
| Using icon_map | Want accurate admin UI preview | Map icon cells to regions showing visual layout structure |
| Defining library | Layout needs CSS | Always attach library with layout-specific CSS |
| Choosing default_region | Layout has primary content area | Set most common region as default for easier block placement |
| Module vs Theme | Layout for reusable distribution | Put in module with `MODULE.layouts.yml` |
| Module vs Theme | Layout specific to this site | Put in theme with `THEME.layouts.yml` |

### Common Mistakes

- **Wrong template location** → Must be in `templates/layout/` directory or specify `path` in layouts.yml
- **Forgetting to clear cache** → Layout discovery cached. New/changed layouts don't appear until cache rebuild
- **Not providing icon_map** → Admin UI shows generic grid. Provide icon_map for better visual representation
- **Hardcoding layout classes** → Use `attributes.addClass()` in template so contrib modules can alter classes
- **Not checking for empty regions** → Use `{% if content.region %}` to avoid rendering empty region markup
- **Missing library attachment** → Layout-specific CSS won't load without library defined and attached
- **Inconsistent layout ID naming** → Follow core convention: use underscores (`custom_hero`) matching core patterns like `layout_twocol_section`, `layout_onecol`
- **Not providing category** → Layouts without category appear in "Unknown" group. Provide category for organization

### See Also

- Section 5: Core Layout Plugins (examples to reference)
- Section 15: Theming Layout Builder (styling layouts)
- Reference: `/core/lib/Drupal/Core/Layout/LayoutDefault.php` (base class)
- Reference: [How to register layouts](https://www.drupal.org/docs/drupal-apis/layout-api/how-to-register-layouts)
