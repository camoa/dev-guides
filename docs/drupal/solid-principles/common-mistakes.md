---
description: Common SOLID violations in Drupal development with real impact explanations
drupal_version: "11.x"
---

# SOLID Violations - Common Mistakes

## When to Use

Recognize these patterns as SOLID violations. Understanding WHY they're bad helps you avoid them and spot them in code review.

## Anti-Patterns

**Violating SRP**

| Anti-pattern | Fix | WHY it matters |
|---|---|---|
| 1000-line "Manager" service doing everything | Split into focused services | Unmaintainable; one change breaks 10 features; impossible to test |
| Controller with business logic, validation, email, logging | Extract to services | Can't reuse in CLI, API, batch jobs |
| Form with complex business logic in submitForm() | Delegate to service | Can't trigger business logic outside form context |
| All hooks in one Hooks.php class | Split by domain (EntityHooks, FormHooks) | 50 hooks in one file is unmaintainable |

**Violating OCP**

| Anti-pattern | Fix | WHY it matters |
|---|---|---|
| Patching core/contrib code | Use plugins, hooks, events | Patches break on updates, lost on reinstall |
| Editing core config YAML files | Use config overrides | Exports overwrite changes; not version-controlled |
| Copying and modifying core functions | Use hooks to alter behavior | Duplicate code breaks when core updates |

**Violating LSP**

| Anti-pattern | Fix | WHY it matters |
|---|---|---|
| Extending ConfigFormBase but not using config | Extend FormBase | Violates ConfigFormBase contract, breaks config validation |
| Not calling parent::submitForm() in form overrides | Always call parent | Breaks cache clearing, hooks, redirects |
| Returning boolean from access hooks | Return AccessResult | Loses cacheability metadata, causes access bugs |
| Assuming all entities have 'title' field | Check hasField('title') | Custom entities may not; causes fatal errors |

**Violating ISP**

| Anti-pattern | Fix | WHY it matters |
|---|---|---|
| Implementing EntityOwnerInterface with fake getOwner() | Don't implement if no owner | Breaks ownership system, confuses developers |
| Creating one giant interface with 50 methods | Split into role interfaces | Forces fake implementations, bloats classes |
| Not using traits when implementing interfaces | Use EntityOwnerTrait, etc. | Reinventing wheel; trait is tested, maintained |

**Violating DIP**

| Anti-pattern | Fix | WHY it matters |
|---|---|---|
| `\Drupal::service()` static calls in classes | Constructor injection | Untestable; can't mock; hides dependencies |
| Type-hinting concrete classes | Type-hint interfaces | Tight coupling; can't swap implementation |
| `new ClassName()` in services | Inject or use factory | Can't inject dependencies into created object |
| No service aliases for interfaces | Add Interface: '@service' | Autowiring can't resolve interface |
| Using `\Drupal::database()` instead of entity API | Use entity storage | Bypasses access control, caching, hooks |

## WHY These Matter - Real Impact

**SRP Violations:**

- **God classes** -- 1000-line services are impossible to understand, test, or change without breaking something
- **Fat controllers** -- Business logic trapped in HTTP context; can't use in drush commands, cron, migrations
- **Mixed concerns** -- Email sending in entity save hook; now can't save without sending email

**OCP Violations:**

- **Core patches** -- Update overwrites patch; security update = site broken; debugging nightmare
- **Modified config files** -- Config export deletes changes; no version control; impossible to track

**LSP Violations:**

- **Wrong base class** -- ConfigFormBase expects config operations; using State API breaks validation
- **Missing parent calls** -- Form cache never cleared; form appears on wrong page; mysterious bugs
- **Boolean access returns** -- User A's content cached for user B; critical security hole

**ISP Violations:**

- **Fake implementations** -- getOwner() throws exception; breaks Views, access control, ownership queries
- **Fat interfaces** -- Implementing 50 methods with 45 returning NULL; dead code everywhere

**DIP Violations:**

- **Static calls** -- Can't unit test; mocking impossible; coupled to Drupal bootstrap
- **Concrete type-hints** -- Can't use service decorators; can't swap to mock implementation
- **No service definitions** -- Container can't manage lifecycle; no autowiring; manual instantiation

## See Also

- [Best Practices Checklist](best-practices-checklist.md) for what to do
- Reference: [Drupal API Best Practices](https://api.drupal.org/api/drupal/core!core.api.php/group/best_practices/11.x)
