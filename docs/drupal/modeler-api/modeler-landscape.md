---
description: Choose between Workflow Modeler, BPMN.iO, and Fallback — comparison of available Modeler plugins
tldr: "Workflow Modeler (drupal/modeler, React Flow + JSON) is the recommended default for new sites; BPMN.iO (drupal/bpmn_io, BPMN XML) is the legacy alternative for BPMN-standard compliance or SVG export. The built-in Fallback modeler is read-only and always present. Both can coexist."
drupal_version: "11.x"
---

# The Modeler Landscape

## When to Use

> Use this when selecting which Modeler module to install, when advising on technology choices, or when troubleshooting modeler-specific behavior.

## Decision

| Modeler | Package | Tech | Format | Status |
|---------|---------|------|--------|--------|
| **Workflow Modeler** | `drupal/modeler` | React Flow + htmx | JSON | Recommended; modern |
| **BPMN.iO** | `drupal/bpmn_io` | BPMN.js | BPMN XML | Legacy; alternative |
| **Fallback** | Built into `modeler_api` | None (no UI) | N/A | Auto-used when no modeler present; read-only |

The `Fallback` modeler (`isEditable(): FALSE`) is always registered. When exactly one real modeler is installed, `Api::getModeler()` returns it; with two or more, a selection UI appears.

| Criterion | Workflow Modeler | BPMN.iO |
|---|---|---|
| JSON-friendly model data | Yes | No (XML) |
| React frontend ecosystem | Yes | No |
| BPMN standard compliance | No | Yes |
| Smaller JS bundle | Yes | No |
| Htmx/Turbo compatible | Yes | Partial |
| SVG diagram export | No | Yes |
| Existing BPMN diagrams | No | Yes |

## Pattern

**Workflow Modeler characteristics:**
- Canvas: React Flow (TypeScript/React SPA compiled into `modeler/react-ui` library)
- Data format: JSON with `{id, metadata, nodes[], edges[]}` structure
- Config forms: `JsonResponse` — Drupal form rendered to JSON structure consumed by React
- Dependencies: `modeler_api:modeler_api` only
- Htmx compatible: Yes (`HX-Request` header detected)
- Replay and dark mode: Supported

**BPMN.iO characteristics:**
- Canvas: BPMN.js (JavaScript library)
- Data format: BPMN XML
- Config forms: `AjaxResponse` — opens off-canvas dialog
- Replay: BPMN shape highlighting via XML mutation
- Standards-based; interoperable with other BPMN tools

Both can coexist on the same site. With both installed, users can choose which modeler to edit with via the "edit with" routes.

## Common Mistakes

- **Wrong**: Assuming BPMN.iO is required for ECA → **Right**: ECA 3.1+ depends on `modeler_api`, not on `bpmn_io`. You can use the Workflow Modeler with ECA.
- **Wrong**: Installing only `modeler_api` and expecting a visual editor → **Right**: With only `modeler_api` installed (no `modeler` or `bpmn_io`), models fall back to non-visual editing.
- **Wrong**: Confusing `drupal/modeler` with `drupal/modeler_api` → **Right**: `modeler_api` is the integration API; `modeler` (without `_api`) is the Workflow Modeler frontend.

## See Also

- [When to Use the Modeler API](when-to-use.md)
- [Building a Modeler Plugin](building-a-modeler.md)
- Reference: `modeler-src/src/Plugin/ModelerApiModeler/WorkflowModeler.php`, `https://www.drupal.org/project/modeler`, `https://www.drupal.org/project/bpmn_io`
