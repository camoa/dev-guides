---
description: Always check whether a Drush command exists for the operation before reaching for `drush php:eval`, `drush php:script`, or `drush sql:query`. `php:eval` is the fallback for genuinely missing commands, not the default.
drupal_version: "11.x"
tldr: Always check whether a Drush command exists for the operation before reaching for `drush php:eval`, `drush php:script`, or `drush sql:query`. `php:eval` is the fallback for genuinely missing commands, not the default.
---

# Use Drush Commands Before php:eval

**What:** Always check whether a Drush command exists for the operation before reaching for `drush php:eval`, `drush php:script`, `drush sql:query`, or hand-written PHP. `php:eval` is the fallback for genuinely missing commands, not the default.

**Rationale:** Built-in Drush commands are tested, idempotent, support standard flags (`--yes`, `--simulate`, `--uri`, `--debug`, `--root`), produce structured output (`--format=json|yaml|csv|table`), integrate with `drush help` and tab completion, and document themselves. `php:eval` bypasses all of that — no help text, no idempotency guarantees, no flags, no shell-quoting safety. Worse, php-eval snippets tend to accumulate as copy-paste artifacts in deploy scripts and READMEs, drifting from current API patterns and hiding bugs (missing cache invalidation, missing dependency resolution, wrong service IDs after refactors).

**When it applies:** Every time you're about to type `drush php:eval`, `drush ev`, `drush php:script`, or `drush scr`. First run `drush list | grep <topic>` for an existing command. Common areas where Drush already provides what you need: users, roles, permissions, modules, themes, config, cache, queues, cron, locale, migration, watchdog, state, search-index, file-system, sql.

**Example:**

```bash
# Wrong — reinvents what Drush provides
drush php:eval "User::create(['name'=>'alice','mail'=>'a@b.com','status'=>1])->save();"

# Right
drush user:create alice --mail=a@b.com
drush user:unblock alice

# Wrong — bypasses module installer, may skip dependencies + cache
drush php:eval "\Drupal::service('module_installer')->install(['my_module']);"

# Right
drush pm:install my_module --yes

# Wrong — manual config import skips validation
drush php:eval "\Drupal::configFactory()->getEditable('system.site')->set('name','New')->save();"

# Right
drush config:set system.site name 'New' --yes

# Wrong — manual queue draining
drush php:eval "while(\$item = \Drupal::queue('my_q')->claimItem()){ /* ... */ }"

# Right
drush queue:run my_q

# Wrong — invents cache rebuild logic
drush php:eval "drupal_flush_all_caches();"

# Right
drush cache:rebuild

# Acceptable php:eval — genuinely no Drush command exists
drush php:eval "echo \Drupal::service('my_module.diagnostics')->snapshot();"
```

When you DO need `php:eval` (no Drush equivalent exists), prefer `php:script` with a versioned `.php` file in the repo over inline strings — it's reviewable, diffable, testable, and survives shell-quoting hell.
