---
description: When you need custom field output: computed values, external API data, complex formatting that can't be achieved with field templates or rewrite ru...
drupal_version: "11.x"
---

## 20. Custom Field Handler

### When to Use
When you need custom field output: computed values, external API data, complex formatting that can't be achieved with field templates or rewrite rules.

### Steps

1. **Create handler class** — Place in `src/Plugin/views/field/MyCustomField.php`
   ```php
   namespace Drupal\mymodule\Plugin\views\field;

   use Drupal\views\Plugin\views\field\FieldPluginBase;
   use Drupal\views\Attribute\ViewsField;
   use Drupal\views\ResultRow;

   #[ViewsField("my_custom_field")]
   class MyCustomField extends FieldPluginBase {
     public function render(ResultRow $values) {
       $value = $this->getValue($values);
       return ['#markup' => strtoupper($value)];
     }
   }
   ```

2. **Integrate with hook_views_data()** — In `mymodule.views.inc`
   ```php
   function mymodule_views_data() {
     $data['node_field_data']['custom_title_upper'] = [
       'title' => t('Title (Uppercase)'),
       'field' => ['id' => 'my_custom_field'],
     ];
     return $data;
   }
   ```

3. **Add options form (optional)** — For configurable fields
   ```php
   protected function defineOptions() {
     $options = parent::defineOptions();
     $options['prefix'] = ['default' => ''];
     return $options;
   }

   public function buildOptionsForm(&$form, FormStateInterface $form_state) {
     $form['prefix'] = [
       '#type' => 'textfield',
       '#title' => t('Prefix'),
       '#default_value' => $this->options['prefix'],
     ];
     parent::buildOptionsForm($form, $form_state);
   }
   ```

4. **Implement query() for computed fields** — Add fields to query
   ```php
   public function query() {
     $this->ensureMyTable();
     $this->addAdditionalFields(['title', 'status']);
   }
   ```

### Decision Points
| At this step... | If... | Then... |
|---|---|---|
| render() | Returning HTML | Use render array with #markup, never raw strings |
| query() | Field pulls from DB | Call ensureMyTable() and addAdditionalFields() |
| query() | Field is purely computed | Skip query() — no DB fields needed |
| options form | Field needs config | Override defineOptions() and buildOptionsForm() |

### Common Mistakes
- Returning string from render() → Return render array; Views expects renderable output
- Not calling ensureMyTable() in query() → Table may not be joined, query fails
- Putting business logic in render() → Keep render() light; extract complex logic to services injected via create()
- Not sanitizing output → Use #markup with trusted content or #plain_text for user input
- Forgetting getValue($values) → Access row data via getValue(), not direct property access

### See Also
- Section 29: Views Data Integration — registering fields in hook_views_data()
- Reference: `core/modules/views/src/Plugin/views/field/FieldPluginBase.php`
- Reference: `core/modules/node/src/Plugin/views/field/Node.php` — real-world example
