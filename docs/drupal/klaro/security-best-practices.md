---
description: Prevent XSS vulnerabilities and secure consent configuration
drupal_version: "11.x"
---

# Security Best Practices

## When to Use

> Secure Klaro configuration to prevent XSS vulnerabilities, injection attacks, and unauthorized consent manipulation.

## Decision

| Security Risk | Mitigation | Why |
|---|---|---|
| XSS in service descriptions | Disable "Allow HTML" or sanitize | Untrusted HTML enables script injection |
| Outdated klaro-js library | Update to 3.0.5+ | Versions <3.0.5 vulnerable to XSS (CVE-2025) |
| User-provided callback code | Never allow user input in callbacks | Direct code execution risk |
| Third-party cookie deletion | Block scripts; don't delete cookies | Cannot delete cross-domain cookies |
| Consent cookie tampering | Use signed cookies (future enhancement) | Users can manually edit consent cookie |

## Pattern

**Secure Service Configuration**:

```yaml
# SECURE: No HTML in descriptions
service:
  description: "We use analytics. See our privacy policy at https://example.com/privacy"
  allow_html_in_texts: false  # Disabled by default

# RISKY: HTML enabled
service:
  description: '<a href="https://example.com">Privacy Policy</a>'
  allow_html_in_texts: true  # Enable ONLY if you control all content

# SECURE: Callback without user input
callback: |
  if (consent) {
    gtag('config', 'GA-MEASUREMENT-ID');
  }

# DANGEROUS: Never do this
# callback: user_provided_code  # Code injection risk
```

**Library Security Updates**:
```bash
# Check current version
composer show klaro-org/klaro-js

# Update to secure version (3.0.5+)
composer update klaro-org/klaro-js

# Verify security advisories
drush pm:security
```

**Prevent Cookie Manipulation** (defense in depth):
```yaml
# Use HTTPS only (prevents MITM attacks on consent cookie)
storage:
  cookie_name: klaro
  # Browser enforces SameSite=Lax by default

# Monitor consent changes server-side
# Log consent decisions for audit trail
```

**Reference**: [Klaro Security Advisory (May 2025)](https://github.com/klaro-org/klaro-js/security/advisories)

## Common Mistakes

- **Wrong**: Enabling "Allow HTML" without content review → **Right**: XSS risk; only enable if you control all service descriptions
- **Wrong**: Using klaro-js <3.0.5 → **Right**: Known XSS vulnerability; update immediately
- **Wrong**: Trusting user consent cookie → **Right**: Users can edit; validate server-side when critical
- **Wrong**: Attempting to delete third-party cookies → **Right**: Impossible; block scripts instead
- **Wrong**: Not reviewing callback code → **Right**: Malicious code execution; audit all callbacks
- **Wrong**: Allowing service configuration by untrusted users → **Right**: Privilege escalation; restrict to admins only
- **Wrong**: Not monitoring security advisories → **Right**: Miss critical updates; subscribe to Klaro security notifications

## See Also

- Reference: [Klaro Releases](https://github.com/klaro-org/klaro-js/releases)
- Security: [OWASP XSS Prevention](https://owasp.org/www-community/attacks/xss/)
