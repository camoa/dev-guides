## 26. Custom Style & Row Plugins

### When to Use
**Style Plugin**: Custom result set formatting (calendar, timeline, accordion) that standard Table/Grid/List can't achieve.
**Row Plugin**: Custom per-row rendering (entity cards, custom templates) reusable across multiple views.

### Style Plugin Steps

1. **Create style plugin** — In `src/Plugin/views/style/MyCustomStyle.php`
   ```php
   namespace Drupal\mymodule\Plugin\views\style;

   use Drupal\views\Plugin\views\style\StylePluginBase;
   use Drupal\views\Attribute\ViewsStyle;

   #[ViewsStyle(
     id: "my_custom_style",
     title: "Custom Style",
     help: "Renders results in custom format",
     theme: "views_view_my_custom",
     display_types: ["normal"],
   )]
   class MyCustomStyle extends StylePluginBase {
     protected $usesRowPlugin = TRUE;
     protected $usesFields = FALSE;
   }
   ```

2. **Create theme template** — In `templates/views-view-my-custom.html.twig`
   ```twig
   <div class="custom-view-wrapper">
     {% for row in rows %}
       <div class="custom-row">{{ row.content }}</div>
     {% endfor %}
   </div>
   ```

3. **Implement hook_theme()** — Register template
   ```php
   function mymodule_theme() {
     return [
       'views_view_my_custom' => [
         'variables' => ['view' => NULL, 'rows' => []],
       ],
     ];
   }
   ```

### Row Plugin Steps

1. **Create row plugin** — In `src/Plugin/views/row/MyCustomRow.php`
   ```php
   namespace Drupal\mymodule\Plugin\views\row;

   use Drupal\views\Plugin\views\row\RowPluginBase;
   use Drupal\views\Attribute\ViewsRow;

   #[ViewsRow(
     id: "my_custom_row",
     title: "Custom Row",
     help: "Renders each row with custom template",
   )]
   class MyCustomRow extends RowPluginBase {
     public function render($row) {
       return [
         '#theme' => 'views_row_my_custom',
         '#row' => $row,
         '#view' => $this->view,
       ];
     }
   }
   ```

### Decision Points
| At this step... | If... | Then... |
|---|---|---|
| usesRowPlugin | Style formats entire set (calendar) | Set $usesRowPlugin = FALSE |
| usesRowPlugin | Style delegates per-row rendering | Set $usesRowPlugin = TRUE |
| usesFields | Style accesses individual fields | Set $usesFields = TRUE |
| template | Complex markup needed | Use Twig template; simple markup can return render array from render() |

### Common Mistakes
- Style plugin rendering rows directly when usesRowPlugin = TRUE → Let row plugin handle rows; style just wraps them
- Not registering theme in hook_theme() → Template won't be discovered
- Wrong variables in template → Check theme registry; pass expected variables in render()
- Missing display_types in attribute → Style won't appear for certain display types
- Not preprocessing variables → Use hook_preprocess_views_view_my_custom() for complex data prep

### See Also
- Section 15: Style & Row Plugins — configuration approach
- Reference: `core/modules/views/src/Plugin/views/style/StylePluginBase.php`
- Reference: `core/modules/views/src/Plugin/views/style/Table.php` — usesFields = TRUE example
- Reference: `core/modules/views/src/Plugin/views/row/EntityRow.php` — entity row plugin

