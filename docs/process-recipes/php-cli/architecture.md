---
# Routing block — an orchestrator reads to here and decides.
name: php_cli_design_architecture
capability: design
description: Use when a PHP CLI project (a Composer library or application whose interface is one or more CLI binaries) enters the design phase and must turn researched requirements into a library-first architecture with a thin CLI entrypoint — fixes the library/CLI boundary, defines a programmatic entry point for every capability, specifies the entrypoint contract (exit codes, stream split, machine-readable output), chooses extension seams, records the dependency posture, and emits a component map the implement and review phases conform to, before any code is written.
# Metadata — read only after a match.
label: PHP CLI architecture
recipe_schema_version: 1.0.0
version: 0.1.0
# Process-recipe routing keys, enforced by validate_recipes.py for any recipe
# under docs/process-recipes/. `capability` above doubles as the phase (the
# lifecycle moment the orchestrator resolves on); there is no separate
# applies_to_phase. `framework` is the second routing dimension.
recipe_class: process
framework: php-cli
assumes:
  - composer
authors:
  - name: camoa
license: GPL-2.0-or-later
---

## Goal

Turn researched requirements into a **library-first architecture with a thin CLI entrypoint** before any code is written. The design decides, for the capability set the tool must deliver, **where the library boundary sits** (all logic in the library, the binary reduced to arg-parsing and wiring), **how every capability is reached programmatically** (a public library API the binary calls, so the CLI is never the only path), **what the entrypoint contract is** (exit-code semantics, the stdout/stderr split, a machine-readable output format alongside the human one), **how the code varies at its extension points** (interfaces and seams, not conditionals), and **what the dependency posture is** (a stated decision, recorded with its reasoning). It records a component map — the architecture artifact the implement and review phases conform to.

The plugin owns the generic design phase — when it runs, the shape of the architecture artifact, and the checklist gate that blocks the implement phase. This recipe owns the part the stack-neutral mechanism cannot know: the PHP-CLI-specific decisions — the library/CLI boundary, the programmatic entry point per capability, the entrypoint contract, the extension seams, and the dependency posture.

## Opinion

**The library is the unit of architecture; the binary is arg-parsing and wiring only.** All logic lives in the library layer (`src/`), so the CLI is one consumer among several — the test suite, another tool, a second binary, a long-running process could each reach the same behaviour without going through argument parsing. A binary that carries logic is a design defect, not a style choice: it strands that behaviour behind a command line where nothing else can call it, and the design is incomplete until the logic is moved into the library and the binary is left thin.

**Every capability the CLI exposes has a programmatic entry point.** For each thing the tool can do, the design names a public library API — a class and method the binary invokes — so the binary is never the only way to reach the behaviour. This is what makes the tool testable without spawning a process, embeddable in another package, and drivable from a second entrypoint. A capability that exists only as a code path inside the binary has no entry point and is flagged for extraction before implement.

**The entrypoint contract is specified explicitly, not left to convention.** The design writes down three things per binary: **exit-code semantics** — `0` for success, distinct non-zero codes for distinct failure classes, so a caller can branch on *why* it failed and not just *that* it did; the **stream split** — data on stdout, diagnostics and progress on stderr, so the tool composes in a pipeline without the human-facing chatter corrupting the data; and a **machine-readable output format** — a `--format=json` mode (or equivalent) alongside the human-readable one, so downstream tools parse structure instead of scraping prose. An entrypoint whose contract is implicit is an entrypoint that breaks its consumers silently the first time a message changes.

**Prefer interfaces and seams over conditionals at extension points.** Where the tool's behaviour is meant to vary — a pluggable formatter, a swappable source, a strategy that differs per input — the design puts an interface with named implementations at that point, not a growing `switch` or a chain of `if` branches. A seam is discoverable, testable in isolation, and extendable without editing the call site; a conditional is none of those. The extension points are decided here, in the architecture, not discovered later under a refactor.

