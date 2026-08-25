---
# Routing block — an orchestrator reads to here and decides.
name: go_design_architecture
capability: design
description: Use when a Go project enters the design phase and must turn researched requirements into a package layout with a compiler-enforced boundary — fixes what lives under internal/ versus the exported surface, holds cmd/ to argument parsing, exit codes and stream wiring only, settles the module path and its compatibility promise, places interfaces at the consumer rather than the producer, threads context through the call graph, decides the wrapped-error and exported-sentinel surface, and bans init() side effects, before any code is written.
# Metadata — read only after a match.
label: Go architecture
recipe_schema_version: 1.0.0
version: 0.1.0
# Process-recipe routing keys, enforced by validate_recipes.py for any recipe
# under docs/process-recipes/. `capability` above doubles as the phase (the
# lifecycle moment the orchestrator resolves on); there is no separate
# applies_to_phase. `framework` is the second routing dimension.
recipe_class: process
framework: go
assumes:
  - go-modules
authors:
  - name: camoa
license: GPL-2.0-or-later
---

## Goal

Turn researched requirements into a **package layout whose boundary the compiler enforces** before any code is written. The design decides **what is exported and what lives under `internal/`** (in Go this is a real boundary, not a naming convention), **what a `cmd/` binary is allowed to contain** (argument parsing, exit codes, stream wiring — and nothing else), **what the module path is and what promise it carries**, **where interfaces are declared** (at the consumer, not the producer), **how `context.Context` threads through the call graph**, **which errors are part of the exported API** and how the rest are wrapped, and **what may not happen at package initialisation**. It records a package map — the architecture artifact the implement and review phases conform to.

The plugin owns the generic design phase — when it runs, the shape of the architecture artifact, and the checklist gate that blocks the implement phase. This recipe owns the part the stack-neutral mechanism cannot know: the Go-specific decisions, most of which are load-bearing in Go precisely because the toolchain enforces them and a later change is a breaking one.

## Opinion

**`internal/` is the default home for a package; the exported surface is what you deliberately promote out of it.** The go command's rule is a compiler rule, not a convention: *code in or below a directory named "internal" is importable only by code that shares the same import path above the internal directory*. That makes it the one boundary in Go that an outside importer physically cannot cross — unlike an unexported identifier, which only guards a package, and unlike a docstring saying "don't use this", which guards nothing. The consequence for the design is a default: **new packages start under `internal/`, and a package is promoted to the exported surface only when an external importer needs it and the project is willing to support it under its compatibility promise.** Starting a package exported and hoping to tidy it later inverts the cost — the promotion is free, the demotion is a breaking change.

**A `cmd/` binary parses arguments, translates a result into an exit code, wires the streams, and stops.** The whole of `main` should be a shim: parse flags into a config value, call one function, translate its error into an exit status. Design that function explicitly — a `run(ctx context.Context, args []string, stdin io.Reader, stdout, stderr io.Writer) error` shaped entry point, living below `cmd/`, that takes its I/O as parameters rather than reaching for the process globals. This is not a testing trick that leaked into the architecture; it is the architecture. A `run` function can be called by a test with buffers, by a second binary, by another tool, or by a long-running process, and `main` becomes the only place that knows about `os.Args`, `os.Stdout`, and `os.Exit`. Logic that lands in `main` instead is stranded behind a process boundary where nothing else can reach it.

**`os.Exit` must be reachable from `main` and nowhere else, because it does not run deferred functions.** This is a design constraint, not a style note: a call to `os.Exit` deeper in the call graph silently skips every pending `defer` above it — the flush that was going to write the last of the output, the cleanup that was going to remove the temp directory, the unlock. So the exit-code contract is designed as *error values returned up to `main`*, which then maps them to codes. Write the mapping down as part of the design: `0` for success, and a distinct non-zero code per failure class a caller might branch on, each named. Alongside it, the stream split — machine-consumable output on stdout, diagnostics, progress, and errors on stderr — so the tool composes in a pipeline without its chatter corrupting the data.

**Do not add a `pkg/` directory.** It is the most-copied and least-justified item in the Go layout folklore, and it is worth being blunt about why: `internal/` is enforced by the compiler and `cmd/` is recognised by the module documentation and by every Go developer reading the tree, but `pkg/` is enforced by nothing and communicates nothing that the module path did not already say. The official module-layout guidance prescribes package directories at the module root, `internal/` for what should not be imported, and `cmd/` for commands — and does not include `pkg/` at all. Adding it buys one extra path segment in every import statement of every consumer. The one case where it is defensible is repository hygiene rather than API design — a repository whose root is already crowded with non-Go directories, where a single Go source root genuinely helps a reader — and even then it should be a recorded decision with that reason attached, not a reflex.

