---
description: "Source references and maintenance manifest for the sdc guides — web sources, code sources, and version history"
---

# Sources & Maintenance

## Research Sources

**Official Drupal Documentation:**
- [Using Single-Directory Components](https://www.drupal.org/docs/develop/theming-drupal/using-single-directory-components) - Official guide
- [Props and Slots Documentation](https://www.drupal.org/docs/develop/theming-drupal/using-single-directory-components/what-are-props-and-slots-in-drupal-sdc-theming) - Props vs slots explained
- [Component.yml Reference](https://www.drupal.org/docs/develop/theming-drupal/using-single-directory-components/annotated-example-componentyml) - Schema documentation
- [FAQ](https://www.drupal.org/docs/develop/theming-drupal/using-single-directory-components/frequently-asked-questions) - Common questions

**Community Resources:**
- [Drupal at your Fingertips (Selwyn Polit)](https://www.drupalatyourfingertips.com/) - Comprehensive Drupal reference (formerly d9book at github.com/selwynpolit/d9book)
- [Drupalize.me SDC Anatomy](https://drupalize.me/tutorial/anatomy-drupal-single-directory-component-sdc) - Component structure
- [Understanding Props and Slots](https://drupalize.me/tutorial/understanding-props-and-slots-drupal-single-directory-components) - Architectural patterns
- [Component Variants Update](https://www.thedroptimes.com/49944/drupal-core-single-directory-components-introduce-component-variants) - New variants API
- [Lullabot SDC Article](https://www.lullabot.com/articles/getting-single-directory-components-drupal-core) - Production patterns

**Security Advisories:**
- [SA-CORE-2025-001](https://www.drupal.org/sa-core-2025-001) - Critical XSS vulnerability
- [SA-CORE-2025-004](https://www.drupal.org/sa-core-2025-004) - XSS in Link field
- [Writing Secure Code](https://www.drupal.org/docs/administering-a-drupal-site/security-in-drupal/writing-secure-code-for-drupal) - Security best practices

**Performance Resources:**
- [Drupal Caching Overview](https://www.drupal.org/docs/7/managing-site-performance-and-scalability/caching-to-improve-performance/caching-overview) - Caching strategies
- [QED42 Caching Guide](https://www.qed42.com/insights/drupal-caching-best-practices-and-performance-monitoring) - Best practices
- [Drupal 11 Performance](https://www.acquia.com/blog/the-power-of-drupal) - New features

**Framework Documentation:**
- [Bootstrap 5 Documentation](https://getbootstrap.com/docs/5.3/) - Radix foundation
- [Twig Documentation](https://twig.symfony.com/doc/3.x/) - Template syntax
- [JSON Schema](https://json-schema.org/) - Schema specification

## Code Reference Locations

**Drupal Core Examples:**
- `/core/themes/olivero/components/teaser/` - Complete teaser component
- `/core/modules/system/tests/modules/sdc_test/components/` - Test components
- `/core/modules/navigation/components/` - Navigation module components
- `/core/lib/Drupal/Core/Theme/ComponentPluginManager.php` - Discovery system
- `/core/lib/Drupal/Core/Template/Attribute.php` - Attribute class
- `/core/assets/schemas/v1/metadata.schema.json` - Official JSON Schema

**Radix Theme Examples:**
- `/themes/contrib/radix/components/button/` - Button component
- `/themes/contrib/radix/components/card/` - Card component with complex schema
- `/themes/contrib/radix/components/navbar/` - Navigation organism
- `/themes/contrib/radix/components/alert/` - Alert with slots and props

## Related Guides

**Within This Repository:**
- `design_system_radix_sdc_mapping_guide.md` - Radix implementation patterns
- `drupal_development_guide.md` - General Drupal development standards

**External Guides:**
- Companion guide covers Radix-specific SDC implementation
- Bootstrap mapping guide covers design token translation
- Design system recognition guide for identifying component patterns

## Maintenance Schedule

**Update Triggers:**
- Drupal core SDC API changes
- New security advisories related to components
- Bootstrap version updates in Radix
- New component integration modules (UI Patterns, SDC Display, etc.)
- Community best practice evolution

**Review Cadence:**
- Security advisories: Monitor drupal.org/security continuously
- Core API changes: Review after each minor Drupal release
- Best practices: Quarterly review of community resources
- Code examples: Validate against latest core/Radix code

**Last Comprehensive Review:** 2026-02-12

---
