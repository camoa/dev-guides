---
description: Build Sass, JavaScript, and optimize assets for Drupal themes in CI/CD pipelines
drupal_version: "11.x"
---

# Theme Asset Compilation

## When to Use

> Use when building Sass, JavaScript, and optimizing assets for Drupal themes in automated workflows.

## Decision

| Situation | Choose | Why |
|-----------|--------|-----|
| Sass compilation | `npm run build` with Dart Sass | Modern, maintained, supports latest CSS features |
| JavaScript bundling | Webpack or Rollup | Tree-shaking, code splitting, production optimization |
| Asset optimization | imagemin, svgo, cssnano | Reduces payload size, improves performance |
| CSS purging | PurgeCSS | Removes unused Bootstrap/framework classes |
| Critical CSS | critical package | Inline above-fold CSS for fast render |

## Pattern

```yaml
- uses: actions/setup-node@v4
  with:
    node-version: '18'
    cache: 'npm'
    cache-dependency-path: 'themes/custom/*/package-lock.json'

- name: Build theme
  run: |
    cd themes/custom/my_theme
    npm ci --prefer-offline
    npm run build:prod
    npm run optimize
```

Example package.json scripts:
```json
{
  "scripts": {
    "build:prod": "webpack --mode production",
    "sass:build": "sass src/scss:dist/css --style compressed",
    "optimize": "imagemin src/images/* --out-dir=dist/images"
  }
}
```

## Common Mistakes

- **Wrong**: Using `npm install` instead of `npm ci` → **Right**: Non-deterministic builds
- **Wrong**: Not caching npm dependencies → **Right**: Slow builds
- **Wrong**: Committing compiled assets → **Right**: Merge conflicts, bloated repo
- **Wrong**: Using outdated node-sass → **Right**: Deprecated, use Dart Sass

## Performance

Use production mode for webpack. Enable tree-shaking. Minify CSS/JS. Compress images before committing (don't rely on build-time optimization for checked-in assets).

## Development Standards

Lint Sass and JavaScript before build. Use .nvmrc for consistent Node versions. Pin dependency versions in package-lock.json.

## Anti-patterns

Never use `npm audit fix` in CI (can introduce breaking changes). Don't skip linting in production builds (catches issues before deployment).

## See Also

- Previous: [PHPUnit Testing](phpunit-testing.md)
- Next: [Deployment Artifacts](deployment-artifacts.md)
- Reference: [Bootstrap theme compilation](https://getbootstrap.com/docs/5.3/customize/sass/)