**Interfaces are declared by the consumer, not the producer — so this design does not draw a seam at every point of variation.** Go's convention is to accept interfaces and return structs: a package that produces a thing returns its concrete type, and each package that *consumes* it declares, locally, the narrowest interface it actually needs. This inverts the habit imported from languages where the producer publishes an interface and the consumers depend on it. The practical rules for the design: **no `interfaces.go` file** cataloguing the project's abstractions; **no exported single-implementation interface published "for testing"** by the package that implements it — the test declares what it needs; and **an interface with one method is normal and good**, because a narrow consumer-side interface is exactly the point. Where the requirements genuinely call for several interchangeable implementations chosen at runtime, name the interface, name the implementations, and name the package that *declares* it — which is the consumer's, unless the set of implementations is itself the exported API.

**`context.Context` is the first parameter of anything that blocks, and it is never a struct field.** Design the call graph so a context created in `main` — from `signal.NotifyContext`, so a Ctrl-C actually cancels work — threads down through every function that does I/O, waits, or spawns a goroutine, as an explicit first parameter named `ctx`. Storing a context in a struct hides its lifetime from the caller and makes a value that was scoped to one operation outlive it. Decide here, not later: which entry points take a context, where deadlines are set, and which long-running operations must observe cancellation. Retrofitting context into a call graph is a signature change to every function on the path, which is why it is a design decision rather than an implementation detail. Request-scoped *values* in a context are a narrow tool for data that genuinely crosses an API boundary the design cannot change; they are not a way to pass arguments.

**Errors are wrapped with `%w` on the way up, and the exported error surface is part of the API.** Every layer that adds context to an error wraps it — `fmt.Errorf("reading config %s: %w", path, err)` — so a caller can still match the cause with `errors.Is` or extract a typed error with `errors.As`. What the design has to decide, and record, is the **exported** part: which sentinel values (`var ErrNotFound = errors.New(…)`) and which error types the package publishes for callers to match on. That set is public API under the compatibility promise, and it is the only part of an error a caller may depend on — the message text is not. Decide it deliberately and keep it small; a package that exports no sentinels forces its callers to match on strings, and a package that exports twenty has made its internals into API.

**No `init()` side effects, and no package-level mutable state.** An `init` function that reads the environment, opens a file, dials a network, starts a goroutine, or registers itself into a global runs on *import*, in an order the design does not control, before any caller has had a chance to configure anything — and it runs even for an importer that wanted one unrelated symbol from the package. It is also unreachable from a test that wants to vary it. Construct dependencies explicitly in `main` and pass them down. The established exception is blank-import driver registration (the pattern behind SQL drivers and image format decoders); that is a pattern to *consume* where the standard library defines it, not one to author.

**The module path is decided once and carries a promise.** The module path is simultaneously the import path every consumer types, the identity the proxy and checksum database key on, and — through its major-version suffix — the compatibility contract. Changing it later breaks every importer. Record it now, along with the honest version posture: `v0` states that the API may break on any minor release, which is a legitimate and often correct choice for a young project; `v1` is a commitment not to break exported API, and `v2+` requires the major version in the path. The design records which of these the project is choosing and, if `v1` or later, what the exported surface it is committing to actually is — which is a direct consequence of the `internal/` default above.

**Design decides; it does not build.** This phase produces an architecture decision for a human to approve — the package map, the boundary, the entry-point contract, the interface placement, the context and error surfaces, and the build order. It writes no Go, creates no directory, edits no `go.mod`, and requires nothing. Recording the decision into the architecture artifact is the plugin's design phase; building from it is the implement phase.

## Preconditions

- A Go project with a `go.mod` at the module root (or a decided module path where the module does not yet exist), and a resolvable toolchain — so the language version constrains which features the design may assume.
- The research phase has produced requirements and any prior-art findings (see the prior-art recipe under this framework) — the design starts from a known problem and a known stdlib / copy-a-slice / reuse / extend / build-new posture, and honours it rather than re-deriving one.
- The plugin's generic design phase is present: the architecture artifact and the checklist that gates the implement phase. This recipe supplies the Go-specific design method; it does not recreate the artifact or the gate.

## Input contract

Source-agnostic, supplied by the caller (the orchestrator at the design phase, or a human operator).

