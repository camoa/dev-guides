---
description: "Apply a pre-release fix with cweagans/composer-patches, and know whether a failed patch stops the build on 1.x or 2.x."
tldr: "Use cweagans/composer-patches to apply a fix to core or a contrib package before its maintainer releases it. Read its output on every run, because the 1.x line skips a failed patch and Composer still succeeds."
drupal_version: "10.x, 11.x"
---

# Composer: Patches

## When to Use

Use `cweagans/composer-patches` to apply a fix to core or a contrib package before its maintainer releases it. Read its output on every run, because the 1.x line skips a failed patch and Composer still succeeds.

## Decision

| If you need... | Use... | Why |
|---|---|---|
| To know whether a failed patch stops Composer | Check the plugin's major in `composer.lock` | 1.x skips and continues; 2.x throws |
| 1.x to stop on a failed patch | `extra.composer-exit-on-patch-failure: true` | Turns the skip into an exception |
| A patch from a drupal.org merge request | Download the diff into the repository, point at the local path | A merge request URL changes when someone pushes to it |
| To track why each patch exists | An inventory: source, date, reason, issue | A patch with no known source cannot be retired |
| 2.x to pick up a patch change | `composer patches-relock`, then `composer patches-repatch` | 2.x reads `patches.lock.json`, not `composer.json`, once it exists |

## Pattern

```json
{
  "extra": {
    "composer-exit-on-patch-failure": true,
    "patches": {
      "drupal/core": {
        "#3110362: Keep config changed by update hooks (MR !123, 2026-09-01)": "patches/core-3110362-mr123.diff"
      }
    }
  }
}
```

The key is the description, and it doubles as the inventory: issue, source, date. The value is a path relative to the project root.

**Reference:** composer-patches 1.x `src/Patches.php` (tag 1.7.3); [Defining patches](https://docs.cweagans.net/composer-patches/usage/defining-patches/); [Recommended workflows](https://docs.cweagans.net/composer-patches/usage/recommended-workflows/)

## How the Two Majors Behave

| Behavior | 1.x (1.7.3) | 2.x (2.0.0) |
|---|---|---|
| A patch fails | Prints `Could not apply patch! Skipping. The error was: …` and continues; the command succeeds | Throws `No available patcher was able to apply patch <url> to <package>`; the command fails |
| Stop on failure | `extra.composer-exit-on-patch-failure: true`, or `COMPOSER_EXIT_ON_PATCH_FAILURE` in the environment | Always |
| Record of patches | `PATCHES.txt` and `patches_applied` written into the installed package; no lock file | `patches.lock.json`, committed with `composer.lock` |
| Adding a patch | Edit the definition; it applies when the package is next installed | Edit the definition, `composer patches-relock`, `composer patches-repatch` |
| How it applies | `git apply`, then `patch`, at depths `-p1`, `-p0`, `-p2`, `-p4` | Patcher plugins; no option skips a failure |

2.0.0 was released on 2025-10-30. Drupal core issue #3564942 asked whether 2.x works with Drupal. It closed as a support request: the reporter's patches lacked the `a/` and `b/` path prefixes, and the 2.x configuration differs from 1.x. Nothing in core blocks 2.x. Moving from 1.x to 2.x is a configuration change, so treat it as its own change.

## Opinion: Snapshot Every Remote Patch

The plugin's own documentation warns that a pull request or merge request patch changes when someone pushes to it, and that a malicious user could use that to deploy code you did not review. A drupal.org merge request `.diff` URL is that case. Download the file, commit it under `patches/`, and name the merge request and the date in the description. The build then applies exactly what you reviewed.

## Common Mistakes

- Trusting exit 0 on a 1.x project → Search the output for `Could not apply patch`, or set `composer-exit-on-patch-failure`
- Pointing at a merge request URL → Commit a local copy; the remote content moves
- A patch description of "fix" → Name the issue, the source and the date; that is how you know when to drop it
- Keeping a patch after the fix ships → The patch usually fails against the new release. On 1.x it is skipped silently. Check each patch's issue on every update
- Upgrading to 2.x without relocking → Run `patches-relock` and commit `patches.lock.json`, or teammates apply a different set
- A patch without `a/` and `b/` prefixes on 2.x → Regenerate it with `git diff`

## See Also

- [Composer: Update vs Require](composer-update-vs-require.md) — a patch reapplies whenever its package moves
- [Composer: Resolution Conflicts](composer-conflicts.md) — one failure at a time applies to patches too
- Recipe: [`drupal_dependency_update`](../../agentic-recipes/drupal/dependency-update.md) — a failed patch is a stopping point
- Reference: [Composer Patches commands](https://docs.cweagans.net/composer-patches/usage/commands/)
