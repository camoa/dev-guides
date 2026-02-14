---
description: Theming Layout Builder admin UI and frontend
drupal_version: "11.x"
---

# Theming Layout Builder

### When to Use

When styling Layout Builder admin UI, layout frontend output, or section/component markup.

### Steps

1. **Theming Layout Templates**
   ```twig
   {# Override core layout template in theme #}
   {# templates/layout/layout--twocol-section.html.twig #}

   <div{{ attributes.addClass('layout-twocol-section') }}>
     {% if content.first %}
       <div class="layout-region layout-region--first">
         {{ content.first }}
       </div>
     {% endif %}
     {% if content.second %}
       <div class="layout-region layout-region--second">
         {{ content.second }}
       </div>
     {% endif %}
   </div>
   ```

2. **Styling Layout Output**
   ```scss
   // Use Bootstrap grid for layout structure
   .layout-twocol-section {
     @include make-row();

     .layout-region--first {
       @include make-col-ready();
       @include make-col(8);
     }

     .layout-region--second {
       @include make-col-ready();
       @include make-col(4);
     }
   }
   ```

3. **Theming Admin UI**
   ```css
   /* Hide Layout Builder UI elements for cleaner admin */
   .layout-builder__add-block,
   .layout-builder__add-section {
     /* Style add block/section buttons */
   }

   .layout-builder-block {
     /* Style block wrappers in admin */
   }
   ```

4. **Template Suggestions**
   ```php
   function mytheme_theme_suggestions_layout_alter(array &$suggestions, array $variables) {
     // Add suggestion based on layout ID
     $layout = $variables['layout'];
     $layout_id = $layout->getPluginId();
     $suggestions[] = 'layout__' . $layout_id;

     // Add suggestion for specific entity bundle
     if (isset($variables['content']['#entity'])) {
       $entity = $variables['content']['#entity'];
       $suggestions[] = 'layout__' . $layout_id . '__' . $entity->bundle();
     }

     return $suggestions;
   }
   ```

5. **Preprocessing**
   ```php
   function mytheme_preprocess_layout(&$variables) {
     // Add custom classes based on layout settings
     if (isset($variables['settings']['column_widths'])) {
       $widths = $variables['settings']['column_widths'];
       $variables['attributes']['class'][] = 'layout-widths--' . str_replace('-', '_', $widths);
     }

     // Add custom variables
     $variables['layout_id'] = $variables['layout']->getPluginId();
   }
   ```

6. **Attaching Libraries**
   ```php
   function mytheme_preprocess_layout__twocol_section(&$variables) {
     $variables['#attached']['library'][] = 'mytheme/twocol_layout';
   }
   ```

### Decision Points

| At this point... | If... | Then... |
|---|---|---|
| Choosing template location | Overriding core layout | Place in `templates/layout/` with same name as core template |
| Choosing template location | Custom layout | Define template in layouts.yml and place in specified path |
| Styling approach | Using Bootstrap or framework | Use framework grid classes in layout template |
| Styling approach | Custom CSS | Define semantic classes, style in theme stylesheet |
| Admin vs frontend | Different styles for each | Use `.layout-builder-form` parent selector for admin-only styles |
| Library attachment | Layout-specific CSS/JS | Attach in layout plugin definition or preprocess |

### Common Mistakes

- **Not using `attributes.addClass()`** → Hardcoding classes prevents contrib modules from altering. Use `attributes` variable
- **Forgetting mobile-first** → Layout CSS should be responsive. Desktop-first layouts break on mobile
- **Styling without checking empty** → Use `{% if content.region %}` before outputting region markup to avoid empty divs
- **Over-nesting in templates** → Keep layout templates focused on structure. Block theming handles block markup
- **Not namespacing classes** → Generic classes like `.first` conflict. Use `.layout-region--first` or similar
- **Ignoring cache in preprocess** → Preprocessing runs on every render. Don't do expensive operations without caching
- **Not providing template suggestions** → Make layouts themeable per entity bundle or context with suggestions

### See Also

- Section 11: Layout Builder Styles (applying CSS classes via UI)
- Section 12: Custom Layout Plugins (creating layouts with templates)
- Reference: `/core/modules/layout_builder/templates/layout.html.twig`
- Reference: Core theme templates in `/core/themes/*/templates/layout/`
