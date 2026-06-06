# Contributing to Dev Guides

Decision-making guides for web development, optimized for AI/LLM consumption.

## Architecture

```
Source Guide (local)          Published Site (GitHub Pages)
┌──────────────────┐          ┌──────────────────────────┐
│ Comprehensive    │  guide-  │ docs/drupal/forms/       │
│ single file with │──parti──→│   index.md (TOC)         │
│ PARTITION markers│  tioner  │   config-form-base.md    │
│                  │          │   validation.md          │
└──────────────────┘          │   ...                    │
        ▲                     └──────────────────────────┘
        │ guide-framework-                │
        │ maintainer                      ▼
        │                          partition-manifest.json
   Research, update,              (tracks source hashes)
   add best practices
```

**Two agents, two jobs:**

| Agent | Purpose | When to use |
|-------|---------|-------------|
| `guide-framework-maintainer` | Research and update source guides | Source content is outdated or incomplete |
| `guide-partitioner` | Extract atomic guides from source | Source guide has been updated (hash mismatch) |

## Workflow

### Updating existing content

1. **Edit your source guide** — update content, add partition markers
2. **Check if re-partitioning is needed** — `sha256sum <source-file>` vs `partition-manifest.json`
3. **Run the partitioner** — extracts atomic guides, updates manifest with your name and hash
4. **Submit a PR** — the manifest shows what changed and who did it

### Creating a new topic

The fastest path is the **`/create-guide`** command (Claude Code), which orchestrates the whole
chain and stops at an opened PR:

```
/create-guide <topic-or-capability>
```

It runs: **scope gate** (charter) → **miss check** (topic must not already exist) → branch off
`main` → **`guide-framework-maintainer`** researches and writes the comprehensive *source* guide
(with PARTITION markers, to `~/workspace/claude_memory/guides/` — outside this repo) → **human
review pause** → **`guide-partitioner`** extracts atomic guides into `docs/<topic>/` (index +
routing table + `mkdocs.yml` nav + manifest) → **`guide-meta-populator`** + `add_tldr` backfill
(idempotent) → local `mkdocs build` → opens a PR. It **never** merges or deploys.

Doing it by hand instead:

1. **Write a comprehensive source guide** with partition markers (use the maintainer agent to help).
   The source lives in `~/workspace/claude_memory/guides/` and is **never committed** to this repo.
2. **Run the partitioner** — generates `docs/<topic>/` with index + atomic guides, updates
   `mkdocs.yml` and `partition-manifest.json`.
3. **Open a PR** touching only `docs/**`, `mkdocs.yml`, and `partition-manifest.json`. Mention the
   (local) source guide path in the PR description. Do **not** commit `site/`, `llms.txt`, or
   `agentic-recipes.txt` — CI regenerates those on merge.

### Using the agents (Claude Code)

```
# Maintain/update a source guide (research, add best practices)
Use guide-framework-maintainer agent on /path/to/source-guide.md

# Extract atomic guides from source
Use guide-partitioner agent on /path/to/source-guide.md for topic drupal/forms
```

## Guide Format

### Source Guide (partition markers)

```markdown
<!-- PARTITION: section-slug -->
## Section Title

### When to Use
Brief scenario description.

### Decision
| If you need... | Use... | Why |

### Pattern
Minimal code (5-15 lines).

### Common Mistakes
- Mistake → Correction

### See Also
- Reference: source file or URL
<!-- END PARTITION: section-slug -->
```

### Published Atomic Guide

Each file covers one decision:

```markdown
---
description: One-line summary
drupal_version: "11.x"
---

# Topic Name

## When to Use
## Decision
## Pattern
## Common Mistakes
## See Also
```

**Rules:**
- No prose — tables, bullets, code only
- One decision per file
- Keep lean — no filler, as long as content requires
- Include core file references and documentation URLs

### Topic Index

Each topic directory has an `index.md` routing table:

```markdown
| I need to... | Guide |
|-------------|-------|
| Do X | [Guide Name](file.md) |
```

## Partition Manifest

`partition-manifest.json` tracks source-vs-published drift:

```json
{
  "drupal/forms": {
    "source_hash": "sha256-of-source-at-partition-time",
    "partitioned": "2026-02-12",
    "partitioned_by": "contributor-name",
    "guides_extracted": 27
  }
}
```

- Hash mismatch = source was updated, needs re-partitioning
- The partitioner updates this automatically after each run
- Git history on the manifest provides full audit trail

## Structure

```
docs/
├── drupal/
│   ├── index.md              # Drupal master TOC
│   ├── forms/
│   │   ├── index.md          # Forms routing table
│   │   ├── config-form-base.md
│   │   └── ...
│   ├── sdc/
│   └── js-development/
├── design-systems/
│   ├── index.md              # Design Systems master TOC
│   ├── recognition/
│   ├── bootstrap/
│   └── radix-sdc/
├── nextjs/                   # Coming soon
└── decoupled/                # Coming soon
```

## Updating mkdocs.yml

Both sections must stay in sync:

```yaml
nav:
  - drupal/forms/my-guide.md

plugins:
  - llmstxt-md:
      sections:
        "Drupal":
          - drupal/forms/my-guide.md: "Description for llms.txt"
```

## Local Development

```bash
pip install -r requirements.txt
mkdocs serve    # Preview at http://localhost:8000
mkdocs build    # Build to site/
```

## External contributors

Contributors work as **repo collaborators on branches — no fork.** `main` is protected.

- Branch from `main` using a `feature/*` branch; never push to `main` directly.
- Open a PR into `main`. It must pass the **`build`** status check (`.github/workflows/pr-check.yml`:
  `mkdocs build --strict` + recipe validation) and get **1 approving review** before it can merge.
- A PR should touch only `docs/**`, `mkdocs.yml`, and `partition-manifest.json`. Generated indexes
  (`site/`, `llms.txt`, `agentic-recipes.txt`) are **CI artifacts** — never commit them. Source
  guides live outside the repo (the manifest records only their hash) — never commit them either.
- **Merging the PR is the deploy.** `deploy.yml` runs only on push to `main`, and with `main`
  protected the only such push is a reviewed PR merge — which then regenerates the indexes and
  publishes to GitHub Pages.

## Deployment

A merge to `main` is the deploy. GitHub Actions (`deploy.yml`) builds the site, regenerates
`llms.txt` and `agentic-recipes.txt`, and publishes to GitHub Pages. It triggers only on push to
`main` (a reviewed PR merge) for changes under `docs/`, `mkdocs.yml`, `scripts/`,
`partition-manifest.json`, `llms.txt.template`, or `requirements.txt`. PRs themselves only build
and validate (`pr-check.yml`) — they do not deploy.

## License

MIT
