---
description: You're creating new SDC components using Radix CLI
drupal_version: "11.x"
---

## 3.8 Radix CLI Integration

### When to Use This Section
- You're creating new SDC components using Radix CLI
- You want to import existing Radix components into your sub-theme
- You need consistent component structure and Bootstrap integration

### Radix CLI Installation

#### Decision: Global vs Local Installation

| Installation Type | Command | Use When |
|-------------------|---------|----------|
| Global (recommended) | `npm install -g drupal-radix-cli` | Working on multiple Radix projects |
| Local (project-specific) | `npm install --save-dev drupal-radix-cli` | Single project, team consistency |

**RECOMMENDED:** Global installation for convenience across projects.

```bash
npm install -g drupal-radix-cli
```

**Verify installation:**
```bash
drupal-radix-cli --version
```

### Component Creation Patterns

#### Pattern: Create New Atom Component

**Decision: When to use CLI for component creation**
- You want consistent SDC structure (YAML, Twig, SCSS)
- You need Bootstrap integration scaffolding
- You want CLI to handle boilerplate

**Command:**
```bash
cd themes/custom/THEME_NAME
drupal-radix-cli create button-primary
```

**What CLI Creates:**
```
components/button-primary/
├── button-primary.component.yml  # Component schema
├── button-primary.twig           # Template
└── button-primary.scss           # Styles (optional)
```

**Generated `button-primary.component.yml`:**
```yaml
$schema: https://git.drupalcode.org/project/drupal/-/raw/10.1.x/core/modules/sdc/src/metadata.schema.json
name: Button Primary
status: stable
props:
  type: object
  properties:
    content:
      type: string
      title: Button Content
```

**Generated `button-primary.twig`:**
```twig
<button class="btn btn-primary">
  {{ content }}
</button>
```

**WHY USE CLI:**
- Ensures correct directory structure
- Includes proper YAML schema reference
- Sets up Bootstrap classes automatically
- Saves time over manual creation

#### Pattern: Create Molecule Component

**Command:**
```bash
drupal-radix-cli create search-form
```

**CLI Options:**
```bash
# Specify component type
drupal-radix-cli create search-form --type molecule

# Skip SCSS file creation
drupal-radix-cli create search-form --no-scss

# Create in specific directory
drupal-radix-cli create search-form --directory molecules/
```

**Generated structure:**
```
components/search-form/
├── search-form.component.yml
├── search-form.twig
└── search-form.scss
```

Then customize with atom composition:
```twig
{# search-form.twig #}
<form class="search-form d-flex" role="search">
  {% include 'THEME_NAME:input-search' with {
    placeholder: 'Search...',
  } %}
  {% include 'THEME_NAME:button-primary' with {
    content: 'Search',
    type: 'submit',
  } %}
</form>
```

### Component Import Patterns

#### Pattern: Import Radix Component to Sub-Theme

**Decision: When to import vs override**
- You need to customize an existing Radix component
- You want to extend Radix component with additional features
- You're creating a variant of a Radix component

**IMPORTANT:** Importing creates a COPY in your sub-theme. You own maintenance.

**Command:**
```bash
# Import specific Radix component
drupal-radix-cli import button

# This copies from radix/components/button/ to your sub-theme
```

**What Gets Copied:**
```
themes/custom/THEME_NAME/components/button/
├── button.component.yml     # Copied from Radix
├── button.twig              # Copied from Radix
└── button.scss              # Copied from Radix
```

**Now you can customize the copy:**
```twig
{# themes/custom/THEME_NAME/components/button/button.twig #}
{# Your customizations here #}
<button{{ attributes.addClass(classes) }}>
  {# Add custom icon #}
  {% if icon %}
    <i class="bi bi-{{ icon }}"></i>
  {% endif %}
  {{ content }}
</button>
```

**WHY IMPORT:**
- Provides starting point based on Radix component
- Maintains SDC structure and Bootstrap integration
- Faster than creating from scratch

**TRADE-OFF:**
- Imported component is now YOUR responsibility
- You won't get Radix updates for this component
- Must manually merge Radix updates if needed

#### Decision Table: Create vs Import vs Override

| Goal | Method | Command | Maintenance |
|------|--------|---------|-------------|
| New unique component | Create | `drupal-radix-cli create NAME` | You own |
| Customize Radix component | Import | `drupal-radix-cli import NAME` | You own |
| Use Radix as-is | Include | `{% include 'radix:NAME' %}` | Radix maintains |
| Override Radix template only | Copy manually | See [8.3](#83-overriding-radix-components) | Partial ownership |

**RECOMMENDATION:** Use `include` whenever possible. Only import/override when absolutely necessary.

### CLI Best Practices

**1. Use CLI for initial structure, then customize**

```bash
# Generate boilerplate with CLI
drupal-radix-cli create hero-section

# Then customize YAML, Twig, SCSS to your needs
```

**WHY:** CLI ensures correct structure; customization adds your requirements.

---

**2. Don't import Radix components unless you're customizing**

```bash
# BAD: Importing without changes
drupal-radix-cli import button
# Now you own button maintenance

# GOOD: Use Radix button directly
{% include 'radix:button' with { content: 'Click' } %}
```

**WHY:** Every imported component increases maintenance burden. Reuse when possible.

---

**3. Keep component names semantic, not presentational**

```bash
# BAD: Describes appearance
drupal-radix-cli create blue-rounded-button

# GOOD: Describes purpose
drupal-radix-cli create button-submit
drupal-radix-cli create button-cta
```

**WHY:** Semantic names survive design changes (button might not stay blue/rounded).

---

**4. Document why you imported/customized**

```yaml
# button-custom.component.yml
name: Custom Button
# REASON FOR CUSTOMIZATION:
# - Added icon support not in Radix button
# - Changed variant prop to match design system naming
status: stable
```

**WHY:** Future developers (including you) need context for customization decisions.

### Common Mistakes

**1. Editing Radix base theme components directly**

```bash
# BAD: Editing contrib theme
vim themes/contrib/radix/components/button/button.twig
```

**WHY:** Updates overwrite changes. Never edit contrib code.

**CORRECT:**

```bash
# Import to sub-theme, then edit
drupal-radix-cli import button
vim themes/custom/THEME_NAME/components/button/button.twig
```

---

**2. Creating overly generic component names**

```bash
# BAD: Name collision risk
drupal-radix-cli create card
# Conflicts with Radix card component
```

**WHY:** Sub-theme components with same name override Radix components. Be intentional.

**CORRECT:**

Either:
```bash
# Option 1: More specific name
drupal-radix-cli create card-product

# Option 2: Intentional override (import first)
drupal-radix-cli import card  # Then customize
```

---

**3. Not clearing cache after creating components**

```bash
drupal-radix-cli create navbar-custom
# Try to use in template → component not found
```

**WHY:** Drupal caches component discovery. New components invisible until cache clear.

**CORRECT:**

```bash
drupal-radix-cli create navbar-custom
drush cr  # Clear cache to register new component
```

### See Also
- [3.2 SDC Component Structure](#32-sdc-component-structure)
- [3.5 SDC Component Best Practices](#35-sdc-component-best-practices)
- [8.1 Radix Component Catalog](#81-radix-component-catalog)
- [8.3 Overriding Radix Components](#83-overriding-radix-components)