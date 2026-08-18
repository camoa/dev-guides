---
description: "Using replaces from themes and modules, the schema-compatibility rule it enforces, and the migration path from Twig templates"
tldr: "replaces is not themes-only — modules can replace components too, with a theme in the active hierarchy winning over a module fallback. The replacement schema must be compatible (required props match, shared props' type/enum lists are supersets), not identical; a narrowing replacement throws IncompatibleComponentSchema at cache rebuild, in production too."
drupal_version: "11.x"
---

# Replacing Templates with SDCs

## When to Use

> Use this when you're migrating existing Twig templates to SDC, overriding contrib module/theme components, or implementing field formatters with components.

## Decision

**Themes and modules can both use `replaces`.** The rule is precedence, not prohibition: `ComponentNegotiator::doNegotiate()` collects every definition whose `replaces` equals the requested ID, then `maybeNegotiateByTheme()` picks the winner from the active theme hierarchy (active theme first, then base themes by order); if no theme in that hierarchy claims it, `maybeNegotiateByModule()` returns a module candidate. Core ships a fixture module that does exactly this: `core/modules/system/tests/modules/sdc_test_replacements/` (`type: module`) replaces `sdc_test:my-button`.

The replacement must be **schema-compatible, not identical.** `SchemaCompatibilityChecker::isCompatible()` runs two checks and no others:
1. the two components' *required* prop sets must match;
2. for props present in **both** schemas, the replacement's `type` list and `enum` list must be supersets of the original's.

Adding a new optional prop, accepting an extra type, or accepting an extra enum value all pass. Dropping a prop the original declared is ignored entirely — only shared props are compared.

One hard precondition: **both** components must declare a `props` schema. `ComponentPluginManager::alterDefinitions()` (`:282-291`) errors with "component replacement requires both components to have schema definitions" if either side has none.

**WHY compatibility rather than equality:** calling code written against the original must keep working. Anything that only *adds* to the accepted input satisfies that; anything that narrows it does not.

Unlike prop validation, **this check is not `assert()`-gated** — `alterDefinitions()` throws `IncompatibleComponentSchema` outright (`:307-309`), in production too, during the cache rebuild that discovers the definitions. An incompatible replacement takes the site down at `drush cr`, not at render time.

One quiet exception: if the component named in `replaces` does not exist at all, the candidate is filtered out (`:276-279`) and no error is raised. A typo'd `replaces` target is silently ignored.

## Pattern

**Override with `replaces`:**

```yaml
# themes/my_theme/components/enhanced-button/enhanced-button.component.yml
$schema: https://git.drupalcode.org/project/drupal/-/raw/HEAD/core/assets/schemas/v1/metadata.schema.json
name: 'Enhanced Button'
replaces: 'radix:button'

props:
  type: object
  required:
    # must be the same set as radix:button's required list
    - text
  properties:
    text:
      type: string
    variant:
      # widening is allowed: original enum ⊆ this enum
      type: string
      enum: [primary, secondary, danger, ghost]
    icon:
      # a brand-new optional prop is allowed
      type: string
```

**Custom Field Formatter** — Reference: Field formatter integration patterns

```php
// Custom field formatter using components
class ComponentFieldFormatter extends FormatterBase {

  public function viewElements(FieldItemListInterface $items, $langcode) {
    $elements = [];

    foreach ($items as $delta => $item) {
      $elements[$delta] = [
        '#type' => 'component',
        '#component' => 'my_theme:field-card',
        '#props' => [
          'title' => $item->title,
          'variant' => $this->getSetting('variant'),
        ],
        '#slots' => [
          'content' => [
            '#markup' => $item->value,
          ],
        ],
      ];
    }

    return $elements;
  }
}
```

**Migration Path from Traditional Templates:**
1. Create SDC with equivalent structure.
2. Update calling templates to use `include('provider:component')`.
3. Test in development with schema validation enabled.
4. For complete replacement, use the `replaces` directive (from a theme or a module).

## Common Mistakes

- **Wrong**: Expecting a same-named component in your theme to take over a module's → **Right**: Components are namespaced by provider. `my_theme:card` and `my_module:card` are separate plugins and both stay live. Replacement happens only through an explicit `replaces` key.
- **Wrong**: Assuming a module cannot replace a component → **Right**: It can. A theme candidate in the active theme hierarchy wins when there is one; the module candidate is the fallback, not a forbidden case.
- **Wrong**: Narrowing the schema when using `replaces` → **Right**: Removing a `type`, dropping an `enum` value, or changing the required-prop set breaks callers written against the original and throws at cache rebuild. *Widening* is fine — extra optional props, extra accepted types, extra enum values all pass.

## See Also

- Reference: `/core/lib/Drupal/Core/Theme/Component/SchemaCompatibilityChecker.php:35-51` — the entire compatibility contract
- Reference: `/core/lib/Drupal/Core/Theme/ComponentNegotiator.php:72-140` — theme-then-module precedence
- Reference: `/core/modules/system/tests/modules/sdc_test_replacements/` — a module that replaces a component
- [SDC Architecture](sdc-architecture.md)
- [Component YAML Schema](component-yaml-schema.md)
- [UI Patterns Module](https://www.drupal.org/project/ui_patterns) — Component integration
