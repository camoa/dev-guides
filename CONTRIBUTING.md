# Contributing to Dev Guides

Decision-making guides for web development, optimized for AI/LLM consumption.

## How Guides Work

This site uses a two-stage workflow:

1. **Comprehensive source guides** — detailed single-file guides with partition markers, maintained elsewhere
2. **Atomic guides** — extracted from source guides into small, focused files (max 80 lines each)

The `guide-partitioner` agent (`.claude/agents/guide-partitioner.md`) handles the extraction from source to atomic format.

## Guide Format

### Atomic Guide (what gets published)

Each guide covers one decision and follows this template:

```markdown
---
description: One-line summary
drupal_version: "11.x"
---

# Topic Name

## When to Use
> Use [this] when [condition].

## Decision
| Situation | Choose | Why |
|-----------|--------|-----|

## Pattern
Minimal code (5-15 lines).

## Common Mistakes
- **Wrong**: X → **Right**: Y

## See Also
- [Related guide](link.md)
```

**Rules:**
- Max 80 lines per file
- No prose — tables, bullets, code only
- One decision per file
- Include core file references and documentation URLs

### Topic Index

Each topic directory has an `index.md` with a routing table:

```markdown
| I need to... | Guide |
|-------------|-------|
| Do X | [Guide Name](file.md) |
```

Max 30 lines. Maps user intent to the right guide.

## Structure

```
docs/
├── drupal/
│   ├── index.md          # Drupal master TOC
│   ├── forms/
│   │   ├── index.md      # Forms TOC
│   │   ├── config-form-base.md
│   │   └── ...
│   ├── entities/
│   └── ...
├── nextjs/
└── decoupled/
```

## Adding a Guide

1. Create the `.md` file in the appropriate `docs/` directory
2. Follow the atomic guide template above
3. Update the topic's `index.md` with a new routing entry
4. Update `mkdocs.yml`:
   - Add to `nav` under the correct section
   - Add to `plugins.llmstxt-md.sections` with a description

## Updating mkdocs.yml

Both sections must stay in sync:

```yaml
nav:
  - drupal/forms/my-new-guide.md    # Navigation

plugins:
  - llmstxt-md:
      sections:
        "Drupal":
          - drupal/forms/my-new-guide.md: "Description for llms.txt"
```

## AI Agent

The `.claude/agents/guide-partitioner.md` agent automates extraction from comprehensive source guides. It reads partition markers and generates atomic guides in the correct format.

## Local Development

```bash
pip install -r requirements.txt
mkdocs serve    # Preview at http://localhost:8000
mkdocs build    # Build to site/
```

## Deployment

Push to `main` — GitHub Actions builds and deploys to GitHub Pages automatically.

## License

MIT
