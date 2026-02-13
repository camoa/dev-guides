---
description: Enable automatic detection and blocking of external resources without manual HTML attributes
drupal_version: "11.x"
---

# Automatic Resource Attribution

## When to Use

> Enable automatic detection and blocking of external resources without manually adding HTML attributes. Critical for preventing pre-consent tracking.

## Decision

| If you need to block... | Enable... | Why |
|---|---|---|
| JS library files | Process js_alter | Matches script files from Drupal libraries |
| Manually attached JS | Process page_attachments | Catches JS added via render arrays |
| Embedded media (oEmbed, media fields) | Process preprocess_field | Blocks iframes from media fields |
| All external resources (experimental) | Process final HTML | Contextually blocks iframe/img/audio/video/script |
| Unknown external resources | Block unknown resources + Log unknown | Catches unmanaged third-party scripts |

## Pattern

**Recommended Configuration** (`/admin/config/user-interface/klaro`):

```yaml
automatic_attribution:
  process_js_alter: true  # Block library scripts
  process_page_attachments: true  # Block attached JS
  process_preprocess_field: true  # Block media embeds
  process_final_html: false  # EXPERIMENTAL - test first

unknown_resources:
  log_unknown: true  # Creates watchdog entries
  block_unknown: true  # Requires process_final_html
  unknown_label: "Unknown External Service"
  unknown_description: "This resource is not listed in our consent configuration."
```

**Progressive Enablement** (recommended workflow):
```yaml
# Phase 1: Enable safe options
process_js_alter: true
process_page_attachments: true
log_unknown: true  # Monitor what's missed

# Phase 2: Test field processing on staging
process_preprocess_field: true

# Phase 3: Test final HTML on staging (risky)
process_final_html: true  # Can break malformed HTML
block_unknown: true  # Aggressive blocking
```

**Manual Attribution** (fallback if automatic fails):
```html
<!-- Add data-klaro attribute to elements -->
<script src="analytics.js" data-type="text/plain" data-name="google_analytics"></script>
<iframe data-src="https://youtube.com/embed/..." data-name="youtube"></iframe>
```

**Reference**: `/modules/contrib/klaro/src/EventSubscriber/` for attribution implementation

## Common Mistakes

- **Wrong**: Enabling process_final_html on production without testing → **Right**: Breaks malformed HTML; test on staging first
- **Wrong**: Not enabling log_unknown before block_unknown → **Right**: Miss identifying unknown resources; log first to discover
- **Wrong**: Blocking unknown resources without reviewing logs → **Right**: May break legitimate content; identify unknowns first
- **Wrong**: Assuming automatic attribution catches everything → **Right**: Always test; some dynamic scripts evade detection
- **Wrong**: Enabling all options at once → **Right**: Hard to debug issues; enable progressively
- **Wrong**: Not configuring services for detected resources → **Right**: Automatic blocking works but users can't consent; add services
- **Wrong**: Forgetting to clear cache after enabling → **Right**: Changes don't take effect; clear Drupal cache

## See Also

- [Translation and Localization](translation-and-localization.md)
- [Menu Integration](menu-integration.md)
- Reference: [Klaro Attribution Documentation](https://www.drupal.org/docs/extending-drupal/contributed-modules/contributed-module-documentation/klaro-cookie-consent-management)
