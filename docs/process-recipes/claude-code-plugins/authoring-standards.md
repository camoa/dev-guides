---
# Routing block — an orchestrator reads to here and decides.
name: cc_plugins_implement_authoring_standards
capability: implement
description: Use when a Claude Code plugin project enters the implementation phase and must hold each component to its authoring contract — scaffolds from the canonical templates, writes the SKILL.md / command / agent / hook frontmatter and body to standard, honours progressive disclosure, and paper-tests every component's instructions to catch logic errors and hallucinated tools before they ship. Defers scaffolding to plugin-creation-tools and the blocking structural gate to the review phase.
# Metadata — read only after a match.
label: Component authoring standards (Claude Code)
recipe_schema_version: 1.0.0
version: 0.3.0
# Machine-readable dependency declaration (recipe-loader resolves these
# without parsing prose). The test-discipline rules are stack-neutral: they are
# cited here, never restated per framework.
requires_guides:
  - development/tdd-spec-driven
# Process-recipe routing keys, enforced by validate_recipes.py for any recipe
# under docs/process-recipes/. `capability` above doubles as the phase (the
# lifecycle moment the orchestrator resolves on); there is no separate
# applies_to_phase. `framework` is the second routing dimension.
recipe_class: process
framework: claude-code-plugins
assumes:
  - claude-code
authors:
  - name: camoa
license: GPL-2.0-or-later
---

## Goal

Build the components the design recorded, holding each to its authoring contract as it is written. The implementation scaffolds from the canonical templates, writes each `SKILL.md`, command, agent, and hook to the frontmatter and body rules its component type requires, honours the body/`references/` split the design fixed, and **paper-tests every component's instructions** — tracing them with concrete values to catch logic errors and hallucinated tools before the work reaches the gate. It applies the standards and the test-first discipline; it defers the scaffolding execution to `plugin-creation-tools` and the blocking structural verdict to the review phase.

The plugin owns the generic implement phase — when it runs and the oracle/envelope it emits. This recipe owns what the stack-neutral mechanism cannot know: the Claude-Code component contracts, the authoring rules that keep a component loadable and a description fire-able, and what "test-first" means for a plugin whose substance is instructions.

## Opinion

**Scaffold from the templates; do not hand-roll structure.** A new plugin comes from `/plugin-creation-tools:create` and a new component from `/plugin-creation-tools:add-component`, so the directory shape, the manifest, and the frontmatter skeleton start correct. Hand-built structure is how a plugin acquires a misplaced manifest or a frontmatter key the loader silently drops.

**Frontmatter is the contract, and a bad one fails silently.** A `SKILL.md` `name` is kebab-case, at most 64 characters, and contains no reserved word (`anthropic`, `claude`); its `description` states *what* it does and *when* to use it, in the third person, inside the budget, with no XML angle brackets in any frontmatter value. A command carries `description` and `allowed-tools`. An agent carries `name`, a `description` with explicit delegation triggers, `tools`, and `model`. The block must parse as YAML — a parse failure drops every key at load with no error, so the frontmatter is authored as carefully as the body.

**The tool-block casing split is real and unforgiving.** A skill hard-blocks tools with kebab-case `disallowed-tools`; an agent uses camelCase `disallowedTools`. The wrong casing on the wrong component type is silently ignored, so the block is written to the component type, not from habit.

**Skill bodies are imperative instructions, not documentation.** The body tells the model what to do, in the imperative, kept under the length the design fixed, with the depth in `references/`. Prose that *describes* the skill instead of *instructing* the model is a body that will not drive behaviour.

**Hooks are authored to the event and the handler, defensively.** A hook binds a recognised event and a valid handler type; it prefers the exec form with explicit `args` over a shell-form string; it braces its placeholders (`${CLAUDE_PLUGIN_ROOT}`, not a bare `$CLAUDE_PLUGIN_ROOT`); it sets an explicit timeout; and it never writes to `/dev/tty`, which has no controlling terminal. A one-time install belongs on a setup event, not on session start.

**Test-first for a plugin is paper-testing the instructions.** A component's "code" is the instruction set it feeds the model, so the test that matters is a line-by-line trace of that instruction set with concrete values — does the skill's logic hold, does the command's argument handling do what the frontmatter promises, does the hook fire on the event it claims. This trace is run *before* the component is trusted, the Red-Green discipline applied to prose, and it is deferred to `code-paper-test:paper-test` (or `/code-paper-test:test-team` for a large or security-sensitive component) rather than re-implemented here.

**The paper-test is the loop's analogue, and it is worth being precise about how far the analogy runs.** A plugin's substance is instructions, so there is no failing assertion to watch go red — what stands in for it is tracing the instruction set against what the component was designed to do, before anyone relies on it. That much is genuinely the same discipline: the contract comes first, and the component is judged against it rather than described by it. What it is not is a substitute for a test suite where a plugin ships executable code — a hook script, a validator, a helper — which is ordinary code and gets ordinary test-first treatment at the tier its dependency surface calls for.

