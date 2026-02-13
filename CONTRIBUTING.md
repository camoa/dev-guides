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

1. **Write a comprehensive source guide** with partition markers (use the maintainer agent to help)
2. **Run the partitioner** — generates `docs/<topic>/` with index + atomic guides
3. **Submit a PR** — include the source guide path in your PR description

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

## Deployment

Push to `main` — GitHub Actions builds and deploys to GitHub Pages automatically. The workflow only triggers on changes to `docs/`, `mkdocs.yml`, or `requirements.txt`.

## License

MIT
