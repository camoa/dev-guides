---
description: Author a missing dev-guides topic end to end — research a source guide, partition it, populate metadata, and open a PR. Stops at the PR; never merges or deploys.
argument-hint: <topic-or-capability> (e.g. "drupal/queue-api" or "how to use the Drupal Queue API")
allowed-tools: Read, Glob, Grep, Write, Edit, Bash, Task
model: claude-opus-4-8
---

# /create-guide

Orchestrate the creation of a **new** dev-guides topic from a gap to an opened pull request.
You are running inside the `~/workspace/dev-guides` content repo. You chain three existing
authoring agents (`guide-framework-maintainer`, `guide-partitioner`, `guide-meta-populator`)
and the repo's own scripts. **You end at an opened PR — you never push to `main`, never merge,
never deploy.** (Deploy runs only on merge to protected `main`; merge is the deploy.)

The requested topic/capability: **$ARGUMENTS**

---

## Hard rules (read before doing anything)

- **End at a PR.** Never `git push origin main`, never merge, never trigger a deploy.
- **Never commit generated indexes or sources.** Do NOT stage `site/`, `llms.txt`, `llms.hash`,
  `agentic-recipes.txt`, `agentic-recipes.hash`, or the source guide. The source guide lives
  *outside* this repo (in `~/workspace/claude_memory/guides/`) and stays there; CI regenerates
  all indexes on merge. A PR touches **only** `docs/**`, `mkdocs.yml`, and `partition-manifest.json`.
- **Respect the charter.** dev-guides documents *how to do things* in Drupal / CSS / JS / design
  systems / Next.js — APIs, configs, mechanics, framework patterns, and opinionated best practices
  for using them. It is NOT a home for information-architecture decision frameworks, content-modeling
  methodology, project-structure strategy, or "which approach should I pick" design intelligence.
  If the request is out of scope, **STOP at step 1** and route it elsewhere.
- **Confirm interfaces, don't guess.** If an agent or script behaves differently than described
  here, surface the mismatch and stop — do not improvise.

---

## Step 1 — Scope gate (charter)

Apply the litmus test: *Could a developer act on this guide by reading framework/Drupal APIs?*
- **In scope:** mechanics ("How to use the Queue API"), config/schema, hooks, plugin declaration,
  decisions *between framework mechanisms* ("FormBase vs ConfigFormBase").
- **Out of scope:** IA decisions ("taxonomy vs list_string for classification"), methodology
  ("Q1–Q6 field-storage decision tree"), project-architecture strategy, "what should I build."

If out of scope → **STOP.** Report the scope conflict in one line and suggest an alternate home
(design-intelligence skill / methodology doc). Do not create a branch.

## Step 2 — Miss check (new topic only)

Derive the topic path (e.g. `drupal/queue-api`). Confirm `docs/<topic>/` does **NOT** exist.
- If it exists → **STOP.** `/create-guide` is for *new* topics. Updating/refreshing an existing
  topic is a different flow (edit the source guide, re-run the partitioner). Report and exit.

## Step 3 — Branch off main

```bash
git fetch origin
git checkout main && git pull --ff-only
git checkout -b feature/<topic-dasherized>
```
Use a dasherized topic for the branch name (e.g. `feature/drupal-queue-api`).

## Step 4 — Research + write the SOURCE guide (maintainer)

Decide the source path: `~/workspace/claude_memory/guides/<category>-<topic>.md` (kebab-case, e.g.
`drupal-queue-api.md`). **Confirm this path with the user** before dispatching.

Dispatch the **`guide-framework-maintainer`** agent (Task tool, `subagent_type: guide-framework-maintainer`)
to research and write the comprehensive source guide **with `<!-- PARTITION: slug -->` markers** to
that local path. Pass it: the topic, the target source path, and the target docs topic path.

Notes:
- The maintainer authors **outside this repo** — its output is NOT committed here. Good.
- The maintainer may **ask for a clean Drupal research-install path** on first use. If it does,
  relay that question to the user and pass the answer back — do not invent a path.
