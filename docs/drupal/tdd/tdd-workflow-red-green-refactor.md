---
description: Apply the RED-GREEN-REFACTOR TDD cycle to Drupal module development.
tldr: "Applying the Test-Driven Development cycle to Drupal module development. Use this workflow when building new features, refactoring existing code, or fixing bugs where the expected behavior can be specified upfront."
---

# TDD Workflow: RED-GREEN-REFACTOR

## When to Use
Applying the Test-Driven Development cycle to Drupal module development. Use this workflow when building new features, refactoring existing code, or fixing bugs where the expected behavior can be specified upfront.

## Decision
| If you're working on... | TDD makes sense? | Why |
|---|---|---|
| Service business logic (calculations, transformations) | YES -- HIGH VALUE | Fast unit/kernel tests, behavior well-defined |
| Plugin implementations (blocks, field formatters) | YES -- HIGH VALUE | Clear input/output contracts, testable in isolation |
| Access control logic | YES -- HIGH VALUE | Security-critical, explicit pass/fail conditions |
| Entity/form validation | YES -- MEDIUM VALUE | Validation rules well-defined, but setup overhead |
| Admin UI configuration forms | MAYBE -- LOW VALUE | Primarily CRUD, little custom logic, high setup cost |
| Theme templates/preprocessing | NO -- LOW VALUE | Visual output hard to assert, changes frequently |
| Migration plugins | MAYBE -- MEDIUM VALUE | Good for transform logic, expensive for full pipeline |

## Pattern

**The RED-GREEN-REFACTOR cycle** -- TDD's core rhythm:

```
1. RED    -> Write a failing test (5-10 minutes)
             Assert expected behavior before implementation exists

2. GREEN  -> Write minimal code to pass (5-15 minutes)
             Don't optimize, don't add features -- just make it green

3. REFACTOR -> Clean up while tests stay green (5-10 minutes)
               Extract methods, improve names, remove duplication

4. REPEAT -> Next requirement or edge case
```

**Cycle rhythm, not a quota**: a healthy cycle runs in minutes, so 3-6 per hour for simple features and 1-2 for complex integrations is what the pace tends to look like. It is a description, not a target. Do not write extra tests to reach it -- the number of cycles is set by the number of behaviors you were asked to build.

**Step 1: RED -- Write a failing test**:
```php
namespace Drupal\Tests\my_module\Kernel;

use Drupal\KernelTests\KernelTestBase;

class DiscountCalculatorTest extends KernelTestBase {

  protected static $modules = ['my_module'];

  public function testTenPercentDiscountApplied(): void {
    $calculator = $this->container->get('my_module.discount_calculator');

    // This WILL fail -- service doesn't exist yet
    $result = $calculator->calculate(100, 'SAVE10');

    $this->assertEquals(90, $result);
  }
}
```

Run test -> **RED** (failure expected). Output: "Service 'my_module.discount_calculator' not found."

**Step 2: GREEN -- Minimal implementation**:
```php
// my_module.services.yml
services:
  my_module.discount_calculator:
    class: Drupal\my_module\Service\DiscountCalculator

// src/Service/DiscountCalculator.php
namespace Drupal\my_module\Service;

class DiscountCalculator {
  public function calculate($price, $code) {
    // Hardcoded to pass THIS test only
    if ($code === 'SAVE10') {
      return $price * 0.9;
    }
    return $price;
  }
}
```

Run test -> **GREEN** (test passes). Don't add validation, error handling, or other codes yet.

**Step 3: REFACTOR -- Clean up**:
```php
// Add type hints, extract constant, improve readability
class DiscountCalculator {

  private const DISCOUNT_RATES = [
    'SAVE10' => 0.10,
  ];

  public function calculate(float $price, string $code): float {
    $discount_rate = self::DISCOUNT_RATES[$code] ?? 0;
    return $price * (1 - $discount_rate);
  }
}
```

Run test -> **Still GREEN**. Now add next test for different discount code, repeat cycle.

**Step 4: REPEAT -- Next requirement**:
```php
public function testTwentyPercentDiscountApplied(): void {
  $calculator = $this->container->get('my_module.discount_calculator');
  $result = $calculator->calculate(100, 'SAVE20');
  $this->assertEquals(80, $result);
}
```

RED -> add 'SAVE20' to DISCOUNT_RATES -> GREEN -> refactor if needed.

## Test Naming Conventions for Drupal

**Test method naming**: `test{Action}{Condition}{ExpectedOutcome}`
- `testUnpublishedNodeNotVisibleToAnonymous()` -- readable as sentence
- `testNodeCreation()` -- acceptable for simple cases
- `testSave()` -- too vague, AVOID

**Group annotations**: Use `#[Group('module_name')]` for filtering
```php
use PHPUnit\Framework\Attributes\Group;

#[Group('my_module')]
#[Group('commerce')]
class DiscountCalculatorTest extends KernelTestBase {
  // ...
}
```

**Covers annotations**: Document what code is tested (optional but useful for coverage)
```php
use PHPUnit\Framework\Attributes\CoversClass;

#[CoversClass(DiscountCalculator::class)]
class DiscountCalculatorTest extends KernelTestBase {
  // ...
}
```

## When TDD Doesn't Make Sense in Drupal

- **Exploratory coding**: When you don't know what the solution looks like yet (spike first, then TDD)
- **Tight coupling to Drupal UI**: Testing admin forms that are 90% configuration, 10% logic (test the 10%)
- **Visual/UX changes**: Theme adjustments, CSS, layout (manual QA more effective)
- **One-off scripts**: Drush commands that run once during migration (cost > benefit)
- **Prototyping**: Proof-of-concept work where requirements will change

## Common Mistakes

- Writing tests after implementation -- loses TDD benefits (design feedback, confidence)
- GREEN phase does too much -- adds features not covered by test, defeats safety net
- Skipping REFACTOR -- technical debt accumulates, code becomes unmaintainable
- Tests too large (testing entire feature in one test) -- hard to debug when RED, slow feedback
- Not running tests frequently -- accumulate failures, lose the RED-GREEN rhythm
- Perfectionism in GREEN phase -- spend 30 minutes optimizing before REFACTOR (just make it pass, then improve)
- Editing a test in GREEN to make it pass -- GREEN is for production code only; if the test is wrong, return to RED and change it deliberately
- Growing assertions on tests you did not write while reviewing -- a reviewer emits findings, not commits

## See Also
- [Test Type Decision Matrix](test-type-decision-matrix.md)
- [PHPUnit Configuration](phpunit-configuration.md)
- [Red, Green, Refactor | Codecademy](https://www.codecademy.com/article/tdd-red-green-refactor)
- [The Cycles of TDD - Uncle Bob](https://blog.cleancoder.com/uncle-bob/2014/12/17/TheCyclesOfTDD.html)
- Related: [TDD & Spec-Driven Development — Changing Existing Tests](https://camoa.github.io/dev-guides/development/tdd-spec-driven/changing-existing-tests/) -- who may change a test, and when
- Related: [TDD & Spec-Driven Development — Fixing Bugs with TDD](https://camoa.github.io/dev-guides/development/tdd-spec-driven/fixing-bugs-with-tdd/)
