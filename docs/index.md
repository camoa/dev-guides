---
description: AI-friendly decision guides for Drupal, Next.js, and decoupled web development
---

# Dev Guides

> **This site is designed for AI/LLM consumption, not human reading.** Content is structured as lean decision trees and pattern references optimized for token efficiency. If you're a human developer, you may find the format useful but terse — it's intentional.

Decision-making guides that answer: "When you need to do X, what should you choose and why?"

| Area | Topics |
|------|--------|
| [Drupal](drupal/index.md) | Forms, SDC, JS, Entities, Plugins, Routing, Config Forms, Icon API, AI Content, Blocks, Media, Migration, ECA, Klaro, GitHub Actions, Testing, Recipes, JSON:API, Taxonomy, Image Styles, Layout Builder, Views, Caching, Config Management, Custom Field, DRY, Render API, Security, Services, SOLID, TDD |
| [Next.js](nextjs/index.md) | Next.js for Drupal, Tiptap Editor, DeepChat |
| [Development Practices](development/index.md) | TDD, SOLID, DRY, Security Practices |
| [Design Systems](design-systems/index.md) | Recognition, Bootstrap Mapping, Radix SDC, Radix Components |

## For AI Consumers

This site is built for **targeted, on-demand retrieval** — not monolithic context loading. Every guide is a standalone atomic decision document (5-20KB) fetched individually as needed.

### Discovery & Retrieval Flow

| Step | Endpoint | Purpose |
|------|----------|---------|
| 1. Cache check | [`llms.hash`](llms.hash) | Tiny SHA-256 of `llms.txt` — fetch first to check if cache is fresh |
| 2. Topic catalog | [`llms.txt`](llms.txt) | ~1,500-line index of all topics with URLs to topic index pages and guide counts |
| 3. Routing table | `docs/{topic}/index.md` | Each topic's `index.md` contains a "I need to..." routing table + `guide-meta:` frontmatter (concepts/not/requires/complements) for intent disambiguation |
| 4. Atomic guide | `docs/{topic}/{guide}.md` | Individual decision guide — one decision per page, token-efficient |

**For raw markdown (bypasses MkDocs HTML rendering):**

```
https://raw.githubusercontent.com/camoa/dev-guides/main/docs/{topic}/{guide}.md
```

### Why No Giant Bundle?

We deliberately avoid a monolithic `llms-full.txt` or per-topic `.txt` bundles. The navigator plugin pattern fetches only the guides relevant to the current task, keeping context windows lean. See [dev-guides-navigator](https://github.com/camoa/claude-skills) for a reference implementation of this retrieval pattern.

### Format Conventions

- **Atomic guides**: One decision per file. YAML frontmatter → H1 → When to Use → Decision table → Pattern → Common Mistakes → See Also
- **`guide-meta:` frontmatter** on topic index pages: `concepts` (keywords that map here), `not` (disambiguation terms), `requires` (prerequisite topics), `complements` (related topics)
- **Content style**: Tables, bullets, minimal code. No prose paragraphs.
