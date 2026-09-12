---
# Routing block — an orchestrator reads to here and decides.
name: php_cli_test_execution
capability: test-execution
description: Use when anything needs to run a PHP CLI project's tests — the failing-test step watching one case, a baseline taken before code exists, a build check running the suite, or a fixer running the tests over its change — and needs the command, its cost, and how to tell a failed assertion from a runner that was misused.
# Metadata — read only after a match.
label: Test execution (PHP CLI)
recipe_schema_version: 1.0.0
version: 0.2.0
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

Answer one question for a PHP CLI project: what command runs a test, at each of the scopes something actually asks for — the whole suite, one file, one case, the tests covering a change, and the cheapest thing that proves the runner works at all. Carry the traps that make a PHPUnit invocation select more or fewer tests than it reads as, and the output that separates a failed assertion from a runner that was misused.

This recipe runs nothing and judges nothing. It is read by whatever is about to run a test, and the callers differ: the author watching one case fail, the baseline taken before any code exists, each build check, and the fixer running the tests over its own change.

## Opinion

**A command is argv, never a shell string.** Each row below is a list of tokens executed directly. A token that is exactly a named placeholder is replaced whole, and the substituted value never reaches a shell.

**A `--filter` matches a substring of the test identifier, so it over-selects.** `--filter testPasses` also runs `testPassesToo` — observed on PHPUnit 11.5.56. Anchor it as a regular expression, `/::testPasses$/`, when one case is what was asked for.

**A `--filter` that matches nothing exits zero.** PHPUnit prints `No tests executed!` and reports success, so a mistyped case name is indistinguishable from a passing run by exit code alone. Read the test count.

**Exit 2 means two different things and only one of them is about the code.** A test that threw an uncaught exception exits 2 with `ERRORS!` and a counts line; a missing test file or an unknown option also exits 2, with a bare message and no counts line at all. The first is a real observation about the code, the second is a runner that never started. The counts line is what tells them apart.

**A filesystem probe of the runner is honest here, and that is worth stating.** `test -x vendor/bin/phpunit` genuinely probes the documented invocation for this framework, because a PHP CLI project runs the binary directly with no container between the caller and the runner. The same check on a containerised stack answers a different question from the one it appears to; here it does not.

**PHPUnit has no changed-file test selection, and saying so is the answer.** No flag maps a set of changed paths to the tests that cover them. `--group` selects what an author annotated, which is a different thing. The caller passes the test file paths it decided cover the change.

## Preconditions

- A PHP project, Composer-managed, with a configured PHPUnit runner — `php vendor/bin/phpunit` against a committed `phpunit.xml` or `phpunit.xml.dist`.

Declared in machine-readable form below, with the owner it already had. The check is a genuine probe of the invocation the commands use, not a proxy for it: the binary the check names is the binary every row below runs.

```yaml
preconditions:
  - id: test-runner
    what: a PHPUnit runner whose failure the failing-test step can observe
    check: test -x vendor/bin/phpunit
    owner: code-quality-tools:setup
```

## Input contract

Source-agnostic, supplied by the caller.

```yaml
code_path: string             # absolute path to the PHP project root
scope: string                 # suite | file | test | changed | smoke — the row to resolve
file: string                  # optional; one test file path
test_id: string               # optional; one anchored --filter regular expression
paths: [string]               # optional; the test files a change is scoped to
```

## Test commands

Six rows. Each is a command or a named statement that this framework has none. `{file}` is one test file path, `{test_id}` one anchored filter, and `{paths}` a list that expands to one token per element.

```yaml
test_commands:
  - id: suite
    argv: ["php", "vendor/bin/phpunit"]
    cost: end-of-task
    trap: >-
      Runs every suite the configuration declares, the fixture-driven CLI
      end-to-end tier included, which spawns the built binary once per case.
  - id: file
    argv: ["php", "vendor/bin/phpunit", "{file}"]
    cost: every-attempt
    trap: >-
      A path argument overrides the configured suites, so a file outside the
      configured test tree still runs. That is useful and it also means a typo in
      the path is an error rather than a silently empty run — exit 2, not exit 0.
  - id: test
    argv: ["php", "vendor/bin/phpunit", "{file}", "--filter", "{test_id}"]
    id_form: >-
      An anchored regular expression against the test identifier, `/::testName$/`.
      A bare `testName` matches as a substring and also selects `testNameToo`.
    cost: every-attempt
    trap: >-
      A filter that matches nothing prints `No tests executed!` and exits 0, so a
      mistyped identifier reports success. Read the test count, not the exit code.
  - id: changed
    absent: >-
      PHPUnit maps no set of changed paths to the tests covering them. `--group`
      selects what an author annotated, which answers a different question. The
      caller decides which test files cover the change and passes them.
    nearest: ["php", "vendor/bin/phpunit", "{paths}"]
  - id: smoke
    argv: ["php", "vendor/bin/phpunit", "--list-suites"]
    cost: every-attempt
    trap: >-
      Proves the configuration parses, the bootstrap loads and the suites resolve.
      It runs no test, so it proves nothing about behaviour.
  - id: mutation
    argv: ["php", "vendor/bin/infection", "run", "--no-interaction", "{paths}"]
    cost: end-of-task
    trap: >-
      A report, not a gate. Infection 0.35 exits 0 whatever the score unless
      `--min-msi` is passed; the score is the `Mutation Score Indicator (MSI)` line and
      the survivors are the `Escaped mutants` section, twenty by default. It needs an
      `infection.json5` naming the source directories and a coverage driver (pcov or
      Xdebug); the fixture-driven end-to-end tier spawns the binary once per case per
      mutant, so `--only-covering-test-cases` is the difference between a run that
      finishes and one that does not.
```

