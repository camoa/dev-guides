---
description: Set up automated quality gates at pre-commit, pre-push, and CI/CD stages with GrumPHP, PHPStan, and PHPCS.
---

# Quality Gates & Audit Checklist

## When to Use
Establishing automated quality checks at different stages of development to catch issues early, enforce standards, and prevent broken code from reaching production.

## Decision Framework

| Stage | Gate type | Checks | Speed target | Failure action |
|---|---|---|---|---|
| **Pre-commit** | Local, fast | Code style (PHPCS), basic static analysis | <30 seconds | Block commit, show errors |
| **Pre-push** | Local, thorough | Unit + kernel tests, coverage threshold | <2 minutes | Block push, run fixes |
| **Pre-merge (CI)** | Remote, complete | Full test suite, security audit, coverage report | <10 minutes | Block merge, require fixes |
| **Post-merge** | Monitoring | Integration tests, deployment checks | Varies | Alert team, auto-rollback |

**Principle**: Fast feedback loops -- cheap to fix. Slow gates (browser tests, full coverage) run in CI, not locally.

## Pattern

**Pre-commit gates** (fastest, catches obvious errors):

Using **GrumPHP** (recommended for Drupal):
```yaml
# grumphp.yml
grumphp:
  tasks:
    phplint: ~
    phpcs:
      standard: Drupal,DrupalPractice
      triggered_by: [php, module, inc, install, theme]
    phpstan:
      level: 6
      configuration: phpstan.neon

  testsuites:
    pre_commit:
      tasks:
        - phplint
        - phpcs
        - phpstan
```

Install: `composer require --dev phpro/grumphp`

**Manual pre-commit hook** (`.git/hooks/pre-commit`):
```bash
#!/bin/bash

# Get staged PHP files
FILES=$(git diff --cached --name-only --diff-filter=ACM | grep -E '\.(php|module|install|theme)$')

if [ -z "$FILES" ]; then
  exit 0
fi

# PHPCS check
echo "Running PHPCS..."
./vendor/bin/phpcs --standard=Drupal,DrupalPractice $FILES
if [ $? -ne 0 ]; then
  echo "PHPCS failed. Run phpcbf to auto-fix or fix manually."
  exit 1
fi

# PHPStan check (level 6 minimum)
echo "Running PHPStan..."
./vendor/bin/phpstan analyse --level=6 $FILES
if [ $? -ne 0 ]; then
  echo "PHPStan failed. Fix errors before committing."
  exit 1
fi

exit 0
```

Make executable: `chmod +x .git/hooks/pre-commit`

**Pre-push gates** (slower, catches logic errors):

`.git/hooks/pre-push`:
```bash
#!/bin/bash

echo "Running unit and kernel tests..."
./vendor/bin/phpunit --testsuite unit,kernel --stop-on-failure

if [ $? -ne 0 ]; then
  echo "Tests failed. Fix before pushing."
  exit 1
fi

# Optional: Check coverage threshold
echo "Checking coverage threshold..."
COVERAGE=$(./vendor/bin/phpunit --coverage-text --colors=never | grep -oP 'Lines:\s+\K\d+')
if [ "$COVERAGE" -lt 70 ]; then
  echo "Coverage is $COVERAGE%, minimum is 70%"
  exit 1
fi

exit 0
```

**Composer scripts** (standardized commands):
```json
{
  "scripts": {
    "lint": "parallel-lint web/modules/custom web/themes/custom",
    "phpcs": "phpcs --standard=Drupal,DrupalPractice web/modules/custom",
    "phpcbf": "phpcbf --standard=Drupal,DrupalPractice web/modules/custom",
    "phpstan": "phpstan analyse --level=6 web/modules/custom",
    "test:unit": "phpunit --testsuite unit",
    "test:kernel": "phpunit --testsuite kernel",
    "test:all": "phpunit",
    "coverage": "phpunit --coverage-html reports/",
    "quality": [
      "@lint",
      "@phpcs",
      "@phpstan",
      "@test:unit",
      "@test:kernel"
    ]
  }
}
```

Run: `composer quality` before pushing.

