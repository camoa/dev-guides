---
description: Diagnose consent modal, script blocking, and configuration issues
drupal_version: "11.x"
---

# Troubleshooting

## When to Use

> Diagnose and resolve common Klaro configuration issues, script blocking failures, and modal rendering problems.

## Decision

| Problem | Diagnosis | Solution |
|---|---|---|
| Consent modal doesn't appear | Permissions not granted | Grant "use klaro ui" to anonymous/authenticated roles |
| Scripts load before consent | Automatic attribution disabled | Enable process_js_alter and process_page_attachments |
| Service doesn't appear on modal | Service not enabled | Edit service → check "Enabled" → save |
| CKEditor preview broken | Klaro processes preview HTML | Exclude `\\/media\\/.*\\/preview` pattern |
| Unknown scripts not blocked | Log unknown resources disabled | Enable log_unknown → review logs → create services |
| Modal shows wrong language | Translation missing | Add translation for user's language |
| Third-party cookies not deleted | Cookies on different domain | Impossible to delete; block scripts instead |

## Pattern

**Diagnostic Steps**:

```yaml
# Step 1: Verify library installed
# Check /libraries/klaro/ or vendor/klaro-org/klaro-js/ exists

# Step 2: Verify permissions
# Navigate to /admin/people/permissions
# Grant "use klaro ui" to all roles including anonymous

# Step 3: Check service enabled
# Navigate to /admin/config/user-interface/klaro/services
# Ensure "Enabled" checkbox is checked

# Step 4: Enable logging
advanced:
  log_unknown: true
# Review /admin/reports/dblog for "klaro" entries

# Step 5: Test automatic attribution
automatic_attribution:
  process_js_alter: true
  process_page_attachments: true
  log_unknown: true
# Clear cache and test

# Step 6: Verify script blocking
# Open browser DevTools → Network tab
# Scripts should show "blocked by Klaro" before consent
```

**Common Issue: GTM Scripts Load Before Consent**:
```yaml
# Problem: Google Tag Manager fires before consent
# Cause: GTM loaded outside Klaro control
# Solution: Configure GTM as service
service:
  name: google_tag_manager
  sources:
    - "https://www.googletagmanager.com/gtag/js"
    - "https://www.googletagmanager.com/gtm.js"
  callback: |
    if (consent) {
      dataLayer.push({'event': 'consent_given'});
    }
```

**Common Issue: Modal Doesn't Display**:
```bash
# Check Klaro JS library loaded
curl -I https://yoursite.com/libraries/klaro/klaro.js

# Verify console for errors
# Browser DevTools → Console → look for Klaro errors

# Check consent mode configured
# Navigate to /admin/config/user-interface/klaro
# Ensure mode is NOT "Silent" unless intentional
```

**Reference**: `/admin/reports/dblog` for Klaro log entries

## Common Mistakes

- **Wrong**: Not clearing cache after configuration changes → **Right**: Old config persists; clear Drupal cache
- **Wrong**: Testing with browser cache enabled → **Right**: Stale scripts load; test in incognito/private mode
- **Wrong**: Assuming all scripts auto-detected → **Right**: Some dynamic scripts evade detection; check logs
- **Wrong**: Disabling services but expecting them to block → **Right**: Disabled services don't appear or block; re-enable
- **Wrong**: Not checking browser console → **Right**: JavaScript errors break Klaro; always check console
- **Wrong**: Forgetting to test anonymous users → **Right**: Different permissions than authenticated; test both
- **Wrong**: Not reviewing watchdog logs → **Right**: Unknown resources logged but ignored; check /admin/reports/dblog

## See Also

- [URL Pattern Exclusions](url-pattern-exclusions.md)
- [Automatic Resource Attribution](automatic-resource-attribution.md)
- Reference: [Klaro Module Issue Queue](https://www.drupal.org/project/issues/klaro)
