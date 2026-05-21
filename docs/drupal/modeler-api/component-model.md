---
description: The Component value object — types, successors, colors, and the ComponentWrapperPlugin pattern
tldr: "Component is a transient value object (never stored) that is the universal currency between Model Owners and Modelers. Seven typed constants on Api represent canvas node types; annotations and swimlanes are handled by the API itself and must not be passed to addComponent()."
drupal_version: "11.x"
---

# The Component Model

## When to Use

> Read this when implementing `addComponent()`, `usedComponents()`, or `readComponents()`, or when you need to understand how domain plugins map to the canvas.

## Decision

| Value Object | What it represents | Immutable? |
|---|---|---|
| `Component` | A single node on the canvas | Mostly (configuration can be set) |
| `ComponentSuccessor` | A directed edge from one component to another, optionally via a condition | Yes (`readonly`) |
| `ComponentColor` | Fill and stroke color for a component | Yes (`readonly`) |

**Component types** — constants on `Api`:

| Constant | Integer | String name | Typical domain mapping |
|---|---|---|---|
| `COMPONENT_TYPE_START` | 1 | `start` | Events / triggers |
| `COMPONENT_TYPE_SUBPROCESS` | 2 | `subprocess` | Sub-processes / nested models |
| `COMPONENT_TYPE_SWIMLANE` | 3 | `swimlane` | Visual grouping lanes |
| `COMPONENT_TYPE_ELEMENT` | 4 | `element` | Actions / tasks |
| `COMPONENT_TYPE_LINK` | 5 | `link` | Conditions / sequence flows |
| `COMPONENT_TYPE_GATEWAY` | 6 | `gateway` | Decision / merge gateways |
| `COMPONENT_TYPE_ANNOTATION` | 7 | `annotation` | Text annotations (not saved as domain plugins) |

Annotations and swimlanes are handled specially by the API — stored as third-party settings on the model entity, not passed to `addComponent()`.

## Pattern

```php
use Drupal\modeler_api\Component;
use Drupal\modeler_api\ComponentSuccessor;
use Drupal\modeler_api\Api;

$successors = [
  new ComponentSuccessor('Action_abc123', ''),          // no condition
  new ComponentSuccessor('Action_def456', 'Cond_xyz'),  // via condition
];

$component = new Component(
  owner: $this,
  id: 'Event_abc123',
  type: Api::COMPONENT_TYPE_START,
  pluginId: 'kernel:controller',
  label: 'Controller request',
  configuration: ['event_id' => 'controller'],
  successors: $successors,
);
```

When your components are not Drupal plugins but plain config arrays, use `ComponentWrapperPlugin`:

```php
use Drupal\modeler_api\Plugin\ComponentWrapperPlugin;

// In availableOwnerComponents():
return [
  'manual_trigger' => new ComponentWrapperPlugin(
    type: Api::COMPONENT_TYPE_START,
    id: 'manual_trigger',
    configuration: [],
    label: 'Manual Trigger',
  ),
];
```

## Common Mistakes

- **Wrong**: Returning annotations from `addComponent()` → **Right**: Do not route `COMPONENT_TYPE_ANNOTATION` through `addComponent()`. The API filters annotations before calling that method.
- **Wrong**: Adding swimlane components manually → **Right**: `COMPONENT_TYPE_SWIMLANE` is handled separately by `getUsedComponents()`.
- **Wrong**: Storing `Component` objects → **Right**: They are transient value objects for the save/read cycle. Store domain config in the entity; reconstruct Components on demand.

## See Also

- [Architecture: Owners vs Modelers](architecture-owners-vs-modelers.md)
- [Registering a Model Owner](registering-model-owner.md)
- Reference: `src/Component.php`, `src/ComponentSuccessor.php`, `src/ComponentColor.php`, `src/Api.php`
