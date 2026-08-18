---
description: "Accessing props, the three slot call paths, and why {% if slot %} around {% block slot %} silently drops content"
tldr: "A slot arrives differently on each call path — {% embed %} gives a block override, include() gives a context variable, #type: component gives both. Default to rendering every slot through {% block %} with the fallback inside it; testing a slot-named variable around a {% block %} breaks the {% embed %} path with no error."
drupal_version: "11.x"
---

# Twig Templates in SDCs

## When to Use

> Use this when you're writing component Twig templates, accessing props and rendering slots, or working with the `attributes` object.

## Decision

**Accessing Props:** props are available as Twig variables directly. **The template, not the YAML, decides what a missing prop becomes** — see [THE MECHANISM](component-yaml-schema.md). Every prop with a `default:` in the `.component.yml` needs a matching `??` or `|default()` here, or the default does not exist.

Props you never declared in the YAML also arrive here and work: the validator narrows the context to declared names before checking it, and it is `assert()`-gated anyway. That is convenient and it is a trap — an undeclared prop is invisible to every tool that reads the YAML (UI Patterns, component pickers, IDE autocompletion), so declare what you use.

**Rendering Slots — the three call paths.** A slot reaches the template by one of three routes, and they do **not** deliver it the same way:

| Caller | Slot arrives as | `{% block name %}` sees it | `{{ name }}` sees it |
|---|---|---|---|
| `{% embed 'p:c' %}{% block name %}…{% endblock %}{% endembed %}` | a Twig **block override** | yes | **no — `name` is undefined** |
| `{{ include('p:c', {name: …}) }}` | a **context variable** | **no — block renders its own body** | yes |
| `#type: component` + `#slots` | **both** | yes | yes |

The render-element path is generous because `ComponentElement::generateComponentTemplate()` writes `$context[$slot_name] = $slot_value` *and* emits `{% block $slot_name %}{{ $slot_name }}{% endblock %}` into the generated embed (`ComponentElement.php:138-147`). The two hand-written paths each give you only one of the two.

**Default: render every declared slot through `{% block %}`, with the fallback inside the block.** That is what core does.

## Pattern

Reference: `/themes/contrib/radix/components/button/button.twig`

```twig
{# Props available as variables — and this is where defaults are actually applied #}
{% set button_html_tag = button_html_tag ?? 'button' %}
{% set size = size ? [size] : [] %}
{% set disabled_classes = disabled ? ['disabled'] : [] %}
```

Reference: `/core/themes/olivero/components/teaser/teaser.twig` (bare blocks), `/core/modules/system/tests/themes/sdc_theme_test/components/my-card/my-card.twig` (fallback inside the block)

```twig
{# Slot rendering — no conditionals around the block #}
<header>
  {% block prefix %}{% endblock %}
  <div class="teaser__meta">
    {% block meta %}{% endblock %}
  </div>
</header>

<div class="teaser__content">
  {% block content %}
    {{ content|default('') }}   {# also serves the include() path #}
  {% endblock %}
</div>
```

Putting `{{ content|default('') }}` *inside* the block makes the component work on all three paths at once: `{% embed %}` overrides the block, `include()` leaves the block alone and the fallback prints the variable, and the render element does both and the override wins.

**Attributes Object** — the `attributes` object (type `Drupal\Core\Template\Attribute`) provides attribute merging.

```twig
{# Class addition #}
<div{{ attributes.addClass('component', 'component--' ~ variant) }}>

{# Attribute setting #}
<button{{ attributes.setAttribute('disabled', disabled).setAttribute('type', 'button') }}>

{# Multiple operations chained #}
<article{{ attributes
  .addClass(['teaser', variant ? 'teaser--' ~ variant])
  .setAttribute('role', 'article')
  .removeAttribute('id') }}>
```

**Conditional Slot Rendering** — you will want to skip an empty wrapper. Doing it the obvious way silently deletes your caller's content:

```twig
{# ✗ BROKEN — do not do this #}
{% if header %}
  <header class="component__header">
    {% block header %}{% endblock %}
  </header>
{% endif %}
```

Called as `{% embed 'my_theme:card' with {...} only %}{% block header %}…{% endblock %}{% endembed %}`, the variable `header` is **undefined** — a block override is not a context variable. The `if` is false, the block is never reached, the caller's header disappears, and **nothing errors**. It "works" the first time you test it only if you happened to test through `#type: component`, which is the one path that sets both.

Drop the `only` and it gets worse rather than better: an unrelated `header` variable in the calling template's scope leaks in and makes the conditional true or false for reasons that have nothing to do with the slot.

**Correct pattern: capture the block, then test the captured output.**

```twig
{% set header_content %}
  {% block header %}{{ header|default('') }}{% endblock %}
{% endset %}
{% if header_content|trim is not empty %}
  <header class="component__header">{{ header_content }}</header>
{% endif %}
```

The capture renders the block — picking up an `{% embed %}` override — and its in-block fallback prints the variable for the `include()` and render-element paths. Now the `if` is testing what will actually be output, on every call path. Real-world reference: `/modules/contrib/commerce/components/commerce-admin-card/commerce-admin-card.twig:70-80`.

`{% if slot %}` around a **bare `{{ slot }}`** (no `{% block %}`) is a different, smaller mistake: it is correct for `include()` and the render element, and inert for `{% embed %}` — the component simply cannot receive that slot from an embed at all.

## Common Mistakes

- **Wrong**: Wrapping `{% block name %}` in `{% if name %}` → **Right**: Only the render-element path defines a variable named after the slot. On the `{% embed %}` path the conditional is always false and the caller's content vanishes with no error. Capture the block into a variable and test that instead.
- **Wrong**: Applying complex logic to slot content → **Right**: Slots contain arbitrary renderables. Test the *rendered* capture (`|trim is not empty`), never the renderable's internals. All logic should be in props.

## See Also

- Reference: `/core/lib/Drupal/Core/Template/Attribute.php` — Attribute class
- Reference: `/core/lib/Drupal/Core/Render/Element/ComponentElement.php:114-151` — `generateComponentTemplate()`, the only place a slot-named context variable is created
- [Component YAML Schema — THE MECHANISM](component-yaml-schema.md)
- [Component Composition](component-composition.md)
- [Props vs Slots Decision Framework](props-vs-slots-decision-framework.md)