**Adding a check is not automatically progress.** The same brake applies here as to any suite: a check earns its place by specifying a behaviour the component promised, and past that it makes the component harder to review without constraining anything new. The full set of excess cases belongs to `development/tdd-spec-driven` and is cited, not restated. Two local forms worth naming: a paper-test that re-asserts the frontmatter rules `/plugin-creation-tools:validate` already enforces deterministically is duplication of a check that runs for free, and a trace that quotes a component's own body back as evidence that the body is correct is the ratifying case in its plainest form — the trace has to come from the design, not from the prose it is judging.

**Every external reference is verified to exist.** A skill that tells the model to call a tool, invoke a sibling skill, or pass a flag is verified against the real surface — a hallucinated tool name, a non-existent flag, or a renamed API (the Agent SDK rename is the common one) is the plugin equivalent of a hallucinated symbol, and it is caught at authoring time, not left for a user to hit.

**Implement authors to the contract and sanity-checks; the blocking gate is review's.** The implementation may run `/plugin-creation-tools:validate --dry-run` as it goes to catch a structural slip early, but the authoritative structural verdict — the one that blocks acceptance — is the review phase's. This phase produces correct, paper-tested components; it does not own the gate.

## Preconditions

- A Claude Code environment with plugin support and the `plugin-creation-tools` and `code-paper-test` plugins available — this recipe drives them rather than reproducing them.
- The component map is available (see the architecture recipe under this framework): every component with its type, responsibility, trigger, permissions, model, and body/`references/` split. The implementation builds what the map recorded, not a re-derived design.
- The plugin's generic implement phase is present: the phase that invokes this method and emits its oracle/envelope. This recipe supplies the Claude-Code authoring standards and the paper-test discipline; it does not recreate the phase.

Two of these are declared in machine-readable form below, and the split is deliberate.

The manifest condition has a real filesystem probe. The plugin-availability one does not: whether `plugin-creation-tools` and `code-paper-test` are installed is not answerable from the project tree by any argv-safe command, so it is declared with no `check:` and the engine records it `unknown` — never `met`. That keeps a genuine precondition visible instead of dropping it for being unverifiable, which is the defect this declaration exists to close. It does mean this recipe cannot currently reach an overall `met` verdict; that is the honest state, not a bug in the declaration.

preconditions:
  - id: plugin-manifest
    what: a .claude-plugin/ directory, so the project is a plugin or marketplace repo at all
    check: test -d .claude-plugin
    owner: plugin-creation-tools:create
  - id: authoring-plugins
    what: plugin-creation-tools and code-paper-test available — this recipe drives them rather than reproducing them
    owner: plugin-creation-tools:create

## Input contract

Source-agnostic, supplied by the caller (the orchestrator at the implement phase, or a human operator).

```yaml
component_map: string         # path to / content of the architecture artifact:
                              #   the components to build and their contracts
plugin_path: string           # absolute path to the plugin root (existing, when extending)
target: string                # new-plugin | extend; mirrors the design boundary
scope: [string]               # optional; the subset of components to author this pass
```

## Sequence

If invoked in dry-run mode, perform the reads and emit an authoring plan plus the paper-test targets instead of writing components. Dry-run is required.

1. **Scaffold from the templates.** For a new plugin, run `/plugin-creation-tools:create` with the component set from the map; for an extend, run `/plugin-creation-tools:add-component` per new component. The structure, manifest, and frontmatter skeletons start from the canonical templates.

2. **Author each component to its contract.** Write the `SKILL.md` / command / agent / hook frontmatter to its type's rules (the `name`/`description`/budget/reserved-word/XML rules for skills; `description` + `allowed-tools` for commands; `name` + trigger `description` + `tools` + `model` for agents; the correct tool-block casing per type) and the body in imperative voice, grounded in `plugin-creation-tools:plugin-creation` rather than recalled.

3. **Honour progressive disclosure.** Keep each `SKILL.md` body to the lean instruction set the design fixed and place the on-demand depth in `references/`; confirm every referenced file and script the frontmatter or body names actually exists.

4. **Author hooks defensively.** Bind the recognised event and a valid handler, prefer exec form with explicit `args`, brace every `${CLAUDE_*}` placeholder, set an explicit timeout, and route nothing to `/dev/tty`.

5. **Paper-test every component before trusting it.** Trace each component's instructions with concrete values through `code-paper-test:paper-test` (or `/code-paper-test:test-team` for a large or security-sensitive component), and verify every external reference — tool, sibling skill, flag, API symbol — resolves to something real. Fix what the trace surfaces before the component is considered done. Where the component ships executable code, its tests follow the ordinary test-first discipline, and once such a test is committed, who may change or delete it is the mutability matrix's answer in `development/tdd-spec-driven`, not this phase's.

