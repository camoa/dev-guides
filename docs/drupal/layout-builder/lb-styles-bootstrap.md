## 11.3. Layout Builder Styles + Bootstrap Integration

### When to Use

When using Bootstrap-based themes (Radix, Bootstrap Barrio), map Layout Builder Styles to Bootstrap utility classes for consistent design system integration. Avoids custom CSS for common patterns.

### Decision

| If you need... | Use Bootstrap classes... | Why |
|---|---|---|
| Section backgrounds | `bg-primary`, `bg-secondary`, `bg-light`, `bg-dark` | Semantic color system |
| Section spacing | `p-{0-5}`, `py-{0-5}`, `px-{0-5}`, `m-{0-5}` | Consistent spacing scale |
| Text color on colored backgrounds | `text-white`, `text-dark`, `text-body` | Accessible contrast |
| Component alignment | `text-center`, `text-end`, `d-flex justify-content-center` | Responsive alignment |
| Component spacing | `mb-{0-5}`, `mt-{0-5}`, `gap-{0-5}` | Margin/gap utilities |
| Shadows | `shadow-sm`, `shadow`, `shadow-lg` | Elevation system |
| Borders | `border`, `border-{side}`, `border-{color}` | Border utilities |
| Rounded corners | `rounded`, `rounded-{size}`, `rounded-{side}` | Border radius |

### Pattern

**Spacing Group (Single Selection):**
```yaml
# layout_builder_styles.group.section_spacing.yml
id: section_spacing
label: 'Section Padding'
multiselect: single
required: false
weight: 0

# Styles in this group
---
# layout_builder_styles.style.section_padding_none.yml
id: section_padding_none
label: 'No Padding'
classes: 'p-0'
type: section
group: section_spacing
weight: 0

---
# layout_builder_styles.style.section_padding_small.yml
id: section_padding_small
label: 'Small Padding'
classes: 'py-3 px-2'        # Mobile-first: smaller on small screens
type: section
group: section_spacing
weight: 10

---
# layout_builder_styles.style.section_padding_medium.yml
id: section_padding_medium
label: 'Medium Padding'
classes: 'py-4 px-3'
type: section
group: section_spacing
weight: 20

---
# layout_builder_styles.style.section_padding_large.yml
id: section_padding_large
label: 'Large Padding'
classes: 'py-5 px-4'
type: section
group: section_spacing
weight: 30
```

**Background Color Group (Single Selection):**
```yaml
# layout_builder_styles.group.section_background.yml
id: section_background
label: 'Background Color'
multiselect: single
required: false
weight: 10

---
# layout_builder_styles.style.bg_none.yml
id: bg_none
label: 'No Background'
classes: ''                 # No classes
type: section
group: section_background
weight: 0

---
# layout_builder_styles.style.bg_primary.yml
id: bg_primary
label: 'Primary Background'
classes: 'bg-primary text-white'    # Include text color for contrast
type: section
group: section_background
weight: 10

---
# layout_builder_styles.style.bg_light.yml
id: bg_light
label: 'Light Background'
classes: 'bg-light'
type: section
group: section_background
weight: 20
```

**Component Effects (Multiple Selection):**
```yaml
# layout_builder_styles.group.component_effects.yml
id: component_effects
label: 'Visual Effects'
multiselect: multiple       # Can combine shadow + rounded + border
form_type: checkboxes
required: false
weight: 20

---
# layout_builder_styles.style.shadow.yml
id: shadow
label: 'Drop Shadow'
classes: 'shadow'
type: component
group: component_effects
weight: 0

---
# layout_builder_styles.style.rounded.yml
id: rounded
label: 'Rounded Corners'
classes: 'rounded'
type: component
group: component_effects
weight: 10

---
# layout_builder_styles.style.border.yml
id: border
label: 'Border'
classes: 'border'
type: component
group: component_effects
weight: 20
```

**Responsive Spacing with Breakpoint Classes:**
```yaml
# layout_builder_styles.style.responsive_padding.yml
id: responsive_padding
label: 'Responsive Padding (Small → Large)'
classes: 'p-2 p-md-3 p-lg-4 p-xl-5'    # Increases with screen size
type: section
group: section_spacing
weight: 40
```

**Container Width Control:**
```yaml
# layout_builder_styles.group.container_width.yml
id: container_width
label: 'Container Width'
multiselect: single
required: false
weight: 5

---
# layout_builder_styles.style.container_fluid.yml
id: container_fluid
label: 'Full Width'
classes: 'container-fluid'
type: section
group: container_width
weight: 0

---
# layout_builder_styles.style.container_fixed.yml
id: container_fixed
label: 'Fixed Width (Responsive)'
classes: 'container'
type: section
group: container_width
weight: 10
```

**Radix Theme Integration:**
```yaml
# Use Radix-specific utility classes
# layout_builder_styles.style.radix_bg_primary.yml
id: radix_bg_primary
label: 'Primary Background (Radix)'
classes: 'bg-primary text-white py-5'
type: section
group: section_background
layout_restrictions:
  - radix_onecol
  - radix_twocol
  - radix_threecol
```

Reference: [Bootstrap 5.3 Utilities](https://getbootstrap.com/docs/5.3/utilities/)

### Common Mistakes

- **Forgetting text color with backgrounds** → `bg-primary` alone unreadable if text stays dark. Include `text-white` or `text-dark`
- **Missing responsive classes** → `p-5` same on mobile and desktop. Use `p-2 p-md-3 p-lg-5` for mobile-first scaling
- **Overriding Bootstrap with custom CSS** → Define custom classes in theme instead of adding `!important` to Bootstrap
- **Not checking accessibility** → Color combinations need sufficient contrast. Test with browser dev tools
- **Combining conflicting utilities** → `p-3 py-5` results in `py-5` winning. Don't mix same-property utilities
- **Using outdated Bootstrap syntax** → `pull-left` and `text-left` deprecated in Bootstrap 5. Use `float-start` and `text-start`
- **Not testing on actual devices** → Responsive classes behave differently on real mobile vs browser resize

### See Also

- Section 11.2: Style Definitions (creating styles)
- Design System Bootstrap Mapping Guide (complete Bootstrap utility reference)
- Section 15: Theming Layout Builder (custom CSS for styles)
- Reference: [Bootstrap Spacing](https://getbootstrap.com/docs/5.3/utilities/spacing/)
- Reference: [Bootstrap Colors](https://getbootstrap.com/docs/5.3/utilities/colors/)
