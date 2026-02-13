---
description: Install Klaro module and klaro-js library via Composer or manual methods
drupal_version: "11.x"
---

# Installation Methods

## When to Use

> Install Klaro module and klaro-js JavaScript library before configuration. Choose installation method based on your Drupal project's dependency management approach.

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
# - drupal/klaro (module)
# - drupal/klaro_js (library wrapper)
# - klaro-org/klaro-js (JavaScript library)

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

## See Also

- [Service Configuration](service-configuration.md)
- Reference: [Klaro Module Project Page](https://www.drupal.org/project/klaro)
- Security: [Klaro XSS Vulnerability (fixed in 3.0.5)](https://github.com/klaro-org/klaro-js/releases/tag/v3.0.5)
