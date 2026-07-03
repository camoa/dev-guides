---
description: Rebrand a required theme without forking it — ship neutral logo/favicon as permanent managed files (they travel via core Default Content) and override via theme-settings; beware Canvas re-seeding brand strings from the theme's SDC examples.
drupal_version: "11.x"
tldr: Reuse a required theme unmodified while replacing its branded logo/favicon: ship neutral binaries as PERMANENT managed files under `public://branding/` (core Default Content exports the file entities + binaries) and point `<theme>.settings` logo/favicon overrides at them (`use_default: false`). Theme untouched, no theme release. Beware: Canvas regenerates component-config `default_value` from the theme's SDC `examples:` on every export — neutralize those upstream and patch post-export.
---

# Rebrand a Required Theme Without Forking

**What:** To ship a template on a required theme whose default logo/favicon embed someone else's wordmark, override the brand assets at the **template** level: ship neutral binaries as permanent managed files and set them via `<theme>.settings` config. Do not edit or fork the theme.

**Rationale:** Editing the theme's SVGs (or forking/renaming the theme) has a high blast radius — it forces a theme re-tag/release and can regress every other consumer of that theme. Instead, keep the theme a read-only caret dependency and override only what's branded:

- **Managed-file assets travel via Default Content.** Register the neutral `logo-{light,dark}.svg` / favicon as **permanent** `file` entities under `public://branding/…`. Core's Default Content exporter serializes managed-file entities *and their binaries*, so `site:export` carries the actual asset bytes into the package's `content/`. (A raw file dropped in the theme would require touching the theme; a managed file does not.)
- **Theme-settings override, not theme edit.** Set `<theme>.settings` `logo`/`favicon` with `use_default: false` pointing at the shipped file. The theme's own files stay byte-identical — the "reused as-is" guarantee holds and no theme release is needed.

**Beware the Canvas SDC-examples feedback loop:** Canvas regenerates a component config's `default_value` from the theme's SDC `examples:` block on **every** export. If the theme's `author-byline` SDC example still says `Elena Martinez`, that brand string is re-seeded into your exported `canvas.component.*` config each export. Handle it in two places: neutralize the `examples:` upstream in the theme (proper fix / upstream follow-up) AND keep a post-export patch until that lands.

**When it applies:** Any site template that requires a shared theme carrying brand identity in its logo/favicon/SDC examples, where the theme must remain unmodified (zero-diff, no release).

**Example:**

```bash
# 1. Neutral binaries as PERMANENT managed files so Default Content exports them
drush php:eval '\Drupal\file\Entity\File::create([
  "uri" => "public://branding/meridian-logo-light.svg", "status" => 1,
])->save();'   # status=1 (permanent); repeat for dark logo + favicon
```

```yaml
# 2. Theme-settings override — theme files untouched
# config/<theme>.settings.yml
logo:
  use_default: false
  path: 'public://branding/meridian-logo-light.svg'
favicon:
  use_default: false
  path: 'public://branding/meridian-favicon.svg'
```

```text
# 3. Every export: neutralize brand re-seeded from the theme's SDC examples:
#    canvas.component.sdc.<theme>.author-byline default_value  ← re-patch post-export
#    upstream follow-up: fix examples: in the theme's author-byline.component.yml
```
