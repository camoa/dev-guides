---
description: Measure code coverage with PCOV or Xdebug, set coverage targets by code type, and avoid coverage anti-patterns.
---

# Coverage Metrics Strategy

## When to Use
Measuring how much of your code is executed during tests, identifying untested code paths, setting coverage targets for CI/CD.

## Decision: PCOV vs Xdebug

| Criteria | PCOV | Xdebug |
|---|---|---|
| **Speed** | 2-5x faster (15s vs 50s for typical suite) | Slower but acceptable for thorough analysis |
| **Coverage types** | Line coverage ONLY | Line, branch, path, function coverage |
| **Setup complexity** | Simple (single PHP extension) | Moderate (configure modes) |
| **Maintenance status** | Not actively maintained (last release 2021) | Actively developed, well-supported |
| **PHP 8.4+ compatibility** | Requires patches | Native support |
| **Use case** | Daily dev workflow, CI line coverage | Deep analysis, branch/path coverage |

**Recommendation**: Use **PCOV for fast feedback** in development and CI/CD (line coverage is 90% of value). Use **Xdebug when branch/path coverage matters** (security-critical code, complex conditionals). For projects targeting PHP 8.4+, prefer Xdebug due to PCOV maintenance concerns.

## Coverage Types Explained

| Type | What it measures | Example | Why it matters |
|---|---|---|---|
| **Line coverage** | % of executable lines run | 50 lines total, 40 executed = 80% | Quick indicator of test breadth |
| **Branch coverage** | % of conditional branches taken | `if ($x) { A } else { B }` -- both A and B executed? | Finds untested edge cases |
| **Path coverage** | % of unique execution paths | Function with 3 ifs = 8 possible paths | Ensures all combinations tested |
| **Function coverage** | % of functions/methods called | 10 methods, 8 called = 80% | Identifies dead code |

**Line coverage** is the baseline -- fast to collect, easy to understand. **Branch coverage** catches the "happy path only" problem. **Path coverage** is expensive but critical for security-sensitive code. **Function coverage** is a sanity check (0% = completely untested class).

## Pattern

**Installing PCOV** (DDEV example):
```bash
# In .ddev/config.yaml
webimage_extra_packages: [php-pcov]

# Or manually
ddev exec sudo apt-get install php-pcov
ddev exec sudo phpenmod pcov
ddev restart
```

**Installing Xdebug** (DDEV includes it by default):
```bash
ddev xdebug on  # Enable Xdebug in coverage mode
```

**Running PHPUnit with line coverage** (PCOV or Xdebug):
```bash
# HTML report (open reports/index.html in browser)
./vendor/bin/phpunit --coverage-html reports/

# Clover XML (for CI/CD tools like GitLab, SonarQube)
./vendor/bin/phpunit --coverage-clover coverage.xml

# Text report (terminal output)
./vendor/bin/phpunit --coverage-text

# Filter to specific directory
./vendor/bin/phpunit --coverage-html reports/ web/modules/custom/my_module/
```

**Running PHPUnit with branch/path coverage** (Xdebug only):
```bash
# Requires Xdebug 3.1+
XDEBUG_MODE=coverage ./vendor/bin/phpunit \
  --coverage-html reports/ \
  --path-coverage
```

**Interpreting coverage reports**:
```
Code Coverage Report:
  Classes: 85.00% (17/20)
  Methods: 78.57% (22/28)
  Lines:   82.35% (140/170)

MyService.php
  Lines: 92.31% (12/13) -- GOOD
  Untested line 45: Exception handler

DiscountCalculator.php
  Lines: 50.00% (5/10) -- NEEDS WORK
  Untested lines 20-24: Edge case validation
```

**Coverage in CI/CD** (GitLab CI example):
```yaml
test:
  script:
    - composer install
    - ./vendor/bin/phpunit --coverage-text --colors=never
  coverage: '/^\s*Lines:\s*\d+.\d+\%/'
  artifacts:
    reports:
      coverage_report:
        coverage_format: cobertura
        path: coverage.xml
```

## Coverage Targets by Code Type

| Code type | Target coverage | Rationale |
|---|---|---|
| **Services (business logic)** | 80-90% | High reuse, critical to functionality |
| **Plugins (blocks, formatters)** | 70-85% | Well-defined contracts, moderate complexity |
| **Controllers** | 60-75% | HTTP overhead, test logic not routing |
| **Forms (validation/submit)** | 50-70% | Setup expensive, focus on custom logic |
| **Hooks/event subscribers** | 60-80% | Integration points, side effects matter |
| **Entity classes (custom)** | 70-85% | Data integrity critical |
| **Utility classes** | 90%+ | Pure functions, easy to test thoroughly |
| **Admin UI / config forms** | 30-50% | Mostly CRUD, low custom logic |

**Why 100% is a waste**: Chasing 100% coverage leads to testing trivial getters/setters, framework code, and defensive branches that never execute. **Meaningful coverage** tests behavior, not code structure.

## Common Coverage Anti-Patterns

- **Testing getters/setters** -- 100% line coverage, 0% value (trivial code)
- **Covering dead branches** -- `if (FALSE) { unreachable }` counts toward coverage but tests nothing
- **Ignoring branch coverage** -- 80% line coverage but only "happy path" tested, failures uncaught
- **Coverage theater** -- hitting lines without asserting behavior (test runs code but verifies nothing)
- **Excluding too much** -- `--coverage-exclude` hides real gaps instead of writing tests
- **Coverage targets without context** -- 80% of what? If 80% excludes all security checks, target is meaningless

## See Also
- [Running Tests](running-tests.md)
- [Quality Gates & Audit Checklist](quality-gates-audit-checklist.md)
- [PCOV or Xdebug? | The PHP Consulting Company](https://thephp.cc/articles/pcov-or-xdebug)
- [Code Coverage -- PHPUnit Manual](https://docs.phpunit.de/en/10.5/code-coverage.html)
