## 25. Custom Display Plugin

### When to Use
New output channel beyond Page/Block/REST: CLI output, email rendering, queue processing, specialized API formats.

### Steps

1. **Create display plugin** — In `src/Plugin/views/display/MyCustomDisplay.php`
   ```php
   namespace Drupal\mymodule\Plugin\views\display;

   use Drupal\views\Plugin\views\display\DisplayPluginBase;
   use Drupal\views\Attribute\ViewsDisplay;

   #[ViewsDisplay(
     id: "my_custom_display",
     title: "Custom Display",
     admin: "Custom",
     help: "Custom display type description",
   )]
   class MyCustomDisplay extends DisplayPluginBase {
     public function execute() {
       return $this->view->render();
     }
   }
   ```

2. **Define display options** — Add display-specific settings
   ```php
   protected function defineOptions() {
     $options = parent::defineOptions();
     $options['custom_setting'] = ['default' => ''];
     return $options;
   }

   public function optionsSummary(&$categories, &$options) {
     parent::optionsSummary($categories, $options);
     $options['custom_setting'] = [
       'category' => 'other',
       'title' => t('Custom setting'),
       'value' => $this->options['custom_setting'],
     ];
   }
   ```

3. **Implement rendering** — Override render or preview
   ```php
   public function render() {
     $this->view->execute($this->display['id']);
     $output = [];
     foreach ($this->view->result as $row) {
       $output[] = $this->view->rowPlugin->render($row);
     }
     return ['#markup' => implode("\n", $output)];
   }
   ```

4. **Route integration (optional)** — For URL-accessible displays
   ```php
   public function execute() {
     $response = new Response();
     $response->setContent($this->render());
     return $response;
   }
   ```

### Decision Points
| At this step... | If... | Then... |
|---|---|---|
| Rendering | Needs custom output format | Override render() to control final output structure |
| Routing | Display has URL | Define route in mymodule.routing.yml referencing display |
| Options | Display-specific settings | Override defineOptions() and optionsSummary() |
| Preview | Admin preview needed | Override preview() to return admin-viewable output |

### Common Mistakes
- Not calling $this->view->execute() → Results won't populate; always execute before rendering
- Returning wrong type from execute() → Page displays return render array, REST returns Response object
- Missing route definition → URL-based displays need routing.yml entry pointing to view
- Not extending correct base → Extend DisplayPluginBase, not PluginBase
- Forgetting usesXxx properties → Set $usesAJAX, $usesAttachments, $usesOptions based on display capabilities

### See Also
- Section 4-7: Display types configuration
- Reference: `core/modules/views/src/Plugin/views/display/DisplayPluginBase.php`
- Reference: `core/modules/rest/src/Plugin/views/display/RestExport.php` — REST display example

