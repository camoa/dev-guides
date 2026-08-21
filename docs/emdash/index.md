---
description: Adopting and building on EmDash — a beta full-stack TypeScript CMS on Astro + Cloudflare. Getting started, architecture, deploy targets, and content modeling with collections, generated types, and Portable Text.
tracks:
  - project: emdash
    registry: npm
    channel: stable
    declared: "0.20.0"
    verified: 2026-06-17
guide-meta:
  concepts:
    - EmDash CMS
    - Astro integration
    - Cloudflare D1/R2/Workers
    - Node + SQLite
    - sandboxed plugins
    - definePlugin
    - Worker Loaders
    - capability manifest
    - collections (content types)
    - visual schema builder
    - generated TypeScript types
    - npx emdash types
    - Astro live collections
    - getEmDashCollection
    - Portable Text
    - TipTap editor
    - passkey auth
    - revisions and scheduling
    - full-text search
    - WordPress migration
  not:
    - headless content delivery over REST
    - WordPress/PHP
    - Drupal
    - Next.js
  requires: []
  complements:
    - nextjs/next-drupal
    - css/modern-css
  specializes: ""
  category: emdash
---

# EmDash CMS

> **Beta preview.** EmDash is beta-preview software; APIs and config shapes change between releases. These guides pin what they were verified against — re-check the [official docs](https://docs.emdashcms.com/) and [repo](https://github.com/emdash-cms/emdash) before relying on details.

EmDash is a full-stack TypeScript CMS built on Astro that runs on Cloudflare (D1 + R2 + Workers) or Node + SQLite. Content is modelled in a built-in admin UI and served in-process through Astro's live content collections — it is deliberately **not** a headless-over-HTTP CMS. It positions itself as a modern successor to WordPress.

| I need to... | Guide |
|---|---|
| Understand EmDash, scaffold a project, run it locally, and choose a deploy target | [Getting Started and Architecture](getting-started-and-architecture.md) |
| Decide whether EmDash fits vs Next.js-headless or WordPress | [Getting Started and Architecture](getting-started-and-architecture.md) |
| Define content types, generate types, and query content | [Content Modeling](content-modeling.md) |
| Model structured content with Portable Text; handle revisions, drafts, scheduling, search | [Content Modeling](content-modeling.md) |

Verified against: `emdash-cms/emdash` `main@23c37f3` (2026-06-17), release `emdash@0.20.0`, docs at <https://docs.emdashcms.com/> (fetched 2026-06-16/17).
