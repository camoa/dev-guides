---
description: Controlling AI crawler access in robots.txt — block training bots while allowing search and retrieval bots for AI discoverability
tldr: "You need a deliberate policy on which AI crawlers can access your Drupal site and for what purpose. AI crawlers serve three distinct functions — training data collection, search/retrieval indexing, and user-initiated browsing — and should…"
drupal_version: "11.x"
---

# AI Crawler Policy

## When to Use

> You need a deliberate policy on which AI crawlers can access your Drupal site and for what purpose. AI crawlers serve three distinct functions — training data collection, search/retrieval indexing, and user-initiated browsing — and should be controlled separately. Getting this wrong either prevents your content from being cited by AI search engines or gives away content for model training without your consent.

## Decision

| Business situation | Policy | Reasoning |
|-------------------|--------|-----------|
| Content site wanting AI search visibility | Block training, allow search/retrieval | AI Overviews and Perplexity cite from their search indexes |
| SaaS product docs | Allow all search/retrieval | Visibility in AI coding assistants is valuable |
| Paywalled or licensed content | Block all AI crawlers | Training and retrieval both represent unauthorized use |
| News/journalism site | Block training, evaluate retrieval | OpenAI and Google have licensing programs for news |
| Default / no policy yet | Block training only (conservative default) | Prevents training use; preserves search discoverability |

## AI Crawler User Agents

| Company | Bot name | Purpose | Block to prevent |
|---------|----------|---------|-----------------|
| OpenAI | `GPTBot` | Training data collection | Model training on your content |
| OpenAI | `OAI-SearchBot` | ChatGPT search index | ChatGPT web search citations |
| OpenAI | `ChatGPT-User` | User-initiated browsing | ChatGPT user browsing your pages |
| Anthropic | `ClaudeBot` | Training data collection | Claude model training |
| Anthropic | `Claude-SearchBot` | Search and retrieval | Claude web search citations |
| Anthropic | `Claude-User` | User-initiated browsing | Claude users browsing your pages |
| Google | `Google-Extended` | Gemini/Bard training | Gemini model training (separate from Googlebot) |
| Perplexity | `PerplexityBot` | Search index + training | Perplexity citations |
| Meta | `FacebookBot` | General crawling | Facebook AI training |
| Common Crawl | `CCBot` | Open training datasets | Open-source model training |

Note: Blocking `Googlebot` is separate from blocking `Google-Extended`. Never block `Googlebot` — it drives traditional SEO. `Google-Extended` specifically controls Gemini/Bard use.

## Pattern: Recommended Configuration

Block training bots, allow search/retrieval bots. This is the recommended default for content sites wanting AI search visibility.

```
# =========================================
# AI Crawler Policy
# Block training, allow search/retrieval
# =========================================

# OpenAI: block training, allow search and user browsing
User-agent: GPTBot
Disallow: /

# OpenAI search and user agents: allow
User-agent: OAI-SearchBot
Allow: /

User-agent: ChatGPT-User
Allow: /

# Anthropic: block training, allow search and user browsing
User-agent: ClaudeBot
Disallow: /

User-agent: Claude-SearchBot
Allow: /

User-agent: Claude-User
Allow: /

# Google: block Gemini training, never block Googlebot
User-agent: Google-Extended
Disallow: /

# Perplexity: allow (search + citations)
User-agent: PerplexityBot
Allow: /

# Common Crawl: block (used for open model training)
User-agent: CCBot
Disallow: /

# Meta: block
User-agent: FacebookBot
Disallow: /
```

## Pattern: Block All AI Crawlers

For paywalled or licensed content:

```
User-agent: GPTBot
Disallow: /

User-agent: OAI-SearchBot
Disallow: /

User-agent: ChatGPT-User
Disallow: /

User-agent: ClaudeBot
Disallow: /

User-agent: Claude-SearchBot
Disallow: /

User-agent: Claude-User
Disallow: /

User-agent: Google-Extended
Disallow: /

User-agent: PerplexityBot
Disallow: /

User-agent: CCBot
Disallow: /
```

## Pattern: Allow All AI Crawlers

For developer documentation or open content where maximum AI visibility is the goal:

```
# Allow all AI crawlers for documentation sites
User-agent: GPTBot
Allow: /

User-agent: OAI-SearchBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: Claude-SearchBot
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Google-Extended
Allow: /
```

## Drupal robots.txt Management

Drupal 11 serves robots.txt as a static file at `web/robots.txt`. The `drupal_cms_seo_tools` recipe adds a `robots.append.txt` pattern — additional rules appended to the base robots.txt during deployment.

**Option A: Edit web/robots.txt directly**

Add AI crawler rules after the existing Drupal-generated rules. Simple, but changes are overwritten if the file is regenerated.

**Option B: robots.append.txt pattern**

Create `web/robots.append.txt` with only your additions. Include a deploy step that appends it:

```bash
cat web/robots.txt web/robots.append.txt > /tmp/robots-combined.txt
mv /tmp/robots-combined.txt web/robots.txt
```

**Option C: RobotsTxt module**

The `drupal/robotstxt` module serves robots.txt dynamically from Drupal config, allowing per-environment rules without file edits.

## Decision Tree

```
Do you want any AI search citations (ChatGPT Browse, Perplexity, AI Overviews)?
├── YES → Allow OAI-SearchBot, Claude-SearchBot, PerplexityBot
│   └── Do you want to allow model training on your content?
│       ├── YES → Allow GPTBot, ClaudeBot, Google-Extended, CCBot
│       └── NO  → Block GPTBot, ClaudeBot, Google-Extended, CCBot (recommended default)
└── NO  → Block all AI crawlers listed above
    └── Is your content paywalled/licensed?
        ├── YES → Consider OpenAI/Anthropic publisher licensing programs
        └── NO  → Revisit — blocking search bots reduces AI discoverability
```

## Common Mistakes

- **Wrong**: Blocking `Googlebot` to prevent AI training → **Right**: Block `Google-Extended` specifically; `Googlebot` drives traditional search ranking and must not be blocked
- **Wrong**: Assuming robots.txt is legally enforceable → **Right**: robots.txt is a convention; major crawlers honor it, but it carries no legal weight on its own
- **Wrong**: Setting one `Disallow: /` for all bots → **Right**: `User-agent: *` applies to all unspecified bots; add specific entries for AI crawlers above the `*` rule
- **Wrong**: Blocking all AI crawlers "to be safe" → **Right**: Blocking search/retrieval bots prevents AI citation; only block training bots if you want AI search presence
- **Wrong**: Setting rules and never reviewing them → **Right**: AI crawler policies are evolving rapidly; review every 6 months as new crawlers emerge
- **Wrong**: Expecting immediate effect → **Right**: Crawlers respect robots.txt on future visits; existing cached content in AI training data is unaffected

## See Also

- [llms.txt Implementation](llms-txt-implementation.md) — actively guide AI systems to your content
- [GEO Overview](geo-overview.md) — why AI discoverability matters
- [Robots.txt](robots-txt.md) — full robots.txt configuration for traditional SEO
- Reference: [OpenAI GPTBot documentation](https://platform.openai.com/docs/gptbot)
- Reference: [Google-Extended documentation](https://developers.google.com/search/docs/crawling-indexing/google-extended)
