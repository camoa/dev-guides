---
description: Validate and debug Schema.org JSON-LD structured data — Google Rich Results Test, Schema.org Validator, Chrome DevTools, Drupal debugging, and common errors
drupal_version: "11.x"
---

# Testing & Validation

## When to Use

> Run validation immediately after configuring any structured data — before the page is indexed. A single missing required property (like `image` on Article) prevents rich result eligibility. Validation catches token mapping errors, missing fields, and malformed JSON before Google does.

## Decision

| Goal | Tool | Why |
|------|------|-----|
| Check rich result eligibility | Google Rich Results Test | The authoritative source; tests exactly what Google sees |
| Validate schema syntax | Schema.org Validator | Checks against Schema.org spec directly |
| Debug token rendering | Drupal metatag preview | See actual token output before Google does |
| Inspect raw JSON-LD in page | Chrome DevTools / view-source | Fast, no external service required |
| Catch regressions in CI | Drush + curl + JSONPath | Automate checks on deploy |
| Debug missing schema output | Drupal admin metatag UI | Verify configuration is saved correctly |

## Pattern

### 1. Google Rich Results Test

URL: `https://search.google.com/test/rich-results`

Enter your page URL or paste raw HTML. The tool shows:
- Which rich result types are detected
- Required vs recommended properties present
- Missing properties that block eligibility
- Warnings for recommended (non-blocking) issues

Rich result types that have specific eligibility requirements:
Article, FAQPage, HowTo, Product, Event, Recipe, BreadcrumbList, VideoObject, JobPosting

Pages with valid but non-eligible types (WebPage, Organization, Person) will show as "No rich results detected" — this is expected.

### 2. Schema.org Validator

URL: `https://validator.schema.org`

Validates against the Schema.org specification (not Google's subset). Useful for:
- Catching property name typos (`datePublish` vs `datePublished`)
- Verifying nested type structures
- Checking types Google's tool doesn't cover

Paste page URL or raw JSON-LD. The validator highlights unknown properties and type mismatches.

### 3. Chrome DevTools — Inspect JSON-LD

View raw output without any external tool:

```
1. Open page in Chrome
2. View page source: Ctrl+U (Cmd+U on Mac)
3. Search for: application/ld+json
4. Or: DevTools → Elements → Ctrl+F → search "ld+json"
```

For formatted inspection in DevTools Console:

```javascript
// Get all JSON-LD blocks on the page
document.querySelectorAll('script[type="application/ld+json"]')
  .forEach(s => console.log(JSON.parse(s.textContent)));
```

### 4. Drupal Metatag Debug

Check what Drupal is outputting before it reaches the browser:

```
# View metatag configuration for a specific content type
/admin/config/search/metatag

# Check token values on a specific node
/admin/config/search/metatag → Edit → use "Browse available tokens" link

# Enable Metatag debug output temporarily (Devel module)
drush en devel
# Then view node and check HTML source for rendered metatag output
```

Verify token resolution is working:

```
# Example: if [node:created:html_datetime] renders empty,
# check that:
# 1. The node has a created date (always true for Drupal nodes)
# 2. The html_datetime format is available in date formats
# /admin/config/regional/date-time → check for html_datetime format
```

### 5. Automated Testing Pattern

For CI pipelines or regression checking after deployments:

```bash
# Fetch page and extract JSON-LD
curl -s "https://example.com/my-article" \
  | grep -o '<script type="application/ld+json">.*</script>' \
  | sed 's/<[^>]*>//g'

# More reliable: use Python to extract all JSON-LD blocks
python3 -c "
import urllib.request, json, re
url = 'https://example.com/my-article'
html = urllib.request.urlopen(url).read().decode()
blocks = re.findall(r'<script type=\"application/ld\+json\">(.*?)</script>', html, re.DOTALL)
for b in blocks:
    print(json.dumps(json.loads(b), indent=2))
"

# Validate required properties exist
# Article must have: headline, image, datePublished, author
```

### Common Validation Errors and Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| "Missing field 'image'" | Image token not configured or field empty | Map `image > url` to hero image field; ensure field has content |
| "The value provided for 'datePublished' must be a valid date" | Token outputs non-ISO format | Use `[node:created:html_datetime]` not `[node:created]` |
| "Invalid URL" in image or url properties | Relative URL used | Always use `:absolute` URL token variants |
| "Invalid JSON" | Malformed token output (quotes, special chars) | Check for untokenized brackets; verify field contains plain text |
| "No items detected" | JSON-LD block not in page source | Check metatag config is saved; verify module is enabled; clear cache |
| Duplicate JSON-LD blocks | Both Schema Metatag and schemadotorg_jsonld active | Disable one; pick one output method per content type |
| "The value for property 'author' must be..." | Author set as plain string not Person object | Use nested type: `author > @type: Person` + `author > name: [token]` |

### Drupal Caching and Testing

Structured data output can be cached at multiple layers. When testing config changes:

```bash
# Always clear cache before testing
drush cr

# If using Varnish/CDN, also purge the cache for the test URL
# Or add ?nocache=1 (if site has cache-busting mechanism)
# Or use incognito window + disable cache in DevTools (Network tab)
```

For authenticated admin users, Drupal's page cache does not apply, so you'll see fresh output. Anonymous users may see cached output with old schema.

## Common Mistakes

- **Wrong**: Testing structured data while logged in as admin and assuming anonymous users see the same → **Right**: Log out or use a private window to test as anonymous; Drupal's page cache serves cached schema to anonymous users
- **Wrong**: Fixing errors in the Google Rich Results Test URL input field (which reformats HTML) → **Right**: Use the URL option, not HTML paste, for accurate rendering; paste HTML only when the page is behind authentication
- **Wrong**: Treating "No rich results detected" as an error for Organization or Person types → **Right**: Those types don't generate rich results; their value is entity association; use Rich Results Test only for eligible types
- **Wrong**: Validating only once at setup → **Right**: Re-validate after any token change, field rename, or module update; schema output breaks silently when underlying fields change
- **Wrong**: Only checking the homepage → **Right**: Test representative URLs for each content type (article, product, FAQ) since each has different token mappings

## See Also

- [Schema Metatag Setup](schema-metatag-setup.md)
- [Schema Types Reference](schema-types-reference.md)
- [Custom Schema Types](custom-schema-types.md)
- [Structured Data Decision](structured-data-decision.md)
- Reference: [Google Rich Results Test](https://search.google.com/test/rich-results)
- Reference: [Schema.org Validator](https://validator.schema.org)
- Reference: [Google Search Console Rich Results report](https://search.google.com/search-console/rich-results)
