---
# Routing block — an orchestrator reads to here and decides.
name: drupal_module_test_authoring
capability: drupal-module-test-authoring
description: Use when a Drupal module needs tests written or extended — deciding which kind of test each behaviour gets, writing it to the conventions current core and PHPUnit enforce, and proving the run actually collected it.
# Metadata — read only after a match.
label: Drupal module test authoring
recipe_schema_version: 1.0.0
version: 0.1.0
# Machine-readable dependency declaration (recipe-loader resolves these without parsing prose).
requires_guides:
  - drupal/testing/framework-selection-decision-matrix
  - drupal/testing/phpunit-unit-tests
  - drupal/testing/phpunit-kernel-tests
  - drupal/testing/phpunit-functional-tests
  - drupal/testing/phpunit-functionaljavascript-tests
  - drupal/testing/testing-infrastructure-setup
  - drupal/testing/running-debugging-tests
  - drupal/tdd/test-type-decision-matrix
  - drupal/tdd/nightwatch-testing
drupal_compatibility: "^10.3 || ^11"
authors:
  - name: Palcera
license: GPL-2.0-or-later
---

## Goal

Give a module the tests its behaviours deserve: one kind chosen per behaviour rather than one kind for the module, written so the runner collects them, and proved by a run whose output the author read. The recipe owns the choice and the proof. The mechanics of each kind — base class, directory, namespace, setup calls — belong to the guides it cites and are not restated here.

## Opinion

**Start at Kernel and move only for a reason.** A Kernel test boots the container, installs the modules it names, and reaches the database, which covers most of what a Drupal module is: services, entities, plugins, hooks, configuration. Move down to Unit only when the code under test touches no container at all. Move up to Functional only for a reason this recipe names. The two mature contrib modules surveyed for this recipe write Kernel over Functional by 141 to 2 and 194 to 65, and core is converting Functional tests to Kernel where coverage allows because the conversion cuts about three quarters of the runtime.

**From Drupal 11.4, needing to read a page is no longer a reason to go Functional.** `KernelTestBase` uses `Drupal\Tests\HttpKernelUiHelperTrait`, so every Kernel test has `drupalGet()`, `clickLink()` and `assertSession()` without opting in, and sends its request through the HTTP kernel. What a Kernel test still cannot do: submit a form, log in, run JavaScript, or answer anything that needs a real web server — `submitForm()` and `drupalLogin()` exist on `BrowserTestBase` only. Those four are the reasons to go Functional, and the only ones. On Drupal 10 the older rule holds: no `drupalGet()` at all, so reading a page is Functional's job there.

**A kind of test the project's pipeline does not run is worse than no test.** It is written, it is reviewed, it reports nothing, and it looks like coverage. One of the surveyed modules refuses Build, FunctionalJavascript and Component tests through its own coding-standards rule for exactly this reason, saying so in the rule: without the guard "tests of these types would silently never execute, appearing to pass in CI when they have not run at all." Before choosing a kind, establish that the pipeline runs it. If it does not, either add pipeline support first or choose a kind that runs.

**Read the status line, never the exit code alone.** A run that selected nothing prints `No tests executed!` and exits 0 — it did not pass, it did not run, and the exit code says nothing about it. `FAILURES!` means a test ran and an assertion did not hold. `ERRORS!` means something broke before the assertion, whatever the assertion count. An author who reports "tests pass" without quoting the status line has not checked.

**Cite the skill for the traps it already carries.** The `drupal-automated-testing` skill in `ai_best_practices` is the current source on the unasserted `waitForElement`, the dual-container trap in Functional tests, and the per-kind namespaces including the `FunctionalJavascript` capitalisation. This recipe does not restate them. It parts company with that skill in two places. The skill makes Functional the default and this recipe starts at Kernel, for the reasons above. And from Drupal 11.4 reading a page stopped being a reason to reach for Functional, which the skill predates.

## Preconditions

- Drupal 10.3+ or 11.x, Composer-managed, with core's development dependencies installed so PHPUnit resolves.
- A `phpunit.xml` the project owns, at the project root beside `composer.json`, with its `bootstrap=`, its testsuite directories and its browser-output directory written for that location, and `SIMPLETEST_DB` filled in. `drupal/testing/testing-infrastructure-setup` is the reference; a run against core's own configuration is not this recipe's form.
- The module exists and its `.info.yml` is in place. Nothing here scaffolds a module, and a test cannot be watched to fail against a module the extension scan cannot find.
- For Kernel and above, a database the runner can reach. For Functional, a served site. For FunctionalJavascript, a WebDriver endpoint.
- Knowledge of which kinds the project's pipeline actually runs. If that cannot be established, this recipe's first sequence step surfaces it as a finding rather than guessing.

