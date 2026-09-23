---
description: Write kernel tests with KernelTestBase for services, entities, and database operations without a full site install.
tldr: "Testing services, entities, database operations, and other Drupal integrations without a full site install. Sweet spot for most Drupal testing. From 11.4 it can request a page with drupalGet(), but not submit a form or log in."
---

# Kernel Tests with KernelTestBase

## When to Use
Testing services, entities, database operations, and other Drupal integrations without a full site install. Sweet spot for most Drupal testing.

## Decision
| Feature | Unit | Kernel | Browser |
|---|---|---|---|
| Container & services | ✗ | ✓ | ✓ |
| Database access | ✗ | ✓ | ✓ |
| Entity API | ✗ | ✓ | ✓ |
| Config system | ✗ | ✓ | ✓ |
| HTTP requests (`drupalGet()`) | ✗ | ✓ from 11.4 | ✓ |
| Form rendering | ✗ | ✓ from 11.4 | ✓ |
| Form submission (`submitForm()`) | ✗ | ✗ | ✓ |
| Logged-in session (`drupalLogin()`) | ✗ | ✗ | ✓ |
| Speed (seconds per test) | 0.01 | 0.5-2 | 10-30 |

**Use Kernel when**: Service interaction matters, database needed, no logged-in browser session required.

## Pattern
**Basic kernel test setup**:
```php
namespace Drupal\Tests\my_module\Kernel;

use Drupal\KernelTests\KernelTestBase;
use PHPUnit\Framework\Attributes\RunTestsInSeparateProcesses;

#[RunTestsInSeparateProcesses]
class MyServiceTest extends KernelTestBase {

  protected static $modules = ['system', 'user', 'my_module'];

  protected function setUp(): void {
    parent::setUp();
    $this->installEntitySchema('user');
    $this->installConfig(['my_module']);
  }

  public function testServiceMethod(): void {
    $service = $this->container->get('my_module.my_service');
    $result = $service->doSomething();
    $this->assertNotEmpty($result);
  }
}
```

**Module installation hierarchy**:
1. `protected static $modules` -- loads module services/hooks, no install process
2. `installEntitySchema('entity_type')` -- creates database tables for entity type
3. `installConfig(['module'])` -- imports YAML config from config/install
4. `installSchema('module', ['table'])` -- creates custom tables from hook_schema, for the few modules that still declare one

`installSchema()` is the rare step, not a routine one: most modules declare no `hook_schema()` at all, and `installSchema()` throws a `LogicException` when the named module is not installed. In particular, do not copy `installSchema('system', ['sequences'])` out of an older test. `sequences` is the only table `system.install` still declares, it has been deprecated since drupal:10.2.0, and it is removed from drupal:12.0.0 ([change record](https://www.drupal.org/node/3220378)). `node.install` still declares `node_access`, so `installSchema('node', ['node_access'])` remains correct for node tests.

**Requesting a page from a Kernel test** (Drupal 11.4 and later): `KernelTestBase` uses `Drupal\Tests\HttpKernelUiHelperTrait`, so `drupalGet()`, `clickLink()`, `assertSession()` and `getSession()` are already there. No `use` line goes in the test. The request travels through the HTTP kernel, not a web server, and the trait's docblock names the limits:

- No logged in user. Add `UserCreationTrait` and call `setCurrentUser()`.
- No active theme. Install a theme and set it active before placing a block.
- Session semantics differ. Rely on nothing beyond the session's existence — there is no persistence and no regeneration.
- Page caching modules do not work. See `Drupal\Tests\Traits\Core\Cache\PageCachePolicyTrait` for how to set them up.

`submitForm()` and `drupalLogin()` are absent, so form submission and a logged-in session stay with `BrowserTestBase`. On Drupal 10 a Kernel test has no `drupalGet()` at all.

```php
use Drupal\Tests\user\Traits\UserCreationTrait;
use PHPUnit\Framework\Attributes\RunTestsInSeparateProcesses;

#[RunTestsInSeparateProcesses]
class ReportPageTest extends KernelTestBase {

  use UserCreationTrait;

  protected static $modules = ['system', 'user', 'my_module'];

  public function testReportPage(): void {
    $this->setCurrentUser($this->createUser(['access my module reports']));
    $this->drupalGet('my-module/report');
    $this->assertSession()->statusCodeEquals(200);
    $this->assertSession()->pageTextContains('Monthly report');
  }
}
```

**File location**: `modules/my_module/tests/src/Kernel/MyServiceTest.php`

Reference: `/core/tests/Drupal/KernelTests/KernelTestBase.php` lines 69-82

## Common Mistakes
- Forgetting `installEntitySchema()` before entity operations -- "Table 'node' doesn't exist"
- Not declaring module dependencies in `$modules` -- services missing from container
- Expecting `drupalGet()` to run as a logged-in user -- the request is anonymous until `setCurrentUser()` has run
- Installing unnecessary modules -- slower tests (only install what you need)
- Not calling `parent::setUp()` -- bootstrap incomplete, random failures

## See Also
- [Unit Tests with UnitTestCase](unit-tests.md)
- [Browser Tests with BrowserTestBase](browser-tests.md)
- Reference: `/core/tests/Drupal/KernelTests/KernelTestBase.php`
- Example: `/core/modules/block/tests/src/Kernel/BlockViewBuilderTest.php`
- [PHPUnit in Drupal | Drupal.org](https://www.drupal.org/docs/develop/automated-testing/phpunit-in-drupal)
