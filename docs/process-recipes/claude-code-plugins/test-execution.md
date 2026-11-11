---
# Routing block — an orchestrator reads to here and decides.
name: claude_code_plugins_test_execution
capability: test-execution
description: Use when anything needs to run a Claude Code plugin project's tests and needs a straight answer that no suite command runs a plugin's components — which row runs one shell spec an order owns, what stands in for the rest, where the structural verdict comes from instead, and which framework's recipe answers for a component that does ship executable code.
# Metadata — read only after a match.
label: Test execution (Claude Code plugins)
recipe_schema_version: 1.0.0
version: 0.3.0
# Process-recipe routing keys, enforced by validate_recipes.py for any recipe
# under docs/process-recipes/. `capability` above doubles as the phase; there is
# no separate applies_to_phase. `framework` is the second routing dimension.
recipe_class: process
framework: claude-code-plugins
authors:
  - name: camoa
license: GPL-2.0-or-later
---

## Goal

Answer one question for a Claude Code plugin project: what command runs a test. The answer is that no suite row here runs one, and this recipe exists to say so by name rather than to leave a caller resolving nothing and guessing what that meant. The one exception is a shell spec for the executable code a plugin ships: the `file` row runs one with `bash`.

A plugin's components are instructions — a skill body, a command, an agent definition, a hook binding. No suite row here executes them, because there is nothing compiled and nothing to assert against. `claude plugin eval`, from Claude Code 2.1.269, does run a plugin's skills against eval cases, but it calls a model on every case. The skill-authoring agentic recipe runs it as its verifier, not as a suite row here. What stands in place of a test run is a trace of the instructions with concrete values, performed by an agent rather than by a command, and a structural verdict produced by a validator at the review phase. Neither is a test command, and calling either one would misreport what happened.

## Opinion

**Absent is an answer, and it is not the same as a row nobody wrote.** A caller that resolves this recipe and finds five rows answered by name and one `file` row knows no suite row runs this framework's components. A caller that resolves nothing cannot tell that from a recipe that was never authored, and the second one invites an improvised command — which is the failure this catalog keeps re-learning.

**A structural validator is not a test runner, and reporting it as one would be false.** `/plugin-creation-tools:validate` answers whether the frontmatter parses, the manifest is valid, the naming rules hold and a hook is bound to a real event. That is a genuine verdict and it belongs to the review phase, which owns it. It asserts nothing about whether a component does what it was written to do, so a green from it must never be reported as a passing test.

**The paper-test is the discipline in this framework, and it is not a command.** Tracing a component's instructions with concrete values through `code-paper-test:paper-test` is what the implement phase does in place of running a test. An agent performs it; there is no argv for it, no exit code, and no counts line. A caller asking for a test command for an instruction is asking for something that does not exist here, and it is better told that than handed the nearest thing that does.

**Where a component ships executable code, that language answers.** A plugin carrying a Python script or a Go binary has tests in that language, and the commands for them come from that framework's own test-execution recipe, resolved by its framework rather than by this one. This recipe does not answer for them, because the resolution key is the framework, and the code's framework is not this one. A shell spec is the exception: it is a bash script that drives the code from outside, and the `file` row runs it.

## Preconditions

None specific to running tests. The `file` row needs `bash`, which every shell spec already needs.

The two conditions this framework does declare — a `.claude-plugin` directory, and the availability of the authoring plugins — are conditions of *authoring* a component rather than of running one, so they stay with the `implement` recipe where they already are. Moving them here would put a precondition in front of a phase that does nothing with it.

```yaml
preconditions: []
```

## Input contract

Source-agnostic, supplied by the caller. Every field is accepted and none changes the answer.

```yaml
plugin_path: string           # absolute path to the plugin root
scope: string                 # suite | file | test | changed | smoke — the row to resolve
file: string                  # optional; one shell spec path, for the `file` row
```

## Test commands

Six rows: one command and five statements of absence. The `file` row runs one `<plugin>/tests/*-spec.sh` spec, the file `claude-code-plugins/test-authoring.md` writes for the executable code a plugin ships. Each absent row says what a caller asking for that scope should do instead.

