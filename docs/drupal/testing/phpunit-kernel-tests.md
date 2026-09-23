---
description: Write PHPUnit Kernel tests for service integration, database operations, and entity CRUD without full Drupal installation
tldr: "Write Kernel tests when you need to test integration with Drupal services, database operations, entity CRUD, or service container interactions without needing a full Drupal installation."
drupal_version: "11.x"
---

# PHPUnit Kernel Tests

## When to Use

Write Kernel tests when you need to test integration with Drupal services, database operations, entity CRUD, or service container interactions without needing a full Drupal installation.

## Decision

| If you need... | Use Kernel Tests | Why |
|----------------|------------------|-----|
| Test service integration | Yes | Access to container and dependency injection |
| Entity CRUD operations | Yes | Database and entity storage available |
| Configuration system | Yes | Config system fully functional |
| Read a page over HTTP | Yes, on Drupal 11.4 or later | `KernelTestBase` sends the request through the HTTP kernel |
| Submit a form, or act as a logged-in user | No, use Functional | A Kernel test has no `submitForm()` and no `drupalLogin()` |
| Test JavaScript | No, use FunctionalJavascript | No browser environment |

## Pattern

```php
<?php
namespace Drupal\Tests\my_module\Kernel;

use Drupal\KernelTests\KernelTestBase;
use Drupal\node\Entity\Node;
use Drupal\node\Entity\NodeType;
use Drupal\user\Entity\User;
use PHPUnit\Framework\Attributes\Group;
use PHPUnit\Framework\Attributes\RunTestsInSeparateProcesses;

/**
 * Tests the my_module entity processor service.
 */
#[Group('my_module')]
#[RunTestsInSeparateProcesses]
class EntityProcessorTest extends KernelTestBase {

  protected static $modules = [
    'system', 'user', 'node', 'field', 'text', 'my_module',
  ];

  protected function setUp(): void {
    parent::setUp();

    // Install database schemas
    $this->installEntitySchema('user');
    $this->installEntitySchema('node');
    
    // Install configuration
    $this->installConfig(['system', 'node', 'my_module']);
    
    // Create content type
    NodeType::create([
      'type' => 'article',
      'name' => 'Article',
    ])->save();

    // Create required users (user 0 = anonymous, user 1 = admin)
    User::create(['uid' => 0, 'name' => 'guest'])->save();
    User::create(['uid' => 1, 'name' => 'admin'])->save();
  }

  public function testEntityProcessing(): void {
    $node = Node::create([
      'type' => 'article',
      'title' => 'Test Article',
      'uid' => 1,
    ]);
    $node->save();

    // Test service from container
    $processor = $this->container->get('my_module.entity_processor');
    $result = $processor->process($node);

    $this->assertTrue($result['success']);
    $this->assertEquals('Test Article', $result['title']);
    $this->assertInstanceOf(Node::class, $result['entity']);
  }

  public function testConfigurationIntegration(): void {
    // Test configuration system
    $config = $this->config('my_module.settings');
    $config->set('api_enabled', TRUE)->save();

    $service = $this->container->get('my_module.api_client');
    $this->assertTrue($service->isEnabled());
  }
}
```

**File Location**: `modules/my_module/tests/src/Kernel/EntityProcessorTest.php`

**Every Kernel, Functional, FunctionalJavascript and Performance class needs `#[RunTestsInSeparateProcesses]`.** Core's `KernelTestBase::setUp()` triggers a deprecation when the attribute is absent: `Kernel test classes must specify the #[RunTestsInSeparateProcesses] attribute, not doing so is deprecated in drupal:11.3.0 and will throw an exception in drupal:12.0.0` ([node/3548485](https://www.drupal.org/node/3548485)). `BrowserTestBase::setUp()` does the same for `Functional/FunctionalJavascript test classes`. In 11.3 and 11.4 it is still only a deprecation, so add the attribute now and the class survives Drupal 12. Unit tests have no such check — leave the attribute off them.

**The attribute is not inherited.** PHPUnit reads it from the class it is about to run, so a concrete subclass of a decorated abstract base reports no such metadata. A project base class cannot carry it for its children, which is why core decorates every concrete test class instead.

