---
# Routing block — an orchestrator reads to here and decides.
name: python_cli_implement_standards_and_tests
capability: implement
description: Use when a Python project enters the implementation phase and must hold code to the project's formatting, linting and typing standards alongside test-first discipline — writes the failing test before the code, keeps logic in the importable package and out of the console script, honours the entrypoint contract the design fixed, adds no dependency the design did not decide, and runs the toolchain locally before the change is offered for review.
# Metadata — read only after a match.
label: Python implementation standards and tests
recipe_schema_version: 1.0.0
version: 0.3.0
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
framework: python-cli
assumes:
  - pyproject
  - pytest
authors:
  - name: camoa
license: GPL-2.0-or-later
---

## Goal

Write the change so it conforms to the architecture and passes the review gates before it reaches them. The implementation writes the failing test first, keeps every unit of logic in the importable package, honours the entrypoint contract, adds nothing the design did not decide, and runs the toolchain locally.

The plugin owns the generic implement phase — when it runs, the TDD discipline, and the gate that blocks review. This recipe owns the Python-specific part: which tools run, what they must say, and the conformance rules a linter cannot express.

## Opinion

**The failing test comes first, and it fails for the right reason.** A test that fails with `ImportError` has not tested anything. Write it so it fails on the assertion, then make it pass.

**Tests import the package; they do not shell out.** A test that runs the console script as a subprocess tests the wiring and nothing else, slowly. Test the entry point the design named. One test per console script may exercise the wiring end to end; the rest reach the library.

**The test tier matches the dependency surface — pick the smallest that answers the question.** Five tiers, and naming one deliberately is the point:

- **plain unit** — pure logic with no collaborators and no I/O. Constructs the object or calls the function and asserts on what comes back.
- **unit with collaborators wired** — the behaviour needs its collaborators. Use the real ones where they are cheap and deterministic; reach for a double only at a boundary that must be isolated (network, clock, randomness).
- **integration / fixture** — only the composed pieces answer the question: real file I/O against `tmp_path`, a real config tree, a real database.
- **entry point** — calls the function the console script wraps, passing argv as a list and reading streams through `capsys`. This is the **default tier for CLI behaviour**: it exercises argument parsing, the exit-code mapping and the library call in one fast, coverage-instrumented, debuggable test with no build or subprocess.
- **subprocess** — reserved for what only exists at the process boundary: the exit status the interpreter actually returns, signal handling, and stdin arriving from a real pipe. At most one per console script, per the rule above.

Pushing pure logic into a fixture test that needs a temp tree, or doubling a collaborator a unit really needs so the test proves nothing, are both tier mismatches. `pytest.mark.parametrize` is the table-driven shape and is the default for a tier with more than two cases.

**Every tier above is inside the TDD loop; browser E2E and visual regression are not.** The line is not whether a subprocess is spawned, it is whether the test was written before the code and run red. All five tiers are written from the contract the design fixed, so they constrain it. A Playwright suite or a snapshot baseline, where a project has one, runs against something already built, cannot drive a design decision, and does not count toward the test-first requirement here.

**Adding a test is not automatically progress.** The loop's requirement for a change is one specification per behaviour it creates, at the smallest tier that answers the question, each seen to fail first. Past that, more tests make the change harder to review without specifying anything new. The full set of excess cases belongs to `development/tdd-spec-driven` and is cited, not restated. Two local forms worth naming: `parametrize` rows that differ only in input formatting while reaching the same branch are duplication wearing a table's clothes, and an assertion on `capsys` output text pins prose nobody promised — assert on the return value, the raised exception type, or the exit code the contract assigns, and where a behaviour has no surface but printed prose, that is a finding about the tool rather than a reason to match harder.

**No logic in the console script.** If a change adds a branch to the script that is not argument parsing or wiring, it belongs in the package. This is the rule the design fixed and the one most easily eroded one commit at a time.

**Exceptions carry the failure class the contract names.** The design assigned a distinct exit code per failure class; the implementation raises a distinct exception type per class and the script maps type to code in one place. A bare `except Exception` that swallows and returns `1` erases the contract.

**Nothing is caught to be ignored.** `except: pass` and a bare `except Exception` around a block that then continues are how a tool reports success while doing nothing. Catch the specific exception, or let it propagate.

**No mutable default arguments, and no work at import time.** `def f(x=[])` shares one list across every call. Module-level code that opens files, reads the environment or builds objects runs on import, which makes the module untestable and the CLI slow to start.

**Paths are `pathlib.Path`, and subprocesses take a list.** String path joining breaks on the case nobody tested. `subprocess.run(cmd, shell=True)` with any interpolated value is a shell injection; pass a list and no shell.

**A dependency the design did not decide is not added here.** If the implementation needs one, that is a design question going back, not a line added to `pyproject.toml` mid-change.

