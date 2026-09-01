---
# Routing block — an orchestrator reads to here and decides.
name: php_cli_implement_standards_and_tests
capability: implement
description: Use when a PHP CLI project (a Composer library or application whose interface is one or more CLI binaries) enters the implementation phase and must hold code to PHP/PSR standards and test-first discipline — applies PSR-12 with declare(strict_types=1) and readonly value objects, selects the smallest PHPUnit tier that answers the question, tests every CLI flag and exit code with a fixture-driven end-to-end tier, and syntax-checks every shipped binary including extensionless ones. Defers linter execution to the code-quality-tools plugin.
# Metadata — read only after a match.
label: PHP CLI standards and tests
recipe_schema_version: 1.0.0
version: 0.4.0
# Machine-readable dependency declaration (recipe-loader resolves these
# without parsing prose). The test-mutability rule is stack-neutral: it is
# cited here, never restated per framework.
requires_guides:
  - development/tdd-spec-driven
# Process-recipe routing keys, enforced by validate_recipes.py for any recipe
# under docs/process-recipes/. `capability` above doubles as the phase (the
# lifecycle moment the orchestrator resolves on); there is no separate
# applies_to_phase. `framework` is the second routing dimension.
recipe_class: process
framework: php-cli
assumes:
  - composer
  - phpunit
authors:
  - name: camoa
license: GPL-2.0-or-later
---

## Goal

Hold PHP CLI implementation-phase code to the standard it must meet before it can be reviewed: PHP/PSR coding standards applied as the code is written, every unit of logic covered by a PHPUnit test written test-first at the smallest tier that answers the question, every CLI flag and exit code exercised, and a fixture-driven end-to-end tier that runs the built binary against a fixture tree and asserts on its output. The judgement of *which* standard applies and *which* test tier fits is the recipe's; running the linters is the code-quality-tools plugin's.

The plugin owns the generic mechanism — when the implement phase runs, the test-first gate that blocks completion, the oracle-tamper guard that stops a builder weakening a measurement file, and how findings are recorded against the task. This recipe owns the part the stack-neutral mechanism cannot know: how PHP coding standards are applied to a CLI library, how the PHPUnit test tiers are selected and shaped, what "test the CLI end-to-end" means without a browser, and the extensionless-binary trap a naive syntax-check glob walks straight into.

## Opinion

**The test is written first, and it is seen to fail.** No production code is written until a test for the behaviour exists and has been run to confirm it fails (RED) for the right reason — a missing implementation, not a typo in the test. Then the minimum code to pass (GREEN), then refactoring under a green bar (REFACTOR). A test that passes on its first run is suspect: it is probably asserting nothing. "Too simple to test" is not a reason to skip; a CLI flag or an exit code is exactly the kind of one-liner that silently regresses.

**PSR-12, strict types everywhere, readonly value objects across seams.** Every file carries `declare(strict_types=1)` and conforms to PSR-12 layout, PascalCase classes / camelCase methods, docblocks on classes and public methods, and type hints on every parameter and return. Data carried between layers — from the thin binary into the library, from one collaborator to the next — travels as a `readonly` value object, not a loose array, so the shape is explicit and cannot be mutated behind a caller's back. No deprecated APIs reach the diff.

**The test tier matches the dependency surface, not habit — pick the smallest that answers the question.** Pure logic with no collaborators is a plain unit test that constructs the class and asserts on its return. Logic that needs collaborators is a unit test with those collaborators wired (real ones where cheap, doubles where a boundary must be isolated). Behaviour that only makes sense against the whole library — a service composed of several parts, real file I/O against a temp tree — is a fixture or integration tier that exercises the library API. Pushing pure logic into a slow fixture test, or faking a collaborator a unit really needs so the test proves nothing, are both tier mismatches — name the tier deliberately.

**Every CLI flag and exit code needs a test, and a check-style unit needs a negative case.** Each flag the binary accepts and each exit code it can return is a behaviour with a contract, and each gets a test that pins it — a flag that changes output, a bad-input path that returns the documented non-zero code. A **check-style** unit — one whose job is to *report problems* (a linter rule, a scanner, a validator) — additionally needs a **negative case**: an assertion that correct input produces **no** output and no finding. Without the negative case the check cannot be tuned — a rule that flags everything and a rule that flags nothing both pass a suite that only ever feeds them bad input.

