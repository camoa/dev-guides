---
# Routing block — an orchestrator reads to here and decides.
name: python_cli_test_authoring
capability: test-authoring
description: Use when a context is about to write the tests for one unit of work on a Python library or console-script project, before any production code exists, and needs to know which level the behaviour belongs at, where the file goes, what the test function is called, how the criterion it specifies is traced to it, and what a pytest test may not do.
# Metadata — read only after a match.
label: Test authoring (Python CLI)
recipe_schema_version: 1.0.0
version: 0.2.0
# Machine-readable dependency declaration (recipe-loader resolves these without parsing prose).
requires_guides:
  - development/tdd-spec-driven
# Process-recipe routing keys, enforced by validate_recipes.py for any recipe
# under docs/process-recipes/. `capability` above doubles as the phase; there is
# no separate applies_to_phase. `framework` is the second routing dimension.
recipe_class: process
framework: python-cli
assumes:
  - pyproject
authors:
  - name: camoa
license: GPL-2.0-or-later
---

## Goal

Answer four questions for whoever is about to write a Python test: which level the behaviour belongs
at, where the file goes and what the test function is called, how the criterion it specifies is
recoverable from it, and what a pytest test may not do.

**This recipe stops at red.** Its reader writes the test, watches it fail, and stops. It does not
write the code that turns the test green, and nothing here tells it to. The green and refactor half
of the cycle belongs to `python-cli/standards-and-tests.md`, read by a different context. Running the
test belongs to `python-cli/test-execution.md`, which several callers share.

The reader also cannot open the production source of anything already built. Every rule below is
therefore decidable from the behaviour the test must observe and from the names the package declares.
A rule that needs the module in front of you is a rule this reader cannot follow.

## Opinion

**The level follows the dependency surface, decided from the behaviour and not from the code.**

| Level | Where the file goes | Choose it when the behaviour needs | Cost |
|---|---|---|---|
| plain unit | `tests/<path mirroring the package>/test_<module>.py` | nothing but the function or object and its arguments: call it and assert on what comes back | microseconds |
| unit with collaborators wired | the same | its collaborators — real ones where they are cheap and deterministic, a double only at a boundary that must be isolated (network, clock, randomness) | milliseconds |
| integration / fixture | the same, with the tree it needs built under `tmp_path` | only the composed pieces answer the question: real file I/O, a real config tree, a real database | tenths of a second |
| entry point | `tests/test_cli.py`, or the file mirroring the module the console script wraps | anything the console script exposes: argument parsing, the exit-code mapping and the library call, driven by passing argv as a list and reading the streams through `capsys` | milliseconds |
| subprocess | the same file as the entry-point test for that script | only what exists at the process boundary: the exit status the interpreter really returns, signal handling, stdin arriving from a real pipe | a process per test |

pytest does **not** map a level to a directory: it discovers by filename pattern, and the level is a
judgement recorded in the test's own shape. Nothing enforces it, which is why naming it deliberately
is the point.

**Start at the entry point for anything the console script exposes.** That is the default, because
argument parsing, the exit-code mapping and the library call are one contract and no cheaper level
tests them together. The subprocess level is the exception reserved for the three process-boundary
things above — at most one per console script, because a test that runs the script as a subprocess
tests the wiring and nothing else, slowly. For library behaviour the plain unit is genuinely right
first. What stops it being reached for when it is wrong is one check: if answering the question means
doubling a collaborator the behaviour actually needs, the level is too low and the test proves the
double. `pytest.mark.parametrize` is the table-driven shape and is the default for a level with more
than two cases.

**All five levels are written before the code. A browser suite and a snapshot baseline are not.**
Where a project has either, they run against something already built, cannot drive a design decision,
never substitute for a level chosen here, and are reported separately rather than counted toward the
test-first requirement.

**Where the file goes, and what it is called.** This is stated here because nothing else in this
framework's set states it, and a rule that lives only inside a delete-guard glob is not an
instruction anyone can follow.

- Test files live under `tests/` at the project root, mirroring the package layout, never inside the
  package. Under the `src/` layout the design prefers, that placement is also what forces a test to
  import the **installed** package rather than a sibling directory — which is what "tests import the
  package, they do not shell out" means in practice.
- A file is named `test_<module>.py`. pytest's default discovery accepts `test_*.py` and `*_test.py`
  both; pick the first and be consistent, because the delete guard watches both and a project mixing
  them makes its own test tree harder to read.
- A test function is named `test_<behaviour>_<criterion>`. pytest collects a function only when its
  name starts with `test`, so a helper named `check_something` in a test file is silently not
  collected — verified on pytest 9.1.1, where it simply does not appear in `--collect-only`.
- Shared fixtures go in `tests/conftest.py`. That file is a declared oracle rather than ordinary
  test code, because it can drop files from collection entirely and turn a suite green by running
  less; `python-cli/standards-and-tests.md` declares it and says why.

**One test per behaviour the criterion names, and no more.** `parametrize` rows that differ only in
input formatting while reaching the same branch are duplication wearing a table's clothes. The full
set of excess cases belongs to `development/tdd-spec-driven` and is cited, not restated.

## Preconditions

This phase writes files and runs nothing itself, so it declares no machine-checkable environment
condition of its own. The conditions for running a Python test — the manifest, the interpreter and
the runner in the project's own environment — are declared by `python-cli/test-execution.md`, beside
the commands they are conditions of. The step that watches a test fail reads them there.

```yaml
preconditions: []
```

## Input contract

