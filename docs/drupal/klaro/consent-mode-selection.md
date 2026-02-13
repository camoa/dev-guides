---
description: Choose between Silent, Notice, or Modal consent modes based on regulatory requirements
drupal_version: "11.x"
---

# Consent Mode Selection

## When to Use

> Choose consent mode based on your site's regulatory requirements and user experience priorities. Configure at **Administration > Configuration > User interface > Klaro! > General** (Consent section).

## Decision

| If you need... | Use... | Why |
|---|---|---|
| No visible notice (minimal friction) | Silent mode | Blocks external resources but shows no dialog |
| Informational notice allowing page use | Notice dialog | Non-modal notice visible while site usable |
| Force acknowledgment before site access | Notice dialog as modal | Modal blocks interaction until dismissed |
| Granular service choices required | Consent dialog modal | Full service list; blocks site until decision |
| Post-decision preference changes | Toggle button (any mode) | Floating button to reopen consent dialog |

## Pattern

**Silent Mode** (default, minimal intervention):
```yaml
consent_mode: silent
toggle_button: true  # Users can still access dialog via button
# Result: No dialog shown, external resources blocked with placeholders
```

**Notice Dialog** (informational approach):
```yaml
consent_mode: notice_dialog
toggle_button: true
accept_all_notice: false  # Only accept required services on quick accept
# Result: Non-modal notice; users can browse while visible
```

**Modal Consent** (GDPR-compliant strict approach):
```yaml
consent_mode: consent_dialog_modal
toggle_button: true
buttons:
  accept_all: true
  decline_all: true  # Equal prominence required for GDPR
  close_button: true  # Mandatory in some jurisdictions
# Result: Full service list in modal; site blocked until decision
```

**Reference**: `/admin/config/user-interface/klaro` configuration page

## Common Mistakes

- **Wrong**: Using Silent mode for sites requiring explicit consent → **Right**: Upgrade to Notice/Modal mode for GDPR compliance
- **Wrong**: Omitting toggle button → **Right**: Users have no way to modify preferences later; violates GDPR withdrawal right
- **Wrong**: Accepting all services in Notice mode → **Right**: Set `accept_all_notice: false` to only enable required services
- **Wrong**: No decline button in consent modal → **Right**: Dark pattern violation; always include equal-prominence decline option
- **Wrong**: Forgetting close button → **Right**: Mandatory in some EU countries; configure `close_button: true`

## See Also

- [Legal Compliance Requirements](legal-compliance-requirements.md)
- [Service Configuration](service-configuration.md)
- Reference: [Klaro Mode Configuration](https://www.drupal.org/docs/extending-drupal/contributed-modules/contributed-module-documentation/klaro-cookie-consent-management)
