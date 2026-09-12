---
# Routing block — an orchestrator reads to here and decides.
name: cc_plugins_research_prior_art
capability: research
description: Use when a Claude Code plugin project enters the research phase and must establish prior art before building — searches the plugin's own components first, then the installed skill / command / agent / hook / MCP surface and the reachable marketplaces, reads each candidate for availability, maintenance, trust and trigger-surface fit, and returns the candidates with the evidence behind each, ordered by closeness, for the design stage to decide on.
# Metadata — read only after a match.
label: Plugin prior-art research (Claude Code)
recipe_schema_version: 1.0.0
version: 0.1.0
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

Establish prior art before a single Claude Code component is scaffolded. The research asks one question from several angles: **does the capability already exist** — as a component of the plugin being worked on, as an installed skill, command, agent, hook, or MCP server, or as a plugin reachable in a marketplace. It returns the candidates it found with the evidence behind each.

**No verdict.** The recipe does not return reuse, extend or build-new. It returns what it found and what it read, ordered by closeness to the framed need, and the design stage decides. Ordering by closeness is a fact; choosing between two candidates that both pass is judgment, and judgment belongs to the stage that owns it.

**And no defer.** "Do not build this yet" is a decision about whether the task should happen at all. That is the scope stage's question, not research's and not design's. Where the recurrence evidence is thin, the research records the evidence and says the recurrence question belongs to scope — it does not sit on a verdict list here.

The plugin owns the generic research phase — when it runs and how its findings are recorded. This recipe owns the part the stack-neutral mechanism cannot know: *where* Claude Code capabilities live (the installed registry and the marketplaces), *how* to read a candidate's trigger surface, and *what* makes a candidate unusable.

## Opinion

**The default is not to build.** A new component earns its place only when nothing installed and nothing reachable covers the need. The cheapest plugin is the one already loaded; the second cheapest is one more component added to a plugin that already exists. A brand-new plugin is the most expensive option and the last one considered.

**Record the recurrence evidence against the 5-and-10 threshold; do not apply it as a decision.** A component is worth authoring when the task it automates has been done five or more times and will plausibly recur ten or more. Research records how often the task has actually occurred and what suggests it will recur, so the stage that owns the build decision has the evidence in front of it. A build justified on a one-off is waste, and the way research prevents it is by writing the count down, not by ruling.

**Search the model-invoked surface, not just the slash menu.** Skills are auto-triggered on their `description`; a capability can already be covered by a skill the user never types. Reading only the `/command` list misses exactly the components designed to fire without being named. The search reads the installed skill, command, agent, hook, and MCP surface together.

**A plugin that owns the domain is itself a candidate, and a distinct kind of one.** When a plugin owns the right domain but lacks the one component needed, that plugin is prior art — recorded as a candidate of the extendable kind, with the component it is missing named, and with `/plugin-creation-tools:add-component` as the handoff the design stage would use. It is a finding about what exists, not a ruling that fragmenting the surface is forbidden.

**The registry and the APIs are read live, never from memory.** Which plugins are installed, what a marketplace currently offers, and what the plugin / skill / hook contracts are this version — all move. The research reads the authoritative documentation through `superpowers-developing-for-claude-code:working-with-claude-code` and the live registry rather than recalling how it worked.

**Trust is a selection criterion.** A candidate from an unknown marketplace owner, or one that traverses paths it should not, is a finding, not a dependency. The research weighs the source the same way it weighs fit.

**A claim with no source is not a finding.** Every claim names where it was read — the registry, a marketplace listing, a plugin's own manifest — and the date it was read. A claim that can go stale and carries no source came from a model's memory, and memory is not research.

**Research reports; it does not scaffold.** The phase returns prior art. It creates no plugin, writes no component, installs nothing. Acting on the findings is the design and implement phases' work.

## Preconditions

- A Claude Code environment with plugin support, with the installed plugin / skill / command / agent / MCP registry readable and at least one marketplace reachable.
- A described need — the capability to be built, framed (or framable) as the trigger or use-case that would invoke it.
- The plugin's generic research phase is present: the phase that invokes this method and records its findings as `research/<search>.json`, rendered as `research/<search>.md` beside it. This recipe supplies the Claude-Code-specific search and reading; it does not recreate the phase.

## Input contract

Source-agnostic, supplied by the caller (the orchestrator at the research phase, or a human operator).

