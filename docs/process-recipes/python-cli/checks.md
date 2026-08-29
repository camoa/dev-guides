---
# Routing block — an orchestrator reads to here and decides.
name: python_cli_review_checks
capability: review
description: Use when a Python change reaches the review phase and must pass its gates before a pull request is accepted — runs the toolchain gates in a named blocking order (formatter clean, linter clean, type checker clean, tests passing, dependency audit clean) alongside the conformance checks a linter cannot make (logic in a console script, a swallowed exception, an undeclared dependency, import-time work, a shell-injection or path-traversal sink, a test that shells out instead of importing), and returns a pass / block verdict with the specific violations behind it.
# Metadata — read only after a match.
label: Python review checks
recipe_schema_version: 1.0.0
version: 0.1.0
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

Decide whether a change may be offered as a pull request, and when it may not, say exactly which check failed and where. The review runs the toolchain gates in a blocking order and then makes the judgements a tool cannot, returning a pass or block verdict with the violations behind it.

The plugin owns the generic review phase — when it runs, the verdict artifact, and that a block stops the pull request. This recipe owns the Python-specific part: which gates run, in what order, and what a linter structurally cannot check.

## Opinion

**The gates run in a blocking order and the first failure stops the rest.** A change that does not format cannot usefully be type-checked; a change that does not import cannot usefully be tested. Running everything and reporting a wall of failures hides which one is the cause.

**A clean tool run is not a review.** Every rule below the toolchain exists because no linter expresses it: whether logic crept into a console script, whether a dependency was added that the design did not decide, whether an exception is caught and dropped.

**A swallowed exception is a blocking finding, not a style note.** `except Exception: pass`, or a catch that logs and continues where the caller needed the failure, is how a tool reports success having done nothing.

**Shell and path sinks are read directly.** `subprocess` with `shell=True` and any interpolated value is an injection. A path built from external input and opened without being resolved and checked against its intended root is a traversal. Both are read in the diff, not inferred from a tool's silence.

**A dependency the design did not decide blocks.** Not because the package is bad, but because the posture was a decision and this is where it is enforced.

**`# noqa` and `# type: ignore` need a reason.** An unexplained suppression is a check deleted. With a reason it is a decision; without one it is an unreviewed exemption.

**The project's `pyproject.toml` names the gates; where it names none, this recipe does.** Python has no `gofmt` — no single formatter and linter that ships with the interpreter and settles the question — and the tools that fill the gap have genuinely turned over: Black and Flake8 were the answer for years and are now largely served by Ruff's `ruff format` and `ruff check`, and the type checker is an open field rather than a default: mypy and pyright have both been production tools for years, Meta's pyrefly reached a stable 1.0 and is the default checker on Instagram's codebase, and Astral's ty is still beta on `0.0.x` with no stable API. So a review that hard-codes a toolchain will, on a real project, run tools the project deliberately did not choose and report a wall of findings the project already decided against. Deferring to `[tool.*]` in `pyproject.toml` is the correct default, and it is a position, not an omission.

**That deferral has one limit, and this is where it is closed.** A project with no declared toolchain gets nothing from a rule that says "run what the project declares" — the gates would resolve to no commands and the review would pass on silence. So where `pyproject.toml` declares no formatter, linter or type checker, run this floor and record that it was the recipe's choice rather than the project's: `ruff format --check` for formatting (it exits non-zero on a file that would be reformatted and writes nothing, which is what a review needs), `ruff check` for linting, `mypy` for typing at the strictness the design recorded, and `pytest` for tests. Ruff earns the floor by being one binary configured from one `pyproject.toml` section for both jobs; mypy earns it by being maintained in the `python` organisation and configured from `[tool.mypy]`, where `strict` is a single switch — not by being the fastest, which it is not. A project that has chosen otherwise overrides all of this, and a project that has chosen pyright or pyrefly has chosen well; the floor exists for the project that has chosen nothing.

**The dependency audit is `pip-audit`, and that one is named outright.** No churn argument applies to it: it is maintained in the `pypa` organisation, it reads the Python Packaging Advisory Database through the PyPI JSON API, and it audits an environment, a requirements file, or a project directory directly. There is no equivalent second option whose existence would make naming it presumptuous, so it is named rather than deferred.

