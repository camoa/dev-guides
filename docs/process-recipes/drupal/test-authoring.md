---
# Routing block — an orchestrator reads to here and decides.
name: drupal_test_authoring
capability: test-authoring
description: Use when a context is about to write the tests for one unit of work on a Drupal project, before any production code exists, and needs to know which tier the behaviour belongs at, where the file goes, what it is called, how the criterion it specifies is reported for it, and what a Drupal test may not do.
# Metadata — read only after a match.
label: Test authoring (Drupal)
recipe_schema_version: 1.0.0
version: 0.5.0
# Machine-readable dependency declaration (recipe-loader resolves these without parsing prose).
requires_guides:
  - development/tdd-spec-driven
  - drupal/testing
  - drupal/tdd
# Process-recipe routing keys, enforced by validate_recipes.py for any recipe
# under docs/process-recipes/. `capability` above doubles as the phase; there is
# no separate applies_to_phase. `framework` is the second routing dimension.
recipe_class: process
framework: drupal
drupal_compatibility: "^10.3 || ^11"
assumes:
  - composer
  - ddev
authors:
  - name: camoa
license: GPL-2.0-or-later
---

## Goal

Answer four questions for whoever is about to write a Drupal test: which tier the behaviour belongs
at, where the file goes and what it is called, how the criterion each test proves is reported, and what
a Drupal test may not do.

**This recipe stops at red.** Its reader writes the test, watches it fail, and stops. It does not
write the code that turns the test green, and nothing here tells it to. The green and refactor half
of the cycle belongs to `drupal/standards-and-tests.md`, read by a different context. Running the
test belongs to `drupal/test-execution.md`, which several callers share.

The reader also cannot open the production source of anything already built. Every rule below is
therefore decidable from the behaviour the test must observe and from the names the unit declares.
A rule that needs the class in front of you is a rule this reader cannot follow.

## Opinion

**Do not start at Unit.** This is the correction that matters most and it reverses the obvious
default. Drupal code is mostly integration: services resolved from a container, hooks, entities,
configuration. Start at Kernel, or at Functional where a real request is involved, and reach for Unit
only for a pure function with no container dependency. Two independent sources agree on the failure
mode: the stack-neutral definition of a unit test is a set of dependency exclusions and a speed
target, which excludes almost nothing and therefore does not stop you; and an agent asked for "the
smallest tier that answers the question" reads that as Unit and mocks a container it should have
booted. A Unit test that mocks the container proves the mock.

**The tier follows the dependency surface, decided from the behaviour and not from the code.**

| Tier | Directory | Choose it when the behaviour needs | Cost |
|---|---|---|---|
| Kernel | `tests/src/Kernel/` | a service, an entity, code that reads configuration, or the database, with a minimal container. Exported site configuration itself is no tier's subject: it is proved by the `## Configuration gate` in `drupal/standards-and-tests.md`, not by a test | seconds per test |
| Functional | `tests/src/Functional/` | a real request, a form, a route, or rendered output, with no JavaScript | a site boot per test |
| FunctionalJavascript | `tests/src/FunctionalJavascript/` | JavaScript executed in a browser: Ajax, a modal, dynamic visibility. Never written test-first, as below | a site boot plus a browser session per test |
| Unit | `tests/src/Unit/` | nothing from Drupal at all: a pure function over its arguments | milliseconds |
| Build | `tests/src/Build/` | the assembled codebase itself, such as Composer resolution, driven from the command line | rare, advanced |

The tier names are core's own. `core/phpunit.xml.dist` in 11.4.5 declares six testsuites —
`unit-component`, `unit`, `kernel`, `functional`, `functional-javascript` and `build` — and each maps
a suite to `tests/src/<Tier>` under a module. Two limits of the declared suites are worth knowing
before choosing Build: the `build` suite scans `modules/**` only, so a Build test under a theme or a
profile is not discovered by it at all; and `unit-component` is core's own, not a tier a project
writes into.

Kernel installs nothing on its own. A Kernel test that needs a table calls `installEntitySchema()`,
`installConfig()` or `installSchema()` itself. "Table does not exist" is that call missing, not the
behaviour absent — the running-a-test twin of this is declared in `drupal/test-execution.md`, which
reads it out of a failure rather than preventing it.

