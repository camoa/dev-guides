---
description: Configure Open Graph meta tags in Drupal 11 using the metatag_open_graph submodule for Facebook, LinkedIn, WhatsApp, and Slack sharing
drupal_version: "11.x"
---

# Open Graph

## When to Use

> You need content shared on Facebook, LinkedIn, WhatsApp, or Slack to display a rich preview with title, image, and description instead of a bare URL. Enable the `metatag_open_graph` submodule and configure token-based defaults for each content type. All major platforms read Open Graph tags; Twitter/X has its own card system but falls back to OG when no twitter: tags are present.

## Decision

| If you need... | Approach | Why |
|----------------|----------|-----|
| Rich previews on all social platforms | Enable metatag_open_graph, configure og:image | OG is the universal social sharing standard |
| Different image per content type | Token `[node:field_image:entity:url]` per type | Content-type-specific image field |
| Site-wide fallback image | Hardcode image URL in Global group og:image | Catches pages without a field image |
| Article-specific metadata (author, publish date) | Set `og:type` to `article`, add article:* tags | Facebook uses article type for news/blog content |
| E-commerce product cards | Set `og:type` to `product` | Platform-specific product display |
| Verify what platforms see | Facebook Sharing Debugger, LinkedIn Post Inspector | Platforms cache OG; use debuggers to force refresh |

## Pattern

Enable submodule, then configure at `/admin/config/search/metatag`:

```
og:title:       [node:title]
og:description: [node:field_summary]
og:image:       [node:field_image:entity:url]
og:url:         [current-page:url]
og:type:        article          (for blog/news content types)
og:site_name:   [site:name]
```

For content types without `field_image`, chain a fallback:

```
og:image: [node:field_image:entity:url]
           ↳ empty → Global og:image fallback image URL
```

Metatag evaluates the first non-empty token value. Set a hardcoded fallback image URL in the Global group so every page has an OG image even without a content image.

## Tag Reference

| Tag | Token pattern | Notes |
|-----|--------------|-------|
| `og:title` | `[node:title]` | Do not append site name — OG title is for social cards, not SERPs |
| `og:description` | `[node:field_summary]` | 2-4 sentences; platforms truncate at ~300 chars |
| `og:image` | `[node:field_image:entity:url]` | See image requirements below |
| `og:url` | `[current-page:url]` | Canonical URL for deduplication in social analytics |
| `og:type` | `website` / `article` / `product` | Default: `website`; set `article` for blog/news types |
| `og:site_name` | `[site:name]` | Appears below title in Facebook previews |
| `article:published_time` | `[node:created:html_datetime]` | Only for `og:type = article` |
| `article:modified_time` | `[node:changed:html_datetime]` | Only for `og:type = article` |
| `article:author` | Author profile URL | Facebook page URL or profile URL |

## Image Requirements

| Platform | Minimum size | Recommended | Aspect ratio | Format |
|----------|-------------|-------------|--------------|--------|
| Facebook | 200x200 px | 1200x630 px | 1.91:1 | JPG, PNG |
| LinkedIn | 1104x736 px | 1200x628 px | ~1.91:1 | JPG, PNG |
| WhatsApp | 300x200 px | 1200x630 px | 1.91:1 | JPG, PNG, GIF |
| Slack | No minimum | 1200x630 px | 1.91:1 | JPG, PNG |
| Twitter/X | 300x157 px | 1200x630 px | 1.91:1 | JPG, PNG, GIF |

**The 1200x630 standard covers all platforms.** Configure your image fields with Focal Point (included in `drupal_cms_seo_tools` recipe) so crops hit the right subject area when generating social card derivatives.

Set up an image style for OG images:

1. Create image style `social_card` at `/admin/config/media/image-styles`: Scale and Crop to 1200x630
2. Use the styled image URL token: `[node:field_image:social_card:url]` (requires Image module token support)
3. Alternatively use the `metatag_image_field_widget` approach with a dedicated OG image field

## Platform Behavior

| Platform | Cache TTL | Refresh method | Notes |
|----------|----------|----------------|-------|
| Facebook | 24 hours (default) | Facebook Sharing Debugger → "Scrape Again" | First scrape sets the cache |
| LinkedIn | ~7 days | LinkedIn Post Inspector | Cache is aggressive; test before publishing |
| WhatsApp | Session-based | Send new message after update | No manual purge tool |
| Slack | ~30 minutes | Unfurl re-triggers on new message | Generally self-refreshes quickly |
| Twitter/X | 7 days | Twitter Card Validator | Uses twitter: tags first, OG as fallback |

## Debugging

**Facebook Sharing Debugger**: `https://developers.facebook.com/tools/debug/`
- Paste URL → click "Debug" → "Scrape Again" to force cache refresh
- Shows exactly which OG tags Facebook reads and any warnings

**LinkedIn Post Inspector**: `https://www.linkedin.com/post-inspector/`
- Paste URL → "Inspect" — shows preview as LinkedIn sees it
- LinkedIn is strict about image dimensions; undersized images show no image card

**Manual inspection**: In browser DevTools, search page source for `og:` to see rendered tags. Or use curl:

```bash
curl -s https://example.com/my-article | grep 'og:'
```

## Common Mistakes

- **Wrong**: Setting `og:image` to a relative path like `/sites/default/files/image.jpg` → **Right**: OG image must be an absolute URL (`https://example.com/sites/...`); use `[node:field_image:entity:url]` which resolves to the full URL
- **Wrong**: Using the same image for all content types via a Global hardcode without a per-type override → **Right**: Set a per-content-type token for the image field first; Global hardcode serves as fallback only
- **Wrong**: Skipping `og:url` → **Right**: Always set `og:url` to `[current-page:url]`; platforms use it to deduplicate shares and attribute analytics correctly
- **Wrong**: Setting `og:type = article` on all content types → **Right**: `article` is for news/blog posts; use `website` for landing pages, homepages, and product categories
- **Wrong**: Not testing with the platform debugger before launch → **Right**: Always test in Facebook Sharing Debugger and LinkedIn Post Inspector — each platform has quirks not visible in page source
- **Wrong**: Image smaller than platform minimums → **Right**: Use 1200x630 px; undersized images either display tiny or get suppressed entirely

## See Also

- [Metatag Architecture](metatag-architecture.md) — cascading inheritance and submodule activation
- [Twitter Cards](twitter-cards.md) — twitter: tags with OG fallback strategy
- [Core Meta Tags](core-meta-tags.md) — title and description tokens that OG builds on
- Reference: [Open Graph Protocol](https://ogp.me/)
- Reference: [Facebook Sharing Debugger](https://developers.facebook.com/tools/debug/)
- Reference: [LinkedIn Post Inspector](https://www.linkedin.com/post-inspector/)