```yaml
code_path: string             # absolute path to the project root (the dir with pyproject.toml)
module: string                # the package module the behaviour belongs to
criterion_id: string          # the identifier of the criterion this test specifies
behavior: string              # what the test must observe, in a sentence
interface: string             # the names the module declares, and the names its dependencies declare
test_level: string            # optional; plain-unit | unit-with-collaborators | integration | entry-point | subprocess
```

`interface` is the only thing this reader gets about code that already exists, and it is a
declaration rather than source. Where it is empty, the behaviour must be observable from the
package's public API or from the console script's own contract.

## Sequence

If invoked in dry-run mode, emit the level choice, the file path, the test names, the parametrize
cases and the assertions planned, and write nothing. Dry-run is required.

1. **Select the level.** From `behavior` and the dependency surface it implies, using the table in
   Opinion. Use `test_level` if supplied. If the behaviour cannot be placed without opening the code,
   stop and report that rather than guessing: the choice belongs earlier.

2. **Place and name the file.** `tests/<path mirroring the package>/test_<module>.py`.

3. **Name the criterion in the test, and mark it.** The criterion identifier goes at the end of the
   function name, after an underscore, and nothing follows it:
   `test_submitted_form_saves_the_node_c3`. That keeps the criterion in the failure output and
   findable by grep with no runner support.

   For **selection**, add `@pytest.mark.criterion(id="c3")` as well, and register `criterion` under
   `[tool.pytest.ini_options] markers` so `--strict-markers` accepts it. Three things about this were
   checked on pytest 9.1.1 and each changes what a caller should write:

   - `-k` is an unanchored substring match with no regular expression and no anchor, so `-k c3` also
     selects `test_decodes_header_c30`. It cannot express "this criterion and no other" except as
     `-k 'c3 and not c30'`, which needs to know the sibling exists.
   - `-m 'criterion(id="c3")'` selects exactly the one test. The marker expression grammar accepts
     **keyword arguments only**.
   - `-m 'criterion("c3")'` — the positional form — does **not** filter and does **not** error. It
     parses as the bare marker name and selects every test carrying the marker at all. A caller that
     writes it gets a green run over the wrong set.

   The reliable selector without the marker is the node id, `tests/test_x.py::test_..._c3`, which is
   exact. A script reads the marks back out with `--collect-only -q` plus the marker expression.

4. **Write the test.** At the level selected, importing the package rather than shelling out. Assert
   on the return value, the exception type the contract assigns, or the exit code — never on prose
   captured from `capsys` that nothing promised. Assert on what the criterion names, and nothing
   else.

5. **Watch it fail.** Run it through `python-cli/test-execution.md` and read the failure signal
   declared there. Confirm the failure is the assertion, not an `ImportError` — a test that fails on
   an import has not tested anything. A test that passes immediately is rewritten once; if it still
   passes with no code behind it, stop and report it as proving nothing.

6. **Stop.** Return the level, the path, the test names, the criterion each carries, and the failure
   output for each. Write no production code.

## Data flow

Input: one criterion, the behaviour it names, the declared interface, the module.
Output: one or more test files under `tests/`, and for each test the criterion it carries and the
output of the run that failed.
Boundaries: reads no production source; writes only under the test tree and its fixtures; runs no
command except through `python-cli/test-execution.md`; produces no task record of its own.

## State-awareness contract

Before writing a new test, look for an existing test that already specifies the behaviour, by
searching the test tree for the criterion identifier, for the marker, and for the behaviour's own
vocabulary. Add a `parametrize` row to the existing test rather than adding a second one that
overlaps it. A bug fix almost always belongs on the existing test for the behaviour that broke.

Do not read the production source to make that decision. The test tree is readable; the code is not.

## Verifier

- Each test carries its criterion identifier at the end of its function name and a matching
  `@pytest.mark.criterion(id=...)`, so the criterion is both readable in the failure output and
  exactly selectable.
- Each test file sits under `tests/`, is named `test_<module>.py`, and every test function name
  starts with `test`. A helper that does not is not collected and nothing reports it.
- The `criterion` marker is registered in `pyproject.toml`, so `--strict-markers` does not reject it.
- Each new test was seen to fail on its assertion, not on an import, and not because working code was
  removed.
- No test asserts on prose captured from `capsys` that no contract pins. Assert on the return value,
  the raised exception type, or the exit code the contract assigns. Where a behaviour has no surface
  but printed prose, that is a finding about the tool rather than a reason to match harder.
- No test shells out to the console script except the single subprocess-level test per script that
  exists for the process boundary.
- No production file was written or changed.

## References

### Stack-neutral discipline (referenced, not authored here)

| Guide | What it holds |
|---|---|
| `development/tdd-spec-driven` | What a failing test proves, when not to write a test at all, the anti-patterns, and when a double is legitimate. Written for one person doing red, green and refactor; this reader does red and stops |

### Sibling process recipes

| Recipe | What it holds |
|---|---|
| `python-cli/test-execution.md` | The command at each scope, its cost, the conditions for running one, the node-identifier form, and how to read what came back |
| `python-cli/standards-and-tests.md` | The green and refactor half, the conformance rules a linter cannot see, and the `## Oracle files` declaration that names the test file patterns and `conftest.py` |

### External origins (referenced, not authored here)

| Origin | What it settled |
|---|---|
| pytest 9.1.1 | That a function not named `test*` is silently not collected; that `-k` is an unanchored substring match; that `-m` matches marker **keyword** arguments exactly, and that the positional form silently selects every test carrying the marker |