```yaml
code_path: string             # absolute path to the Go module root (the dir with go.mod)
requirements: string          # the researched capability/problem to architect
research:                     # optional; the research phase's stdlib/copy/reuse/extend/
  recommendation: string      #   build call, so the design builds on the prior-art
                              #   decision rather than re-deriving it
components:                   # optional; pre-identified units to design for
  - string                    #   e.g. "the scan capability", "the report writer"
module_path: string           # optional; the module path; if absent, read from go.mod
go_version: string            # optional; the target language version;
                              #   if absent, read from the `go` line in go.mod
```

## Sequence

If invoked in dry-run mode, perform all reads but emit a package-map preview instead of recording anything. Dry-run is required.

1. **Settle the module path and the version posture.** Read the existing `module` line, or decide one. Record the posture — `v0` (no compatibility promise, breaking changes allowed on any minor), `v1` (committed not to break exported API), or `v2+` (major version carried in the path) — because everything downstream about what may be exported depends on which promise the project is making.

2. **Draw the boundary, `internal/` first.** From `requirements` (and `research`, so a reuse recommendation leans on the found module rather than re-implementing it), list the packages the capability needs, and place every one of them under `internal/` by default. Then promote, one at a time and with a stated reason: a package moves to the exported surface only if an external importer needs it and the project will support it under the posture fixed in step 1. Record the exported set explicitly — it is the API the compatibility promise covers.

3. **Design the binaries as shims.** For each command, fix what `cmd/` contains: flag parsing into a config value, the single call into the package below, the error-to-exit-code translation, and the stream wiring. Name the entry-point function that sits below it — the `run(ctx, args, stdin, stdout, stderr) error` shape — and confirm `os.Exit` appears only in `main`, so no deferred cleanup below it is skipped. Any logic the requirements put in a command is moved down into a package and named there.

4. **Write down the exit-code contract and the stream split.** Per binary: `0` for success and a distinct non-zero code per failure class a caller might branch on, each named against the condition that produces it; and the stdout/stderr split — machine-consumable output on stdout, diagnostics, progress, and errors on stderr. Where a machine-readable output mode is called for, decide it here (a `--format=json` flag or equivalent) rather than leaving downstream tools to scrape prose.

5. **Place the interfaces at their consumers.** For each point where behaviour genuinely varies, identify the *consuming* package and declare the narrow interface there; the producing package returns its concrete type. Reject an exported single-implementation interface published by its implementer, and reject a central `interfaces.go`. Where a set of interchangeable implementations *is* the exported API, say so and record the interface and its implementations as part of the exported surface from step 2.

6. **Thread the context and decide the error surface.** Mark every entry point and every function on a blocking path as taking `ctx context.Context` first, rooted at a cancellable context in `main`; confirm no design element stores a context in a struct. Then record the exported error surface: the sentinel values and error types callers may match with `errors.Is` and `errors.As`, and the rule that every intermediate layer wraps with `%w` and that message text is never part of the contract.

7. **Rule out initialisation side effects.** Confirm nothing in the design depends on work happening in an `init` function or on package-level mutable state — configuration is read in `main` and passed down, and collaborators are constructed explicitly. Where a blank-import registration pattern is being consumed from a library, record it as a consumed pattern with its reason.

8. **Assemble the package map.** Produce the map in dependency order: the `internal/` packages first (each with its purpose, its exported-within-the-module surface, and the interfaces its consumers declare over it), then the promoted exported packages with the reason each was promoted, then the `cmd/` shims with their argument surface and the entry point each calls. Include the module path and version posture, the exit-code contract, the context and error surfaces, and the build order — packages → entry-point function → command shim → tests. Hand the map to the caller; the plugin's design phase records it into the architecture artifact and runs the checklist gate. The recipe method writes no file of its own.

## Data flow

```
input: code_path, requirements, research (optional), components (optional),
       module_path (optional), go_version (optional)

reads project state:
       go.mod (module path, the `go` language line, the existing require closure)
       the existing package tree (what is already under internal/, cmd/, the root)
       the existing exported surface (what a consumer can already import today)
       existing architecture artifact
       the research recommendation (stdlib | copy-a-slice | reuse | extend | build-new)

applies opinion:
       internal/ is the default and the compiler enforces it · cmd/ parses, exits,
       wires streams, nothing else · os.Exit only in main because defers are skipped ·
       no pkg/ · interfaces at the consumer, concrete types returned · context first
       parameter, never a struct field · wrap with %w, export a small deliberate
       sentinel surface · no init() side effects, no package-level mutable state ·
       the module path is decided once and carries a promise · design decides,
       never builds

emits (to the caller; the recipe method writes nothing):
       module:     path + version posture (v0 no-promise | v1 committed | v2+ suffixed)
       packages:   internal/ set first, each with purpose + surface; then the promoted
                   exported set, each with the reason it was promoted
       commands:   the cmd/ shims — argument surface, the run(ctx,…) entry point called,
                   and os.Exit confined to main
       contract:   exit-code semantics · stdout/stderr split · machine-readable format
       seams:      each interface, the CONSUMING package that declares it, and its
                   implementations
       errors:     the exported sentinel/type surface + the wrap-with-%w rule
       order:      packages → entry-point function → command shim → tests
```

