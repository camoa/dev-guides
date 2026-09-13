---
# Routing block — an orchestrator reads to here and decides.
name: drupal_test_authoring
capability: test-authoring
description: Use when a context is about to write the tests for one unit of work on a Drupal project, before any production code exists, and needs to know which tier the behaviour belongs at, where the file goes, what it is called, how the criterion it specifies is traced to it, and what a Drupal test may not do.
# Metadata — read only after a match.
label: Test authoring (Drupal)
recipe_schema_version: 1.0.0
version: 0.2.0
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
at, where the file goes and what it is called, how the criterion it specifies is recoverable from it,
and what a Drupal test may not do.

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
| Kernel | `tests/src/Kernel/` | a service, an entity, configuration, or the database, with a minimal container | seconds per test |
| Functional | `tests/src/Functional/` | a real request, a form, a route, or rendered output, with no JavaScript | a site boot per test |
| FunctionalJavascript | `tests/src/FunctionalJavascript/` | JavaScript executed in a browser: Ajax, a modal, dynamic visibility | a site boot plus a browser session per test |
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

**All five tiers are written before the code. Playwright and visual regression are not.** Those run
against a site that already stands, cannot drive a design decision, and never substitute for a tier
chosen here. "The end-to-end suite covers it" is not an answer to "which tier specifies this
behaviour".

**One test per behaviour the criterion names, and no more.** Past that, tests make the change harder
to review without specifying anything new. The full set of excess cases belongs to
`development/tdd-spec-driven` and is cited, not restated.

**Mechanics are referenced, not re-authored.** How a base class is extended, how a Kernel test
installs its schema, and the house conventions belong to `drupal/testing`, `drupal/tdd` and
`drupal/best-practices/camoa`.

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
criterion_id: string          # the identifier of the criterion this test specifies
behavior: string              # what the test must observe, in a sentence
interface: string             # the names the unit declares, and the names its dependencies declare
test_tier: string             # optional; kernel | functional | functional-javascript | unit | build
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

3. **Name the method so the runner collects it, then name the criterion in it.** A method is
   collected only when its name begins with `test` or it carries the `#[Test]` attribute. Neither is a
   style preference: a method with neither is not collected and nothing says so — on the PHPUnit
   11.5.56 that core 11.4.5 resolves, it simply does not appear in `--list-tests`, so the behaviour
   looks covered and is not.

   The criterion identifier goes at the end of the
   test method name, capitalised, with no separator, because the Drupal coding standard rejects an
   underscore in a method name: `testSubmittedFormSavesTheNodeC3()`. It goes last and nothing follows
   it, which keeps the criterion in the failure output and findable by grep with no runner support.

   For **selection**, add `#[Group('c3')]` to the method as well. The group is the mechanism the
   runner gives that the name cannot match: `--group c3` is an **exact** match, while `--filter`
   takes a regular expression over the test identifier, so a bare `--filter C3` also selects
   `testDecodeC30` and only the anchored `--filter '/C3$/'` selects the one test — and `--filter`
   alone searches every discovered tier, so it needs `--testsuite` or a path beside it. Both forms
   were checked on the PHPUnit 11.5.56 that core 11.4.5 resolves, against a deliberate `C30` sibling.
   A criterion group is a *second* group beside the module group every Drupal test class already
   carries; core stacks two `#[Group]` attributes on a class itself, so this is idiomatic rather than
   a local invention. A script reads the tags back out with `--list-groups`, or resolves one with
   `--list-tests --group <id>`. A test that specifies two criteria carries both names and both tags.

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

6. **Stop.** Return the tier, the path, the test names, the criterion each carries, and the failure
   output for each. Write no production code.

## Data flow

Input: one criterion, the behaviour it names, the declared interface, the module.
Output: one or more test files, and for each test the criterion it carries and the output of the run
that failed.
Boundaries: reads no production source; writes only under the module's test tree; runs no command
except through `drupal/test-execution.md`; produces no task record of its own.

## State-awareness contract

Before writing a new test, look for an existing test that already specifies the behaviour, by
searching the module's test tree for the criterion identifier and for the behaviour's own vocabulary.
Update the existing test rather than adding a second one that overlaps it. A bug fix almost always
belongs on the existing test for the behaviour that broke.

Do not read the production source to make that decision. The test tree is readable; the code is not.

## Verifier

- Each test carries its criterion identifier at the end of its method name and a matching
  `#[Group]` tag, so the criterion is both readable in the failure output and exactly selectable.
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