**The project's `pyproject.toml` names the tools; where it names none, run the review recipe's floor.** Python ships no `gofmt` — no formatter and linter settled by the interpreter — and the tools that fill the gap have genuinely turned over, so hard-coding a toolchain here would impose one the project may have rejected. Defer to `[tool.*]`. The limit of that deferral is a project that declares nothing, where deferring means running nothing: in that case run the floor the review recipe under this framework names (`ruff format --check`, `ruff check`, `mypy` at the design's strictness, `pytest`) rather than leaving the standards unenforced until review. Whichever runs, it must be the same one review will run — a local pass against a different tool is not a pass.

## Preconditions

- The design phase has run and its component map is available — module boundary, entry points, entrypoint contract, seams, postures.
- The project's toolchain is declared in `pyproject.toml` and installable.
- The change to implement is scoped to one capability or one component of the map.

Three of these are prose because they are design-artifact and scoping conditions with no filesystem probe behind them. The project and runner claims are checkable, and are declared in machine-readable form below.

One honest limitation, recorded rather than hidden. `python3 --version` is both the check and its own subject: with no interpreter on the path it exits 127 and the engine records `unknown / check_command_not_found` — a missing checker says nothing about the precondition, applied to the case where the missing checker *is* the finding. That is weaker than `unmet`, but it is not `met`, so the phase still does not proceed as though an interpreter were present. The manifest check has no such ambiguity: `test` is always available, so it answers either way. The runner check sits between them — it returns a real `unmet` when the interpreter is present and pytest is not, which is the case worth catching, and degrades to the same `unknown` as the interpreter check when there is no interpreter at all.

The `test-runner` check looks in `.venv/bin/`, matching what the PHP CLI recipe does with the PHPUnit binary under `vendor/` — the convention the packaging tool actually creates. It is checked there rather than through the system interpreter because a project's runner lives in the project's environment: `python3 -m pytest` asks whatever interpreter the engine happens to run under, which on a uv, poetry or plain-venv project is not the one the tests run on, and reports `unmet` against a project whose pytest is installed and working.

The limit is worth stating rather than discovering. `.venv/` is a convention, not a standard: a project using tox, a container with pytest on `PATH` and no local virtualenv, or a poetry install configured to keep its environment outside the tree will report `unmet` while being perfectly runnable. That is a fail-closed error in the safe direction — the phase halts and the operator reads the `what:` line — but it is a false negative, and no single argv command (the engine never uses a shell, so these cannot be OR'd) covers both layouts.

preconditions:
  - id: python-project
    what: a pyproject.toml at the project root, where the toolchain and postures are declared
    check: test -f pyproject.toml
  - id: python-interpreter
    what: a Python interpreter on the path, so the toolchain and the tests can run at all
    check: python3 --version
  - id: test-runner
    what: a pytest runner in the project's own environment whose failure the failing-test step can observe
    check: test -x .venv/bin/pytest

## Input contract

```yaml
code_path: string             # absolute path to the project root (the dir with pyproject.toml)
architecture: string          # path to the component map the change must conform to
scope: string                 # the capability or component being implemented
test_tier: string             # optional; plain-unit | unit-with-collaborators | integration |
                              # entry-point | subprocess — derived from the dependency surface if absent
target_pythons: [string]      # optional; the versions the change must work on
```

## Sequence

If invoked in dry-run mode, perform all reads and report the plan and the commands it would run, changing nothing. Dry-run is required.

1. **Read the component map for the scope.** Find the entry point this change delivers, the protocol it implements or consumes, and the entrypoint contract it must honour. A change with no corresponding entry in the map is out of scope; stop and say so.

2. **Select the test tier.** From the behaviour and the component's dependency surface, choose the smallest tier that answers the question: **plain unit** for pure logic; **unit with collaborators wired** where the behaviour needs them; **integration/fixture** where only the composed pieces answer it; the **entry-point** tier for anything the console script exposes; and the **subprocess** tier only for the real exit status, signals, or a real stdin pipe. Use `test_tier` if supplied; otherwise derive it.

3. **Write the failing test.** At the tier selected above, importing the package rather than shelling out. Run it and confirm it fails on the assertion rather than on an import. Record the failure message. Rewriting *this* test is the author's own move, made before the production code exists; once a test is committed, who may change or delete it is the mutability matrix's answer in `development/tdd-spec-driven`, not this phase's.

4. **Write the minimum code to pass it.** In the package module the map names, not in the console script. Annotate the public signature — the typing posture the design recorded applies from the first line, not as a later pass.

5. **Wire the console script, if this capability is reached from one.** Argument parsing and a call to the entry point. Map each exception type the change can raise to the exit code the contract assigns it, in the one place the script does that mapping.

6. **Run the toolchain and make it silent.** Formatter, linter, type checker and tests, in that order, over the changed scope — the tools `pyproject.toml` declares, or the review recipe's floor (`ruff format --check`, `ruff check`, `mypy`, `pytest`) where it declares none. Each must report nothing. A warning left for later is a review-phase block moved into someone else's day.

7. **Check the conformance rules a linter cannot see.** No logic added to the console script; no dependency added the design did not decide; no exception swallowed; no work moved to import time; no `shell=True` with an interpolated value; no mutable default argument. Each is a read of the diff, not a tool run.

8. **Report the change against the map.** Which entry point it delivers, which tests cover it, what the toolchain said, and anything the change revealed that the design did not anticipate. Hand it to the caller; the plugin's implement phase records it.

## Data flow

```
input:  code_path, architecture, scope, test_tier (optional), target_pythons (optional)
step 1: the map entry for this scope — entry point, protocol, contract obligations
step 2: the chosen tier, derived from the dependency surface unless supplied
step 3: a failing test at that tier, failing on its assertion
step 4: package code that passes it, annotated
step 5: script wiring, with exception type mapped to the contract's exit code
step 6: formatter, linter, type checker, tests — each silent over the changed scope
step 7: conformance reads over the diff, one per rule
step 8: report — entry point delivered, tests, tool output, surprises against the design
output: the change, and the report. The plugin's implement phase records it.
```

## State-awareness contract

The recipe writes package code, tests and script wiring inside `code_path`. It does not edit the dependency list, does not change the toolchain configuration, and does not alter the architecture artifact. Where the change needs any of those, it stops and reports the need rather than taking it.

## Verifier

After the recipe runs, verify:

1. Every implemented behaviour has a test at a deliberately chosen tier (plain unit / unit-with-collaborators / integration / entry-point / subprocess), it was written before the code, and it fails on its assertion when the code is removed — no test passed on its first run unexamined.
2. Tests import the package rather than running the console script, except for at most one end-to-end wiring test per script.
3. No logic was added to a console script — the diff's script changes are argument parsing and wiring only.
4. Every failure class the change introduces raises a distinct exception type, and the script maps it to the exit code the contract assigns.
5. The formatter, linter and type checker each report nothing over the changed scope, and the tests pass.
6. No dependency was added that the design did not decide; `pyproject.toml`'s dependency list is unchanged unless the design changed it.
7. No swallowed exception, no import-time work, no `shell=True` with an interpolated value, no mutable default argument.
8. Public signatures are annotated to the typing posture the design recorded.
9. Each test names the behaviour it specifies, and no test in the change was written after the code it covers — a test that cannot name a behaviour is measuring or ratifying, and does not count toward item 1.
10. No test asserts on the wording of captured stdout or stderr; assertions land on the return value, the raised exception type, or the exit code the contract assigns.
11. Every `parametrize` row reaches a branch or boundary no other row reaches; rows differing only in input formatting are duplication, not coverage.
12. Every pre-existing test the change modified or deleted was changed by a role the mutability matrix permits — the only rows that may delete are a feature removal taking its own tests in the same commit; RED authoring is the only row that writes an assertion, and GREEN, REFACTOR and a bug fix change none. A reviewer that wanted a test changed filed a finding instead. See `development/tdd-spec-driven`.

This recipe ships no executable verifier of its own — the checks above are the agent-driven protocol; the plugin's implement phase owns the gate that blocks review.
## Oracle files

A measurement oracle is a file the gates read to decide pass or fail — a test, a tool config, a coverage threshold. An autonomous builder must never weaken one to make a red gate go green: only adding tests or fixing code is allowed, never suppressing a finding or narrowing what gets measured. The plugin's deterministic oracle-tamper guard enforces this at the review/critique rung, but the guard itself is framework-agnostic — it carries no Python knowledge and monitors only the file list it is handed. This section is that list for a Python project: the caller reconstructs it from here on every run (so there is no persistent project file a builder could empty to switch monitoring off) and hands it to the guard.

Each rule names the change kinds it watches (A added, M modified, D deleted), the oracle class the change touches, and a severity. A **halt** is terminal tamper unless the work-order's `oracle_update` field explicitly exempts that class; a **flag** is recorded and the work ships flagged, never blocked.

The class names match the work-order `oracle_update` exemption vocabulary, so a human-authored exemption lines up with what the guard sees.

| Oracle file | Watches | Class | Severity | Why |
|---|---|---|---|---|
| Test files (pytest's default discovery patterns, `test_*.py` and `*_test.py`, anywhere in the tree) | delete | test-delete | halt | Deleting a test removes the behaviour it guards — the builder must add tests, never drop them, to pass. |
| `conftest.py`, anywhere in the tree | modify / delete | test-delete | flag | A conftest can set `collect_ignore` or `collect_ignore_glob` and drop test files from collection entirely, so the suite goes green by running less. A halt would fire on the ordinary fixture work that also lives here, so it is a flag — but a conftest diff is read for a change to collection scope specifically, not skimmed as fixture noise. |
| `pyproject.toml` | modify | dependency-manifest | flag | One file carries the dependency list, the target versions, the linter and type-checker configuration and, in most projects, the coverage threshold — so a change here can lower any gate without touching a line of Python; recorded for review. |
| Standalone tool configs (`ruff.toml`, `.ruff.toml`, `mypy.ini`, `.mypy.ini`, `pyrightconfig.json`) | modify | lint-config | flag | Where the project keeps tool configuration outside the manifest, this is the same surface as the row above: which rules run, which paths are excluded, whether strict mode is on. |
| `.coveragerc` | modify | coverage-threshold | flag | Where coverage is configured outside the manifest, its `fail_under` and its omit list are the coverage gate; recorded for review. |

The caller emits this list as the oracle-tamper guard's JSON input. The two columns the guard needs beyond the table are the path globs and the watched-change set:

```json
[
  { "type": "test_delete",        "globs": ["**/test_*.py", "**/*_test.py"],                               "changes": ["D"],     "oracle_class": "test-delete",         "severity": "halt" },
  { "type": "conftest",           "globs": ["**/conftest.py"],                                             "changes": ["M","D"], "oracle_class": "test-delete",         "severity": "flag" },
  { "type": "dependency_manifest","globs": ["pyproject.toml"],                                             "changes": ["M"],     "oracle_class": "dependency-manifest", "severity": "flag" },
  { "type": "lint_config",        "globs": ["ruff.toml", ".ruff.toml", "mypy.ini", ".mypy.ini", "pyrightconfig.json"], "changes": ["M"], "oracle_class": "lint-config",  "severity": "flag" },
  { "type": "coverage_threshold", "globs": [".coveragerc"],                                                "changes": ["M"],     "oracle_class": "coverage-threshold",  "severity": "flag" }
]
```

Two things about this list are worth stating, because they are what makes it worth declaring rather than copying from another framework.

**The highest-value suppressions in Python are not files, so no glob reaches them.** `# noqa` and `# type: ignore` sit inline in the source, and an unexplained one deletes a check exactly as a baseline entry would — but the guard matches paths, and a comment has no path. This is the same shape as Go's `//nolint`, and it has the same answer: the rule against unexplained suppressions is enforced by the reviewer reading the diff (see the review recipe under this framework), never by the tamper guard. Do not read this table as covering them.

**Python has no static-analysis baseline in the toolchain, so that halt rule has no counterpart here.** There is no equivalent of a phpstan baseline to append a new finding to; the nearest thing is a per-file ignore list inside a tool config, which is why those configs are watched. A project that layers a snapshot-testing plugin on top of pytest gains a real golden-file oracle and should add its snapshot directory to this list with a halt — that path is plugin-specific and is not asserted here. A project that declares no oracle files at all is an honest "no oracle configured" state: the guard reports it ran with nothing to watch, rather than reporting a pass it never checked.

## References

### External origins (referenced, not authored here)

| Source | Used for |
|---|---|
| The project's `pyproject.toml` | The authority on which tools run and in what configuration — the declaration this phase defers to before the floor applies, and the manifest whose dependency list the change may not edit |
| pytest (`python_files`, `conftest.py`, `collect_ignore` / `collect_ignore_glob`) | The test runner every tier executes against, the default discovery patterns behind the oracle globs, and the collection-scope mechanism that makes a conftest an oracle rather than ordinary code |
| Ruff (`ruff format --check`, `ruff check`) and mypy (`[tool.mypy]`, `strict`) | The formatting, linting and typing floor for a project that declares none — the same tools review runs, so a local pass and a review pass mean the same thing |
| PEP 8 and PEP 257 | The style and docstring baseline the formatter and linter enforce |
| PEP 561 | What the typing posture commits the package to — the `py.typed` marker and the stub surface annotated from the first line rather than in a later pass |
| The component map from the design phase | The recorded decision this recipe conforms to rather than reinterprets — the entry point, the protocol, the entrypoint contract |

### Plugin-side generic mechanism (ai-dev-assistant)

The stack-neutral implement phase this recipe binds Python into — when implementation runs, the test-first gate that blocks completion, the oracle-tamper guard that reads the list above, how the `## Preconditions` block is checked before the phase starts, and how the results are recorded against the task — is documented in the plugin itself, not duplicated here. The recipe supplies only the Python-specific standards-and-tests method: the library-not-the-script boundary, tests that import rather than shell out, one exception type per failure class mapped to the contract's exit codes, and the import-time, mutable-default and shell-injection traps.

Unlike the PHP CLI recipe under this root, this one does not defer linter execution to the `code-quality-tools` plugin: that plugin detects Drupal and Next.js projects and lints PHP and JavaScript file extensions, and has no Python arm.
