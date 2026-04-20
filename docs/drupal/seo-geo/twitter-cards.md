---
description: Configure Twitter/X Cards in Drupal 11 using the metatag_twitter_cards submodule — card types, token mappings, and OG fallback strategy
tldr: "You need content shared on Twitter/X to display a rich card preview rather than a bare link. Enable the `metatag_twitter_cards` submodule."
drupal_version: "11.x"
---

# Twitter Cards

## When to Use

> You need content shared on Twitter/X to display a rich card preview rather than a bare link. Enable the `metatag_twitter_cards` submodule. Twitter/X reads `twitter:` tags first, then falls back to Open Graph tags — so if you have already configured OG tags, twitter: tags only need to provide values that differ from OG or add Twitter-specific fields (`twitter:card`, `twitter:site`, `twitter:creator`).

## Decision

| If you need... | Card type | Why |
|----------------|----------|-----|
| Standard link preview with small thumbnail | `summary` | Default card — image appears beside text |
| Large hero image above the tweet | `summary_large_image` | Dominates visual feed space; better for editorial content |
| App download card | `app` | Links directly to App Store / Google Play |
| Video player in timeline | `player` | Requires approved video player; rarely used |
| Minimal card, no image | `summary` with no image | Still renders title and description |

Most Drupal content uses `summary_large_image` for articles and `summary` for utility pages.

## Pattern

Minimal configuration — rely on OG fallback for shared values:

```
twitter:card:        summary_large_image
twitter:site:        @YourSiteHandle
twitter:creator:     @[node:author:field_twitter_handle]   (if author has a Twitter field)
twitter:title:       (leave empty — falls back to og:title)
twitter:description: (leave empty — falls back to og:description)
twitter:image:       (leave empty — falls back to og:image)
twitter:image:alt:   [node:field_image:alt]
```

Only `twitter:card` and `twitter:site` need explicit values. The rest can be empty and Twitter/X reads them from OG. This keeps configuration DRY and prevents values diverging between platforms.

## Tag Reference

| Tag | Required | Value / Token | Notes |
|-----|----------|---------------|-------|
| `twitter:card` | Yes | `summary` or `summary_large_image` | Must be explicit; no OG fallback |
| `twitter:site` | Recommended | `@sitename` | Twitter account for the site — appears in card footer |
| `twitter:creator` | Optional | `@authorhandle` | Author's personal Twitter account |
| `twitter:title` | Optional | `[node:title]` | Falls back to `og:title` if empty |
| `twitter:description` | Optional | `[node:field_summary]` | Falls back to `og:description` if empty |
| `twitter:image` | Optional | `[node:field_image:entity:url]` | Falls back to `og:image` if empty |
| `twitter:image:alt` | Recommended | `[node:field_image:alt]` | No OG fallback — must be set explicitly for accessibility |

## OG Fallback Strategy

Twitter/X's fallback order for each tag:

```
twitter:title        → og:title         → page <title>
twitter:description  → og:description   → none
twitter:image        → og:image         → none (no card image shown)
twitter:image:alt    → (no fallback)    → empty alt text
```

**Practical recommendation**: Set only `twitter:card`, `twitter:site`, and `twitter:image:alt` in Metatag. Everything else falls back to OG values. This avoids maintaining duplicate token patterns for title, description, and image.

## Card Appearance

| Card type | Image position | Image size displayed | Best for |
|-----------|---------------|---------------------|----------|
| `summary` | Thumbnail left of text | ~120x120 px square crop | Product pages, profiles, short updates |
| `summary_large_image` | Full-width above text | ~2:1 ratio | Articles, blog posts, events, editorial content |

For `summary_large_image`, image must be at least 300x157 px; recommended 1200x630 px (same as OG image — reuse the same image style).

## Validation and Debugging

**Twitter Card Validator**: `https://cards-dev.twitter.com/validator`

- Enter URL → "Preview Card" — shows exactly how the card renders
- Also shows which tags were read and any errors
- Cards are cached; after changes, use the validator to force a fresh fetch

Note: As of 2023, Twitter/X limited Card Validator access. If the validator is restricted, use a browser extension like "Open Graph Preview" or check the page source directly:

```bash
curl -s https://example.com/my-article | grep -E 'twitter:|og:'
```

**Drupal Devel output**: With Devel module active, the metatag debug block shows rendered tag values before the page is cached.

## Common Mistakes

- **Wrong**: Setting `twitter:card` to empty or omitting it → **Right**: `twitter:card` has no OG fallback — without it, Twitter/X displays a bare link with no card
- **Wrong**: Duplicating og: and twitter: values with the same tokens → **Right**: Leave twitter:title, twitter:description, twitter:image empty to rely on OG fallback; maintain one set of tokens
- **Wrong**: Using `twitter:site` without the `@` prefix → **Right**: Value must be `@yourhandle` including the `@` symbol
- **Wrong**: Omitting `twitter:image:alt` → **Right**: Alt text has no OG fallback; set `[node:field_image:alt]` explicitly for accessibility compliance
- **Wrong**: Setting `summary_large_image` on content types that have no image field → **Right**: Either ensure all items have images, or use `summary` card type for image-optional content types
- **Wrong**: Testing only in page source view → **Right**: Use the Twitter Card Validator or an OG preview tool — some image requirements only manifest in the actual card render

## See Also

- [Open Graph](open-graph.md) — OG tags that Twitter/X falls back to; configure these first
- [Metatag Architecture](metatag-architecture.md) — submodule activation and cascading inheritance
- [Core Meta Tags](core-meta-tags.md) — base title and description tokens
- Reference: [Twitter Cards documentation](https://developer.twitter.com/en/docs/twitter-for-websites/cards/overview/abouts-cards)
- Reference: [Twitter Card Validator](https://cards-dev.twitter.com/validator)
