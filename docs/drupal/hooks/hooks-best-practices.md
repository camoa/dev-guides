---
description: "Standards a senior reviewer applies to hook classes: injection, class shape, naming, security in alter hooks, and performance."
tldr: "Standards for writing or reviewing a hook class: constructor injection, class shape, naming, security in alter hooks, and production failure modes."
drupal_version: "11.x"
---

# Hooks Best Practices

## When to Use

> You are writing or reviewing a hook class and want the standards a senior reviewer applies: injection, class shape, naming, file placement, security in alter hooks, and the failure modes that only show up in production.

## Development standards

| Do | Not | Why |
|---|---|---|
| Inject through the constructor | `\Drupal::service()` inside a hook method | The class is already an autowired service. Static calls hide dependencies and block unit testing. `core/themes/olivero/src/Hook/OliveroPagePreprocessHooks.php` injects four services; `core/themes/claro/src/Hook/ClaroHooks.php` still uses `\Drupal::service()` in `pageAttachmentsAlter()` and is the shape to move away from |
| `final class` with `private readonly` promoted properties | Open class with public properties | `core/modules/system/src/Hook/PageAttachmentsHook.php` is `final` with `private readonly`. A hook class has no consumers that should extend it. Core also writes non-final classes with `protected readonly` (`NodeHelpHooks`); choose `final` unless you designed for extension |
| One method per hook, named for the hook: `entityPresave()`, `formAlter()`, `preprocessHtml()` | A generic `handle()` that switches on a string | The method name and the `Implements hook_X().` docblock are how a reader finds the implementation; the attribute alone is not searchable by hook name in an IDE symbol index |
| One class per concern: form hooks, entity hooks, theme hooks, requirements | One `MyModuleHooks` with forty methods | Core's node module ships fourteen hook classes. See https://camoa.github.io/dev-guides/drupal/solid-principles/hook-classes-srp/ |
| Helpers as private methods on the hook class or a service | Helpers left in `.module` | A live `.module` forces the procedural scan unless you stop it, and the plan to deprecate `.module` is open (issue 3481555). For themes the `.theme` file is already deprecated in 11.5.0 |
| Return types on every method (`void`, `array`, `?string`, `AccessResultInterface`) | Untyped methods | Core's converted hooks carry return types; `invokeAll()` merges array results with `NestedArray::mergeDeep()` and appends scalars, so a wrong return type corrupts the merged result silently |

## Security

- **Alter hooks run for every request and every user.** `hook_form_alter()`, `hook_entity_access()` alterations, and `hook_ENTITY_TYPE_access()` change behavior globally. Never set `#access = TRUE` or return `AccessResult::allowed()` from an alter or access hook without a condition that names the permission or ownership being granted. Patterns: https://camoa.github.io/dev-guides/drupal/security/accessresult-patterns/, https://camoa.github.io/dev-guides/drupal/security/entity-access-control/
- **`module:` grants your code another module's identity.** An implementation registered on behalf of `other_module` is what `invoke('other_module', $hook)` runs. Use it only to fill a hook the other module is expected to provide, never to override its behavior; that is what `#[ReorderHook]` and `#[RemoveHook]` are for.
- **`#[RemoveHook]` can remove a security control.** Removing another module's `entity_access` or `form_alter` implementation removes whatever that implementation enforced. Treat it like a core patch in review.
- **Install requirements run before the container exists.** `InstallRequirementsInterface::getRequirements()` is static and uninjected. Do not read user input or the request there.

## Performance

- **Discovery cost is at container build, not runtime.** `HookCollectorPass` parses every `.module`, `.inc`, `.install`, `.profile` of every module unless stopped. Set `skip_procedural_hook_scan` when a module is fully converted; see [Procedural Scan Performance](procedural-scan-performance.md).
- **A hook class is a service; its constructor runs whenever the container instantiates it.** Every injected dependency is built with it. Group hooks that fire on every page (`page_attachments`, `preprocess_html`) into a lean class, and keep entity-save hooks with their heavier dependencies in another.
- **`hook_preprocess_HOOK()` and cache metadata** belong to the render layer. Variables added in preprocess need their cacheability bubbled; see https://camoa.github.io/dev-guides/drupal/twig/preprocess-functions/ and https://camoa.github.io/dev-guides/drupal/caching/cache-metadata-trinity/.
- **`hasImplementations()` is cheap, `invokeAll()` is not.** Guard expensive branches with `hasImplementations('my_hook')` the way `core/modules/node/src/Hook/NodeRequirements.php` guards `node_grants`.

## Common Mistakes

- **Double execution.** A converted hook plus an unmarked procedural function both run on 11.1+. Symptoms: duplicated messages, doubled mail, `entity_presave` side effects applied twice. Fix: `#[LegacyHook]` on the function or delete it.
- **Double requirements on 11.2.** `#[LegacyRequirementsHook]` is not recognized in 11.2, so a module supporting 11.2 that ships both `hook_requirements()` and `hook_runtime_requirements()` reports every requirement twice on that version. The doubling lasts only while the module also supports cores below 11.2 and so must keep `hook_requirements()`; accept it for that window, or raise the minimum to 11.2 and delete `hook_requirements()`.
- **Ordering by module weight.** Changing `system.schema` weights to move one hook moves every hook the module implements. Use `order:` on the one implementation.
- **`Order::First` as a default.** Two modules both asking for first produce an undefined winner. Order relative to the module you actually depend on with `OrderBefore`/`OrderAfter`.
- **Hooks in `.inc` files included by hand.** They are collected in 11.4.5 and silently ignored from 12.0.0 (change record 3613767). Convert them.
- **A hook class that is also a service in `services.yml` with a different id.** The collector registers the class name as the id only when no definition exists. Two ids for one class means two instances and two sets of injected state.

## See Also

- ← [Hooks Deprecation Timeline](hooks-deprecation-timeline.md)
- Dependency injection in general: https://camoa.github.io/dev-guides/drupal/services/constructor-injection/, https://camoa.github.io/dev-guides/drupal/services/drupal-global-helper/
- Hooks vs events for extension points you own: https://camoa.github.io/dev-guides/drupal/solid-principles/hooks-events-ocp/
- Testing: https://camoa.github.io/dev-guides/drupal/tdd/testing-events-hooks/
