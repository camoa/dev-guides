---
description: Drupal development best practices for extending, theming, and testing Klaro
drupal_version: "11.x"
---

# Development Standards

## When to Use

> Follow Drupal and Klaro development best practices when extending, theming, or integrating Klaro into custom code.

## Decision

| Development Task | Standard | Why |
|---|---|---|
| Add custom service programmatically | Use Configuration API | Exportable, version-controllable, translatable |
| Modify Klaro behavior | Use event subscribers | Proper Drupal architecture; avoid hacks |
| Theme consent modal | Override CSS variables first | Maintains upgradeability; avoids conflicts |
| Test consent flow | Automated browser testing | Regression prevention; compliance verification |
| Deploy configuration | Use config export/import | Consistent across environments |

## Pattern

**Programmatic Service Creation** (use Configuration API):

```php
// In custom module or update hook
use Drupal\klaro\Entity\KlaroService;

$service = KlaroService::create([
  'id' => 'custom_analytics',
  'label' => 'Custom Analytics',
  'description' => 'Our custom analytics implementation',
  'status' => TRUE,
  'purposes' => ['statistics'],
  'required' => FALSE,
  'toggled_by_default' => FALSE,
  'sources' => ['https://analytics.example.com/tracker.js'],
  'cookies' => ['_custom_analytics'],
]);
$service->save();
```

**Event Subscriber** (modify Klaro behavior):
```php
// src/EventSubscriber/KlaroAlterSubscriber.php
namespace Drupal\my_module\EventSubscriber;

use Symfony\Component\EventDispatcher\EventSubscriberInterface;
use Drupal\klaro\Event\KlaroConfigAlterEvent;

class KlaroAlterSubscriber implements EventSubscriberInterface {

  public static function getSubscribedEvents() {
    return [
      KlaroConfigAlterEvent::EVENT_NAME => 'alterKlaroConfig',
    ];
  }

  public function alterKlaroConfig(KlaroConfigAlterEvent $event) {
    $config = $event->getConfig();
    // Modify config array
    $event->setConfig($config);
  }
}
```

**Configuration Export Workflow**:
```bash
# Export Klaro configuration
drush config:export

# Files exported:
# - klaro.settings.yml (main settings)
# - klaro.service.*.yml (each service)
# - klaro.purpose.*.yml (each purpose)

# Import on other environment
drush config:import
```

**Automated Testing**:
```php
// tests/src/FunctionalJavascript/KlaroConsentTest.php
namespace Drupal\Tests\my_module\FunctionalJavascript;

use Drupal\FunctionalJavascriptTests\WebDriverTestBase;

class KlaroConsentTest extends WebDriverTestBase {

  public function testConsentFlow() {
    $this->drupalGet('<front>');

    // Verify modal appears
    $this->assertSession()->waitForElement('css', '#klaro');

    // Click accept
    $this->click('.cm-btn-accept-all');

    // Verify cookie set
    $this->assertTrue($this->getCookie('klaro'));
  }
}
```

**Reference**: `/modules/contrib/klaro/src/Entity/` for entity definitions

## Common Mistakes

- **Wrong**: Creating services via UI only → **Right**: Not version-controlled; use config export
- **Wrong**: Directly modifying klaro.js library → **Right**: Lost on updates; use event subscribers/CSS overrides
- **Wrong**: Hard-coding service configuration → **Right**: Not translatable; use Configuration API
- **Wrong**: Skipping automated testing → **Right**: Consent flow breaks unnoticed; test critical paths
- **Wrong**: Not exporting configuration → **Right**: Dev/staging/prod configs drift; export and commit
- **Wrong**: Using hook_preprocess instead of events → **Right**: Not Klaro-specific; use proper event subscribers
- **Wrong**: Inline JavaScript modifications → **Right**: Maintenance nightmare; use proper API/events

## See Also

- Reference: [Configuration API](https://www.drupal.org/docs/drupal-apis/configuration-api)
- Testing: [FunctionalJavascript Tests](https://www.drupal.org/docs/testing/javascript-testing-using-nightwatch)
