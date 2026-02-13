---
description: Add approval gates, wait timers, and validation for production deployments
drupal_version: "11.x"
---

# Environment Protection

## When to Use

> Use when adding approval gates and validation for production deployments to prevent accidental releases.

## Decision

| Situation | Choose | Why |
|-----------|--------|-----|
| Manual production approval | Environment protection rules | Prevents accidental production deploys |
| Wait timer before deploy | Environment wait timer | Grace period to cancel deployments |
| Required reviewers | Environment required reviewers | Team oversight for critical changes |
| Branch restrictions | Environment deployment branches | Only main/release can deploy to prod |

## Pattern

In GitHub repository settings → Environments → Create "production":
- Required reviewers: Select team members
- Wait timer: 5 minutes
- Deployment branches: Only main

```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    environment:
      name: production
      url: https://example.com
    steps:
      - name: Validate environment
        run: |
          if [[ "${{ github.event.inputs.environment }}" == "production" ]]; then
            if [[ "${{ github.ref }}" != "refs/heads/main" ]]; then
              echo "Production deploys only from main"
              exit 1
            fi
          fi

      - name: Deploy
        run: [deployment steps]
```

## Common Mistakes

- **Wrong**: Not configuring environment protection → **Right**: Accidental production deploys
- **Wrong**: Skipping validation in workflow → **Right**: Protection rules bypassed
- **Wrong**: Using same environment name for staging/prod → **Right**: Approval gates on staging
- **Wrong**: Not documenting approval process → **Right**: Team confusion

## Security

Require 2+ approvers for production. Use branch protection rules in addition to environment protection. Log all production deployments. Implement rollback workflow with same approval process.

## Development Standards

Use descriptive environment names (production, staging-us-east, dev). Set environment URLs for quick access. Document required secrets per environment in README.

## Anti-patterns

Don't skip approval for "hotfix" deployments (create fast-track approval process instead). Don't use admin override regularly (defeats purpose of protection). Don't configure protection without team buy-in (will be disabled when inconvenient).

## See Also

- Previous: [Secret Management](secret-management.md)
- Next: [Troubleshooting](troubleshooting.md)
- Reference: [GitHub environment protection](https://docs.github.com/en/actions/deployment/targeting-different-environments/using-environments-for-deployment#environment-protection-rules)
