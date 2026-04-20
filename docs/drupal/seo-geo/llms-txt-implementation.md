---
description: Implementing llms.txt on a Drupal site — static file, custom route, or build script — for AI assistant discoverability
tldr: "You want AI coding assistants, documentation tools, and LLM-powered search to find and understand your site's content. The llms.txt standard (llmstxt.org, September 2024) is a lightweight convention: place a machine-readable index at…"
drupal_version: "11.x"
---

# llms.txt Implementation

## When to Use

> You want AI coding assistants, documentation tools, and LLM-powered search to find and understand your site's content. The llms.txt standard (llmstxt.org, September 2024) is a lightweight convention: place a machine-readable index at `/llms.txt` so AI systems know what your site contains and where to find full content. Primary value is for AI coding assistants (Cursor, Copilot, Claude Code) that read project docs — not yet honored at inference time by ChatGPT or Google AI Overviews.

## Decision

| Situation | Approach | Effort |
|-----------|----------|--------|
| Static site or docs site | Static `llms.txt` file in web root | Minimal |
| Drupal site, content changes rarely | Static file in `/web/` committed to repo | Low |
| Drupal site, content changes frequently | Custom route that generates file dynamically | Medium |
| Large site with many content types | Build script — generate from MkDocs/CMS on deploy | Medium |
| You want full page content for RAG | Also generate `llms-full.txt` with page body | Medium |
| AI assistants are your primary audience | llms.txt as a topic catalog linking to per-guide `.md` files | Dev docs pattern |

## The llms.txt Format

Defined at llmstxt.org. The format is intentionally minimal — structured Markdown that LLMs can parse without special tooling.

```markdown
# Site or Product Name

> One-paragraph description of what this site/product is and who it is for.
> Written for an LLM audience: factual, concise, complete.

## Section Name

- [Page Title](https://example.com/page/): One-line description of what this page covers
- [Another Page](https://example.com/other/): Description

## Another Section

- [Guide Title](https://example.com/guide/): Description
```

**Format rules:**
- H1: site or product name
- Blockquote after H1: description paragraph (required)
- H2: logical sections grouping related links
- Bullet list entries: `- [Title](URL): description`
- Keep descriptions to one line — LLMs read these to decide whether to fetch the full page
- `llms-full.txt` is the same format but includes the full body of each page inline, for RAG vectorization

## Confirmed Adopters (as of Q1 2026)

| Organization | URL | Notes |
|-------------|-----|-------|
| Cloudflare | cloudflare.com/llms.txt | Developer docs, Workers, AI Gateway |
| Anthropic | anthropic.com/llms.txt | Claude API docs, model reference |
| Stripe | stripe.com/llms.txt | Payment API documentation |
| Supabase | supabase.com/llms.txt | Database and auth docs |
| Vercel | vercel.com/llms.txt | Deployment and framework docs |
| FastAPI | fastapi.tiangolo.com/llms.txt | Python web framework |

Adoption is concentrated in developer-tool companies because the primary current use case is AI coding assistants reading documentation.

## Current Limitations

| Limitation | Detail |
|------------|--------|
| No AI company committed to honoring at inference time | As of Q1 2026, OpenAI, Google, and Anthropic have not confirmed they read llms.txt during ChatGPT/AI Overviews/Claude web answers |
| No standardized crawl protocol | There is no GPTBot or ClaudeBot equivalent that specifically fetches llms.txt |
| Discovery depends on tool implementation | AI coding assistants (Cursor, GitHub Copilot Workspace) actively support it; consumer AI chat does not yet |
| Spec is still evolving | llmstxt.org is community-maintained; breaking changes possible |

**Primary value today:** AI coding assistants. If your Drupal site serves developer documentation, llms.txt is worth implementing. For consumer content sites, it is a low-effort forward-looking signal.

## Pattern: Static File (Recommended for Most Sites)

Place a file at `/web/llms.txt` in your Drupal repo. This works because Drupal's front controller only intercepts paths that don't match existing files.

```markdown
# My Drupal Site

> Developer documentation and guides for configuring [Site Name] on Drupal 11.
> Covers [main topics]. For site builders and developers.

## Getting Started

- [Overview](https://example.com/docs/overview/): What this site does and how it is organized
- [Installation](https://example.com/docs/install/): Requirements and install steps

## Configuration

- [SEO Configuration](https://example.com/docs/seo/): Meta tags, structured data, sitemaps
- [Content Types](https://example.com/docs/content-types/): Available content models

## API Reference

- [REST API](https://example.com/api/): JSON:API endpoints and authentication
```

