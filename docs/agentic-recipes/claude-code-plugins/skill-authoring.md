---
# Routing block — an orchestrator reads to here and decides.
name: claude_code_skill_authoring
capability: claude-code-skill-authoring
description: Use when a Claude Code plugin needs a skill written or changed — the SKILL.md frontmatter, a description that makes the skill fire on the right requests and not on others, a body that discloses its depth through references/ and scripts/, and an eval suite that proves it fires and does its job, run by `claude plugin eval` with graders that call no judge.
# Metadata — read only after a match.
label: Claude Code skill authoring
recipe_schema_version: 1.0.0
version: 0.1.0
assumes:
  - claude-code
authors:
  - name: camoa
license: GPL-2.0-or-later
---

## Goal

Deliver one skill inside a plugin that fires on the requests it names, stays quiet on the requests it does not, and does what its body says once it fires. The proof is an eval suite beside the plugin, run by `claude plugin eval`. The recipe owns the order of the work, the shape of the description and the eval, and the verify line. Each component's authoring contract belongs to `process-recipes/claude-code-plugins/authoring-standards`, and this recipe does not restate it.

## Opinion

**The description is the trigger, so it is tested like code.** Claude decides to load a skill from its name and description alone. A description that reads well and never fires is a defect nobody sees until a user asks. So each request that must fire the skill gets an eval case, and so does at least one request that must not.

**Write the eval before the skill.** A case written first fails for the right reason: the skill is absent, so `Skill` is never called. A case written after the skill tends to grade what the skill already does. Watch each case fail once before the skill exists.

**Grade with graders that call no judge.** `regex`, `tool_used`, `tool_order` and `file_exists` read the transcript and the files, cost nothing, and give the same verdict on the same run. `llm` and `baseline` call a judge model, whose vote can change between runs. The cases the verify line runs use the first four only. A judge grader may live in another case, which a person runs; it never sits in a case the verifier names.

**Each case gets two graders: one on the steps, one on the result.** A `tool_used` grader with `tool: Skill` and an `input_match` naming the skill proves the skill fired. A `regex` or `file_exists` grader proves the result. A case that must not fire uses `tool_used` with `min: 0` and `max: 0`.

**One run is a gate, not a measurement.** The verify line runs each case once, with no baseline arm, because it answers one question: does the skill fire and finish on this commit. Whether the skill helps compared with no skill at all is the three-run, two-arm suite, `--ablation with-without`. A person runs that, and its delta never changes the exit code.

**Disclose depth progressively.** `SKILL.md` holds the steps Claude follows, in the imperative, under 500 lines. Detail Claude reads only on some paths goes in `references/`, and `SKILL.md` names each file and says when to read it. Code Claude runs rather than reads goes in `scripts/`, called through `${CLAUDE_SKILL_DIR}`. A file that `SKILL.md` never names is never read.

**Write frontmatter to the strictest surface the skill will reach.** Claude Code needs neither field. It takes `name` from the directory and truncates `description` plus `when_to_use` at 1,536 characters. The Agent Skills specification is stricter: `name` of at most 64 lowercase letters, digits and hyphens, without `anthropic` or `claude`, and a `description` of at most 1,024 characters with no XML tags. A plugin skill written to the stricter rule loads everywhere.

**`claude plugin eval` is this framework's harness for a skill.** `process-recipes/claude-code-plugins/test-execution` answers that no suite row runs the components. For a skill's triggering and its read-only result, `claude plugin eval`, from Claude Code 2.1.269, runs the skill against eval cases, but it calls a model per case, so this recipe runs it as its verifier and not as a suite row. The paper trace in `process-recipes/claude-code-plugins/authoring-standards` still runs; the eval does not replace reading the instructions.

## Preconditions

- Claude Code 2.1.269 or later on `PATH`, signed in with the credential the person's sessions use. Every eval run is a real model call on that account.
- Git 2.31 or later, when git is installed. An older git stops `claude plugin eval` before any case runs.
- The plugin exists, with `plugin.json` or `.claude-plugin/plugin.json` at `plugin_path`. Nothing here scaffolds a plugin; `/plugin-creation-tools:create` does.
- The design names the skill, its purpose, and the requests that must and must not fire it.

