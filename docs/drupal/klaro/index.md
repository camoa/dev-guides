---
description: Klaro Cookie & Consent Management — GDPR-compliant consent for Drupal sites
guide-meta:
  concepts:
    - Klaro module
    - cookie consent
    - GDPR compliance
    - ePrivacy
    - consent modes
    - service configuration
    - automatic resource attribution
  not:
    - EU Cookie Compliance module
    - CookieBot
  requires: []
  complements:
    - drupal/security
    - drupal/seo-geo
  category: drupal
tracks:
  - project: klaro
    channel: stable
    declared: "3.1.1"
    note: module version 3.1.1 now stated in Installation Methods prose, distinct from the 3.0.5+ klaro-js JavaScript library version
    verified: 2026-08-16
---

# Klaro Cookie & Consent Management

| I need to... | Guide | Summary |
|-------------|-------|---------|
| Understand what consent management is and when to use it | [What is Consent Management](what-is-consent-management.md) | Use consent management when your Drupal site loads external resources (scripts, iframes, images) that may collect visitor data or set cookies. Required for GDPR, ePrivacy Directive, and similar privacy regulations. |
| Ensure GDPR and ePrivacy compliance | [Legal Compliance Requirements](legal-compliance-requirements.md) | Understand legal requirements before implementing consent management to ensure your configuration meets regulatory standards for GDPR, ePrivacy Directive, and other privacy laws. |
| Choose between Silent, Notice, or Modal consent modes | [Consent Mode Selection](consent-mode-selection.md) | Choose consent mode based on your site's regulatory requirements and user experience priorities. Configure at **Administration > Configuration > User interface > Klaro! |
| Install Klaro module and library | [Installation Methods](installation-methods.md) | Install Klaro module (current stable: 3.1.1) and klaro-js JavaScript library — two independently versioned lines — before configuration. Choose installation method based on your Drupal project's dependency management approach. |
| Configure third-party services (analytics, tracking) | [Service Configuration](service-configuration.md) | Configure a service when you need to control external resources (scripts, iframes, images) that collect data or set cookies. Each third-party integration requires a service definition. |
| Group services by category (purposes) | [Purpose Management](purpose-management.md) | Create purposes to group related services into categories. Purposes appear as sections in the consent modal and allow users to enable/disable entire groups at once. |
| Set cookie expiration and domain scope | [Storage Settings](storage-settings.md) | Configure how Klaro stores user consent decisions. Storage method and duration affect user experience, browser compatibility, and compliance requirements. |
| Customize colors, positioning, and branding | [Styling and UI Customization](styling-and-ui-customization.md) | Customize Klaro's appearance to match your site's branding, position elements, and control HTML rendering in descriptions. |
| Translate consent UI for multi-language sites | [Translation and Localization](translation-and-localization.md) | Translate Klaro's consent interface for multi-language Drupal sites. Requires Configuration Translation module enabled. |
| Automatically block external scripts before consent | [Automatic Resource Attribution](automatic-resource-attribution.md) | Enable automatic detection and blocking of external resources without manually adding HTML attributes. Critical for preventing pre-consent tracking. |
| Add privacy settings link to menu | [Menu Integration](menu-integration.md) | Provide users a way to modify consent preferences after initial decision. GDPR requires the ability to withdraw consent at any time. |
| Exclude admin pages or previews from consent manager | [URL Pattern Exclusions](url-pattern-exclusions.md) | Disable Klaro on specific URL patterns where consent management isn't needed (admin pages, previews) or interferes with functionality. |
| Fix consent modal or script blocking issues | [Troubleshooting](troubleshooting.md) | Diagnose and resolve common Klaro configuration issues, script blocking failures, and modal rendering problems. |
| Prevent XSS vulnerabilities and secure configuration | [Security Best Practices](security-best-practices.md) | Secure Klaro configuration to prevent XSS vulnerabilities, injection attacks, and unauthorized consent manipulation. |
| Optimize for page load performance | [Performance Optimization](performance-optimization.md) | Optimize Klaro for fast page load times, minimal render blocking, and efficient resource management. |
| Extend Klaro with custom code or event subscribers | [Development Standards](development-standards.md) | Follow Drupal and Klaro development best practices when extending, theming, or integrating Klaro into custom code. |
