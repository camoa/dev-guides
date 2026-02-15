---
description: Decision framework for when to abstract vs duplicate in Drupal, with security, performance, testing, and development standards considerations.
---

# Best Practices Decision Framework

## When to Use

When making any decision about abstracting, reusing, or duplicating code in Drupal.

## Decision Framework

```
+---------------------------------------------+
| Is it configuration or code?                |
+-------------+-------------------------------+
              |
    +---------+----------+
    |                    |
    v                    v
Configuration        Code Logic
    |                    |
    v                    v
Use config entity    Is it used in
or config file       multiple places?
    |                    |
    |            +-------+--------+
    |            |                 |
    |            v                 v
    |         No (1-2)          Yes (3+)
    |            |                 |
    |            v                 v
    |      Keep in class    Extract to service,
    |      (don't abstract  base class, trait,
    |       prematurely)    or plugin
    |                            |
    v                            v
Export, version             Apply Rule of Three
control, deploy             (wait for 3rd use)
```

## Security Considerations

| Practice | Security Impact |
|----------|----------------|
| Config as single source of truth | Reduces XSS risk (config is sanitized), ensures consistent validation |
| Services instead of static calls | Easier to audit dependencies, better access control |
| Avoiding duplicate validation logic | One validation rule = one place to secure properly |
| Template inheritance | Reduces XSS risk by reusing secured parent templates |
| Render arrays over raw HTML | Automatic XSS protection, consistent sanitization |

**Critical Security Anti-Pattern**: Duplicating validation or sanitization logic across multiple places creates security vulnerabilities. One copy gets patched, others don't.

## Performance Considerations

| Practice | Performance Impact |
|----------|-------------------|
| Config caching | Config reads are cached by default; reusing config is fast |
| Service instantiation | Services are singletons; reusing services is free |
| Render array caching | Structured render arrays support granular cache tags/contexts |
| Template inheritance | Minimal overhead; Twig compiles templates to PHP |
| Over-abstraction | Excessive layers of abstraction add function call overhead |

**Performance Anti-Pattern**: God services with 20+ methods often load more dependencies than needed, slowing instantiation.

## Development Standards

| Standard | DRY Application |
|----------|----------------|
| Dependency injection over static calls | Reuse container-managed services, don't duplicate `\Drupal::` calls |
| Configuration over code | Don't duplicate site settings in code |
| Services over utility classes | Testable, injectable, reusable |
| Traits for cross-cutting concerns | Reuse translation, logging, messaging patterns |
| Plugin system for extensibility | Reuse plugin scaffolding instead of custom discovery |

## Testing Implications

| Practice | Testing Benefit |
|----------|----------------|
| Services with DI | Easy to mock dependencies, unit-testable |
| Config as single source | Test config export/import, not hardcoded values |
| Shared base classes | Test base class once, subclasses inherit tests |
| Thin controllers/commands | Business logic in services is easier to test |

## Decision Table

| Scenario | Decision | Reasoning |
|----------|----------|-----------|
| Need site name in 5 places | Read from `system.site` config | Single source of truth |
| Same validation in 3 forms | Extract to service method | Rule of Three, reusable |
| Similar blocks with shared config | Create base block class | Inherit common patterns |
| Translation needed in service | Use `StringTranslationTrait` | Standard Drupal pattern |
| API call from web and CLI | Service called by controller and Drush | Reuse business logic |
| Override one section of template | `{% extends %}` parent template | DRY markup structure |
| Reusable UI component | SDC with props/slots | Design system consistency |

## See Also

- [Over-DRY Anti-Patterns](over-dry-anti-patterns.md)
- [Code Reference Map](code-reference-map.md)
- Reference: [Best practices for developers | Drupal API](https://api.drupal.org/api/drupal/core!core.api.php/group/best_practices/11.x)
- Reference: `dev-dry-principles.md` section on Best Practices Decision Framework
