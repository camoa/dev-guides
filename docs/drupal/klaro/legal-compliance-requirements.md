---
description: GDPR, ePrivacy, and legal requirements for consent management configuration
drupal_version: "11.x"
---

# Legal Compliance Requirements

## When to Use

> Understand legal requirements before implementing consent management to ensure your configuration meets regulatory standards for GDPR, ePrivacy Directive, and other privacy laws.

## Decision

| Regulation | Requirement | Klaro Implementation |
|---|---|---|
| GDPR Article 7 | Freely given, specific, informed consent | Notice/Modal mode with granular services |
| ePrivacy Directive Article 5(3) | Prior consent before storing data in browser | Block scripts/cookies until consent received |
| GDPR Article 21 | Right to withdraw consent | Toggle button or menu link to reopen dialog |
| GDPR Article 13 | Transparency about data processing | Service descriptions with privacy policy URLs |

## Pattern

**Legal Compliance Checklist**:

```yaml
# Minimum compliant configuration
consent_mode: notice_dialog_modal  # Force decision before site use (for GDPR)
services:
  - name: analytics
    required: false  # Optional services must allow rejection
    toggled_by_default: false  # No pre-selected consent
    privacy_policy_url: required  # Transparency requirement
    description: specific  # Purpose must be clear
buttons:
  decline_all: true  # Equal prominence with accept
  close_button: true  # Mandatory in some jurisdictions
storage:
  expires_days: 365  # Max 12-24 months recommended
```

**Reference**: [GDPR Consent Management Requirements (2026)](https://secureprivacy.ai/blog/gdpr-consent-management)

## Common Mistakes

- **Wrong**: Pre-selecting consent checkboxes → **Right**: Violates GDPR "freely given" requirement; €150M SHEIN fine in 2025
- **Wrong**: Making rejection harder than acceptance (dark patterns) → **Right**: Fines averaging €4.9M; use equal button prominence
- **Wrong**: Setting cookies before consent obtained → **Right**: ICO warned 134 UK websites in 2025; ensure script blocking works
- **Wrong**: Auto-accepting after timeout or on scroll → **Right**: Violates "unambiguous" consent requirement
- **Wrong**: Generic "accept all" without granular choices → **Right**: GDPR requires separate consent per purpose
- **Wrong**: No way to withdraw consent → **Right**: Violate Article 21; always include toggle button or menu link
- **Wrong**: Missing privacy policy links → **Right**: Fails transparency requirements; mandatory per GDPR Article 13

## See Also

- [Consent Mode Selection](consent-mode-selection.md)
- Reference: [GDPR Dark Pattern Avoidance 2026](https://secureprivacy.ai/blog/dark-pattern-avoidance-2026-checklist)
