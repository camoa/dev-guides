---
description: Find Drupal test base classes, traits, assertions, and example test files in core.
---

# Code Reference Map

## When to Use
Finding test base classes, traits, assertions, example tests in Drupal core.

## Test Base Classes
| Class | Path | Use Case |
|-------|------|----------|
| UnitTestCase | `/core/tests/Drupal/Tests/UnitTestCase.php` | Pure PHP logic, no Drupal dependencies |
| KernelTestBase | `/core/tests/Drupal/KernelTests/KernelTestBase.php` | Services, database, entities, no HTTP |
| BrowserTestBase | `/core/tests/Drupal/Tests/BrowserTestBase.php` | Full Drupal, HTTP simulation, no JS |
| WebDriverTestBase | `/core/tests/Drupal/FunctionalJavascriptTests/WebDriverTestBase.php` | JavaScript, AJAX, real browser |

## Test Traits
| Trait | Path | Provides |
|-------|------|----------|
| UserCreationTrait | `/core/modules/user/tests/src/Traits/UserCreationTrait.php` | createUser(), createRole(), drupalLogin() |
| NodeCreationTrait | `/core/modules/node/tests/src/Traits/NodeCreationTrait.php` | createNode(), getNodeByTitle() |
| ContentTypeCreationTrait | `/core/modules/node/tests/src/Traits/ContentTypeCreationTrait.php` | createContentType() |
| BlockCreationTrait | `/core/modules/block/tests/src/Traits/BlockCreationTrait.php` | placeBlock() |
| RandomGeneratorTrait | `/core/tests/Drupal/Tests/RandomGeneratorTrait.php` | randomMachineName(), randomString() |
| SchemaCheckTestTrait | `/core/tests/Drupal/Tests/SchemaCheckTestTrait.php` | assertConfigSchema() |
| AssertContentTrait | `/core/tests/Drupal/KernelTests/AssertContentTrait.php` | assertText(), assertNoText() for Kernel |

## Assertions (WebAssert)
| Method | Purpose | Example |
|--------|---------|---------|
| statusCodeEquals() | HTTP status | `$this->assertSession()->statusCodeEquals(200)` |
| pageTextContains() | Text on page | `$this->assertSession()->pageTextContains('Welcome')` |
| fieldExists() | Form field present | `$this->assertSession()->fieldExists('title')` |
| elementExists() | CSS selector | `$this->assertSession()->elementExists('css', '.message')` |
| linkExists() | Link present | `$this->assertSession()->linkExists('Edit')` |
| buttonExists() | Button present | `$this->assertSession()->buttonExists('Save')` |
| addressEquals() | Current URL | `$this->assertSession()->addressEquals('user/login')` |
| waitForElement() | Element appears | `$this->assertSession()->waitForElement('css', '#result')` |

## Example Test Files
| Module | Type | Path |
|--------|------|------|
| Node Unit | Unit | `/core/modules/node/tests/src/Unit/` |
| Node Kernel | Kernel | `/core/modules/node/tests/src/Kernel/` |
| Node Functional | Browser | `/core/modules/node/tests/src/Functional/` |
| Node JS | WebDriver | `/core/modules/node/tests/src/FunctionalJavascript/` |
| System Kernel | Kernel | `/core/modules/system/tests/src/Kernel/` |
| User Functional | Browser | `/core/modules/user/tests/src/Functional/` |
| Block Kernel | Kernel | `/core/modules/block/tests/src/Kernel/` |

## Test Modules (Fixtures)
| Path | Purpose |
|------|---------|
| `/core/modules/node/tests/modules/node_test/` | Node module test fixtures |
| `/core/modules/system/tests/modules/` | System test modules (200+ examples) |
| `/core/modules/user/tests/modules/` | User module test fixtures |

## Configuration Files
| File | Purpose |
|------|---------|
| `/core/phpunit.xml.dist` | PHPUnit configuration template |
| `/core/tests/README.md` | Official test running documentation |
| `/core/.env.example` | Nightwatch environment template |

## See Also
- Official API documentation: [Drupal API](https://api.drupal.org/api/drupal/core!core.api.php/group/testing/11.x)
- Test discovery: Run `./vendor/bin/phpunit --list-groups` to see all available test groups
