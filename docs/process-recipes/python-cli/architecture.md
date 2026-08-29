---
# Routing block — an orchestrator reads to here and decides.
name: python_cli_design_architecture
capability: design
description: Use when a Python project (a library, or a tool whose interface is one or more console scripts) enters the design phase and must turn researched requirements into a library-first architecture with a thin CLI entrypoint — fixes the package/CLI boundary, names a programmatic entry point per capability, specifies the entrypoint contract (exit codes, stream split, machine-readable output), chooses extension seams as protocols rather than conditionals, records the dependency and typing posture, and emits a component map the implement and review phases conform to, before any code is written.
# Metadata — read only after a match.
label: Python CLI architecture
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
authors:
  - name: camoa
license: GPL-2.0-or-later
---

## Goal

Turn researched requirements into a **library-first architecture with a thin CLI entrypoint** before any code is written. The design decides where the package boundary sits, how each capability is reached programmatically, what the entrypoint contract is, where behaviour varies and through what seam, and what the dependency and typing postures are. It records a component map — the artifact the implement and review phases conform to.

The plugin owns the generic design phase. This recipe owns what the stack-neutral mechanism cannot know: the Python-specific decisions — the package layout, the console-script boundary, the entry-point contract, protocol seams, and the postures on dependencies and typing.

## Opinion

**The CLI is a thin shell over a library, always.** Argument parsing and wiring in the console script; every piece of logic in an importable module. The test suite calls the library, not the binary, and a second consumer — a web handler, another tool, a notebook — reaches the same capability without shelling out.

**A `src/` layout, and a `pyproject.toml`.** The `src/` layout stops the tests from importing the working directory instead of the installed package, which is the single most common way a Python test suite passes against code nobody ships. `pyproject.toml` is where the project is declared; `setup.py` is legacy.

**Console scripts are declared, not scripted.** `[project.scripts]` in `pyproject.toml`, pointing at a function. A shell wrapper, a `__main__` that does work, or a script outside the package are all ways of putting logic where the tests cannot reach it.

**Extension seams are `typing.Protocol`, not base classes or conditionals.** A protocol states what a collaborator must provide without forcing an inheritance relationship, which is what makes a second implementation — including a fake in a test — cheap. A seam invented with no second implementation in view is speculative and is not added.

**The dependency posture is a decision with a number.** State whether the tool ships zero runtime dependencies or takes named ones, and record the transitive count the research phase measured. Where the posture is zero and a capability tempts a dependency, record the call — vendor a narrow slice, reimplement, or accept it with justification.

**The typing posture is part of the architecture.** Decide whether the package is fully typed and ships `py.typed`, and whether the type checker runs in strict mode. Deciding it here is what lets the review phase gate on it; deciding it later means retrofitting annotations across a codebase.

**Data structures before behaviour.** Where the design carries records, `dataclasses` or `TypedDict` at the boundary rather than dictionaries with implied keys. A dictionary whose shape lives only in the code that reads it is a contract nothing can check.

## Preconditions

- The research phase has run, and its reuse / extend / build verdicts are available.
- The target Python versions are decided, or this design decides them and records why.
- No code has been written for the capabilities being designed.

## Input contract

```yaml
requirements: string          # the capabilities the design must deliver
research: string              # optional; path to the research artifact, so an extend
                              # verdict reuses the found package rather than re-implementing
code_path: string             # optional; absolute path to the project root, when one exists
target_pythons: [string]      # optional; e.g. ["3.11", "3.12", "3.13"]
```

## Sequence

If invoked in dry-run mode, perform all reads but emit a component-map preview instead of recording anything. Dry-run is required.

1. **Fix the package boundary.** Draw the line between the importable package that holds all logic and the console script that only parses arguments and wires collaborators. List the package modules first — the script depends on them. Confirm no unit of logic is left inside the script, and that the layout is `src/<package>/`.

2. **Name the programmatic entry point per capability.** For each capability in the requirements, name the public function or class-and-method the console script calls. This is what the tests exercise and what a second consumer imports. A capability with no named entry point is not yet designed.