```yaml
test_commands:
  - id: suite
    absent: >-
      No suite command runs a plugin's components. They are instructions, not compiled
      code, and nothing here executes them to report. The implement phase traces each one with
      `code-paper-test:paper-test` instead, which an agent performs rather than a
      command runs.
  - id: file
    argv: ["bash", "{file}"]
    cost: every-attempt
    trap: >-
      Runs one shell spec, which exits 0 when every case passed and non-zero when
      one failed or none ran. `{file}` expands to every test file the order owns, one
      token each, and bash runs only the first: the rest become that spec's
      arguments, so a spec that ignores its arguments passes without the others
      running. An order owns one spec file. A unit test in the script's own language
      is not a shell script and is not run here. A skill, command or agent has no
      file here at all; it is traced, not run.
  - id: test
    absent: >-
      There is no test case to select. The unit of verification here is a component
      and a traced scenario, neither of which has an identifier a runner resolves.
  - id: changed
    absent: >-
      No row maps a change to the specs and components it touches, and bash takes
      one script, so no command runs a set of specs. The caller reads the diff: the
      components it touches are re-traced, and an order's own spec runs through the
      `file` row.
  - id: smoke
    absent: >-
      Nothing proves a suite runs, because no suite row exists here. The nearest thing
      is the structural validator the review phase owns, and it is not a test run —
      a green from it says the files parse, never that a component behaves.
  - id: mutation
    absent: >-
      No mutation tool is established for this framework, and there is no suite for
      one to run: a mutant of an instruction has no test that would kill it.
```

**What answers instead, and who owns it.**

| The question | What answers it | Whose phase |
|---|---|---|
| Does this component's instruction hold up with concrete values? | `code-paper-test:paper-test`, or `/code-paper-test:test-team` for a large or security-sensitive component | implement |
| Does the frontmatter parse, the manifest validate, the naming and hook bindings hold? | `/plugin-creation-tools:validate`, under `--strict` | review |
| Does the executable code a component ships behave, seen from its exit code and output? | Its shell spec, through the `file` row | implement |
| Does the executable code a component ships behave, function by function? | That language's test-execution recipe, resolved by its own framework | not this one |

```yaml
failure_signal:
  absent: >-
    No output shape is shared. A shell spec prints a line per failed case in its own
    words and exits non-zero, and bash itself exits 127 for a missing spec and 2 for
    one that does not parse, so the exit code says that something failed and only
    the printed label says which case. A paper-test returns an agent's findings,
    and the structural validator returns errors and warnings; neither is an
    assertion result, and neither should be reported as a test outcome, red or
    green.
```

## Sequence

If invoked in dry-run mode, the answer is identical, because nothing is executed either way. Dry-run is required and is a formality here.

1. **Resolve the row.** The `file` row returns `bash` and the spec path; every other row is answered with absence. Return the command or the statement for the requested scope.

2. **Return what answers instead.** Name the paper-test for a behavioural question and the review phase's structural validator for a structural one, so the caller has somewhere to go rather than an empty result.

3. **Check whether the component ships executable code.** Where it does, its shell spec runs through the `file` row. For a unit test in the code's own language, name the language, so the caller resolves that framework's test-execution recipe rather than concluding the code is untestable.

4. **Report absence as absence.** Never report the structural validator's result as a test result. A caller told "no tests ran" can decide what to do; a caller told "tests passed" has been given something that was never checked.

## Data flow

```
input: plugin_path, scope

reads project state:
       the component set (which components exist, and whether any ships code)

applies opinion:
       absent is an answer, and it is named rather than left empty · a structural
       validator is not a test runner · the paper-test is a trace an agent performs,
       not a command · a shell spec runs through the `file` row · a unit test in
       another language is answered by its own framework

references origin (never duplicated):
       code-paper-test:paper-test        — the instruction trace the implement phase runs
       /plugin-creation-tools:validate   — the structural verdict the review phase owns

emits (to the caller; the recipe runs nothing):
       answer:   the `file` command, or absence by name, for the requested scope
       instead:  what answers the question, and whose phase owns it
```

## State-awareness contract

The recipe reads. It writes no file, runs no command, and records nothing against the task. Its answer does not depend on project state, except for the one read that decides whether a component ships executable code and therefore belongs to another framework's recipe.

## Verifier

After the recipe runs, verify:

1. The requested row was answered with its command or its statement of absence, not with an empty result and not with a substitute command.
2. A `file` run named one spec, and that spec's exit code was read as its result.
3. No structural-validator run was reported as a test result, in either direction.
4. Where a component ships executable code with no shell spec, the caller was pointed at that language's test-execution recipe rather than told the component has no tests.
5. Anything downstream that required a test result received "no tests ran" rather than a pass.

This recipe ships no executable verifier of its own. Its one command is the `file` row.

## References

### Plugin-side tooling (referenced, not authored here)

| Source | Used for |
|---|---|
| `code-paper-test:paper-test` | The instruction trace that stands in place of a test run, performed by an agent at the implement phase |
| `/plugin-creation-tools:validate` | The structural verdict — frontmatter parse, manifest validity, naming and hook bindings — owned by the review phase |

### Plugin-side generic mechanism (ai-dev-assistant)

The phases that would run a test command elsewhere are the plugin's. This recipe supplies the one thing that cannot be guessed at for this framework: that there is nothing for them to run, and what answers the question instead.
