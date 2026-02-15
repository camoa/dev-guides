---
description: Reuse business logic between web controllers and Drush CLI commands by extracting shared logic into services.
---

# Drush and CLI Reuse

## When to Use

When you need to perform operations via command line (cron, batch processing, deployments) and want to reuse the same business logic that exists in web controllers/forms.

## Decision

| If you need... | Use... | Why |
|---|---|---|
| CLI version of web feature | Drush command that calls same service | Reuse business logic, avoid duplication |
| Batch processing | Drush command + Batch API service | CLI for triggering, service for logic |
| Cron tasks | Service called by both hook_cron and Drush | Testable, reusable between web and CLI |
| Web-only operation | Keep in controller | Don't create CLI version until needed |

## Pattern

```php
// Service with business logic (shared between web and CLI)
namespace Drupal\mymodule;

class DataProcessor {

  public function processItems(array $items): array {
    $results = [];
    foreach ($items as $item) {
      // Business logic here
      $results[] = $this->processItem($item);
    }
    return $results;
  }

  protected function processItem($item) {
    // Actual processing logic
    return $item;
  }
}
```

```php
// Web controller uses service
namespace Drupal\mymodule\Controller;

class ProcessController extends ControllerBase {

  public function __construct(
    protected DataProcessor $processor,
  ) {}

  public function process() {
    $items = $this->getItems();
    $results = $this->processor->processItems($items);
    return ['#markup' => 'Processed ' . count($results) . ' items'];
  }
}
```

```php
// Drush command uses SAME service
namespace Drupal\mymodule\Commands;

use Drush\Commands\DrushCommands;

class MyModuleCommands extends DrushCommands {

  public function __construct(
    protected DataProcessor $processor,
  ) {
    parent::__construct();
  }

  #[CLI\Command(name: 'mymodule:process')]
  public function process() {
    $items = $this->getItems();
    $results = $this->processor->processItems($items);
    $this->output()->writeln('Processed ' . count($results) . ' items');
  }
}
```

Reference: `core/lib/Drupal/Core/Command/`, Drush documentation for custom commands

## Common Mistakes

- **Duplicating logic between web and CLI** — Extract to service, inject into both controller and Drush command
- **Business logic in Drush command class** — Keep commands thin, delegate to services
- **Not considering memory limits in CLI** — Batch processing should be in service, callable from both web (Batch API) and CLI
- **Hardcoding CLI-specific assumptions in services** — Services should work in any context (web, CLI, queue worker)

## See Also

- [Recipes for Reusable Config](recipes-reusable-config.md)
- [Over-DRY Anti-Patterns](over-dry-anti-patterns.md)
- Reference: [Drush Commands | Drupal.org](https://www.drush.org/latest/commands/)
- Reference: Service architecture best practices in `core/core.services.yml`
