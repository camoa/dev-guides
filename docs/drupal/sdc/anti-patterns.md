---
description: "Twelve SDC anti-patterns for code review: over-componentizing, logic in Twig, missing schemas, slot conditionals, and replacement mistakes"
tldr: "The two highest-impact anti-patterns: wrapping {% block name %} in {% if name %} silently drops content on the embed path with no error, and narrowing a replacement's schema throws IncompatibleComponentSchema at cache rebuild in production. Both trace back to THE MECHANISM — the YAML declares, the Twig (and SchemaCompatibilityChecker) decide."
drupal_version: "11.x"
---

# Anti-Patterns

## When to Use

> Use this when you're code reviewing component implementations, debugging component issues, or establishing component development standards.

## Decision

Twelve recurring mistakes, grouped by consequence: some are dead weight (schema keys nothing reads), some silently drop content, and two throw hard errors at cache rebuild in production.

## Pattern

**Anti-Pattern 1: Over-Componentizing**

```
components/
├── heading/
├── paragraph/
├── link/
├── image/
└── text-with-heading/  ← Combines previous 4
```

**WHY this is wrong:** Each component has discovery/loading overhead. Group elements that always appear together into a single component.

**CORRECT:** Create components at a meaningful abstraction level (atoms/molecules, not sub-atomic particles).

---

**Anti-Pattern 2: Logic in Twig Templates**

```twig
{# BAD: Complex business logic in template #}
{% set user_role = user.roles|first %}
{% if user_role == 'administrator' or user_role == 'editor' %}
  {% set can_edit = true %}
{% else %}
  {% set can_edit = false %}
{% endif %}
```

**WHY this is wrong:** Business logic belongs in preprocessing/controllers. Templates should be presentation-only.

**CORRECT:** Pass computed values as props. The template only handles display logic.

---

**Anti-Pattern 3: Missing Schema Definitions**

```yaml
# BAD: No schema for props
name: 'Button'
status: stable
# No props or slots defined
```

**WHY this is wrong:** Core tolerates it — an empty `.component.yml` is a valid component, and a theme's components only *require* a schema when `enforce_prop_schemas: true` is set (module components always require one). But with no schema there is no IDE support, no description of the component API, and integration modules (UI Patterns, SDC Display, component pickers) have nothing to build a UI from.

**CORRECT:** Always define complete props/slots schemas with descriptions — and keep them matching the `.twig`, which is the artifact that actually decides behaviour (see [Component YAML Schema — THE MECHANISM](component-yaml-schema.md)). A schema that has drifted from its template is worse than none, because readers believe it.

---

**Anti-Pattern 4: Using Slots for Simple Typed Data**

```yaml
# BAD: Using slot for boolean/enum
slots:
  variant:
    title: 'Variant'  # Should be prop
  disabled:
    title: 'Disabled State'  # Should be prop
```

**WHY this is wrong:** Slots bypass validation. Simple typed values should be validated props for type safety and better errors.

**CORRECT:** Slots are for renderable content only. Use props for typed configuration data.

---

**Anti-Pattern 5: Hardcoding Child Components**

```twig
{# BAD: Hardcoded child components #}
<div class="card__actions">
  {{ include('my_theme:button', { text: 'Edit' }) }}
  {{ include('my_theme:button', { text: 'Delete' }) }}
</div>
```

**WHY this is wrong:** Reduces flexibility. Different contexts might need different buttons or no buttons.

**CORRECT:** Use a slot for the actions area. Let calling code decide what buttons to include.

---

**Anti-Pattern 6: Not Using `with_context = false`**

```twig
{# BAD: Leaking all variables into component #}
{{ include('my_theme:button', { text: 'Click' }) }}
```

**WHY this is wrong:** The component inherits all parent template variables. Creates hidden dependencies and unpredictable behavior.

**CORRECT:** Use `with_context = false` to isolate component context.

---

**Anti-Pattern 7: Complex Conditionals on Slots**

```twig
{# BAD: Complex slot logic #}
{% if content and content.field_name and content.field_name|render|striptags|trim %}
  {{ content }}
{% endif %}
```

