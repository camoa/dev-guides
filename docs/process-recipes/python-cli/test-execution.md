---
# Routing block — an orchestrator reads to here and decides.
name: python_cli_test_execution
capability: test-execution
description: Use when anything needs to run a Python project's tests — the failing-test step watching one case, a baseline taken before code exists, a build check running the suite, or a fixer running the tests over its change — and needs the command, its cost, and how to tell a failed assertion from a collection that never happened.
# Metadata — read only after a match.
label: Test execution (Python CLI)
recipe_schema_version: 1.0.0
version: 0.2.1
requires_guides:
  - development/tdd-spec-driven
# Process-recipe routing keys, enforced by validate_recipes.py for any recipe
# under docs/process-recipes/. `capability` above doubles as the phase; there is
# no separate applies_to_phase. `framework` is the second routing dimension.
recipe_class: process
framework: python-cli
authors:
  - name: camoa
license: GPL-2.0-or-later
---

## Goal

Answer one question for a Python project: what command runs a test, at each of the scopes something actually asks for — the whole suite, one file, one case, the tests covering a change, and the cheapest thing that proves the runner works at all. Carry the traps that make a pytest invocation select something other than what it reads as, and the exit codes that separate a failed assertion from a collection that never happened.

This recipe runs nothing and judges nothing. It is read by whatever is about to run a test, and the callers differ: the author watching one case fail, the baseline taken before any code exists, each build check, and the fixer running the tests over its own change.

## Opinion

**A command is argv, never a shell string.** Each row below is a list of tokens executed directly. A token that is exactly a named placeholder is replaced whole, and the substituted value never reaches a shell.

**The runner is the project's, not a fixed binary.** Every row starts with `{runner}`, resolved from what the project declares in `pyproject.toml` and defaulting to `.venv/bin/pytest`. The Python tooling has genuinely turned over and a project may have rejected the runner we would otherwise name; the design phase already declines to hard-code one, and a command row that named a binary would quietly undo that.

**`python -m pytest` and `pytest` are not the same command.** The module form prepends the current directory to `sys.path`, so a project whose package is importable only from the tree passes under one and fails to import under the other. Whichever form the project declares is the form every row uses, because a baseline taken with one and a check run with the other are not comparable.

**pytest's exit codes carry real information, which is unusual and worth using.** Exit 1 is a failed assertion. Exit 4 is a usage error, which is also what a mistyped node identifier and a missing file produce. Exit 5 is nothing collected. All three were observed on pytest 9.1.1. Unlike the other frameworks in this catalog, a mistyped selector here does not report success.

**`-k` deselects, and deselecting everything is a success by count and a failure of intent.** A `-k` that matches nothing exits 5, so it is detectable — but `-k` matches substrings across the whole identifier, so a pattern intended to select one case routinely selects several. A node identifier selects exactly one; prefer it.

**pytest has no changed-file test selection, and saying so is the answer.** `--lf` and `--ff` reorder or repeat what failed last time, which is a different question. The caller passes the test files it decided cover the change.

## Preconditions

- A `pyproject.toml` at the project root, where the toolchain is declared.
- A Python interpreter on the path, so the runner can run at all.
- A pytest runner in the project's own environment whose failure the failing-test step can observe.

All three are checkable and are declared in machine-readable form below. All three name the operator as owner, because nothing in this catalog installs a Python interpreter or provisions a project's virtual environment. That is a real value, not a placeholder for one: an entry nobody owns and an entry whose owner was forgotten are different states, and leaving the key off makes them look the same.

Two honest limitations, recorded rather than hidden. `python3 --version` is both the check and its own subject, so with no interpreter it exits 127 and the engine records `unknown / check_command_not_found` — weaker than `unmet`, but not `met`. And the runner check looks in `.venv/bin/`, which is a convention rather than a standard: a project using tox, a container with pytest on `PATH` and no local virtualenv, or a poetry install keeping its environment outside the tree reports `unmet` while being perfectly runnable. That is a false negative in the safe direction, and no single argv command covers both layouts, because the engine never uses a shell and the alternatives cannot be OR'd.

```yaml
preconditions:
  - id: python-project
    what: a pyproject.toml at the project root, where the toolchain and the runner are declared
    check: test -f pyproject.toml
    owner: operator
  - id: python-interpreter
    what: a Python interpreter on the path, so the toolchain and the tests can run at all
    check: python3 --version
    owner: operator
  - id: test-runner
    what: a pytest runner in the project's own environment whose failure the failing-test step can observe
    check: test -x .venv/bin/pytest
    owner: operator
```

## Input contract

Source-agnostic, supplied by the caller.

