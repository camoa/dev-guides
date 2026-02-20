## 5. Core Layout Plugins

### When to Use

When selecting a layout for a section or creating custom layouts based on core patterns.

### Items

#### layout_onecol

**Description:** Single column layout — one content region

**Regions:**
| Region | Label | Description |
|--------|-------|-------------|
| content | Content | Full-width content area |

**Default Region:** content

**Use Case:** Simple full-width sections, no columns

**Template:** `layout--onecol.html.twig`

**Provided By:** layout_discovery module (core)

```yaml
layout_id: layout_onecol
layout_settings:
  label: ''
```

**Gotchas:**
- Simplest layout, good default for initial sections
- No configuration options (just label)

#### layout_twocol

**Description:** Two column layout with top and bottom regions — 4 total regions

**Regions:**
| Region | Label | Description |
|--------|-------|-------------|
| top | Top | Full-width top area |
| first | First | Left column |
| second | Second | Right column |
| bottom | Bottom | Full-width bottom area |

**Default Region:** first

**Use Case:** Sidebar layouts, two-column content with header/footer

**Template:** `layout--twocol.html.twig`

**Provided By:** layout_discovery module (core)

```yaml
layout_id: layout_twocol
layout_settings:
  label: 'Two columns'
```

**Gotchas:**
- Fixed 50/50 column widths (no settings)
- Top and bottom regions span both columns

#### layout_twocol_section

**Description:** Two column section layout with configurable widths — Layout Builder variant

**Regions:**
| Region | Label | Description |
|--------|-------|-------------|
| first | First | Left column |
| second | Second | Right column |

**Default Region:** first

**Configuration:**
| Setting | Type | Options | Default |
|---------|------|---------|---------|
| column_widths | string | '50-50', '33-67', '67-33', '25-75', '75-25' | '50-50' |

**Use Case:** Two-column sections with adjustable widths

**Template:** `layout--twocol-section.html.twig`

**Provided By:** layout_builder module (core)

```yaml
layout_id: layout_twocol_section
layout_settings:
  label: ''
  column_widths: '67-33'
```

**Gotchas:**
- Part of layout_builder module, not layout_discovery
- Width settings affect CSS classes, theme must implement widths
- No top/bottom regions like layout_twocol

#### layout_threecol_section

**Description:** Three column section layout with configurable widths

**Regions:**
| Region | Label | Description |
|--------|-------|-------------|
| first | First | Left column |
| second | Second | Middle column |
| third | Third | Right column |

**Default Region:** second

**Configuration:**
| Setting | Type | Options | Default |
|---------|------|---------|---------|
| column_widths | string | '33-34-33', '25-50-25', '25-25-50', '50-25-25' | '33-34-33' |

**Use Case:** Three-column content sections, feature grids

**Template:** `layout--threecol-section.html.twig`

**Provided By:** layout_builder module (core)

```yaml
layout_id: layout_threecol_section
layout_settings:
  label: ''
  column_widths: '25-50-25'
```

**Gotchas:**
- Middle column (second) is default region
- Width options not evenly distributed for variety

#### layout_fourcol_section

**Description:** Four column section layout

**Regions:**
| Region | Label | Description |
|--------|-------|-------------|
| first | First | Column 1 |
| second | Second | Column 2 |
| third | Third | Column 3 |
| fourth | Fourth | Column 4 |

**Default Region:** first

**Use Case:** Four-column grids, feature blocks, icon rows

**Template:** `layout--fourcol-section.html.twig`

**Provided By:** layout_builder module (core)

```yaml
layout_id: layout_fourcol_section
layout_settings:
  label: ''
```

**Gotchas:**
- No width configuration (fixed 25% each)
- Can be overwhelming on mobile — consider responsive theming

#### layout_twocol_bricks

**Description:** Complex two-column layout with top, bottom, and middle regions — 7 total regions

**Regions:**
| Region | Label | Description |
|--------|-------|-------------|
| top | Top | Full-width top |
| first_above | First above | Left column above middle |
| second_above | Second above | Right column above middle |
| middle | Middle | Full-width middle |
| first_below | First below | Left column below middle |
| second_below | Second below | Right column below middle |
| bottom | Bottom | Full-width bottom |

**Default Region:** middle

**Use Case:** Complex page layouts with alternating full-width and column sections

**Template:** `layout--twocol-bricks.html.twig`

**Provided By:** layout_discovery module (core)

```yaml
layout_id: layout_twocol_bricks
layout_settings:
  label: ''
```

**Gotchas:**
- Most complex core layout (7 regions)
- All regions render even if empty (theme accordingly)
- No width configuration

#### layout_threecol_25_50_25

**Description:** Three column layout with 25/50/25 width split and top/bottom regions

**Regions:**
| Region | Label | Description |
|--------|-------|-------------|
| top | Top | Full-width top |
| first | First | 25% left sidebar |
| second | Second | 50% main content |
| third | Third | 25% right sidebar |
| bottom | Bottom | Full-width bottom |

**Default Region:** second

**Template:** `layout--threecol-25-50-25.html.twig`

**Provided By:** layout_discovery module (core)

**Gotchas:**
- Fixed width ratio
- Similar to layout_threecol_section but with top/bottom regions

#### layout_threecol_33_34_33

**Description:** Three column layout with even width split and top/bottom regions

**Regions:**
| Region | Label | Description |
|--------|-------|-------------|
| top | Top | Full-width top |
| first | First | 33% left column |
| second | Second | 34% middle column |
| third | Third | 33% right column |
| bottom | Bottom | Full-width bottom |

**Default Region:** first

**Template:** `layout--threecol-33-34-33.html.twig`

**Provided By:** layout_discovery module (core)

**Gotchas:**
- Middle column slightly wider (34% vs 33%) for even distribution
- Not the same as layout_threecol_section

### Common Mistakes

- **Confusing layout_twocol with layout_twocol_section** → Discovery layouts have top/bottom regions and no settings. Builder layouts have settings but fewer regions
- **Not theming width classes** → `column_widths` setting adds CSS classes to regions. Theme must define corresponding styles
- **Expecting responsive behavior** → Core layouts provide structure, not responsive CSS. Themes handle mobile breakpoints
- **Using wrong layout family** → layout_discovery layouts (onecol, twocol, threecol_*) for general use. layout_builder layouts (*_section) specifically for LB with configuration
- **Assuming all layouts available** → Layout discovery scans modules/themes. Disabled modules/themes remove their layouts

### See Also

- Section 12: Custom Layout Plugins (creating your own)
- Section 15: Theming Layout Builder (styling layouts)
- Reference: `/core/modules/layout_builder/layout_builder.layouts.yml`
- Reference: `/core/modules/layout_discovery/layout_discovery.layouts.yml`