**WHY this is wrong:** Slots contain arbitrary renderables. Can't reliably access their properties. Logic should be in calling code.

**CORRECT:** Render the slot into a variable and test the resulting string, never the renderable's internals — and never a slot-named variable placed around a `{% block %}` (see Anti-Pattern 9). Complex conditions belong in preprocessing.

---

**Anti-Pattern 8: Using `@extend` in SCSS**

```scss
// BAD: Using @extend
.my-button {
  @extend .btn;
  @extend .btn-primary;
}
```

**WHY this is wrong:** Creates unexpected selector chains, bloats compiled CSS, makes debugging difficult.

**CORRECT:** Use mixins or utility classes. Or include Bootstrap classes directly in the template.

---

**Anti-Pattern 9: Wrapping a `{% block %}` in `{% if slot %}`**

```twig
{# BAD: the block is unreachable from {% embed %} #}
{% if header %}
  <header class="component__header">
    {% block header %}{% endblock %}
  </header>
{% endif %}
```

**WHY this is wrong:** Only the `#type: component` render element defines a context variable named after the slot (`ComponentElement.php:138-147`). A `{% block %}` override supplied by `{% embed %}` is not a variable, so `header` is undefined, the `if` is false, and the caller's content is dropped with no error and no log entry. The component looks fine in whatever preview you built with the render element.

Rendering a bare `{{ header }}` with no `{% block %}` (the older wording of this anti-pattern) has the mirror-image problem: an `{% embed %}` caller has no way to fill that slot at all.

**CORRECT:** Capture the block, then test what it produced.

```twig
{% set header_content %}
  {% block header %}{{ header|default('') }}{% endblock %}
{% endset %}
{% if header_content|trim is not empty %}
  <header class="component__header">{{ header_content }}</header>
{% endif %}
```

Simpler and usually good enough: no conditional at all, fallback content inside the block — the way `core/modules/system/tests/themes/sdc_theme_test/components/my-card/my-card.twig` does it.

---

**Anti-Pattern 10: Global CSS Selectors**

```css
/* BAD: Generic selectors */
.button { }
.card { }
.title { }
```

**WHY this is wrong:** Collides with other components and global styles. Not scoped to the component.

**CORRECT:** Use BEM with a component-specific namespace: `.my-component__element`.

---

**Anti-Pattern 11: Expecting a Same-Named Component to Win**

```yaml
# BAD: my_theme/components/button/button.component.yml, no `replaces` key,
# added in the hope it takes over my_module:button
name: Button
```

**WHY this is wrong:** Components are namespaced by provider. `my_theme:button` and `my_module:button` are two live plugins; the module's keeps rendering wherever it was already called. `ComponentNegotiator::doNegotiate()` only considers definitions that explicitly declare `replaces` (`:72-78`).

**CORRECT:** Declare `replaces: 'my_module:button'`. Both **themes and modules** may do this — a theme in the active hierarchy wins, a module is the fallback (`ComponentNegotiator.php:94-140`, and core's own `sdc_test_replacements` module fixture).

---

**Anti-Pattern 12: Narrowing the Schema in a `replaces` Component**

```yaml
# BAD: replacement drops an accepted enum value
replaces: 'radix:button'
props:
  type: object
  properties:
    variant:
      type: string
      enum: [primary]   # original also accepted secondary, danger
```

**WHY this is wrong:** Calling code written against the original passes `secondary` and now fails. `SchemaCompatibilityChecker::isCompatible()` requires the replacement's `type` and `enum` lists to be **supersets** of the original's for shared props, and the required-prop sets to match. Violate it and `alterDefinitions()` throws `IncompatibleComponentSchema` during cache rebuild — in production too, this one is not `assert()`-gated.

**CORRECT:** The schemas must be *compatible*, not identical. Adding an optional prop, an extra accepted type, or an extra enum value is allowed and is the normal way to extend a replacement.

## Common Mistakes

See the twelve anti-patterns above — each entry states the mistake, why it is wrong, and the correction.

## See Also

- [Props vs Slots Decision Framework](props-vs-slots-decision-framework.md)
- [Security](security.md)
- [Component Composition](component-composition.md)