6. **Sanity-check, and hand the gate to review.** Optionally run `/plugin-creation-tools:validate --dry-run` to catch a structural slip early. The blocking structural verdict is not formed here — it is the review phase's; this phase returns the authored, paper-tested components and the trace results.

## Data flow

```
input: component_map, plugin_path, target (new-plugin | extend), scope (optional)

reads project state:
       the component map (the components to build and their contracts)
       the existing plugin layout, when extending
       the documented component contracts + authoring rules (read, not recalled)

applies opinion:
       scaffold from templates · frontmatter is the contract, bad parses fail silently
       · the disallowed-tools casing split · imperative skill bodies · hooks to event +
       handler, defensively · test-first = paper-test the instructions · verify every
       external reference · implement authors + sanity-checks, review owns the gate

references origin (never duplicated):
       plugin-creation-tools:plugin-creation — component contracts + authoring rules
       /plugin-creation-tools:create, /plugin-creation-tools:add-component — scaffolding
       /plugin-creation-tools:validate --dry-run — mid-build structural sanity
       code-paper-test:paper-test, /code-paper-test:test-team — the instruction trace

emits (to the caller; the recipe records via the tools it drives):
       components:   the authored skill / command / agent / hook files
       trace:        per-component paper-test result + external-reference verification
       handoff:      the components handed to the review phase, which owns the verdict
```

## State-awareness contract

The recipe reads the component map and, when extending, the existing plugin layout before writing — it builds the recorded design into the real plugin, not an idealized scaffold, and it adds to what is already there rather than overwriting it. The writes it makes are mediated by the scaffolding tools it drives (`/plugin-creation-tools:create`, `/plugin-creation-tools:add-component`) and the component files it authors; it forms no blocking verdict and installs no gate — the paper-test results and the authored components are handed to the review phase, which owns acceptance.

Idempotent against the map: re-running over the same component map and the same plugin state reproduces the same components and the same trace targets; a scaffolder run twice adds the missing component once and is a no-op on what already conforms. Output that changes because the map changed is the implementation reflecting the current design, not a non-deterministic recipe.

## Verifier

After the recipe runs, verify:

1. New structure came from the scaffolders (`/plugin-creation-tools:create` / `/plugin-creation-tools:add-component`), not hand-rolled — the manifest sits in `.claude-plugin/plugin.json` and each component is in its component directory.
2. Every component's frontmatter parses as YAML and meets its type's contract — skill `name`/`description`/budget/reserved-word/no-XML rules, command `description` + `allowed-tools`, agent `name` + trigger `description` + `tools` + `model`, and the correct `disallowed-tools` (skill, kebab) vs `disallowedTools` (agent, camel) casing.
3. Each `SKILL.md` body is imperative and within the designed length, with depth in `references/`, and every referenced file and script exists.
4. Each hook binds a recognised event and a valid handler, uses exec form with braced `${CLAUDE_*}` placeholders and an explicit timeout, and writes nothing to `/dev/tty`.
5. Every component was paper-tested before being trusted, and every external reference it names — tool, sibling skill, flag, API symbol — was verified to resolve; what the trace surfaced was fixed.
6. Each paper-test traces the component against what the design said it must do, not against the component's own body, and no trace duplicates a rule `/plugin-creation-tools:validate` already enforces deterministically.
7. Where the change ships executable code, that code has a test at a deliberately chosen tier, written before it and seen to fail.
8. The blocking structural verdict was left to review — this phase returned authored, paper-tested components and their trace results, not an acceptance decision.
9. Every pre-existing test the change modified or deleted was changed by a role the mutability matrix permits — the only rows that may delete are a feature removal taking its own tests in the same commit; RED authoring is the only row that writes an assertion, and GREEN, REFACTOR and a bug fix change none. A reviewer that wanted a test changed filed a finding instead. See `development/tdd-spec-driven`.

This recipe ships no executable verifier of its own — the authoring-and-trace steps are the agent-driven protocol, executed through the tools it drives; the plugin's implement phase owns its oracle/envelope, and the structural gate belongs to the review phase.
## Oracle files

A measurement oracle is a file the gates read to decide pass or fail — a test, a lint suppression baseline, a CI definition. An autonomous builder must never weaken one to make a red gate go green: only adding tests or fixing components is allowed, never suppressing a finding. The plugin's deterministic oracle-tamper guard enforces this at the review/critique rung, but the guard itself is framework-agnostic — it carries no Claude-Code knowledge and monitors only the file list it is handed. This section is that list for a plugin project: the caller reconstructs it from here on every run (so there is no persistent project file a builder could empty to switch monitoring off) and hands it to the guard.