```yaml
code_path: string             # absolute path to the project root (the dir with pyproject.toml)
scope: string                 # suite | file | test | changed | smoke — the row to resolve
runner: string                # optional; the runner the project declares (default .venv/bin/pytest)
file: string                  # optional; one test file path
test_id: string               # optional; one node identifier
paths: [string]               # optional; the test files a change is scoped to
```

## Test commands

Six rows. Each is a command or a named statement that this framework has none. `{runner}` is the project's declared runner, `{file}` one test file path, `{test_id}` one node identifier, and `{paths}` a list that expands to one token per element.

```yaml
test_commands:
  - id: suite
    argv: ["{runner}"]
    cost: end-of-task
    trap: >-
      Collects from the roots `pyproject.toml` declares. A project that declares
      none collects from the working directory, so the same command run from a
      subdirectory silently runs a different set of tests.
  - id: file
    argv: ["{runner}", "{file}"]
    cost: every-attempt
    trap: >-
      A path that does not exist is a usage error and exits 4, not an empty run.
      This is the framework where a typo is caught rather than reported as success.
  - id: test
    argv: ["{runner}", "{test_id}"]
    id_form: >-
      A node identifier, `tests/test_thing.py::TestGroup::test_name`, with the class
      segment present only where the test is a method. A parametrized case carries
      its parameters in brackets after the name.
    cost: every-attempt
    trap: >-
      Prefer a node identifier to `-k`. `-k` matches substrings across the whole
      identifier, so a pattern meant to select one case selects several, and a
      pattern that selects nothing exits 5 rather than failing outright.
  - id: changed
    absent: >-
      pytest maps no set of changed paths to the tests covering them. `--lf` and
      `--ff` reorder what failed last time, which answers a different question. The
      caller decides which test files cover the change and passes them.
    nearest: ["{runner}", "{paths}"]
  - id: smoke
    argv: ["{runner}", "--collect-only", "-q"]
    cost: every-attempt
    trap: >-
      Proves collection and every import it performs. It runs no test, so it proves
      nothing about behaviour — but an import error in the package surfaces here,
      which is the failure most often mistaken for a failing test.
  - id: mutation
    argv: ["mutmut", "run"]
    cost: end-of-task
    trap: >-
      A report, not a gate, and it takes no path. mutmut 3.8.0 exited 0 with 658 of
      2,982 mutants survived; the last line of the run is a count per outcome — `🎉`
      killed, `🙁` survived, `⏰` timed out, `🫥` no test covered it — and
      `mutmut results` lists each survivor by mutant name, `pkg.m.x_big__mutmut_1`.
      What it mutates comes from `[tool.mutmut] source_paths` in `pyproject.toml`, not
      from argv: `run` accepts mutant names, and `--paths-to-mutate` is not an option.
      Scoping to changed files is `use_git_change_detection` in that section, not a
      change to this row. It rewrites the source into a `mutants/` directory at the
      project root and leaves it there, and its first step runs the whole suite once
      and stops at the first failure with `failed to collect stats. runner returned 1`,
      exit 1.
```

**Why the mutation row carries no `{paths}`.** mutmut 3 rewrote its interface: `mutmut run` takes
mutant names, the source paths live in `pyproject.toml`, and the older `paths_to_mutate` key is
deprecated in favour of `source_paths`. A mutant name that matches nothing —
`mutmut run pkg.m.big` — stops with `Filtered for specific mutants, but nothing matches` and exit 1,
so a scoped run that mistypes its target is an error rather than an empty pass.

**Two kinds of test do not work under mutmut, and both are ones this catalog asks for.** mutmut runs
pytest from inside `mutants/`, a copy of the tree holding a rewritten package whose every function
imports a trampoline from `mutmut` itself. A test that runs the package in a child interpreter —
the subprocess level, `python -S -c` with only `src` on the path — either cannot import the
trampoline and fails, or imports the real package from its own path and exercises unmutated code,
so a mutant covered only by such tests reports as survived or as `🫥 no tests` and is not a test
gap. A test that builds the wheel finds a tree with no `README.md` and with `.meta` and `.spans`
files in it. Both were hit on a project with 27 source files: the stats run stopped on an
isolated-child test, then on a wheel test. What made it run was a `[tool.mutmut]` section with
`also_copy = ["README.md", "LICENSE", "NOTICE"]` and `pytest_add_cli_args` deselecting the
subprocess and packaging tests; 2,982 mutants then ran in 70 s, and 401 of the 406 `no tests`
results sat in the one module that is tested through the console script.

**What each row costs.** The tiers this framework's implement recipe selects among differ mostly at the subprocess boundary.

