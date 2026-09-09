---
# Routing block — an orchestrator reads to here and decides.
name: php_cli_test_authoring
capability: test-authoring
description: Use when a context is about to write the tests for one unit of work on a PHP CLI project, before any production code exists, and needs to know which level the behaviour belongs at, where the file goes, what the class and method are called, how the criterion it specifies is traced to it, and what a PHPUnit test may not do.
# Metadata — read only after a match.
label: Test authoring (PHP CLI)
recipe_schema_version: 1.0.0
version: 0.1.0
# Machine-readable dependency declaration (recipe-loader resolves these without parsing prose).
requires_guides:
  - development/tdd-spec-driven
# Process-recipe routing keys, enforced by validate_recipes.py for any recipe
# under docs/process-recipes/. `capability` above doubles as the phase; there is
# no separate applies_to_phase. `framework` is the second routing dimension.
recipe_class: process
framework: php-cli
assumes:
  - composer
authors:
  - name: camoa
license: GPL-2.0-or-later
---

## Goal

Answer four questions for whoever is about to write a PHP CLI test: which level the behaviour belongs
at, where the file goes and what the class and method are called, how the criterion it specifies is
recoverable from it, and what a PHPUnit test may not do.

**This recipe stops at red.** Its reader writes the test, watches it fail, and stops. It does not
write the code that turns the test green, and nothing here tells it to. The green and refactor half
of the cycle belongs to `php-cli/standards-and-tests.md`, read by a different context. Running the
test belongs to `php-cli/test-execution.md`, which several callers share.

The reader also cannot open the production source of anything already built. Every rule below is
therefore decidable from the behaviour the test must observe and from the names the unit declares.
A rule that needs the class in front of you is a rule this reader cannot follow.

## Opinion

**The level follows the dependency surface, decided from the behaviour and not from the code.**

| Level | Choose it when the behaviour needs | Cost |
|---|---|---|
| plain unit | nothing but the class and its arguments: construct it and assert on what comes back | milliseconds |
| unit with collaborators wired | its collaborators — real ones where they are cheap and deterministic, a double only at a boundary that must be isolated | milliseconds |
| integration / fixture | only the composed library API answers the question: real file I/O against a temp tree, a real config tree | tenths of a second |
| CLI end to end | the whole contract a user hits: run the built binary against a fixture tree and assert on stdout, stderr and the exit code | a process per test |

The CLI end-to-end level is this framework's real end-to-end shape. "No browser e2e" does not mean
the tool has no end-to-end test, and that level is written before the code like the other three.

**Where the file goes.** Under `tests/` at the project root, in the namespace `composer.json` maps
there under `autoload-dev`, mirroring the `src/` layout of the unit under test. The file is named
after the class and ends in `Test.php`. The authoritative file pattern is declared once, in
`php-cli/standards-and-tests.md` under `## Oracle files`, and is not repeated here.

**One test per behaviour the criterion names, and no more.** Past that, tests make the change harder
to review without specifying anything new. The full set of excess cases belongs to
`development/tdd-spec-driven` and is cited, not restated.

## Preconditions

This phase writes files and runs nothing itself, so it declares no machine-checkable environment
condition of its own. The condition for running a PHP CLI test — a configured runner against a
committed `phpunit.xml` or `phpunit.xml.dist` — is declared by `php-cli/test-execution.md`, beside
the commands it is a condition of. The step that watches a test fail reads it there.

```yaml
preconditions: []
```

## Input contract

```yaml
code_path: string             # absolute path to the project root
component: string             # the unit the behaviour belongs to
criterion_id: string          # the identifier of the criterion this test specifies
behavior: string              # what the test must observe, in a sentence
interface: string             # the names the unit declares, and the names its dependencies declare
test_level: string            # optional; unit | unit-with-collaborators | integration | cli-e2e
```

`interface` is the only thing this reader gets about code that already exists, and it is a
declaration rather than source. Where it is empty, the behaviour must be observable from the
library's public API or from the binary's own contract.

## Sequence

If invoked in dry-run mode, emit the level choice, the file path, the class and method names and the
assertions planned, and write nothing. Dry-run is required.

1. **Select the level.** From `behavior` and the dependency surface it implies, using the table in
   Opinion. Use `test_level` if supplied. If the behaviour cannot be placed without opening the code,
   stop and report that rather than guessing: the choice belongs earlier.

2. **Place and name the file.** `tests/<Path mirroring src>/<Name>Test.php`, class `<Name>Test`, in
   the namespace `autoload-dev` maps to `tests/`.