**The dependency posture is a stated decision, not an accident.** Whether the tool ships with zero runtime dependencies, or takes a specific one, is written down with the reasoning — the prior-art research surfaced what exists, and the design records the call it drove. A zero-dependency stance is recorded as a deliberate constraint (with the vendor-a-slice or reimplement-a-narrow-piece consequences it implies); a chosen dependency is recorded with why it earned its place against that bar. Either way the posture is legible to the implement and review phases, which enforce it, rather than emerging silently from whatever the first `composer require` happened to pull in.

**Design decides; it does not build.** This phase produces an architecture decision for a human to approve — the library API, the thin binary, the entrypoint contract, the extension seams, the dependency posture, and the build order. It writes no PHP, adds no binary to `bin/`, edits no `composer.json`, and installs nothing. Recording the decision into the architecture artifact is the plugin's design phase; building from it is the implement phase.

## Preconditions

- A PHP project, Composer-managed, whose PHP version constraint is resolvable (so pattern and language-feature availability can be judged against it).
- The research phase has produced requirements and any prior-art findings (see the prior-art recipe under this framework) — the design starts from a known problem and a known reuse / extend / build-new posture, and honours a stated dependency stance rather than re-deriving one.
- The plugin's generic design phase is present: the architecture artifact and the checklist that gates the implement phase. This recipe supplies the PHP-CLI-specific design method; it does not recreate the artifact or the gate.

## Input contract

Source-agnostic, supplied by the caller (the orchestrator at the design phase, or a human operator).

```yaml
code_path: string             # absolute path to the PHP project root
requirements: string          # the researched capability/problem to architect
research:                     # optional; the research phase's reuse/extend/build call
  recommendation: string      #   and the dependency posture it surfaced, so the design
                              #   builds on the prior-art decision rather than re-deriving it
components:                   # optional; pre-identified units to design for
  - string                    #   e.g. "the scan capability", "the report formatter"
php_version: string           # optional; the target PHP constraint;
                              #   if absent, derived from the project's composer.json
```

## Sequence

If invoked in dry-run mode, perform all reads but emit a component-map preview instead of recording anything. Dry-run is required.

1. **Fix the library boundary.** From `requirements` (and `research`, so an extend recommendation reuses the found package rather than re-implementing it), draw the line between the library layer that holds all logic and the binary that only parses arguments and wires collaborators. List the library units first — everything the binary calls depends on them. Confirm no unit of logic is left living inside a binary.

2. **Define the programmatic entry point per capability.** For each capability in the requirements, name the public library API — the class and method — that delivers it, the one the binary invokes. This is the contract the test suite and any second consumer reach through. A capability with no named entry point is not yet designed; give it one before moving on.

3. **Specify the entrypoint contract.** For each binary, write down the exit-code semantics (`0` for success; a distinct non-zero code per distinct failure class, each named), the stream split (data to stdout, diagnostics and progress to stderr), and the machine-readable output format (a `--format=json` mode or equivalent) that sits alongside the human-readable one. Record these as part of the design, not as an implementation detail to settle later.

4. **Choose the extension seams.** For each point where behaviour is meant to vary, decide the interface and its named implementations rather than a conditional at the call site. Record each seam: the interface, what varies across it, and the implementations the requirements call for. Points that do not vary get no seam — a seam invented without a second implementation in sight is speculative and is not added here.

5. **Decide and record the dependency posture.** State whether the tool ships zero runtime dependencies or takes a specific one, with the reasoning the prior-art research drove. Where the posture is zero-dependency and a capability tempts a dependency, record the honest call — vendor a narrow slice, reimplement a small piece, or accept the dependency with justification — so the implement and review phases enforce a decision, not a vacuum.

6. **Assemble the component map.** Produce the map in dependency order: the library API first (units, their public entry points, their extension seams), then the thin binary (its argument surface and the entry points it calls), then the wiring (how the binary composes the library, and the entrypoint contract it honours). Include the dependency posture and the build order — library units → binary → wiring → tests. Hand the map to the caller; the plugin's design phase records it into the architecture artifact and runs the checklist gate. The recipe method writes no file of its own.

