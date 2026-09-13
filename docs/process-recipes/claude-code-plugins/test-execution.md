---
# Routing block — an orchestrator reads to here and decides.
name: claude_code_plugins_test_execution
capability: test-execution
description: Use when anything needs to run a Claude Code plugin project's tests and needs a straight answer that there is no test harness to run — what stands in its place, where the structural verdict comes from instead, and which framework's recipe answers for a component that does ship executable code.
# Metadata — read only after a match.
label: Test execution (Claude Code plugins)
recipe_schema_version: 1.0.0
version: 0.2.0
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

Answer one question for a Claude Code plugin project: what command runs a test. The answer is that there is none, and this recipe exists to say so by name rather than to leave a caller resolving nothing and guessing what that meant.

A plugin's components are instructions — a skill body, a command, an agent definition, a hook binding. There is no harness that executes them and reports, because there is nothing compiled and nothing to assert against. What stands in place of a test run is a trace of the instructions with concrete values, performed by an agent rather than by a command, and a structural verdict produced by a validator at the review phase. Neither is a test command, and calling either one would misreport what happened.

## Opinion

**Absent is an answer, and it is not the same as a row nobody wrote.** A caller that resolves this recipe and finds five rows answered by name knows the framework has no harness. A caller that resolves nothing cannot tell that from a recipe that was never authored, and the second one invites an improvised command — which is the failure this catalog keeps re-learning.

**A structural validator is not a test runner, and reporting it as one would be false.** `/plugin-creation-tools:validate` answers whether the frontmatter parses, the manifest is valid, the naming rules hold and a hook is bound to a real event. That is a genuine verdict and it belongs to the review phase, which owns it. It asserts nothing about whether a component does what it was written to do, so a green from it must never be reported as a passing test.

**The paper-test is the discipline in this framework, and it is not a command.** Tracing a component's instructions with concrete values through `code-paper-test:paper-test` is what the implement phase does in place of running a test. An agent performs it; there is no argv for it, no exit code, and no counts line. A caller asking for a test command is asking for something that does not exist here, and it is better told that than handed the nearest thing that does.

**Where a component ships executable code, that language answers.** A plugin carrying a Python script or a Go binary has tests in that language, and the commands for them come from that framework's own test-execution recipe, resolved by its framework rather than by this one. This recipe does not answer for them, because the resolution key is the framework, and the code's framework is not this one.

## Preconditions

None specific to running tests, because nothing here runs tests.

The two conditions this framework does declare — a `.claude-plugin` directory, and the availability of the authoring plugins — are conditions of *authoring* a component rather than of running one, so they stay with the `implement` recipe where they already are. Moving them here would put a precondition in front of a phase that does nothing with it.

```yaml
preconditions: []
```

## Input contract

Source-agnostic, supplied by the caller. Every field is accepted and none changes the answer.

```yaml
plugin_path: string           # absolute path to the plugin root
scope: string                 # suite | file | test | changed | smoke — the row to resolve
```

## Test commands

Six rows, six statements of absence. Each says what a caller asking for that scope should do instead.

```yaml
test_commands:
  - id: suite
    absent: >-
      A plugin has no test harness. Components are instructions, not compiled code,
      and nothing executes them to report. The implement phase traces each one with
      `code-paper-test:paper-test` instead, which an agent performs rather than a
      command runs.
  - id: file
    absent: >-
      There is no harness to scope to a file. A single component is traced the same
      way the whole set is, by reading it with concrete values.
  - id: test
    absent: >-
      There is no test case to select. The unit of verification here is a component
      and a traced scenario, neither of which has an identifier a runner resolves.
  - id: changed
    absent: >-
      There is no harness to scope to a change. The components a change touches are
      the components re-traced, decided by reading the diff.
  - id: smoke
    absent: >-
      Nothing proves a harness runs, because there is no harness. The nearest thing
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
| Does the executable code a component ships behave? | That language's test-execution recipe, resolved by its own framework | not this one |

```yaml
failure_signal:
  absent: >-
    There is no harness output to read. A paper-test returns an agent's findings
    against the component's instructions, and the structural validator returns
    errors and warnings — neither is an assertion result, and neither should be
    reported as a test outcome, red or green.
```

## Sequence

If invoked in dry-run mode, the answer is identical, because nothing is executed either way. Dry-run is required and is a formality here.

1. **Resolve the row.** Every row is answered with absence. Return the statement for the requested scope.

2. **Return what answers instead.** Name the paper-test for a behavioural question and the review phase's structural validator for a structural one, so the caller has somewhere to go rather than an empty result.

3. **Check whether the component ships executable code.** Where it does, say so and name the language, so the caller resolves that framework's test-execution recipe rather than concluding the code is untestable.

4. **Report absence as absence.** Never report the structural validator's result as a test result. A caller told "no tests ran" can decide what to do; a caller told "tests passed" has been given something that was never checked.

## Data flow

```
input: plugin_path, scope

reads project state:
       the component set (which components exist, and whether any ships code)

applies opinion:
       absent is an answer, and it is named rather than left empty · a structural
       validator is not a test runner · the paper-test is a trace an agent performs,
       not a command · executable code is answered by its own framework

references origin (never duplicated):
       code-paper-test:paper-test        — the instruction trace the implement phase runs
       /plugin-creation-tools:validate   — the structural verdict the review phase owns

emits (to the caller; the recipe runs nothing):
       answer:   absence, by name, for the requested scope
       instead:  what answers the question, and whose phase owns it
```

## State-awareness contract

The recipe reads. It writes no file, runs no command, and records nothing against the task. Its answer does not depend on project state, except for the one read that decides whether a component ships executable code and therefore belongs to another framework's recipe.

## Verifier

After the recipe runs, verify:

1. The requested row was answered with its statement of absence, not with an empty result and not with a substitute command.
2. No structural-validator run was reported as a test result, in either direction.
3. Where a component ships executable code, the caller was pointed at that language's test-execution recipe rather than told the component has no tests.
4. Anything downstream that required a test result received "no tests ran" rather than a pass.

This recipe ships no executable verifier of its own, and in this framework it ships no command either.

## References

### Plugin-side tooling (referenced, not authored here)

| Source | Used for |
|---|---|
| `code-paper-test:paper-test` | The instruction trace that stands in place of a test run, performed by an agent at the implement phase |
| `/plugin-creation-tools:validate` | The structural verdict — frontmatter parse, manifest validity, naming and hook bindings — owned by the review phase |

### Plugin-side generic mechanism (ai-dev-assistant)

The phases that would run a test command elsewhere are the plugin's. This recipe supplies the one thing that cannot be guessed at for this framework: that there is nothing for them to run, and what answers the question instead.