```yaml
need: string                  # the capability to research, described as the trigger /
                              #   use-case that would invoke it
code_path: string             # absolute path to the plugin being worked on; its own
                              #   components are the closest prior art there is
acceptance_criteria:          # what a person can see working when the task is done;
  - id: string                #   ids are minted by the caller and are stable
    statement: string
run_mode: string              # optional; interactive | autonomous
component_hint: string        # optional; suspected component type
                              #   (skill | command | agent | hook | mcp | theme)
marketplaces: [string]        # optional; marketplaces to search beyond the installed set
recurrence: string            # optional; evidence of how often the task has occurred /
                              #   will recur, for the 5-and-10 threshold
```

## Sequence

If invoked in dry-run mode, perform all reads and emit a prior-art preview instead of recording findings. Dry-run is required.

1. **Frame the need as a trigger surface.** Restate the need as the user phrasing or task that would invoke it, and as a candidate component type (skill for an auto-triggered workflow, command for a user-typed action, agent for isolated specialized work, hook for an event reaction, MCP for an external integration). This frame is what every candidate is matched against.

2. **Search the plugin's own components, before anything outside it.** The plugin being worked on has its own skills, commands, agents and hooks, and one of them that already fires on the framed trigger is the closest prior art there is.

    Derive the roots from `plugin.json` at `code_path`: it declares the component directories, so read what it declares rather than assuming the conventional layout. Read each candidate where its trigger actually lives — the `description` of a skill or an agent, the front matter and body of a command, the matcher of a hook. Out of bounds: the installed plugins and the marketplaces, which the next two steps cover; reading them here reports someone else's component as this plugin's own.

    A declared component directory that does not exist is recorded, not skipped, and an unreadable `plugin.json` is a gap rather than a clean result.

3. **Search the installed surface.** Read the installed plugins and, within them, the skill `description` triggers, the `/command` set, the agent descriptions, the declared hooks, and the MCP servers. A skill whose description already fires on the framed trigger is prior art even if no command names it. Defer to `superpowers-developing-for-claude-code:working-with-claude-code` for how the registry and loading actually work this version.

4. **Search the reachable marketplaces.** For needs the installed set does not cover, search the configured marketplaces (and any named in `marketplaces`) for candidate plugins, reading each candidate's described capability against the frame.

5. **Read each candidate.** Take the three readings this framework takes: **maintained** (version, recency, changelog), **used** (whether it is installed here, and how widely the marketplace shows it carried), **supported** (trust — the marketplace owner, and no path traversal or over-broad permissions — plus trigger-surface fit, whether its description fires on the framed need, and component-type fit, whether it delivers the need as the right component type).

6. **Record each candidate as a finding.** Per candidate:

    - what it is, and a link to where it was found — the design stage opens it later, and research deliberately does not read it for them;
    - the date it was read;
    - the three readings from the step above;
    - the acceptance criteria it speaks to, by id;
    - its kind, where Claude Code draws a real distinction — a component of the plugin being worked on, a component already installed, a plugin reachable in a marketplace, or a plugin that owns the domain and lacks one component, which the design stage would extend with `/plugin-creation-tools:add-component`.

    Record how often the task has actually happened and whether it looks likely to recur. That evidence is for the stage that decides whether the task should happen at all, which is neither this one nor design.

7. **Record the gaps: an empty search, an unanswered criterion, a reading you could not take.** A candidate that speaks to no acceptance criterion is recorded as such and never dropped — that is how work nobody asked for is caught. If nothing installed and nothing reachable covers the need, say so explicitly with what was searched and when: silence and a negative result look identical from outside, and the design stage cannot go back and look. If a reading could not be taken — a marketplace unreachable, a manifest unreadable — name the reading rather than letting a partial search read as a clean result.

8. **Report.** Order the candidates by closeness to the framed need and hand them to the caller, which records them as `research/<search>.json` and renders `research/<search>.md` beside it. Do not name a winner and do not recommend deferring: closeness is a fact and belongs here, fit belongs to design, and whether to build at all belongs to scope.

## Data flow