## Input contract

Generic, source-agnostic, supplied by the caller (adapter skill, human operator, or orchestrator).

```yaml
core_version: string           # the project's Drupal version, e.g. 11.4.5; the choice in
                               # sequence step 2 branches on 11.4

module:
  name: string                 # machine name
  path: string                 # path to the module, relative to the docroot

behaviours:                    # one entry per thing to be proved
  - id: string                 # caller's identifier, echoed in the report
    statement: string          # what must be true, in one sentence
    touches:                   # what the behaviour reaches, used to choose the kind
      container: boolean       # needs services, entities, config or the database
      page: boolean            # a response must be read
      form_submission: boolean # a form must be submitted, or a user logged in
      served_site: boolean     # needs a real web server: a redirect, a real session,
                               # a header only the server sets
      javascript: boolean      # behaviour only exists with JS or Ajax running

pipeline_runs:                 # the kinds the project's pipeline executes
  - string                     # unit | kernel | functional | functional-javascript

existing_tests: boolean        # whether the module already has a test suite to extend
```

## Sequence

1. **Establish what the pipeline runs.** Read the project's pipeline configuration and record which kinds it executes. A kind absent from it is unavailable to this recipe; report that as a finding before any test is written, because a test of that kind would never run.

2. **Choose the kind per behaviour, not per module.** Ask these in order and stop at the first yes. The order is the rule: a behaviour that is both an Ajax interaction and a form submission is FunctionalJavascript, because the first question catches it.

   1. Does the behaviour need JavaScript or Ajax running? → FunctionalJavascript.
   2. Does it submit a form, need a logged-in session, or need a real web server? → Functional.
   3. Does it read a page, on a project whose `core_version` is below 11.4? → Functional, because a Kernel test has no `drupalGet()` there.
   4. Does it reach the container — a service, an entity, configuration or the database — or does it read a page on 11.4 or later? → Kernel.
   5. Otherwise → Unit.

   Record the reason beside the choice; a choice with no reason is a default in disguise. `drupal/testing/framework-selection-decision-matrix` and `drupal/tdd/test-type-decision-matrix` carry the long form.

3. **Write the test to the kind's guide.** `drupal/testing/phpunit-unit-tests`, `drupal/testing/phpunit-kernel-tests`, `drupal/testing/phpunit-functional-tests` and `drupal/testing/phpunit-functionaljavascript-tests` each carry the base class, directory, namespace and setup calls. Four things this recipe requires on top, because the runner or core enforces them and a guide example is easy to copy past: every Kernel, Functional and FunctionalJavascript class declares `#[RunTestsInSeparateProcesses]` and no Unit class does; the attribute is not inherited, so a project's own test base class cannot carry it for its subclasses; every data provider is `static` and named by `#[DataProvider]`; and metadata goes in attributes, not doc-comments.

4. **Watch each new test fail before the code exists, and read why it failed.** A test that has never been seen red proves nothing about the behaviour. The failure must be an assertion that ran and did not hold, not a harness error and not a run that selected nothing. For a class that does not exist yet, open the test with one assertion that names it so the first run fails an assertion instead of erroring in autoload.

5. **Run, and read the status line.** Run the narrowest scope that covers the new tests, with the project's own configuration named. Quote the status line and the counts in the report. `No tests executed!` is not a pass. A path argument and `--testsuite` do not combine — the path wins and the flag is ignored — so pass one or the other, never both.

6. **Report per behaviour.** Each behaviour in the input gets its chosen kind, the reason, the test's file and method, the status line of the run that proved it, and for a behaviour no test covers, why not. A behaviour whose kind the pipeline does not run is reported as uncovered, whatever was written for it.

## Data flow

```
input:  core_version, module, behaviours[], pipeline_runs[],     supplied by the caller
        existing_tests

step 1: the project's pipeline configuration    → kinds available; kinds refused, as findings
step 2: behaviours[].touches + core_version     → kind per behaviour + recorded reason
step 3: the kind's guide + this recipe's four   → test files under <module>/tests/src/<Kind>/
        requirements
step 4: the runner, narrowest scope             → a red per new test, with its status line
step 5: the runner, narrowest scope             → the status line and counts per run
step 6: everything above                        → report, one row per input behaviour
```

