---
description: Canvas component configs carry an active_version hash of their settings — raw-editing them (setData/cset/YAML) breaks the hash. site:install masks it, but the recipe CLI validator fails. Recompute hashes from a live install.
drupal_version: "11.x"
tldr: "`canvas.component.*` configs store an `active_version` hash of their settings. Raw-editing the config (setData/cset/direct YAML) to genericize a value desyncs the hash from the settings. `drush site:install` and runtime DON'T re-validate, so it looks fine — but the recipe CLI validator (`recipe:apply` / ValidationTest) FAILS: \"active_version … does not match hash of settings\". Never raw-edit versioned Canvas configs; take the hash from a live install and sync every content ref that points at that version."
---

# Canvas Versioned-Config Raw-Edit Trap

**What:** Never `setData()` / `drush cset` / hand-edit a versioned Canvas component config (`canvas.component.sdc.*`) to change its hashed settings. The valid `active_version` hash is computed by Canvas at save time on a **live** install — capture that value and write it into both the component config and every content-template reference that points at the version.

**Rationale:** A Canvas component config carries an `active_version` that is a **hash of the component's settings**. Editing the config's settings directly (to swap a brand string in a `default_value`, say) leaves the stored `active_version` pointing at the OLD hash — the config is now internally inconsistent. The danger is that the inconsistency is **masked**: `drush site:install` and normal runtime don't re-validate the version hash, so the site installs and renders fine and you ship the break. It only surfaces under the **recipe CLI validator** — the `recipe:apply` path exercised by the scaffold's `ValidationTest` — which fails with `active_version c263115f… does not match hash of settings… expected 4997aa29…`. Rollback noise (Linkit/Media uninstall chatter) can bury the real error in STDERR. Because the correct hash can only be produced by letting Canvas recompute it, the fix is: make the change on a live install (or read the validator's "expected" hash), then write that hash into the component config **and** any content reference (e.g. a `person.byline` content-template ref) that must match `active_version`.

**When it applies:** Any time you genericize, patch, or otherwise alter a versioned Canvas component config outside the Canvas UI/API — especially in a `site:export`-produced recipe that will be validated by `recipe:apply` / ValidationTest. Corollary: a value proven to live **outside** the hashed settings (some `default_value` cases) can be patched post-export without breaking the hash — but anything inside the hashed settings must come from a live recompute, never a raw edit.

**Example:**

```text
Raw edit (BROKEN):
  cset canvas.component.sdc.palcera_theme.author-byline settings...  ← desyncs hash
  drush site:install  → PASSES (no hash re-validation)  ← false confidence
  recipe:apply / ValidationTest → FAILS:
    "active_version c263115f… does not match hash of settings… expected 4997aa29…"

Correct:
  1. Change on a live install so Canvas recomputes the hash (or read the "expected" hash).
  2. Write that hash into canvas.component.sdc.<theme>.<component>  active_version.
  3. Sync every content ref (person.byline content-template) to the SAME active_version.
```
