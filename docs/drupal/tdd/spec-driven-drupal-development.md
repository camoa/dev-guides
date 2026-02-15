---
description: Apply TDD spec-driven workflow to Drupal module development with specification, test, implement, refactor cycles.
---

# Spec-Driven Drupal Development

## When to Use
Applying TDD principles to Drupal module development: write specification, write test, implement feature.

## Workflow
**Spec-driven cycle for Drupal module features**:

1. **Write specification** (natural language or structured format)
   - What the feature does
   - Who can access it
   - What data it operates on
   - Expected behavior and edge cases

2. **Write failing test** (based on spec)
   - Choose appropriate test type (Unit/Kernel/Browser)
   - Test one aspect of specification per test method
   - Assert expected behavior

3. **Implement minimum code** to pass test
   - Routes, controllers, services, forms
   - Follow Drupal best practices (DI, render arrays, etc.)

4. **Refactor** while tests stay green
   - Extract services, improve naming, optimize

5. **Repeat** for next specification aspect

## Pattern
**Example: Building a content export feature (spec-driven)**

**Step 1 -- Specification**:
```
Feature: Content Export
As a site administrator
I need to export nodes to CSV
So that I can analyze content in spreadsheets

Acceptance criteria:
- Route /admin/content/export accessible to users with "export content" permission
- Form allows selecting content type
- CSV download contains node ID, title, author, created date
- Unpublished nodes excluded from export
```

**Step 2 -- Write failing test**:
```php
namespace Drupal\Tests\content_export\Functional;

use Drupal\Tests\BrowserTestBase;

class ContentExportTest extends BrowserTestBase {

  protected static $modules = ['node', 'content_export'];
  protected $defaultTheme = 'stark';

  public function testExportFormAccess(): void {
    // Will fail -- route doesn't exist yet
    $user = $this->drupalCreateUser(['export content']);
    $this->drupalLogin($user);
    $this->drupalGet('admin/content/export');
    $this->assertSession()->statusCodeEquals(200);
  }

  public function testExportCsvDownload(): void {
    // Will fail -- functionality doesn't exist yet
    $this->drupalCreateContentType(['type' => 'article']);
    $this->drupalCreateNode(['type' => 'article', 'title' => 'Test Article', 'status' => 1]);

    $user = $this->drupalCreateUser(['export content']);
    $this->drupalLogin($user);
    $this->drupalGet('admin/content/export');
    $this->submitForm(['content_type' => 'article'], 'Export');

    $this->assertSession()->responseHeaderContains('Content-Type', 'text/csv');
    $this->assertSession()->pageTextContains('Test Article');
  }
}
```

**Step 3 -- Implement minimum code**:
- Create route in `content_export.routing.yml`
- Create permission in `content_export.permissions.yml`
- Create form `ContentExportForm`
- Create controller that generates CSV

**Step 4 -- Run tests, verify green**:
```bash
./vendor/bin/phpunit modules/custom/content_export/tests/src/Functional/ContentExportTest.php
```

**Step 5 -- Refactor**:
- Extract CSV generation to service
- Add config for default export settings
- Add tests for edge cases (no content, invalid content type)

## AI-Assisted Workflow
**Using Claude Code for spec-driven Drupal development**:

1. Provide specification to Claude Code
2. Claude Code generates test file based on spec
3. Review test, adjust assertions as needed
4. Ask Claude Code to implement minimum code to pass tests
5. Run tests, iterate until green
6. Ask Claude Code to refactor while keeping tests green

## Common Mistakes
- Writing implementation before tests -- defeats TDD purpose
- Tests too broad (testing entire feature in one test) -- hard to debug failures
- Not running tests frequently -- accumulate failures, hard to isolate
- Skipping refactor step -- code works but unmaintainable
- Specification ambiguity -- tests don't match actual requirements (clarify spec first)

## See Also
- Universal TDD principles: `dev-tdd-spec-driven.md`
- Reference: [Test Driven Development in Drupal | Oliver Davies](https://www.oliverdavies.uk/blog/writing-new-drupal-8-module-using-test-driven-development-tdd)