Each rule names the change kinds it watches (A added, M modified, D deleted), the oracle class the change touches, and a severity. A **halt** is terminal tamper unless the work-order's `oracle_update` field explicitly exempts that class; a **flag** is recorded and the work ships flagged, never blocked.

This section exists because a plugin repository is exactly where the missing-glob-source problem was first found: a project whose substance is instructions looks like it has no test surface, so nothing gets declared, and a guard handed an empty list reports a clean run it never performed.

| Oracle file | Watches | Class | Severity | Why |
|---|---|---|---|---|
| Shell spec files (`*-spec.sh` under any `tests/` directory) | delete | test-delete | halt | These are the executable tests of a plugin's scripts and hooks. Deleting one removes the behaviour it guards — the builder must add tests, never drop them, to pass. |
| A lint suppression baseline (`lint-baseline.txt`, `.shellcheck-baseline`) | add / modify | lint-baseline | halt | A shellcheck baseline suppresses known findings by file and code — appending to it hides a *new* lint error instead of fixing it. Same shape as a phpstan baseline, and the same reason it halts. |
| `Makefile` | modify | lint-config | flag | Where the repository drives its gates through make targets, the Makefile *is* the gate definition — a target that quietly stops running a check lowers the bar without touching a component; recorded for review. |
| CI workflow files (`.github/workflows/*.yml`, `.github/workflows/*.yaml`) | modify | coverage-threshold | flag | A plugin project ships no coverage config, so which gates run and whether a failure blocks lives in the workflow — a change there can disable a gate without touching a line of the plugin; recorded for review. |

The caller emits this list as the oracle-tamper guard's JSON input. The two columns the guard needs beyond the table are the path globs and the watched-change set:

```json
[
  { "type": "test_delete",       "globs": ["**/tests/**/*-spec.sh", "**/tests/**/*-spec.bats"], "changes": ["D"],     "oracle_class": "test-delete",        "severity": "halt" },
  { "type": "lint_baseline",     "globs": ["**/lint-baseline.txt", "**/.shellcheck-baseline"],  "changes": ["A","M"], "oracle_class": "lint-baseline",      "severity": "halt" },
  { "type": "lint_config",       "globs": ["Makefile"],                                         "changes": ["M"],     "oracle_class": "lint-config",        "severity": "flag" },
  { "type": "coverage_threshold","globs": [".github/workflows/*.yml", ".github/workflows/*.yaml"], "changes": ["M"],  "oracle_class": "coverage-threshold", "severity": "flag" }
]
```

Two things about this list are worth stating, because they are what makes it worth declaring rather than assuming a plugin has no oracles.

**A plugin's tests are shell specs, and they are the only executable oracle it has.** There is no phpstan baseline, no coverage threshold, no golden directory. What there is, in a mature plugin repository, is a `tests/` directory of `*-spec.sh` files per plugin plus a shared one under `scripts/`, and a `Makefile` that CI drives. The `**/`-prefixed test glob is required for the same reason it is in the other recipes: the guard expands `**/` to an optional prefix, so an unprefixed `tests/**` would match a repository-root test tree and miss every per-plugin one.

**The paper-test is not an oracle and cannot be one.** The trace of a component's instructions is judgement applied at authoring time and leaves no file behind for a guard to watch. That is a real limit rather than an omission: for the part of a plugin that is prose, the protection against a weakened check is the review phase reading the diff, never the tamper guard. A project that declares no oracle files at all is an honest "no oracle configured" state — the guard reports it ran with nothing to watch, rather than reporting a pass it never checked.

## References

### External origins (referenced, not authored here)

| Source | Used for |
|---|---|
| `plugin-creation-tools:plugin-creation` | The component contracts and authoring rules — `SKILL.md` / command / agent / hook frontmatter, the description budget, the reserved-word and XML rules, the `disallowed-tools` vs `disallowedTools` casing split, hook events and handler types — the mechanics the authoring standards rest on |
| `/plugin-creation-tools:create`, `/plugin-creation-tools:add-component` | The scaffolding from canonical templates that starts each plugin and component correct; this recipe drives them, it does not reproduce them |
| `/plugin-creation-tools:validate` | The mid-build `--dry-run` structural sanity check (the blocking run belongs to the review phase) |
| `code-paper-test:paper-test`, `/code-paper-test:test-team` | The line-by-line instruction trace that is test-first for a plugin — catching logic errors, contract violations, and hallucinated tools before the gate |

### Plugin-side generic mechanism (ai-dev-assistant)

The stack-neutral implement phase this recipe binds Claude Code into — when the phase runs, the oracle/envelope it emits, and how the authored components hand off to review — is documented in the plugin itself, not duplicated here. The recipe supplies only the Claude-Code authoring standards and the paper-test-first discipline on top of that mechanism.