## Data flow

```
input: code_path, requirements, research (optional), components (optional),
       php_version (optional)

reads project state:
       composer.json (PHP constraint, existing bin array, autoload roots)
       existing architecture artifact
       existing library layer + entrypoints (src/, bin/), *.php sources
       the research recommendation + dependency posture (reuse | extend | build-new)

applies opinion:
       the library is the unit of architecture · the binary is arg-parsing +
       wiring only · a programmatic entry point per capability · the entrypoint
       contract is explicit (exit codes / stream split / machine-readable format) ·
       seams over conditionals at extension points · the dependency posture is a
       stated decision · design decides, never builds

emits (to the caller; the recipe method writes nothing):
       library_api:    units (first) — each with its public entry point + seams
       binary:         the thin entrypoint — argument surface + entry points called
       contract:       exit-code semantics · stdout/stderr split · machine-readable format
       dependencies:   the recorded posture (zero-dep | chosen dep) with reasoning
       order:          library units → binary → wiring → tests
```

## State-awareness contract

The recipe reads existing state before deciding. The project's `composer.json` (PHP constraint, the existing `bin` array, the autoload roots), any existing architecture artifact, and the current library-and-entrypoint layout are read so the design extends what is present rather than colliding with it — and so an extend recommendation and a stated dependency posture from prior art are honoured instead of re-derived. The method is read-only on the project: it writes no PHP, adds no binary, edits no `composer.json`, and installs nothing; the component map is returned to the caller, which owns recording it as the architecture artifact the downstream phases consume.

Idempotent: running the recipe twice on identical input and identical project state produces the same component map, with no side effect on either run. A map that changes because the requirements, the research recommendation, or the existing layout changed is the method reflecting current reality, not a non-deterministic recipe.

## Verifier

After the recipe runs, verify:

1. No unit of business logic sits in a binary — every capability's logic lives in the library layer, and each binary is designed as arg-parsing and wiring only.
2. Every capability the CLI exposes has a named programmatic entry point (a public library class and method the binary calls); no capability exists only as a code path inside a binary.
3. The entrypoint contract is written down: exit-code semantics (`0` for success, a distinct non-zero code per distinct failure class), the stdout/stderr split (data vs diagnostics), and a machine-readable output format alongside the human one.
4. Each extension point is a named interface with its implementations, not a conditional at the call site; no seam was invented without a concrete second implementation in view.
5. The dependency posture is recorded with its reasoning — a zero-dependency stance as a deliberate constraint (with its vendor-or-reimplement consequences), or a chosen dependency justified against that bar.
6. The design left the project unchanged — no PHP written, no binary added, no `composer.json` edit, nothing installed; the component map was returned for the plugin's design phase to record as the artifact the implement and review phases conform to.

This recipe ships no executable verifier of its own — the checks above are the agent-driven protocol; the plugin's design phase owns the architecture artifact and the checklist gate that blocks the implement phase on a failed item.

## References

### External origins (referenced, not authored here)

| Source | Used for |
|---|---|
| Composer (getcomposer.org) | The project's PHP constraint, the `bin` array, and the autoload roots the library/binary boundary is designed against — the packaging facts the component map conforms to |
| Symfony Console, the PSR standards | The established command-structure component and the interface conventions the design *may* adopt as prior-art candidates — weighed where the research surfaced them, never assumed as a design default |

### Plugin-side generic mechanism (ai-dev-assistant)

The stack-neutral design phase this recipe binds PHP CLI into — when design runs, the shape of the architecture artifact, the checklist gate that blocks the implement phase, and how the decision is recorded and reviewed — is documented in the plugin itself, not duplicated here. The recipe supplies only the PHP-CLI-specific design method: the library/CLI boundary, the programmatic entry point per capability, the entrypoint contract, the extension seams, and the dependency posture.
