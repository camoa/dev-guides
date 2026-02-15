---
description: Structure a Drupal module following SOLID principles - directory layout and organization
drupal_version: "11.x"
---

# SOLID Module Architecture

## When to Use

Structure your custom module following SOLID principles. This section shows recommended directory layout and organization patterns.

## Pattern

**GOOD: SOLID-compliant module structure**

```
mymodule/
├── mymodule.info.yml
├── mymodule.services.yml          # Service definitions (DIP)
├── src/
│   ├── Controller/
│   │   └── ArticleController.php  # Thin controllers (SRP)
│   ├── Form/
│   │   ├── SettingsForm.php       # Config forms (LSP)
│   │   └── ArticleForm.php
│   ├── Plugin/                     # Extension via plugins (OCP)
│   │   ├── Block/
│   │   │   └── ArticleBlock.php
│   │   └── Field/
│   │       └── FieldFormatter/
│   ├── Service/                    # Business logic services (SRP)
│   │   ├── ArticleManagerInterface.php  # Depend on interface (DIP, ISP)
│   │   ├── ArticleManager.php
│   │   ├── ArticlePublisherInterface.php
│   │   └── ArticlePublisher.php
│   ├── Hook/                       # Drupal 11+ OOP hooks (SRP)
│   │   ├── ArticleEntityHooks.php
│   │   └── ArticleFormHooks.php
│   ├── EventSubscriber/            # Event-based extension (OCP)
│   │   └── ArticleRouteSubscriber.php
│   └── Entity/
│       └── Article.php             # Entity following contracts (LSP)
└── tests/
    └── src/
        └── Unit/
            └── Service/
                └── ArticleManagerTest.php  # Unit test services
```

## Decision

| Module element | SOLID principle | Pattern |
|---|---|---|
| Services | SRP, DIP | One responsibility per service, inject dependencies |
| Controllers | SRP | Thin, delegate to services |
| Plugins | OCP | Extend systems without modification |
| Hook classes | SRP, OCP | Organized by domain, extend behavior |
| Forms | LSP | Extend correct base class |
| Entities | LSP, ISP | Honor contracts, implement only needed interfaces |
| Interfaces | ISP, DIP | Role-specific, type-hint in constructors |

## Common Mistakes

- Putting all code in .module file -- extract to classes. **WHY:** .module always loads; classes autoload on demand (performance, organization)
- No service layer -- controllers do everything -- extract business logic to services. **WHY:** Controllers are HTTP-specific; can't reuse in CLI, batch, API
- Not defining services in services.yml -- define all services. **WHY:** Direct instantiation prevents DI, testing, decoration
- No interfaces for services -- create interfaces for all services. **WHY:** Can't use service decorators, can't swap implementations, tight coupling
- Hook classes mixed with other classes -- separate Hook namespace. **WHY:** Clear organization, PSR-4 autoloading, easier to find
- No unit tests -- test services in isolation. **WHY:** Integration tests are slow, fragile; unit tests are fast, reliable

## See Also

- Reference: [Drupal Module Development](https://www.zend.com/blog/drupal-module-development)