## Input contract

Generic, source-agnostic, supplied by the caller (adapter skill, human operator, or orchestrator).

```yaml
plugin_path: string            # the plugin root, relative to the project root;
                               # `.` when the repository is the plugin

skill:
  name: string                 # the skill directory's name, and its frontmatter `name`
  purpose: string              # what the skill does, in one sentence
  triggers:                    # requests that must fire the skill, one eval case each
    - string
  non_triggers:                # requests near the skill's purpose that must not fire it
    - string
  references:                  # optional; topics that belong in references/, one file each
    - string
  scripts:                     # optional; scripts the skill runs, under scripts/
    - string

eval_cases:                    # the case names under the plugin's eval directory that the
  - string                     # verify line runs; every one uses graders that call no judge
```

## Sequence

If invoked in dry-run mode, print the planned file tree, the description, and each eval case with its graders, and write nothing. Dry-run is required.

1. **Read the plugin.** List its existing skills, their names and descriptions, and its eval directory: `evals/` unless the manifest's `experimental.evals` names another. A new skill whose description overlaps a sibling's fires in its place, or not at all. Report each overlap before writing.

2. **Write the eval cases.** Under the eval directory, one case per entry of `skill.triggers` and at least one per entry of `skill.non_triggers`. Each case is a directory holding `prompt.md` and `graders/*.md`. The prompt is the request, as a user would type it. Its frontmatter sets `max_turns` and `allowed_tools`, and `allowed_tools` names `Skill` plus only what the skill's path needs from the read-only set. Grade each trigger case with a `tool_used` grader on `Skill`, whose `input_match` names the skill, and one `regex` or `file_exists` grader on the result. Grade each non-trigger case with a `tool_used` grader on `Skill` with `min: 0` and `max: 0`. Name the cases so a `--case` glob of the case name selects exactly one. The case names the verify line runs are `eval_cases`.

3. **Watch each trigger case fail.** Run the verify line's command once per case before the skill exists. Each trigger case must exit 1, with its `tool_used` grader failing. A trigger case that passes now tests nothing this skill adds: rewrite its prompt or its graders.

4. **Write the frontmatter.** `name` is `skill.name`. The `description` says what the skill does and when to use it, in the third person, with the key use case first and the words of `skill.triggers` in it. Keep it inside the stricter limits in the Opinion. Set `disable-model-invocation: true` only for a skill a person must start by hand, and then drop its trigger cases, because Claude cannot fire it.

5. **Write the body and its files.** `SKILL.md` holds the imperative steps. Each `skill.references` topic becomes one file under `references/`, named from `SKILL.md` with the condition to read it. Each `skill.scripts` entry goes under `scripts/` and is called as `${CLAUDE_SKILL_DIR}/scripts/<file>`. A script is ordinary code: its spec comes from `process-recipes/claude-code-plugins/test-authoring`.

6. **Trace the instructions.** Paper-test the body as `process-recipes/claude-code-plugins/authoring-standards` requires, and confirm every tool, file, flag and sibling skill it names exists.

7. **Run the eval and read the table.** Run the verify line's command for each case. Each must exit 0. A failing case names the grader that failed and why. Fix the description for a trigger failure, and the body for a result failure. Never weaken a grader to make a case pass.

8. **Report.** Name the skill's files, the description and its length, each case with its graders and its verdict, and the command run. Add a line saying the delta against no skill was not measured, unless a person ran the two-arm suite.

## Data flow

