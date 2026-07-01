---
tldr: "Use allow_custom:false for consistency bundles, allow_custom:true + restrictions for curated editor bundles — posture is per-bundle. Overrides are content, not config; default changes don't propagate to overridden entities."

---
## 9. Defaults vs Overrides

### When to Use

When deciding whether to allow per-entity layout customization or use a single default layout for all entities of a bundle.

### Decision

| If you need... | Use... | Why |
|---|---|---|
| Same layout for all entities of bundle | Defaults only (allow_custom: false) | Single source of truth, easy to update all entities, config-based deployment |
| Per-entity unique layouts | Overrides enabled (allow_custom: true) | Editors can customize individual entity layouts, content stored in entity field |
| Mix of standard and custom layouts | Defaults with selective overrides | Most entities use default, special entities override as needed |
| Staging/production parity | Defaults only | Config export/import, no content dependencies for layout structure |
| Content-driven layout decisions | Overrides | Layout decisions per entity, possibly based on content strategy or editor preference |

### Pattern

**Defaults only:**
```yaml
# core.entity_view_display.node.article.default.yml
third_party_settings:
  layout_builder:
    enabled: true
    allow_custom: false
    sections:
      - layout_id: layout_twocol_section
        layout_settings: {  }
        components:
          - uuid: abc-123
            region: first
            configuration:
              id: 'field_block:node:article:body'
            weight: 0
```

**With overrides enabled:**
```yaml
third_party_settings:
  layout_builder:
    enabled: true
    allow_custom: true  # Allows per-entity customization
    sections:
      # Default sections for entities without overrides
      - layout_id: layout_onecol
        components: []
```

When overrides enabled, entities get a `layout_builder__layout` field (or similar, configurable name) storing per-entity sections.

Reference: `/core/modules/layout_builder/src/Plugin/SectionStorage/DefaultsSectionStorage.php` and `OverridesSectionStorage.php` for implementation.

**The allow_custom editorial-posture spectrum**

`allow_custom` is not just a boolean — combined with restrictions and Layout Builder Styles it yields three editorial postures:

| Posture | Config | Editor experience | Best for |
|---|---|---|---|
| **Locked / templated** | `allow_custom: false` | Cannot customize; default-only layout | Consistency-critical bundles |
| **Curated** | `allow_custom: true` + restrictions allowlist + curated LB Styles | Composes from an approved palette | Most editorial bundles |
| **Open** | `allow_custom: true`, no restrictions | Full freedom | Rare / risky |

Verified: one production site ran a templated bundle (`allow_custom: false`) alongside curated bundles (`allow_custom: true` + per-bundle allowlists) in the same install — the posture is a per-bundle decision, not a site-wide one.

### Decision Points

| At this point... | If... | Then... |
|---|---|---|
| Initial setup | Content editors need flexibility | Enable overrides, but provide good defaults as starting point |
| Initial setup | Layouts should be controlled/consistent | Defaults only, use Views or other tools for content variation |
| Default changes | Some entities overridden | Changes only affect non-overridden entities (overrides don't inherit updates) |
| Default changes | No overrides exist | Changes apply immediately to all entities |
| Content migration | Overrides enabled | Decide whether migrated entities use default or import custom layouts |
| Multisite deployment | Overrides in use | Content sync required (not just config), increases deployment complexity |

### Common Mistakes

- **Enabling overrides by default** → Creates maintenance burden. Changing defaults doesn't update overridden entities. Start with defaults only
- **Not communicating override behavior** → Editors expect layout changes to apply everywhere. Once entity overridden, it's disconnected from defaults — document this clearly
- **Forgetting override permission** → Overrides need separate permission: "Configure editable {entity_type} {bundle} layout overrides". Editors frustrated when can't edit
- **Not planning for default updates** → With overrides, no easy way to push default changes to overridden entities. Either accept divergence or manually update/revert
- **Mixing content and config** → Defaults are config (exportable). Overrides are content (in entity field). Config-only deployment workflows break with overrides
- **Ignoring revert workflows** → Once overridden, only way back to default is "Revert to defaults" button (blows away custom content). No partial revert
- **Assuming overrides are per-field** → Overrides are all-or-nothing for the entire layout. Can't override just one section

### See Also

- Section 2: Enabling Layout Builder (setting allow_custom)
- Section 14: Config Export & Recipes (deployment with defaults)
- Section 16: Best Practices (when to use each approach)
- Reference: [Creating Layout Defaults](https://www.drupal.org/docs/8/core/modules/layout-builder/creating-layout-defaults)
- Reference: [Creating Layout Overrides](https://www.drupal.org/docs/8/core/modules/layout-builder/creating-layout-overrides)
