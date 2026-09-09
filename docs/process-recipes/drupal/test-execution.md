---
# Routing block — an orchestrator reads to here and decides.
name: drupal_test_execution
capability: test-execution
description: Use when anything needs to run a Drupal test — the failing-test step watching one case, a baseline taken before code exists, a build check running a tier, or a fixer running the tests over its change — and needs the command, its cost, and how to tell a failed assertion from a harness that never reached the behaviour.
# Metadata — read only after a match.
label: Test execution (Drupal)
recipe_schema_version: 1.0.0
version: 0.1.0
# Machine-readable dependency declaration (recipe-loader resolves these without parsing prose).
requires_guides:
  - drupal/testing
# Process-recipe routing keys, enforced by validate_recipes.py for any recipe
# under docs/process-recipes/. `capability` above doubles as the phase (the
# lifecycle moment the orchestrator resolves on); there is no separate
# applies_to_phase. `framework` is the second routing dimension.
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

Answer one question for a Drupal project: what command runs a test, at each of the scopes something actually asks for — the whole suite, one file, one case, the tests covering a change, and the cheapest thing that proves the runner works at all. Carry the traps that make a Drupal test command mean something other than what it reads as, the cost of each tier, and the output that separates a failed assertion from a harness that never reached the behaviour.

This recipe runs nothing and judges nothing. It is read by whatever is about to run a test, and the callers differ: the author watching one case fail, the baseline taken over the files a change touches before any code exists, each build check running a tier, and the fixer running the tests that cover its own change. One answer, four callers — which is why it is a file rather than a paragraph inside the phase that writes the code.

## Opinion

**A command is argv, never a shell string.** Each row below is a list of tokens executed directly. A token that is exactly a named placeholder is replaced whole, and the substituted value never reaches a shell. This is the rule `check:` already lives under, for the same reason: a recipe is data written elsewhere, and a command written expecting a shell would quietly mean something other than what its author read.

**`--testsuite` scopes a tier; `--filter` does not.** `--filter` matches against the test identifier, so a tier name handed to it catches whatever happens to contain that string and misses the rest. The tier is `--testsuite`, and the tier names are the ones core's own `phpunit.xml.dist` declares.

**A `--filter` that matches nothing exits zero.** PHPUnit prints `No tests executed!` and reports success, so a mistyped case name is indistinguishable from a passing run by exit code alone. Anchor the filter (`/::testName$/`) and read the test count, because an unanchored `testFoo` also selects `testFooBar`.

**Zero assertions is the tell that the harness never ran.** A Kernel test with no `SIMPLETEST_DB` reports `ERRORS!` with `Assertions: 0` and exits 2 — the same exit code as a mistyped option. A test that errors before it asserts has said nothing about the behaviour, and treating it as a red is how a phase concludes that absent code is proven absent when the database was simply not there.

**The four tiers differ by an order of magnitude, so they carry different costs.** Unit and Kernel are cheap enough to run on every build attempt over the changed scope. Functional boots a real site per test; FunctionalJavascript adds a browser on top of that. Both belong at the end of a task, not inside the loop. A caller with no cost label either runs the cheapest thing and under-checks, or runs everything on every attempt and pays for a full site boot per attempt.

**Drupal has no changed-file test selection, and saying so is the answer.** No flag maps a set of changed paths to the tests that cover them. The caller passes the test file paths it decided cover the change, and every run therefore has a scope somebody chose rather than one the tool derived.

## Preconditions

- A Drupal 10.3+ or 11.x project, Composer-managed, with the runner reachable through the invocation the project documents — a `ddev phpunit` custom command, or `ddev exec vendor/bin/phpunit` — and the environment the tier needs: `SIMPLETEST_DB` for Kernel and above, plus `SIMPLETEST_BASE_URL` for Functional and FunctionalJavascript. See `drupal/testing` for the runner configuration.
- The DDEV environment is running. Every command below executes inside it.

The environment condition is declared in machine-readable form below. What it probes is exactly what it claims: that the DDEV environment is up. It does not claim the database variables are set, which is why the first bullet stays prose.

**Two checks were rejected before this one, and the reasons are worth keeping.** `test -x vendor/bin/phpunit` answers a different question from the one the condition asks: Composer installs that binary on any Drupal project that requires core-dev, so it is present and executable with DDEV stopped and nothing set, and the entry reported `met` while no test in any tier could run. And `ddev exec`, the obvious way to probe the documented path, **starts a stopped project** — observed here, where the containers were built and started by the probe. A check decides whether to proceed and must not change the thing it is deciding about.

`ddev describe -j` does neither. Verified on DDEV v1.25.4: it leaves a stopped project stopped, and it reports the state as JSON. Its exit status is 0 whether the project is running or not, so the answer is in what it printed, which is what `expect:` reads.

