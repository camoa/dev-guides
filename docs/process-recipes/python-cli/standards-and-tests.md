---
# Routing block — an orchestrator reads to here and decides.
name: python_cli_implement_standards_and_tests
capability: implement
description: Use when a Python project enters the implementation phase holding a test that already fails, and must turn it green under the project's formatting, linting and typing standards — keeps logic in the importable package and out of the console script, honours the entrypoint contract the design fixed, adds no dependency the design did not decide, and runs the toolchain locally before the change is offered for review. Which level the test sits at and how it is written belong to the test-authoring recipe.
# Metadata — read only after a match.
label: Python implementation standards and tests
recipe_schema_version: 1.0.0
version: 0.5.0
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

**The failing test comes first, and it fails for the right reason.** A test that fails with `ImportError` has not tested anything. Write it so it fails on the assertion, then make it pass. The right reason is that the behaviour is absent — deleting or breaking working code to watch an existing test fail proves the test is sensitive, never that it came first (see `development/tdd-spec-driven/what-a-failing-test-proves`).

**The level, the file and the test's name are not decided here.** Which level a behaviour belongs at, where the test file goes, what the function is called, how the criterion it specifies is traced to it, and what a pytest test may not do are `python-cli/test-authoring.md`'s — including the rule that tests import the package rather than shelling out to the console script. That reader writes the test and stops at red; this one takes the red test and makes it green. The rules are stated once, there, because a reader that may not write production code cannot be handed this file.

**Every tier above is inside the TDD loop; browser E2E and visual regression are not.** The line is not whether a subprocess is spawned, it is whether the test was written before the code and run red. All five tiers are written from the contract the design fixed, so they constrain it. A Playwright suite or a snapshot baseline, where a project has one, runs against something already built, cannot drive a design decision, and does not count toward the test-first requirement here.

**Adding a test is not automatically progress.** The loop's requirement for a change is one specification per behaviour it creates, at the smallest tier that answers the question, each seen to fail first *because the behaviour it names did not exist yet*. Past that, more tests make the change harder to review without specifying anything new. The full set of excess cases belongs to `development/tdd-spec-driven` and is cited, not restated. Two local forms worth naming: `parametrize` rows that differ only in input formatting while reaching the same branch are duplication wearing a table's clothes, and an assertion on `capsys` output text pins prose nobody promised — assert on the return value, the raised exception type, or the exit code the contract assigns, and where a behaviour has no surface but printed prose, that is a finding about the tool rather than a reason to match harder.

**No logic in the console script.** If a change adds a branch to the script that is not argument parsing or wiring, it belongs in the package. This is the rule the design fixed and the one most easily eroded one commit at a time.

**Exceptions carry the failure class the contract names.** The design assigned a distinct exit code per failure class; the implementation raises a distinct exception type per class and the script maps type to code in one place. A bare `except Exception` that swallows and returns `1` erases the contract.

**Nothing is caught to be ignored.** `except: pass` and a bare `except Exception` around a block that then continues are how a tool reports success while doing nothing. Catch the specific exception, or let it propagate.

**No mutable default arguments, and no work at import time.** `def f(x=[])` shares one list across every call. Module-level code that opens files, reads the environment or builds objects runs on import, which makes the module untestable and the CLI slow to start.

**Paths are `pathlib.Path`, and subprocesses take a list.** String path joining breaks on the case nobody tested. `subprocess.run(cmd, shell=True)` with any interpolated value is a shell injection; pass a list and no shell.

**A dependency the design did not decide is not added here.** If the implementation needs one, that is a design question going back, not a line added to `pyproject.toml` mid-change.

