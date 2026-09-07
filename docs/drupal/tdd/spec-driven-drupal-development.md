---
description: Apply TDD spec-driven workflow to Drupal module development with specification, test, implement, refactor cycle.
tldr: "Applying TDD principles to Drupal module development: write specification, write test, implement feature."
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
- Rename, deduplicate, improve structure; behavior-preserving only

Adding config for default export settings is a new behavior, not a refactor, so it gets its own RED. The edge cases (no content, invalid content type) are new behaviors too: each starts with one failing test in its own cycle. REFACTOR adds no tests and changes no assertions -- see the universal guide's [Changing Existing Tests](https://camoa.github.io/dev-guides/development/tdd-spec-driven/changing-existing-tests/).

## AI-Assisted Workflow
**Using Claude Code for spec-driven Drupal development**:

1. Provide the specification to a test-authoring context: "Create a content export feature with permission-based access, form for content type selection, CSV download". That context writes tests and nothing else
2. It writes one test per acceptance criterion, each seen to fail because the behavior is absent. It does not read implementation code
3. Review the tests against the spec before any implementation exists. Adjust assertions now or never: once implementation begins, an assertion changes only under the rules in the universal guide's [Changing Existing Tests](https://camoa.github.io/dev-guides/development/tdd-spec-driven/changing-existing-tests/) section -- with a recorded reason, and never by a reviewer
4. A separate implementing context writes the minimum code to pass. It has no write access to the test files
5. Run tests until green. Stop
6. Refactor while the tests stay green. No new tests in this step

**What this buys**: tests that constrain the code instead of describing it. "Catches missing test cases" is not a benefit here -- a test the spec did not ask for is a finding to record, not a test to add. See [When Not to Write a Test](https://camoa.github.io/dev-guides/development/tdd-spec-driven/when-not-to-write-a-test/).

## Common Mistakes
- Writing implementation before tests -- defeats TDD purpose
- Tests too broad (testing entire feature in one test) -- hard to debug failures
- Not running tests frequently -- accumulate failures, hard to isolate
- Skipping refactor step -- code works but unmaintainable
- Specification ambiguity -- tests don't match actual requirements (clarify spec first)

## See Also
- [Testing Events & Hooks](testing-events-hooks.md)
- [Nightwatch.js Testing](nightwatch-testing.md)
- [Test Driven Development in Drupal | Oliver Davies](https://www.oliverdavies.uk/blog/writing-new-drupal-8-module-using-test-driven-development-tdd)
