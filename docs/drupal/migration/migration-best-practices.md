---
description: Critical success factors and patterns from community migration experience
drupal_version: "11.x"
---

# Migration Best Practices

## When to Use

Follow these patterns to avoid common migration pitfalls. Based on community experience migrating hundreds of D7 sites.

## Critical Success Factors

**1. Treat as rebuild, not upgrade**
- D7→D11 requires architectural rethinking
- Budget for complete custom code rewrites (unless using Retrofit)
- Opportunity to improve UX and clean up technical debt

**2. Complete assessment before coding**
- Full inventory prevents mid-migration surprises
- Identify contrib replacements for custom functionality
- Document integration requirements early

**3. Test incrementally throughout**
- Small batch migrations reveal issues early
- Iterative testing reduces production risk
- Always test rollback capability

**4. Follow dependency order strictly**
- Users → Taxonomy → Files → Paragraphs → Nodes
- Respect migration_dependencies in YAML
- Test each layer before moving to next

**5. Monitor and log everything**
- Use --feedback flag for progress visibility
- Check migrate_message_* tables for failures
- Log custom transformations for debugging

## Pattern

**Migration project timeline (medium complexity site):**

```
Month 1-2: Assessment & Planning
- Content inventory and architecture mapping
- Custom module audit and rewrite planning
- Migration approach decision
- Development environment setup

Month 3-4: Configuration & Dependencies
- D11 site configuration (content types, fields)
- User migration
- Taxonomy migration
- File/media migration

Month 5-6: Content Migration
- Paragraph migrations
- Node migrations by content type
- Menu and URL alias migrations
- Relationship validation

Month 7-8: Testing & Optimization
- Full staging migration
- Performance optimization
- Security audit
- UAT with stakeholders

Month 9: Production Cutover
- Final incremental migration
- DNS cutover
- Post-launch monitoring
```

## Common Mistakes

- **Wrong**: Underestimating timeline → **Right**: D7→D11 takes months, not weeks
- **Wrong**: Skipping assessment phase → **Right**: Leads to mid-migration scope changes
- **Wrong**: Testing only at the end → **Right**: Compound failures hard to debug
- **Wrong**: Ignoring custom code modernization → **Right**: Technical debt accumulates
- **Wrong**: Inadequate backup strategy → **Right**: Can't roll back if issues found
- **Wrong**: Migrating unused content → **Right**: Increases complexity unnecessarily
- **Wrong**: Attempting complex migrations solo → **Right**: Requires team collaboration

## See Also

- Reference: [Planning successful Drupal migration](https://www.valuebound.com/resources/blog/planning-successful-drupal-migration-key-steps-and-best-practices)
- Reference: [Risk-free D7 to D11 strategies](https://www.valuebound.com/blog/risk-free-drupal-7-11-migration-strategies-work)