**`.py` is not in the change-scoping floor, which is why this recipe declares it.** The review command scopes its change-scoped gates by file extension, unioning the framework's declared extensions onto a framework-neutral floor of `.php` `.js` `.mjs` `.cjs` `.ts` `.tsx` `.vue`. No Python extension is in that floor, so without the `## Code-quality extensions` declaration below, **a pure-Python change would filter down to an empty file list and every change-scoped gate would skip itself** — a run that looks clean because it examined nothing.

**This framework declares no change-impact globs, and the absence is deliberate.** Change-impact globs route a changed file to the **e2e** and **visual-regression** gates. A Python CLI binds neither phase — it has no rendered or browser surface those harnesses target — so declaring globs here would route to gates that cannot fire. A CLI's end-to-end shape is a test tier, not a phase: it lives in the implement recipe as the entry-point tier and is checked here under the test gate.

## Preconditions

- The change is complete and committed or stageable, so the diff scope is knowable.
- The project's toolchain is installable, and its configuration lives in `pyproject.toml`.
- The architecture artifact is available when the change had a design phase.

## Input contract

```yaml
code_path: string             # absolute path to the project root (the dir with pyproject.toml)
changed: [string]             # optional; the changed files or diff scope to review;
                              # when absent, derived from version control
architecture: string          # optional; path to the component map the change should conform to
new_code_only: boolean        # optional; default true. Scope the conformance checks to the
                              # change rather than to the whole project's history.
```

## Sequence

If invoked in dry-run mode, report the gates and the commands it would run, and change nothing. Dry-run is required.

Steps 1 to 3 run the tool the project declares in `pyproject.toml`. Where it declares none, run the floor named in Opinion and record in the verdict that the tool was the recipe's choice, so a reader can tell an enforced project standard from a substituted default.

1. **Formatter, over the diff scope, in a mode that does not write.** It must list nothing. A formatting difference is a block, because everything after it reads against a moving target. Where the project declares no formatter, `ruff format --check`: it exits non-zero on any file it would reformat and leaves the working tree alone, which is the only shape a review may use.

2. **Linter, over the diff scope.** It must report nothing. Where a rule is suppressed, the suppression carries a reason; an unexplained `# noqa` is itself a finding. Where the project declares no linter, `ruff check` — and without a fix flag, because a review that repairs what it found has destroyed the evidence.

3. **Type checker, at the strictness the design recorded.** It must report nothing over the changed scope. A new `# type: ignore` without a reason is a finding. Where the project declares no type checker, `mypy` with the design's strictness — which in `[tool.mypy]` is the `strict` switch when the design recorded strict.

4. **Tests.** They must pass. Where the project declares multiple target Python versions, the review records which one this run used and whether the others were checked.

5. **Dependency audit.** Run `pip-audit` over the project's resolved dependencies and report known advisories that are reachable from this change. An advisory in an unreachable transitive path is recorded, not blocked on. Unlike the gates above, this one is not deferred to the project's declaration: it is named because it has no live alternative to defer between.

6. **Conformance reads over the diff.** Each is a read, not a tool: logic added to a console script; a dependency added the design did not decide; an exception caught and dropped; work moved to import time; `shell=True` with an interpolated value; a path from external input opened without being resolved against its root; a test that shells out where it should import; a public signature left unannotated against the recorded posture.

7. **Return the verdict.** Pass, or block with the specific violations — file, line, and which check. A block names what to change; a verdict that says "issues found" is not a review.

## Data flow

```
input:  code_path, changed (or VC-derived), architecture (optional), new_code_only (optional)
step 1: formatter result over the diff scope — clean or the files it would change
step 2: linter result, plus any suppression lacking a reason
step 3: type checker result at the recorded strictness, plus unexplained ignores
step 4: test result, and which Python version ran
step 5: dependency advisories, split into reachable and not
step 6: conformance findings, one per rule, each with file and line
step 7: pass, or block with the violation list
output: verdict and findings, returned to the caller. The plugin's review phase records it.
```

## Code-quality extensions

```
code_quality_extensions: [".py", ".pyi", ".toml"]
```

Without this declaration a pure-Python change filters to an empty list against the framework-neutral floor (`.php` `.js` `.mjs` `.cjs` `.ts` `.tsx` `.vue`) and every change-scoped gate skips itself — a clean-looking run that examined nothing.