**The key is `status_desc`, and the reason is worth knowing before someone shortens it.** The obvious literal, `"status":"running"`, is wrong: `status` appears once per service as well as once for the project, so a **paused** project reports `"status":"paused"` at the top and still prints `"status":"running"` for any service that stayed up — observed on a paused project whose web and database containers had exited. That environment cannot run a test and the naive string says it can. `status_desc` appears exactly once in the document and carries the project's own state, so it decides all three states correctly: present when running, absent when stopped, absent when paused.

**The expectation names the state it wants, never the one it rejects.** A running project prints `"status":"stopped"` too, for any optional service that is not up, so a test for the absence of that string would fail on a healthy environment. Presence is the answer.

One limit, in the safe direction. The literal includes the closing quote, so it matches only a value of exactly `running`. If a future DDEV appends detail to that field, the check reports the condition unmet and the phase stops, rather than proceeding on a stale reading.

What this still does not decide is `SIMPLETEST_DB`. It reaches the runner either from the container environment or from an `<env>` element in the project's own `phpunit.xml`, and a check is one command that never passes through a shell, so the two places cannot be combined. That condition stays prose, and a Kernel test erroring with `Assertions: 0` is how it surfaces — see the failure signal below.

```yaml
preconditions:
  - id: test-runner
    what: a running DDEV environment, so the runner the project documents can be reached at all
    check: ddev describe -j
    expect: '"status_desc":"running"'
    owner: code-quality-tools:setup
```

## Input contract

Source-agnostic, supplied by the caller.

```yaml
code_path: string             # absolute path to the Drupal project root
scope: string                 # suite | file | test | changed | smoke — the row to resolve
tier: string                  # optional; unit | kernel | functional | functional-javascript
file: string                  # optional; one test file path, for the `file` row
test_id: string               # optional; one test identifier, for the `test` row
paths: [string]               # optional; the test files a change is scoped to
```

## Test commands

Five rows. Each is a command or a named statement that Drupal has none. `{file}` is one test file path, `{test_id}` one anchored filter, `{tier}` one testsuite name, and `{paths}` a list that expands to one token per element.

`ddev phpunit` is the project-defined custom command the preconditions name. Where a project has not defined one, the same argv reads `ddev exec vendor/bin/phpunit -c web/core` and everything else holds.

```yaml
test_commands:
  - id: suite
    argv: ["ddev", "phpunit"]
    cost: end-of-task
    trap: >-
      Runs every tier, Functional and FunctionalJavascript included, each booting a
      real site. This is the end-of-task gate, not something to run inside a loop.
  - id: file
    argv: ["ddev", "phpunit", "{file}"]
    cost: every-attempt
    trap: >-
      Cost follows the tier the file belongs to, not the fact that it is one file.
      One FunctionalJavascript file is not an every-attempt command.
  - id: test
    argv: ["ddev", "phpunit", "{file}", "--filter", "{test_id}"]
    id_form: >-
      An anchored regex against the test identifier, `/::testName$/`. Unanchored
      `testName` also selects `testNameSomethingElse`.
    cost: every-attempt
    trap: >-
      A filter that matches nothing prints `No tests executed!` and exits 0, so a
      mistyped identifier reports success. Read the test count, not the exit code.
  - id: changed
    absent: >-
      Drupal ships no flag that maps changed paths to the tests covering them. The
      caller decides which test files cover the change and passes them.
    nearest: ["ddev", "phpunit", "{paths}"]
  - id: smoke
    argv: ["ddev", "phpunit", "--list-suites"]
    cost: every-attempt
    trap: >-
      Proves the configuration parses and the suites resolve inside the running
      environment. It does not prove `SIMPLETEST_DB` is set, which only a Kernel
      test reaching a database proves.
```

**Tiers and what they cost.** Core's `phpunit.xml.dist` declares six testsuites, not four: `unit-component`, `unit`, `kernel`, `functional`, `functional-javascript` and `build`. The four the implement phase selects among are the middle ones; a caller passing `--testsuite` sees all six and should not invent a name.

| Tier | `--testsuite` | Cost | Run it |
|---|---|---|---|
| Unit | `unit` | milliseconds per test, no bootstrap | every build attempt |
| Kernel | `kernel` | seconds per test, minimal container and an installed schema | every build attempt, over the changed scope |
| Functional | `functional` | a real site boot per test | once, at the end of a task |
| FunctionalJavascript | `functional-javascript` | a site boot plus a browser session per test | once, at the end of a task |

**Telling a failed assertion from harness noise.** PHPUnit's exit code is not enough on its own, because 2 covers both a test that errored and a runner that was misused. The counts line is what separates them: a run that reached the behaviour has assertions.

```yaml
failure_signal:
  assertion: >-
    Exit 1, with `FAILURES!` and a counts line carrying a non-zero assertion count —
    the test ran, asserted, and the assertion did not hold. This is the only outcome
    that proves a behaviour is absent.
  harness: >-
    Exit 2 with `ERRORS!` and a zero assertion count — the run never reached a
    behaviour. Verified on core 11.4.5 with `SIMPLETEST_DB` unset, which errors on
    every test with "There is no database connection so no tests can be run" rather
    than skipping. Exit 2 also covers a missing test file and an unknown option,
    which print no counts line at all. Exit 255 is a PHP fatal before any test ran.
  silent_pass: >-
    Exit 0 with `No tests executed!` — a filter or a path matched nothing. Success
    and "nothing ran" are the same exit code, so the counts line is the only thing
    that distinguishes them.
```

