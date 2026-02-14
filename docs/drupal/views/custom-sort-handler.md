---
description: Custom sort logic: computed fields, weighted sorting, multi-column sorts, integration with external ranking systems.
drupal_version: "11.x"
---

## 22. Custom Sort Handler

### When to Use
Custom sort logic: computed fields, weighted sorting, multi-column sorts, integration with external ranking systems.

### Steps

1. **Create sort plugin** — In `src/Plugin/views/sort/MyCustomSort.php`
   ```php
   namespace Drupal\mymodule\Plugin\views\sort;

   use Drupal\views\Plugin\views\sort\SortPluginBase;
   use Drupal\views\Attribute\ViewsSort;

   #[ViewsSort("my_custom_sort")]
   class MyCustomSort extends SortPluginBase {
     public function query() {
       $this->ensureMyTable();
       $this->query->addOrderBy(
         $this->tableAlias,
         $this->realField,
         $this->options['order']
       );
     }
   }
   ```

2. **Multi-field sort** — Add multiple ORDER BY clauses
   ```php
   public function query() {
     $this->ensureMyTable();
     // Sort by status first, then title
     $this->query->addOrderBy($this->tableAlias, 'status', 'DESC');
     $this->query->addOrderBy($this->tableAlias, 'title', $this->options['order']);
   }
   ```

3. **Computed sort** — Use SQL expressions
   ```php
   public function query() {
     $formula = "LENGTH($this->tableAlias.$this->realField)";
     $this->query->addOrderBy(NULL, $formula, $this->options['order'], $this->tableAlias . '_length');
   }
   ```

4. **Integrate with hook_views_data()**
   ```php
   function mymodule_views_data() {
     $data['node_field_data']['custom_weighted_sort'] = [
       'title' => t('Weighted sort'),
       'sort' => ['id' => 'my_custom_sort'],
     ];
     return $data;
   }
   ```

### Decision Points
| At this step... | If... | Then... |
|---|---|---|
| query() | Sorting by DB field | Use addOrderBy($table, $field, $order) |
| query() | Sorting by formula | Pass NULL as table, formula as field |
| query() | Multi-column sort | Call addOrderBy() multiple times in desired order |
| options form | User-configurable sort | Override defineOptions() and buildOptionsForm() |

### Common Mistakes
- Wrong ORDER BY sequence → Last addOrderBy() call is highest priority; add primary sort last
- Missing alias parameter in formula sorts → Fourth parameter required for SQL expression sorts
- Not respecting $this->options['order'] → User's ASC/DESC choice should be honored
- Sorting by unindexed columns → Performance disaster on large datasets; ensure DB indexes exist
- Overriding parent::query() → Call parent::query() or reimplement ensureMyTable() logic

### See Also
- Section 10: Sort & Contextual Filters — configuration approach
- Reference: `core/modules/views/src/Plugin/views/sort/SortPluginBase.php`
- Reference: `core/modules/views/src/Plugin/views/sort/Random.php` — formula-based sort example