`.pyi` is in because a stub file *is* the declared public typing surface under PEP 561: an edit to one changes the contract the type-checker gate reads, and it is code in every sense the gates care about even though no runtime executes it.

`.toml` is the judgement call, and it goes in for the same reason Go declares `.mod`. `pyproject.toml` is where the dependency posture, the target versions and the tool configuration are decided, and a change that touches only it — adding a dependency the design did not decide, which is a blocking finding above — would otherwise scope to an empty list and be judged by nothing. The honest cost is that this filter matches **extensions, not paths**, so it cannot scope in the manifest while scoping out a generated lockfile the way Go excludes `.sum`: a PEP 751 `pylock` file is also `.toml` and will be pulled in. Treat a lockfile diff as evidence of the dependency decision, not as code to judge on its own terms — and note that the same limitation cuts the other way for suppressions, which is the subject of the next paragraph.

`# noqa` and `# type: ignore` are the checks most worth watching and are reachable by no extension declaration at all, because they are inline comments rather than files. The unexplained-suppression rule in the Sequence is a read of the diff by the reviewer for exactly that reason; no value this block could hold would reach it.

## State-awareness contract

The recipe reads the project and runs its declared tools. It changes no file, fixes nothing it finds, and installs nothing beyond what the project already declares. A review that repairs what it is reviewing has removed the thing it was meant to report.

## Verifier

After the recipe runs, verify:

1. The gates ran in the stated order, and the first failure stopped the rest rather than being buried in a combined report.
2. The formatter, linter and type checker each reported nothing over the diff scope, or the verdict is a block naming what they reported. Each records which tool ran and whether it came from the project's `pyproject.toml` or from this recipe's floor, and the formatter ran in a mode that writes nothing.
3. Tests passed, and the verdict records which Python version ran and whether the other declared targets were checked.
4. The dependency audit ran, and any advisory is recorded as reachable or not.
5. Every conformance rule was read against the diff, and each finding carries a file and line.
6. Every suppression introduced by the change carries a reason.
7. The verdict is pass or block; a block lists the specific violations rather than a summary.
8. The project is unchanged by the review.

This recipe ships no executable verifier of its own — the checks above are the agent-driven protocol; the plugin's review phase owns the verdict artifact and the block that stops the pull request.

## References

### External origins (referenced, not authored here)

| Source | Used for |
|---|---|
| The project's `pyproject.toml` | The authority on which formatter, linter and type checker run and at what strictness — the declaration steps 1 to 3 defer to before the floor applies |
| Ruff (`ruff format --check`, `ruff check`) | The formatting and linting floor for a project that declares neither — one binary for both jobs, and the `--check` behaviour (non-zero exit on a file it would reformat, nothing written) that makes it usable inside a read-only review |
| mypy (`[tool.mypy]`, the `strict` switch) | The typing floor for a project that declares no checker, and the single config switch the design's strict posture maps onto |
| pyright, pyrefly, and ty | The alternatives that make the type checker an open field rather than a default, and the reason the gate defers to the project's declaration — pyrefly stable at 1.0 and Meta's default checker, ty still beta on `0.0.x` with no stable API |
| pip-audit (maintained in the `pypa` organisation) | The dependency audit — named rather than deferred; it reads the Python Packaging Advisory Database through the PyPI JSON API |
| PEP 561 | What a declared typing posture and a shipped `py.typed` marker commit the package to at review time, and why a `.pyi` stub is part of the reviewable surface |
| The component map from the design phase | The recorded decision the conformance reads in step 6 measure against, rather than reconstructing an intent from the code |

### Plugin-side generic mechanism (ai-dev-assistant)

The stack-neutral review phase this recipe binds Python into — when the checks run, the verdict artifact they emit, how the `## Code-quality extensions` declaration above is consumed for change-scoping, and what a block does to the pull request — is documented in the plugin itself, not duplicated here. The recipe supplies only the Python-specific gate set, the blocking order, and the conformance reads a linter cannot express.

Note that, unlike the PHP CLI recipe under this root, this one does not defer linter execution to the `code-quality-tools` plugin: that plugin detects Drupal and Next.js projects and lints PHP and JavaScript file extensions, and has no Python arm. The commands above are therefore named directly.
