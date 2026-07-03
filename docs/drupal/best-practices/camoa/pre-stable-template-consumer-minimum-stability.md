---
description: A site template with pre-stable deps blocks a plain composer require on stable-only roots — stability flags don't propagate transitively; the consumer must set minimum-stability dev + prefer-stable.
drupal_version: "11.x"
tldr: Plain `drupal/cms` roots are `minimum-stability: stable`. A template requiring non-stable deps (alpha/rc/beta), even with caret ranges, blocks a plain `composer require`. Composer stability flags don't propagate transitively — the template can't set them for its consumer. Document `composer config minimum-stability dev` + `prefer-stable true` in BOTH the README install steps AND the CI workflow. `site:export` already warns on non-stable deps, predicting this.
---

# Pre-Stable Template Deps Require Consumer minimum-stability Config

**What:** If your site template's `composer.json` requires any non-stable dependency (alpha, beta, or rc — even behind a caret range), tell the consumer to run `composer config minimum-stability dev` and `composer config prefer-stable true` before requiring the template. Put this in **both** the README install section and the CI install workflow.

**Rationale:** A plain `drupal/cms` project root is created with `minimum-stability: stable`. Composer will not select an alpha/beta/rc version of a transitive dependency on such a root, so `composer require <your-template>` fails to resolve even though every constraint is a rule-compliant caret range. Crucially, **Composer stability flags do not propagate transitively** — a dependency cannot lower `minimum-stability` for the project that installs it; only the consumer's **root** `composer.json` governs stability. So the consumer must opt in explicitly. `prefer-stable: true` keeps everything that *can* be stable stable, limiting the blast radius to the genuinely pre-stable packages. Your **CI** install job needs the same two flags, or it fails identically to a human consumer. `drush site:export` already emits a non-stable-dependency warning at export time — that warning is the early signal that this consumer-side friction exists.

**When it applies:** Any published recipe or site template that ships even one pre-stable contrib dependency (common while `schemadotorg`, `webform` RCs, or a `beta` theme are load-bearing). It is also a marketplace-review optics risk — record it, but a caret range over a pre-stable version is not itself a rule violation.

**Example:**

```bash
# Consumer README install steps — required BEFORE requiring the template
composer config minimum-stability dev
composer config prefer-stable true
composer require drupal/palcera_brochure

# Same two lines belong in the CI workflow's install job, e.g.:
#   - run: composer config minimum-stability dev && composer config prefer-stable true
#   - run: composer require drupal/palcera_brochure
```

```text
Why: stability flags are NOT transitive
  root: minimum-stability=stable
    └─ template (caret deps)
         └─ schemadotorg 1.0.0-alpha37   ← rejected: root won't take alpha
  Fix is at the ROOT, never inside the template.
```
