---
description: Creating and configuring Layout Builder Style groups — organizing styles into categories with single or multiple selection.
---

## 11.1. Layout Builder Style Groups

### When to Use

Style groups organize related styles into categories (e.g., "Padding", "Background Color", "Border Style"). Editors see one form element per group, making the UI manageable when you have many styles. Groups control whether editors can select single or multiple styles from the group.

### Decision

| If you need... | Use... | Why |
|---|---|---|
| Single choice from options | `multiselect: single` | Radio buttons or select dropdown — choose one background color |
| Multiple choices from options | `multiselect: multiple` | Checkboxes or multi-select — combine padding + margin + color |
| Always require selection | `required: true` | Force editors to make a choice, no "None" option |
| Optional selection | `required: false` | Adds "- None -" option, editors can skip |
| Simple multi-select UI | `form_type: checkboxes` | Easier for 2-5 options |
| Compact multi-select UI | `form_type: select` | Better for 6+ options, uses `<select multiple>` |

### Pattern

**Create Group via YAML Config:**
```yaml
# config/sync/layout_builder_styles.group.padding.yml
langcode: en
status: true
dependencies: {  }
id: padding
label: Padding
multiselect: single        # 'single' or 'multiple'
form_type: checkboxes      # 'checkboxes' or 'select' (only for multiselect: multiple)
required: false            # true requires selection
weight: 0
uuid: abc-123
```

**Example Groups Setup:**
```yaml
# layout_builder_styles.group.spacing.yml
id: spacing
label: Spacing
multiselect: multiple      # Can combine padding + margin
form_type: checkboxes
required: false
weight: 0

# layout_builder_styles.group.background.yml
id: background
label: Background Color
multiselect: single        # Only one background color
form_type: radios          # Radio button selection
required: true             # Must choose a background
weight: 10

# layout_builder_styles.group.effects.yml
id: effects
label: Visual Effects
multiselect: multiple      # Can combine shadow + rounded corners
form_type: select          # Multi-select dropdown
required: false
weight: 20
```

**Group Workflow:**
1. Create groups first (styles reference groups)
2. Set multiselect behavior and form type
3. Set weight to control UI order (lower = first)
4. Create styles assigned to each group
5. Export config: `drush config:export --destination=../config/sync`

Reference: `modules/contrib/layout_builder_styles/src/Entity/LayoutBuilderStyleGroup.php`

### Common Mistakes

- **Creating styles before groups** → Admin UI prevents style creation until at least one group exists
- **Wrong form_type for single selection** → `form_type` is ignored when `multiselect: single`. Use radios or select automatically
- **Overlapping group purposes** → Don't create "Padding" and "Spacing" groups. Consolidate related styles
- **Not setting weight** → Groups appear in random order. Set weight to control: Spacing (0), Colors (10), Effects (20)
- **Making everything required** → Required groups frustrate editors. Only require choices that truly matter (e.g., accessibility color contrast)
- **Generic group labels** → "Styles" or "Options" unhelpful. Use specific labels: "Section Background", "Block Alignment"

### See Also

- Section 11.2: Style Definitions (assigning styles to groups)
- Section 11: Overview (architecture and config entities)
- Reference: `modules/contrib/layout_builder_styles/src/Form/LayoutBuilderStyleGroupForm.php`