## State-awareness contract

Re-running this recipe over a module that already has tests extends rather than replaces. A behaviour whose test already exists and already passes is left alone and reported as covered; its file is not rewritten to this recipe's shape unless it is the behaviour being changed. Test files this recipe writes are the only files it writes: it never edits production code to make a test pass, and it never scaffolds a module. Step 4 leaves the module red by design, and the red is the recipe's output, not a failure of it. Nothing here writes to the project's `phpunit.xml`; a configuration that cannot run the chosen kind is a precondition failure, reported, not repaired.

## Verifier

Each check names what the consumer runs and what makes it pass.

1. **`config-assert` — every class carries the attribute its kind requires.** Read each new test file. Every class extending `KernelTestBase`, `BrowserTestBase` or `WebDriverTestBase` declares `#[RunTestsInSeparateProcesses]` with the matching `use` statement; no class extending `UnitTestCase` declares it; and no abstract base class is relied on to supply it, because the attribute is not inherited. Fails on the first class missing it.

2. **`config-assert` — no data provider is an instance method.** Read each new test file. Every method named by a `#[DataProvider]` is declared `static`. A non-static provider drops every test it feeds. When that is the only test in the class the run prints `No tests found in class` and `No tests executed!`; when the class has other tests it keeps them and prints `ERRORS!`. Neither outcome asserts the provider's cases.

3. **`config-assert` — no metadata sits in a doc-comment.** No new test file uses `@group`, `@covers`, `@coversDefaultClass` or `@dataProvider`. The runner prints a deprecation for each and drops support in PHPUnit 12.

4. **`config-assert` — every behaviour in the input is accounted for.** The report has one row per behaviour, each with a kind, a reason, and either a test with its status line or a stated reason for no test. A behaviour silently absent from the report fails this check.

5. **`live-site` — the tests run and the status line says so.** Run the new tests with the project's configuration. Unit tests need no site; Kernel and above need a database, and Functional a served site. The run prints `OK` with a non-zero test count, and prints neither `No tests executed!` nor `ERRORS!`. In an environment with no database or no served site this check cannot run, and that is a correct fail-close rather than a recipe defect: the consumer halts and says which environment piece is missing.

6. **`self-fixture` — a passing test can be made to fail.** For one behaviour of the caller's choosing, invert a single assertion in a copy of the test, run it, and confirm the run prints `FAILURES!` rather than `OK`; then discard the copy. A test that passes both ways is asserting nothing about the behaviour. The fixture is the copy, and the check removes it.

## References

| Source | What it settles |
|---|---|
| [Framework selection decision matrix](../../drupal/testing/framework-selection-decision-matrix.md), [Test type decision matrix](../../drupal/tdd/test-type-decision-matrix.md) | The long form of the choice this recipe sequences |
| [Unit](../../drupal/testing/phpunit-unit-tests.md), [Kernel](../../drupal/testing/phpunit-kernel-tests.md), [Functional](../../drupal/testing/phpunit-functional-tests.md), [FunctionalJavascript](../../drupal/testing/phpunit-functionaljavascript-tests.md) | Base class, directory, namespace, setup calls and the traps of each kind |
| [Testing infrastructure setup](../../drupal/testing/testing-infrastructure-setup.md), [Running and debugging tests](../../drupal/testing/running-debugging-tests.md) | Where `phpunit.xml` lives, what must be rewritten in it, and how a run is scoped |
| [Nightwatch testing](../../drupal/tdd/nightwatch-testing.md) | Why JavaScript coverage is a FunctionalJavascript test rather than a Nightwatch one, and what core's replacement policy has and has not landed |
| `ai_best_practices`, skill `drupal-automated-testing` | The unasserted `waitForElement`, the dual-container trap, the per-kind namespaces. Cited, not restated; this recipe differs from it only on reading a page from a Kernel test, and only from Drupal 11.4 |
| Drupal core 11.4.5 — `KernelTestBase`, `HttpKernelUiHelperTrait`, `BrowserTestBase` | That a Kernel test can read a page but cannot submit a form or log in; that omitting the separate-processes attribute is deprecated as of 11.3 and throws in 12 |
| PHPUnit 11.5.56 | That a non-static data provider asserts nothing; that a run selecting nothing prints `No tests executed!` and still exits 0; that doc-comment metadata is deprecated; that a path argument overrides `--testsuite` |