**The mutation row takes its files as positional arguments.** `--filter` is deprecated since
Infection 0.34 and refused when paths are also given, so the row passes the changed files as
`{paths}`, one token each, which is the form 0.35.4's own help documents. `--no-interaction` is
what makes a missing configuration an error rather than a prompt the caller cannot answer. Read
from the installed tool's help; the host PHP carries no coverage driver, so the run itself was not
observed.

**What each row costs.** The tiers this framework's implement recipe selects among differ mostly at the end-to-end boundary.

| Tier | Cost | Run it |
|---|---|---|
| Plain unit, unit with collaborators | milliseconds per test | every build attempt |
| Integration / fixture | seconds, composed library API | every build attempt, over the changed scope |
| CLI end-to-end | a process spawn per case, against a fixture tree | once, at the end of a task |

**Telling a failed assertion from harness noise.** All exit codes below were observed on PHPUnit 11.5.56.

```yaml
failure_signal:
  assertion: >-
    Exit 1 with `FAILURES!` and a counts line carrying a non-zero assertion count —
    the test ran, asserted, and the assertion did not hold. This is the only outcome
    that proves a behaviour is absent.
  harness: >-
    Exit 2. It covers two different things and the counts line separates them: with
    `ERRORS!` and a counts line, a test threw before it asserted; with a bare message
    and no counts line ("Test file ... not found", "Unknown option"), the runner never
    started. Exit 255 is a PHP fatal before any test ran.
  silent_pass: >-
    Exit 0 with `No tests executed!` — a filter matched nothing. Success and "nothing
    ran" are the same exit code, so the counts line is the only thing that
    distinguishes them.
```

## Sequence

If invoked in dry-run mode, resolve and return the command without executing it. Dry-run is required.

1. **Resolve the row.** Take `scope` and select the matching row above. A row answered with `absent:` returns that statement and its `nearest:` form; it does not fall through to a wider command.

2. **Substitute the placeholders.** Replace each placeholder token whole. A list placeholder expands to one token per element. Nothing is concatenated into a token and nothing is passed through a shell.

3. **Apply the cost label.** Return the row's `cost` with the command, so a caller running on every build attempt does not receive a command that spawns the binary once per case.

4. **Return the command, the cost, and the failure signal.** The caller runs it. This recipe neither executes it nor judges its output.

5. **Read the result against the failure signal.** Whatever ran the command reads the counts line before the exit code: a non-zero assertion count with failures is a red that proves something; `Assertions: 0`, or `No tests executed!`, is a run that said nothing and must not be reported as either red or green.

## Data flow

```
input: code_path, scope, file / test_id / paths (optional)

reads project state:
       phpunit.xml or phpunit.xml.dist (the declared suites and the bootstrap)
       composer.json (the vendor layout the runner path assumes)

applies opinion:
       argv, never a shell string · an anchored filter, because a bare one matches
       as a substring · a filter matching nothing exits 0 · exit 2 covers both an
       errored test and a misused runner, and the counts line separates them ·
       the end-to-end tier costs a process spawn per case

references origin (never duplicated):
       PHPUnit — the runner every tier executes against, and its exit codes

emits (to the caller; the recipe runs nothing):
       command:  the argv token list for the requested row, placeholders substituted
       cost:     every-attempt | end-of-task
       signal:   how to read the output — assertion, harness, or nothing ran
```

## State-awareness contract

The recipe reads. It writes no file, runs no command, and records nothing against the task. Resolving the same row with the same input returns the same command; what the command then does depends on the project's state, which is the caller's to observe.

## Verifier

After the recipe runs, verify:

1. The returned command is a token list, and every placeholder was substituted as a whole token — nothing was concatenated into a token and nothing reached a shell.
2. The row requested was the row returned. A row answered `absent:` returned that statement, not a wider command that happens to include the wanted tests.
3. A command selecting one case used an anchored filter, and the run's test count was read rather than its exit code alone.
4. The cost label travelled with the command, and no caller running on every build attempt received the CLI end-to-end tier.
5. Any result reported as red carried a non-zero assertion count, and an exit 2 was classified by whether a counts line was present at all.
6. A run reporting `No tests executed!` was reported as having said nothing rather than as a pass.

This recipe ships no executable verifier of its own — it produces a command and the means to read the result, and the phase that runs it owns the gate.

## References

### External origins (referenced, not authored here)

| Source | Used for |
|---|---|
| PHPUnit (`php vendor/bin/phpunit`) | The runner every tier executes against, its filter semantics, and its exit codes |
| Composer | The `vendor/bin` layout the runner path assumes |
| `development/tdd-spec-driven` | What a failing test proves, and why a run that asserted nothing is neither red nor green |

### Plugin-side generic mechanism (ai-dev-assistant)

The phases that run these commands — the failing-test step, the baseline, the build checks, the fixer — are the plugin's, along with whatever records their results. This recipe supplies only what PHP CLI cannot be guessed at: the command per scope, its cost, and how to read what came back.
