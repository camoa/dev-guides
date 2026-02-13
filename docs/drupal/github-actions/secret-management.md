---
description: Store and use sensitive credentials for GitHub Actions deployments and third-party services
drupal_version: "11.x"
---

# Secret Management

## When to Use

> Use for storing sensitive credentials for deployments, API access, and third-party services.

## Decision

| Situation | Choose | Why |
|-----------|--------|-----|
| SSH keys for deployment | Repository secret `SSH_PRIVATE_KEY` | Secure, encrypted at rest |
| Database credentials | Service container env vars | Temporary, scoped to workflow |
| Environment-specific secrets | Environment secrets | Different values for staging/prod |
| API tokens | Repository secrets with `${{ secrets.NAME }}` | Never logged, can't be extracted |

## Pattern

```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: production
    steps:
      - name: Deploy
        env:
          SSH_KEY: ${{ secrets.SSH_PRIVATE_KEY }}
          API_TOKEN: ${{ secrets.API_TOKEN }}
        run: |
          echo "$SSH_KEY" > ~/.ssh/id_rsa
          chmod 600 ~/.ssh/id_rsa
          ssh-add ~/.ssh/id_rsa
          # Never echo or log secrets
```

## Common Mistakes

- **Wrong**: Echoing secrets in scripts → **Right**: Leaks to logs
- **Wrong**: Hardcoding credentials in workflows → **Right**: Public repo exposure
- **Wrong**: Not using environment secrets → **Right**: Same creds for staging/prod
- **Wrong**: Storing secrets in repository variables → **Right**: Variables are not encrypted

## Security

Never log secrets to output. Use environment secrets for production. Rotate secrets regularly (every 90 days). Use fine-grained PATs instead of classic tokens. Require secret approval for forks.

## Development Standards

Use descriptive secret names (PROD_SSH_KEY vs SSH_KEY). Document required secrets in README. Use separate secrets for each service.

## Anti-patterns

Don't store secrets in environment variables in workflow file (use GitHub Secrets). Don't commit .env files with secrets (use template .env.example instead). Don't share secrets between unrelated repositories (use organization secrets only for shared infrastructure).

## See Also

- Previous: [Parallel Execution](parallel-execution.md)
- Next: [Environment Protection](environment-protection.md)
- Reference: [GitHub Actions secrets](https://docs.github.com/en/actions/security-guides/using-secrets-in-github-actions)
- Reference: [OWASP secrets management](https://owasp.org/www-community/vulnerabilities/Use_of_hard-coded_password)