**Three Drupal-specific sources of noise worth naming**, because each produces a red that proves nothing about the code:

- A Kernel test failing on a missing table is a setup gap, not an absent behaviour. Kernel tests install nothing on their own; `installEntitySchema()`, `installConfig()` and `installSchema()` are the test's own calls.
- A Functional test runs two Drupal instances sharing one database and holding separate memory — one in PHPUnit, one in the web server. State set in the test process is not visible to the site under test, and a failure caused by that boundary is not the behaviour missing.
- On 11.3 and later, a Kernel, Functional or FunctionalJavascript class without `#[RunTestsInSeparateProcesses]` triggers a deprecation. It is a deprecation today and becomes an exception in Drupal 12; where a project sets `SYMFONY_DEPRECATIONS_HELPER` to fail the run, every such class fails for that reason and for no other.

## Sequence

If invoked in dry-run mode, resolve and return the command without executing it. Dry-run is required.

1. **Resolve the row.** Take `scope` and select the matching row above. A row answered with `absent:` returns that statement and its `nearest:` form; it does not fall through to a wider command.

2. **Substitute the placeholders.** Replace each placeholder token whole, from the caller's input. A list placeholder expands to one token per element. Nothing is concatenated into a token, and nothing is passed through a shell.

3. **Apply the cost label.** Return the row's `cost` with the command, so the caller running on every build attempt does not receive a command that boots a site per test.

4. **Return the command, the cost, and the failure signal.** The caller runs it. This recipe neither executes it nor judges its output.

5. **Read the result against the failure signal.** Whatever ran the command reads the counts line before the exit code: assertions greater than zero with failures is a red that proves something; zero assertions, or `No tests executed!`, is a run that said nothing and must not be reported as either red or green.

## Data flow

```
input: code_path, scope, tier (optional), file / test_id / paths (optional)

reads project state:
       the project's documented invocation (a ddev phpunit custom command, or
                                            ddev exec vendor/bin/phpunit -c web/core)
       core's phpunit.xml.dist — the six testsuite names
       the project's own phpunit.xml, where it declares SIMPLETEST_DB itself

applies opinion:
       argv, never a shell string · --testsuite scopes a tier, --filter does not ·
       an anchored filter, because an unanchored one over-selects · a filter that
       matches nothing exits 0 · zero assertions means the harness never ran ·
       tier cost decides every-attempt versus end-of-task

references origin (never duplicated):
       drupal/testing — the tier base classes, the runner configuration, the env vars

emits (to the caller; the recipe runs nothing):
       command:  the argv token list for the requested row, placeholders substituted
       cost:     every-attempt | end-of-task
       signal:   how to read the output — assertion, harness, or nothing ran
```

## State-awareness contract

The recipe reads. It writes no file, runs no command, starts no container, and records nothing against the task. The one state it depends on is the DDEV environment already running, and it deliberately declines to probe that, because the only command that would is one that starts it.

Idempotent by construction: resolving the same row with the same input returns the same command. What the command then does depends on the project's state, which is the caller's to observe and this recipe's to explain.

## Verifier

After the recipe runs, verify:

1. The returned command is a token list, and every placeholder was substituted as a whole token — nothing was concatenated into a token and nothing reached a shell.
2. The row requested was the row returned. A row answered `absent:` returned that statement, not a wider command that happens to include the wanted tests.
3. A command scoping a tier used `--testsuite` with one of core's declared suite names, never `--filter`.
4. A command selecting one case used an anchored filter, and the run's test count was read rather than its exit code alone.
5. The cost label travelled with the command, and no caller running on every build attempt received a Functional or FunctionalJavascript command.
6. Any result reported as red carried a non-zero assertion count. A run reporting `Assertions: 0`, or `No tests executed!`, was reported as having said nothing rather than as a pass or a failure.

This recipe ships no executable verifier of its own — it produces a command and the means to read the result, and the phase that runs it owns the gate.

## References

### Drupal guides (referenced, not authored here)

| Source | Used for |
|---|---|
| `drupal/testing` | The Unit / Kernel / Functional / FunctionalJavascript base classes, the runner configuration, and the environment variables each tier needs |

### External origins (referenced, not authored here)

| Source | Used for |
|---|---|
| Drupal core `core/phpunit.xml.dist` | The six declared testsuite names and the environment variables the tiers read |
| PHPUnit 11 | The exit codes and the counts line the failure signal reads |
| DDEV (`ddev phpunit`, `ddev exec`) | The invocation path every command runs through |

### Plugin-side generic mechanism (ai-dev-assistant)

The phases that run these commands — the failing-test step, the baseline, the build checks, the fixer — are the plugin's, along with whatever records their results. This recipe supplies only what Drupal cannot be guessed at: the command per scope, its cost, and how to read what came back.
