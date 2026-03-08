---
description: Pathauto URL alias patterns — token syntax, per-content-type configuration, bulk generation, transliteration, and common mistakes
drupal_version: "11.x"
---

# Pathauto Patterns

## When to Use

> Configure Pathauto when you need clean, SEO-friendly URL aliases generated automatically from content fields. Pathauto runs on every node/term/user save and applies your token-based pattern to produce the alias — no manual entry required.

## Decision

| Situation | Choice | Why |
|-----------|--------|-----|
| All content types use same URL structure | Single global pattern | Easier to maintain; apply at the entity level |
| Blog posts need `/blog/title`, events need `/events/date/title` | Per-content-type patterns | Different structures need separate pattern config |
| Site launch with existing content, no aliases | Bulk generation | One-time operation to retroactively create all aliases |
| Non-ASCII characters in titles (French, Arabic, etc.) | Enable transliteration | Prevents encoded characters in URLs; `é` → `e` |
| Alias already exists for a node | Update action: `Create new alias` + delete old | Paired with Redirect module, old alias becomes a redirect automatically |

## Pattern

**Token syntax for common patterns:**

```
/blog/[node:title]
/[node:content-type]/[node:title]
/news/[node:field_date:date:custom:Y]/[node:title]
/[term:vocabulary]/[term:name]
/user/[user:name]
```

**Configure per-content-type pattern** at `admin/config/search/path/patterns/add`:

- Entity type: Content
- Bundle: Article (or your content type)
- Pattern: `/blog/[node:title]`

**Bulk generate aliases** for existing content at `admin/config/search/path/bulk-update`:

- Select entity types to process
- Choose update action: generate aliases for entities without one, or regenerate all
- Run in batches — large sites should use Drush: `drush pathauto:aliases-generate all node`

**Transliteration settings** at `admin/config/search/path/settings`:

- Enable "Transliterate prior to creating alias"
- Set separator (default: `-`)
- Enable "Reduce strings to letters and numbers" for maximum compatibility
- Set maximum alias length (default: 100 characters)

## Common Mistakes

- **Wrong**: Leaving the default global pattern `/content/[node:title]` on a site with multiple content types → **Right**: Create per-content-type patterns immediately; the `/content/` prefix is meaningless for SEO
- **Wrong**: Using `[node:nid]` as part of the pattern on a public site → **Right**: IDs expose content volume and create guessable URLs; use semantic tokens like `[node:title]` or `[node:field_slug]`
- **Wrong**: Generating aliases without the Redirect module active → **Right**: Install Redirect alongside Pathauto so alias changes automatically create 301 redirects; without it, old URLs return 404
- **Wrong**: Pattern produces duplicate aliases (two nodes with same title get same alias) → **Right**: Enable "Avoid duplicate aliases" in Pathauto settings; it appends `-0`, `-1` automatically
- **Wrong**: Very long titles create URLs over 100 characters → **Right**: Set a maximum alias length and enable word-boundary truncation so aliases don't break mid-word

## See Also

- [SEO Recipe Baseline](seo-recipe-baseline.md) — Pathauto is installed by `drupal_cms_seo_basic`
- [Redirect Management](redirect-management.md) — redirect-on-alias-change requires Redirect module
- Reference: [Pathauto on drupal.org](https://www.drupal.org/project/pathauto)
- Reference: [Token module](https://www.drupal.org/project/token) — browse available tokens at `admin/help/token`
