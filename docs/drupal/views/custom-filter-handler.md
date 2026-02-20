## 21. Custom Filter Handler

### When to Use
When standard filter operators aren't sufficient: custom logic, complex conditions, integration with external validation, multi-field filters.

### Steps

1. **Create filter plugin** — In `src/Plugin/views/filter/MyCustomFilter.php`
   ```php
   namespace Drupal\mymodule\Plugin\views\filter;

   use Drupal\views\Plugin\views\filter\FilterPluginBase;
   use Drupal\views\Attribute\ViewsFilter;

   #[ViewsFilter("my_custom_filter")]
   class MyCustomFilter extends FilterPluginBase {
     protected function defineOptions() {
       $options = parent::defineOptions();
       $options['value'] = ['default' => ''];
       return $options;
     }

     public function query() {
       $this->ensureMyTable();
       $this->query->addWhere($this->options['group'],
         "$this->tableAlias.$this->realField",
         $this->value,
         'LIKE'
       );
     }
   }
   ```

2. **Build value form for exposed filters** — Override valueForm()
   ```php
   protected function valueForm(&$form, FormStateInterface $form_state) {
     $form['value'] = [
       '#type' => 'textfield',
       '#title' => t('Filter value'),
       '#default_value' => $this->value,
     ];
   }
   ```

3. **Define operators (optional)** — For multiple filter operations
   ```php
   protected function operators() {
     return [
       'contains' => ['title' => t('Contains'), 'method' => 'opContains'],
       'starts' => ['title' => t('Starts with'), 'method' => 'opStarts'],
     ];
   }

   protected function opContains($field) {
     $this->query->addWhere($this->options['group'], $field, '%' . $this->value . '%', 'LIKE');
   }
   ```

4. **Integrate with hook_views_data()**
   ```php
   function mymodule_views_data_alter(&$data) {
     $data['node_field_data']['title']['filter']['id'] = 'my_custom_filter';
   }
   ```

### Decision Points
| At this step... | If... | Then... |
|---|---|---|
| query() | Simple single-value filter | Use addWhere() directly |
| query() | Multi-value filter (OR conditions) | Use condition group: $this->query->getConnection()->condition('OR') |
| valueForm() | Exposed filter | Check $form_state->get('exposed') and adjust UI accordingly |
| operators() | Multiple operator types needed | Define operators() and create method per operator |

### Common Mistakes
- Not escaping user input in query() → Use query placeholders; Views handles this via addWhere() — never concatenate strings
- Missing $this->ensureMyTable() → Filter may target wrong table alias
- Not implementing adminSummary() → Filter shows no info in Views UI summary area
- Forgetting expose options → Override defaultExposeOptions() to set exposure defaults
- Using wrong operator in addWhere() → '=' for exact, 'LIKE' for patterns, 'IN' for arrays

### See Also
- Section 9: Filters & Exposed Filters — configuration approach
- Reference: `core/modules/views/src/Plugin/views/filter/FilterPluginBase.php`
- Reference: `core/modules/views/src/Plugin/views/filter/BooleanOperator.php` — simple filter example
- Reference: `core/modules/taxonomy/src/Plugin/views/filter/TaxonomyIndexTid.php` — complex filter with DI

