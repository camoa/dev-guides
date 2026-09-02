---
description: "Source references and maintenance manifest for the services guides — web sources, code sources, and version history"
---

# Sources & Maintenance

## Drupal Research Install
Claims here were checked against a local Drupal install of core and the modules named below, rather than quoted from documentation.
## Web Sources

| Source | URL | Guide Sections | Last Verified |
|--------|-----|----------------|---------------|
| Services and dependency injection in Drupal | https://www.drupal.org/docs/drupal-apis/services-and-dependency-injection/services-and-dependency-injection-in-drupal | 1.0, 2.0, 5.0 | 2026-02-14 |
| Structure of a service file | https://www.drupal.org/docs/drupal-apis/services-and-dependency-injection/structure-of-a-service-file | 3.0, 4.0 | 2026-02-14 |
| Service Tags | https://www.drupal.org/docs/drupal-apis/services-and-dependency-injection/service-tags | 10.0 | 2026-02-14 |
| Dependency Injection in a form | https://www.drupal.org/docs/drupal-apis/services-and-dependency-injection/dependency-injection-in-a-form | 7.0 | 2026-02-14 |
| Dependency injection in Plugin (Block) | https://www.drupal.org/docs/drupal-apis/services-and-dependency-injection/dependency-injection-in-plugin-block | 8.0 | 2026-02-14 |
| Altering existing services, providing dynamic services | https://www.drupal.org/docs/drupal-apis/services-and-dependency-injection/altering-existing-services-providing-dynamic-services | 13.0 | 2026-02-14 |
| Subscribe to and dispatch events | https://www.drupal.org/docs/develop/creating-modules/subscribe-to-and-dispatch-events | 12.0 | 2026-02-14 |
| Concept: Services and the Container (Drupalize.me) | https://drupalize.me/tutorial/concept-services-and-container | 2.0 | 2026-02-14 |
| Concept: Dependency Injection (Drupalize.me) | https://drupalize.me/tutorial/concept-dependency-injection | 7.0, 18.0 | 2026-02-14 |
| AutowireTrait allows ContainerInjectionInterface classes to be autowired | https://www.drupal.org/node/3396179 | 6.0, 7.0 | 2026-02-14 |
| Services can be autowired | https://www.drupal.org/node/3218156 | 6.0 | 2026-02-14 |
| Services can now use tagged iterators | https://www.drupal.org/node/3436859 | 11.0 | 2026-02-14 |
| Mastering Dependency Injection in Drupal (TheDropTimes) | https://www.thedroptimes.com/54436/mastering-dependency-injection-in-drupal-best-practices-and-real-world-examples | 18.0 | 2026-02-14 |
| Dependency injection anti-patterns in Drupal (mglaman.dev) | https://mglaman.dev/blog/dependency-injection-anti-patterns-drupal | 9.0, 19.0 | 2026-02-14 |
| Drupal Service Container Deep Dive Part 1 (SparkFabrik) | https://tech.sparkfabrik.com/en/blog/drupal-service-container-deep-dive-part-1/ | 13.0, 14.0 | 2026-02-14 |
| Drupal Service Container Deep Dive Part 3: Service Collectors (SparkFabrik) | https://tech.sparkfabrik.com/en/blog/drupal-service-container-deep-dive-part-3/ | 11.0 | 2026-02-14 |
| Practical Use Cases of Tagged Services in Drupal | https://drupal.com.ua/135/practical-use-cases-tagged-services-drupal | 11.0 | 2026-02-14 |
| Events (Drupal at your Fingertips) | https://www.drupalatyourfingertips.com/events | 12.0 | 2026-02-14 |
| Services (Drupal at your Fingertips) | https://www.drupalatyourfingertips.com/services | 1.0 | 2026-02-14 |
| Overriding services in Drupal 8 - advanced cases (PreviousNext) | https://www.previousnext.com.au/blog/overriding-services-drupal-8-advanced-cases | 13.0 | 2026-02-14 |
| Deep Dive into Drupal's Service Container (TheDropTimes) | https://www.thedroptimes.com/55750/deep-dive-drupals-service-container-tags-compiler-passes-providers-and-autoconfiguration | 13.0 | 2026-02-14 |
| Event Subscriber, Services, and Dependency Injection in Drupal 10 (Medium) | https://medium.com/@tikna/event-subscriber-services-and-dependency-injection-in-drupal-10-1ce306008105 | 12.0 | 2026-02-14 |

## Code Sources

| Module | Relative Path | Guide Sections | Drupal Version |
|--------|---------------|----------------|----------------|
| Core | `core/` | All sections | 11.3.3 |
| Core DI | `core/lib/Drupal/Core/DependencyInjection/` | 2.0, 6.0, 7.0, 13.0, 14.0, 17.0, 21.0 | 11.3.3 |
| Core services | `core/core.services.yml` | 3.0, 4.0, 10.0, 15.0 | 11.3.3 |
| Drupal static helper | `core/lib/Drupal.php` | 9.0 | 11.3.3 |
| System module | `core/modules/system/` | 4.0, 21.0 | 11.3.3 |
| Node module | `core/modules/node/` | 21.0 | 11.3.3 |
| User module | `core/modules/user/` | 21.0 | 11.3.3 |
| Logger | `core/lib/Drupal/Core/Logger/` | 15.0, 16.0 | 11.3.3 |
| Plugin | `core/lib/Drupal/Core/Plugin/` | 8.0 | 11.3.3 |
| Compiler passes | `core/lib/Drupal/Core/DependencyInjection/Compiler/` | 14.0 | 11.3.3 |
| CoreServiceProvider | `core/lib/Drupal/Core/CoreServiceProvider.php` | 14.0, 21.0 | 11.3.3 |

---

**Guide Metadata**:
- **Created**: 2026-02-14
- **Total Sections**: 21 (excluding manifest)
- **Total Lines**: ~2,900
- **Philosophy**: Services ARE configuration — YAML first, code second
- **Target Audience**: Drupal developers learning or mastering dependency injection
- **Prerequisites**: Understanding of OOP, PHP namespaces, YAML syntax
<!-- END PARTITION: sources-maintenance -->