- The maintainer enforces the charter too; if it declines on scope, **STOP** and report.

## Step 5 — PAUSE for human review of the source

**STOP and ask the user to review the source guide** at the path from step 4 before continuing.
The partitioner does NOT judge content quality — that is the maintainer's and the reviewer's job.
Do not proceed to step 6 until the user approves (or asks for edits, which the maintainer handles).

## Step 6 — Partition into docs/ (partitioner)

Dispatch the **`guide-partitioner`** agent (Task tool, `subagent_type: guide-partitioner`) with:
the **source guide path** and the **target topic path** (e.g. `drupal/queue-api`).

The partitioner writes: the atomic guides under `docs/<topic>/`, the topic `index.md` (with the
`guide-meta:` block **and** the 3-column "I need to… | Guide | Summary" routing table), the
`mkdocs.yml` nav entries, the parent **category** index row, and the `partition-manifest.json`
entry (hash, date, `partitioned_by` from `git config user.name`, count).

The partitioner **also enforces the charter** per-partition — if it stops on an out-of-scope
section, **STOP** and report; do not extract around it.

## Step 7 — Populate guide-meta (idempotent safety pass)

Dispatch the **`guide-meta-populator`** agent (Task tool, `subagent_type: guide-meta-populator`).
This is a **backstop**: the partitioner already writes `guide-meta:`, so the populator will usually
report "already had metadata" and skip. Keep it — it fills any gaps the partitioner left. It writes
**only** the `guide-meta:` block of `index.md` and nothing else.

## Step 8 — Backfill the Summary column (idempotent safety pass)

```bash
python scripts/add_tldr_to_routing_tables.py --topic <topic>
```
Scoped to the new topic only. The partitioner already builds the 3-column table, so this is
idempotent (`already-has-summary` → skip). It's a safety net for a partitioner that under-filled.

## Step 9 — Local build preview (do NOT commit output)

```bash
mkdocs build --strict
```
This is a **local preview / validation** only. The `site/` output is gitignored — never stage it.
If `--strict` fails on *this topic's* content, fix the source guide and re-run the partitioner
(do not hand-edit `docs/`). If it fails on unrelated pre-existing warnings, note it and continue.

## Step 10 — Stage, commit, push branch, open PR — then STOP

Stage **only** the three allowed paths (verify nothing else sneaks in):

```bash
git add docs/<topic>/ mkdocs.yml partition-manifest.json
git status --short            # confirm: ONLY docs/**, mkdocs.yml, partition-manifest.json
```

If `git status` shows `site/`, `llms.txt`, `agentic-recipes.txt`, or a source file staged — **unstage
it** before committing. Then:

```bash
git commit -m "docs(<topic>): add <Topic Name> guide

Authored via /create-guide: source researched by guide-framework-maintainer,
partitioned to docs/<topic>/, metadata populated. Source guide lives in
~/workspace/claude_memory/guides/ (not committed). Indexes regenerate in CI on merge.

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"

git push -u origin feature/<topic-dasherized>
gh pr create --base main --head feature/<topic-dasherized> \
  --title "docs(<topic>): add <Topic Name> guide" \
  --body "<summary of the topic, the guides extracted, and a note that the source guide is local and indexes regenerate in CI on merge>"
```

**STOP.** Report the **PR URL** and a summary of what was created (topic, guide count, manifest
entry). Do not merge. Do not deploy. The reviewer's merge into protected `main` is what deploys.

---

## Failure handling

- Out-of-scope (step 1) or existing topic (step 2) → stop cleanly, no branch.
- Any agent declines on charter → stop, report its rationale verbatim.
- Script/agent interface mismatch → stop, surface it, do not improvise.
- If `gh pr create` fails (e.g. no `gh` auth) → report the pushed branch name and the exact
  `gh pr create` command for the user to run; do not merge anything.