**A unit that ships a recipe is proved at Functional, core's own convention for a recipe test.**
When a recipe's `content/` folder creates terms or entities, a Functional test that applies it and
checks what it created proves that. A Kernel test can apply a recipe too, through
`RecipeRunner::processRecipe()` (see `core/tests/Drupal/KernelTests/Core/Recipe/RecipeRunnerTest.php`),
but this recipe picks Functional, the tier `GenericRecipeTestBase` already uses. The gate never
applies a recipe, so it cannot.

Use `GenericRecipeTestBase` (`core/modules/system/tests/src/Functional/Recipe/GenericRecipeTestBase.php`)
as the model, not the base class. Its only test, `testRecipeCanBeApplied()`, applies the recipe
twice to prove it applies and is idempotent, asserts nothing about what the recipe created, and runs
unguarded in any subclass and proves no criterion — extending it puts that test in your class too.
Extend `BrowserTestBase` and `use RecipeTestTrait`
(`Drupal\FunctionalTests\Core\Recipe\RecipeTestTrait`) directly instead, and write your own test
method against its own criterion. Mirror the base's `$profile = 'minimal'` and
`$defaultTheme = 'stark'` properties, and call `$this->setUpCurrentUser(admin: TRUE)` before
applying, as the base does. If a test should also prove idempotency, apply the recipe twice inside
that test, under its own criterion.

**Before the recipe exists, guard the apply so each test still fails on its own assertion.**
`getRecipePath()` and `doApply()` belong to the base class and are not inherited here, so compute
the recipe's path directly: `InstalledVersions::getRootPackage()['install_path']` — the same call
`RecipeTestTrait::runDrupalCommand()` uses to find the project root — plus `recipes/<name>`. Call
`$this->applyRecipe($path)` only when `is_dir($path)` is `TRUE`, then assert on the entities
regardless. Calling `applyRecipe()` against a path that does not exist yet fails inside
`RecipeTestTrait::applyRecipe()`, on the `Process exit code mismatch` line — the shared line every
unguarded recipe test would fail on. With the guard closed, the entity assertion fails on its own
missing value instead.

**Do not put this test in the recipe's own folder.** The only recipes directory core's functional
suite scans is `recipes/*/tests/src/Functional`, under core. A drupal/recommended-project site
installs recipes into a project-root `recipes/` folder that no suite scans. A test copied there
never runs, and the miss is silent. Put the test in a custom module's `tests/src/Functional/`
instead — deriving the path from `InstalledVersions::getRootPackage()['install_path']`, as above,
resolves it whether or not the docroot sits inside the project root. `$this->root`, the Drupal
docroot set in `core/tests/Drupal/Tests/DrupalTestCaseTrait.php`, is not that project root. The
alternative is adding the project's `recipes/` folder to the project-root `phpunit.xml` that
`drupal/test-execution.md` reaches the runner through.

**Kernel, Functional, Unit and Build are written before the code. FunctionalJavascript, Playwright
and visual regression are not.** All three drive a browser. They run against a site that already
stands, cannot drive a design decision, and never substitute for a tier chosen here. A person adds
one after the code stands. Where a browser behaviour has a server half, such as the response an
Ajax callback returns or the value a form saves, specify that half test-first at Kernel or
Functional. "The end-to-end suite covers it" is not an answer to "which tier specifies this
behaviour".

The tests written first run on every build attempt, whatever their tier. A Functional test
therefore pays a site boot per test on each attempt, which is the reason to choose Kernel wherever
Kernel shows the behaviour. The whole suite still runs once, at the end of a task.

**One test per behaviour the criterion names, and no more.** Past that, tests make the change harder
to review without specifying anything new. The full set of excess cases belongs to
`development/tdd-spec-driven` and is cited, not restated.

**Mechanics are referenced, not re-authored.** How a base class is extended, how a Kernel test
installs its schema, and the house conventions belong to `drupal/testing`, `drupal/tdd` and
`drupal/best-practices/camoa`.

