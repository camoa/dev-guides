---
description: Deploy Drupal to staging, production, or multiple hosting environments with approval gates
drupal_version: "11.x"
---

# Multi-Environment Deployment

## When to Use

> Use when deploying to staging, production, or multiple hosting environments with different requirements.

## Decision

| Situation | Choose | Why |
|-----------|--------|-----|
| Automatic staging deploys | `on: push` to main | Fast feedback, continuous staging updates |
| Production approval gate | `workflow_dispatch` + environment protection | Human approval before production |
| Environment-specific secrets | Environment secrets | Different credentials per environment |
| Rollback capability | Tag-based deployments | Can redeploy previous versions |

## Pattern

```yaml
on:
  workflow_dispatch:
    inputs:
      environment:
        type: choice
        options: ['staging', 'production']
        required: true

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: ${{ github.event.inputs.environment }}
    steps:
      - uses: actions/download-artifact@v4
        with:
          name: deployment-${{ github.sha }}

      - name: Deploy
        env:
          SSH_KEY: ${{ secrets.SSH_PRIVATE_KEY }}
          HOST: ${{ secrets.DEPLOY_HOST }}
        run: |
          mkdir -p ~/.ssh
          echo "$SSH_KEY" > ~/.ssh/id_rsa
          chmod 600 ~/.ssh/id_rsa
          scp build.tar.gz $HOST:/var/www/
          ssh $HOST "cd /var/www && tar -xzf build.tar.gz"

      - name: Post-deploy
        run: |
          ssh $HOST "cd /var/www && \
            ./vendor/bin/drush updatedb --yes && \
            ./vendor/bin/drush config:import --yes && \
            ./vendor/bin/drush cache:rebuild"
```

## Common Mistakes

- **Wrong**: Deploying on every commit to main → **Right**: Breaks production without approval
- **Wrong**: Not running database updates → **Right**: Config import fails, site breaks
- **Wrong**: Skipping cache rebuild → **Right**: Old cached pages served
- **Wrong**: Using same secrets for all environments → **Right**: Staging creds leak to production

## Security

Require manual approval for production. Use environment protection rules. Rotate SSH keys regularly. Never log secrets to output.

## Performance

Deploy staging automatically for fast iteration. Use blue-green deployments for zero-downtime. Cache drush/composer on target server.

## Development Standards

Run drush updatedb before config:import. Test deployment script in staging first. Use idempotent deployment steps. Implement health checks after deploy.

## Anti-patterns

Don't run drush cr before config:import (can cause import failures). Don't skip updatedb (database schema mismatches). Don't deploy without testing artifact in staging first.

## See Also

- Previous: [Deployment Artifacts](deployment-artifacts.md)
- Next: [Caching Strategies](caching-strategies.md)
- Reference: [GitHub environments](https://docs.github.com/en/actions/deployment/targeting-different-environments/using-environments-for-deployment)
- Reference: [Drupal deployment best practices](https://drupalodyssey.com/blog/development/streamlining-drupal-deployments-using-drush-and-github-actions-cicd)