3. **Specify the entrypoint contract.** For each console script: the exit-code semantics (`0` for success, a distinct non-zero code per distinct failure class, each named), the stream split (data to stdout, diagnostics and progress to stderr), and a machine-readable output mode alongside the human one. Record these in the design, not as an implementation detail.

4. **Choose the extension seams.** For each point where behaviour is meant to vary, name the `Protocol` and its implementations rather than a conditional at the call site. Record each seam: the protocol, what varies across it, and the implementations the requirements call for.

5. **Record the dependency and typing postures.** State the runtime dependencies with the transitive count behind them, or state zero and what that costs. State whether the package is fully typed, ships `py.typed`, and whether the type checker runs strict. Both are decisions the implement and review phases enforce.

6. **Decide the data shapes at the boundaries.** For each capability's input and output, name the type — a dataclass, a `TypedDict`, a named tuple — rather than an untyped dictionary. Boundaries the tool serialises across get their shape written down here.

7. **Assemble the component map.** In dependency order: the package modules with their entry points and protocols, then the console script with its argument surface and the entry points it calls, then the wiring and the entrypoint contract it honours. Include the postures and the build order — modules → script → wiring → tests. Hand the map to the caller; the plugin's design phase records it. The recipe writes no file of its own.

## Data flow

```
input:  requirements, research (optional), code_path (optional), target_pythons (optional)
step 1: package boundary — module list, src/ layout, script reduced to parse-and-wire
step 2: one named programmatic entry point per capability
step 3: entrypoint contract — exit codes, stream split, machine-readable mode
step 4: seams — protocol per varying point, with its implementations
step 5: dependency posture (with transitive count) and typing posture
step 6: boundary data shapes, named types rather than bare dicts
step 7: component map in dependency order, with the build order
output: component map, returned to the caller. The recipe writes no file of its own.
```

## State-awareness contract

The recipe reads the requirements, the research artifact, and the project when one exists. It writes no Python, adds no console script, edits no `pyproject.toml`, and installs nothing. A design phase that creates the package it just designed has removed the gate between design and implementation.

## Verifier

After the recipe runs, verify:

1. No unit of logic sits in a console script — every capability's logic is in the importable package, and each script is designed as argument parsing and wiring only.
2. Every capability has a named programmatic entry point that the script calls and the tests can import; no capability exists only as a code path inside a script.
3. The entrypoint contract is written down: exit-code semantics with a distinct code per failure class, the stdout/stderr split, and a machine-readable output mode.
4. Each extension point is a named `Protocol` with its implementations, not a conditional; no seam was added without a concrete second implementation in view.
5. The dependency posture is recorded with the transitive count behind it, and the typing posture states whether the package is fully typed, ships `py.typed`, and runs the checker strict.
6. Boundary data has named types rather than untyped dictionaries.
7. The design left the project unchanged — no Python written, no script added, no `pyproject.toml` edit, nothing installed.

This recipe ships no executable verifier of its own — the checks above are the agent-driven protocol; the plugin's design phase owns the architecture artifact and the checklist gate that blocks the implement phase.

## References

### External origins (referenced, not authored here)

| Source | Used for |
|---|---|
| PEP 621 | The `pyproject.toml` project metadata the design's postures are recorded in, and the `[project.scripts]` table that makes a console script a declaration rather than a shell wrapper |
| PEP 544 | `typing.Protocol` and structural subtyping — the basis for choosing a named seam over a base class or a conditional at the call site |
| PEP 561 | `py.typed` and what shipping type information commits the package to, which is why the typing posture is decided here rather than retrofitted |
| The research artifact from the prior-art phase | The reuse / extend / build verdicts the design builds on, so an extend verdict adopts the found package rather than re-implementing it |

### Plugin-side generic mechanism (ai-dev-assistant)

The stack-neutral design phase this recipe binds Python into — when the design runs, the architecture artifact it records, and the checklist gate that blocks the implement phase — is documented in the plugin itself, not duplicated here. The recipe supplies only the Python-specific decisions: the package and console-script boundary, the named programmatic entry point per capability, the entrypoint contract, protocol seams, and the dependency and typing postures.
