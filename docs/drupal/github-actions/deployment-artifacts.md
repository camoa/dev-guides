---
description: Package and upload Drupal builds for deployment to staging or production
drupal_version: "11.x"
---

# Deployment Artifacts

## When to Use

> Use when packaging builds for deployment to staging or production environments.

## Decision

| Situation | Choose | Why |
|-----------|--------|-----|
| Share build between jobs | `actions/upload-artifact@v4` | Avoids rebuilding for deployment job |
| Exclude dev files | Selective copy with tar | Smaller artifact, faster deploys |
| Version artifacts | Include git SHA in name | Traceable deployments |
| Long-term storage | External artifact store | GitHub artifacts expire after 90 days |

## Pattern

```yaml
- name: Create artifact
  run: |
    mkdir -p build
    cp -r web vendor composer.json composer.lock build/
    rm -rf build/web/sites/default/files
    rm -rf build/web/core/tests
    tar -czf build.tar.gz -C build .

- uses: actions/upload-artifact@v4
  with:
    name: deployment-${{ github.sha }}
    path: build.tar.gz
    retention-days: 30

# In deployment job:
- uses: actions/download-artifact@v4
  with:
    name: deployment-${{ github.sha }}
```

## Common Mistakes

- **Wrong**: Including vendor-dev dependencies → **Right**: Bloated artifact with dev tools
- **Wrong**: Not excluding sites/default/files → **Right**: Overwrites uploaded media
- **Wrong**: Uploading artifacts on every build → **Right**: Wastes storage, costs money
- **Wrong**: Missing .gitattributes exclusions → **Right**: Large artifact with git metadata

## Security

Never include .env files or credentials. Scan artifacts for secrets before upload. Use separate artifacts for different environments.

## Performance

Compress with tar -czf for smaller uploads. Use artifact retention policies (7-30 days). Upload only on main branch or tagged releases.

## Anti-patterns

Don't upload artifacts from failed builds (pollutes artifact list). Don't upload the entire repo (use selective copy).

## See Also

- Previous: [Theme Asset Compilation](theme-asset-compilation.md)
- Next: [Multi-Environment Deployment](multi-environment-deployment.md)
- Reference: [GitHub Actions artifacts](https://docs.github.com/en/actions/using-workflows/storing-workflow-data-as-artifacts)