## Pattern: Reading Pages in a Kernel Test

**A Kernel test can request a page.** `KernelTestBase` uses `Drupal\Tests\HttpKernelUiHelperTrait`, so every Kernel test already has `drupalGet()`, `clickLink()`, `assertSession()` and `getSession()`, and sends its requests through the HTTP kernel. Nothing goes in the test to switch this on — no `use` line, no property. A test that only has to read a page no longer has to be Functional, so it skips the full site install. You will still meet `use HttpKernelUiHelperTrait;` written out in core's `help` module Kernel tests. That line is redundant but harmless.

The trait's own docblock names the limits:

- **No logged in user.** Add `Drupal\Tests\user\Traits\UserCreationTrait` and set a current user.
- **No active theme.** To place a block, the test must first install a theme and set it as active.
- **Session semantics differ** from a normal page request. Do not rely on session state beyond its existence — there is no persistence and no regeneration.
- **Page caching modules will not work.** See `Drupal\Tests\Traits\Core\Cache\PageCachePolicyTrait` for how to set them up.

Two methods are absent: `submitForm()` and `drupalLogin()` belong to `BrowserTestBase`. So a form submission, a logged-in browser session, JavaScript, and anything that needs a real web server all remain Functional's job.

**On Drupal 10 the old rule still holds.** The trait arrived in 11.4. A Drupal 10 Kernel test has no `drupalGet()` at all, so a test that has to read a page there is a Functional test.

```php
<?php
namespace Drupal\Tests\my_module\Kernel;

use Drupal\KernelTests\KernelTestBase;
use Drupal\Tests\user\Traits\UserCreationTrait;
use PHPUnit\Framework\Attributes\Group;
use PHPUnit\Framework\Attributes\RunTestsInSeparateProcesses;

/**
 * Tests the my_module report page.
 */
#[Group('my_module')]
#[RunTestsInSeparateProcesses]
class ReportPageTest extends KernelTestBase {

  use UserCreationTrait;

  protected static $modules = ['system', 'user', 'my_module'];

  protected function setUp(): void {
    parent::setUp();
    $this->installEntitySchema('user');
    $this->installConfig(['my_module']);

    // A Kernel test request has no logged in user, so set one explicitly.
    $this->setCurrentUser($this->createUser(['access my module reports']));
  }

  public function testReportPage(): void {
    $this->drupalGet('my-module/report');
    $this->assertSession()->statusCodeEquals(200);
    $this->assertSession()->pageTextContains('Monthly report');
  }
}
```

**File Location**: `modules/my_module/tests/src/Kernel/ReportPageTest.php`

## Common Mistakes

- Not installing entity schemas → Database errors when creating entities
- Not installing configuration → Services fail to load config values
- Not creating required users (uid 0, 1) → Permission errors in entity operations
- Forgetting to list all required modules in `$modules` → Missing dependencies
- Calling `drupalGet()` and expecting a logged-in user → The request is anonymous until `setCurrentUser()` runs
- Calling `submitForm()` or `drupalLogin()` in a Kernel test → Neither method exists; write a Functional test

**WHY these are mistakes**: Kernel tests bootstrap a minimal Drupal environment. Unlike full Functional tests, you must manually install schemas and configuration. Missing setup steps cause cryptic errors. `drupalGet()` works from Drupal 11.4 on, but it goes through the HTTP kernel rather than a web server, so it carries the limits listed above and brings none of `BrowserTestBase`'s session handling with it.

## See Also

- [PHPUnit Unit Tests](phpunit-unit-tests.md)
- [PHPUnit Functional Tests](phpunit-functional-tests.md)
- Reference: [Setup tasks in Kernel tests - Drupal.org](https://www.drupal.org/docs/automated-testing/phpunit-in-drupal/setup-tasks-in-kernel-tests)
- Reference: [Making HTTP requests in Kernel tests - Drupal.org](https://www.drupal.org/docs/develop/automated-testing/phpunit-in-drupal/making-http-requests-programmatically-in-kernel-tests)
- Reference: `/core/tests/Drupal/KernelTests/KernelTestBase.php`