```
input:  plugin_path, skill{name, purpose, triggers[], non_triggers[],     supplied by the caller
        references[], scripts[]}, eval_cases[]

step 1: the plugin's skills and eval directory      → overlaps, as findings
step 2: skill.triggers[], skill.non_triggers[]      → <eval dir>/<case>/prompt.md, graders/*.md
step 3: claude plugin eval, per case                → a red per trigger case, before the skill
step 4: skill.name, skill.purpose, triggers[]       → SKILL.md frontmatter
step 5: skill.references[], skill.scripts[]         → SKILL.md body, references/*, scripts/*
step 6: the body                                    → a paper trace; every named thing exists
step 7: claude plugin eval, per case                → exit 0 per case, or the failing grader
step 8: everything above                            → report
```

## State-awareness contract

The recipe writes the skill's directory and its eval cases, and nothing else in the plugin. Re-running it over a skill that exists changes only what the input changes: a case that already exists and passes is left alone. It never edits a sibling skill's description to resolve an overlap; it reports the overlap. The eval runs write nothing into the tree. Each run works in an empty workspace of its own, and the verify line sends its results to a folder outside the tree.

## Verifier

Each entry is one command, run from the project root after the recipe ran. It is split on spaces and never run through a shell. A non-zero exit fails the entry, whatever `pass` says.

verifier:
  - id: skill-eval-passes
    kind: self-fixture
    run: claude plugin eval {plugin_path} --case {eval_cases} --runs 1 --ablation none --trust-plugin --no-publish --output-dir /tmp/aida-skill-eval
    pass: exit 0

What the entry does not prove, and where the proof is:

- The entry runs once per name in `eval_cases`. It exits 0 only when every grader of that case passed, because `--threshold` defaults to 1.0. It exits 1 when a grader fails, when no case matches the name, or when a case file fails to load. It exits 2 when the credential is rejected. Each of these fails the entry.
- `kind: self-fixture`, because each run builds an empty workspace, loads only this plugin, and discards the workspace after grading. The run also needs the model and the person's credential. Without them the entry fails, and that is a correct fail-close.
- `--trust-plugin` answers the first-run trust prompt, which cannot be asked without a terminal. Pass it only for a plugin the person would run on their own machine.
- The results go to `/tmp/aida-skill-eval`, outside the tree, so the run leaves the working tree clean. A later run replaces them.
- The run grants no tool past the read-only set, so a case whose result needs `Bash`, `Write` or `Edit` fails here. Grade such a skill on what it reads and replies, and prove its scripts through their own specs.
- One run of each case proves the skill fired and finished once. Whether it helps compared with no skill is the two-arm suite in the Opinion, which a person runs.
- The entry does not check the description's length or the body's line count. Sequence steps 4 and 5 carry those, and the review phase's structural validator checks the frontmatter.

## References

### Recipes cited

| Recipe | Used for |
|---|---|
| `process-recipes/claude-code-plugins/authoring-standards` | The frontmatter and body contract per component, and the paper trace |
| `process-recipes/claude-code-plugins/test-authoring` | Specs for the scripts a skill ships |
| `process-recipes/claude-code-plugins/test-execution` | That no suite row runs a plugin's instructions |
| `process-recipes/claude-code-plugins/architecture` | The component map that names the skill and its body/`references/` split |

### External sources

| Source | What it settles |
|---|---|
| Claude Code documentation, "Test plugins with evals", https://code.claude.com/docs/en/plugin-evals | Case layout, the six grader types and which call a judge, `--case`, `--runs`, `--ablation`, `--trust-plugin`, `--no-publish`, `--output-dir`, `--threshold` 1.0, the exit codes, the empty workspace per run, the read-only tool set, Claude Code 2.1.269 and git 2.31 as minimums |
| `claude plugin eval --help`, Claude Code 2.1.322 | The flags above, as the installed CLI prints them |
| Claude Code documentation, "Extend Claude with skills", https://code.claude.com/docs/en/skills | `name` and `description` optional in Claude Code, the 1,536-character listing cap, `SKILL.md` under 500 lines, supporting files and `${CLAUDE_SKILL_DIR}`, `disable-model-invocation` |
| Claude Platform documentation, "Agent Skills" overview, https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview | `name` at most 64 lowercase letters, digits and hyphens without `anthropic` or `claude`; `description` at most 1,024 characters; no XML tags in either |
