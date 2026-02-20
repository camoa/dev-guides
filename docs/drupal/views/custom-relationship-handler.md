## 24. Custom Relationship Handler

### When to Use
Complex JOIN logic beyond standard entity reference relationships: multi-column joins, conditional joins, subquery-based relationships.

### Steps

1. **Create relationship plugin** — In `src/Plugin/views/relationship/MyCustomRelationship.php`
   ```php
   namespace Drupal\mymodule\Plugin\views\relationship;

   use Drupal\views\Plugin\views\relationship\RelationshipPluginBase;
   use Drupal\views\Attribute\ViewsRelationship;

   #[ViewsRelationship("my_custom_relationship")]
   class MyCustomRelationship extends RelationshipPluginBase {
     public function query() {
       $this->ensureMyTable();
       $join = Views::pluginManager('join')->createInstance('standard', [
         'table' => 'custom_table',
         'field' => 'custom_id',
         'left_table' => $this->tableAlias,
         'left_field' => 'nid',
         'type' => 'LEFT',
       ]);
       $this->alias = $this->query->addRelationship($this->tableAlias, $join, 'custom_table', $this->relationship);
     }
   }
   ```

2. **Conditional JOIN** — Add WHERE clause to JOIN
   ```php
   public function query() {
     $join = Views::pluginManager('join')->createInstance('standard', [
       'table' => 'custom_table',
       'field' => 'entity_id',
       'left_table' => $this->tableAlias,
       'left_field' => 'nid',
       'extra' => [
         ['field' => 'entity_type', 'value' => 'node'],
         ['field' => 'status', 'value' => 1],
       ],
     ]);
     $this->alias = $this->query->addRelationship('custom_table', $join, 'custom_table');
   }
   ```

3. **Integrate with hook_views_data()** — Define relationship
   ```php
   function mymodule_views_data() {
     $data['node_field_data']['custom_rel'] = [
       'title' => t('Custom related data'),
       'relationship' => [
         'id' => 'my_custom_relationship',
         'base' => 'custom_table',
         'base field' => 'entity_id',
         'label' => t('Custom data'),
       ],
     ];
     return $data;
   }
   ```

### Decision Points
| At this step... | If... | Then... |
|---|---|---|
| JOIN type | May not match all rows | Use 'LEFT' join to avoid filtering results |
| JOIN type | Must match to show results | Use 'INNER' join to require relationship |
| Conditional JOIN | Need WHERE on joined table | Use 'extra' array in join definition |
| Multiple conditions | Complex join logic | Extend 'extra' array with multiple field/value pairs |

### Common Mistakes
- Wrong join type → INNER joins filter results; use LEFT unless relationship is required
- Forgetting to set $this->alias → Fields/filters on relationship need the alias to reference correct table
- Not defining 'base' in views_data → Views needs to know target table for relationship
- Missing relationship chain support → If relationship depends on another, check $this->relationship and pass to addRelationship()
- Hardcoded table names → Use $this->tableAlias for source table, not 'node_field_data'

### See Also
- Section 11: Relationships — configuration approach
- Reference: `core/modules/views/src/Plugin/views/relationship/RelationshipPluginBase.php`
- Reference: `core/modules/comment/src/Plugin/views/relationship/NodeRevisionComment.php` — complex relationship example