**A test for a module that does not exist yet extends core's base class, not one in the module's
own test namespace.** Nothing registers `Drupal\Tests\<module>\` before the module's info file
does, so a test that extends a module-local base class fatals at autoload before any test runs,
exit 255 and `Fatal error` with `not found`, a harness marker and not an assertion, so it is accepted only for the order that creates the module and refused for every other. The module-local base class waits for the
order that creates the module, or the first tests extend `KernelTestBase` or `BrowserTestBase`
directly. Observed on core 11.4.5, eleven kernel tests of a new module, every one refused.

**A test for a class that does not exist yet must still fail on its own assertion, not on
autoload, and not on a line every other test in the order shares.** The commonest red in
test-first work is a class, or a service, inside a module that exists, and the natural first run
errors in autoload: `Error: Class "..." not found`, `ERRORS!`, exit 2, which the freeze reads as a
setup gap and not as a red, because a red is read by the assertion marker and an autoload error
carries none. Do not repair this by opening the test with an assertion that names the missing
class or service — `assertTrue(class_exists(...))` or `assertTrue($this->container->has(...))` —
because every test in an order then stops on that identical line: on a live ten-test order, all
ten opened this way and every red pointed at the shared opener, not at the ten behaviours, and
five of the ten would still have passed against an implementation that returns an empty list.
Tests that stop on one shared line prove one fact, not many.

Guard the lookup instead, so it yields an empty value when the class or service is absent, and let
the test's own assertion fail on that value. Kernel or Functional, where the missing name is a
service:

```php
$service = $this->container->has('my_module.occurrence_expander')
  ? $this->container->get('my_module.occurrence_expander')
  : NULL;
$this->assertSame(['expected'], $service?->expand($input));
```

Unit, where the missing name is a plain class with no container dependency:

```php
$expander = class_exists(OccurrenceExpander::class) ? new OccurrenceExpander() : NULL;
$this->assertSame(['expected'], $expander?->expand($input));
```

`::class` does not autoload the name it names, so `class_exists()` returns `FALSE` rather than
erroring when the class is absent. Each guard is expected to fail on the mismatch between `NULL`
and `['expected']`, in that test alone; once the class or service exists and returns correctly the
assertion passes. Where the behaviour's own correct answer is itself an empty result, a loose
assertion such as `assertEmpty()` or `assertEquals([], ...)` would pass against `NULL` too, for the
wrong reason — prefer `assertSame()`, which does not, because `NULL` is never `[]`. Add a case for
a non-empty `$input` whose correct result is non-empty, so the guard still fails it. Observed on
PHPUnit 11.5.56: an unguarded reference to the missing class prints `ERRORS! Tests: 1, Assertions:
2, Errors: 1`.

A method that does not exist yet, on a class or service that does, takes a reflection guard:

```php
$expander = $this->container->get('my_module.occurrence_expander');
$result = (new \ReflectionObject($expander))->hasMethod('lookahead')
  ? $expander->lookahead($input)
  : NULL;
