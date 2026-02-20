## 23. Custom Argument Handler (Contextual Filter)

### When to Use
URL-based filtering with custom logic: argument validation, default values, custom summary views, title overrides.

### Steps

1. **Create argument plugin** — In `src/Plugin/views/argument/MyCustomArgument.php`
   ```php
   namespace Drupal\mymodule\Plugin\views\argument;

   use Drupal\views\Plugin\views\argument\ArgumentPluginBase;
   use Drupal\views\Attribute\ViewsArgument;

   #[ViewsArgument("my_custom_argument")]
   class MyCustomArgument extends ArgumentPluginBase {
     public function query($group_by = FALSE) {
       $this->ensureMyTable();
       $this->query->addWhere(0, "$this->tableAlias.$this->realField", $this->argument);
     }
   }
   ```

2. **Add validation** — Validate argument value
   ```php
   public function validateArgument($arg) {
     // Only accept numeric IDs
     if (!is_numeric($arg)) {
       return FALSE;
     }
     $this->argument = $arg;
     return TRUE;
   }
   ```

3. **Set default value** — When argument missing from URL
   ```php
   protected function defineOptions() {
     $options = parent::defineOptions();
     $options['default_argument_type'] = ['default' => 'fixed'];
     $options['default_argument_options'] = ['default' => []];
     return $options;
   }

   public function getDefaultArgument($raw = FALSE) {
     return \Drupal::currentUser()->id();
   }
   ```

4. **Override title** — Dynamic view title based on argument
   ```php
   public function title() {
     $node = \Drupal::entityTypeManager()->getStorage('node')->load($this->argument);
     return $node ? $node->getTitle() : t('Unknown');
   }
   ```

### Decision Points
| At this step... | If... | Then... |
|---|---|---|
| query() | Simple WHERE condition | Use addWhere() with $this->argument |
| query() | Multiple values (e.g., 1+2+3) | Override defaultActions() to handle breakValue() |
| validateArgument() | Strict validation needed | Return FALSE for invalid args, triggers "no results" behavior |
| title() | View title should reflect argument | Override title() to load entity and return label |

### Common Mistakes
- Not storing validated value in $this->argument → query() uses $this->argument, must be set in validateArgument()
- Forgetting to handle missing argument → Define default_argument_type or exception_value behavior
- Loading full entities in query() → Contextual filters run on every view execution; keep query() fast
- Not supporting multiple values → Override breakValue() and update query() to handle arrays if '+' separation desired
- Missing summary view support → If argument can enumerate values, override summaryQuery()

### See Also
- Section 10: Sort & Contextual Filters — configuration approach
- Reference: `core/modules/views/src/Plugin/views/argument/ArgumentPluginBase.php`
- Reference: `core/modules/node/src/Plugin/views/argument/Nid.php` — numeric argument example
- Reference: `core/modules/user/src/Plugin/views/argument/Uid.php` — entity argument example