```
input: need, acceptance_criteria, code_path, component_hint (optional),
       marketplaces (optional), recurrence (optional), run_mode (optional)

reads project state:
       plugin.json at code_path (declares the component directories — read, not assumed)
       the plugin's own skills / commands / agents / hooks, at those directories

reads environment state:
       installed plugins + their skills / commands / agents / hooks / MCP servers
       skill and agent `description` triggers (the model-invoked surface)
       reachable marketplace catalogs (installed + caller-named)
       authoritative Claude Code docs (registry, loading, component contracts)

applies opinion:
       default is not to build · 5-and-10 recorded as evidence, not applied as a
       ruling · search the model-invoked surface, not just /commands · a plugin
       owning the domain is a candidate of its own kind · read the registry and
       APIs live, never from memory · trust is a reading · a claim with no source
       is not a finding · research reports, never scaffolds, never decides

references origin (never duplicated):
       superpowers-developing-for-claude-code:working-with-claude-code — registry,
              loading, component contracts (read live)
       plugin-creation-tools (plugin) — /plugin-creation-tools:add-component and
              /plugin-creation-tools:create, the handoff targets a finding names

emits (to the caller, which records research/<search>.json and renders
       research/<search>.md beside it; the recipe writes no file):
       findings:   per candidate — what it is, a link to where it was found, the
                   date read, the maintained / used / supported readings, the
                   acceptance criteria it speaks to by id, and its kind: installed
                   component, reachable plugin, or a plugin owning the domain and
                   missing one component. Ordered by closeness. No winner named.
       nothing:    an explicit "searched and found nothing", with what was searched
                   and the date, when neither installed nor reachable covers it
       gaps:       any reading that could not be taken, named
       recurrence: the 5-and-10 evidence, recorded for the scope stage
```

## State-awareness contract

The recipe reads the live environment — what is installed, what the reachable marketplaces offer, and the current component contracts — before recording anything. It matches candidates against the framed need, not against an idealized catalog, so a capability already present is found rather than rebuilt. The method is read-only on the environment: it installs nothing, scaffolds nothing, edits no plugin; the findings are returned to the caller, which owns recording them.

Idempotent for a fixed environment: running the research twice over the same installed set, the same reachable marketplaces, and the same need produces the same findings. Findings that change because a marketplace gained a plugin, or a plugin was installed, are the research reflecting current reality, not a non-deterministic recipe.

## Verifier

After the recipe runs, verify:

1. The plugin's own components were searched first, with the directories taken from `plugin.json` rather than assumed, or their absence recorded. A local search that quietly read nothing does not pass.
2. The installed surface was searched across all component types — skills (by `description` trigger), commands, agents, hooks, and MCP servers — not only the `/command` list.
3. The reachable marketplaces were searched for needs the installed set did not cover, and each candidate was read against the framed trigger surface.
4. Every candidate carries its readings — maintained, used, supported (trust, trigger-surface fit, component-type fit) — plus a link to where it was found and the date it was read. A claim carrying no source is not a finding.
5. Every candidate names the acceptance criteria it speaks to, by id, and its kind. One that speaks to none is recorded as such rather than dropped.
6. No verdict was returned, and no build was deferred. The candidates are ordered by closeness and no winner is named; the 5-and-10 recurrence evidence is recorded for the scope stage rather than used to rule a build in or out here.
7. A need that nothing installed and nothing reachable covers is reported explicitly, with what was searched and when, and any reading that could not be taken is named rather than left as an apparently clean result.
8. The research left the environment unchanged — nothing installed, scaffolded, or edited; the findings were returned for the plugin's research phase to record.

This recipe ships no executable verifier of its own — the search-and-read steps are the agent-driven protocol; the plugin's research phase owns recording the findings into `research/<search>.json` and rendering `research/<search>.md`.

## References

### External origins (referenced, not authored here)

| Source | Used for |
|---|---|
| `superpowers-developing-for-claude-code:working-with-claude-code` | The authoritative, live Claude Code documentation — how the plugin / skill / command / agent / hook / MCP registry and loading work this version; read rather than recalled |
| `superpowers-developing-for-claude-code:developing-claude-code-plugins` | The plugin lifecycle overview, for situating a candidate's maturity and where an extend-vs-build decision lands |
| plugin-creation-tools (plugin) | The scaffolding a finding hands off to — `/plugin-creation-tools:add-component` where a plugin owns the domain and lacks the component, `/plugin-creation-tools:create` where nothing does; this recipe names them, it neither invokes nor chooses between them |

### Plugin-side generic mechanism (ai-dev-assistant)

The stack-neutral research phase this recipe binds Claude Code into — when the phase runs, how its findings are recorded as `research/<search>.json` and rendered beside it, and how the design stage reads them — is documented in the plugin itself, not duplicated here. The recipe supplies only the Claude-Code-specific method: where capabilities live (the installed registry and the marketplaces), how to read a candidate's trigger surface, and the kinds of candidate Claude Code distinguishes.
