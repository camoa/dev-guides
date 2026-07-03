---
description: Composer path repos install drupal-recipe packages as symlinks that dangle inside a DDEV container — force symlink:false, and never trust a path repo for tag-accurate resolution.
drupal_version: "11.x"
tldr: Composer path repos symlink drupal-recipe packages, and the symlink points outside the DDEV mount so drush/install can't read the recipe. Force `symlink: false` (or copy the package in). Path repos ignore git tags — use a local `vcs` repo when you must test a tagged constraint. `composer require` also writes a `version` key into the source package's composer.json — revert it.
---

# DDEV + Composer Path Repo for drupal-recipe Packages

**What:** When you develop or verify a `type: drupal-recipe` package locally with a Composer path repository, force `symlink: false`, run require ops on the HOST (not `ddev composer`), use a local `vcs` repo instead of a path repo whenever you need tag-accurate resolution, and revert the `version` key Composer writes back into the source package's `composer.json`.

**Rationale:** A Composer path repository installs the package as a **symlink** by default (`recipes/<pkg> → ../../<pkg>`). Inside a DDEV container only the project directory is mounted, so a symlink to a sibling directory points outside the mount — `drush site:install ../recipes/<pkg>` and `drush recipe` then fail to read `recipe.yml` (file-not-found, even though the host sees it). `ddev composer` has the same blind spot: it can't resolve a `../sibling` path repo the container doesn't mount, so require ops must run on host Composer. Separately, a path repo **always resolves to the working-tree HEAD as a dev version** and ignores git tags — so you cannot exercise a real constraint like `^1.0.0-beta2` through it (you get a `dev-main` vs `^1` canonical-priority conflict instead). Finally, `composer require <path-package>` mutates the **source** package by writing a `"version": "dev-main"` key into its `composer.json`, which quietly breaks a zero-diff guarantee on that repo.

**When it applies:** Any local build/verify loop for a recipe or site-template package (or any package) consumed via a Composer path repository under DDEV.

**Example:**

```jsonc
// composer.json — force a real copy, not a symlink
"repositories": {
  "local-recipe": {
    "type": "path",
    "url": "../palcera_brochure",
    "options": { "symlink": false }   // ← copy into vendor/recipes, survives the container mount
  }
}
```

```bash
# Require on the HOST, not `ddev composer` (the container can't see ../sibling)
composer require drupal/palcera_brochure:@dev

# After requiring, the source package's composer.json gained a bogus "version" key — revert it
git -C ../palcera_brochure checkout composer.json   # restore zero-diff on the source repo

# Need to test a TAGGED constraint (^1.0.0-beta2)? A path repo can't — use a local vcs repo:
"repositories": {
  "local-tagged": { "type": "vcs", "url": "../palcera_theme" }   // reads real git tags
}
```
