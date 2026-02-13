---
description: Inject services into forms using dependency injection pattern
drupal_version: "11.x"
---

# Dependency Injection

## When to Use

> Use dependency injection when forms need services (config factory, entity type manager, database, custom services).

## Decision

| Situation | Choose | Why |
|-----------|--------|-----|
| Config factory only | FormBase::config() or $this->configFactory() | Already injected in FormBase |
| Multiple services | create() + __construct() | Proper DI pattern, testable |
| Entity queries | EntityTypeManagerInterface | Don't use \Drupal::entityTypeManager() |
| Database queries | Connection (database service) | Don't use \Drupal\Core\Database\Database::getConnection() |
| Custom module services | Inject via create() | Decoupled, mockable for tests |

## Pattern

```php
namespace Drupal\mymodule\Form;

use Drupal\Core\Form\ConfigFormBase;
use Drupal\Core\Form\FormStateInterface;
use Drupal\Core\Entity\EntityTypeManagerInterface;
use Drupal\Core\Config\ConfigFactoryInterface;
use Symfony\Component\DependencyInjection\ContainerInterface;

class SettingsForm extends ConfigFormBase {

  protected $entityTypeManager;

  public function __construct(
    ConfigFactoryInterface $config_factory,
    EntityTypeManagerInterface $entity_type_manager
  ) {
    parent::__construct($config_factory);
    $this->entityTypeManager = $entity_type_manager;
  }

  public static function create(ContainerInterface $container) {
    return new static(
      $container->get('config.factory'),
      $container->get('entity_type.manager')
    );
  }

  protected function getEditableConfigNames() {
    return ['mymodule.settings'];
  }

  public function getFormId() {
    return 'mymodule_settings_form';
  }

  public function buildForm(array $form, FormStateInterface $form_state) {
    // Use injected service, not static call
    $content_types = $this->entityTypeManager
      ->getStorage('node_type')
      ->loadMultiple();

    // Build form...
    return parent::buildForm($form, $form_state);
  }
}
```

**Common Services to Inject**:
- `config.factory` - ConfigFactoryInterface
- `entity_type.manager` - EntityTypeManagerInterface
- `database` - Connection
- `current_user` - AccountProxyInterface
- `messenger` - MessengerInterface (though $this->messenger() works in FormBase)
- `date.formatter` - DateFormatterInterface

## Common Mistakes

- **Wrong**: Using \Drupal::service() in form methods → **Right**: Not testable, tight coupling
- **Wrong**: Not calling parent::__construct() → **Right**: Config factory not initialized
- **Wrong**: Injecting too many services → **Right**: Form does too much, refactor to service
- **Wrong**: Forgetting to pass parent constructor args → **Right**: Fatal error
- **Wrong**: Using Database::getConnection() static call → **Right**: Should inject database service

## See Also

- [ConfigFormBase Pattern](configformbase-pattern.md)
- [FormBase Pattern](formbase-pattern.md)
- Reference: [Dependency Injection in a Form](https://www.drupal.org/docs/drupal-apis/services-and-dependency-injection/dependency-injection-in-a-form)
- Reference: core/modules/system/src/Form/SiteInformationForm.php