## State-awareness contract

The recipe reads existing state before deciding. The `go.mod` module path and language line, the current package tree, and whatever is already exported are read so the design extends what is present rather than colliding with it — and so a promotion out of `internal/`, or a change to the module path, is recognised as the breaking change it is rather than made silently. An extend recommendation and a stated dependency posture from prior art are honoured, not re-derived. The method is read-only on the project: it writes no Go, creates no directory, edits no `go.mod`, and requires nothing; the package map is returned to the caller, which owns recording it as the architecture artifact the downstream phases consume.

Idempotent: running the recipe twice on identical input and identical project state produces the same package map, with no side effect on either run. A map that changes because the requirements, the research recommendation, or the existing tree changed is the method reflecting current reality, not a non-deterministic recipe.

## Verifier

After the recipe runs, verify:

1. Every package the design introduces is placed under `internal/` unless it was explicitly promoted, and each promotion carries a recorded reason and an external importer that needs it.
2. The module path and version posture are recorded — `v0`, `v1`, or `v2+` with the major-version suffix in the path — and the exported surface the promise covers is stated, not implied.
3. Each `cmd/` binary is designed as a shim: flag parsing, one call into a named `run(ctx, args, stdin, stdout, stderr) error`-shaped entry point below it, error-to-exit-code translation, stream wiring — and nothing else. No design element places `os.Exit` outside `main`.
4. The exit-code contract is written down (`0` for success, a distinct named non-zero code per failure class) along with the stdout/stderr split, and a machine-readable output mode where one is called for.
5. No `pkg/` directory was introduced, or if one was, it carries a recorded repository-hygiene reason rather than being present by reflex.
6. Every interface is declared by the package that *consumes* it; no exported single-implementation interface is published by its implementer, and no central interface-catalogue file appears in the map.
7. `context.Context` is the first parameter on every entry point and every blocking path, rooted at a cancellable context in `main`; no design element stores a context in a struct.
8. The exported error surface is recorded — the sentinels and error types callers may match with `errors.Is` / `errors.As` — together with the rule that intermediate layers wrap with `%w` and that message text is not part of the contract.
9. Nothing in the design depends on an `init` function side effect or on package-level mutable state; any consumed blank-import registration pattern is recorded as such with its reason.
10. The design left the project unchanged — no Go written, no directory created, no `go.mod` edit, nothing required; the package map was returned for the plugin's design phase to record as the artifact the implement and review phases conform to.

This recipe ships no executable verifier of its own — the checks above are the agent-driven protocol; the plugin's design phase owns the architecture artifact and the checklist gate that blocks the implement phase on a failed item.

## References

### External origins (referenced, not authored here)

| Source | Used for |
|---|---|
| Organizing a Go module (go.dev/doc/modules/layout) | The official layout guidance the package map conforms to — package directories at the module root, `internal/` for what should not be imported, `cmd/` for commands, and the absence of a prescribed `pkg/` |
| The go command's internal-package rule (`go doc cmd/go`, "Internal packages") | The compiler-enforced boundary the `internal/`-by-default decision rests on: code in or below an `internal` directory is importable only by code sharing the import path above it |
| Go Modules Reference (go.dev/ref/mod) | The module-path identity and semantic import versioning rules behind the version posture — `v0` compatibility, the `v1` commitment, and the major-version path suffix from `v2` up |
| Effective Go and the Go proverbs | The interface-placement convention the design applies — accept interfaces, return structs; the interface belongs to the consumer |
| The `context`, `errors`, and `os` package documentation | The context-propagation contract, the `%w` / `errors.Is` / `errors.As` matching surface, and the `os.Exit` behaviour (deferred functions are not run) that confines it to `main` |

### Plugin-side generic mechanism (ai-dev-assistant)

The stack-neutral design phase this recipe binds Go into — when design runs, the shape of the architecture artifact, the checklist gate that blocks the implement phase, and how the decision is recorded and reviewed — is documented in the plugin itself, not duplicated here. The recipe supplies only the Go-specific design method: the `internal/`-by-default boundary, the `cmd/` shim and its exit-code contract, the module path and version posture, consumer-side interface placement, context propagation, the exported error surface, and the ban on initialisation side effects.