Commit this file to `web/llms.txt`. Drupal will serve it as a static asset. Verify with `curl https://example.com/llms.txt`.

## Pattern: Custom Drupal Route

For sites where content changes frequently and you want the index auto-generated:

```php
// mymodule.routing.yml
mymodule.llms_txt:
  path: '/llms.txt'
  defaults:
    _controller: '\Drupal\mymodule\Controller\LlmsTxtController::index'
    _title: 'llms.txt'
  requirements:
    _access: 'TRUE'
  options:
    no_cache: FALSE
```

```php
// LlmsTxtController.php
public function index(): Response {
  $content = $this->buildLlmsTxt();
  return new Response($content, 200, [
    'Content-Type' => 'text/plain; charset=UTF-8',
    'Cache-Control' => 'public, max-age=3600',
  ]);
}
```

The controller queries published nodes by content type and builds the Markdown index. Cache with Drupal's render cache or a dedicated cache bin — regenerating on every request is expensive on large sites.

## Pattern: Topic Catalog + Per-Guide Fetch (Dev Docs Sites)

For dev documentation with many atomic guides, use `llms.txt` as a **topic catalog** pointing to topic index pages. Each topic's index page carries a routing table and KG metadata (concepts, disambiguation) that an AI navigator uses to pick a specific guide. The AI fetches only the guide(s) relevant to the task — no monolithic bundles.

This is the pattern this project uses (see [dev-guides-navigator](https://github.com/camoa/claude-skills) for a reference implementation):

```markdown
# Dev Guides

> Atomic decision guides for Drupal 11, CSS, and frontend development.

## Drupal

- [Drupal SEO & GEO](https://example.com/drupal/seo-geo/): 27 guides covering SEO, structured data, and GEO for Drupal 11
- [Drupal Forms](https://example.com/drupal/forms/): Form API, validation, AJAX, and form alter patterns
```

**Retrieval flow:**

1. `llms.hash` — tiny SHA-256 for cache invalidation (64 bytes)
2. `llms.txt` — topic catalog (~15KB)
3. `{topic}/index.md` — routing table ("I need to..." → guide.md) + `guide-meta:` frontmatter
4. `{topic}/{guide}.md` — the specific atomic guide (5-20KB)

Each atomic guide is fetched independently, keeping AI context windows lean. Compare with per-topic concatenated bundles (5K-41K tokens each): bundles load too much content when the user only needs one decision answered. The per-guide approach is more efficient when the catalog has 1,000+ guides across 70+ topics.

## llms-full.txt for RAG

If you are building a RAG (Retrieval-Augmented Generation) pipeline over your own content — for an AI chatbot, search, or documentation assistant — generate `llms-full.txt` with full page bodies:

```markdown
# Site Name

> Description paragraph.

## Section Name

### [Page Title](https://example.com/page/)

Full page body content here...

---

### [Another Page](https://example.com/other/)

Full page body content here...
```

This is the format used by vector database ingestion pipelines. The `---` separator between pages aids chunking. Size warning: `llms-full.txt` can be several MB for large sites; this is intentional for RAG use but not suitable for direct LLM context injection.

## Common Mistakes

- **Wrong**: Putting `llms.txt` in the Drupal public files directory (`sites/default/files/`) → **Right**: Place in `web/` root alongside `index.php`; files directory URLs are unpredictable
- **Wrong**: Making llms.txt the same as your sitemap (XML + all URLs) → **Right**: llms.txt is a curated, human-readable index with descriptions; include only meaningful pages
- **Wrong**: Expecting ChatGPT to cite you more because you have llms.txt → **Right**: Current value is for AI coding assistants, not consumer AI chat inference
- **Wrong**: Generating llms.txt on every page request → **Right**: Cache aggressively; this file changes at most daily
- **Wrong**: Skipping the blockquote description paragraph → **Right**: The description is required by the spec and is the primary signal LLMs use to decide if this site is relevant

## See Also

- [AI Crawler Policy](ai-crawler-policy.md) — control which AI crawlers access your content
- [GEO Overview](geo-overview.md) — context for why llms.txt matters
- [Content Patterns for AI](content-patterns-ai.md) — the content behind the links
- Reference: [llms.txt Specification](https://llmstxt.org)