**Fixture-driven end-to-end IS the CLI's e2e, and it belongs here.** "No e2e" for a PHP CLI means no *browser* e2e — it does not mean the tool has no end-to-end shape. A CLI tool's real end-to-end test runs the built binary against a fixture tree and asserts on its stdout, its stderr, and its exit code — the whole contract a user actually hits. The plugin's e2e-setup machinery is Playwright-shaped and does not fit a tool with no rendered surface, so this coverage does not live in an e2e-setup phase; it lives here (and in review) as a test tier, driving the binary as a subprocess exactly as a user would invoke it.

**That fixture tier is inside the TDD loop; a browser suite would not be.** The distinction is not whether a subprocess or a browser is involved, it is whether the test was written before the code and run red. The fixture-driven CLI test is written from the flag-and-exit-code contract before the flag exists, so it constrains the design. Visual regression and browser E2E, where a project has them, run against something already built, cannot drive a design decision, and do not count toward the test-first requirement here.

**Adding a test is not automatically progress.** The loop's requirement for a change is one specification per behaviour the change creates, at the smallest tier that answers the question, each seen to fail first. Past that, more tests make the change harder to review without specifying anything new. The full set of excess cases belongs to `development/tdd-spec-driven` and is cited, not restated. The local form worth naming: a CLI tool's most tempting bad assertion is a match on the exact wording of its own stdout. The exit code and the structured output are contracts; the prose around them is not, and a test that pins the prose breaks on a reword while proving nothing. Where a behaviour has no surface but prose, that is a finding about the tool — give it an exit code or a machine-readable mode — not a reason to assert harder.

**Syntax-check and lint every shipped binary, including the extensionless ones.** A Composer CLI's binaries are conventionally extensionless — `bin/<tool>`, not a `.php` file — so a naive `find -name '*.php'` syntax-check glob silently skips the very entrypoints a user runs. Enumerate the binaries to check from the `bin` array in composer.json instead of globbing by extension, and syntax-check (and hand to the linters) every one of them, extensionless included. A binary that never gets linted is the file most likely to ship a fatal parse error.

**Standards are applied by judgement; the linters are run by the tooling.** This recipe decides what PSR-12, strict types, and the house conventions mean for the code in front of it. The *execution* of `phpcs` and `phpstan` over the changed files is the code-quality-tools plugin's job; this recipe references that plugin for the run and does not re-author or replace the linter invocation. Standards live in judgement here; their mechanical enforcement lives in the tooling.

## Preconditions