| Tier | Cost | Run it |
|---|---|---|
| Plain unit, unit with collaborators | milliseconds per test | every build attempt |
| Integration / fixture | seconds, composed pieces | every build attempt, over the changed scope |
| Entry point | in-process, imports the package | every build attempt |
| Subprocess | a process spawn per case | once, at the end of a task |

**Telling a failed assertion from harness noise.** Exit codes 0, 1, 4 and 5 were observed on pytest 9.1.1; 2 and 3 are pytest's documented interrupted and internal-error codes.

```yaml
failure_signal:
  assertion: >-
    Exit 1, with a `FAILED <node id>` line per failing test — the test ran, asserted,
    and the assertion did not hold. This is the only outcome that proves a behaviour
    is absent.
  harness: >-
    Exit 4 is a usage error, and it covers a mistyped node identifier, a missing file
    and an unknown option — the run never started. Exit 5 means nothing was collected,
    which a `-k` that deselects everything produces. Exit 2 is an interrupted run and
    exit 3 an internal error. None of these says anything about the code.
  silent_pass: >-
    None. This is the framework where a selector that matches nothing is a distinct
    exit code rather than a success, so a green here is a green.
```

## Sequence

If invoked in dry-run mode, resolve and return the command without executing it. Dry-run is required.

1. **Resolve the runner.** Take it from the caller, or from what `pyproject.toml` declares, or default to `.venv/bin/pytest`. Whichever it is, it is the same one for every row in this run — a baseline taken with one runner and a check run with another are not comparable.

2. **Resolve the row.** Take `scope` and select the matching row above. A row answered with `absent:` returns that statement and its `nearest:` form; it does not fall through to a wider command.

3. **Substitute the placeholders.** Replace each placeholder token whole. A list placeholder expands to one token per element. Nothing is concatenated into a token and nothing is passed through a shell.

4. **Apply the cost label.** Return the row's `cost` with the command, so a caller running on every build attempt does not receive the subprocess tier.

5. **Return the command, the cost, and the failure signal.** The caller runs it. This recipe neither executes it nor judges its output.

6. **Read the result against the failure signal.** Only exit 1 is a statement about the code. Exit 4 and exit 5 are the run never happening, and reporting either as a red is how absent code gets mistaken for proven-absent code.

## Data flow

```
input: code_path, scope, runner / file / test_id / paths (optional)

reads project state:
       pyproject.toml (the declared runner, the collection roots, the test config)
       .venv/bin/ (the runner the project's own environment provides)

applies opinion:
       argv, never a shell string · the project's declared runner, not a fixed
       binary · python -m pytest and pytest differ in sys.path · a node identifier
       over -k · exit 1 alone is a statement about the code

references origin (never duplicated):
       pytest — the runner, its node-identifier syntax, and its exit codes

emits (to the caller; the recipe runs nothing):
       command:  the argv token list for the requested row, placeholders substituted
       cost:     every-attempt | end-of-task
       signal:   how to read the exit code — assertion, usage, or nothing collected
```

## State-awareness contract

The recipe reads. It writes no file, runs no command, creates no environment, and records nothing against the task. Resolving the same row with the same input returns the same command; what the command then does depends on the project's state, which is the caller's to observe.

## Verifier

After the recipe runs, verify:

1. The returned command is a token list, and every placeholder was substituted as a whole token — nothing was concatenated into a token and nothing reached a shell.
2. The runner came from the project's declaration rather than a hard-coded binary, and the same runner was used for every command in the run.
3. The row requested was the row returned. A row answered `absent:` returned that statement, not a wider command that happens to include the wanted tests.
4. A command selecting one case used a node identifier, and `-k` was used only where selecting several cases was the intent.
5. The cost label travelled with the command, and no caller running on every build attempt received the subprocess tier.
6. Only an exit 1 was reported as a red. An exit 4 or 5 was reported as the run not having happened.

This recipe ships no executable verifier of its own — it produces a command and the means to read the result, and the phase that runs it owns the gate.

## References

### External origins (referenced, not authored here)

| Source | Used for |
|---|---|
| pytest | The runner, its node-identifier syntax, its `-k` semantics, and its exit codes |
| `pyproject.toml` | Where the project declares its runner, its collection roots and its test configuration |
| `development/tdd-spec-driven` | What a failing test proves, and why a run that asserted nothing is neither red nor green |

### Plugin-side generic mechanism (ai-dev-assistant)

The phases that run these commands — the failing-test step, the baseline, the build checks, the fixer — are the plugin's, along with whatever records their results. This recipe supplies only what a Python project cannot be guessed at: the command per scope, its cost, and how to read what came back.