3. **Name the method so the runner collects it.** A method is collected only when its name begins
   with `test` or it carries the `#[Test]` attribute. Neither is a style preference: a method with
   neither is not collected and nothing says so — on PHPUnit 11.5 it simply does not appear in
   `--list-tests`, so the behaviour looks covered and is not.

4. **Name the criterion in the test, and tag it.** The criterion identifier goes at the end of the
   method name and nothing follows it: `testRejectsAnUnknownFlagC3()`. That keeps the criterion in
   the failure output and findable by grep with no runner support. For **selection**, add
   `#[Group('c3')]` to the method as well, because the group is the mechanism PHPUnit gives that the
   name cannot match: `--group c3` is an **exact** match, while `--filter` is a regular expression
   over the test identifier, so `--filter C3` also selects `testDecodeC30` and only the anchored
   `--filter '/C3$/'` selects the one test. Both were checked on PHPUnit 11.5.56 against a deliberate
   `C30` sibling. A script reads the tags back out with `--list-groups`, or resolves one with
   `--list-tests --group <id>`. A test that specifies two criteria carries both names and both tags.

5. **Write the test, shaped Arrange-Act-Assert.** A data provider is declared with
   `#[DataProvider('name')]` and the provider method **must be static** — see Verifier for what
   happens when it is not. Assert on what the criterion names, and nothing else.

6. **Watch it fail.** Run it through `php-cli/test-execution.md` and read the failure signal declared
   there, never the exit status alone — a selector that matched nothing exits 0. Only an assertion
   that ran and did not hold is a red run. A test that passes immediately is rewritten once; if it
   still passes with no code behind it, stop and report it as proving nothing.

7. **Stop.** Return the level, the path, the class and method names, the criterion each carries, and
   the failure output for each. Write no production code.

## Data flow

Input: one criterion, the behaviour it names, the declared interface, the unit.
Output: one or more test classes under `tests/`, and for each test the criterion it carries and the
output of the run that failed.
Boundaries: reads no production source; writes only under the test tree and its fixtures; runs no
command except through `php-cli/test-execution.md`; produces no task record of its own.

## State-awareness contract

Before writing a new test, look for an existing test that already specifies the behaviour, by
searching the test tree for the criterion identifier, for the group tag, and for the behaviour's own
vocabulary. Add a case to the existing class rather than adding a second one that overlaps it. A bug
fix almost always belongs on the existing test for the behaviour that broke.

Do not read the production source to make that decision. The test tree is readable; the code is not.

## Verifier

- Each test carries its criterion identifier at the end of its method name and a matching
  `#[Group]` tag, so the criterion is both readable in the failure output and exactly selectable.
- Each test class sits under `tests/` in the namespace `autoload-dev` maps there, and its file name
  ends in `Test.php`.
- Every test method begins with `test` or carries `#[Test]`. A method with neither is not collected
  and nothing reports it.
- Every data provider method is `static`. On PHPUnit 11.5 a non-static provider makes the **whole
  class** collect nothing: the run reports `is not static`, then `No tests found in class`, then
  `No tests executed!`, and exits 2 — so a class whose only provider was written non-static
  contributes zero tests to a run that otherwise looks fine.
- Each new test was seen to fail, and the recorded failure is an assertion that ran and did not hold
  rather than a harness error or a run that selected nothing.
- No test pins the exact wording of the tool's own prose output. The exit code and any
  machine-readable output are contracts; the prose around them is not. Where a behaviour has no
  surface but prose, that is a finding about the tool — give it an exit code or a machine-readable
  mode — not a reason to assert harder.
- No production file was written or changed.

## References

### Stack-neutral discipline (referenced, not authored here)

| Guide | What it holds |
|---|---|
| `development/tdd-spec-driven` | What a failing test proves, when not to write a test at all, the anti-patterns, and when a double is legitimate. Written for one person doing red, green and refactor; this reader does red and stops |

### Sibling process recipes

| Recipe | What it holds |
|---|---|
| `php-cli/test-execution.md` | The command at each scope, its cost, the condition for running one, and how to read what came back |
| `php-cli/standards-and-tests.md` | The green and refactor half, PSR-12 and strict types, the flag and exit-code coverage rule, and the `## Oracle files` declaration that names the test file pattern |

### External origins (referenced, not authored here)

| Origin | What it settled |
|---|---|
| PHPUnit 11.5.56 | That a method with neither a `test` prefix nor `#[Test]` is not collected and nothing says so; that `--group` matches exactly while `--filter` is an unanchored regular expression; that a non-static data provider makes the whole class collect nothing and exit 2 |