**CI/CD pipeline stages** (GitLab CI example):
```yaml
stages:
  - lint
  - static-analysis
  - test
  - coverage
  - security

# Stage 1: Lint (30 seconds)
lint:
  stage: lint
  script:
    - composer lint
    - composer phpcs

# Stage 2: Static analysis (1-2 minutes)
phpstan:
  stage: static-analysis
  script:
    - composer phpstan

# Stage 3: Tests (2-5 minutes)
unit-tests:
  stage: test
  script:
    - ./vendor/bin/phpunit --testsuite unit

kernel-tests:
  stage: test
  script:
    - ./vendor/bin/phpunit --testsuite kernel

functional-tests:
  stage: test
  script:
    - ./vendor/bin/phpunit --testsuite functional
  timeout: 30m

# Stage 4: Coverage (3-5 minutes)
coverage:
  stage: coverage
  script:
    - ./vendor/bin/phpunit --coverage-text --coverage-cobertura=coverage.xml
  coverage: '/^\s*Lines:\s*\d+.\d+\%/'
  artifacts:
    reports:
      coverage_report:
        coverage_format: cobertura
        path: coverage.xml

# Stage 5: Security (1 minute)
security:
  stage: security
  script:
    - composer audit
    - ./vendor/bin/phpstan analyse --level=6 --error-format=json | jq '.totals.errors'
  allow_failure: false
```

**GitHub Actions** (alternative):
```yaml
name: Quality Gates

on: [push, pull_request]

jobs:
  lint-and-static:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: shivammathur/setup-php@v2
        with:
          php-version: 8.3
          extensions: pcov
      - run: composer install
      - run: composer lint
      - run: composer phpcs
      - run: composer phpstan

  tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: shivammathur/setup-php@v2
        with:
          php-version: 8.3
          extensions: pcov
      - run: composer install
      - run: ./vendor/bin/phpunit --testsuite unit,kernel --coverage-clover coverage.xml
      - uses: codecov/codecov-action@v3
        with:
          files: ./coverage.xml
```

## Issue Triage from Quality Gate Failures

| Failure type | Severity | Response time | Fix approach |
|---|---|---|---|
| **PHPCS (code style)** | Low | Fix before commit | Run `phpcbf` to auto-fix |
| **PHPStan level 6+ errors** | High | Fix before push | Address type errors, null checks |
| **Unit test failures** | Critical | Fix immediately | Logic error, refactor code |
| **Kernel test failures** | Critical | Fix immediately | Integration issue, check setup |
| **Browser test failures** | High | Investigate within 1 hour | May be flaky, re-run; if persistent, fix |
| **Coverage drop >5%** | Medium | Investigate before merge | Add tests for new code |
| **Security audit failures** | Critical | Fix immediately | Update dependencies, patch CVEs |

**Flaky test protocol**: If browser/JS test fails intermittently:
1. Re-run 3 times
2. If 2/3 pass -- investigate but don't block merge
3. If 0/3 or 1/3 pass -- block merge, fix test or code
4. Tag test with `@group flaky` temporarily, create issue to fix

## Common Mistakes

- **All gates at pre-commit** -- slow feedback (30+ seconds per commit), developers disable hooks
- **No gates until CI** -- waste CI resources on trivial errors, slow feedback loop
- **Brittle coverage thresholds** -- 80% coverage requirement blocks legitimate refactoring that temporarily lowers coverage
- **Ignoring gate failures** -- "I'll fix it later" -- technical debt accumulates
- **Testing in CI without local testing first** -- waste CI minutes, clog pipeline
- **Not using `--stop-on-failure`** -- run full suite even after first failure, slow debug loop
- **No composer scripts** -- every developer runs checks differently, inconsistent

## See Also
- [Coverage Metrics Strategy](coverage-metrics-strategy.md)
- [Best Practices & Patterns](best-practices-patterns.md)
- [Git hooks to improve code quality | Medium](https://aicha-fatrah.medium.com/git-hooks-to-improve-code-quality-grumphp-phpcs-phpcpd-and-phpstan-5129b41b94b5)
- [GitHub Actions workflows for PHP CI/CD](https://zuniweb.com/blog/github-actions-workflows-for-php-ci/cd-with-composer-phpstan-and-deployment/)
