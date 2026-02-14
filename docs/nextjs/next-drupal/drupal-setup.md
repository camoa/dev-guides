---
description: "Follow this workflow when setting up a new Drupal backend for Next.js or adding Next.js support to an existing Drupal site."
drupal_version: "11.x"
topic: "drupal/next-drupal"
---

## Drupal Setup

### When to Use

Follow this workflow when setting up a new Drupal backend for Next.js or adding Next.js support to an existing Drupal site.

### Steps

**1. Install Drupal Next module**

```bash
composer require drupal/next
```

**2. Enable required modules**

Visit `/admin/modules` and enable:
- Next.js (core Next module)
- Next.js JSON:API (for JSON:API support) OR Next.js GraphQL (for GraphQL support)

**3. Apply multilingual patches (if needed)**

For multilingual sites, apply the Decoupled Router patch:

```json
// composer.json
"extra": {
  "patches": {
    "drupal/decoupled_router": {
      "Unable to resolve path on node in other language than default": "https://www.drupal.org/files/issues/2024-08-05/decouple_router-3111456-resolve-language-issue-63--get-translation-re-rolled-and-good-redirect.patch"
    }
  }
}
```

Then run: `composer require cweagans/composer-patches`

**4. Configure path aliases**

Visit `/admin/config/search/path/patterns/add` and create patterns for each content type:

- Pattern type: Content
- Path pattern: `blog/[node:title]` (example for articles)
- Content type: Article
- Label: Article

**5. Configure OAuth (for authenticated requests)**

See Authentication Patterns section for OAuth setup.

**6. Configure JSON:API page limit (optional)**

In `sites/default/services.yml`:

```yaml
parameters:
  next_jsonapi.size_max: 100
```

Clear cache: `drush cr`

### Decision Points

| Decision | When | Why |
|----------|------|-----|
| Apply multilingual patch | Using translations | Fixes language resolution issues |
| Configure page limit | Sites with 50+ pages | JSON:API defaults to 50 resource limit |
| Enable JSON:API CRUD operations | Need to create/update content from Next.js | Required at `/admin/config/services/jsonapi` |

### Common Mistakes

- **Skipping path alias configuration** — Routes won't resolve. WHY: Next.js relies on path aliases for routing.
- **Not clearing cache after services.yml changes** — Settings don't apply. WHY: Drupal caches service definitions.
- **Enabling all JSON:API modules** — Security risk. WHY: Exposes unnecessary endpoints. Enable only next_jsonapi.

### See Also

- Authentication Patterns
- Multilingual Support
- drupal-jsonapi.md