$this->assertSame(['expected'], $result);
```

It calls the method directly, so the method's visibility and declared return type still apply. Do
not guard with `method_exists()` or `is_callable()`. Once the method exists, PHPStan reports each
as `function.alreadyNarrowedType`, always true, so the test fails the project's own static analysis
after the task finishes. Do not call through `ReflectionMethod::invoke()` either: it also reaches
a protected or private method, and it returns `mixed`. Until the method exists, PHPStan reports
`method.notFound` on the call, as it does for any test written before its code. This guard is for
an existing class only. A class that is itself new takes the `class_exists()` guard above, and
`?->` covers its methods. Observed on PHPStan 2.3.5 at levels 5 and max, with PHPUnit 11.5.57, on
an object whose class PHPStan knows: before the method exists the test fails with `Failed asserting that null is identical to`, and
after it exists the test passes and analysis is clean.

## Preconditions

This phase writes files and runs nothing, so it declares no machine-checkable environment condition
of its own. The conditions for running a Drupal test — a reachable runner, `SIMPLETEST_DB`, and
`SIMPLETEST_BASE_URL` for the tiers that need them — are declared by `drupal/test-execution.md`,
beside the commands they are conditions of. The step that watches a test fail reads them there.

```yaml
preconditions: []
```

## Input contract

```yaml
code_path: string             # absolute path to the Drupal project root
module: string                # the module the test belongs to
criterion_id: string          # the criterion this test proves, reported to the freeze; the test need not carry it
behavior: string              # what the test must observe, in a sentence
interface: string             # the names the unit declares, and the names its dependencies declare
test_tier: string             # optional; kernel | functional | unit | build
```

`interface` is the only thing this reader gets about code that already exists, and it is a
declaration rather than source. Where it is empty, the behaviour must be observable from the
module's public surface alone.

## Sequence

If invoked in dry-run mode, emit the tier choice, the file path, the test name and the assertions
planned, and write nothing. Dry-run is required.

1. **Select the tier.** From `behavior` and the dependency surface it implies, using the table in
   Opinion. Use `test_tier` if supplied. If the behaviour cannot be placed without opening the code,
   stop and report that rather than guessing: the choice belongs earlier.

2. **Place and name the file.** `tests/src/<Tier>/<Name>Test.php` under the module, in the namespace
   `\Drupal\Tests\<module>\<Tier>`. The tier segment matches the directory exactly, because core maps
   the namespace `Drupal\Tests\<module>\` onto that module's `tests/src` directory and nothing
   normalises the segment below it — so the capitalisation of `FunctionalJavascript` decides whether
   the runner discovers the test at all. The class name ends in `Test`. The authoritative file
   pattern is declared once, in `drupal/standards-and-tests.md` under `## Oracle files`, and is not
   repeated here.

3. **Name the method so the runner collects it, then name it for the behaviour.** A method is
   collected only when its name begins with `test` or it carries the `#[Test]` attribute. Neither is a
   style preference: a method with neither is not collected and nothing says so — on the PHPUnit
   11.5.56 that core 11.4.5 resolves, it simply does not appear in `--list-tests`, so the behaviour
   looks covered and is not.

   Name each test for the behaviour its body checks, in the project's own convention:
   `testSubmittedFormSavesTheNode()`. The Drupal coding standard rejects an underscore in a method
   name, so use camel case. Report the criterion each test proves, with the test's path and name, in
   the return of step 6; the freeze records that mapping, and every later reader joins on the
   recorded name. A test needs no criterion identifier in its name or its tags. Keep the module
   `#[Group]` the project already uses: in Drupal it names the module, and a test keeps it.

   Test names are unique across the suite, not only within a class. A failure is matched back to its
   criterion by the bare test name, ignoring the path, so two classes that share a name tie one
   failure to both criteria.

   A project may still carry the identifier for its own navigation, as a name suffix or a second
   `#[Group]` on the method (a group on the class selects every method in it). If it does, put the identifier last, capitalised, with no separator, and delimit it so
   it cannot be a prefix of another: `testSubmittedFormSavesTheNodeC3()` with `#[Group('c3')]`. An
   anchored `--filter '/C3$/'` then selects the one test, where a bare `--filter C3` also selects
   `testDecodeC30`, and `--group c3` is an exact match. Both forms were checked on the PHPUnit 11.5.56
   that core 11.4.5 resolves, against a deliberate `C30` sibling. `--filter` alone searches every
   discovered tier, so it needs `--testsuite` or a path beside it. A test bound for an upstream
   project, such as a contrib merge request, follows that project's naming and carries no identifier.

4. **Write the test, shaped Arrange-Act-Assert.** Declare `#[RunTestsInSeparateProcesses]` on a
   Kernel, Functional or FunctionalJavascript class — not on a Unit test, which needs none. As of
   core 11.4.5 the base classes trigger a deprecation when the attribute is absent, naming
   drupal:11.3.0 as the version that deprecated it and drupal:12.0.0 as the version that throws:
   so it is not yet fatal, and it fails the run today on any project whose deprecation helper is set
   to fail. Assert on what the criterion names, and nothing else.

5. **Watch it fail.** Run it through `drupal/test-execution.md` and read the failure signal declared
   there, never the exit status. Only an assertion that ran and did not hold is a red run. A harness
   that never reached the behaviour is a setup gap, and a run that selected nothing exits zero and
   proves nothing. A test that passes immediately is rewritten once; if it still passes with no code
   behind it, stop and report it as proving nothing.