- A PHP project, Composer-managed, with a configured PHPUnit runner (`php vendor/bin/phpunit` against a committed `phpunit.xml` / `phpunit.xml.dist`) — so the tests and the code-quality-tools linters can run.
- The design phase has produced an architecture decision (see the architecture recipe under this framework): the library boundary, the thin-binary contract, the exit-code semantics, and the component map are known, so this phase tests and builds against a plan rather than improvising structure.
- The code-quality-tools plugin is available for linter execution (`phpcs`, `phpstan` at the project's declared level); this recipe does not bundle or re-author those runners.
- The plugin's generic implement phase is present: the test-first gate, the oracle-tamper guard, and the task record. This recipe supplies the PHP-CLI-specific standards-and-tests method; it does not recreate the gate.

The runner bullet is the one the engine can check, so it is also declared in machine-readable form below. The rest stay prose: they are design-artifact and plugin-availability conditions with no argv-safe filesystem probe.

preconditions:
  - id: test-runner
    what: a PHPUnit runner whose failure the RED step can observe
    check: test -x vendor/bin/phpunit
    owner: code-quality-tools:setup

## Input contract

Source-agnostic, supplied by the caller (the orchestrator at the implement phase, or a human operator).

```yaml
code_path: string             # absolute path to the PHP project root
component: string             # the unit being implemented (a service, a command, a rule…)
behavior: string             # the specific behaviour to test-drive and build
test_tier: string             # optional; unit | unit-with-collaborators | integration |
                              #   cli-e2e — if absent, derived from the dependency surface
architecture_ref: string      # optional; pointer to the design decision this implements
```

## Sequence

If invoked in dry-run mode, perform all reads and emit a test-and-standards plan (the tier choice, the test shape, the flag/exit-code list to cover, the binaries to syntax-check) instead of writing any test or production code. Dry-run is required.

1. **Select the test tier.** From `behavior` and the component's dependency surface, choose the smallest tier that answers the question: a **plain unit** test for pure logic; a **unit with collaborators wired** where the behaviour needs them; an **integration/fixture** tier where only the composed library API makes sense; and, for anything the binary exposes, the **CLI end-to-end** tier that runs the built binary against a fixture tree. Use `test_tier` if supplied; otherwise derive it. Tests live under `tests/`.

2. **Write the failing test (RED).** Author the test before any production code, shaped Arrange-Act-Assert. For every CLI flag and exit code the component touches, include an exit-code-contract test that invokes the binary and asserts on the returned status and the stdout/stderr split; for behaviour a user reaches through the binary, include fixture-based CLI end-to-end coverage that drives the built binary as a subprocess against a fixture tree. If the component is a check-style unit, include the **negative case** — correct input yields no output/no finding. Run the tests and confirm each fails for the right reason. A test that passes immediately is rejected and rewritten. Rewriting *this* test is the author's own move, made before the production code exists; once a test is committed, who may change or delete it is the mutability matrix's answer in `development/tdd-spec-driven`, not this phase's.

3. **Write the minimum code to pass (GREEN).** Implement only what the tests demand — no extra features, no premature optimisation. As you write, hold the standards inline: `declare(strict_types=1)` at the top of every file, PSR-12 layout, docblocks and type hints, PascalCase classes / camelCase methods, and `readonly` value objects for data crossing the binary/library seam or passed between collaborators rather than loose arrays. Keep the binary thin — arg parsing and wiring only, logic in the library (the boundary the architecture recipe fixed). Run the tests to green.

4. **Apply and confirm the standards inline.** Before the unit is considered done, confirm no deprecated APIs entered the diff, every new file declares strict types, and the layer boundary held (no business logic leaked into `bin/`). Any gap is fixed now, with a test that proves the fix where the behaviour is testable.

5. **Syntax-check every shipped binary, extensionless included.** Enumerate the binaries from the `bin` array in composer.json — not from a `*.php` glob, which skips the extensionless ones — and syntax-check every entry (`php -l` per binary). An extensionless `bin/<tool>` is checked exactly like a `.php` file. A binary that fails the syntax check is fixed before the phase hands back.

6. **Refactor under green (REFACTOR).** With tests green, improve structure without changing behaviour — extract duplication into the library, lean on interfaces at the extension seams the design named, tighten the value objects. Re-run the tests; they stay green or the refactor is reverted.

7. **Defer the linters to the tooling, then hand back.** Invoke the code-quality-tools plugin to run `phpcs` and `phpstan` over the changed files, binaries included — this recipe judges what the standards mean but does not re-author or replace that run. Return the test results, the tier choices, the flag/exit-code coverage, the fixture-based CLI-e2e result, the binary syntax-check outcome, and the linter outcome to the caller; the plugin's implement phase records them against the task and owns the completion gate. The recipe writes test and production code for the component, but writes no task record of its own.

## Data flow

```
input: code_path, component, behavior, test_tier (optional), architecture_ref (optional)

reads project state:
       architecture decision (the library boundary + thin-binary + exit-code contract)
       composer.json (the bin array — the authoritative list of shipped binaries)
       existing library + entrypoints (src/, bin/) and existing tests (tests/)

applies opinion:
       test-first (RED→GREEN→REFACTOR) · PSR-12 + declare(strict_types=1) + readonly
       value objects · smallest tier that answers the question · every flag + exit code
       tested · check-style unit needs a negative case · fixture-driven CLI e2e lives
       here · syntax-check every binary incl. extensionless · standards by judgement,
       linters by tooling

references origin (never duplicated):
       PHPUnit                     — the test runner every tier executes against
       code-quality-tools (plugin) — phpcs + phpstan execution over the changed files
       the architecture recipe     — the library boundary, thin-binary, exit-code contract

emits (to the caller; the recipe writes no task record):
       tests:        the test(s) per component at the chosen tier, seen to fail then pass,
                     incl. flag/exit-code contract tests + fixture-based CLI e2e
       code:         the minimum production code that turns them green, standards held inline
       binaries:     the per-binary syntax-check outcome (extensionless included)
       linting:      the code-quality-tools run outcome over the changed files
```

## State-awareness contract

The recipe reads existing state before writing. The architecture decision, the current library layout (`src/`, `bin/`), the `bin` array in composer.json, and any existing tests under `tests/` are read so new code extends the design, the binary list is enumerated from source of truth rather than guessed, and new tests extend the suite rather than colliding with or duplicating it. The method writes test and production code for the component under implementation, but installs nothing and writes no task record — the results are returned to the caller, which owns recording them and gating completion.

Idempotent at the discipline level: re-running on a component whose tests already pass, whose standards already hold, and whose binaries already syntax-check produces no new change — the tests stay green, the linters stay clean, nothing is rewritten. A change on re-run means a regression was found or the behaviour moved, which is the method reflecting current reality, not non-determinism.

## Verifier

After the recipe runs, verify:

1. Every implemented behaviour has a PHPUnit test at a deliberately chosen tier (plain unit / unit-with-collaborators / integration / CLI end-to-end), and each test was seen to fail before the code existed — no test passed on its first run unexamined.
2. Every check-style unit carries a negative case — an assertion that correct input produces no output and no finding — so the check can be tuned, not just fired.
3. Every CLI flag and every exit code the component touches is covered, and fixture-based CLI end-to-end coverage exists that drives the built binary against a fixture tree and asserts on stdout / stderr / exit code.
4. Each test names the behaviour it specifies, and no test in the change was written after the code it covers — a test that cannot name a behaviour is measuring or ratifying, and does not count toward item 1.
5. No test asserts on the wording of a printed message; assertions land on the exit code, structured output, returned values, or thrown exception types.
6. Every shipped binary — enumerated from the `bin` array in composer.json, extensionless entries included — was syntax-checked and passes; none was skipped by an extension-only glob.
7. New code carries `declare(strict_types=1)` in every file, PSR-12 layout, docblocks and type hints, `readonly` value objects across the seams, no deprecated APIs, and no business logic in `bin/`.
8. The code-quality-tools `phpcs` and `phpstan` run over the changed files (binaries included) is clean, or its findings are recorded for the gate; this recipe did not re-author that run.
9. The tests are green and the refactor (if any) left them green; the results were returned to the caller for the plugin's implement phase to record — the recipe wrote no task record of its own.
10. Every pre-existing test the change modified or deleted was changed by a role the mutability matrix permits — the only rows that may delete are a feature removal taking its own tests in the same commit; RED authoring is the only row that writes an assertion, and GREEN, REFACTOR and a bug fix change none. A reviewer that wanted a test changed filed a finding instead. See `development/tdd-spec-driven`.

This recipe ships no executable verifier of its own — the checks above are the agent-driven protocol; the linter execution is the code-quality-tools plugin's, and the plugin's implement phase owns the test-first completion gate.
## Oracle files

A measurement oracle is a file the gates read to decide pass or fail — a static-analysis baseline, a test, a coverage config. An autonomous builder must never weaken one to make a red gate go green: only adding tests or fixing code is allowed, never suppressing a finding. The plugin's deterministic oracle-tamper guard enforces this at the review/critique rung, but the guard itself is framework-agnostic — it carries no PHP knowledge and monitors only the file list it is handed. This section is that list for a PHP CLI project: the caller reconstructs it from here on every run (so there is no persistent project file a builder could empty to switch monitoring off) and hands it to the guard.

Each rule names the change kinds it watches (A added, M modified, D deleted), the oracle class the change touches, and a severity. A **halt** is terminal tamper unless the work-order's `oracle_update` field explicitly exempts that class; a **flag** is recorded and the work ships flagged, never blocked.

The class names match the work-order `oracle_update` exemption vocabulary, so a human-authored exemption lines up with what the guard sees.

| Oracle file | Watches | Class | Severity | Why |
|---|---|---|---|---|
| `phpstan-baseline.neon` | add / modify | phpstan-baseline | halt | The phpstan baseline suppresses known findings — adding to it hides a *new* static-analysis error instead of fixing it. |
| `phpstan.neon` / `phpstan.neon.dist` | modify | phpstan-baseline | flag | The phpstan config sets the rule level and paths — a change can quietly lower the bar; recorded for review. |
| `phpunit.xml` / `phpunit.xml.dist` | modify | coverage-threshold | flag | The PHPUnit config carries coverage thresholds and the suite definition — a change can relax the coverage gate; recorded for review. |
| PHPUnit test files (`*Test.php` under a `tests/` or `test/` tree, at any depth) | delete | test-delete | halt | Deleting a test removes the behaviour it guards — the builder must add tests, never drop them, to pass. |

The caller emits this list as the oracle-tamper guard's JSON input. The two columns the guard needs beyond the table are the path globs and the watched-change set:

```json
[
  { "type": "phpstan_baseline",  "globs": ["phpstan-baseline.neon"],            "changes": ["A","M"], "oracle_class": "phpstan-baseline",   "severity": "halt" },
  { "type": "phpstan_config",    "globs": ["phpstan.neon", "phpstan.neon.dist"],"changes": ["M"],     "oracle_class": "phpstan-baseline",   "severity": "flag" },
  { "type": "coverage_threshold","globs": ["phpunit.xml", "phpunit.xml.dist"],  "changes": ["M"],     "oracle_class": "coverage-threshold", "severity": "flag" },
  { "type": "test_delete",       "globs": ["**/tests/**/*Test.php", "**/test/**/*Test.php"], "changes": ["D"], "oracle_class": "test-delete",   "severity": "halt" }
]
```

Two things about the test glob are deliberate, and both were established by running the guard's own
glob translation rather than by reading it.

**The `**/` prefix is required.** The guard anchors a glob at both ends and expands `**/` to an
*optional* path prefix, so `tests/**/*Test.php` matches a test tree at the repository root and
nothing else — any package whose tests sit below the root, such as a nested or multi-package layout,
fails it. `**/tests/**/*Test.php` covers both the nested layout and the root one, which is why it is
the only `tests/` glob needed here.

**`test/` singular is a real convention, not a typo.** Across 139 Composer packages declaring a
dev-autoload test path, 60 use `tests/` and 13 use `test/`. A PHP CLI project is as likely to be one
of the latter, and a delete guard that watches only `tests/` silently watches nothing on it — the
same failure mode as a missing prefix, which is why both are declared.

These are the standards-and-tests oracle files — the same set a standalone PHP CLI project carries as a Drupal one, since the measurement surface (the phpstan baseline, the phpstan config, the PHPUnit config, and the test files) is identical. A `php-cli` project binds no visual-regression or e2e-setup phase, so it declares no further oracle files from those recipes; the caller still unions declarations across every recipe that applies before handing the combined list to the guard. A project that declares no oracle files at all is an honest "no oracle configured" state: the guard reports it ran with nothing to watch, rather than reporting a pass it never checked.

## References

### Plugin-side tooling (referenced, not authored here)

| Source | Used for |
|---|---|
| code-quality-tools (plugin) | Execution of `phpcs` and `phpstan` over the changed files, binaries included — the linter run this recipe defers to rather than re-authoring |

### External origins (referenced, not authored here)

| Source | Used for |
|---|---|
| PHPUnit (`php vendor/bin/phpunit`) | The test runner every tier — plain unit, unit-with-collaborators, integration, and the fixture-driven CLI end-to-end — executes against |
| Composer (composer.json `bin` array) | The authoritative list of shipped binaries the syntax-check enumerates, so extensionless entrypoints are not skipped by an extension-only glob |

### Plugin-side generic mechanism (ai-dev-assistant)

The stack-neutral implement phase this recipe binds PHP CLI into — when implementation runs, the test-first gate that blocks completion, the oracle-tamper guard that reads the list above, and how the results are recorded against the task — is documented in the plugin itself, not duplicated here. The recipe supplies only the PHP-CLI-specific standards-and-tests method (PSR-12 with strict types and readonly value objects, PHPUnit tier selection, the CLI flag/exit-code and fixture-driven end-to-end coverage, and the extensionless-binary syntax check) on top of that mechanism.