**The project's `pyproject.toml` names the tools; where it names none, run the review recipe's floor.** Python ships no `gofmt` — no formatter and linter settled by the interpreter — and the tools that fill the gap have genuinely turned over, so hard-coding a toolchain here would impose one the project may have rejected. Defer to `[tool.*]`. The limit of that deferral is a project that declares nothing, where deferring means running nothing: in that case run the floor the review recipe under this framework names (`ruff format --check`, `ruff check`, `mypy` at the design's strictness, `pytest`) rather than leaving the standards unenforced until review. Whichever runs, it must be the same one review will run — a local pass against a different tool is not a pass.

## Preconditions

- The design phase has run and its component map is available — module boundary, entry points, entrypoint contract, seams, postures.
- The project's toolchain is declared in `pyproject.toml` and installable. The manifest, interpreter and runner claims carry machine-readable entries in the `test-execution` recipe for this framework, which owns the commands they are conditions of.
- The change to implement is scoped to one capability or one component of the map.

All three stay prose here. The checkable half — the manifest, the interpreter and the runner in the project's own environment — moved to the `test-execution` recipe alongside the commands that need them, carrying with it the two limitations worth recording rather than discovering: `python3 --version` is both the check and its own subject, and `.venv/` is a convention rather than a standard, so a tox or container layout reports `unmet` while being perfectly runnable.

```yaml
preconditions: []
```

## Input contract

```yaml
code_path: string             # absolute path to the project root (the dir with pyproject.toml)
architecture: string          # path to the component map the change must conform to
scope: string                 # the capability or component being implemented
test_tier: string             # the level the test-authoring recipe chose, carried through
target_pythons: [string]      # optional; the versions the change must work on
```

## Sequence

If invoked in dry-run mode, perform all reads and report the plan and the commands it would run, changing nothing. Dry-run is required.

1. **Read the component map for the scope.** Find the entry point this change delivers, the protocol it implements or consumes, and the entrypoint contract it must honour. A change with no corresponding entry in the map is out of scope; stop and say so.

2. **Take the failing test.** The level, the file, the function name and the criterion it carries are `python-cli/test-authoring.md`'s, and it hands them over red. A capability arriving with no failing test does not enter this phase; send it back.

3. **Confirm the red is the right red.** The failure is the assertion, not an `ImportError`, and it is there because the behaviour is absent rather than because working code was removed (see `development/tdd-spec-driven/what-a-failing-test-proves`). Record the failure message. A test that passed on arrival is not a starting point; return it. Once a test is committed, who may change or delete it is the mutability matrix's answer in `development/tdd-spec-driven`, not this phase's — and this phase changes none.

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

1. Every implemented behaviour arrived with a test that had been seen to fail on its assertion *because the behaviour did not exist yet* — a failure produced by removing working code proves sensitivity, not authoring order, and no test passed on arrival unexamined. The level that test sits at is `python-cli/test-authoring.md`'s choice, verified there.
3. No logic was added to a console script — the diff's script changes are argument parsing and wiring only.
4. Every failure class the change introduces raises a distinct exception type, and the script maps it to the exit code the contract assigns.
5. The formatter, linter and type checker each report nothing over the changed scope, and the tests pass.
6. No dependency was added that the design did not decide; `pyproject.toml`'s dependency list is unchanged unless the design changed it.
7. No swallowed exception, no import-time work, no `shell=True` with an interpolated value, no mutable default argument.
8. Public signatures are annotated to the typing posture the design recorded.
9. No test in the change was written after the code it covers — a test that cannot name a behaviour is measuring or ratifying, and does not count toward item 1. This phase wrote none of them.
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

### Sibling process recipes

| Recipe | What it holds |
|---|---|
| `python-cli/test-authoring.md` | Which level a behaviour belongs at, where the file goes and what the test function is called, how a criterion is traced to a test, and what a pytest test may not do — the half of the cycle that ends at red |
| `python-cli/test-execution.md` | The command at each scope, its cost, the conditions for running one, the node-identifier form, and how to read what came back |

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

The stack-neutral implement phase this recipe binds Python into — when implementation runs, the test-first gate that blocks completion, the oracle-tamper guard that reads the list above, how the `## Preconditions` block is checked before the phase starts, and how the results are recorded against the task — is documented in the plugin itself, not duplicated here. The recipe supplies only the Python-specific method it owns: the library-not-the-script boundary, one exception type per failure class mapped to the contract's exit codes, and the import-time, mutable-default and shell-injection traps.

Unlike the PHP CLI recipe under this root, this one does not defer linter execution to the `code-quality-tools` plugin: that plugin detects Drupal and Next.js projects and lints PHP and JavaScript file extensions, and has no Python arm.