6. **Stop.** Return the tier, the path, the test names, the criterion each proves, and the failure
   output for each. Write no production code.

## Data flow

Input: one criterion, the behaviour it names, the declared interface, the module.
Output: one or more test files, and for each test the criterion it proves and the output of the run
that failed.
Boundaries: reads no production source; writes only under the module's test tree; runs no command
except through `drupal/test-execution.md`; produces no task record of its own.

## State-awareness contract

Before writing a new test, look for an existing test that already specifies the behaviour, by
searching the module's test tree for the behaviour's own vocabulary, and for the criterion
identifier where the project carries one. Update the existing test rather than adding a second one
that overlaps it. A bug fix almost always belongs on the existing test for the behaviour that broke.

Do not read the production source to make that decision. The test tree is readable; the code is not.

## Verifier

- Each test name describes the behaviour its body checks, and is unique across the suite.
- A criterion is reported for every test, with its path and name.
- Every test method begins with `test` or carries `#[Test]`. A method with neither is not collected
  and nothing reports it.
- Every data provider method is `static`. On PHPUnit 11.5 a non-static provider makes the whole class
  collect nothing — the run reports `is not static`, then `No tests found in class`, then
  `No tests executed!`, and exits 2 — so a class whose only provider was written non-static
  contributes zero tests to a run that otherwise looks fine.
- Each test sits in the directory and the namespace its tier requires, and the file name ends in
  `Test.php`.
- Each Kernel, Functional or FunctionalJavascript class declares `#[RunTestsInSeparateProcesses]`.
- Each new test was seen to fail, and the recorded failure is an assertion that ran and did not hold
  rather than a harness error or a run that selected nothing.
- No Unit test mocks the container. A behaviour needing the container is at Kernel or above.
- No `waitForElement` or a sibling in its family is left without an assertion on its return value.
  Core declares the return type `\Behat\Mink\Element\NodeElement|null` and returns NULL when the
  element never appears, so an unasserted call is a test that always passes.
- No Functional test asserts on rendered markup that no template or API contract pins. The repair is
  a Kernel test against the service that produced the value, not a stricter string match.
- No production file was written or changed.

## References

### Drupal guides (referenced, not authored here)

| Guide | What it holds |
|---|---|
| `drupal/testing` | The tier base classes, the runner configuration, and the environment each tier needs |
| `drupal/tdd` | The Drupal form of the cycle |
| `drupal/best-practices/camoa` | House conventions |

### Stack-neutral discipline (referenced, not authored here)

| Guide | What it holds |
|---|---|
| `development/tdd-spec-driven` | What a failing test proves, when not to write a test at all, the anti-patterns, and when a double is legitimate. Written for one person doing red, green and refactor; this reader does red and stops |

### Sibling process recipes

| Recipe | What it holds |
|---|---|
| `drupal/test-execution.md` | The command at each scope, its cost, the conditions for running one, and how to read what came back |
| `drupal/standards-and-tests.md` | The green and refactor half, the coding standards, the security rules, and the `## Oracle files` declaration that names the test file pattern |

### External origins (referenced, not authored here)

| Origin | What it settled |
|---|---|
| `ai_best_practices`, skill `drupal-automated-testing`, citing a core committer and drupal.org issue #3581672 | That starting at Unit is wrong for Drupal; the unasserted `waitForElement`; the per-tier namespace and the `FunctionalJavascript` capitalisation; build tests as a fifth type |
| Drupal core 11.4.5 — `core/phpunit.xml.dist`, `BrowserTestBase`, `KernelTestBase`, `JSWebAssert`, `TestDiscovery` | The six declared testsuites and what each scans; the deprecation status of `#[RunTestsInSeparateProcesses]`; the nullable return of the wait helpers; the namespace-to-directory mapping; that core itself stacks two `#[Group]` attributes on a class |
| PHPUnit 11.5.56, the runner core 11.4.5 resolves | That a method with neither a `test` prefix nor `#[Test]` is not collected and nothing says so; that `--group` matches exactly while `--filter` is an unanchored regular expression over the test identifier; that a non-static data provider makes the whole class collect nothing and exit 2 |
