---
description: Install Klaro module (3.1.1) and klaro-js library via Composer or manual methods
tldr: "Install Klaro module (current stable: 3.1.1) and klaro-js JavaScript library — two independently versioned lines — before configuration. Choose installation method based on your Drupal project's dependency management approach."
drupal_version: "11.x"
---

# Installation Methods

## When to Use

> Install the Klaro module (current stable: 3.1.1) and the klaro-js JavaScript library it depends on before configuration. These are two separate version lines — the Drupal module and the upstream JS library — tracked independently; see Security Best Practices for the library's version requirement. Choose installation method based on your Drupal project's dependency management approach.

## Decision

| If your project uses... | Use... | Why |
|---|---|---|
| Composer (standard Drupal) | `composer require drupal/klaro` | Automatic dependency resolution; klaro-js installs automatically |
| Composer with SBOM tracking | Root composer.json repository definition | Tracks klaro-js in Software Bill of Materials |
| composer-merge-plugin | composer.libraries.json merge | Legacy approach for library dependencies |
| No Composer | Manual download | Not recommended; manual updates required |

## Pattern

**Recommended (Composer)**:
```bash
composer require drupal/klaro
# Automatically installs:
# - drupal/klaro (module) — current stable: 3.1.1
# - drupal/klaro_js (library wrapper)
# - klaro-org/klaro-js (JavaScript library — a separate version line; see Security Best Practices)

# Enable module
drush en klaro

# Grant permissions
drush role:perm:add anonymous 'use klaro ui'
drush role:perm:add authenticated 'use klaro ui'
```

**SBOM Tracking (root composer.json)**:
```json
{
  "repositories": {
    "klaro-org.klaro-js": {
      "type": "package",
      "package": {
        "name": "klaro-org/klaro-js",
        "type": "drupal-library",
        "version": "0.7.22",
        "dist": {
          "url": "https://github.com/klaro-org/klaro-js/archive/refs/tags/v0.7.22.zip",
          "type": "zip"
        }
      }
    }
  }
}
```

**Reference**: `/modules/contrib/klaro/composer.json` for dependency definitions

## Common Mistakes

- **Wrong**: Manual library installation → **Right**: Composer handles this automatically; avoid manual library folder management
- **Wrong**: Skipping permission grants → **Right**: Anonymous users won't see consent dialog; grant "use klaro ui" to all roles
- **Wrong**: Not whitelisting drupal/klaro_js in repo.packagist.org → **Right**: May block installation; add to allowed packages
- **Wrong**: Using outdated klaro-js version → **Right**: Security vulnerability in versions <3.0.5 (XSS risk); update to 3.0.5+
- **Wrong**: Enabling module before library installed → **Right**: Module will report missing library; verify library presence first
- **Wrong**: Conflating the module version with the library version → **Right**: `drupal/klaro` (currently 3.1.1) and `klaro-org/klaro-js` (currently 3.0.5+) version independently; check each separately when auditing for updates

## See Also

- [Service Configuration](service-configuration.md)
- Reference: [Klaro Module Project Page](https://www.drupal.org/project/klaro)
- Security: [Klaro XSS Vulnerability (fixed in 3.0.5)](https://github.com/klaro-org/klaro-js/releases/tag/v3.0.5)
