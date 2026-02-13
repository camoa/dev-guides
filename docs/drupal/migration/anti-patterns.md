---
description: Common migration failures that cause project delays and technical debt
drupal_version: "11.x"
---

# Anti-Patterns to Avoid

## When to Use

Learn from common migration failures. These patterns consistently cause project delays, cost overruns, and technical debt.

## Anti-Patterns

**1. The "Big Bang" Migration**
- **What**: Attempt to migrate everything at once on launch day
- **Why it fails**: No incremental testing, all failures discovered in production
- **Instead**: Migrate in phases, test each component, final incremental sync

**2. The "Copy-Paste Code Port"**
- **What**: Copy D7 .module files to D11, try to make them work
- **Why it fails**: D7 hooks/APIs completely different, causes fatal errors
- **Instead**: Rewrite using D11 patterns (plugins, services, event subscribers)

**3. The "No Rollback Plan"**
- **What**: Migrate production without tested rollback procedure
- **Why it fails**: Issues found post-launch can't be undone quickly
- **Instead**: Test rollback on staging, keep D7 site running during migration window

**4. The "Migrate Everything" Approach**
- **What**: Attempt to migrate all content including obsolete pages
- **Why it fails**: Wastes time on unused content, increases migration complexity
- **Instead**: Audit content, retire outdated material, migrate only active content

**5. The "Settings.php Credentials"**
- **What**: Hardcode database passwords in settings.php committed to Git
- **Why it fails**: Security vulnerability, credentials exposed in version control
- **Instead**: Use environment variables, settings.local.php excluded from Git

**6. The "No Dependency Order"**
- **What**: Migrate nodes before users/taxonomy/files they reference
- **Why it fails**: Migration lookups fail, broken references, orphaned content
- **Instead**: Always follow dependency chain: users → taxonomy → files → paragraphs → nodes

**7. The "Full HTML Migration"**
- **What**: Migrate D7 content with Full HTML text format preserved
- **Why it fails**: XSS vulnerabilities, deprecated/malicious code executed
- **Instead**: Use restrictive formats (basic_html), sanitize during migration

**8. The "Solo Developer Migration"**
- **What**: One person handles entire complex migration alone
- **Why it fails**: Knowledge silos, no code review, burnout, delays
- **Instead**: Team approach - frontend, backend, content editors collaborate

**9. The "No Testing Until Production"**
- **What**: Skip staging migrations, test directly on live site
- **Why it fails**: Data corruption, downtime, public-facing errors
- **Instead**: Multiple staging migrations, UAT, performance testing before production

**10. The "Retrofit Forever"**
- **What**: Use Retrofit as permanent solution, never modernize D7 code
- **Why it fails**: Accumulates technical debt, harder to maintain over time
- **Instead**: Retrofit as bridge, schedule modernization sprints post-launch

## See Also

- [Migration best practices](migration-best-practices.md) for correct patterns
- Reference: [Drupal 7 migration challenges](https://www.skynettechnologies.com/blog/drupal-7-to-11-migration-key-checklist-and-challenges)
